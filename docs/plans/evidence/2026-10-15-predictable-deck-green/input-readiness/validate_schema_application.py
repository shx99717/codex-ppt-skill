"""Exercise the portable guide's actual schema/draft-view seam; never approve.

Owned artifacts only. Original cards/talk and scripted decisions are immutable
inputs; their schema representation changes, not their content or user decisions.
"""
from pathlib import Path
import copy
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SKILL = Path("D:/git/codex-ppt-skill/skills/codex-ppt")
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))
from planning_contract import ContractError, validate_spec  # actual repository API

CASES = ("D1", "D2", "D3", "mixed")

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def run(label, args):
    args=[args[0],"-B",*args[1:]]
    result = subprocess.run([str(v) for v in args], capture_output=True, text=True,
                            encoding="utf-8", errors="strict")
    entry = {"label": label, "argv": [str(v) for v in args], "returncode": result.returncode,
             "stdout": result.stdout, "stderr": result.stderr}
    commands.append(entry)
    return entry

commands = []
archive_checks = []
red = []
green = []
originals = {}
card_hashes = {}

# Archive every incompatible JSON before writing any compatible candidate.
# Existing archives are immutable; a rerun consumes them, never replaces them.
for case in CASES:
    current = ROOT / case / "deck_spec.draft.json"
    archive = ROOT / "schema-red" / f"{case}.json"
    if not archive.exists():
        raw = current.read_bytes()
        archive.parent.mkdir(parents=True, exist_ok=True)
        archive.write_bytes(raw)
        assert archive.read_bytes() == raw
        archive_checks.append({"case": case, "archive": str(archive), "original_sha256": sha(raw),
                               "archived_sha256": sha(archive.read_bytes()), "byte_identical_at_archive": True})
    else:
        raw = archive.read_bytes()
        previous = ROOT / "schema-verification.json"
        if previous.exists():
            entries = json.loads(previous.read_text(encoding="utf-8"))["original_archives"]
            entry = next(x for x in entries if x["case"] == case)
            assert entry["original_sha256"] == sha(raw)
            archive_checks.append(entry)
        else:
            raise RuntimeError("Archive exists without its recorded byte-preservation evidence")
    originals[case] = json.loads(raw.decode("utf-8"))
    card_hashes[case] = {name: sha((ROOT / case / name).read_bytes())
                         for name in ("interaction.md", "outline.draft.md", "speech.draft.md")}

for case, original in originals.items():
    try:
        validate_spec(original)
    except ContractError as exc:
        red.append({"case": case, "operation": "planning_contract.validate_spec(original archived JSON)",
                    "error_type": type(exc).__name__, "error": str(exc)})
    else:
        raise AssertionError(f"Expected original {case} to be incompatible")
    outcome = run(f"{case} archived red draft CLI",
                  [sys.executable, SCRIPTS / "planning_views.py", "--spec", ROOT / "schema-red" / f"{case}.json",
                   "--deck", ROOT / case / "schema-red-draft-attempt", "--draft"])
    assert outcome["returncode"] != 0
    assert "Missing deck_name" in outcome["stderr"]

# Capture help and an actual fresh bundled template generation as prescribed.
for script in ("prepare_slide_prompts.py", "planning_views.py"):
    result = run(f"{script} help", [sys.executable, SCRIPTS / script, "--help"])
    assert result["returncode"] == 0
result = run("bundled schema template", [sys.executable, SCRIPTS / "prepare_slide_prompts.py",
                                        "--write-template", ROOT / "bundled-template.json"])
assert result["returncode"] == 0
template = json.loads((ROOT / "bundled-template.json").read_text(encoding="utf-8"))

