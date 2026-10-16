# Predictable Deck Execution

Started: 2026-10-14; current execution date: 2026-10-15 (Asia/Shanghai).
Branch/task: feature/SQ5GEN-predictable-deck-generation / SQ5GEN-195.

The user authorized: “Continue to the end; pause only when you genuinely need my decision or input.” This replaces routine task/batch approval stops. It does not switch the session's named autonomous mode or authorize publication, installation, live/paid generation, new chats, or main changes.

## Progress

- [x] Task 1: Existing 75 tests passed; actual missing-approval RED captured; nine baseline applications archived.
- [x] Task 2: Validation, common semantic contexts, path normalization, policy and plan gates. 15 focused tests passed.
- [x] Task 3: Actual scoped decisions, immutable asset/sample snapshots, draft/approved views. 13 decision tests and 3 view tests passed; contract tests remain green.
- [x] Task 4: Managed compiler, explicit calibration/legacy routes, exact filtered prompts, preserve current jobs/results on note-only changes. 10 managed preparation, 1 prompt projection, 7 ratio and 8 language tests passed. Original missing-approval regression is now GREEN.
- [x] Task 5: Lifecycle, QA, first batch and bounded repairs implemented; all accepted review findings corrected and re-reviewed.
- [x] Task 6: Bulk current-image human review and canonical-order transactional assembly verified, including repaired calibration through production/delivery.
- [x] Task 7: Portable adaptive planning and complete note guide; actual behavior artifacts evaluated; four schema/view applications pass with original copy/talk intact.
- [x] Task 8: All zh/en/ko README/site counterparts, English changelog and live smoke prompts synchronized; published order issue corrected and reviewed.
- [x] Task 9: Final168-test suite and10 smoke-verifier tests pass; synthetic plain2/branded4/notes mapping verified; source/archive/link checks pass; delivery and memory saved.

## RED / GREEN evidence

All commands use the existing shared Python with `-B -m unittest discover -s skills/codex-ppt/scripts/tests -p NAME`.

| File pattern | RED observation | Latest GREEN |
|---|---|---|
| test_planning_contract.py | Missing planning_contract module/API; exit 1 | 15 tests; exit 0 |
| test_record_plan_approval.py | Missing sample gate/recorder API; exit 1 | 13 tests; exit 0 |
| test_planning_views.py | Missing views module; exit 1 | 3 tests; exit 0 |
| test_managed_preparation.py | Missing gates/phase, conflicting override accepted, dispatched rewrite accepted, false template approvals; 7 failures + 1 error | 11 tests; exit 0 |
| test_prompt_contract.py | Missing approved_prompt_blocks API; exit 1 | 1 test; exit 0 |
| test_managed_lifecycle.py | 5 demonstrated failures: stale plan/sample, mutated prompt, retained QA/review, silent legacy; exit 1 | 8 tests; exit 0 |
| test_record_slide_qa.py | First-batch dispatch ungated; helper missing; 4 failures; production phase repair bypass additionally RED | 6 tests; exit 0 |
| test_managed_assembly.py | 10 failures/11 tests; source-mutation during assembly additionally RED | 13 tests; exit 0 |
| test_skill_contract.py | Missing portable guides, legacy frontmatter and links: 2 failures + 1 error | 3 tests; exit 0 in full suite |
| test_review_regressions.py | Review issues + zero capacity; calibration continuation additionally RED | 10 tests; exit 0 |
| test_managed_execution.py | Missing adapter, unsupported config, strict integer/global locks/stale return; native Windows race additionally RED | 10 tests; exit 0 |

One additional recorder regression exposed final speech being rewritten during partial approval while a dependent talk binding remained stale. Observed actual RED, then corrected derived-view installation: only a fully current candidate creates final views; partial approved candidates produce draft views and preserve existing approved speech/outline. Rerun passed all 13 recorder tests.

A preparation test's raw string-prefix assertion failed for Windows short/full user-directory aliases. Diagnostics showed both paths resolve inside the same deck; changed the test to resolved path containment. No production path logic was changed for this fixture issue.

## Implementation decisions

