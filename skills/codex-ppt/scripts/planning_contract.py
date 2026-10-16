"""Approved semantic projections and shared managed-workflow gates."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any


class ContractError(ValueError):
    pass


def digest(value: Any) -> str:
    try:
        raw = json.dumps(
            value, sort_keys=True, ensure_ascii=False,
            separators=(",", ":"), allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ContractError("Contract must contain finite JSON values") from exc
    return hashlib.sha256(raw).hexdigest()


def file_digest(path: Path) -> str:
    if not path.is_file():
        raise ContractError(f"Required asset missing: {path}")
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def slide_id(slide: dict) -> str:
    return f"slide_{slide['number']:02d}"


def dependency_closure(owner: str, slides: dict[str, dict]) -> list[str]:
    seen: set[str] = set()
    pending = list(slides[owner].get("depends_on", []))
    while pending:
        current = pending.pop()
        if current not in slides:
            raise ContractError(f"Unknown dependency: {current}")
        if current == owner or current in seen:
            continue
        seen.add(current)
        pending.extend(slides[current].get("depends_on", []))
    return sorted(seen)


def source_path(declared: str, base: Path) -> Path:
    path = Path(declared).expanduser()
    return (path if path.is_absolute() else base / path).resolve()


def normalize_asset_paths(spec: dict, draft_root: Path) -> tuple[dict, list[dict]]:
    """No writes: freeze original path meaning before displaying/approving a draft."""
    normalized = copy.deepcopy(spec)
    provenance = []
    base = draft_root.resolve()

    def resolve(entry: dict, key: str, field: str) -> None:
        declared = entry[key]
        path = source_path(declared, base)
        sha = file_digest(path)  # A missing asset refuses the whole candidate.
        provenance.append({
            "field": field, "declared_path": declared,
            "draft_root": base.as_posix(), "source_path": path.as_posix(),
            "sha256": sha,
        })
        entry[key] = path.as_posix()

    for slide in normalized["slides"]:
        for index, image in enumerate(slide["required_images"]):
            resolve(image, "path", f"{slide_id(slide)}.required_images[{index}]")
    for key, value in sorted(normalized["planning"]["shared_visuals"].items()):
        if value.get("asset_path"):
            resolve(value, "asset_path", f"shared_visuals.{key}.asset_path")
    return normalized, provenance


def asset_entries(entries: list[dict], base: Path) -> list[dict]:
    return [
        {
            "path": source_path(entry["path"], base).as_posix(),
            "sha256": file_digest(source_path(entry["path"], base)),
            "role": entry.get("role"), "fidelity": entry.get("fidelity"),
        }
        for entry in entries
    ]


def build_contexts(spec: dict, base: Path) -> tuple[dict, dict, dict]:
    validate_spec(spec)
    spec, _ = normalize_asset_paths(spec, base)
    planning = spec["planning"]
    slides = {slide_id(s): s for s in spec["slides"]}
    runtime = {
        "workflow_version", "slides", "planning", "updated_at",
        "max_concurrent_slides",
    }
    global_visual = {
        "spec": {k: v for k, v in spec.items() if k not in runtime},
        "story": planning["story"], "generation": planning["generation"],
        "brief": {k: v for k, v in planning["brief"].items()
                  if k not in {"output_profile", "landing_title"}},
    }
    global_notes = {
        "brief": {
            k: v for k, v in planning["brief"].items()
            if k not in {"output_profile", "landing_title"}
        },
        "delivery": planning["delivery"], "story": planning["story"],
        "deck_context": spec["deck_context"], "goal": spec["goal"],
        "language": spec["language"],
    }
    local_visual, local_notes = {}, {}
    for sid, slide in slides.items():
        shared = {
            key: planning["shared_visuals"][key]
            for key in slide["shared_visual_ids"]
        }
        shared_assets = asset_entries([
            {"path": value["asset_path"], "role": key}
            for key, value in sorted(shared.items()) if value.get("asset_path")
        ], base)
        assets = asset_entries(slide["required_images"], base)
        local_visual[sid] = {
            "shared_visuals": shared, "shared_assets": shared_assets,
            "slide": {
                k: v for k, v in slide.items()
                if k not in {"speaker_notes", "sample_approved",
                             "approved_sample", "updated_at"}
            },
            "assets": assets,
        }
        local_notes[sid] = {
            "notes": slide["speaker_notes"],
            "semantic_content": {
                "title": slide["title"], "intent": slide["intent"],
                "role": slide["role"], "key_points": slide.get("key_points", []),
                "visible_copy": slide["visible_copy"],
                "claim_sources": slide["claim_sources"],
                "visual_meaning": {
                    key: slide["visual_plan"][key]
                    for key in ("subject", "objects", "relationships")
                },
                "shared_meanings": {
                    key: value["meaning"] for key, value in shared.items()
                },
                "assets": assets, "shared_assets": shared_assets,
            },
        }
    visual_contexts, note_contexts = {}, {}
    for sid in slides:
        dependencies = dependency_closure(sid, slides)
        visual_contexts[sid] = {
            "global": global_visual, "local": local_visual[sid],
            "dependencies": {d: local_visual[d] for d in dependencies},
        }
        note_contexts[sid] = {
            "global": global_notes, "local": local_notes[sid],
            "dependencies": {d: local_notes[d] for d in dependencies},
        }
    return spec, visual_contexts, note_contexts


def build_manifest(spec: dict, base: Path) -> dict:
    spec, visual_contexts, note_contexts = build_contexts(spec, base)
    planning = spec["planning"]
    bindings = {
        sid: {
            "visual_hash": digest(visual_contexts[sid]),
            "notes_hash": digest(note_contexts[sid]),
        }
        for sid in visual_contexts
    }
    policy = {
        "review_policy": planning["review_policy"],
        "output_profile": planning["brief"]["output_profile"],
        "landing_title": planning["brief"].get("landing_title"),
    }
    return {
        "plan_hash": digest({"spec": spec, "bindings": bindings}),
        "style_hash": digest({
            "style": spec["style"], "generation": planning["generation"],
            "language": spec["language"], "aspect_ratio": spec["aspect_ratio"],
        }),
        "policy": policy, "policy_hash": digest(policy), "slides": bindings,
        "calibration_hash": digest(planning["sample_strategy"]),
    }


def _validate_spec(spec: dict) -> None:
    def need(condition: bool, message: str) -> None:
        if not condition:
            raise ContractError(message)

    def nonempty(value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip())

    def strings(value: Any) -> bool:
        return isinstance(value, list) and all(isinstance(v, str) for v in value)

    need(isinstance(spec, dict), "Spec must be an object")
    need(spec.get("workflow_version") == 2, "Managed workflow_version must be 2")
    digest(spec)  # Reject nonfinite/unserializable values.
    for key in ("deck_name", "language", "selected_image_backend", "goal"):
        need(nonempty(spec.get(key)), f"Missing {key}")
    need(spec.get("aspect_ratio") in {"16:9", "4:3"}, "Unsupported ratio. Choose 16:9 or 4:3")
    for key in ("approved_style_reference", "sample_generation_method"):
        need(key not in spec, f"{key} is ledger-owned in managed v2")
    need(isinstance(spec.get("style"), dict) and bool(spec["style"]), "Missing style")
    need(isinstance(spec.get("deck_context"), dict), "Missing deck_context")
    p = spec.get("planning")
    need(isinstance(p, dict), "Missing planning")
    for key in ("brief", "readiness", "shared_visuals", "delivery", "generation", "sample_strategy"):
        need(isinstance(p.get(key), dict), f"Missing planning.{key}")
    need(nonempty(p.get("story")), "Missing story")
    need(p.get("unresolved") == [], "Unresolved approval blockers")
    need(p.get("review_policy") in {"consolidated", "strict"}, "Invalid review policy")
    brief = p["brief"]
    for key in ("audience", "purpose", "notes_language", "tone"):
        need(nonempty(brief.get(key)), f"Missing brief.{key}")
    need(brief.get("output_profile") in {"none", "medavis", "both"}, "Invalid output profile")
    if brief["output_profile"] != "none":
        need(nonempty(brief.get("landing_title")), "Branded output requires landing title")
    generation = p["generation"]
    for key in ("backend_used", "tool_name", "mode"):
        need(nonempty(generation.get(key)), f"Missing generation.{key}")
    need(generation["backend_used"] == spec["selected_image_backend"], "Backend conflict")
    need(generation.get("aspect_ratio") == spec["aspect_ratio"], "Generation ratio conflict")
    for key, value in p["shared_visuals"].items():
        need(nonempty(key) and isinstance(value, dict), "Malformed shared visual")
        need(nonempty(value.get("meaning")) and nonempty(value.get("appearance")), "Incomplete shared visual")
        if "asset_path" in value:
            need(nonempty(value["asset_path"]), "Empty shared asset path")

    slides = spec.get("slides")
    need(isinstance(slides, list) and bool(slides), "Missing slides")
    ids = set()
    for expected, slide in enumerate(slides, 1):
        need(isinstance(slide, dict), "Slide must be an object")
        number = slide.get("number")
        need(isinstance(number, int) and not isinstance(number, bool) and number == expected,
             "Internal slide numbers must match consecutive plan order")
        ids.add(slide_id(slide))
        for key in ("title", "role", "intent"):
            need(nonempty(slide.get(key)), f"Missing slide.{key}")
        for key in ("sample_approved", "approved_sample"):
            need(key not in slide, f"{key} is not approval evidence")
        need(strings(slide.get("depends_on")), "Invalid dependencies")
        need(strings(slide.get("shared_visual_ids")), "Invalid shared visual IDs")
        need(all(s in p["shared_visuals"] for s in slide["shared_visual_ids"]), "Unknown shared visual")
        copy = slide.get("visible_copy")
        need(isinstance(copy, dict), "Missing visible_copy")
        need(copy.get("title") == slide["title"], "Visible title conflict")
        need(strings(copy.get("body")) and strings(copy.get("labels")), "Malformed visible copy")
        visual = slide.get("visual_plan")
        need(isinstance(visual, dict), "Missing visual_plan")
        for key in ("type", "subject", "composition"):
            need(nonempty(visual.get(key)), f"Missing visual_plan.{key}")
        need(strings(visual.get("objects")), "Malformed visual objects")
        need(isinstance(visual.get("relationships"), list), "Malformed relationships")
        for relation in visual["relationships"]:
            need(isinstance(relation, dict), "Relation must be an object")
            need(nonempty(relation.get("from")) and nonempty(relation.get("to")), "Incomplete relationship")
            need(relation["from"] in visual["objects"] and relation["to"] in visual["objects"],
                 "Relationship references an unknown object")
        notes = slide.get("speaker_notes")
        need(isinstance(notes, dict) and nonempty(notes.get("text")), "Missing talk")
        timing = notes.get("speaking_time_seconds")
        need(timing is None or (
            isinstance(timing, (int, float)) and not isinstance(timing, bool) and timing > 0
        ), "Invalid speaking time")
        need(nonempty(notes.get("transition")), "Missing speaking transition")
        sources = slide.get("claim_sources")
        need(isinstance(sources, list), "Missing claim/source status")
        for source in sources:
            need(isinstance(source, dict), "Malformed claim source")
            need(source.get("status") in {"provided", "proposed", "external_source"}, "Unresolved claim")
            need(nonempty(source.get("claim")) and nonempty(source.get("source")), "Missing claim evidence")
        images = slide.get("required_images")
        need(isinstance(images, list), "Missing normalized required_images")
        for image in images:
            need(isinstance(image, dict) and nonempty(image.get("path")), "Malformed asset")
            need(nonempty(image.get("role")) and nonempty(image.get("fidelity")), "Missing asset role/fidelity")
    for slide in slides:
        need(all(d in ids for d in slide["depends_on"]), "Unknown dependency")
    required = p["sample_strategy"].get("required_slides")
    need(strings(required) and bool(required) and len(required) == len(set(required)),
         "Required representative sample IDs must be explicit and unique")
    need(all(s in ids for s in required), "Unknown required sample")


def validate_spec(spec: dict) -> None:
    try:
        _validate_spec(spec)
    except (TypeError, KeyError, IndexError) as exc:
        raise ContractError("Malformed managed specification") from exc


def read_contract_json(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ContractError(f"Missing or malformed {label}: {path}") from exc
    if not isinstance(value, dict):
        raise ContractError(f"{label} must be an object")
    return value


def load_managed_spec(deck_dir: Path) -> dict:
    if (Path(deck_dir) / ".planning_transaction.json").exists():
        raise ContractError("Interrupted planning transaction; re-record the reviewed decision")
    spec = read_contract_json(Path(deck_dir) / "deck_spec.json", "managed spec")
    validate_spec(spec)
    return spec


def approval_event(ledger: dict, event_id: str, scope: str) -> dict:
    events = ledger.get("events")
    if not isinstance(events, list):
        raise ContractError("Malformed approval events")
    ids = []
    for event in events:
        if not isinstance(event, dict) or not isinstance(event.get("id"), str):
            raise ContractError("Malformed approval event")
        ids.append(event["id"])
    if len(ids) != len(set(ids)):
        raise ContractError("Duplicate approval event IDs")
    event = next((e for e in events if e["id"] == event_id), None)
    if not event or event.get("actor") != "user":
        raise ContractError(f"Missing actual user approval event for {scope}")
    if not isinstance(event.get("evidence"), str) or not event["evidence"].strip():
        raise ContractError("User approval requires evidence")
    scopes = event.get("scopes")
    if not isinstance(scopes, list) or not all(isinstance(v, str) for v in scopes) or scope not in scopes:
        raise ContractError(f"User event does not approve {scope}")
    from datetime import datetime
    timestamp = event.get("timestamp")
    try:
        parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        if parsed.utcoffset() is None:
            raise ValueError("Unzoned timestamp")
    except (AttributeError, ValueError, TypeError) as exc:
        raise ContractError("Approval event requires a zoned timestamp") from exc
    return event


def require_policy_approval(manifest: dict, ledger: dict) -> None:
    record = ledger.get("policy")
    expected = manifest["policy"]
    if not isinstance(record, dict) or record.get("policy_hash") != manifest["policy_hash"]:
        raise ContractError("Missing or stale policy approval")
    if {"review_policy": record.get("value"),
        "output_profile": record.get("output_profile"),
        "landing_title": record.get("landing_title")} != expected:
        raise ContractError("Policy approval values conflict with fingerprint")
    approval_event(ledger, record.get("event_id"), "policy")


def load_ledger(deck_dir: Path) -> dict:
    ledger = read_contract_json(Path(deck_dir) / "plan_approvals.json", "plan approval ledger")
    if ledger.get("workflow_version") != 2:
        raise ContractError("Missing managed approval ledger version")
    for name in ("slides", "samples", "extra_repairs"):
        if not isinstance(ledger.get(name), dict):
            raise ContractError(f"Malformed approval ledger {name}")
    if not isinstance(ledger.get("events"), list):
        raise ContractError("Malformed approval ledger events")
    return ledger


def require_plan_approval(deck_dir: Path, manifest: dict, slide_ids: list[str]) -> dict:
    ledger = load_ledger(deck_dir)
    validate_plan_records(manifest, ledger, slide_ids)
    return ledger


def validate_plan_records(manifest: dict, ledger: dict, slide_ids: list[str]) -> None:
    require_policy_approval(manifest, ledger)
    calibration=ledger.get("calibration")
    if not isinstance(calibration,dict) or calibration.get("strategy_hash")!=manifest["calibration_hash"]:
        raise ContractError("Missing or stale calibration strategy approval")
    approval_event(ledger,calibration.get("event_id"),"visual")
    if not slide_ids or len(slide_ids) != len(set(slide_ids)):
        raise ContractError("Approval selection must be nonempty and unique")
    for sid in slide_ids:
        expected = manifest["slides"].get(sid)
        record = ledger["slides"].get(sid)
        if expected is None or not isinstance(record, dict):
            raise ContractError(f"Missing plan approval for {sid}")
        for field, scope in (("visual_hash", "visual"), ("notes_hash", "talk")):
            if record.get(field) != expected[field]:
                raise ContractError(f"Missing or stale {scope} approval for {sid}")
            approval_event(ledger, record.get(f"{scope}_event_id", record.get("event_id")), scope)


def require_legacy_allowed(deck_dir: Path) -> None:
    deck_dir = Path(deck_dir)
    if (deck_dir / "plan_approvals.json").exists():
        raise ContractError("Legacy mode cannot bypass managed approval markers")
    for name in ("deck_spec.json", "slide_jobs.json"):
        path = deck_dir / name
        if path.exists():
            value = read_contract_json(path, name)
            if "workflow_version" in value or "planning" in value:
                raise ContractError("Legacy mode cannot bypass managed workflow markers")


def planning_lock(deck_dir: Path):
    from filelock import FileLock
    deck_dir = Path(deck_dir)
    if not deck_dir.is_dir():
        raise ContractError(f"Deck directory missing: {deck_dir}")
    return FileLock(str(deck_dir / ".planning.lock"))


def selection(value: str | None, expected: list[str]) -> list[str]:
    if value is None:
        return list(expected)
    from slide_run_state import normalize_slide_id
    try:
        result = [normalize_slide_id(v.strip()) for v in value.split(",")]
    except ValueError as exc:
        raise ContractError(str(exc)) from exc
    if not result or len(set(result)) != len(result) or any(s not in expected for s in result):
        raise ContractError("Unknown, empty or duplicate slide selection")
    return result

def inside_path(deck_dir: Path, reference: str) -> Path:
    if not isinstance(reference, str) or not reference:
        raise ContractError("Missing deck file reference")
    path = (Path(deck_dir) / reference).resolve()
    try:
        path.relative_to(Path(deck_dir).resolve())
    except ValueError as exc:
        raise ContractError("Managed artifact must stay inside the deck") from exc
    return path


def require_samples(deck_dir: Path, spec: dict, manifest: dict, ledger: dict) -> list[dict]:
    from slide_image_ratio import RATIO_BY_LABEL, require_image_ratio
    by_id = {slide_id(s): s for s in spec["slides"]}
    refs = []
    for sid in spec["planning"]["sample_strategy"]["required_slides"]:
        record = ledger["samples"].get(sid)
        if not isinstance(record, dict):
            raise ContractError(f"Missing sample approval for {sid}")
        approval_event(ledger, record.get("event_id"), "sample")
        if (record.get("style_hash") != manifest["style_hash"]
                or record.get("backend") != spec["selected_image_backend"]
                or record.get("aspect_ratio") != spec["aspect_ratio"]
                or record.get("visual_family") != by_id[sid]["visual_plan"]["type"]):
            raise ContractError(f"Stale sample style/config/suitability for {sid}")
        path = inside_path(deck_dir, record.get("image"))
        if file_digest(path) != record.get("image_sha256"):
            raise ContractError(f"Changed sample bytes for {sid}")
        try:
            require_image_ratio(str(path), RATIO_BY_LABEL[spec["aspect_ratio"]], spec["aspect_ratio"])
        except (OSError, ValueError) as exc:
            raise ContractError(str(exc)) from exc
        refs.append({"slide_id": sid, "path": record["image"],
                     "sha256": record["image_sha256"], "style_hash": record["style_hash"]})
    return refs

def render_assets(context: dict) -> list[dict]:
    result=[]
    seen=set()
    for local in [context["local"],*context["dependencies"].values()]:
        for asset in local["assets"]+local["shared_assets"]:
            key=(asset["path"],asset.get("role"),asset.get("fidelity"))
            if key not in seen:
                result.append(asset)
                seen.add(key)
    return result


def approved_source_inputs(deck_dir: Path, context: dict, ledger: dict) -> list[dict]:
    result=[]
    for asset in render_assets(context):
        record=ledger.get("assets",{}).get(asset["path"])
        if not isinstance(record,dict) or record.get("sha256")!=asset["sha256"]:
            raise ContractError("Missing or stale approved source snapshot")
        snapshot=inside_path(deck_dir,record.get("path"))
        if file_digest(snapshot)!=asset["sha256"] or file_digest(Path(asset["path"]))!=asset["sha256"]:
            raise ContractError("Approved source or snapshot bytes changed")
        result.append({"path":str(snapshot),"source_path":asset["path"],"sha256":asset["sha256"],
                       "role":asset.get("role"),"fidelity":asset.get("fidelity")})
    return result


def accepted_sample_is_current(deck_dir: Path, sid: str, manifest: dict, ledger: dict) -> bool:
    record=ledger.get("samples",{}).get(sid,{})
    accepted=record.get("accepted_final")
    if not isinstance(accepted,dict) or accepted.get("visual_hash")!=manifest["slides"][sid]["visual_hash"]:
        return False
    approval_event(ledger,record.get("event_id"),"sample")
    path=inside_path(deck_dir,accepted.get("path"))
    return path.is_file() and file_digest(path)==accepted.get("image_sha256")

from contextlib import contextmanager


@contextmanager
def consumer_lock(deck_dir: Path, legacy: bool=False):
    try:
        if legacy:
            require_legacy_allowed(deck_dir)
            yield False
        else:
            with planning_lock(deck_dir):
                load_managed_spec(deck_dir)
                yield True
    except ContractError as exc:
        raise SystemExit(str(exc)) from exc


def require_job_current(deck_dir: Path, jobs: dict, slide: dict) -> dict:
    if jobs.get("workflow_version")!=2:
        raise ContractError("Missing managed job metadata; explicit legacy mode is required")
    spec=load_managed_spec(deck_dir)
    manifest=build_manifest(spec,deck_dir)
    sid=slide.get("slide_id")
    ledger=require_plan_approval(deck_dir,manifest,[sid])
    path=inside_path(deck_dir,slide.get("job"))
    if file_digest(path)!=slide.get("job_sha256"):
        raise ContractError(f"Compiled prompt SHA changed for {sid}")
    job=read_contract_json(path,"compiled prompt")
    from image_input_contract import require_version
    try:
        require_version(jobs,job)
    except ValueError as exc:
        raise ContractError(str(exc)) from exc
    expected=manifest["slides"][sid]["visual_hash"]
    if job.get("workflow_version")!=2 or job.get("visual_hash")!=expected or slide.get("visual_hash")!=expected:
        raise ContractError(f"Stale visual job for {sid}")
    if (job.get("generation_config")!=spec["planning"]["generation"]
            or job.get("expected_backend")!=spec["selected_image_backend"]
            or job.get("style_hash")!=manifest["style_hash"]):
        raise ContractError("Stale job backend/style configuration")
    phase=job.get("phase")
    if phase not in {"sample","production","repair"} or slide.get("phase")!=phase:
        raise ContractError("Malformed compiled phase")
    refs=[]
    render_phase=job.get("render_phase")
    if render_phase not in {"sample","production"} or (phase!="repair" and render_phase!=phase):
        raise ContractError("Malformed compiled render phase")
    if render_phase=="sample":
        if sid not in spec["planning"]["sample_strategy"]["required_slides"]:
            raise ContractError("Unapproved representative sample selection")
    else:
        refs=require_samples(deck_dir,spec,manifest,ledger)
    if job.get("sample_refs")!=refs:
        raise ContractError("Stale compiled sample inputs")
    context=build_contexts(spec,deck_dir)[1][sid]
    expected_images=[{"path":str(inside_path(deck_dir,r["path"])),"sha256":r["sha256"],
                     "role":"approved style sample","fidelity":"style only"} for r in refs]
    expected_images+=approved_source_inputs(deck_dir,context,ledger)
    if job.get("input_images")!=expected_images or slide.get("input_images")!=expected_images:
        raise ContractError("Compiled source/image inputs differ from approved snapshots")
    from generation_execution import execution_contract
    if job.get("execution")!=execution_contract(spec["planning"]["generation"],expected_images,spec["selected_image_backend"]):
        raise ContractError("Compiled execution differs from the approved method/input policy")
    if phase=="repair":
        repair=job.get("repair")
        if (repair!=slide.get("repair_request") or not isinstance(repair,dict)
                or repair.get("render_phase")!=render_phase or repair.get("visual_hash")!=expected):
            raise ContractError("Compiled repair differs from current recorded QA")
    return job


def qa_is_current(deck_dir: Path, slide: dict, manifest: dict) -> bool:
    qa=slide.get("qa")
    sid=slide.get("slide_id")
    if not isinstance(qa,dict) or qa.get("actor")!="agent" or qa.get("status")!="passed":
        return False
    if sid not in manifest["slides"] or qa.get("visual_hash")!=manifest["slides"][sid]["visual_hash"]:
        return False
    if not isinstance(qa.get("evidence"),str) or not qa["evidence"].strip():
        return False
    path=inside_path(deck_dir,slide.get("out"))
    return path.is_file() and qa.get("image_sha256")==file_digest(path)


def sequence_binding(deck_dir: Path,jobs: dict,manifest: dict) -> str:
    by_id={s["slide_id"]:s for s in jobs["slides"]}
    if set(by_id)!=set(manifest["slides"]) or len(by_id)!=len(jobs["slides"]):
        raise ContractError("Job IDs differ from expected plan")
    return digest({"images":[{"slide_id":sid,"sha256":file_digest(inside_path(deck_dir,by_id[sid]["out"])),
                              "visual_hash":manifest["slides"][sid]["visual_hash"]}
                             for sid in manifest["slides"]],
                   "talk":{sid:v["notes_hash"] for sid,v in manifest["slides"].items()}})


def authorize_dispatch(deck_dir: Path,jobs: dict,slide: dict,job: dict) -> None:
    spec=load_managed_spec(deck_dir)
    manifest=build_manifest(spec,deck_dir)
    ledger=require_plan_approval(deck_dir,manifest,[slide["slide_id"]])
    phase=job["phase"]
    if phase=="production":
        first=jobs.setdefault("first_batch",{"ids":[],"sealed":False})
        if first["ids"] and (first["sealed"] or len(first["ids"])>=jobs["max_concurrent_slides"]):
            by_id={s["slide_id"]:s for s in jobs["slides"]}
            regenerating_member=slide["slide_id"] in first["ids"]
            if not regenerating_member and not all(qa_is_current(deck_dir,by_id[sid],manifest) for sid in first["ids"]):
                raise ContractError("First production batch needs current agent QA before later dispatch")
            first["sealed"]=True
            if all(qa_is_current(deck_dir,by_id[sid],manifest) for sid in first["ids"]):
                jobs["systemic_pause"]=False
        if jobs.get("systemic_pause") and slide["slide_id"] not in first["ids"]:
            raise ContractError("Production paused: correct the repeated first-batch failure")
        if spec["planning"]["review_policy"]=="strict":
            from slide_run_state import review_is_valid
            for prior in jobs["slides"]:
                if prior.get("status")=="recorded" and not review_is_valid(deck_dir,prior):
                    raise ContractError("Strict policy requires previous batch user image review")
        if not first["sealed"] and slide["slide_id"] not in first["ids"]:
            first["ids"].append(slide["slide_id"])
    if phase=="repair":
        visual=slide["visual_hash"]
        counts=slide.setdefault("repair_counts",{})
        used=counts.get(visual,0)
        extra=0
        records=ledger["extra_repairs"].get(slide["slide_id"],[])
        if not isinstance(records,list):
            raise ContractError("Malformed extra repair authorizations")
        for record in records:
            if record.get("visual_hash")!=visual:
                continue
            event=approval_event(ledger,record.get("event_id"),"repair")
            attempts=record.get("attempts")
            if not isinstance(attempts,int) or isinstance(attempts,bool) or attempts<1:
                raise ContractError("Invalid authorized repair count")
            if event.get("additional_attempts")!=attempts or event.get("visual_hash")!=visual:
                raise ContractError("Repair authorization conflicts with actual user event")
            extra+=attempts
        if used>=1+extra:
            raise ContractError("Repair limit reached; actual extra-attempt user authorization required")
        counts[visual]=used+1

def require_managed_ready(deck_dir: Path,output_profile: str,aspect_ratio: str,landing_title: str|None) -> None:
    import re
    from slide_image_ratio import RATIO_BY_LABEL,require_image_ratio
    from slide_run_state import review_is_valid
    spec=load_managed_spec(deck_dir)
    manifest=build_manifest(spec,deck_dir)
    ledger=require_plan_approval(deck_dir,manifest,list(manifest["slides"]))
    require_samples(deck_dir,spec,manifest,ledger)
    if (output_profile!=manifest["policy"]["output_profile"] or aspect_ratio!=spec["aspect_ratio"]
            or landing_title!=manifest["policy"]["landing_title"]):
        raise ContractError("Output profile, ratio or title differs from actual approved policy")
    jobs=read_contract_json(Path(deck_dir)/"slide_jobs.json","managed jobs")
    by_id={s["slide_id"]:s for s in jobs.get("slides",[])}
    if len(by_id)!=len(jobs.get("slides",[])) or set(by_id)!=set(manifest["slides"]):
        raise ContractError("Expected completed job set is missing or duplicated")
    image_dir=Path(deck_dir)/"origin_image"
    images=[]
    if image_dir.is_dir():
        for path in image_dir.iterdir():
            if path.is_file() and re.match(r"^slide_\d+\.(png|jpe?g|gif|bmp)$",path.name,re.I):
                images.append(path.name.lower())
    expected=[f"{sid}.png" for sid in manifest["slides"]]
    if sorted(images)!=sorted(expected):
        raise ContractError("Final images are missing, extra or duplicated")
    for sid,slide in by_id.items():
        current_job=require_job_current(deck_dir,jobs,slide)
        from image_input_contract import require_recorded_submission,measured_output
        require_recorded_submission(current_job,slide,inside_path(deck_dir,slide["out"]))
        measured_output(inside_path(deck_dir,slide["out"]),aspect_ratio,spec["planning"]["generation"].get("output_requirements"))
        if slide.get("out")!=f"origin_image/{sid}.png" or slide.get("status") not in {"recorded","accepted"}:
            raise ContractError(f"Final slide is incomplete: {sid}")
        path=inside_path(deck_dir,slide["out"])
        require_image_ratio(str(path),RATIO_BY_LABEL[aspect_ratio],aspect_ratio)
        if not qa_is_current(deck_dir,slide,manifest):
            raise ContractError(f"Current agent QA required for {sid}")
        sample=accepted_sample_is_current(deck_dir,sid,manifest,ledger)
        if not sample and not review_is_valid(deck_dir,slide):
            raise ContractError(f"Current actual user image approval required for {sid}")
    deck_qa=jobs.get("deck_qa",{})
    if (deck_qa.get("actor")!="agent" or deck_qa.get("status")!="passed"
            or not isinstance(deck_qa.get("evidence"),str) or not deck_qa["evidence"].strip()
            or deck_qa.get("binding")!=sequence_binding(deck_dir,jobs,manifest)):
        raise ContractError("Current complete-sequence/talk QA required")
    if jobs.get("systemic_pause"):
        raise ContractError("Unresolved systematic rendering failure")
    try:
        speech=(Path(deck_dir)/"speech.md").read_text(encoding="utf-8")
    except OSError as exc:
        raise ContractError("Approved speech.md is missing") from exc
    headings=list(re.finditer(r"^#{2,4}\s*(?:Slide\s*(\d+)|第\s*(\d+)\s*页)\b[^\n]*$",speech,re.M|re.I))
    numbers=[int(h.group(1) or h.group(2)) for h in headings]
    if numbers!=[s["number"] for s in spec["slides"]]:
        raise ContractError("Talk headings are missing, duplicated or out of order")
    for i,(heading,slide) in enumerate(zip(headings,spec["slides"])):
        stop=headings[i+1].start() if i+1<len(headings) else len(speech)
        text=speech[heading.end():stop].strip()
        if text!=slide["speaker_notes"]["text"].replace("\r\n","\n").strip():
            raise ContractError(f"Speech differs from approved talk: {slide_id(slide)}")




