# Managed core follow-up review

Frozen snapshot: `C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-fixed-review-0f104cfc5fdf4d40ae275d34dcd17678/codex-ppt`.

Comparison baseline: `C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-core-review-1d5apjke/review/report.md` and its original snapshot. Plan: this snapshot parent's frozen `implementation-plan.md`. Locations below refer to the fixed snapshot unless explicitly identified as historical. No source or repository edits were made.

## Scope and strengths

The changes remain coherent with Tasks 2–6 and the nine review findings. The additional executable generation policy and CLI adapter address a real integration gap; they are within scope. Pending skill/docs/localization Tasks 7–8 are excluded.

Seven original findings are resolved. Repair jobs now retain whether they are repairing calibration or production. Immutable sample references survive accepted-final repair; first-batch members can regenerate after scoped approval; assembly consumes canonical plan order; result and compiler writes use grouped transactions; compiler and blocker share planning→jobs lock order. The CLI adapter forwards actual prompt/config/image inputs and uses an explicit approved `reference_mode="edit"` policy for image-conditioned production, preserving text-only calibration. These are substantive improvements supported by running tests and additional failure probes.

Two original findings have residual failures, and the new adapter introduces a concurrency regression.

## Stable-ID status

| ID | Status | Evidence / fixed location |
|---|---|---|
| Important-1 | Resolved | `prepare_slide_prompts.py:483` excludes repair from accepted-final short circuits. `test_accepted_sample_repair_dispatches_and_preserves_style_snapshot` runs needs-repair→compile→dispatch→result→QA→user image approval and confirms immutable style bytes are unchanged. |
| Important-2 | Partially resolved; open | `render_phase` fixes the initial missing-sample repair prerequisite (`prepare_slide_prompts.py:472`, `planning_contract.py:545`). The next transition from approved repaired calibration into production still fails; see finding below. |
| Important-3 | Resolved | `prepare_slide_prompts.py:459` refuses a missing tracked prompt before phase choice or writes. `test_missing_tracked_prompt_cannot_bypass_repair_or_dispatch` confirms refusal and byte-identical jobs state. |
| Important-4 | Resolved | `planning_contract.py:604` permits regeneration of existing first-batch members while other members remain gated on current QA. `test_first_batch_revision_regenerates_before_later_production` confirms blocked later dispatch until the revised first image passes QA. |
| Important-5 | Resolved | `assemble_ppt.py:510` looks up jobs in canonical spec order. `test_assembly_uses_plan_order_after_job_array_reordering` verifies the red first image blob and corresponding opening notes after job-array reversal. |
| Important-6 | Resolved | `record_slide_result.py:219` stages/verifies the candidate; lines 252–256 group final-image/jobs installation. Existing partial-copy regression passes. Additional independent state-write failure probe confirms old image and job bytes both survive and the transaction marker is removed after rollback. |
| Important-7 | Resolved | `prepare_slide_prompts.py:532` groups prompt payloads and jobs state. `test_compilation_rolls_back_prompt_and_jobs_write_failures` verifies rollback for first prompt, second prompt, and jobs-write failures. |
| Important-8 | Mostly resolved; open parameter preflight gap | `generation_execution.py` and `run_slide_job.py` now map/forward configured operations, size/quality/model/output parameters, and every image input. Real bundled CLI dry-runs pass for supported integer configurations and text-only calibration. Numeric values accepted by compiler/dispatch can still fail CLI parsing; see below. |
| Important-9 | Resolved | `prepare_slide_prompts.py:427` and `record_slide_blocker.py:29` share planning→jobs ordering. `test_compiler_and_blocker_do_not_lose_interleaved_state` confirms the blocker waits for compilation and its final blocked state persists. |

## Open findings

### Important-2 — Repaired calibration cannot transition into production after acceptance

**File:line:** `scripts/prepare_slide_prompts.py:490`–`497`; accepted-final exclusion at lines 483–484.

**What's wrong:** The initial unapproved calibration repair now works. After the repaired image passes agent QA and the user accepts it as the representative sample, full production compilation still sees its recorded repair request. `keep_finished_repair` compares the old calibration repair's empty `sample_refs` with the new production job's approved sample references, rejects that difference, and raises the phase-bypass error. The accepted-final condition also excludes all previous repair-phase jobs.

**Why it matters:** A normal calibration sequence still cannot reach production if its first candidate needed a repair. The new regression proves repair and acceptance but stops one operation before this failure. Re-approving a defective first image is no longer necessary, but manual state surgery would still be required to proceed after the successful repair.

**Executable evidence:** `review/followup_probes.py`, `repaired_calibration_to_production`: plan approval → sample compile/dispatch/result → needs-repair → repair compile/dispatch/red result → QA pass → actual synthetic sample approval → full production compile with `--force`. Every step through sample approval exits 0; production exits 1 with `Recorded repair requires --phase repair; production/sample cannot bypass the repair limit`.

**How to fix:** Preserve the completed accepted calibration repair as its actual generation provenance when it has current QA and an accepted-final sample binding. Its calibration inputs should not be replaced by the later production style-input set merely to prepare other slides. Extend the regression through full production compilation, remaining slide dispatch/results, and final approval/assembly readiness while retaining one-repair accounting.

