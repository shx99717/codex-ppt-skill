# Final managed core review — Tasks 2–6

Frozen snapshot: `C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-final-core-review-c1984fa745a547259759a8bfb0ea53ae/codex-ppt`. Plan: `implementation-plan.md` in its parent directory.

Historical reports: the original `codex-ppt-core-review-1d5apjke/review/report.md` and follow-up `codex-ppt-fixed-review-0f104cfc5fdf4d40ae275d34dcd17678/review/report.md`, both beneath the user's local Temp directory. This report preserves **Important-1 through Important-10**. All code locations below refer to the final frozen snapshot.

## Scope and strengths

The changeset remains coherent with the approved managed generation contract and the accepted review fixes. No scope drift was found. Pending Task 8 published documentation/localization/changelog work is excluded from findings.

The common render/talk projections, scoped human decision events, immutable source/style snapshots, fail-closed managed commands, exact job integrity checks, distinct agent QA and user acceptance, and grouped/revalidated assembly remain sound foundations. The corrections now support the full repaired-calibration transition, preserve prior artifacts on tested copy/write failures, normalize assembly order, coordinate compiler/blocker writes, validate actual CLI argument types, and permit concurrent provider work while rejecting stale attempts.

## Stable finding status

| ID | Status | Final implementation and executable evidence |
|---|---|---|
| **Important-1** | **Resolved** | `scripts/prepare_slide_prompts.py:483` excludes repair compilation from accepted-final short circuits. `test_accepted_sample_repair_dispatches_and_preserves_style_snapshot` verifies pending repair→dispatch→result→QA→current user image acceptance while the immutable style snapshot stays unchanged. |
| **Important-2** | **Resolved** | Calibration repairs keep their original `render_phase` and sample prerequisites (`prepare_slide_prompts.py:472`, `planning_contract.py:545`). The additional accepted-calibration branch at `prepare_slide_prompts.py:491` preserves actual repaired sample provenance. `test_unapproved_calibration_repairs_without_approving_defective_sample` now continues through sample acceptance, full production compilation, remaining slide result/QA, complete-sequence QA, actual synthetic image review, and successful PPTX assembly. |
| **Important-3** | **Resolved** | `prepare_slide_prompts.py:459` rejects a missing tracked prompt before changing phase or state. `test_missing_tracked_prompt_cannot_bypass_repair_or_dispatch` confirms refusal and unchanged job bytes. Existing repair counters and phase guards remain intact. |
| **Important-4** | **Resolved** | `planning_contract.py:604` permits approved regeneration of an original first-batch member while later production remains gated on that member's current QA. `test_first_batch_revision_regenerates_before_later_production` verifies redispatch succeeds and later dispatch remains blocked until current QA passes. |
| **Important-5** | **Resolved** | `assemble_ppt.py:510` selects jobs using canonical spec order. `test_assembly_uses_plan_order_after_job_array_reordering` verifies the actual first PPTX image blob stays red and receives slide 1's opening notes after reversing the stored job array. |
| **Important-6** | **Resolved** | `record_slide_result.py:219` stages/verifies a new candidate and lines 252–256 install final image and jobs as a grouped transaction. `test_partial_result_copy_preserves_previous_image_and_jobs` and `test_result_state_write_failure_preserves_previous_image_and_state` confirm previous image/state bytes survive both partial-copy and jobs-write failures. |
| **Important-7** | **Resolved** | `prepare_slide_prompts.py:541` groups changed prompts and updated jobs state. `test_compilation_rolls_back_prompt_and_jobs_write_failures` confirms rollback when the first prompt, second prompt, or jobs write fails. |
| **Important-8** | **Resolved** | `generation_execution.py:14` compiles a shared executable operation/parameter policy; lines 31–35 strictly validate integer `n` and compression values. `run_slide_job.py:44` forwards configured parameters and verified image snapshots. Actual bundled CLI dry-runs verify text-only calibration uses generate, image-conditioned production/repair uses explicitly approved edit, model/size/quality/output settings are forwarded, and every image is supplied. Invalid float/bool/string integer representations are refused before job creation/dispatch. |
| **Important-9** | **Resolved** | `prepare_slide_prompts.py:427` and `record_slide_blocker.py:29` use planning→jobs lock order. `test_compiler_and_blocker_do_not_lose_interleaved_state` confirms a worker blocker waits for compilation and its resulting blocked state survives. Run-state synchronization occurs after the jobs locks are released. |
| **Important-10** | **Resolved** | `run_slide_job.py:27` validates/stages under the global locks, line 56 runs the provider outside them, and lines 59–74 revalidate job/current inputs/dispatch plus candidate ratio. Per-candidate locking preserves ownership without serializing the deck. `test_two_provider_calls_overlap_without_global_state_locks` uses a two-worker barrier and independent state update to prove overlap. `record_slide_dispatch.py:62` adds a unique attempt ID. Independent probes confirm same-agent/new-attempt and source drift are rejected on return. |

