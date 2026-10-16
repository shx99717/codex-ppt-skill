# Follow-up intake

Date: 2026-10-15. Basis: fixed Tasks 2–6 snapshot. [Full report](2026-10-15-managed-core-followup-review.md).

The 161 passing tests cover supported paths, not these uncovered cases. The reviewed core has not changed since the snapshot. I reran the independent follow-up probes before fixes: repaired calibration cannot compile production (exit 1); float n/compression compile and dispatch but dry-run exits 2; both global locks block during the mocked provider call. Result state-write failure preserves both prior image and jobs.

| ID | Evaluation | Decision |
|---|---|---|
| Important-1, 3, 4, 5, 6, 7, 9 | Resolved by full relevant regressions and independent probes. Retain fixes. | ACCEPTED resolution |
| Important-2 | Existing regression ends at sample acceptance. Next production compile still rejects the finished calibration repair because inputs differ. | ACCEPTED residual fix |
| Important-8 | Forwarded fields are correct, but equality/int coercion preflight permits floats rejected by actual argparse. | ACCEPTED residual fix |
| Important-10 | Adapter holds planning/jobs locks around expensive subprocess.run, preventing concurrent work and updates. | ACCEPTED new fix |

User continuous execution overrides the routine two-cycle review stop; these are implementation corrections within the confirmed design, not unresolved user choices. Extend RED tests through completed calibration→production→review→assembly, strict CLI integer parsing, concurrent provider mocks and stale post-call refusal. Stage immutable inputs while locked, release global locks for the call, and revalidate before returning. Follow-up review remains required before completion; no publication is authorized.
