# Predictable Deck Generation: RED Baseline Evidence

Date: 2026-10-14 (Asia/Shanghai).
Checkpoint verified: 2026-10-15, Asia/Shanghai; the execution crossed midnight.
Branch: `feature/SQ5GEN-predictable-deck-generation`.
Task: `SQ5GEN-195`.
Execution scope: user requested execution of the revised written plan in this session. Publication, installation and live image generation remain outside this execution authorization.

## Execution checklist

- [x] Task 1: Capture skill and script RED baselines — script RED and nine isolated behavior runs saved and evaluated.
- [ ] Task 2: Contract validation and scoped fingerprints.
- [ ] Task 3: Actual plan/talk/sample decisions and derived views.
- [ ] Task 4: Managed compilation and calibration.
- [ ] Task 5: Dispatch/result integrity, QA and bounded repair.
- [ ] Task 6: Bulk human review and managed assembly.
- [ ] Task 7: Adaptive planning and natural speaker-note guidance.
- [ ] Task 8: Synchronized published documentation and changelog.
- [ ] Task 9: GREEN behavior, loophole checks and delivery.

## Method and isolation

Read the complete revised [implementation plan](../2026-10-14-predictable-deck-generation-handoff.md), [execute prompt](../2026-10-14-predictable-deck-generation-handoff-PROMPT-execute.md), and [original speaker message](../../memory/memory-20261014-predictable-ppt-generation/speaker-notes-style-reference.md). The archived message remains authoritative and unchanged.

Copied the 59 existing skill files into an unchanged temporary baseline snapshot before adding tests. Read-only scenario agents receive only this snapshot and their assigned D1–D8 inputs/scripted responses. They receive neither the implementation plan, approved design, memory nor new note guide. Actual planning/note artifacts and ordered traces will be preserved below. Generation/preview actions are text-only mocks, not rendered/model images or real image-quality evidence. D9 state-drift checks are script work: the initial missing-approval regression is recorded here; production drift regressions remain Tasks 2–6/9.

No production scripts or skill instructions changed during Task 1. No installed personal skills were modified. The existing image API unit-test log below uses `_FakeProvider` from `test_image_gen.py`, not a network call.

## Reference-contract preflight

Command: existing shared Python, `-B -c`, extract and execute the saved Appendix G Python block from the on-disk plan.

Exit code: 0.

```text
{
  "Important-1": "PASS: common filtered projection; unused/shared/order/note controls",
  "Important-2": "PASS: factual/source/dependency changes stale talk; appearance/layout controls",
  "Important-3": "PASS: explicit policy fingerprint/event; output changes stale approval",
  "Important-4": "PASS: draft normalization, provenance, relocation and name-conflict checks",
  "scope": "Reference-contract checks only; implementation and live-quality checks remain pending"
}
```

These four PASS records validate reference expectations only, not an implemented managed gate.

## Fresh existing-suite baseline (before adding the new regression)

Command:

```powershell
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B -m unittest discover -s skills/codex-ppt/scripts/tests -p 'test_*.py'
```

Exit code: 0. Observed: 75 existing tests passed.

```text
...................................OPENAI_API_KEY is set. API target: official OpenAI API (OPENAI_BASE_URL unset).
Calling Image API (generation). This can take up to a couple of minutes.
Generation completed in 0.0s.
........................................
----------------------------------------------------------------------
Ran 75 tests in 5.267s

OK
Wrote 1 slide job file(s) to C:\Users\RAYMON~1.SHE\AppData\Local\Temp\tmpo1epryg2\demo\prompts
Wrote slide job state to C:\Users\RAYMON~1.SHE\AppData\Local\Temp\tmpo1epryg2\demo\slide_jobs.json
```

## New meaningful regression: missing approval

Added `skills/codex-ppt/scripts/tests/test_managed_preparation.py` and independent fresh-copy fixture helper `planning_fixtures.py`. The helper contains the complete synthetic Section 0.7 fixture; no fixture approval is represented as a real user decision.

The canonical spec exists inside the deck and has valid planned content/backend/ratio. There is no approval ledger. Expected behavior: compiler refuses with an approval error before creating `prompts/`. Baseline behavior: compiler exits 0 and creates two prompt jobs, `slide_jobs.json`, and `slide_run_state.json`.

Command:

```powershell
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_managed_preparation.py
```

Exit code: 1. This is a real expected RED assertion, not a missing dependency or fixture error.

