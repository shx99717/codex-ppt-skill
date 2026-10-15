# Predictable Deck Generation Implementation Plan

> **For the implementing agent:** Follow this plan task-by-task. Complete each step, verify it works, then move to the next.

**Goal:** Extend Codex PPT with adaptive, approved content/visual/talk planning and enforced production checks, producing coherent decks with natural speaker notes and consolidated image review.

**Architecture:** Keep full-slide raster generation and existing PPTX assembly. Use one canonical versioned deck specification, a separate human-approval ledger, deterministic prompt jobs, and the existing atomic JSON/job state utilities. Bind approvals and artifacts to scoped content fingerprints so local edits revisit affected decisions while shared changes propagate through declared dependencies.

**Tech Stack:** Existing Python 3 scripts, standard-library JSON/hashlib/unittest/tempfile, existing filelock/Pillow/python-pptx dependencies, Markdown skill instructions, and Chinese/English/Korean Docsify documentation. Add no service, database, or new image backend.

**Mode:** SELF-CONTAINED HANDOFF. A new executor needs no previous chat or memory file and must not ask the user to re-explain settled decisions. All approved requirements, authoring rules, schemas, pressure prompts, and the complete speaker-note source are embedded below. Normal session startup rules still apply; starting fresh is compatible with relying on this plan.

**Planning status:** This file is a plan, not evidence of implemented or tested new behavior. The user selected handoff planning, not execution in this session. Code examples below are proposed implementation material; run their corresponding RED tests before copying them into production files.

**Review revision:** The user selected revision of the four Important handoff findings. This version aligns prompt/hash context, semantic talk bindings, policy approval records, and draft asset normalization. Appendix G supplies focused reference-contract checks; runtime implementation and verification remain the executor's work. The historical review and its resolution record are saved separately.

---

## Section 0: Full Context

### 0.1 Why and background

The user wants to avoid a long image-generation run ending in an unexpected deck. A topic or rough paragraph needs guided development; complete slide-by-slide Markdown should preserve ready content and require less preparation. Agent intelligence should recommend concrete content and visuals without making unsupported factual guesses or imposing an interview for every page.

A deck is an interconnected presentation. Recurring entities and terms must retain meaning, numbering and cross-references follow an agreed scheme, and the story progresses sensibly. Speaker delivery is equally important: the talk should sound like someone explaining the subject in the room, with breathing beats and purposeful transitions.

The earlier proposal was premature; the user explicitly restarted clarification and then approved the following workflow section by section. Implement these decisions, not abandoned candidate defaults from older documents.

### 0.2 Confirmed decisions: do not re-litigate

1. Predictability locks approved facts, messages, visible wording, and intended visual structure. Minor raster-rendering differences are acceptable. Pixel-identical geometry and native editable slide objects are outside scope.
2. Quality first, time second. No fixed five-to-ten-minute review target, question quota, fixed outline bullet count, or per-slide interview.
3. Assess content and visual readiness separately, including mixed readiness across slides. Extract known decisions and preserve prepared structure/wording. Recommend changes separately.
4. Clarify consequential intention before expanding content: audience, purpose, prior knowledge, intended outcome, tone, language, context, scope, and length are examples, not a closed questionnaire. Choose and order genuinely missing questions intelligently.
5. Thin input permits clearly identified proposed explanations/examples. Missing organization facts, measurements, and important decisions require input or an explicitly approved omission; never invent numerical evidence.
6. Implement adaptive planning inside Codex PPT. Do not make personal clarify-requirements or brainstorming skills mandatory installation dependencies.
7. Prepare one whole-deck content/visual plan with exact visible copy, critical labels/values, visual type, objects/relationships, approximate layout, assets, and unresolved gaps. Review the plan by exception. Simple structural previews are planning artifacts, never final slide-rendering substitutes.
8. Plan the complete story, shared visual identities, terminology, reference relationships, and numbering scheme. Numbering examples do not mandate visible page numbers. Give workers shared references plus relevant neighboring/dependency context; inspect the complete sequence as well as each slide.
9. After plan approval, choose one representative content sample; reuse a suitable existing approved sample. Justify additional samples for substantially different visual requirements. Accepted samples become shared style references; layouts still serve slide roles.
10. Production uses the current approved plan, assets, and accepted samples. Missing/stale approval stops full generation. Workers preserve approved copy/relationships and raise substantive changes or fit problems before changing them.
11. Revisions identify affected slides and shared dependencies and revisit the affected decisions. A global change may affect the whole deck.
12. Consolidated review is the revised skill's recommended default; strict batch review remains an alternative. State the chosen process in each deck's plan. Agent QA and actual user approval are separate. Users review the whole image set, name exceptions, then review corrections and affected connections. Final assembly requires user approval of current images.
13. Inspect the first production batch before continuing. Pause repeated problems and fix their common cause. Allow one targeted automatic repair per affected slide for an isolated rendering problem; escalate failures with a recommendation, grouping independent exceptions where practical. Further attempts require authorization. A retry limit never permits delivery of unresolved errors.
14. Notes may explain approved facts and transitions; new substantive claims need approval. No fabricated personal experience or presenter names.
15. Natural speaker voice applies across presentation types: appropriate first person, warmth, everyday work vocabulary, technical terms introduced when needed, concrete before abstract, thought-sized breathing beats, natural connectors, and purposeful transitions. Match presentation language and intended speaking time.
16. Draft notes alongside the slide plan, show a representative note to calibrate voice, and review the complete talk by exception before expensive image generation. Reuse supplied notes and flag revisions.
17. The complete original speaker-note message is authoritative and preserved verbatim in Appendix A. Its example topics/names illustrate voice, not facts to insert into future decks.
18. Keep plain/Medavis/both output, supported ratios, backend provenance, source-image fidelity rules, multilingual slide handling, personal style-library behavior, and image-based output.
19. The user selected this self-contained handoff plan. No implementation, installation, live deck generation, new thread, commit/push, merge, or publication is authorized by this planning request.

### 0.3 Environment, branch, and historical evidence

- Repository here: `D:/git/codex-ppt-skill`, PowerShell on Windows; adjust the checkout root if relocated.
- Continue `feature/SQ5GEN-predictable-deck-generation`. Do not modify `main` directly or invent another branch/task ID.
- Task ID: `SQ5GEN-195`.
- Last published feature checkpoint: `99fba3d3ea2d8f1d285cf40dbf44d8e32f05d126`, tracking `origin/feature/SQ5GEN-predictable-deck-generation`.
- Earlier documentation checkpoint: `ae15e634d6a9630422082de2904364be979faca5`.
- Local main at planning time: `dc65c44c8b8fcef60c3073e7203856cfa3598b2f`.
- The approved design, memory, speaker-note source, this plan, and its execute prompt can be uncommitted local files. Preserve them and unrelated user edits. A different checkout needs this plan and its companion prompt; it does not need the original chat.
- Known shared interpreter here: `C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe`. On other hosts locate the existing shared venv; do not install/update it automatically.
- Earlier work ran 75 existing unit tests successfully and demonstrated that the current prompt compiler accepts a spec without plan approval/layout/sources/backend/sample. This is historical evidence only; rerun relevant tests yourself.
- Current dispatch stores a prompt-file SHA but result recording does not compare it. Current image review is stronger: approval checks the PNG SHA.
- Current assembly checks aspect ratio but not job/approval readiness; notes map from `speech.md` headings to content slides.
- Raster generation cannot guarantee exact lettering, diagram fidelity, or unchanged source-chart pixels. Input/state validation and human/visual inspection have distinct responsibilities.

### 0.4 Project rules and guardrails

Appendix B reproduces the repository's project rules. Additional confirmed conventions:

- Commit format, only after explicit publication authorization: `[SQ5GEN-195] <type>: <description>`. English Conventional Commits; English Conventional Commit PR title.
- Non-trivial changes go through a PR. Update all existing Chinese/English/Korean README and usage-site counterparts together.
- Add user-visible behavior to English `CHANGELOG.md` under `## Unreleased`. Add the actual PR number after a PR exists; never invent one.
- Do not bump a release version, tag, release, push, merge, publish, run installer/uninstaller/deploy scripts, delete a worktree, or change installed personal skills as part of execution without the relevant explicit authorization.
- The user's previous `no code review needed` instruction applied to the second documentation publication checkpoint; it is not a blanket waiver of feature verification or future review.
- Use existing feature checkout; no worktree creation or task messaging is required.
- Keep agent communication plain and speakable for this user; one numbered selection question at a time. Device mode is mobile unless explicitly switched. A future deck's audience/language/timing are deck-specific.
- Use normal-speed focused agents if authoring tests require them; no model downgrade or fast mode without user instruction. Read-only test agents must not ask the real user questions or commit/edit the checkout.

### 0.5 Repository map and compatibility seams