### Important-8 — Executable contract accepts numeric arguments that the bundled CLI rejects

**File:line:** `scripts/generation_execution.py:31` and `42`; argument emission at `scripts/run_slide_job.py:43`–`45`.

**What's wrong:** The preflight compares `n` by numeric equality and calls payload validators that use `int(value)`. Thus JSON `n: 1.0` and `output_compression: 50.5` pass compilation and dispatch. The adapter emits their original strings `1.0` / `50.5`, while the bundled CLI declares those arguments as integers, so the real invocation fails during argparse processing. No API access is necessary to observe this.

**Why it matters:** The approved executable contract is supposed to reject unsupported parameters before dispatch. These accepted configurations strand a dispatched job and contradict the preflight guarantee. Forwarding the fields correctly is insufficient unless their actual CLI representation is valid.

**Executable evidence:** `review/followup_probes.py`, two `noninteger_cli_parameter` cases: each deck compiles and dispatches with exit 0. Adapter dry-run exits 2 with either `argument --n: invalid int value: '1.0'` or `argument --output-compression: invalid int value: '50.5'`.

**How to fix:** Validate integer parameters explicitly, reject booleans/fractional numeric values, and either reject noncanonical numeric representations or normalize only semantically valid integers into the compiled execution projection. Ensure compiler/consumer/adapter share the same normalized argument contract. Add actual adapter dry-run regressions for integer, float, boolean, and invalid optional values.

### Important-10 — The CLI adapter holds global state locks throughout image generation

**File:line:** `scripts/run_slide_job.py:25` and `50`.

**What's wrong:** The adapter enters both the deck-wide planning lock and the jobs lock, then keeps them held during the external image-generation subprocess. Every other managed worker and dispatch/result/QA/blocker command needs those same locks.

**Why it matters:** Approved concurrency no longer produces concurrent CLI generation. An expensive provider request serializes all workers for that deck and blocks normal result/exception recording for its duration. The scheduling capacity still reports multiple available/dispatched jobs, so this silently changes the retained concurrency behavior and prevents timely first-batch feedback.

**Executable evidence:** `review/followup_probes.py`, `backend_call_holds_global_locks`: invoke the adapter through a valid dispatch, substitute only the provider subprocess, and have an independent worker acquire each lock while the subprocess hook is active. Both attempts time out: `.planning.lock="blocked"`, `.slide_jobs.json.lock="blocked"`. No live call, paid generation, or sleep is involved.

**How to fix:** Under the normal lock order, validate the dispatch/job SHA and stage verified immutable prompt/input snapshots and the candidate ownership path. Release global locks before calling the backend. Revalidate the current dispatched attempt and hashes after the call before returning a usable result, preserving stale-attempt refusal. Add a two-worker mock regression proving backend operations overlap and independent status/exception updates can complete while generation runs.

## Verification evidence

Independent focused command:

```powershell
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B 'C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-fixed-review-0f104cfc5fdf4d40ae275d34dcd17678/review/run_tests.py'
```

Observed exit 0: **13 tests passed in 25.636 seconds**, comprising all nine tests in `test_review_regressions.py` and four in `test_managed_execution.py`.

Independent additional probes:

```powershell
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B 'C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-fixed-review-0f104cfc5fdf4d40ae275d34dcd17678/review/followup_probes.py'
```

Observed exit 0 with these probe results:

```json
{"probe":"repaired_calibration_to_production","production_rc":1,"error":"Recorded repair requires --phase repair; production/sample cannot bypass the repair limit"}
{"probe":"result_state_failure_rolls_back","image_preserved":true,"jobs_preserved":true,"marker":false}
{"probe":"backend_call_holds_global_locks",".planning.lock":"blocked",".slide_jobs.json.lock":"blocked"}
{"probe":"noninteger_cli_parameter","field":"n","value":1.0,"dispatch_rc":0,"execution_rc":2}
{"probe":"noninteger_cli_parameter","field":"output_compression","value":50.5,"dispatch_rc":0,"execution_rc":2}
```

All test/probe temporary roots were placed inside the assigned `review/` scratch area; `-B` and `PYTHONDONTWRITEBYTECODE` prevent source cache writes. Synthetic images, decisions, filesystem faults, CLI dry-runs, and mocked provider operations do not establish real user approval, backend availability, rendered lettering, factual truth, or natural speaker delivery. No live API call was performed. The full suite was running elsewhere when review was dispatched and is not claimed GREEN by this report.

## Decisions and readiness

Review decisions: preserve the approved executable `reference_mode` policy rather than require an identical HTTP endpoint for text-only and image-conditioned calls; keep original finding IDs; mark improvements resolved only where the full relevant transition/failure evidence supports them; report the concurrency regression as the new stable **Important-10**; do not treat pending documentation as code defects.

Open counts: **Critical 0; Important 3; Minor 0.** Original nine: **seven resolved, two partially resolved/open**. One new Important finding.

**Not yet ready to claim production-ready Tasks 2–6 or merge readiness.** Fix the repaired-calibration transition, exact integer CLI preflight, and adapter lock duration, then verify full calibration→production→review→assembly and concurrent mocked execution. Existing transaction, immutable-reference, ordered-output, and lock-coordination fixes are supported and should be retained.