- Audience/purpose/tone and other content-facing brief fields enter the common render context, excluding output profile/title. This ensures a changed audience invalidates relevant visual instructions and talk together. Policy stays separately bound.
- Dependency cycles use a sorted reachable closure, rather than recursive hashes.
- Visual/talk event IDs are separate so note-only approval retains the prior visual decision. Policy-only/scoped slide choices do not refresh an unapproved policy.
- Source declaration/root provenance remains in events; normalized canonical original paths and hash-named byte-identical snapshots preserve asset identity after relocation.
- Sample style snapshots remain immutable when final sample content images are repaired. Style-only imported reuse is supported by an explicit optional flag.
- Approved canonical/spec/ledger/views are written with atomic files and a planning transaction marker. Ordinary failures roll back; a hard interruption remains fail-closed until the actual reviewed decision is re-recorded.
- Review/repair/assembly gate APIs are implemented with their matching later RED tasks; no untested success stubs were installed.

## Boundaries

No live image generation, model-pixel QA, timed voice playback, installed-skill edits, commit/push/PR/merge or release. Existing planning/source edits are preserved. Synthetic provider tests can print API-call status but call mocks, not a live API. [Final delivery evidence](2026-10-15-predictable-deck-green.md) records exact verification, reviews, supplemental-check limits and completed scope.

## Independent review and corrections

The initial independent frozen-snapshot review found Important-1 through Important-9; all were independently reproduced and accepted. Full [report](2026-10-15-managed-core-review.md) and [triage](2026-10-15-managed-core-review-triage.md) are saved. Repairs retain sample/production prerequisites, missing prompts fail closed, first-batch revisions can regenerate, assembly uses canonical order, result/compiler mutations roll back together, and compiler/blocker use planning→jobs locks.

The executable CLI adapter is a justified implementation addition: the original bundled batch path ignored nested configuration and required image inputs. Jobs bind an explicit approved input-dependent operation policy, and preflight/adapter share one execution projection. Synthetic test fixtures now explicitly specify model, quality and reference_mode=edit; original Task1 archived bytes and approvals remain unchanged.

Follow-up review resolved seven original findings but exposed the final repaired-calibration→production transition, strict integer CLI representation, and a new long-held-global-lock issue (Important-10). All three were independently reproduced; [report](2026-10-15-managed-core-followup-review.md) and [triage](2026-10-15-managed-core-followup-triage.md) preserve evidence. Extended regressions preceded corrections. The 161-test result is valid covered-case evidence, not a claim of final readiness. The user's continuous authorization overrides routine review-cycle stops; none of these fixes needs a new design/publication decision.

Final core review cleared Important1–10; the later real Windows candidate-directory race was independently reproduced, fixed minimally and reviewed. Final full suite:168 passed/114.337s/exit0; smoke verifier:10 passed/exit0. Synthetic managed output:plain2, branded4, exact note text/blank lines and content offsets verified.165 links,114 archived artifacts,7 runners/audits and complete speaker-source hashes pass.

Guidance review's approval-order finding was corrected across all9 README/design/workflow counterparts and cleared. Parent behavioral evaluation found4 incompatible JSON draft shapes despite good readable cards; originals were archived, minimal template guidance added, and all4 actual schema/draft-view checks passed without content changes. The isolated agent authored that replay; the primary completed it after helper usage limits. Publication preflight found the independent supplementary template-paragraph review already saved in the guidance follow-up report, despite its failed final notification. That paragraph is independently cleared; the corrected four-case replay remains primary verification, not another fresh-agent application test.

## Authorized publication checkpoint — 2026-10-15

After receiving the human briefing, the user explicitly requested: “Update memory, commit and push.” This authorizes publishing the completed implementation, tests, synchronized documentation, plans/evidence and updated memory on the existing feature branch with task ID SQ5GEN-195. Earlier local-only boundaries above describe the implementation checkpoint and are superseded for these requested actions. No installation, live generation, PR/merge, release or main change is part of this request. Verify the final commit and remote SHA after publication; this pre-commit record does not claim a successful push in advance.

Fresh publication verification: 168 script tests passed in 124.288 seconds; 10 smoke-verifier tests passed in 0.268 seconds; both exits 0. Source/Appendix/portable voice integrity, 114 baseline artifact hashes, 7 runner/audit hashes and 165 local Markdown links passed again. Core adapter and execution-regression hashes still match the independently reviewed snapshot. No production code changed during publication preparation.

Inspected the166-file staged scope (approximately1.97 MB); no file exceeds1 MB and no private-key/API-token patterns were found. The expanded staged whitespace check reports16 formatting-only notices in reviewed Markdown, generated draft views and final blank lines in reviewed source/test files. These are retained; the earlier tracked-only check excluded new files and is not a claim that the complete staged check is clean.