## Independent verification

Focused regression/execution suites were independently rerun with the existing interpreter, `-B`, and all temporary roots redirected into the assigned review scratch directory:

```powershell
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B 'C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-final-core-review-c1984fa745a547259759a8bfb0ea53ae/review/run_tests.py'
```

**Observed exit 0: 19 tests passed in 39.126 seconds** — 10 review regressions plus 9 managed execution tests. This includes the repaired-calibration path through actual synthetic assembly, strict integer parameter preflight, provider overlap, real CLI dry-run method consumption, immutable snapshot bytes, stale-attempt refusal, and result/compiler failure rollback.

Additional independent failure/integration probes:

```powershell
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B 'C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-final-core-review-c1984fa745a547259759a8bfb0ea53ae/review/final_probes.py'
```

**Observed exit 0**, with these asserted results:

- **Original-source drift during provider work:** staged image bytes match their hash-named snapshots; changing the original source while the backend runs causes post-call rejection (`Missing or stale visual approval for slide_01`); no usable candidate summary is returned.
- **New attempt with the same agent:** replacing only the dispatch attempt UUID while retaining the agent produces `Dispatched attempt changed during backend execution`; no usable result is emitted.
- **Provider failure:** mocked exit 7 is propagated; existing final-image and jobs bytes remain unchanged; no candidate-success summary is emitted.
- **Incorrect provider ratio:** a synthetic square candidate is rejected against the approved 16:9 ratio before returning a usable result.
- **Actual repair adapter integration:** initial result→needs-repair→compiled repair→authorized dispatch→mocked adapter `edit`→normal result recorder→agent QA completes successfully, with repair count exactly 1 and current recorded/passed state.

No live image/API call, installation, commit, publication, or source/repository edit was performed. Probe files and transient decks were confined to `review/`; temporary fixtures are cleaned up by the scripts. Synthetic decisions and PNGs remain test evidence rather than real user approval or production model output.

## Findings, decisions, and limits

**All ten stable findings are resolved. New demonstrated defects: none.**

Open severity counts: **Critical 0 / Important 0 / Minor 0**. There is no unresolved scope finding.

Review decisions: accept the explicit approved reference-operation policy as an executable implementation of the user's backend requirement; preserve completed repaired-sample provenance instead of rewriting it merely to match production style inputs; test actual CLI parsing and bytes/attempt transitions; assess concurrency with provider mocks rather than call a paid service; do not expand synthetic evidence into claims about actual model lettering, source-chart pixel fidelity, factual truth, natural voice, or real user decisions.

Coverage limits: this review independently ran the 19 focused suites and the additional probes, not the entire repository test suite. Pending public documentation and the main agent's final aggregate verification remain outside this core review result. Provider availability and real rendered/speaker quality still need the specified workflow checks during real deck runs.

## Readiness

**Managed core review is clear for Tasks 2–6 within the approved contract.** There are no remaining demonstrated code-review blockers from Important-1 through Important-10. Continue the remaining documentation/aggregate verification before claiming the complete feature delivered. This internal review is not authorization to commit, push, merge, or publish.
