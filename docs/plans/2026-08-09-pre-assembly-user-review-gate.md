# Pre-Assembly User Review Gate Implementation Plan

> **For the implementing agent:** Follow this plan task-by-task. Complete each step, verify it works, then move to the next.

**Goal:** Add a prose-enforced, per-slide user review gate after each dispatch wave (with durable run-state markers via a thin recorder script) so full-deck images are human-approved before the next wave and before assembly — without hard-blocking `assemble_ppt.py`.

**Architecture:** Keep existing slide statuses (`pending → dispatched → recorded`; sample `accepted`). Add a separate per-slide `user_review` field written only by `scripts/record_user_review.py`, mirrored into `slide_run_state.json` so smoke-deck T1 can see the literal marker `user_reviewed` (only while at least one approval is currently valid). Docs teach a wave loop: dispatch → agent visual check + record results → user full-res review → impact-aware regen if needed → re-approve → next wave. No contact sheet. No `assemble_ppt.py` enforcement.

**Tech Stack:** Python 3 (same as existing `scripts/record_*.py`), `slide_run_state.py` helpers (`locked_jobs`, `locked_run_state`, `sha256_file`, …), Markdown skill docs under `skills/codex-ppt/`.

---

> **SELF-CONTAINED HANDOFF PLAN.** The executor needs no prior chat session or memory file and must not ask the user to re-explain context. All task context lives in this plan (and its appendices). Normal session-start rules still apply, but you may start fresh and rely on this document.

## Section 0: Full Context

### 0.1 Why / background

`codex-ppt` generates each slide as one full-page AI image, then assembles PNGs into a `.pptx`. Today it has five user approval gates — all **before** any full-deck image exists. After sample-slide approval, generation runs through agent-only QA and assembly with **no user review of final slide images**.

This fork (`d:/git/codex-ppt-skill`, branch `feature/SQ5GEN-195-improvement-2026-08-09`) is implementing three committed goals over time. **This plan is only goal 1** (pre-assembly / mid-generation user review). Goals 2 (backend menu) and 3 (multilingual) are out of scope.

The skill under `skills/codex-ppt/` was still byte-identical to upstream when this design was approved; only `tests/smoke-deck/` exists as fork-specific work so far (may be uncommitted).

### 0.2 Confirmed decisions (do not re-litigate)

1. **Enforcement = prose-only for v1.** Docs/`SKILL.md` require waiting for user approval and recording markers. **`assemble_ppt.py` stays unchanged** — no hard block.
2. **No contact sheet** in v1. Final review needs full-res `origin_image/slide_XX.png`; thumbnail grids lose detail and are pointless for near-ship review.
3. **Per-slide approval**, timed **after each completed dispatch wave** (or after each slide if `max_concurrent_slides == 1`). Do not overlap the next wave while reviewing.
4. **Reject path:** regenerate affected work after **required** impact analysis (other slides, speech/notes, visuals), re-approve those slides, then continue to the next wave. Impact analysis is **mandatory in docs**, not optional soft advice.
5. **Approach = docs + thin `record_user_review.py`.** Not docs-only (fragile / conflicts with “don’t hand-edit statuses”). Not a new terminal slide status in the state machine.
6. **Do not overload `accepted`.** That status already means “approved sample slide,” not “user reviewed this full-deck slide.”
7. **Do not commit** unless the user explicitly asks. Commit message prefix if/when asked: `[SQ5GEN-195]`.
8. **Parked:** content-generation skill vs codex-ppt boundary; backend gate; multilingual fixes; shipping style preview images.

**Rejected alternatives (do not reopen):**
- Hard-block in `assemble_ppt.py`
- Soft-state-only without docs gate / or docs-only without a recorder
- Contact-sheet helper in this v1
- Whole-deck single approval (user chose per-slide / per-wave)
- Overlapping next-wave dispatch during review
- New `user_reviewed` value inside `TERMINAL_SLIDE_STATUSES` (Approach 3)

### 0.3 Audience & assumptions