# Each tuple chooses existing object collections as the ends of the already
# written relation. A description retains the exact original relationship text.
# Composite objects can describe an internal relationship (same from/to); this
# introduces no new visual object or new visible text.
ENDS = {
    "D1": [[(0, 1)], [(0, 1)], [(0, 1), (0, 1), (2, 1)],
           [(0, 2), (1, 2)], [(0, 2), (1, 0), (0, 2)], [(0, 2), (1, 2), (1, 2)]],
    "D2": [[(1, 0)], [(0, 1)], [(0, 0), (1, 1)]],
    "D3": [[(0, 1)], [(0, 2)], [(0, 1), (2, 1)], [(0, 0), (3, 2)],
           [(0, 1), (1, 1), (2, 1)]],
    "mixed": [[(1, 0)], [(0, 1)], [(0, 0), (1, 1), (2, 2)]],
}

def compatible(case, original):
    old_deck = original["deck"]
    data = copy.deepcopy(template)
    data["deck_name"] = f"input-readiness-{case.lower()}"
    data["language"] = old_deck["language"]
    data["aspect_ratio"] = old_deck["aspect_ratio"]
    data["selected_image_backend"] = old_deck["selected_image_backend"]
    data["goal"] = old_deck["purpose"]
    data["test_context"] = copy.deepcopy(original["test_context"])
    data["test_context"]["schema_mapping"] = "Implementation representation only; no changed copy, note text, visual objects/meaning or scripted user decision. No actual approval is recorded."
    data["deck_context"] = {
        "source_summary": "Same supplied and proposed material recorded in interaction.md and original human cards; no new organization facts.",
        "canonical_terms": [{"term": key, "meaning": value} for key, value in old_deck["canonical_terminology"].items()],
        "source_readiness": copy.deepcopy(old_deck["readiness"]),
        "visible_numbering": old_deck["visible_numbering"],
        "source_card_files": ["interaction.md", "outline.draft.md", "speech.draft.md"],
    }
    data["style"] = copy.deepcopy(old_deck["style"])
    data["style"]["visual_direction"] = "; ".join(old_deck["style"].get("rules", [])) or old_deck["style"]["visual_language"]
    p = data["planning"]
    p["brief"] = {
        "audience": old_deck["audience"], "purpose": old_deck["purpose"],
        "notes_language": old_deck["language"], "tone": "Natural, clear presenter voice; supplied notes remain exact",
        "output_profile": "none", "landing_title": old_deck["landing_title"],
    }
    p["readiness"] = copy.deepcopy(old_deck["readiness"])
    p["story"] = " → ".join(old_deck["story"])
    p["shared_visuals"] = {key: {"meaning": value, "appearance": value}
                           for key, value in old_deck["shared_visual_identities"].items()}
    p["delivery"] = {"voice": "natural-presenter", "speaker_names": [], "intent": old_deck["delivery_intent"]}
    p["review_policy"] = old_deck["review_policy"]
    old_samples = copy.deepcopy(old_deck["required_representative_samples"])
    required = [x["id"] for x in old_samples]
    if case == "D3":
        # The managed schema addresses sample requirements by current slide ID.
        # Associate the same supplied style-only fixture with the provider-entry
        # visual scope; it still accepts no new content page, produces no image
        # and creates no sample event.
        required = ["slide_03"]
    p["sample_strategy"] = {"required_slides": required, "original_strategy": old_samples}
    if case == "D3":
        p["sample_strategy"]["representation_mapping"] = {
            "clean_reference_fixture": "slide_03 representative provider-entry scope; reuse the same supplied compatible style-only calibration",
            "actual_reuse_record": "not recorded; real bytes/provenance and human sample evidence remain required",
        }
    old_gen = copy.deepcopy(original["planning"]["generation"])
    p["generation"] = {
        "backend_used": old_gen["selected_image_backend"], "tool_name": "codex-gpt-image",
        "mode": old_gen["mode"], "aspect_ratio": old_gen["aspect_ratio"],
        "model": old_gen["underlying_model"], "size": old_gen["size"],
        "input_method": old_gen["input_method"], "reference_mode": old_gen["reference_mode"],
        "capability_basis": old_gen["capability_basis"],
    }
    # All content questions have the same scripted decisions. Unverified real
    # runtime evidence stays explicit outside the planning approval blockers;
    # this is a schema-complete TEST candidate, never production authorization.
    p["unresolved"] = []
    p["runtime_limitations"] = [
        "MOCK/TEST fixture only; no real backend probe, live image call or approval event",
        "Actual approved style/reference/sample bytes and acceptance provenance are not supplied",
        "Schema and draft-view acceptance cannot establish image readiness or actual human approval",
    ]
    data["slides"] = []
    slide_template = template["slides"][0]
    for idx, old in enumerate(original["slides"]):
        s = copy.deepcopy(slide_template)
        s["number"] = old["internal_order"]
        s["title"] = old["visible_copy"]["title"]
        s["intent"] = old["purpose"]
        s["role"] = old["role"]
        s["key_points"] = copy.deepcopy(old["visible_copy"]["body"])
        s["language"] = old["language"]
        s["audience_state"] = copy.deepcopy(old["audience_state"])
        s["visible_copy"] = {"title": old["visible_copy"]["title"], "body": copy.deepcopy(old["visible_copy"]["body"]),
                             "labels": copy.deepcopy(old["visible_copy"]["critical_labels"])}
        old_visual = old["visual_plan"]
        objects = copy.deepcopy(old_visual["objects"])
        descriptions = old_visual["relationships"]
        endpoints = ENDS[case][idx]
        assert len(endpoints) == len(descriptions)
        s["visual_plan"] = {
            "type": old_visual["type"], "subject": old_visual["subject"], "objects": objects,
            "relationships": [{"from": objects[a], "to": objects[b], "description": text}
                              for (a, b), text in zip(endpoints, descriptions)],
            "composition": old_visual["approximate_composition"],
        }
        s["shared_visual_ids"] = copy.deepcopy(old["shared_visual_ids"])
        s["depends_on"] = copy.deepcopy(old["depends_on"])
        s["required_images"] = copy.deepcopy(old["required_images"])
        s["speaker_notes"] = copy.deepcopy(old["speaker_notes"])
        status = "provided" if old["source_mapping"]["visible_copy"].startswith("provided") else "proposed"
        s["claim_sources"] = [{"status": status, "claim": text,
                               "source": f"{case} interaction.md and original outline.draft.md: {old['source_mapping']['visible_copy']}"}
                              for text in [s["title"], *s["visible_copy"]["body"]]]
        s["claim_sources"] += [
            {"status": "proposed", "claim": old_visual["subject"],
             "source": f"{case} original visual proposal; object and relationship wording retained exactly"},
            {"status": "provided" if old["source_mapping"]["speaker_notes"].startswith("provided") else "proposed",
             "claim": "Presenter talk for this page", "source": f"{case} original speech.draft.md: exact unchanged speaker_notes.text"},
        ]
        s["source_mapping"] = copy.deepcopy(old["source_mapping"])
        data["slides"].append(s)
    return data