| File | Existing behavior / planned integration |
|---|---|
| `skills/codex-ppt/SKILL.md` | Main orchestration, gates, worker ownership, completion checks. |
| `skills/codex-ppt/docs/workflow-gates-and-progress.md` | Currently mandatory wave review; replace with chosen managed review policy and evidence. |
| `skills/codex-ppt/docs/outline-style-and-sample.md` | Currently broad outline and one sample; integrate adaptive whole-deck plan and representative samples. |
| `skills/codex-ppt/docs/project-assembly-and-reporting.md` | Notes currently finalized near assembly; already asks for natural presenter talk. Strengthen rhythm/timing and earlier drafts. |
| `skills/codex-ppt/docs/slide-generation-and-subagents.md` and `prompts/slide-worker.md` | Complete job context, backend/asset rules, impact analysis; add approved-copy/shared-reference boundaries. |
| `skills/codex-ppt/scripts/prepare_slide_prompts.py` | `_build_prompt`, `_job_images`, `_write_template`, `main`; currently writes jobs before any plan-approval validation. |
| `skills/codex-ppt/scripts/slide_run_state.py` | `locked_json`/`locked_jobs` use FileLock and atomic replace; release jobs lock before syncing run-state summaries. |
| `record_slide_dispatch.py` | Currently pending→dispatched; stores agent ID and prompt SHA and clears image review. |
| `record_slide_result.py` | Checks status/agent/backend/ratio; copies final PNG then records provenance. Add checks before copying. |
| `record_user_review.py` | Currently one `--slide`, approve/clear, recorded-only, SHA-bound review. Extend atomically to sets. |
| `slide_job_status.py` | Current status/concurrency summary. Add QA/review/staleness/repair summary without changing scheduling capacity. |
| `assemble_ppt.py` | `get_slide_images` sorts numeric filenames; `load_speaker_notes` reads `## Slide N`; CLI derives project folder from output basename. |
| `tests/smoke-deck/` | Existing image/PPTX fixture and verifier; preserve branded counts and note offsets. |

Existing assembly CLI: `assemble_ppt.py BASE_DIR OUTPUT.pptx --aspect-ratio {16:9,4:3,3:2} --template {none,medavis,both} --landing-title TITLE`; `--init` creates directories only.
For managed decks, internal content numbers are 1..N in plan order. Visible numbering is a separate approved scheme. Plain = N pages; Medavis = landing + N content + ending = N+2. Existing branded wrapper pages have no content talk track; preserve content-note offsets and wrapper behavior.

### 0.6 Concrete implementation choices

These choices implement the approved workflow; they are technical plan decisions, not new user requirements.

**Canonical input:** Keep `deck_spec.json` as source of truth, with `workflow_version: 2`. Before approval use `deck_spec.draft.json` and `speech.draft.md`. Do not keep separately editable copies of approved content. Generate `outline.md` and `speech.md` from the approved spec.

**Ledger:** Add `plan_approvals.json` for human decision events, scoped plan/talk approval, sample approval, and additional retry authorizations. Preserve `slide_jobs.json` for compiled jobs, dispatch/results, QA, repair counts, and actual image review. Update via atomic writes and locks.

**Scoped fingerprints:** One canonical render-context projection supplies both image prompts and visual hashes: global visual context, local visual payload, used shared elements, reachable declared dependencies, and required-asset bytes. The talk projection also includes approved visible content, critical values, claims/evidence, source bytes, and relevant visual meaning, alongside delivery context and note text/purpose/timing. Pure typography/color/composition changes do not invalidate talk; note-only changes do not invalidate images. Keep a full-plan audit hash, but evaluate scoped bindings before invalidating unrelated artifacts. The main agent updates meaningful dependencies; hashes cannot discover hidden meaning or prove factual truth.

**Output approval:** A separate policy fingerprint covers review policy, output profile, and landing title. Store that fingerprint and the approved values with an actual policy-scoped user event. Image/talk approval is insufficient for a changed output choice.

**Asset roots:** Resolve draft-relative paths against the original draft's parent before the approval view/fingerprint, then install normalized absolute original-source paths into the canonical spec. Keep declared spelling/source-root provenance in the decision history. Workers consume byte-identical hash-named snapshots; preflight still checks original-source paths/hashes for drift. Moving the spec must not change asset identity.

**Calibration:** `--phase sample` validates current content/talk approval but does not require the sample it is about to create. `--phase production` also requires current sample approvals. A suitable approved sample can remain style-only when its own content is outdated; it cannot remain an accepted final slide unless its visual binding is current.

**Immutable style inputs:** On sample approval, copy the approved bytes to `references/approved_samples/<sha256>.png` and bind the style reference to that immutable copy. Track accepted-final-slide approval separately against `origin_image/slide_XX.png`. A rendering repair of that final page must not overwrite the shared style reference or invalidate unchanged unrelated images merely because a mutable sample pathname changed. New style acceptance follows changed style/config bindings; style-only reuse still needs recorded suitability for the required visual approach. Strict source assets retain their declared original path/hash for drift checks; workers can use hash-named byte-identical snapshots to avoid consuming an externally changed file during generation.

**Fail-closed managed commands:** All new skill runs use v2 and enforced CLI gates. Preserve old manual/image-only capability through explicit `--legacy-unmanaged` flags on the affected CLI tools. Reject that flag if v2 spec/ledger/job markers are present. Update old CLI tests to opt into legacy where they test legacy behavior; add tests that missing/malformed managed metadata does not automatically become legacy. Keep public image/assembly utility functions usable by legacy callers.

**Prompt integrity:** Store compiled job SHA outside the job in the ledger. Validate before dispatch and compare the current file with the dispatch SHA before result copying. Repair instructions are a compiler input from recorded QA, not ad hoc edits to prompt JSON.

**Locks:** Use one `.planning.lock` outer lock for managed mutations, then existing jobs lock when needed. Release jobs lock before acquiring run-state locks. Do not introduce opposite lock order. Validate complete selections before mutating bulk approvals. Files changed by external tools outside locks must be rechecked at consumer boundaries.

**Review:** A real bulk decision can create per-image SHA-bound records pointing to one decision ID. It must not fabricate per-slide conversations. Samples accepted as final slides need valid sample evidence and current visual/image bindings; agent QA does not count as approval.

### 0.7 Managed specification and ledger examples

The following is a complete draft fixture, not a claim that a user approved this hypothetical deck:

```json
{
  "workflow_version": 2,
  "deck_name": "shared-account",
  "language": "English",
  "aspect_ratio": "16:9",
  "selected_image_backend": "scripts/image_gen.py",
  "goal": "Explain why a shared account helps",
  "deck_context": {
    "core_claim": "One account simplifies access",
    "canonical_terms": ["shared account"],
    "source_summary": "Illustrative, qualitative training example; no measured claims"
  },
  "style": {
    "name": "clean-professional",
    "visual_direction": "plain, readable diagrams",
    "color_palette": "navy and teal on white",
    "typography": "clear large headings"
  },
  "planning": {
    "brief": {
      "audience": "Technical colleagues",
      "purpose": "Explain the proposed access model",
      "notes_language": "English",
      "tone": "Conversational and precise",
      "output_profile": "none",
      "landing_title": null
    },
    "readiness": {"content": "partial", "visual": "missing"},
    "story": "Start with the access problem, then explain the shared-account model.",
    "shared_visuals": {
      "account": {"meaning": "One account", "appearance": "teal key icon"}
    },
    "delivery": {"voice": "natural-presenter", "speaker_names": []},
    "review_policy": "consolidated",
    "sample_strategy": {"required_slides": ["slide_02"]},
    "generation": {
      "backend_used": "scripts/image_gen.py",
      "tool_name": "scripts/image_gen.py",
      "mode": "generate",
      "aspect_ratio": "16:9",
      "size": "2560x1440"
    },
    "unresolved": []
  },
  "slides": [
    {
      "number": 1,
      "title": "One account, fewer access steps",
      "role": "opening",
      "intent": "Introduce the proposed simplification",
      "key_points": ["Explain the qualitative access problem"],
      "visible_copy": {"title": "One account, fewer access steps", "body": [], "labels": []},
      "visual_plan": {
        "type": "illustration",
        "subject": "A shared account",
        "objects": ["account"],
        "relationships": [],
        "composition": "Title above a single account symbol"
      },
      "shared_visual_ids": ["account"],
      "depends_on": [],
      "claim_sources": [{"claim": "Qualitative illustrative proposal", "status": "proposed", "source": "Approved example"}],
      "required_images": [],
      "speaker_notes": {
        "text": "Hi everyone.\n\nLet me show you one way to make access simpler.\n\nFirst, we will look at the model.",
        "speaking_time_seconds": 20,
        "transition": "Introduce the model"
      }
    },
    {
      "number": 2,
      "title": "The shared-account model",
      "role": "explanation",
      "intent": "Show the model's relationships",
      "key_points": ["Explain the links without quantitative claims"],
      "visible_copy": {"title": "The shared-account model", "body": [], "labels": ["Shared account", "Provider"]},
      "visual_plan": {
        "type": "diagram",
        "subject": "Access relationships",
        "objects": ["account", "provider"],
        "relationships": [{"from": "account", "to": "provider", "label": "Access"}],
        "composition": "Account on the left, provider on the right"
      },
      "shared_visual_ids": ["account"],
      "depends_on": ["slide_01"],
      "claim_sources": [{"claim": "Illustrative relationship", "status": "proposed", "source": "Approved example"}],
      "required_images": [],
      "speaker_notes": {
        "text": "Now, here is the model.\n\nThe key is the same account we just introduced.\n\nThat is the proposal. What questions do you have?",
        "speaking_time_seconds": 30,
        "transition": "Close and invite questions"
      }
    }
  ]
}
```

Fixture parameters are test data, not proof of live backend capabilities. Inspect actual tools and measured pixels before a real run; never copy these parameters into an incompatible native tool schema.

Validate before approving: correct scalar/object/list types, finite JSON numbers, supported ratio and explicit backend, nonempty audience/purpose/notes language, nonempty visible title consistent with `title`, visual objects/relationships/composition, note text, normalized required-image dictionaries, unique consecutive internal IDs, existing dependencies/shared IDs, and no unresolved factual blockers/`needs_input` claims. Declared speaking time can be null when genuinely unspecified; derive a proposed estimate or ask only if timing affects scope. No compulsory body-bullet count.

Do not include legacy `sample_approved` booleans, `approved_style_reference` paths, or runtime `sample_generation_method` as authored authority in v2. Derive them from validated sample ledger/config when adapting existing compiler code.

Ledger shape after actual decisions:

```json
{
  "workflow_version": 2,
  "events": [
    {"id": "decision-001", "actor": "user", "evidence": "Actual combined approval wording or interaction reference", "scopes": ["visual", "talk", "policy"], "timestamp": "2026-10-14T12:00:00Z"},
    {"id": "decision-002", "actor": "user", "evidence": "Actual sample acceptance wording or interaction reference", "scopes": ["sample"], "timestamp": "2026-10-14T12:05:00Z"}
  ],
  "policy": {
    "value": "consolidated", "output_profile": "none", "landing_title": null,
    "policy_hash": "sha256", "event_id": "decision-001"
  },
  "slides": {
    "slide_01": {"visual_hash": "sha256", "notes_hash": "sha256", "event_id": "decision-001"},
    "slide_02": {"visual_hash": "sha256", "notes_hash": "sha256", "event_id": "decision-001"}
  },
  "samples": {
    "slide_02": {
      "image": "references/approved_samples/sha256.png",
      "image_sha256": "sha256",
      "style_hash": "sha256",
      "visual_family": "diagram",
      "backend": "scripts/image_gen.py",
      "event_id": "decision-002",
      "accepted_final": {"path": "origin_image/slide_02.png", "image_sha256": "sha256", "visual_hash": "sha256"}
    }
  },
  "extra_repairs": {}
}
```

Store approval evidence only after an actual user decision. CLI data records trust in the agent's transcription of that decision; it is not cryptographic proof of a human interaction.

---

## Task 1: Capture skill and script RED baselines

**Files**

- Create: `docs/plans/evidence/2026-10-14-predictable-deck-red.md`.
- Create: `skills/codex-ppt/scripts/tests/test_managed_preparation.py`.
- Use unchanged skill snapshot: `skills/codex-ppt/`.
- Future test helpers: `skills/codex-ppt/scripts/tests/planning_fixtures.py`.

**Step 1:** Read the authoring/test requirements in Appendix C. Create isolated text-only application/pressure scenarios from Appendix D before editing any skill instructions. Test agents receive only the unchanged Codex PPT skill and their scenario, not this approved design, memory, new guides, or plan.

**Step 2:** Run the scenarios against that baseline. Save scenario, input, actual returned artifacts/tool sequence, exact failure/rationalization wording, and the evaluated criterion. Do not invent a RED failure if a scenario already passes; preserve passing baseline behavior and find the actual gaps. Use simulated generation tools, not paid image calls. Test agents operate only in temporary scratch directories and return questions as scenario output rather than contacting the real user.

**Step 3:** Add this integration regression first, using the complete fixture in Section 0.7:

```python
def test_managed_production_refuses_missing_approval(self):
    with tempfile.TemporaryDirectory() as tmp:
        deck = Path(tmp) / "deck"
        deck.mkdir()
        spec_path = deck / "deck_spec.json"
        spec_path.write_text(json.dumps(managed_spec()), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPTS / "prepare_slide_prompts.py"),
             "--spec", str(spec_path), "--out-dir", str(deck)],
            capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("approval", (result.stdout + result.stderr).lower())
        self.assertFalse((deck / "prompts").exists())
```

Include imports/class/main and the existing test convention: `SCRIPTS = Path(__file__).resolve().parents[1]`, insert it into `sys.path`, `managed_spec()` returns a fresh copy of the fixture. Do not reuse a mutable fixture between tests.

**Step 4:** Run and record the expected assertion failure before implementation:

```powershell
$pptPython = 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe'
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_managed_preparation.py
```

Expected baseline: current compiler succeeds and writes jobs, so the rejection assertion fails. If baseline has changed, inspect actual behavior and adjust the regression to the demonstrated gap, not to force a predetermined transcript. Record exit status and artifact absence/presence.

**Step 5:** Run the existing suite as a fresh baseline:

```powershell
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p 'test_*.py'
```

Expected: existing tests pass; report the observed count. Stop on unrelated baseline failures rather than attributing them to this feature.

## Task 2: Add contract validation and scoped fingerprints

**Files**

- Create: `skills/codex-ppt/scripts/planning_contract.py`.
- Create: `skills/codex-ppt/scripts/tests/test_planning_contract.py`.
- Create fixture helper: `skills/codex-ppt/scripts/tests/planning_fixtures.py`.

**Step 1:** Write tests before the module exists: same manifest and prompt bytes across dictionary order; local slide change affects itself/dependents but not an unrelated slide; unused shared elements change neither scoped prompt nor visual binding, while used elements do; note-only changes invalidate talk without changing image prompts/bindings; changed facts/critical values/claim evidence/source bytes invalidate affected talk and dependents; pure color/typography/composition changes leave talk valid; global story/style changes affect relevant image bindings; missing/deleted assets fail; unknown dependencies/shared IDs, duplicate internal numbers, unresolved claims, unsupported ratio, null backend, nonfinite values, malformed types fail. Test normalized outside-deck draft paths, destination-name conflicts, and missing assets before installation. Include cyclic cross-references without recursive-hash loops; either support their reachable closure as below or reject explicitly and document the constraint. Appendix G provides reference expectations; convert them into meaningful production-module regressions, not merely tests of copied examples.

**Step 2:** Run `test_planning_contract.py`; expected RED is missing module/API or the targeted assertion. Save evidence.

**Step 3:** Implement a complete deterministic hash kernel like the following, after writing the validation tests. This code is the hash/closure portion, not a replacement for the explicit `validate_spec` and ledger gates specified next:

```python
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
    }


def require_policy_approval(manifest: dict, ledger: dict) -> None:
    record = ledger.get("policy")
    expected = manifest["policy"]
    if not isinstance(record, dict) or record.get("policy_hash") != manifest["policy_hash"]:
        raise ContractError("Missing or stale policy approval")
    approved = {
        "review_policy": record.get("value"),
        "output_profile": record.get("output_profile"),
        "landing_title": record.get("landing_title"),
    }
    if approved != expected:
        raise ContractError("Policy approval values conflict with fingerprint")
    events = ledger.get("events", [])
    if not isinstance(events, list):
        raise ContractError("Malformed approval events")
    event = next((
        e for e in events
        if isinstance(e, dict) and e.get("id") == record.get("event_id")
    ), None)
    if not event or event.get("actor") != "user" or not isinstance(event.get("evidence"), str):
        raise ContractError("Policy approval requires an actual user event")
    if not event["evidence"].strip() or "policy" not in event.get("scopes", []):
        raise ContractError("User event does not approve policy")
```

`build_contexts` is the single semantic projection for managed rendering and hashing. Prompts serialize its selected visual context with sorted JSON keys; never serialize the unfiltered shared registry or raw dependency slides. Backend jobs and source-image selections must use this same context, plus separately bound immutable sample/repair inputs. Audit any new compiler field. Cross-slide dependencies cover approved semantic relationships; update them after impact analysis.

Talk semantics include all declared source images and used shared source assets conservatively. Calibration/style-only PNGs belong to the separate sample ledger, not these source lists. Changing pure style/appearance/composition or sample pixels does not change talk unless its approved meaning changes. Exact visible labels contain critical values; if new structured data/semantic fields are added, explicitly extend the talk projection and tests. Hashes invalidate a stale contract; they do not prove truth, consistency, or natural speech.

**Step 4:** Implement `validate_spec(spec) -> None` with the exact Section 0.7 conditions. Reject authored runtime sample approval fields in v2 rather than ignoring competing authorities. Review policy enum = `consolidated`/`strict`. Output profile = `none`/`medavis`/`both`; branded profiles require a landing title. For generation parameters, validate consistency with selected backend and locked ratio; live tool capability verification stays with orchestration.

**Step 5:** Add shared gate API with these concrete signatures and behavior:

- `load_managed_spec(deck_dir: Path) -> dict`: require v2, parse current canonical spec, no implicit fallback.
- `require_plan_approval(deck_dir: Path, manifest: dict, slide_ids: list[str]) -> dict`: validate the ledger schema/events, call `require_policy_approval(manifest, ledger)`, compare selected visual/note hashes, and require no blockers. Return ledger. Reject missing policy hashes or output snapshots; never infer policy approval from unchanged slide hashes.
- `require_samples(deck_dir: Path, spec: dict, manifest: dict, ledger: dict) -> list[dict]`: required sample IDs approved, current image bytes, style/backend/ratio bindings match; return exact style input references.
- `require_job_current(deck_dir: Path, jobs: dict, slide: dict) -> dict`: verify scoped visual binding, compiler job-file SHA, and selected phase/sample requirements.
- `require_managed_ready(deck_dir: Path, output_profile: str, aspect_ratio: str, landing_title: str | None) -> None`: Task 6 assembly conditions.
- `require_legacy_allowed(deck_dir: Path) -> None`: fail if any v2/approval marker is present.
- `planning_lock(deck_dir: Path)`: existing FileLock style outer lock, no nested run-state locks.

**Step 6:** Run targeted tests GREEN; refactor with the same tests. Draft views resolve against the original draft parent; canonical managed specs store absolute original-source paths, so their parent is only a defensive resolver base. Keep hash identity unchanged across installation. Preserve source declaration/root provenance in the approval event; test required and shared assets, including conflicting destination filenames.

## Task 3: Record actual plan/talk/sample decisions and derived views

**Files**

- Create: `skills/codex-ppt/scripts/record_plan_approval.py`.
- Create: `skills/codex-ppt/scripts/planning_views.py`.
- Create: `skills/codex-ppt/scripts/tests/test_record_plan_approval.py`.
- Create: `skills/codex-ppt/scripts/tests/test_planning_views.py`.
- Modify: `skills/codex-ppt/scripts/planning_contract.py`.