- Executor works in repo root: `d:/git/codex-ppt-skill` on branch `feature/SQ5GEN-195-improvement-2026-08-09`.
- Python available; skill scripts import sibling `slide_run_state.py` (run from `skills/codex-ppt/scripts` or with that dir on `PYTHONPATH` / invoke as other scripts do via the runtime venv).
- Smoke-deck verifier already exists at `tests/smoke-deck/verify_deck.py`. T1 currently fails until a `user_reviewed` / `review_approved` / `userreviewed` substring appears in `slide_run_state.json`.
- Installed copies under `~/.codex/skills/codex-ppt` etc. are **not** the edit target — edit the fork’s `skills/codex-ppt/` only. Do not run collection install/uninstall scripts.

### 0.4 Project rules / conventions to honor

- Prefer matching existing `record_slide_*.py` CLI style and `slide_run_state` locking.
- Do not hand-edit `slide_jobs.json` statuses in docs instructions — always point at scripts.
- Keep ASCII unless a file already uses non-ASCII (some Chinese tip strings exist in assembly docs — leave those alone unless editing that paragraph).
- YAGNI: no contact sheet, no assemble hard-block, no backend/multilingual work in this plan.
- After implementation, verification before any “done” claim (`verification-before-completion` mindset): run commands and read output.

### 0.5 Formats & reference material

See **Appendix A** (T1 assertion), **Appendix B** (target `user_review` JSON shape), **Appendix C** (full `record_user_review.py` implementation), **Appendix D** (doc wording to insert), **Appendix E** (pressure scenarios for skill RED/GREEN).

---

### Task 1: RED — baseline pressure (skill behavior missing)

**Files:**
- Create: `docs/plans/evidence/2026-08-09-review-gate-red.md` (short evidence log)

**Step 1: Confirm current docs lack the gate**

Run from repo root:

```bash
rg -n "user_review|user_reviewed|record_user_review|pre-assembly|dispatch wave" skills/codex-ppt -g '*.md' -g '*.py' || true
```

Expected: **no** `record_user_review.py`; no wave-review gate language (may match unrelated “approval” hits for outline/sample — note those are pre-generation gates).

**Step 2: Write RED evidence file**

Create `docs/plans/evidence/2026-08-09-review-gate-red.md` documenting:

1. The five existing gates all precede full-deck images (`docs/workflow-gates-and-progress.md` phases 1–5; phase 6–7 have no user image review).
2. Predicted agent failure modes without the new docs/script (copy these into the evidence file verbatim as baseline rationalizations to defeat later):

   - R1: “Sample was already approved; full deck can assemble after agent QA.”
   - R2: “I’ll dispatch the next wave while the user looks at the previous PNGs to save time.”
   - R3: “User said slide 3’s title is wrong — regenerate only slide 3 and continue.”
   - R4: “Statuses are `recorded`; assembly checklist is satisfied.”

3. Confirm T1 fails on a deck without markers (optional if no real run dir): note that `check_targets` requires substring in `slide_run_state.json` (Appendix A).

**Step 3: Stop**

Do not edit skill files until Task 1 evidence file exists.

---

### Task 2: Unit tests for the recorder (TDD — fail first)

**Files:**
- Create: `skills/codex-ppt/scripts/tests/test_record_user_review.py`  
  (If `scripts/tests/` does not exist, create it. Prefer running with `python -m pytest` from `skills/codex-ppt/scripts` after adding an empty `__init__` only if required — otherwise run the file as a script-style unittest. Simplest: use stdlib `unittest` in that file so no pytest dependency is assumed.)

**Step 1: Write failing tests** covering:

1. `--approve` on a `recorded` slide writes `user_review.status == "user_reviewed"`, `reviewed_at`, and `image_sha256` matching the PNG.
2. Approve updates `slide_run_state.json` so `json.dumps(state).lower()` contains `"user_reviewed"`.
3. `--approve` on `pending` / `dispatched` / `blocked` exits non-zero.
4. `--clear` removes `user_review` from the slide and refreshes run-state summary.
5. After approve, if PNG bytes change (rewrite file) without re-approve, a helper `review_is_valid(slide, deck_dir)` returns False (sha mismatch) — implement this helper in `record_user_review.py` or a tiny shared function in the same module.
6. Sample slide with status `accepted` may be skipped for approve **or** explicitly rejected — **decision for implementer: only allow `--approve` when `status == "recorded"`** (samples stay `accepted` and are not part of this gate). Document that in the script docstring.
7. After `--clear` removes the last valid approval, `slide_run_state.json` must **not** contain the substring `user_reviewed` (no sticky marker).
8. After a slide with `user_review` is re-dispatched via `record_slide_dispatch.py`, that slide’s `user_review` key is gone (add a focused test that calls the dispatch script or its clear line).

**Step 2: Run tests — expect FAIL** (module missing)

```bash
cd skills/codex-ppt/scripts
python -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: import / file-not-found failure (module under test missing).

---

### Task 3: Implement `record_user_review.py` (GREEN for script)

**Files:**
- Create: `skills/codex-ppt/scripts/record_user_review.py` (full target code in Appendix C)
- Modify: `skills/codex-ppt/scripts/record_slide_dispatch.py` — clear stale `user_review` on re-dispatch

**Step 1: Add `record_user_review.py`** using Appendix C as the implementation source of truth (adapt only if a helper name already exists; do not change behavior).

**Step 2: Clear on re-dispatch**

In `record_slide_dispatch.py`, inside the `locked_jobs` block after status checks succeed, before setting `dispatched`:

```python
        slide.pop("user_review", None)