preservation = []
for case, original in originals.items():
    candidate = compatible(case, original)
    candidate_path = ROOT / case / "deck_spec.draft.json"
    write_json(candidate_path, candidate)
    # Validate the actual serialized complete candidate, not an in-memory claim.
    current = json.loads(candidate_path.read_text(encoding="utf-8"))
    validate_spec(current)
    validate_result = {"operation": "planning_contract.validate_spec(serialized compatible candidate)", "result": "returned without exception"}
    result = run(f"{case} compatible draft CLI",
                 [sys.executable, SCRIPTS / "planning_views.py", "--spec", candidate_path,
                  "--deck", ROOT / case / "runtime-draft-views", "--draft"])
    assert result["returncode"] == 0, result
    cli = json.loads(result["stdout"])
    assert cli["draft"] is True
    assert cli["asset_provenance"] == []
    derived = ROOT / case / "runtime-draft-views" / "speech.draft.md"
    text = derived.read_text(encoding="utf-8")
    headings = list(re.finditer(r"^## Slide (\d+):[^\n]*$", text, re.MULTILINE))
    assert [int(h.group(1)) for h in headings] == list(range(1, len(current["slides"]) + 1))
    for i, (old, new) in enumerate(zip(original["slides"], current["slides"])):
        assert new["visible_copy"]["title"] == old["visible_copy"]["title"]
        assert new["visible_copy"]["body"] == old["visible_copy"]["body"]
        assert new["visible_copy"]["labels"] == old["visible_copy"]["critical_labels"]
        assert new["speaker_notes"] == old["speaker_notes"]
        assert new["visual_plan"]["objects"] == old["visual_plan"]["objects"]
        assert new["visual_plan"]["composition"] == old["visual_plan"]["approximate_composition"]
        assert [r["description"] for r in new["visual_plan"]["relationships"]] == old["visual_plan"]["relationships"]
        stop = headings[i + 1].start() if i + 1 < len(headings) else len(text)
        spoken = text[headings[i].end():stop].strip()
        assert spoken == old["speaker_notes"]["text"]
    after_hashes = {name: sha((ROOT / case / name).read_bytes()) for name in card_hashes[case]}
    assert after_hashes == card_hashes[case]
    preservation.append({"case": case, "existing_cards_and_interactions_byte_unchanged": True,
                         "existing_file_sha256": after_hashes,
                         "all_visible_titles_body_labels_notes_visual_objects_relationship_descriptions_equal": True,
                         "cli_derived_speech_matches_every_original_note_with_internal_blank_lines": True,
                         "preserved_fixed_pages": len(original["slides"]) if case == "D2" else 2 if case == "mixed" else 0})
    green.append({"case": case, "candidate_path": str(candidate_path), "sha256": sha(candidate_path.read_bytes()),
                  "validate_spec": validate_result, "draft_cli_returncode": result["returncode"],
                  "draft_cli_result": cli, "derived_outline": str(ROOT / case / "runtime-draft-views" / "outline.draft.md"),
                  "derived_speech": str(derived), "content_pages": len(current["slides"])})
    action_path = ROOT / case / "actions.json"
    actions = json.loads(action_path.read_text(encoding="utf-8"))
    actions["schema_application_actually_performed"] = [
        "archived original incompatible draft JSON byte-for-byte in schema-red",
        "used actual bundled --write-template and help output",
        "mapped existing content into exact template fields without changing cards, notes or decisions",
        "ran actual validate_spec against archived and compatible serialized JSON",
        "ran actual planning_views.py --draft CLI against both shapes",
        "verified derived talk, fixed-copy/note preservation and original card byte hashes",
    ]
    actions["schema_representation_only"] = [
        "top-level deck_name/language/aspect_ratio/backend/goal/style plus planning.brief replace nested deck",
        "internal_order/purpose map to number/intent; fixed title/body/notes stay exact",
        "critical_labels map to labels; approximate_composition maps to composition",
        "original relationship prose retained as description with existing-object from/to endpoints",
        "plain output maps to machine output_profile none",
        "D3 existing style-only fixture maps to slide_03 representative scope; no new sample event",
    ]
    write_json(action_path, actions)

