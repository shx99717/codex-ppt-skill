# Independent runtime review

## Original review

Changeset scope matches the plan. The implementation preserves attempt binding, ordered input evidence, distinct trust labels, original image bytes, and mandatory execution versions. No unrelated runtime changes found.

Findings:

- **R1 — Important — `skills/codex-ppt/scripts/generation_execution.py:46`**
  **Problem:** Managed capability validation reads `OPENAI_BASE_URL` before loading runtime `.env`, while `image_gen.py` loads that file before execution.
  **Trigger/impact:** A provider configured only through `CODEX_PPT_HOME/.env` gets rejected during compilation/current-job checks as a profile mismatch. I reproduced rejection followed by successful validation after calling `_load_runtime_env()`.
  **Fix:** Resolve effective runtime configuration consistently before compiler and consumer validation.
  **Validation:** Test provider configuration supplied exclusively through a temporary runtime `.env`, including compilation, dispatch, and adapter execution.

- **R2 — Important — `skills/codex-ppt/scripts/image_providers/atlascloud.py:194`**
  **Problem:** Routing still rewrites every configured model ID, stripping operation suffixes, adding an `openai/` namespace when absent, and appending `/edit` or `/text-to-image`.
  **Trigger/impact:** `vendor/exact-route` becomes `vendor/exact-route/edit`; capability evidence binds the configured ID rather than that substituted request route. This leaves the plan’s explicit configured-route preservation requirement unimplemented and can select an undocumented route.
  **Fix:** Preserve exact documented routes. Make any operation-specific routing explicit in approved provider configuration, or restrict legacy conversion to explicitly supported aliases.
  **Validation:** Assert exact submitted IDs for provider-specific identifiers and operation-specific IDs; reject unknown route conversions before submission.

- **R3 — Important — `skills/codex-ppt/scripts/image_providers/atlascloud.py:133`**
  **Problem:** The adapter silently drops approved `background`, `input_fidelity`, `output_compression`, and `moderation` parameters. New capability validation can approve them, but only size, quality, and format reach the provider.
  **Trigger/impact:** An approved transparent-background or fidelity-sensitive job executes without those settings and can receive `adapter_verified` evidence despite the incomplete request.
  **Fix:** Implement documented translations or reject unsupported adapter parameters before invoking the provider.
  **Validation:** Capture actual request bodies for each supported setting and assert unsupported settings fail before network execution.

- **R4 — Important — `skills/codex-ppt/scripts/image_gen.py:907`**
  **Problem:** Batch capability validation runs against command-line defaults before JSONL overrides are merged. Effective per-job payloads receive only generic validation at lines 565 and 618.
  **Trigger/impact:** I reproduced a successful dry-run using a profile bound to `approved-model`, medium quality, and minimum 100,000 pixels, while the actual job used `UNPROFILED-MODEL`, `REJECTED-QUALITY`, and `32x18`. Real batch execution follows the same unchecked merge.
  **Fix:** Validate each merged payload against the supplied profile in both dry-run and execution paths.
  **Validation:** Add batch cases overriding model, quality, size, and background; mismatches and known unsupported values must fail before provider calls.

- **R5 — Minor — `skills/codex-ppt/scripts/generation_execution.py:16`**
  **Problem:** `output_requirements` becomes accepted control metadata without schema validation during compilation. Validation happens only when measuring a generated candidate.
  **Trigger/impact:** Requirements such as `{"min_width": false}` compile successfully, then fail after potentially paid generation.
  **Fix:** Extract requirement-schema validation and invoke it during approved-plan/compilation validation as well as output measurement.
  **Validation:** Invalid keys, booleans, nonpositive dimensions, and malformed requirement containers should fail before dispatch.

Verification: 15 focused tests passed across submission evidence, capabilities, input contracts, output requirements, and backend contracts. `git diff --check` passed. Reproductions were offline; no live image-generation claims, network calls, or repository edits.

## Follow-up review of fixes

Scope remains coherent. R1, R2, R3, and R5 are resolved in the reviewed source: managed validation loads runtime configuration; explicit Atlas routes are preserved and conflicting operation suffixes rejected; unsupported Atlas settings fail before transport; output-requirement schemas are validated during compilation. R4 now rejects unsupported merged batch overrides in dry-run, preflight, and per-job execution paths.

### Remaining finding

- **R4 — Important — `skills/codex-ppt/scripts/image_gen.py:918`**
  **Problem:** Main-level capability validation still checks unmerged batch defaults before the new effective-payload validation. The negative override bypass is fixed, but valid per-job overrides can be rejected because defaults that will never be submitted do not match the profile.
  **Concrete trigger:** A profile documents `qualities: ["max"]` and `size_constraints: {"max_edge": 1000}` for `vendor/model`. Every JSONL job explicitly sets `quality: "max"` and `size: "160x90"`; the CLI supplies that model/profile without redundant `--quality` or `--size`. The command fails with `ValueError: Unsupported API setting: qualities` because main validates default `medium` before reading the effective jobs. Default `2560x1440` would similarly fail despite the valid per-job size. This was reproduced through the real CLI parser in an offline dry-run.
  **Impact:** The supplied profile rejects valid supported batches and requires redundant CLI defaults matching values already overridden by every job.
  **Fix:** Skip main-level profile validation for `generate-batch`; validate the complete merged payloads through the new preflight/dry-run paths. Keep single-generate/edit validation.
  **Suggested validation:** Add a positive batch regression where profile-incompatible defaults are completely overridden by profile-supported JSONL values. Assert accepted dry-run and fake-provider execution, while retaining the negative override tests.

Follow-up verification: all 26 tests passed across `test_image_capabilities.py` (6), `test_output_requirements.py` (2), `test_provider_input_boundary.py` (3), `test_image_gen.py` (1), `test_managed_execution.py` (10), and `test_submission_evidence.py` (4). `git diff --check` passed. Provider boundary tests used fake SDK/HTTP transports. No paid or network generation occurred. Only this review evidence file was written by the reviewer.

## R4 closure verification

R4 is resolved. Main-level profile validation now excludes `generate-batch`; merged-payload checks remain in the batch dry-run, preflight, and execution paths. The positive regression `test_batch_supported_overrides_replace_unused_defaults` exercises supported `quality=max,size=160x90` JSONL values overriding unused incompatible defaults. The negative override cases remain covered.

Independent verification command: `python -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_image_capabilities.py -v`. Actual result: 7 tests passed, exit 0. The positive regression printed the expected effective max/160x90 dry-run payload and created no provider. No paid or network generation occurred. This was a targeted closure check, not a new review cycle. No unresolved original R1–R5 findings remain.