```

**Step 3: Re-run unit tests — expect PASS**

```bash
cd skills/codex-ppt/scripts
python -m unittest discover -s tests -p 'test_*.py' -v
```

**Step 4: Manual smoke on a temp deck**

Create a minimal temp deck dir with `origin_image/slide_02.png` (any small PNG), `slide_jobs.json` with one `recorded` slide, empty/default `slide_run_state.json`. Run approve; confirm both JSON files. Run clear; confirm removal.

---

### Task 4: Skill docs — wave review gate (GREEN for prose)

**Files:**
- Modify: `skills/codex-ppt/SKILL.md` (steps 8–11 area; Acceptance Criteria)
- Modify: `skills/codex-ppt/docs/workflow-gates-and-progress.md`
- Modify: `skills/codex-ppt/docs/slide-generation-and-subagents.md` (Parent responsibilities + Dispatch loop)
- Modify: `skills/codex-ppt/docs/project-assembly-and-reporting.md` (readiness bullet before assembly)

**Step 1: Apply Appendix D wording** (integrate into existing structure; do not duplicate contradictory old text). Key replacements:

- Phase list gains an explicit **user review of generated slides per dispatch wave** between generation and assembly (or as phase 6.5 / split phase 6).
- Progress checklist gains a step that is only complete when `record_user_review.py` has approved every full-deck (`recorded`) slide.
- Dispatch loop: after **agent visual check + `record_slide_result.py`** for the wave, **stop**; present each full-res PNG; on approve run recorder; on change request run **mandatory impact analysis** (Appendix D); clear + regen; re-approve; only then next wave.
- Assembly readiness: every non-sample slide must be `recorded` **and** have valid `user_review` (status `user_reviewed` and matching sha). Samples remain `accepted`. Still do **not** claim `assemble_ppt.py` enforces this.
- Do **not** modify `slide_job_status.py` in v1. The parent tracks the current wave's slide ids (the set just recorded) in prose and requires those approvals before refilling dispatch slots.

**Step 2: Defeat rationalizations R1–R4** with explicit counters in the docs (short “Do not…” lines are fine):

- Do not treat sample approval as full-deck image approval.
- Do not dispatch the next wave until every slide in the current wave is user-reviewed.
- Do not regenerate only the named slide without impact analysis (other slides / speech / visuals) and user confirmation when scope expands.
- Do not assemble when any `recorded` slide lacks a valid `user_review`.

**Step 3: ASO / skill meta check (lightweight)**

- Do **not** change SKILL.md YAML description into a workflow summary dump.
- If you touch frontmatter at all, keep third-person description; prefer **not** changing frontmatter unless needed for discoverability of “review” — default: leave frontmatter unchanged.

---

### Task 5: VERIFY GREEN — pressure scenarios + T1

**Files:**
- Create: `docs/plans/evidence/2026-08-09-review-gate-green.md`

**Step 1: Re-run rg for new symbols**

```bash
rg -n "record_user_review|user_review|impact analysis|dispatch wave" skills/codex-ppt -g '*.md' -g '*.py'
```

Expected: hits in the new script + the four doc files (+ dispatch clear).

**Step 2: Synthetic T1 proof**

Build a tiny deck directory (can be under `docs/plans/evidence/t1-deck/`) with `slide_run_state.json` updated by actually running `record_user_review.py` (not hand-edited). Then:

```bash
python tests/smoke-deck/verify_deck.py --help
```

If the verifier requires a full smoke deck layout, either:

- Run only the T1 logic by importing `check_targets` with a minimal deck that has `slide_run_state.json` containing the marker, **or**
- Document that you ran `record_user_review.py` and show `rg -i user_reviewed path/to/slide_run_state.json` matching.

Minimum bar: prove the recorder produces a state blob that satisfies Appendix A’s substring check.

**Also document:** T1 can PASS after the first `--approve` even if other slides are still pending review. Assembly readiness is stricter: `user_review.pending_recorded_slide_ids` must be empty / `all_recorded_slides_approved` true. Do not treat T1 alone as “deck fully reviewed.”

**Step 3: Write GREEN evidence**

In `docs/plans/evidence/2026-08-09-review-gate-green.md`, map R1–R4 → the exact doc sentences / script behaviors that now block them. Paste command outputs.

**Step 4: Confirm `assemble_ppt.py` untouched**

```bash
git diff -- skills/codex-ppt/scripts/assemble_ppt.py
```

Expected: empty.

---

### Task 6: Optional loophole closure

**Step 1:** Re-read docs as an adversarial agent. If a loophole remains (e.g. “user said skip review”), add one hard rule: skipping the gate requires an **explicit** user skip for this deck, and still record a run-state note — **only if** you find the loophole; otherwise skip this task.

**Step 2:** Do not broaden into contact sheet / hard assemble / backend / multilingual.

---

## Verification Summary (acceptance checklist)

Executor self-check when all tasks are done:

- [ ] `skills/codex-ppt/scripts/record_user_review.py` exists and unit tests pass
- [ ] `record_slide_dispatch.py` clears `user_review` on re-dispatch
- [ ] `assemble_ppt.py` diff is empty
- [ ] `SKILL.md` + `workflow-gates-and-progress.md` + `slide-generation-and-subagents.md` + `project-assembly-and-reporting.md` describe wave review + mandatory impact analysis + no next-wave overlap
- [ ] Docs explicitly counter R1–R4
- [ ] Running approve writes `user_reviewed` into `slide_run_state.json` (T1 substring satisfied); clearing the last approval removes that substring again
- [ ] RED and GREEN evidence files exist under `docs/plans/evidence/`
- [ ] No commit created unless the user asked

---

## Appendix A — Smoke-deck T1 (current code)

From `tests/smoke-deck/verify_deck.py`:

```python
# T1 -- pre-assembly review gate
state_path = deck / "slide_run_state.json"
reviewed = False
if state_path.exists():
    state = read_json(state_path)
    blob = json.dumps(state, ensure_ascii=False).lower()
    reviewed = "user_reviewed" in blob or "review_approved" in blob or "userreviewed" in blob
r.targ(reviewed, "T1 pre-assembly review recorded in run state",
       "no review marker found" if not reviewed else "")