verification = {
    "execution_provenance": "Helper authored by the isolated scenario agent; executed and evaluated by the primary agent after the helper session reached its usage limit.",
    "scope": "Actual schema validation and draft-view seam, not an all-quality pass or production readiness verdict",
    "original_archives": archive_checks,
    "observed_red": red, "observed_compatible_candidates": green,
    "preservation": preservation, "actual_commands": commands,
    "live_backend_consumed": False, "actual_approval_or_sample_events_written": False,
    "limits": [
        "Backend/reference compatibility remains the exact MOCK/TEST fixture, not a live probe result",
        "validate_spec accepts plan shape and declared semantics; it does not validate factual truth or image pixels",
        "Draft CLI success writes readable draft views and a lock file only, not canonical approved plans or approval ledgers",
        "No image attachment, sample generation, image inspection, worker dispatch, final image acceptance or PPTX assembly",
        "D3 style-only reuse is expressed against a current representative slide scope; real sample identity/bytes/evidence remain absent",
    ],
}
write_json(ROOT / "schema-verification.json", verification)

# Preserve the original verification report and extend its index with actual
# execution evidence rather than relabelling its old schema-untested disclosure.
old_verification_path = ROOT / "verification.json"
old_verification = json.loads(old_verification_path.read_text(encoding="utf-8"))
old_verification["schema_application_evidence"] = "schema-verification.json"
old_verification["compatible_candidate_and_draft_cli_cases"] = list(CASES)
old_verification["existing_cards_and_talk_preserved"] = True
write_json(old_verification_path, old_verification)

