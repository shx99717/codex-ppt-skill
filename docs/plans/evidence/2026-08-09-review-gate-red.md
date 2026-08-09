# RED evidence — pre-assembly user review gate (baseline)

**Date**: 2026-08-09  
**Repo**: `d:/git/codex-ppt-skill`  
**Branch**: `feature/SQ5GEN-195-improvement-2026-08-09`

## Step 1 — Search before any skill edits

Command:

```bash
rg -n "user_review|user_reviewed|record_user_review|pre-assembly|dispatch wave" skills/codex-ppt -g '*.md' -g '*.py' || true
```

Result: **no matches**.  
`skills/codex-ppt/scripts/record_user_review.py` does **not** exist (`NO_RECORDER_OK`).

Unrelated pre-generation “approval” language still exists for outline / style / backend / sample gates; those are not wave review of full-deck images.

## Existing gates (all before full-deck images)

From `skills/codex-ppt/docs/workflow-gates-and-progress.md`:

1. Source reading and asset extraction  
2. Outline confirmation  
3. Visual style confirmation  
4. Image backend confirmation  
5. One sample slide approval  
6. Full slide generation — **no user image review**  
7. QA, speaker notes finalization, and PPT assembly — **agent QA only; no user review gate**

## Baseline rationalizations to defeat (R1–R4)

- R1: “Sample was already approved; full deck can assemble after agent QA.”
- R2: “I’ll dispatch the next wave while the user looks at the previous PNGs to save time.”
- R3: “User said slide 3’s title is wrong — regenerate only slide 3 and continue.”
- R4: “Statuses are `recorded`; assembly checklist is satisfied.”

## T1 without markers

`tests/smoke-deck/verify_deck.py` `check_targets` T1 requires `slide_run_state.json` JSON blob (lowercased) to contain one of: `user_reviewed`, `review_approved`, `userreviewed`. A deck with no such marker yields TARGET fail: `T1 pre-assembly review recorded in run state` / `no review marker found`.

---

**Stop**: no skill files edited in Task 1.