```text
F
======================================================================
FAIL: test_managed_production_refuses_missing_approval (test_managed_preparation.ManagedPreparationTests.test_managed_production_refuses_missing_approval)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\git\codex-ppt-skill\skills\codex-ppt\scripts\tests\test_managed_preparation.py", line 30, in test_managed_production_refuses_missing_approval
    self.assertNotEqual(
AssertionError: 0 == 0 : Managed production succeeded without approval. Artifacts: ['deck_spec.json', 'prompts/slide_01.json', 'prompts/slide_02.json', 'slide_jobs.json', 'slide_run_state.json']. Output: Wrote 2 slide job file(s) to C:\Users\RAYMON~1.SHE\AppData\Local\Temp\tmplc809ses\deck\prompts
Wrote slide job state to C:\Users\RAYMON~1.SHE\AppData\Local\Temp\tmplc809ses\deck\slide_jobs.json


----------------------------------------------------------------------
Ran 1 test in 0.203s

FAILED (failures=1)
```

## Full suite with the intentional RED regression

Command: same full-discovery command as the original baseline.

Exit code: 1. Observed: 76 tests, exactly one failure (the new missing-approval test); the 75 preserved-capability tests still pass.

```text
...................................OPENAI_API_KEY is set. API target: official OpenAI API (OPENAI_BASE_URL unset).
Calling Image API (generation). This can take up to a couple of minutes.
Generation completed in 0.0s.
.F.......................................
======================================================================
FAIL: test_managed_production_refuses_missing_approval (test_managed_preparation.ManagedPreparationTests.test_managed_production_refuses_missing_approval)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\git\codex-ppt-skill\skills\codex-ppt\scripts\tests\test_managed_preparation.py", line 30, in test_managed_production_refuses_missing_approval
    self.assertNotEqual(
AssertionError: 0 == 0 : Managed production succeeded without approval. Artifacts: ['deck_spec.json', 'prompts/slide_01.json', 'prompts/slide_02.json', 'slide_jobs.json', 'slide_run_state.json']. Output: Wrote 2 slide job file(s) to C:\Users\RAYMON~1.SHE\AppData\Local\Temp\tmpvert22ow\deck\prompts
Wrote slide job state to C:\Users\RAYMON~1.SHE\AppData\Local\Temp\tmpvert22ow\deck\slide_jobs.json


----------------------------------------------------------------------
Ran 76 tests in 4.776s

FAILED (failures=1)
Wrote 1 slide job file(s) to C:\Users\RAYMON~1.SHE\AppData\Local\Temp\tmpt0j69alc\demo\prompts
Wrote slide job state to C:\Users\RAYMON~1.SHE\AppData\Local\Temp\tmpt0j69alc\demo\slide_jobs.json
```

Task 4 must turn this regression GREEN. No production fix has been applied at this checkpoint.

## Behavior scenarios: observed applications

Nine isolated runs cover D1–D8, with both review-policy variants of D5. Their actual written artifacts, scripted questions/answers, exact prompt text and decision rationalizations are preserved in the linked JSON bundles. Each artifact includes its original-byte SHA-256. [Metadata and archived runners/audits](./2026-10-14-predictable-deck-baseline/metadata.json) retain the unchanged source snapshot and explain the mock boundary.

| Case | Observed behavior | Evaluation against the approved target |
|---|---|---|
| [D1: thin organization input](./2026-10-14-predictable-deck-baseline/D1.json) | Used supplied engineering audience/English, asked purpose, proposed eight-slide qualitative story, identified absent measurements and illustrative journeys. Six proposed questions through sample preparation. | Preserve: no fabricated percentages or company architecture. The proposed count was a recommendation; this run does not prove a forced-count failure. Combined talk/visual/policy approval was not represented. |
| [D2: prepared content/talk](./2026-10-14-predictable-deck-baseline/D2.json) | Kept the three supplied titles, single visible-copy items and note wording/blank lines; restated clean diagrams without a style menu. Four proposed questions. | Preserve: exact prepared material and focused visual completion. No invented failure for ready-note rewriting or bullet padding. |
| [D3: ready visual reference](./2026-10-14-predictable-deck-baseline/D3.json) | Asked audience/purpose before content expansion; reused style-only reference without another style menu. Five proposed questions. | Preserve: distinguishes content and visual readiness. Unseen reference details were not invented. |
| [D4: interconnected change](./2026-10-14-predictable-deck-baseline/D4.json) | Changed all four cards/notes to provider-scoped credentials, retained teal-key identity, and revised step order while keeping steps 1/2 then 3/4. | Preserve: actual impact analysis and numbering continuity. Content-scope acceptance did not become mock-image acceptance. |
| [D5: consolidated](./2026-10-14-predictable-deck-baseline/D5-consolidated.json) | Treated selected consolidated policy/continuation as intermediate-wave deferral, represented the remaining slides, then awaited final human review. Rejected worker instruction to mark approved. | Preserve: QA is not human approval. Baseline implements this as a waiver; revised managed default/policy evidence still requires implementation. |
| [D5: strict](./2026-10-14-predictable-deck-baseline/D5-strict.json) | Stopped for slide 2 review before simulating slide 3 dispatch. No final acceptance was supplied. | Preserve: chosen strict review order. |
| [D6: English voice](./2026-10-14-predictable-deck-baseline/D6.json) | Wrote 139 words in four thought paragraphs around illustrative Maya; natural presenter phrasing, concrete scene, no invented measurements. Replay wrote/reviewed notes after visual acceptance. | Voice criterion passes this written sample. Early talk preparation/review criterion fails the represented baseline route: no note review before images or user talk acceptance. Estimated 57.5 seconds at an assumed 145 words/minute is not timed oral evidence. |
| [D7: Chinese voice](./2026-10-14-predictable-deck-baseline/D7.json) | Wrote a concrete hypothetical scene, spoken connectors, separated thought beats and invitation for questions in Chinese; no statistics. Notes were again reviewed after visual acceptance. | Natural written-language sample passes; early talk review has the same baseline gap as D6. Character counts are observations, not prescribed quotas. |
| [D8: repeated failure/repair](./2026-10-14-predictable-deck-baseline/D8.json) | After repeated unreadable labels and one unsuccessful isolated repair, prepared another constrained same-backend attempt on both affected cards; kept exact `Shared account`. | Preserves required content and avoids false success. Fails the approved bounded-repair/escalation target: no explicit extra-attempt event or retry threshold; no calibrated first-batch gate is enforced. |