write_json(ROOT / "artifact-index.json", {
    "original_archived_incompatible_json": [f"schema-red/{case}.json" for case in CASES],
    "compatible_complete_candidates": [f"{case}/deck_spec.draft.json" for case in CASES],
    "unchanged_original_human_cards_and_talk": [f"{case}/{name}" for case in CASES for name in ("interaction.md", "outline.draft.md", "speech.draft.md")],
    "actual_cli_derived_views": [f"{case}/runtime-draft-views/{name}" for case in CASES for name in ("outline.draft.md", "speech.draft.md")],
    "verification": ["verification.json", "schema-verification.json"],
    "actual_generator_template": "bundled-template.json",
})

(ROOT / "README.md").write_text("""# Input readiness behavioral evidence

Four independent text-only applications are in D1/, D2/, D3/ and mixed/. The original whole-deck human cards and talk remain unchanged: 6, 3, 5 and 3 content pages respectively. Their interaction.md files retain the exact written questions and scripted MOCK/TEST decisions.

The original guide-shaped JSONs were actually rejected by planning_contract.validate_spec and planning_views.py --draft with `Missing deck_name`. All four original files are preserved byte-for-byte under schema-red/. schema-verification.json records their byte hashes and actual failures.

After reading the corrected portable guide, the isolated agent authored this schema replay. The primary agent executed and evaluated it after the helper session reached its usage limit. It runs actual `prepare_slide_prompts.py --help`, `--write-template` and `planning_views.py --help`; bundled-template.json is the actual generated schema template. The four deck_spec.draft.json files now use its exact required fields, existing-object relationship endpoints and claim_sources. This is implementation representation only: original title/body/notes, visual objects/composition/relationship wording and scripted choices remain the same. Plain output maps to machine `output_profile: none`. D3's same supplied style-only calibration is associated with the current slide_03 representative scope; no new sample was generated or approved.

The replay calls validate_spec against each serialized compatible candidate and runs planning_views.py --spec <candidate> --deck <case>/runtime-draft-views --draft. All four validators returned without exception and all four CLI commands exited 0. Actual CLI-derived outline.draft.md and speech.draft.md files are under runtime-draft-views/; original human cards and talk stay in each case folder. Derived notes match every original note, including all D2 supplied notes and mixed slides 1–2 with their internal blank lines. Existing interaction/card/talk file hashes remain unchanged.

artifact-index.json maps originals, compatible candidates, human cards, actual CLI views and verification artifacts. schema-verification.json preserves command argv, stdout/stderr, exit codes, returned draft hashes, preservation checks and limitations. validate_schema_application.py replays the schema mapping from immutable originals. Do not run the historical build_evidence.py over the completed artifacts; it is preserved as the first-application generator.

No live backend, images/API, managed approval ledger, compiled job, sample event, worker, final image QA or PPTX was used or created. The compatible backend/reference details remain explicitly a MOCK/TEST fixture. Draft-view success proves that the portable planning artifacts reach the actual schema/CLI seam; it does not establish factual truth, actual reference bytes, generation capability, user approval, rendered readability or complete presentation quality. No automatic all-quality pass verdict is made.
""", encoding="utf-8")

print(json.dumps({"archived_cases": list(originals), "original_actual_error": red[0]["error"],
                  "actual_validate_spec_returned": [x["case"] for x in green],
                  "actual_draft_cli_exit_zero": [x["case"] for x in green],
                  "existing_cards_and_talk_unchanged": True,
                  "real_approval_events": False, "evidence": str(ROOT / "schema-verification.json")}, indent=2))
