# Image backend capabilities: implementation delivery

Date: 2026-10-16. Repository: `D:\git\codex-ppt-skill`. Branch: `feature/SQ5GEN-predictable-deck-generation`.

The approved cold handoff plan is implemented as uncommitted source changes. No user decision blocks source delivery. No commit, push, PR, release, installed-skill update, or paid generation was performed.

## Resulting behavior

- Callable Codex `image_gen` remains recommended without dedicated ratio/size fields. Request the approved ratio in its prompt and measure original output pixels. Native model identity remains host-managed.
- Cursor `GenerateImage` uses its live supported ratio argument. The user's 2026-10-16 evidence supersedes the older fixed-ratio assumption; this implementation run did not call Cursor.
- API fallback retains the explicitly configured model, without a permanent model default or model-family substring restrictions. Missing configuration requires a documented selection. Capability evidence is bound to the exact provider, model and operation; required unknowns block managed work.
- All compiled source/style inputs require ordered attachment evidence bound to immutable hashes, job, dispatch attempt and candidate. Native/bridge receipts remain `agent_reported`. Adapter verification requires successful registered execution; missing evidence, dry-run completion, substituted inputs and stale attempts cannot establish it. Local records are consistency checks, not security attestation against a malicious filesystem writer.
- Output records include measured dimensions and ratio. Mandatory min/exact size requirements are distinct from preferences and checked against original pixels. Prompted native resolution remains unproven; API resolution documentation does not establish native limits.
- Only 16:9 and 4:3 are supported. The bundled 3:2 template is deleted; both supported templates and all twelve visual styles remain. Existing exported PPTX files and historical smoke evidence are preserved. New managed operations on historical artifacts require recompilation and fresh evidence; no automatic migration is added.
- Worker instructions, primary generation commands, README/site documentation in Chinese/English/Korean, smoke guidance and Unreleased changelog are synchronized.

## Verification actually run

| Check | Actual result |
|---|---|
| Full script suite: `python -B -m unittest discover -s skills/codex-ppt/scripts/tests -v` | 190 tests passed, 156.457 seconds, exit 0; no skips reported |
| Smoke verifier suite: `python -B -m unittest discover -s tests/smoke-deck -p 'test_*.py' -v` | 10 tests passed, 0.258 seconds, exit 0 |
| Separate skill/frontmatter/local-link check | 3 tests passed, 0.007 seconds; also included in the 190 above |
| Changed Python AST parse | 30 changed/new Python files parsed successfully |
| Whitespace check: `git diff --check` | Exit 0 |
| Active retired-ratio scan | Only rejection tests and removal notice remain; historical plans/memory/smoke runs intentionally retained |
| Fixed-model scan | No fixed production model default; empty/None defaults require configuration. Remaining compiler text recognizes and removes obsolete historical size metadata rather than selecting that model |
| Asset retention | 16:9 and 4:3 PPTX templates present; 3:2 template absent; twelve reference style files retained |

Full suite output was captured in the local temporary `codex-ppt-capabilities-tests.log`. Provider boundary tests invoke the actual CLI with fake OpenAI SDK and AtlasCloud HTTP transports, checking ordered reference bytes and exact route IDs. No live paid-provider claim follows from those mocks.

## RED/GREEN evidence

The initial five backend regression tests failed against the old implementation before fixes. New contract-module tests initially failed on missing imports. The later batch positive regression also failed before its correction with `Unsupported API setting: qualities`, then passed after validation moved to merged effective job payloads.

Actual hypothetical behavioral responses are preserved in [RED evidence](2026-10-16-image-backend-red.md) and [GREEN evidence](2026-10-16-image-backend-green.md). Six scenarios cover native eligibility, Cursor arguments, model drift, input capacity, resolution honesty and retired ratios. These used the same evaluator exposed to expected results, so they are not a blinded independent evaluation or executed image-generation proof. Earlier native ratio/resolution experiments and dated official model facts remain in the plan and session memory.

## Review closure

Original findings and follow-ups remain verbatim in the [runtime review](2026-10-16-image-backend-runtime-review.md) and [guidance review](2026-10-16-image-backend-guidance-review.md).

| ID | Correction and closure |
|---|---|
| R1 | Load runtime environment before managed provider capability binding; regression passed |
| R2 | Preserve exact AtlasCloud model route; reject conflicting operation suffix; boundary tests passed |
| R3 | Reject unsupported AtlasCloud settings before transport instead of silently dropping them; boundary tests passed |
| R4 | Validate merged per-job batch settings; skip unused default profile validation; positive and negative regressions passed; reviewer closed |
| R5 | Validate output requirement schema during compilation before provider work; tests passed |
| D1 | Primary result command includes the mandatory submission receipt |
| D2 | Actual provider boundary exercised with fake SDK/HTTP, checking every input byte |
| D3 | Negative managed tests assert specific errors and unchanged state instead of swallowing broad assertions |
| D4 | Correct translated wording and restore Korean fallback/subscription caution |

Both reviewers independently verified their original finding closures. No unresolved review findings remain. GitHub workflow files were unchanged, so workflow YAML/shell checks were inapplicable.

## Remaining limits

Exact native resolution control and a universal maximum have not been established. Native attachment receipts remain agent reports. Cursor evidence is user-provided and dated. Live provider compatibility depends on the selected provider's current documented capabilities and actual responses. Deployment of the installed skill is separate work and has not occurred.