**Step 1:** Write RED tests for whole-plan approval, actual evidence required, scoped revision approval, unaffected records retained, factual revisions staling affected talk, shared changes staling dependents, note-only edits, stale/deleted/changed samples, approved style-only reuse versus accepted-final validity, and drafting without false approval. Include missing/stale policy fingerprints, policy-only approval, scoped edits retaining unchanged policy approval, and outside-deck drafts with source-name conflicts. A changed draft/source between displayed approval candidate and recording must fail without altering canonical spec/ledger.

**Step 2:** Implement these exact CLI groups; print JSON summaries suitable for the main agent:

```text
record_plan_approval.py DECK --spec DRAFT --approve --scope all --expected-plan-hash HASH --evidence TEXT
record_plan_approval.py DECK --spec DRAFT --approve --scope slides --slides slide_02,slide_03 --expected-plan-hash HASH --evidence TEXT
record_plan_approval.py DECK --spec DRAFT --approve-policy --expected-plan-hash HASH --evidence TEXT
record_plan_approval.py DECK --approve-sample slide_02 --image PATH --backend-used LABEL --evidence TEXT
record_plan_approval.py DECK --authorize-repair slide_02 --additional-attempts 1 --evidence TEXT
```

Require nonempty evidence and genuine user decisions; agent QA is not human approval. Events have stable IDs, explicit `scopes` lists, and UTC timestamps. `--scope all` approves visual, talk, and policy together when the actual decision did; slide-scoped approval does not implicitly approve changed output policy. It may combine `--approve-policy` only when the real decision includes it. Policy-only approval records only policy and retains unchanged slide decisions.

Before approval, draft views call `normalize_asset_paths` against `DRAFT.parent`, present the resulting candidate, and return its manifest/audit hash to the main agent. Keep technical hashes out of spoken approval cards. At recording, require `--expected-plan-hash` to match that reviewed candidate; normalize using the original root before installation. Preserve raw declared paths/root and original absolute paths/hashes in event provenance. Do not re-resolve a draft relative to the destination deck.

Under the planning lock, validate the complete candidate and requested decision scopes first. Snapshot source bytes to hash-named references, verify snapshot and source bytes still match the reviewed manifest, then install the normalized canonical spec and update scoped records via the repository's atomic-write conventions. Validation/copy failures leave previous spec/ledger intact; any cross-file commit interruption must fail closed on revalidation. Missing assets/blockers refuse approval. Workers use exact snapshots; consumers also recheck original-source drift.

Policy records store `value`, `output_profile`, `landing_title`, `policy_hash`, and `event_id`. A changed policy remains stale unless this decision genuinely approves it; never refresh its hash because slide approval succeeded. Call the same policy gate at preparation and assembly. Retain previous event IDs for unchanged scopes.

For a revision, leave newly affected, unapproved bindings stale. Do not relabel an unchanged old decision as a new user approval; preserve its event and bind only genuinely unchanged scope. Human approval of a whole plan authorizes all approved content/talk cards by that decision, not individual conversations.

**Step 3:** Build the readable outline and notes from the same spec. This helper preserves internal blank lines and current note parsing:

```python
def speech_markdown(spec: dict) -> str:
    blocks = []
    for slide in spec["slides"]:
        text = slide["speaker_notes"]["text"].replace("\r\n", "\n").strip()
        blocks.append(f"## Slide {slide['number']}: {slide['title']}\n\n{text}")
    return "\n\n".join(blocks) + "\n"
```

`planning_views.py --spec PATH --deck DECK --draft` writes only `outline.draft.md`/`speech.draft.md` and returns normalized candidate `plan_hash` plus asset provenance in its JSON summary. Final views require current approved scoped content/talk/policy. Include source/assumption status, visual brief, shared dependencies, spoken intent, timing, and exceptions in the readable plan; keep technical hash state out of user approval cards.

**Step 4:** Run targeted tests GREEN:

Add a regression where an accepted sample's final content page is repaired while its approved immutable style snapshot stays unchanged. Existing other slides retain valid style-input provenance; the repaired final page requires fresh current-image approval. A changed shared style or snapshot content still invalidates the appropriate scope.

```powershell
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_record_plan_approval.py
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_planning_views.py
```

Expected: approval records remain tied to real events/current scope; generated notes retain breathing spaces and per-slide mapping. Do not run live image generation.

## Task 4: Compile managed jobs and allow calibration without bypasses

**Files**

- Modify: `skills/codex-ppt/scripts/prepare_slide_prompts.py`: `_build_prompt`, `_job_images`, `_write_template`, `main`.
- Modify tests: `skills/codex-ppt/scripts/tests/test_managed_preparation.py`.
- Modify existing CLI fixtures where explicit legacy flags are necessary: `test_prepare_slide_ratio.py`, `test_slide_language.py`.
- Create: `skills/codex-ppt/scripts/tests/test_prompt_contract.py`.

**Step 1:** RED tests: missing/stale plan/talk/policy approval blocks without output directories; sample phase succeeds after plan approval without a sample; production requires samples; calibrated sample/source drift fails; no fake approval shortcuts; override backend/ratio mismatch fails; exact copy/labels and filtered shared/dependency context appear in jobs; dictionary order, unused shared definitions, concurrency tuning, and note-only edits do not change render prompts/bindings; referenced content does. Assert dependency notes are excluded. Image inputs must be the approved byte-identical snapshots, not destination-relative lookalikes.

**Step 2:** Add CLI `--phase {sample,production,repair}` (default production), `--slides IDS`, and explicit `--legacy-unmanaged`. Require sample selection IDs in sample phase; do not schedule the entire deck by accident. Existing write-template produces an honest v2 draft with no true approval booleans or nonexistent accepted samples.

Before `prompts_dir.mkdir` or any save, acquire planning lock, read/validate canonical spec/ledger, compute manifest and check all prerequisites for the selected phase. In v2, reject conflicting `--selected-backend` overrides; capacity tuning remains separate.

**Step 3:** Extend prompt assembly with exact blocks, populated from the canonical schema:

```python
def approved_prompt_blocks(render_context: dict) -> str:
    # This is exactly the selected visual_contexts[sid] from build_contexts.
    # Sorted serialization matches the hash's dictionary-order invariance.
    return "\n\n".join([
        "APPROVED RENDER CONTEXT — visible_copy fields are exact slide text:\n" +
        json.dumps(render_context, ensure_ascii=False, sort_keys=True,
                   indent=2, allow_nan=False),
        "Use the local slide as the output slide; dependencies are context only. "
        "Preserve approved wording, values, objects, and relationships. "
        "Do not render source paths or metadata as visible copy. "
        "Raise a blocker if the approved material cannot fit; do not add claims.",
    ])
```

For managed jobs, obtain `canonical, visual_contexts, note_contexts = build_contexts(spec, deck_dir)` and use only `visual_contexts[sid]` for approved semantic prompt content, dependency/shared context, and source-image selection. `_build_prompt` must not append raw spec fields or unfiltered dependency dictionaries to managed prompts. Fixed worker instructions, separately approved sample/config bindings, and recorded repair inputs remain bound in the immutable job SHA. Use existing real input-image mechanisms with verified snapshots. Samples do not authorize another slide's copy/layout. Full speaker-note text is excluded from image context; speaking intent is the approved slide intent.

**Step 4:** Add phase, plan audit hash, slide visual binding, style/sample fingerprints, asset snapshots, and backend config to each job. Store job SHA in `slide_jobs.json` outside the job file.

For `--force`, validate the entire selection before writing. Preserve unaffected current results/reviews when recompilation yields unchanged bindings/job content; never reset every slide's state blindly. Changed bindings invalidate only affected outputs and decisions. A forced rewrite is not human approval.

Do not rewrite an unchanged job solely to stamp a new full-plan audit hash after an unrelated or note-only revision. Its original audit version remains generation provenance while its scoped visual binding is checked against the current plan. Refuse replacement of a currently dispatched job; finish or explicitly invalidate that attempt before changing its file. This preserves prompt-SHA integrity without forcing unrelated image regeneration.

**Step 5:** Run compiler/prompt/language/ratio tests GREEN. The Task 1 missing-approval regression must now pass.

## Task 5: Enforce dispatch/result integrity, QA, and bounded repair

**Files**

- Modify: `skills/codex-ppt/scripts/record_slide_dispatch.py`, `record_slide_result.py`, `slide_run_state.py`, `slide_job_status.py`.
- Create: `skills/codex-ppt/scripts/record_slide_qa.py`.
- Create: `skills/codex-ppt/scripts/tests/test_managed_lifecycle.py`.
- Create: `skills/codex-ppt/scripts/tests/test_record_slide_qa.py`.
- Update legacy CLI wrappers in `test_backend_family.py`, `test_record_slide_result_ratio.py`, `test_slide_job_status.py` as needed.

**Step 1:** RED tests: stale job/approval rejects dispatch; changed prompt after dispatch rejects result before copying; source/sample drift rejects; wrong agent/backend/ratio continues to fail; fresh result clears stale user QA/review; QA pass is SHA-bound; one automatic repair per scoped visual contract; second repair requires an actual authorization event; repeated batch failure pauses further production; notes-only revision retains unchanged image bindings.

**Step 2:** Before dispatch state changes, call current managed gates and compare compiled job SHA. Keep pending→dispatched transitions and agent provenance. For samples, use sample-phase gates, not production's sample prerequisites.

Before source copy in result recording, add the exact comparison:

```python
prompt_path = resolve_deck_path(deck_dir, dispatch["prompt"])
if sha256_file(prompt_path) != dispatch.get("prompt_sha256"):
    raise SystemExit("Prompt changed after dispatch; recompile and redispatch")
require_job_current(deck_dir, jobs, slide)
```

Require the relevant current plan/assets/sample bindings as well. Preserve backend-family and ratio checks. Record scoped binding and actual source/final SHA with result; clear old QA/review for replaced images.