### Exact relevant baseline wording

D8 rationalization, verbatim from the actual report:

> The user’s “Just keep trying until it works; I do not want surprises” authorizes continued correction at that semantic scope.

Its stated limitation, verbatim:

> The unchanged baseline contains no numeric retry budget, no two-slide recurring-error threshold, and no mandatory escalation after one isolated repair.

D6/D7 trace states that there is no pre-image notes artifact and records visual approval sequence 30, delivery selection 32, notes write 33 and review 34. The same trace explicitly discloses that the generator contains prewritten wording. These sequences describe the agent's represented route; they do not prove physical authorship happened after a real image call.

### Evidence limits and harness issues

All image generation, user decisions, worker calls, preview/visual QA and image-review actions are simulated. Actual operations are baseline reads, scratch artifact writes, read-only backend probes and deterministic prompt compilation where recorded. These are application artifacts, not mere rules recitals, but the offline traces are authored replays rather than a tool-enforced multi-turn conversation. Future GREEN tests must keep the same inputs/scripted answers and disclose that distinction; script gates need independent executable regressions.

The agents' isolated empty-home probes identify bundled CLI availability, not real API authorization. No PNG/PPTX was produced by these scenario agents. No live image tool, network generation, audio timing or human deck approval occurred. The D9 full drift/mutation matrix remains executable regression work in Tasks 2–6 and 9; Appendix G's reference PASS records do not satisfy it.

Final archive verification exited 0: nine case bundles, 114 original-byte-verified artifacts, 68 nested JSON files parsed, 59 original skill source files unchanged, two new test files AST-parsed, thirteen local report links resolved, and original speaker-message SHA confirmed. D2 visible copy and supplied note wording/paragraphs match after CRLF-to-LF comparison normalization. The first semantic note-containment check failed because it compared raw Windows CRLF text with LF expected text; diagnostics confirmed all titles/copy/note metadata equal and all three note blocks present after normalization. Only that verification comparison changed; archived bytes retain their original hashes.

The input-readiness agent recovered an oversized PowerShell command through scratch-only patching. The coherence agent's first Python helper call created two bytecode caches in the temporary baseline copy; later calls used `-B`. These cache paths are recorded in metadata and excluded from archived source artifacts. All 59 original source-file hashes still match both the repository and baseline snapshot. No repository production code/skill instruction was edited.

## Task 1 checkpoint and next work

Task 1's baseline artifacts and genuine missing-approval RED are complete. The only intentionally failing test remains `test_managed_production_refuses_missing_approval`; Task 4 must make it pass. No managed feature is implemented yet. Formal feature review and GREEN behavior verification remain ahead.

Next: Task 2's validation/scoped-context regressions before production module edits, followed by the approval recorder/views and managed compiler. Follow executing-plans review checkpoints for the selected execution cadence. Existing planning/source files remain preserved; changes are uncommitted, HEAD/upstream remain `99fba3d3ea2d8f1d285cf40dbf44d8e32f05d126`, and main remains `dc65c44c8b8fcef60c3073e7203856cfa3598b2f`.