```

The recorder **must** write the literal substring `user_reviewed` into `slide_run_state.json` (recommended key path below).

---

## Appendix B — Target JSON shapes

### Per-slide in `slide_jobs.json`

```json
{
  "slide_id": "slide_02",
  "status": "recorded",
  "user_review": {
    "status": "user_reviewed",
    "reviewed_at": "2026-08-09T12:00:00Z",
    "image_sha256": "<sha256 of origin_image/slide_02.png>"
  }
}
```

### Summary in `slide_run_state.json`

```json
{
  "status": "slides_recorded",
  "user_review": {
    "marker": "user_reviewed",
    "approved_slide_ids": ["slide_02", "slide_03"],
    "pending_recorded_slide_ids": ["slide_04"],
    "all_recorded_slides_approved": false,
    "updated_at": "2026-08-09T12:00:00Z"
  }
}
```

`marker` is set to the literal `"user_reviewed"` **only when `approved_slide_ids` is non-empty**. After the last approval is cleared, omit `marker` (or leave summary without that substring) so smoke-deck T1 fails again until a fresh approve.

---

## Appendix C — `record_user_review.py` (implement this)

```python
#!/usr/bin/env python3
"""Record per-slide user review for codex-ppt (full-res image approval)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from slide_run_state import (
    deck_dir_from_target,
    find_slide,
    locked_jobs,
    locked_run_state,
    now_iso,
    resolve_deck_path,
    sha256_file,
)


def _final_image_path(deck_dir: Path, slide: Dict[str, Any]) -> Path:
    out_ref = slide.get("out") or f"origin_image/{slide['slide_id']}.png"
    return resolve_deck_path(deck_dir, out_ref)


def review_is_valid(deck_dir: Path, slide: Dict[str, Any]) -> bool:
    review = slide.get("user_review")
    if not isinstance(review, dict):
        return False
    if review.get("status") != "user_reviewed":
        return False
    path = _final_image_path(deck_dir, slide)
    if not path.is_file():
        return False
    return review.get("image_sha256") == sha256_file(path)


def _sync_run_state(deck_dir: Path, jobs: Dict[str, Any]) -> None:
    approved: List[str] = []
    pending: List[str] = []
    for slide in jobs.get("slides", []):
        if slide.get("status") == "accepted":
            continue  # sample — not part of this gate
        if slide.get("status") != "recorded":
            continue
        sid = slide.get("slide_id")
        if review_is_valid(deck_dir, slide):
            approved.append(sid)
        else:
            pending.append(sid)
    with locked_run_state(deck_dir) as state:
        summary: Dict[str, Any] = {
            "approved_slide_ids": approved,
            "pending_recorded_slide_ids": pending,
            "all_recorded_slides_approved": bool(approved) and not pending,
            "updated_at": now_iso(),
        }
        # T1 looks for substring "user_reviewed". Only emit it while at least one
        # slide currently holds a valid approval — clearing the last approval must
        # make T1 fail again (do not leave a sticky marker).
        if approved:
            summary["marker"] = "user_reviewed"
        state["user_review"] = summary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", help="Deck directory or slide_jobs.json")
    parser.add_argument("--slide", required=True, help="slide_01 or 1")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--approve", action="store_true")
    group.add_argument("--clear", action="store_true")
    args = parser.parse_args()

    deck_dir = deck_dir_from_target(args.deck)
    with locked_jobs(deck_dir) as jobs:
        slide = find_slide(jobs, args.slide)
        slide_id = slide["slide_id"]
        if args.approve:
            if slide.get("status") != "recorded":
                raise SystemExit(
                    f"{slide_id} must be recorded before user review; got {slide.get('status')}"
                )
            path = _final_image_path(deck_dir, slide)
            if not path.is_file():
                raise SystemExit(f"Final image missing for {slide_id}: {path}")
            slide["user_review"] = {
                "status": "user_reviewed",
                "reviewed_at": now_iso(),
                "image_sha256": sha256_file(path),
            }
        else:
            slide.pop("user_review", None)

    # Sync run state AFTER releasing the jobs lock (avoid nested file locks on Windows).
    from slide_run_state import load_jobs

    _sync_run_state(deck_dir, load_jobs(deck_dir))

    action = "user_reviewed" if args.approve else "review_cleared"
    print(json.dumps({"slide_id": slide_id, "action": action}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

**Canonical locking rule:** never call `locked_run_state` while holding `locked_jobs`. Mutate jobs, exit the jobs lock, reload, then sync run state.

---

## Appendix D — Doc wording (integrate; do not paste as a disconnected blob)

### Wave review rules (for SKILL.md + slide-generation doc)

Within a dispatch wave, order is:

1. Spawn workers → `record_slide_dispatch.py`.
2. Worker returns → **agent** quick visual check → `record_slide_result.py` (copies into `origin_image/`).
3. When the wave’s results are recorded: **Stop. Do not spawn the next wave.**
4. For each newly recorded slide in the wave, present the full-resolution `origin_image/slide_XX.png` to the user (no contact sheet). This is the **user** review gate — distinct from the agent’s quick check in step 2.
5. On approve: run `record_user_review.py <deck> --slide slide_XX --approve`.
6. On change request: perform **mandatory impact analysis** before regenerating:
   - Other slides (sequence, paired layouts, shared motifs, continuity)
   - Spoken narrative alignment: update `speech.md` **if it already exists**; otherwise adjust `outline.md` / slide job context (`local_context` / `deck_context`) so later notes stay consistent — do **not** assume `speech.md` exists mid-generation
   - Visual system / sample-anchor consistency
   - Propose the regen scope; if it expands beyond the named slide(s), confirm with the user
   - Clear review (`--clear` or re-dispatch), regenerate, re-record, re-approve those slides
7. Only when every slide in the wave is user-reviewed, dispatch the next wave.
8. Before assembly: every non-sample slide is `recorded` with a **valid** `user_review` (status + matching image sha). `assemble_ppt.py` does not enforce this — the agent must.

### Impact-analysis required line (copy into docs)

> When the user requests a change to a generated slide, do not blindly regenerate only that slide. Analyze whether the change also affects other slides, the planned spoken narrative (`speech.md` if present, otherwise outline / slide context that will drive notes), or the deck’s visual consistency with the approved sample. Report the blast radius, confirm expanded scope with the user when needed, then regenerate and re-run user review for every affected slide before continuing.

---

## Appendix E — Pressure scenarios (skill RED/GREEN)

Use these as mental (or live) agent pressures when verifying docs:

| ID | Prompt pressure | Required compliant behavior |
|----|-----------------|-----------------------------|
| P1 | “All slides recorded — assemble now.” | Refuse until all `recorded` slides have valid user_review; show pending ids. |
| P2 | “Wave 1 done — start wave 2 while I glance at the PNGs.” | Refuse overlap; finish per-slide approve for wave 1 first. |
| P3 | “Slide 4 title wrong — fix it and keep going.” | Impact analysis first; possible speech/neighbors; then clear/regen/re-approve. |
| P4 | “Sample looked fine, skip reviewing the rest.” | Only skip if user explicitly waives the gate for this deck; otherwise require reviews. |

---

## Appendix F — Related paths cheat sheet

| Path | Role |
|------|------|
| `skills/codex-ppt/SKILL.md` | Orchestration contract |
| `skills/codex-ppt/docs/workflow-gates-and-progress.md` | Phase gates + progress checklist |
| `skills/codex-ppt/docs/slide-generation-and-subagents.md` | Dispatch loop |
| `skills/codex-ppt/docs/project-assembly-and-reporting.md` | Assembly readiness |
| `skills/codex-ppt/scripts/slide_run_state.py` | Locking + paths |
| `skills/codex-ppt/scripts/record_slide_dispatch.py` | Clear `user_review` here |
| `skills/codex-ppt/scripts/record_slide_result.py` | Pattern for record_* scripts |
| `skills/codex-ppt/scripts/assemble_ppt.py` | **Do not modify** |
| `tests/smoke-deck/verify_deck.py` | T1 acceptance |
| `tests/smoke-deck/RUN_PROMPT.md` | How to re-run smoke deck later |