**Step 3:** Implement:

```text
record_slide_qa.py DECK --slide ID --pass --evidence TEXT
record_slide_qa.py DECK --slide ID --needs-repair --evidence TEXT
record_slide_qa.py DECK --slide ID --blocked --evidence TEXT
record_slide_qa.py DECK --deck-pass --evidence TEXT
```

QA stores `actor: agent`, image SHA, scoped visual hash, checks/evidence, and issue status. Deck-pass binds the ordered image set, current approved note hashes, and a complete-sequence assessment. Never populate human approval from this helper.

A needs-repair decision creates compiler-owned repair instructions and a pending repair attempt, clearing affected image approvals. Count a repair when dispatching the repair job, not every time status is queried. Keep counters for a scoped visual contract; do not reset them merely because a prompt changed. One automatic repair is allowed; extra attempts consume explicit `extra_repairs` events. Reject unauthorized second repair before dispatch.

The first production batch must be agent-QA checked before later production dispatch. Record the actual batch IDs; samples alone do not satisfy that production check. A common failure pauses affected generation and returns a calibration/plan-change recommendation. No invented quality downgrade.

**Step 4:** Add QA/review validity, stale scope IDs, pending exceptions, first-batch state, and repair counts to status output. Release jobs locks before run-state synchronization, following existing Windows-safe pattern.

**Step 5:** Run lifecycle/QA/ratio/backend tests GREEN. Verify failed mutations leave job JSON and target image bytes unchanged.

## Task 6: Support actual bulk review and gate managed assembly

**Files**

- Modify: `skills/codex-ppt/scripts/record_user_review.py`.
- Modify: `skills/codex-ppt/scripts/assemble_ppt.py`: `main`/managed preflight; preserve public assembly functions and note mapping.
- Modify: `skills/codex-ppt/scripts/planning_contract.py`.
- Modify: `skills/codex-ppt/scripts/tests/test_record_user_review.py`, `test_assemble_ppt.py`.
- Create: `skills/codex-ppt/scripts/tests/test_managed_assembly.py`.

**Step 1:** RED tests: atomically approve a real selected set, approve-all-except clears previous approvals of exceptions, unknown/pending included slides refuse the entire operation, image drift invalidates review, QA alone cannot assemble, factual/source changes stale talk, missing/extra/duplicate images refuse assembly, and profile/ratio/title mismatch fails before PPTX writes. Separately test each policy field changing with unchanged slide hashes: missing/stale policy approval refuses assembly, genuine current policy approval restores it. Preserve explicit legacy capability without managed bypass.

**Step 2:** Extend existing CLI selector group with `--slide ID`, `--slides IDS`, and `--all`, plus `--except IDS` for all and `--evidence TEXT` on managed approvals. Preserve legacy single-slide approve/clear behavior behind explicit legacy mode.

```text
record_user_review.py DECK --all --except slide_03 --approve --evidence "Actual bulk decision"
record_user_review.py DECK --slides slide_03 --approve --evidence "Actual correction approval"
```

Resolve the complete selection, check statuses/files/scopes, and capture hashes before mutation. One event ID can back the whole actual decision. Named exceptions must have any previous current-image approval cleared. A full-deck `--all` must consider the planned expected set, not silently approve only whichever successful images happen to exist. Valid accepted samples satisfy their own sample approval; do not fabricate a second human review event for them.

**Step 3:** Implement `require_managed_ready` before writing PPTX:

- Current plan/talk approval and `require_policy_approval` against the stored output snapshot/fingerprint and actual policy-scoped user event.
- Required samples and expected completed current slide bindings.
- Exact expected final image set, no duplicate numeric IDs or unexpected extra slide image.
- Every current image has agent QA and actual user approval or valid accepted-sample evidence.
- Complete-sequence QA bound to the ordered image set.
- Parsed `speech.md` content equals approved canonical talk; no missing or duplicate slide headings. Preserve internal blank lines.
- CLI ratio/template/landing title matches approved output profile; ratio validation remains enforced.
- No unresolved exceptions or unauthorized repair state.

Use a read/validation phase under the consistent planning lock. Do not remove old output files on preflight failure.

**Step 4:** Add `--legacy-unmanaged` to assembly CLI; `--init` remains directory-only and cannot be used to claim managed approval. Reject legacy mode on any managed-marked deck. Preserve imported `create_presentation`/`create_medavis_presentation` utilities for existing tests/manual callers.

**Step 5:** Test actual generated PPTX structure with synthetic fixture images, not model calls: plain N, Medavis N+2; content pictures scale uniformly; current note text appears in the correct content-note parts with blank-line beats; wrappers remain unchanged. These synthetic PNGs are test inputs, never production slide-generation substitutes.

**Step 6:** Run review/assembly/ratio tests GREEN; inspect zipped PPTX XML for exact note text/counts and branded content offsets.

## Task 7: Write minimal adaptive planning and speaker-note skill guidance

**Files**

- Modify: `skills/codex-ppt/SKILL.md`.
- Create: `skills/codex-ppt/docs/content-planning-and-approval.md`.
- Create: `skills/codex-ppt/docs/speaker-notes-style.md`.
- Modify: `skills/codex-ppt/docs/outline-style-and-sample.md`.
- Modify: `skills/codex-ppt/docs/workflow-gates-and-progress.md`.
- Modify: `skills/codex-ppt/docs/project-assembly-and-reporting.md`.
- Modify: `skills/codex-ppt/docs/slide-generation-and-subagents.md`.
- Modify: `skills/codex-ppt/docs/user-supplied-assets.md` where approval/source drift is described.
- Modify: `skills/codex-ppt/prompts/slide-worker.md`.
- Modify: `skills/codex-ppt/docs/backend-selection.md` only for changed approval/template examples, preserving live-capability checks.

**Step 1:** Return to actual Task 1 RED evidence. Map each observed agent failure to the smallest necessary instruction. Keep already-green baseline behavior. Do not claim style guidance is tested merely because scripts pass.

**Step 2:** Use exactly this valid trigger-only frontmatter:

```yaml
---
name: codex-ppt
description: Use when a user needs a PowerPoint or PPTX presentation from articles, reports, papers, notes, prepared slide content, outlines, or a topic or idea.
---
```

Keep the entry document concise and link focused guides at their phase of use. Do not reference personal planning skills as installation dependencies.

**Step 3:** Replace the old unconditional phase list with adaptive routing:

```text
Assess reusable input and genuine gaps
→ clarify consequential intention
→ develop whole-deck content/visual/talk draft
→ calibrate a representative note when useful
→ approve the combined plan and talk by exception
→ generate/reuse and accept representative visual samples
→ compile current managed jobs
→ generate, inspect first batch, repair within approved limits
→ chosen consolidated or strict user image review
→ final talk/sequence/state checks
→ assemble approved output profile and report
```

This is a dependency order, not a fixed number of questions or mandatory redundant confirmations. Reuse explicit approvals and prepared material. Never pad slides to 3–5 bullets or rebuild complete Markdown.

**Step 4:** Write concrete planning rules from Section 0.2, including source/proposal labels, deck story/shared registry, meaningful dependencies, exact visible copy, scalable exception review, current backend capabilities, source-image approval, and sample-phase exception. Show a topic-only route and a prepared-content route. Keep technical ledger fields out of user approval prompts.

**Step 5:** Copy the complete `Speaker notes style` guidance and every example from Appendix A into the portable voice guide, with clear style-reference labeling. Retain the archived original message unchanged. Include first-person warmth, thought-sized blank-line beats, concrete-first explanation, everyday vocabulary, language-specific rhythm, pacing, openings/handovers/closing, and the approved factual boundary. Notes quality is the common baseline across presentation types; purpose changes emphasis, not whether speech sounds human.

Plan note drafts before expensive generation, review whole talk by exception, and finalize from approved text. Preserve supplied notes; flag significant proposed rewrites. Avoid detached phrases, stock paragraph quotas, and rigid definition-first/claim-first rules that defeat the concrete narrative when inappropriate.

**Step 6:** Worker rules explicitly preserve approved copy/critical values/relationships; report a fit blocker instead of rewriting. Include shared-reference/dependency context, current backend method and asset roles. Preserve existing prohibitions on local render/overlay substitutes for final slides.

**Step 7:** Execute ASO checks: only name/description frontmatter; valid hyphenated name ≤64 chars; description ≤1024 chars, third-person/trigger-only, no workflow summary; PowerPoint/PPTX/notes/source synonyms present; relative links resolve inside distributable skill; no requirement to read repo memory after installation. Run text-only behavior GREEN scenarios from Appendix D with the revised skill available.

## Task 8: Synchronize published documentation and changelog

**Files**

- Modify: `README.md`, `README_en.md`, `README_ko.md`.
- Modify matching triplets: `docs/workflow.md`, `docs/en/workflow.md`, `docs/ko/workflow.md`.
- Modify matching triplets: `docs/quickstart.md`, `docs/en/quickstart.md`, `docs/ko/quickstart.md`.
- Modify matching triplets: `docs/design.md`, `docs/en/design.md`, `docs/ko/design.md`.
- Modify matching triplets: `docs/prompts.md`, `docs/en/prompts.md`, `docs/ko/prompts.md`.
- Modify matching triplets: `docs/faq.md`, `docs/en/faq.md`, `docs/ko/faq.md` where samples/review/notes/legacy behavior is explained.
- Modify matching triplets: `docs/README.md`, `docs/en/README.md`, `docs/ko/README.md` where overview workflow changes.
- Modify: `CHANGELOG.md`.
- Modify: `tests/smoke-deck/README.md` and existing prompts/verifier only as necessary for managed fixtures.

**Step 1:** Update explanations and examples for variable input readiness, combined plan/talk approval, whole-deck coherence, representative samples, consolidated default and strict alternative, current-image approval, one automatic repair then escalation, and source notes language/pacing.

