# Managed core Windows concurrency correction review

Reviewed the single post-clearance correction in `skills/codex-ppt/scripts/run_slide_job.py:20`–`27` and the Windows-native regression in `skills/codex-ppt/scripts/tests/test_managed_execution.py:193`. This is a focused follow-up to the cleared managed core review; it does not reopen the complete Tasks 2–6 changeset.

## Scope and assessment

The implementation matches the demonstrated root cause documented in [Windows candidate-directory race](2026-10-15-windows-candidate-path-race.md). Comparing the current adapter with the previously cleared frozen snapshot shows only the short planning-lock region around candidate path resolution, confinement checks, and parent-directory creation, plus its explanatory comment. No unrelated runtime changes were found.

The fix is appropriate and minimal. Two legitimate managed workers cannot create their shared candidate parent while another resolves that parent under the planning lock. The confinement and new-PNG checks are retained. The initial planning lock is released before per-candidate ownership is acquired, so the change does not introduce a planning/candidate lock inversion. Provider work remains outside the global planning/jobs locks (`run_slide_job.py:60`); current attempt/input checks still run after it returns.

The new regression wraps the actual Windows native final-path call and permits a competing creator only when it can obtain the same planning lock. It exercises the real namespace-prefix failure rather than mocking a successful containment result.

## Independent verification

Existing interpreter: `C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe`, with `-B`. Test temporary roots and helper scripts were confined to the reviewer's existing local Temp scratch area; source/test files were not modified by this review.

```powershell
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B 'C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-final-core-review-c1984fa745a547259759a8bfb0ea53ae/review/run_windows_tests.py'
```

Observed exit **0**: **10 managed execution tests passed in 14.237 seconds**, including:

- The new Windows-native candidate-parent creation regression, which executed on Windows rather than being skipped.
- Two mocked provider calls overlapping at a barrier while an independent planning/jobs state update succeeds.
- Global locks being available during provider work and image inputs using byte-identical staged snapshots.
- Stale-attempt rejection, output confinement, executable config/image forwarding, strict integer preflight, text-only calibration, and repair operation policy.

The regression was also run against the previously cleared adapter via an isolated module replacement in scratch, without changing either source version:

```powershell
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B 'C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-final-core-review-c1984fa745a547259759a8bfb0ea53ae/review/verify_windows_red.py'
```

The one Windows test produced the expected **RED** on the previous adapter: a legitimate child resolved as `\\?\C:\...\candidates\new.png` while its root stayed `C:\...`, raising `Managed artifact must stay inside the deck`. The helper explicitly asserted that exact expected error and exited **0**. This independently confirms the test distinguishes the broken ordering from the corrected ordering.

Reviewed file SHA-256 values:

```text
run_slide_job.py
9E3976761D35907BB6FA2D111EBB0A171DD113A7EB00A7829DCF54537DC4A0C9

test_managed_execution.py
764905AAB5F6549AD072FA0D5617F271FEBC2773A747B5FD264A126CD7BBFCD5
```

## Findings and readiness

**No new review findings. Critical 0 / Important 0 / Minor 0.** The Windows correction is verified, and the prior **Important-1 through Important-10 remain resolved**. In particular, Important-10's provider-concurrency correction is preserved by the passing overlap and independent state-update checks.

Proceed with the planned complete-suite rerun and remaining delivery checks. This report confirms only this focused runtime correction; it does not claim the complete repository suite has passed after it. No live API calls, paid generation, source edits, installation, commits, pushes, merges, or publication were performed. Synthetic mocks/dry-runs do not establish real provider availability or rendered slide quality.
