# GREEN evidence — pre-assembly user review gate

**Date**: 2026-08-09  
**Repo**: `d:/git/codex-ppt-skill`  
**Branch**: `feature/SQ5GEN-195-improvement-2026-08-09`

## Symbols present after implementation

`rg -n "record_user_review|user_review|impact analysis|dispatch wave" skills/codex-ppt` hits:

- `skills/codex-ppt/scripts/record_user_review.py` (new)
- `skills/codex-ppt/scripts/record_slide_dispatch.py` (`slide.pop("user_review", None)`)
- `skills/codex-ppt/scripts/tests/test_record_user_review.py`
- `skills/codex-ppt/SKILL.md`
- `skills/codex-ppt/docs/workflow-gates-and-progress.md`
- `skills/codex-ppt/docs/slide-generation-and-subagents.md`
- `skills/codex-ppt/docs/project-assembly-and-reporting.md`

## `assemble_ppt.py` untouched

```text
git diff -- skills/codex-ppt/scripts/assemble_ppt.py
# empty
```

## Unit tests

```text
cd skills/codex-ppt/scripts
python -m unittest discover -s tests -p 'test_*.py' -v
# Ran 6 tests ... OK
```

## T1 substring proof (recorder-produced, not hand-edited)

Deck: `docs/plans/evidence/t1-deck/`

```text
python record_user_review.py <t1-deck> --slide slide_02 --approve
# {"slide_id": "slide_02", "action": "user_reviewed"}
T1_SUBSTRING_OK True
pending []
all_approved True
```

Note: T1 can PASS after the first approve even if other slides were still pending; assembly readiness requires `pending_recorded_slide_ids` empty / `all_recorded_slides_approved` true.

Deviation from early plan draft: run-state field is `all_recorded_slides_approved` (not `...user_reviewed`) so clearing the last approval does not leave a sticky T1 substring.

## R1–R4 counters

| ID | Baseline rationalization | Counter now in skill |
|----|--------------------------|----------------------|
| R1 | Sample approved ⇒ assemble after agent QA | workflow-gates: "Do not treat sample approval as full-deck image approval." SKILL acceptance requires valid `user_review` on every non-sample recorded slide. |
| R2 | Dispatch next wave while user glances | slide-generation: "Do not spawn the next wave yet." / "Do not overlap the next wave while the user is still reviewing." workflow-gates hard rule on wave gating. |
| R3 | Regen only named slide and continue | slide-generation + project-assembly: mandatory impact analysis; confirm expanded scope; clear/regen/re-approve affected slides. |
| R4 | `recorded` ⇒ assembly OK | SKILL step 11 + project-assembly: recorded **and** valid `user_review`; assemble_ppt does not enforce — agent must. |

## P4 loophole closure (Task 6)

Added hard rule: skipping user review requires an **explicit** user waiver for this deck, with a recorded note — no silent skip.