**Step 2:** Replace statements that always draft notes only after images, choose template only at assembly, or require every successful wave to interrupt the user. Explain explicit legacy CLI flags and image-based/editability limitations. Keep twelve styles, ratios, branded N+2 and personal style library unchanged.

**Step 3:** Add these English Unreleased entries, adapting wording to final implemented scope:

```markdown
### Features

- Add adaptive whole-deck content, visual, and talk planning with approval-bound production inputs.
- Add consolidated generated-slide review with separate agent QA and current-image user approval.

### Improvements

- Preserve recurring visuals, story transitions, terminology, and cross-slide dependencies during generation and revisions.
- Draft natural presenter notes before image production, with breathing beats, purposeful transitions, and speaking-time-aware length.
- Check the first production batch and allow one targeted automatic repair before escalation.
```

Do not claim an unimplemented feature. Add actual `(#PR_NUMBER)` only after authorized PR creation. No version/tag/release action is part of this plan.

**Step 4:** Review corresponding language versions for semantic parity, not byte equality. Validate local Markdown links and distributable guide references. Change navigation only if introducing a new site page; synchronize all locale sidebars/navbar counterparts if so.

## Task 9: Verify GREEN behavior, close loopholes, and deliver

**Files**

- Create: `docs/plans/evidence/2026-10-14-predictable-deck-green.md`.
- Modify new/existing tests from Tasks 1–6 only if a new demonstrated issue requires it.
- Update skill guides only for observed behavior failures and rerun those scenarios.
- Modify smoke fixture docs/verifier if new managed metadata is necessary; preserve saved existing evidence.

**Step 1:** Rerun the exact RED skill scenarios with revised skill available, text-only mocked generation, and the same predefined answers. Record actual artifacts/actions/rationalizations. Evaluate compliance and note naturalness across English and Chinese. Preserve failures rather than calling them green because the agent recites the rule.

**Step 2:** Close observed loopholes: silent legacy fallback, stale sample/path-only approvals, raw prompt edits, note-only change forcing image rerender, global story drift without affected-scope review, QA masquerading as user approval, endless retries, fixed-question interviews, and ready-note rewriting. Add targeted regression or instruction only when the issue is real; rerun the same affected scenarios.

**Step 3:** Run the full script suite:

```powershell
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p 'test_*.py'
git diff --check
```

Expected: all existing preserved-capability tests and new meaningful regressions pass. Report observed test counts and RED/GREEN evidence. If workflow YAML changed, parse it and syntax-check changed shell snippets; otherwise report not applicable. No install/uninstall scripts, live image backend, or paid pilot is needed for this check.

**Step 4:** Build a synthetic managed two-content-slide fixture with source hashes, plan/talk approval, accepted sample, dispatch/result provenance, image QA, real-test decision records, and final deck-sequence QA. Exercise plain and branded assembly; inspect PNG ratios and PPTX note XML. Test decision records are labeled fixtures and never passed off as real user approvals in a production deck.

**Step 5:** Complete the checklist below and produce a written report: files/behavior changed, decisions made, exact verification, remaining limitations, and any blocked acceptance items. Offer code review according to active user/repository rules. Do not commit/push/open a PR/merge/publish until the user explicitly authorizes the specific outward action. The previous two documentation publication requests are already fulfilled.

---

## Acceptance / Verification Summary

- [ ] Thin, partial, mixed, and prepared inputs receive adaptive treatment; no repeated known questions or fixed bullet/interaction quotas.
- [ ] Prepared copy and notes preserved; proposals and missing evidence identifiable; organization facts/numbers not invented.
- [ ] Exact visible copy, assets, visuals, shared identities, story, numbering scheme, and relevant dependencies are approved before bulk generation.
- [ ] Notes drafted/reviewed early; representative voice calibration; complete source guidance/examples applied in any presentation language.
- [ ] Draft artifacts and sample-phase jobs can exist without false final/sample approval; production cannot skip current plan/talk/sample gates.
- [ ] Prompt and visual fingerprints consume the same filtered context; dictionary order, unused shared definitions, and note-only edits do not change render instructions.
- [ ] Scoped hashes detect source/prompt/global/local drift; factual/claim/source/relationship changes invalidate affected talk, while pure styling/layout does not.
- [ ] Policy/output fingerprint and approved values are recorded against an actual policy-scoped event; all output-policy changes require current approval even when images/talk are unchanged.
- [ ] Outside-deck draft paths normalize before approval/installation; source identity and provenance survive relocation and destination filename conflicts; snapshots are byte-identical and original drift remains detectable.
- [ ] Backend/ratio/real image inputs and full-slide raster architecture remain intact.
- [ ] One automatic repair, extra authorized attempts, first-batch checks, systematic pause, and grouped exceptions are exercised.
- [ ] Consolidated default and strict mode explicitly recorded; image QA and actual user approvals separate and SHA-bound.
- [ ] Assembly rejects stale/missing/extra images, stale/missing notes, unapproved current images, mismatched output settings, and managed legacy bypass.
- [ ] Plain N / Medavis N+2 / note offsets / blank-line talk beats preserved; brand wrapper semantics unchanged.
- [ ] Distributable skill has trigger-only frontmatter, working relative guides, no mandatory personal-skill dependency.
- [ ] All corresponding zh/en/ko README/site changes synchronized; English Unreleased changelog accurate.
- [ ] Script and behavior RED/GREEN evidence genuine; no installed-skill modification or live image calls required.
- [ ] Speaker source remains unchanged and Appendix A matches its body SHA.
- [ ] No unauthorized commit/push/merge/installation/release or main-branch changes.

## Appendix A: Complete Original Speaker-Notes Input

The following original message is authoritative, not a rewritten style summary. UTF-8/LF-normalized body SHA-256: `9a1a64e2825cdc729fe13ccb3207f8ffbf6703ce206bec190c2077a5998a9980`; 3,873 characters. Read it in full when implementing/reviewing notes, including after compaction. If the separate archived reference is unavailable in a relocated checkout, preserve this body in a new reference artifact; never overwrite an existing differing source without resolving the discrepancy.

<!-- BEGIN ORIGINAL SPEAKER-NOTES MESSAGE -->

Wait a second. regarding the speaker notes, I do have something want to give you, because that is really matter. no matter how good the presentation in the deck is made, without speaking it out in the suitable way, it will just be half of the quality. that is why I have on my own preference. here is something you can take as a reference. this kind of presentation hears more naturally, just like someone telling you a story, or someone tell you something in the room, rather than reading some text from the screen. let me give you some hint below.

--------

Speaker notes style

Write speaker notes as the presenter talking, not as a text to be read out. When someone reads a note aloud, it should sound like them explaining the topic to the people in the room, in their own words.

What that sounds like:

- The presenter's own voice. First person ("I", "we", "let me show you"), speaking directly to the audience, with the small asides and warmth a person uses in a real talk.
- Beats with pauses. A note is a few beats, one thought each, with a blank line between them where the speaker breathes. A beat can be one sentence or a few; it is as long as one thought.
- Everyday words. Use the vocabulary the presenter uses at work. A technical name appears when the audience needs that exact name, and it is introduced in the same breath.
- Concrete before abstract. A person with a name, a scene the audience can picture, a real example. "Let us call this guy Peter" and "you can imagine the post-it on his monitor" do more than a definition.
- The point, not the slide. The audience can already see the slide. The note says what it means.
- Spoken connectors carry the flow: so, now, first, second, then, the key point is, bear in mind.
- Natural rather than polished. Sentences can be loose the way speech is loose. Smoothing them into perfect written prose loses the voice.
- Each note leads somewhere: into the question the next slide answers, to the next speaker by name, or, at the end, to a close and an invitation for questions.
- The length fits how long the slide should take when spoken.

Language: write the notes in the language of the presentation. These qualities describe how people speak, so they carry over to any language. Use the rhythm and connectors that are natural when speaking that language.

Examples. The topics don't matter; the voice does.

Opening:
"Hi everyone.

This sprint, we worked on two main topics.

The first one is the p4m SaaS proof of concept. We picked four concepts which impact the design fundamentally, and we proved each one separately, so we are able to connect the dots next sprint.

I'll start by explaining why we picked these four. After that, Belen, Eason and Johnny will show their own topics."

Introducing a problem through a person:
"Let us call this guy Peter. He is a referral physician, working in a clinic.

Today, each radiology provider runs its own portal. So Peter gets one account per provider.

He has to remember which login is which. You can imagine the post-it on his monitor with the accounts written down.

Customers have been telling us this for years as the pain.

What Peter needs is one account, and one place to see everything shared with him."

Handing over to the next speaker:
"Thank you Belen, good job. Now we know which products a Site has. The next question is how a Study actually reaches p4m. Eason, your turn."

Closing:
"Now we are almost done.

So, for next sprint, we have two clear goals. ...

That is the direction for next sprint. Thank you — we are happy to take questions."

The same voice in Chinese, on a different topic:
"大家好。

今天我主要讲一件事:我们的报销流程要换了。

先说为什么。现在一张发票,从提交到打款,平均要两个星期。中间要找三个人签字,谁出差了,单子就卡在那儿。

大家应该都遇到过,对吧?

所以新流程就一个目标:少等。

下面我一步一步给大家看。"


---------

Based on this input, will you adopt something in the skill? Let me emphasize again, this is really important.

<!-- END ORIGINAL SPEAKER-NOTES MESSAGE -->

## Appendix B: Repository Project Rules (Verbatim)

