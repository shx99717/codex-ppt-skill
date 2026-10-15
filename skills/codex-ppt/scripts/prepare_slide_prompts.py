#!/usr/bin/env python3
"""Prepare per-slide image generation jobs for codex-ppt.

This script is deterministic. It does not call an image model. It turns a
structured deck spec into one self-contained JSON job file per slide.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Dict, Iterable, List, Optional

from slide_run_state import (
    DEFAULT_MAX_CONCURRENT_SLIDES,
    now_iso,
    rel_to_deck,
    save_jobs,
    set_run_status,
)
from slide_image_ratio import gpt_image_size


def _locked_aspect_ratio(spec: Dict[str, Any]) -> str:
    raw = spec.get("aspect_ratio")
    if raw is None or str(raw).strip() == "":
        return "16:9"
    label = str(raw).strip()
    if label not in {"16:9", "4:3", "3:2"}:
        _die(f"aspect_ratio must be 16:9, 4:3, or 3:2 (got {label!r})")
    return label


def _die(message: str) -> None:
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        _die(f"Spec file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _die(f"Invalid JSON in {path}: {exc}")
    if not isinstance(data, dict):
        _die("Deck spec must be a JSON object.")
    return data


def _as_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _string_list(value: Any) -> List[str]:
    return [str(item).strip() for item in _as_list(value) if str(item).strip()]


_MARKDOWN_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")


def _parse_markdown_image(value: str) -> Optional[Dict[str, str]]:
    match = _MARKDOWN_IMAGE_RE.search(value)
    if not match:
        return None
    alt_text = match.group(1).strip()
    path = match.group(2).strip()
    description = value[: match.start()].strip(" \t\n\r:-;")
    role_parts = [part for part in [description, alt_text] if part]
    return {
        "path": path,
        "role": " — ".join(role_parts) if role_parts else "reference image",
    }


def _resolve_image_path(path: str, *, base_dir: Path) -> str:
    path = path.strip()
    if not path:
        return path
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", path):
        return path
    candidate = Path(path)
    if candidate.is_absolute():
        return str(candidate)
    return str((base_dir / candidate).resolve())


def _normalize_input_image(entry: Any, *, slide_number: int, image_index: int, base_dir: Path) -> Dict[str, Any]:
    if isinstance(entry, dict):
        image = dict(entry)
        raw_path = image.get("path") or image.get("attachment") or image.get("markdown")
        if isinstance(raw_path, str):
            parsed = _parse_markdown_image(raw_path)
            if parsed:
                image["path"] = parsed["path"]
                image.setdefault("role", parsed["role"])
        if isinstance(image.get("path"), str):
            image["path"] = _resolve_image_path(image["path"], base_dir=base_dir)
        return image
    if isinstance(entry, str):
        parsed = _parse_markdown_image(entry)
        if not parsed:
            _die(
                f"Slide {slide_number}: required_images entry {image_index} must be an "
                "object or a Markdown image reference like ![alt](path)."
            )
        lowered = entry.lower()
        fidelity = ""
        if "strict input asset" in lowered:
            fidelity = "strict input asset; preserve the supplied image content"
        return {
            "path": _resolve_image_path(parsed["path"], base_dir=base_dir),
            "role": parsed["role"],
            "fidelity": fidelity,
        }
    _die(f"Slide {slide_number}: required_images entry {image_index} has unsupported type.")


def _slide_images(slide: Dict[str, Any], *, slide_number: int, base_dir: Path) -> List[Dict[str, Any]]:
    images: List[Dict[str, Any]] = []
    for index, image in enumerate(_as_list(slide.get("required_images") or slide.get("input_images")), start=1):
        images.append(_normalize_input_image(image, slide_number=slide_number, image_index=index, base_dir=base_dir))
    return images


def _is_gpt_image_2_backend(label: Optional[str]) -> bool:
    if not label:
        return False
    n = re.sub(r"[^a-z0-9]+", "", label.lower())
    if "generateimage" in n:
        return False
    return "imagegen" in n or "codexgptimage" in n or "gptimage" in n


def _method_backend_label(method: Optional[Dict[str, Any]]) -> Optional[str]:
    if not method:
        return None
    for key in ("backend_used", "selected_backend", "backend", "tool_name"):
        value = method.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _sample_generation_method(spec: Dict[str, Any], *, base_dir: Path) -> Optional[Dict[str, Any]]:
    method = spec.get("sample_generation_method") or spec.get("image_generation_method")
    if method is None:
        return None
    if not isinstance(method, dict):
        _die("sample_generation_method must be an object when present.")
    method = dict(method)
    for key in ("approved_sample_path", "sample_slide_path", "sample_output_path"):
        if isinstance(method.get(key), str):
            method[key] = _resolve_image_path(method[key], base_dir=base_dir)
    label = _locked_aspect_ratio(spec)
    backend = _method_backend_label(method)
    if _is_gpt_image_2_backend(backend):
        method["size"] = f"gpt-image-2 --size {gpt_image_size(label)}"
    else:
        method["aspect_ratio"] = label
        size = method.get("size")
        if isinstance(size, str) and "gpt-image-2 --size" in size:
            del method["size"]
    return method


def _format_block(title: str, value: Any) -> str:
    if value is None or value == "" or value == [] or value == {}:
        return ""
    if isinstance(value, (dict, list)):
        body = json.dumps(value, ensure_ascii=False, indent=2)
    else:
        body = str(value).strip()
    return f"## {title}\n{body}\n"


def _format_input_images(images: Iterable[Dict[str, Any]]) -> str:
    lines: List[str] = []
    for idx, image in enumerate(images, start=1):
        path = str(image.get("path") or image.get("attachment") or "").strip()
        role = str(image.get("role") or "reference image").strip()
        fidelity = str(image.get("fidelity") or image.get("constraints") or "").strip()
        if not path:
            _die(f"Input image {idx} is missing path or attachment.")
        if fidelity:
            lines.append(f"- Image {idx}: {path} — {role}; {fidelity}")
        else:
            lines.append(f"- Image {idx}: {path} — {role}")
    return "\n".join(lines)


def _slide_number(slide: Dict[str, Any], fallback: int) -> int:
    raw = slide.get("number", fallback)
    try:
        number = int(raw)
    except (TypeError, ValueError):
        _die(f"Invalid slide number: {raw}")
    if number <= 0:
        _die(f"Slide number must be positive: {number}")
    return number


def _normalize_language_kind(value: str) -> str:
    stripped = value.strip()
    n = re.sub(r"[^a-z0-9]+", "", stripped.lower())
    # Exact CJK label BEFORE alnum fold — `中文`.lower() stays CJK and would be stripped to "".
    if stripped in {"中文"} or n in {"chinese", "zh", "zhcn", "zhtw"}:
        return "zh"
    if n in {"english", "en", "enus", "engb"}:
        return "en"
    if n in {"mixed", "zhen", "enzh", "bilingual"}:
        return "mixed"
    return "other"


def _resolve_slide_language(slide: Dict[str, Any], deck: Dict[str, Any]) -> tuple[str, str]:
    raw = slide.get("language")
    if not (isinstance(raw, str) and raw.strip()):
        raw = deck.get("language")
    if not (isinstance(raw, str) and raw.strip()):
        raw = "English"
    display = raw.strip()
    return display, _normalize_language_kind(display)


def _text_quality_constraint(kind: str, display: str) -> str:
    if kind == "zh":
        return "- Render Chinese text exactly and legibly; avoid garbled characters.\n"
    if kind == "en":
        return "- Render English (Latin-script) text exactly and legibly; avoid garbled characters.\n"
    if kind == "mixed":
        return (
            "- Render both Chinese (CJK) and Latin-script text exactly and legibly; "
            "avoid garbled characters.\n"
        )
    return f"- Render text in {display} exactly and legibly; avoid garbled characters.\n"


def _build_prompt(
    *,
    deck: Dict[str, Any],
    slide: Dict[str, Any],
    number: int,
    global_style_reference: Optional[Dict[str, Any]],
    base_dir: Path,
) -> str:
    title = str(slide.get("title") or f"Slide {number}").strip()
    style = deck.get("style", {})
    display_lang, lang_kind = _resolve_slide_language(slide, deck)
    images: List[Dict[str, Any]] = []
    if global_style_reference:
        images.append(global_style_reference)
    images.extend(_slide_images(slide, slide_number=number, base_dir=base_dir))
    required_background = {
        key: value
        for key, value in {
            "deck_context": deck.get("deck_context"),
            "slide_local_context": slide.get("local_context"),
        }.items()
        if value not in (None, "", [], {})
    }

    prompt_parts = [
        "# Codex PPT Slide Image Prompt\n",
        _format_block("Canvas", {
            "type": f"{_locked_aspect_ratio(deck)} full-slide PowerPoint image",
            "language": display_lang,
            "slide_number": number,
            "render_slide_number": False,
            "gpt_image_2_size": gpt_image_size(_locked_aspect_ratio(deck)),
        }),
        _format_block("Deck Goal", deck.get("goal")),
        _format_block("Required Background", required_background),
        _format_block("Global Style", style),
    ]

    if images:
        prompt_parts.append("## Input Images\n")
        prompt_parts.append(_format_input_images(images))
        prompt_parts.append("\n")

    prompt_parts.extend(
        [
            _format_block("Slide", {
                "number": number,
                "title": title,
                "role": slide.get("role"),
                "intent": slide.get("intent"),
            }),
            _format_block("Text", {
                "title": title,
                "key_points": _string_list(slide.get("key_points")),
                "speaker_focus": slide.get("speaker_focus"),
            }),
            _format_block("Layout", slide.get("layout")),
            _format_block("Visual Elements", slide.get("visual_elements")),
            _format_block("Source Image Rules", slide.get("source_image_rules")),
            _format_block("Constraints", _string_list(slide.get("constraints"))),
        ]
    )

    if global_style_reference:
        prompt_parts.append(
            "## Style Reference Rule\n"
            "Use Image 1 as the approved sample-slide style reference. Match its palette, "
            "typography mood, density, texture, and overall visual identity. Do not copy "
            "its exact layout unless this slide's layout explicitly asks for it.\n"
        )

    if images:
        prompt_parts.append(
            "## Input Image Handling Rules\n"
            "For any input image marked as a strict input asset, include it visibly and "
            "preserve its content. Do not redraw, replace, relabel, or invent a similar "
            "figure. Scale and crop only as needed for composition while keeping the "
            "important labels, arrows, data, and relationships recognizable.\n"
        )

    prompt_parts.append(
        "## Universal Constraints\n"
        "- The final image itself must contain the title and key points.\n"
        f"{_text_quality_constraint(lang_kind, display_lang)}"
        "- Keep the confirmed deck style consistent while varying layout by slide role.\n"
        "- No watermark, unrelated logo, or extra slide number.\n"
    )
    return "\n".join(part for part in prompt_parts if part)


def _job_images(
    slide: Dict[str, Any],
    *,
    number: int,
    global_style_reference: Optional[Dict[str, Any]],
    base_dir: Path,
) -> List[Dict[str, Any]]:
    images: List[Dict[str, Any]] = []
    if global_style_reference:
        images.append(global_style_reference)
    images.extend(_slide_images(slide, slide_number=number, base_dir=base_dir))
    return images


def _write_template(path: Path) -> None:
    # An honest editable draft; replace unresolved facts and check actual tool
    # capabilities before approval. No runtime sample or human approval is asserted.
    template={
        "workflow_version":2,"deck_name":"example-deck","language":"English",
        "aspect_ratio":"3:2","selected_image_backend":"GenerateImage","goal":"Define the presentation goal.",
        "deck_context":{"source_summary":"Replace with provided evidence.","canonical_terms":[]},
        "style":{"name":"clean-professional","visual_direction":"Readable technical diagrams"},
        "planning":{"brief":{"audience":"Confirm audience","purpose":"Confirm purpose",
            "notes_language":"English","tone":"Natural, clear","output_profile":"none","landing_title":None},
            "readiness":{"content":"partial","visual":"partial"},"story":"Confirm the deck story.",
            "shared_visuals":{},"delivery":{"voice":"natural-presenter","speaker_names":[]},
            "review_policy":"consolidated","sample_strategy":{"required_slides":["slide_02"]},
            "generation":{"backend_used":"GenerateImage","tool_name":"GenerateImage",
                          "mode":"generate","aspect_ratio":"3:2"},
            "unresolved":["Confirm intention, exact copy, evidence, visuals, talk and live backend capabilities"]},
        "slides":[]}
    for number,title,role in [(1,"Opening","opening"),(2,"Explain the idea","explanation")]:
        template["slides"].append({"number":number,"title":title,"role":role,"intent":"Confirm slide purpose.",
            "key_points":[],"visible_copy":{"title":title,"body":[],"labels":[]},
            "visual_plan":{"type":"diagram","subject":"Confirm visual meaning","objects":[],
                           "relationships":[],"composition":"Confirm approximate layout"},
            "shared_visual_ids":[],"depends_on":[],"claim_sources":[],"required_images":[],
            "speaker_notes":{"text":"Draft the presenter talk with breathing beats.",
                             "speaking_time_seconds":None,"transition":"Confirm next spoken beat."}})
    from slide_run_state import write_json
    write_json(path,template)



def approved_prompt_blocks(render_context: dict) -> str:
    return "\n\n".join([
        "APPROVED RENDER CONTEXT — visible_copy fields are exact slide text:\n"+
        json.dumps(render_context,ensure_ascii=False,sort_keys=True,indent=2,allow_nan=False),
        "Use the local slide as the output slide; dependencies are context only. "
        "Preserve approved wording, values, objects, and relationships. "
        "Do not render source paths or metadata as visible copy. "
        "Raise a blocker if the approved material cannot fit; do not add claims.",
    ])


def _managed_job(spec,context,sid,manifest,sample_refs,images,phase,repair):
    from generation_execution import execution_contract
    prompt=approved_prompt_blocks(context)
    prompt+="\n\nGenerate one full-slide image with the locked ratio. "
    prompt+="Use source images with their stated fidelity. Style sample images supply visual style only; "
    prompt+="do not copy their text or layout. No local drawing, overlays or raster substitutes."
    if repair:
        prompt+="\n\nRECORDED RENDERING REPAIR:\n"+json.dumps(repair,sort_keys=True,ensure_ascii=False)
    return {"workflow_version":2,"slide":context["local"]["slide"]["number"],
        "title":context["local"]["slide"]["title"],"phase":phase,
        "render_phase":repair["render_phase"] if repair else phase,"prompt":prompt,
        "out":f"{sid}.png","input_images":images,"requires_context_images":bool(images),
        "expected_backend":spec["selected_image_backend"],
        "generation_config":spec["planning"]["generation"],
        "execution":execution_contract(spec["planning"]["generation"],images,spec["selected_image_backend"]),
        "sample_generation_method":spec["planning"]["generation"],
        "visual_hash":manifest["slides"][sid]["visual_hash"],"style_hash":manifest["style_hash"],
        "sample_refs":sample_refs,"repair":repair,"plan_hash":manifest["plan_hash"],
        "generation_contract":{"must_use_selected_image_backend":True,
            "forbidden_final_image_methods":["local drawing","Pillow","SVG/HTML/canvas","manual overlays"],
            "must_return":["backend_used","selected_source","qa_note"]}}


def _comparable_job(job):
    return {k:v for k,v in job.items() if k!="plan_hash"}


def prepare_managed(args) -> int:
    from planning_contract import (ContractError,accepted_sample_is_current,approved_source_inputs,
        build_contexts,build_manifest,file_digest,inside_path,load_managed_spec,planning_lock,
        require_plan_approval,require_samples,selection,slide_id,digest,qa_is_current)
    from slide_run_state import read_json
    from filelock import FileLock
    deck=Path(args.out_dir).resolve()
    if Path(args.spec).resolve()!=(deck/"deck_spec.json").resolve():
        raise ContractError("Managed compilation uses approved canonical deck_spec.json")
    with planning_lock(deck), FileLock(str(deck/".slide_jobs.json.lock")):
        spec=load_managed_spec(deck)
        canonical,contexts,_=build_contexts(spec,deck)
        manifest=build_manifest(canonical,deck)
        ids=list(manifest["slides"])
        selected=selection(args.slides,ids)
        if args.phase=="sample":
            required=spec["planning"]["sample_strategy"]["required_slides"]
            if not args.slides or any(s not in required for s in selected):
                raise ContractError("Sample phase needs explicit required representative --slides")
        ledger=require_plan_approval(deck,manifest,selected)
        if args.selected_backend and args.selected_backend!=spec["selected_image_backend"]:
            raise ContractError("Backend override conflicts with approved plan")
        capacity=(args.max_concurrent_slides if args.max_concurrent_slides is not None
                  else spec.get("max_concurrent_slides",DEFAULT_MAX_CONCURRENT_SLIDES))
        if not isinstance(capacity,int) or isinstance(capacity,bool) or capacity<1:
            raise ContractError("Invalid concurrency capacity")
        jobs=read_json(deck/"slide_jobs.json",default={})
        if jobs and jobs.get("workflow_version")!=2:
            raise ContractError("Managed compilation cannot overwrite legacy job state")
        old_entries={s["slide_id"]:s for s in jobs.get("slides",[])}
        entries={}
        writes={}
        for sid in ids:
            old=old_entries.get(sid)
            entries[sid]=dict(old) if old else {
                "slide_id":sid,"number":contexts[sid]["local"]["slide"]["number"],
                "title":contexts[sid]["local"]["slide"]["title"],"out":f"origin_image/{sid}.png",
                "job":None,"status":"unprepared","dispatch":None,"result":None,"blocker":None}
            if sid not in selected:
                continue
            path=deck/f"prompts/{sid}.json"
            if old and old.get("job") and not path.is_file():
                raise ContractError(f"Missing tracked compiled prompt: {sid}; restore the recorded artifact")
            if old and old.get("status")=="dispatched":
                # Identical recompilation below is allowed; a missing artifact is not.
                if not path.is_file():
                    raise ContractError(f"Cannot replace dispatched job: {sid}")
            repair=None
            if args.phase=="repair":
                repair=entries[sid].get("repair_request")
                if (not isinstance(repair,dict)
                        or repair.get("visual_hash")!=manifest["slides"][sid]["visual_hash"]
                        or repair.get("render_phase") not in {"sample","production"}):
                    raise ContractError(f"No current recorded repair request for {sid}")
            render_phase=repair["render_phase"] if repair else args.phase
            if render_phase=="sample":
                if sid not in spec["planning"]["sample_strategy"]["required_slides"]:
                    raise ContractError("Unapproved representative sample selection")
                sample_refs=[]
            else:
                sample_refs=require_samples(deck,spec,manifest,ledger)
            image_inputs=[{"path":str(inside_path(deck,r["path"])),"sha256":r["sha256"],
                           "role":"approved style sample","fidelity":"style only"} for r in sample_refs]
            image_inputs+=approved_source_inputs(deck,contexts[sid],ledger)
            job=_managed_job(spec,contexts[sid],sid,manifest,sample_refs,image_inputs,args.phase,repair)
            accepted=(args.phase!="repair" and accepted_sample_is_current(deck,sid,manifest,ledger)
                      and not (old and old.get("phase")=="repair"))
            if old and path.exists():
                existing=read_json(path)
                if file_digest(path)!=old.get("job_sha256"):
                    raise ContractError(f"Job was edited outside compiler: {sid}")
                current_repair=(old.get("repair_request") or {}).get("visual_hash")==job["visual_hash"]
                if current_repair and args.phase!="repair":
                    keep_accepted_calibration=(old.get("phase")=="repair"
                        and existing.get("render_phase")=="sample"
                        and existing.get("style_hash")==job["style_hash"]
                        and accepted_sample_is_current(deck,sid,manifest,ledger)
                        and qa_is_current(deck,old,manifest))
                    if keep_accepted_calibration:
                        # Retain the real repaired calibration packet and its
                        # empty style inputs, rather than changing its provenance.
                        continue
                    keep_finished_repair=(old.get("phase")=="repair"
                        and existing.get("style_hash")==job["style_hash"]
                        and existing.get("sample_refs")==job["sample_refs"]
                        and qa_is_current(deck,old,manifest))
                    if keep_finished_repair:
                        continue
                    raise ContractError("Recorded repair requires --phase repair; production/sample cannot bypass the repair limit")
                # Accepted sample provenance stays its actual sample-phase job.
                same=(_comparable_job(existing)==_comparable_job(job))
                keep_sample=(accepted and args.phase!="repair" and existing.get("phase")=="sample"
                             and existing.get("visual_hash")==job["visual_hash"]
                             and existing.get("style_hash")==job["style_hash"])
                if same or keep_sample:
                    if accepted:
                        entries[sid]["status"]="accepted"
                    continue
                if old.get("status")=="dispatched":
                    raise ContractError(f"Cannot replace dispatched job: {sid}")
                if not args.force:
                    raise ContractError(f"Changed job exists: {sid}; use --force after scope approval")
            elif path.exists():
                raise ContractError(f"Untracked prompt exists: {sid}")
            body=(json.dumps(job,ensure_ascii=False,sort_keys=True,indent=2)+"\n").encode("utf-8")
            import hashlib
            entry=entries[sid]
            for key in ("qa","user_review","dispatch","result","blocker"):
                entry.pop(key,None)
            entry.update(job=f"prompts/{sid}.json",job_sha256=hashlib.sha256(body).hexdigest(),
                visual_hash=job["visual_hash"],phase=args.phase,input_images=image_inputs,
                status="accepted" if accepted else "pending",dispatch=None,result=None,blocker=None)
            if accepted:
                entry["result"]={"accepted_sample":True,"final_image":entry["out"],
                    "final_image_sha256":ledger["samples"][sid]["accepted_final"]["image_sha256"],
                    "visual_hash":job["visual_hash"]}
            writes[path]=body
        # Validate all selected entries first, then save; one invalid selection must
        # never replace an earlier valid prompt in the same invocation.
        jobs.update(workflow_version=2,run_status="jobs_prepared",deck_name=spec["deck_name"],
            selected_backend=spec["selected_image_backend"],aspect_ratio=spec["aspect_ratio"],
            sample_generation_method=spec["planning"]["generation"],max_concurrent_slides=capacity,
            slides=[entries[sid] for sid in ids],updated_at=now_iso())
        from record_plan_approval import atomic_group
        payload={p.relative_to(deck).as_posix():body for p,body in writes.items()}
        payload["slide_jobs.json"]=(json.dumps(jobs,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
        atomic_group(deck,payload)
    set_run_status(deck,"jobs_prepared","compiled current managed slide inputs")
    print(json.dumps({"phase":args.phase,"selected":selected,"written":len(writes),
                      "plan_hash":manifest["plan_hash"]},ensure_ascii=False))
    return 0

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec", help="Deck spec JSON file.")
    parser.add_argument("--out-dir", help="Deck project directory.")
    parser.add_argument("--write-template", help="Write an example deck spec JSON and exit.")
    parser.add_argument(
        "--selected-backend",
        help="Confirmed image backend label, such as `GenerateImage`, `codex-gpt-image`, or `scripts/image_gen.py`.",
    )
    parser.add_argument(
        "--max-concurrent-slides",
        type=int,
        default=None,
        help=f"Maximum slide subagents to dispatch at once. Defaults to {DEFAULT_MAX_CONCURRENT_SLIDES}.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing prompt files.")
    parser.add_argument("--phase", choices=["sample", "production", "repair"], default="production")
    parser.add_argument("--slides", help="Explicit comma-separated managed slide IDs")
    parser.add_argument("--legacy-unmanaged", action="store_true")
    args = parser.parse_args()

    if args.write_template:
        _write_template(Path(args.write_template))
        return 0

    if not args.spec or not args.out_dir:
        _die("Use --spec and --out-dir, or --write-template.")

    spec_path = Path(args.spec)
    spec = _read_json(spec_path)
    from planning_contract import ContractError, require_legacy_allowed
    try:
        if not args.legacy_unmanaged:
            return prepare_managed(args)
        require_legacy_allowed(Path(args.out_dir))
        if "workflow_version" in spec or "planning" in spec:
            raise ContractError("Legacy flag cannot bypass managed input")
    except ContractError as exc:
        _die(str(exc))
    spec_dir = spec_path.resolve().parent
    slides = spec.get("slides")
    if not isinstance(slides, list) or not slides:
        _die("Deck spec must include a non-empty slides array.")

    numbered_slides: List[tuple[int, Dict[str, Any], int]] = []
    seen_slide_numbers: Dict[int, int] = {}
    for fallback, slide in enumerate(slides, start=1):
        if not isinstance(slide, dict):
            _die(f"Slide entry {fallback} must be an object.")
        number = _slide_number(slide, fallback)
        if number in seen_slide_numbers:
            _die(
                f"Duplicate slide number {number}: slide entries "
                f"{seen_slide_numbers[number]} and {fallback} would both write slide_{number:02d}.json."
            )
        seen_slide_numbers[number] = fallback
        numbered_slides.append((fallback, slide, number))

    out_dir = Path(args.out_dir)
    prompts_dir = out_dir / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "origin_image").mkdir(parents=True, exist_ok=True)

    global_style_reference = spec.get("approved_style_reference")
    if global_style_reference is not None and not isinstance(global_style_reference, dict):
        _die("approved_style_reference must be an object when present.")
    if global_style_reference and isinstance(global_style_reference.get("path"), str):
        global_style_reference = dict(global_style_reference)
        global_style_reference["path"] = _resolve_image_path(global_style_reference["path"], base_dir=spec_dir)

    sample_generation_method = _sample_generation_method(spec, base_dir=spec_dir)
    max_concurrent_slides = args.max_concurrent_slides
    if max_concurrent_slides is None:
        max_concurrent_slides = int(spec.get("max_concurrent_slides", DEFAULT_MAX_CONCURRENT_SLIDES))
    if max_concurrent_slides < 1:
        _die("max_concurrent_slides must be >= 1.")
    selected_backend = (
        args.selected_backend
        or spec.get("selected_image_backend")
        or spec.get("image_backend")
        or _method_backend_label(sample_generation_method)
    )
    slide_job_entries: List[Dict[str, Any]] = []

    for fallback, slide, number in numbered_slides:
        use_style_reference = bool(slide.get("use_approved_style_reference", True))
        slide_style_reference = global_style_reference if use_style_reference else None
        prompt = _build_prompt(
            deck=spec,
            slide=slide,
            number=number,
            global_style_reference=slide_style_reference,
            base_dir=spec_dir,
        )
        images = _job_images(slide, number=number, global_style_reference=slide_style_reference, base_dir=spec_dir)
        job = {
            "slide": number,
            "title": slide.get("title", f"Slide {number}"),
            "prompt": prompt,
            "out": f"slide_{number:02d}.png",
            "input_images": images,
            "requires_context_images": bool(images),
            "expected_backend": selected_backend,
            "sample_generation_method": sample_generation_method,
            "generation_contract": {
                "must_use_selected_image_backend": True,
                "must_match_sample_generation_method": bool(sample_generation_method),
                "forbidden_final_image_methods": [
                    "local drawing/rendering scripts",
                    "Pillow-generated slides",
                    "SVG/HTML/CSS/canvas screenshots",
                    "python-pptx/PptxGenJS/native PPT layout screenshots",
                    "manually composited text/image overlays",
                ],
                "must_return": ["backend_used", "selected_source", "qa_note"],
            },
        }
        prompt_path = prompts_dir / f"slide_{number:02d}.json"
        if prompt_path.exists() and not args.force:
            _die(f"Slide job file already exists: {prompt_path} (use --force)")
        prompt_path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        slide_id = f"slide_{number:02d}"
        final_image = out_dir / "origin_image" / f"{slide_id}.png"
        sample_approved = bool(slide.get("sample_approved") or slide.get("approved_sample"))
        status = "accepted" if sample_approved and final_image.exists() else "pending"
        slide_job_entries.append(
            {
                "slide_id": slide_id,
                "number": number,
                "title": slide.get("title", f"Slide {number}"),
                "job": rel_to_deck(out_dir, prompt_path),
                "out": rel_to_deck(out_dir, final_image),
                "input_images": images,
                "requires_context_images": bool(images),
                "status": status,
                "dispatch": None,
                "result": {
                    "final_image": rel_to_deck(out_dir, final_image),
                    "accepted_sample": True,
                }
                if status == "accepted"
                else None,
                "blocker": None,
            }
        )

    slide_jobs = {
        "run_status": "jobs_prepared",
        "deck_name": spec.get("deck_name"),
        "selected_backend": selected_backend,
        "aspect_ratio": _locked_aspect_ratio(spec),
        "sample_generation_method": sample_generation_method,
        "max_concurrent_slides": max_concurrent_slides,
        "slides": slide_job_entries,
        "updated_at": now_iso(),
    }
    save_jobs(out_dir, slide_jobs)
    set_run_status(out_dir, "jobs_prepared", "prepared slide prompt jobs")

    print(f"Wrote {len(slides)} slide job file(s) to {prompts_dir}")
    print(f"Wrote slide job state to {out_dir / 'slide_jobs.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
