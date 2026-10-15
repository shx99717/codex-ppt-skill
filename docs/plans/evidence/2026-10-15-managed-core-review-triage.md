# Managed Core Review Intake

Date: 2026-10-15. Review basis: frozen Tasks 2–6 snapshot, base `99fba3d3ea2d8f1d285cf40dbf44d8e32f05d126`. See [complete report](2026-10-15-managed-core-review.md).

The earlier 145 passing tests are evidence for their covered cases, not evidence against these additional failures. I discarded the prior readiness conclusion, checked every referenced module against the reviewed snapshot (all six relevant source files have identical SHA256), and reran all three independent probe scripts. The user authorized continuous execution and routine fixes; no additional design or publication decision is needed for these corrections.

| ID | Falsification attempt and observed evidence | Decision |
|---|---|---|
| Important-1 | Actual accepted-sample repair compile succeeds but status is accepted; dispatch exits 1. Existing sample-preservation test does not exercise repair dispatch. | ACCEPTED |
| Important-2 | Actual first-sample repair exits 1 for missing sample approval; alternate sample phase also exits 1. No usable calibration-repair route. | ACCEPTED |
| Important-3 | Delete tracked prompt after exhausted repair; production recompile and dispatch both succeed with repair count still 1. File absence defeats the guard. | ACCEPTED |
| Important-4 | Approved first-member wording revision yields pending job but dispatch exits 1 because that member's own new QA is missing. | ACCEPTED |
| Important-5 | Reversed jobs pass ready preflight and assembly. First image pixel is white instead of approved red, with slide-one notes. | ACCEPTED |
| Important-6 | Injected partial copy leaves jobs intact but overwrites prior image with incomplete bytes. Consumer rejection afterward does not restore artifact. | ACCEPTED |
| Important-7 | Injected second-prompt write failure preserves jobs but changes first prompt; no transaction marker. | ACCEPTED |
| Important-8 | Actual bundled CLI dry-run ignores nested high quality/3840×2160 settings and style input, using medium/2560×1440/text-only generation. Manual edit attaches inputs but changes operation. | ACCEPTED |
| Important-9 | Actual blocker CLI interleaving records blocked, then compiler overwrites pending and clears blocker. Planning lock alone does not coordinate both writers. | ACCEPTED |

All severities remain Important. No findings were rejected or left unverified. Corrections retain the approved architecture: immutable references, actual scoped decisions, bounded repairs, first-batch QA, exact sequence, fail-closed grouped mutations, and the existing CLI backend. Add regression RED before each implementation change, then GREEN and follow-up review. Any executable reference-operation mapping must be explicit in the approved generation policy, never silently change endpoints or omit inputs.