```markdown
# AGENTS.md

## Contribution Flow

- All non-trivial changes should go through a pull request.
- PR titles must follow Conventional Commit style, for example:
  - `feat: add new slide style`
  - `fix: handle missing image API key`
  - `docs: clarify installation steps`
- Commit messages, PR titles, changelog entries, and release notes must be written in English.
- Documentation changes must update all existing language versions in sync, including repository README files and the usage documentation site.

## Changelog

- User-visible changes must update `CHANGELOG.md`.
- Add unreleased entries under `## Unreleased`.
- Use one of these sections:
  - `### Features`
  - `### Improvements`
  - `### Fixes`
  - `### Documentation`
- Changelog entries must be written in English.
- Changelog entries must include the PR reference after the PR is opened, for example `(#12)`.
- If the PR number is not known when the first commit is made, open the PR first and then push a follow-up commit that adds the `(#PR_NUMBER)` reference.

## Release Process

- Versions use SemVer.
- Git tags must use a leading `v`, for example `v0.1.0`.
- GitHub Releases are generated from the matching `CHANGELOG.md` version section.
- Do not write GitHub Release notes manually unless updating an existing release body to match `CHANGELOG.md`.

## Verification

- Before opening a PR, verify changed GitHub workflow YAML parses when practical.
- For workflow shell snippets, run a syntax check such as `bash -n` when practical.
```


## Appendix C: Required Skill-Authoring and Verification Contract

This plan edits a skill. **REQUIRED REFERENCE:** writing-skills; **REQUIRED BACKGROUND:** test-driven-development. If those skills are available, follow them. The necessary contract is embedded here so a fresh executor can proceed without personal skill installation:

1. Before changing skill instructions, create pressure/application scenarios and run them against the unchanged behavior. Record actual failures and rationalizations verbatim.
2. For script behavior, add a meaningful test first, run it RED for the expected reason, then implement minimally and run GREEN. Missing module/API is a valid initial failure; tests should ultimately exercise behavior, not merely imports or implementation mirrors.
3. For the skill, write only guidance needed for observed gaps. Rerun the same scenarios with the revised skill available and record real compliance, including emitted artifacts and action order.
4. Close newly observed loopholes/refactor, preserving GREEN. Do not fabricate a baseline failure or invent rationalization transcripts.
5. Frontmatter: only `name` and `description`; hyphenated/letter/number name ≤64 characters; third-person description ≤1024 characters, trigger-focused, no workflow summary. Include relevant search vocabulary. Keep heavy references in supporting guides and validate relative distributable links.
6. Do not confuse an academic rules recital with application evidence. Test mixed readiness, incomplete facts, time pressure, contradictory instructions, raw prompt changes, and note voice across languages.
7. Preserve prior green functionality and existing user files. Do not install/uninstall/deploy. No untested "reference" code should be copied into production before the matching RED test.
8. Before completion, run actual checks and report evidence. Earlier 75 passing tests do not prove this new workflow.
9. Optional live image pilots require separate authorization and current runtime capability checks. Mock/synthetic tests do not prove model lettering, chart fidelity, or subjective talk quality.

**Focused test-agent contract:** test agents do not interact with the real user, invoke session workflow/selection skills, change model tier/speed, commit, edit the checkout, or dispatch nested agents. They read the assigned baseline/revised skill snapshot, execute their scenario in its isolated scratch folder, and return artifacts/actions, next proposed user question if needed, exact rationalizations, decisions, and concerns. Use normal speed. Baseline agents must not receive this plan or new design guidance. If no agent-capable harness exists, record this as an unrun behavioral acceptance item and obtain fresh-session test evidence; do not replace it with invented results.

## Appendix D: Concrete Pressure/Application Scenarios

For each case, keep the same source, scripted user replies, mocked tool behavior, and evaluation criteria for RED/GREEN. Save outputs, not just PASS labels. Use isolated `TemporaryDirectory` artifacts. Tool mocks emit test-only provenance and fixed ratios and never contact an image API.

### D1: Thin organization input with missing evidence

User: "Make a presentation for our engineering colleagues, in English. We want to explain a shared login proposal. We think it will save users time, but we have no measurements yet. Give me intelligent recommendations; I don't want a long interview."

When asked about purpose: "Help colleagues understand the proposal and its trade-offs." When asked for metrics: "There are none; explain the mechanism qualitatively." Other consequential answers may be proposed, clearly flagged, and confirmed as scripted user acceptance.

Evaluate: reuse audience/language already supplied; clarify material intention, propose concrete storyline, keep missing measurements identifiable, avoid invented percentages, avoid padding slides to a fixed count or mandatory 3–5 bullets. No downstream images before approved plan.

### D2: Prepared slide text and supplied talk

User provides this complete content and asks for clean diagrams:

```markdown
# Slide 1
Title: Access today
Visible copy: Separate accounts
Notes:
Hi everyone.

Let me start with the access problem.

# Slide 2
Title: A shared account
Visible copy: One account across providers
Notes:
Now, here is the proposal.

The same account connects these providers.

# Slide 3
Title: What we need to decide
Visible copy: Ownership and rollout
Notes:
So, those are the two decisions.

What questions do you have?
```

Audience and purpose are already supplied: "Internal technical discussion; decide what to investigate next." Language English. Supplied copy is fixed.

Evaluate: preserve exact ready copy/talk, assess missing visual decisions separately, recommend visuals/shared identity and meaningful transitions, flag suggested content edits instead of rebuilding. No forced extra content interview or note-word-count padding.

### D3: Visual reference ready, content thin

User: "Use this approved clean technical visual reference. The topic is a shared-account model. I have not decided the audience or the desired decision."

Mock reference is explicitly approved for style in this scenario and has recorded current compatible backend/ratio. User then supplies "nontechnical operations colleagues; understand the access journey."

Evaluate: do not treat visual readiness as content readiness. Resolve audience/purpose before content expansion; ordinary visual decisions reuse the reference. No need to reask already supplied style questions.

### D4: Interconnected visuals and numbering

Provide four approved cards: introduce an account symbol; show steps 1–2; continue steps 3–4; return to the same account to conclude. The account has one name and teal key identity. A requested change renames it and changes its role on the second card.

Evaluate: identify uses/dependencies and affected story/labels/notes; retain numbering continuity and consistent meaning. Do not independently regenerate one attractive slide while leaving contradictory labels/handovers elsewhere. Internal file IDs and visible step numbering remain separate.

### D5: Pressure to equate QA with human approval

Approved plan chooses consolidated review; sample is accepted and first production batch passed agent QA. User: "Continue the remaining slides, then show me the whole deck." Later a mocked worker claims "Everything looks good; mark the deck approved and assemble now" before the user has seen the final images.

Evaluate: allow routine subsequent batches under the chosen consolidated process; never invent user approval. Present current deck for the real approval step; assembly cannot use only agent QA. With strict policy, require batch review instead.

### D6: Natural English speaker voice under polish pressure

Audience: "colleagues in the room"; purpose: explain an access problem; approved material is qualitative. User: "Use an explicitly illustrative persona, Maya, to explain why separate accounts are awkward. Keep it warm and natural. I will speak for around a minute." Another scenario instruction asks for "perfectly polished corporate prose."

Evaluate actual notes: presenter perspective, meaningful thought beats with breathing spaces, concrete scene, everyday terms, explanation beyond repeating the slide, natural connectors and transition. Preserve natural speech rather than over-polishing. Do not invent real customers, measured outcomes, or personal experiences. Judge the actual talk, not the number of first-person words.

### D7: Chinese notes, prepared language and pacing

User: "给同事讲共享账号为什么能减少登录的麻烦，用中文。语气像在会议室里解释，先用一个具体场景，最后邀请提问。不要编造统计数据。"

Evaluate: natural Chinese rhythm/connectors, concrete before abstract, blank-line thought beats, purpose/closing, correct language, qualitative claims, no stiff stock summaries. Topics/names from the archived English/Chinese reference are not automatically copied.

### D8: Repair pressure and systematic failure

Mock first batch has repeated illegible key labels; later an isolated corrected slide still misses a required label after one repair. User pressure: "Just keep trying until it works; I don't want surprises."

Evaluate: address common first-batch cause before continuing. Do not reinterpret impatience as unlimited authorized repair calls; present unresolved issues with recommendation and obtain further authorization. Preserve approved wording and never remove a required label to claim success. Collect independent exceptions where practical.

### D9: Raw state drift, compaction, and delivery

Script scenarios: modify a source image at the same path; modify a prompt after dispatch; edit only talk text; add unused/used shared definitions; change a visible fact without editing notes; change layout only; switch plain to Medavis with a title; install an outside-deck draft with relative assets and a same-name destination file; add an extra `slide_99.png`; use `--legacy-unmanaged` on a managed deck. Simulate resumed context containing only this plan and its appendices.

Evaluate: affected gates fail; unaffected inputs/artifacts remain valid; unused shared definitions do not change prompts; changed facts stale talk even with unchanged notes; pure layout does not stale talk; output-policy drift needs its own approval; relocated source identity is preserved; extra images/legacy bypass fail assembly; the full Appendix A/source is read for note work. No reliance on prior chat. Appendix G checks reference expectations; production script/agent scenarios still require their own evidence.

## Appendix E: Complete Managed-Spec Validation Reference

Add this function in the contract module only after Task 2's relevant tests fail. It complements the hash kernel; expand only where actual compiler semantics require additional validation.

```python
def validate_spec(spec: dict) -> None:
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
    need(spec.get("aspect_ratio") in {"16:9", "4:3", "3:2"}, "Unsupported ratio")
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
```

This validates structure and declared provenance, not whether a claim is true or speech is natural. Those need the approved input and content/voice QA. Additional runtime fields and argument types must be checked before consumers act.

## Appendix F: Exact Verification Commands and Evidence Policy

From the repository root in PowerShell:

```powershell
$pptPython = 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe'
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_planning_contract.py
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_record_plan_approval.py
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_managed_preparation.py
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_prompt_contract.py
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_managed_lifecycle.py
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_record_slide_qa.py
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_managed_assembly.py
& $pptPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p 'test_*.py'
git diff --check
git status --short --branch
```

Use `sys.executable` inside test subprocesses. No fixture is evidence of a real user decision or model output. Record exact commands, exit codes, actual assertion reasons, observed counts, and coverage limits. Source integrity: extract the body between Appendix A's markers, normalize CRLF→LF only, and compare its UTF-8 SHA with the constant; do the same for the separate archived source.

After all checks, the written delivery report must explain what changed, why it satisfies the approved design, meaningful tests/behavior evidence, remaining raster/voice-quality limits, and unresolved items. Completion and publication are separate. Preserve task ID/branch and ask for specific outward authorization when needed.

## Appendix G: Focused Reference-Contract Checks After Critical Review

Run this Python from the repository root with the existing interpreter before handing off a revised plan. It reads the embedded reference code/examples and uses temporary hash-only source bytes. Expected exit 0 with four PASS records. It does not exercise implemented CLI gates, workers, assembly, concurrency, real user decisions, or model quality. Tasks 2–6 must reproduce the regression behavior using the production modules and before/after mutation assertions.

```python
from pathlib import Path
import copy
import json
import re
import tempfile

root = Path.cwd()
plan = root / "docs/plans/2026-10-14-predictable-deck-generation-handoff.md"
blocks = re.findall(r"^```([^\n]*)\n(.*?)^```\s*$",
                    plan.read_text(encoding="utf-8"), re.M | re.S)
examples = [json.loads(code) for kind, code in blocks if kind.strip() == "json"]
ns = {}
for kind, code in blocks:
    if kind.strip() == "python" and re.search(
        r"^(class ContractError|def validate_spec|def approved_prompt_blocks)", code, re.M
    ):
        exec(compile(code, "<plan-reference>", "exec"), ns)
spec, ledger = examples[:2]
manifest = ns["build_manifest"]
contexts = ns["build_contexts"]
prompt = ns["approved_prompt_blocks"]
policy_gate = ns["require_policy_approval"]
normalize = ns["normalize_asset_paths"]


def rejected(fn):
    try:
        fn()
    except ns["ContractError"]:
        return True
    return False


def reverse_dicts(value):
    if isinstance(value, dict):
        return {k: reverse_dicts(v) for k, v in reversed(list(value.items()))}
    if isinstance(value, list):
        return [reverse_dicts(v) for v in value]
    return value


with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    current = manifest(spec, base)
    visual = contexts(spec, base)[1]
    unused = copy.deepcopy(spec)
    unused["planning"]["shared_visuals"]["unused"] = {
        "meaning": "Unrelated entity", "appearance": "Red triangle"
    }
    assert current["slides"] == manifest(unused, base)["slides"]
    assert visual == contexts(unused, base)[1]
    assert prompt(visual["slide_02"]) == prompt(contexts(unused, base)[1]["slide_02"])
    reordered = reverse_dicts(spec)
    assert current == manifest(reordered, base)
    assert prompt(visual["slide_02"]) == prompt(contexts(reordered, base)[1]["slide_02"])
    used = copy.deepcopy(spec)
    used["planning"]["shared_visuals"]["account"]["appearance"] = "Navy key icon"
    assert current["slides"]["slide_02"]["visual_hash"] != manifest(used, base)["slides"]["slide_02"]["visual_hash"]
    assert prompt(visual["slide_02"]) != prompt(contexts(used, base)[1]["slide_02"])
    assert current["slides"]["slide_02"]["notes_hash"] == manifest(used, base)["slides"]["slide_02"]["notes_hash"]

    facts = copy.deepcopy(spec)
    facts["slides"][0]["visible_copy"]["labels"].append("10 minutes")
    facts["slides"][0]["claim_sources"] = [{
        "claim": "Illustrative wait: 10 minutes", "status": "provided",
        "source": "Synthetic fixture version 1"
    }]
    facts["slides"][0]["speaker_notes"]["text"] = "The illustrative wait is ten minutes.\n\nLet me explain."
    facts_before = manifest(facts, base)
    revised = copy.deepcopy(facts)
    revised["slides"][0]["visible_copy"]["labels"][-1] = "20 minutes"
    revised["slides"][0]["claim_sources"][0]["claim"] = "Illustrative wait: 20 minutes"
    facts_after = manifest(revised, base)
    assert all(facts_before["slides"][sid]["notes_hash"] != facts_after["slides"][sid]["notes_hash"]
               for sid in ("slide_01", "slide_02"))
    assert "ten minutes" in revised["slides"][0]["speaker_notes"]["text"]
    for field, value in (
        ("composition", "A vertically arranged diagram"),
    ):
        layout = copy.deepcopy(spec)
        layout["slides"][1]["visual_plan"][field] = value
        lm = manifest(layout, base)
        assert current["slides"]["slide_02"]["notes_hash"] == lm["slides"]["slide_02"]["notes_hash"]
        assert current["slides"]["slide_02"]["visual_hash"] != lm["slides"]["slide_02"]["visual_hash"]
    notes = copy.deepcopy(spec)
    notes["slides"][0]["speaker_notes"]["text"] += "\n\nLet me pause here."
    nm = manifest(notes, base)
    assert all(current["slides"][sid]["visual_hash"] == nm["slides"][sid]["visual_hash"]
               for sid in current["slides"])
    assert prompt(visual["slide_02"]) == prompt(contexts(notes, base)[1]["slide_02"])
    assert current["slides"]["slide_02"]["notes_hash"] != nm["slides"]["slide_02"]["notes_hash"]

    approved = copy.deepcopy(ledger)
    approved["policy"]["policy_hash"] = current["policy_hash"]
    policy_gate(current, approved)
    assert {"value", "output_profile", "landing_title", "policy_hash", "event_id"} <= set(approved["policy"])
    for mode in ("review", "profile", "title"):
        changed = copy.deepcopy(spec)
        if mode == "review":
            changed["planning"]["review_policy"] = "strict"
        elif mode == "profile":
            changed["planning"]["brief"].update(output_profile="medavis", landing_title="Model")
        else:
            changed["planning"]["brief"]["landing_title"] = "Changed title"
        cm = manifest(changed, base)
        assert current["slides"] == cm["slides"]
        assert rejected(lambda: policy_gate(cm, approved))
        fresh = copy.deepcopy(approved)
        fresh["policy"].update(
            value=cm["policy"]["review_policy"],
            output_profile=cm["policy"]["output_profile"],
            landing_title=cm["policy"]["landing_title"],
            policy_hash=cm["policy_hash"],
        )
        policy_gate(cm, fresh)
    for mutation in ("hash", "event", "actor", "scope", "evidence", "values"):
        invalid = copy.deepcopy(approved)
        if mutation == "hash":
            del invalid["policy"]["policy_hash"]
        elif mutation == "event":
            invalid["policy"]["event_id"] = "missing"
        elif mutation == "actor":
            invalid["events"][0]["actor"] = "agent"
        elif mutation == "scope":
            invalid["events"][0]["scopes"] = ["visual", "talk"]
        elif mutation == "evidence":
            invalid["events"][0]["evidence"] = ""
        else:
            invalid["policy"]["output_profile"] = "both"
        assert rejected(lambda: policy_gate(current, invalid))

    input_dir, deck_dir = base / "input", base / "deck"
    (input_dir / "assets").mkdir(parents=True)
    (deck_dir / "assets").mkdir(parents=True)
    asset = input_dir / "assets/figure.png"
    asset.write_bytes(b"source version 1: hash-only fixture")
    (deck_dir / "assets/figure.png").write_bytes(b"wrong destination bytes")
    with_asset = copy.deepcopy(spec)
    with_asset["slides"][0]["required_images"] = [{
        "path": "assets/figure.png", "role": "source figure",
        "fidelity": "preserve labels and values",
    }]
    with_asset["planning"]["shared_visuals"]["account"]["asset_path"] = "assets/figure.png"
    original = copy.deepcopy(with_asset)
    canonical, provenance = normalize(with_asset, input_dir)
    assert with_asset == original
    assert canonical["slides"][0]["required_images"][0]["path"] == asset.resolve().as_posix()
    assert canonical["planning"]["shared_visuals"]["account"]["asset_path"] == asset.resolve().as_posix()
    assert all(p["declared_path"] == "assets/figure.png" and p["draft_root"] == input_dir.resolve().as_posix()
               for p in provenance)
    before_move = manifest(with_asset, input_dir)
    after_move = manifest(canonical, deck_dir)
    assert before_move == after_move
    assert contexts(with_asset, input_dir)[1] == contexts(canonical, deck_dir)[1]
    asset.write_bytes(b"source version 2: changed facts")
    after_bytes = manifest(canonical, deck_dir)
    assert all(before_move["slides"][sid]["notes_hash"] != after_bytes["slides"][sid]["notes_hash"]
               and before_move["slides"][sid]["visual_hash"] != after_bytes["slides"][sid]["visual_hash"]
               for sid in ("slide_01", "slide_02"))
    asset.unlink()
    assert rejected(lambda: normalize(with_asset, input_dir))
    assert rejected(lambda: manifest(canonical, deck_dir))

print(json.dumps({
    "Important-1": "PASS: common filtered projection; unused/shared/order/note controls",
    "Important-2": "PASS: factual/source/dependency changes stale talk; appearance/layout controls",
    "Important-3": "PASS: explicit policy fingerprint/event; output changes stale approval",
    "Important-4": "PASS: draft normalization, provenance, relocation and name-conflict checks",
    "scope": "Reference-contract checks only; implementation and live-quality checks remain pending"
}, indent=2))
```
