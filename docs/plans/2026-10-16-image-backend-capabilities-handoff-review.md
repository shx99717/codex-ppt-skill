# Critical Review: Image Backend Capabilities Handoff

**Date:** 2026-10-16 Asia/Shanghai
**Artifact reviewed:** docs/plans/2026-10-16-image-backend-capabilities-handoff.md
**Method:** Main-agent source inspection plus the available think-mcp sequentialthinking tool. No reviewer subagent was dispatched. No implementation was performed and no new runtime test results are claimed.
**Initial verdict:** Revise before cold execution. The scope matches the user's decisions, but three substantive contract gaps leave implementation choices that should be settled in the handoff. One smaller source-map error should also be corrected. See the authorized revision/re-review below for current status.

## Finding 1 — Important: Attachment requirements are optional at the version boundary

**Plan locations:** Section 0.6 attachment manifest (line 132), Task 4 step 4, Task 5 step 6.

The plan calls input_contract_version=1 "suggested" metadata in the author-approved generation method while also requiring every new compiled attempt to carry evidence. It preserves older records, but never defines how the runtime distinguishes a legitimately historical job from a newly compiled job that simply omitted the field. An executor could implement `if version == 1: require_receipt()` and accidentally allow new jobs to bypass the requirement by omitting the optional field.

The current compiler reads an approved canonical spec and compares generation configuration against it. It cannot silently add approved generation metadata without affecting the method's fingerprints. The handoff must specify where the authoritative compiler/contract version lives and how approval transitions work.

**Correction to include:** Give newly emitted jobs a mandatory compiler-owned contract version, validate supported versions explicitly at dispatch/result/assembly, and require fresh attempts compiled by the revised tool to use the new evidence contract regardless of whether the author supplied a metadata flag. Preserve historical output/approval records without relabeling them; define read-only compatibility versus new execution explicitly. If the change needs an approved method update, provide one clear reapproval/recompile path rather than auto-mutating the canonical spec. Do not use timestamps as an authenticity signal.

**Required tests:** A new spec without an input version cannot produce an evidence-free accepted result; deleting/downgrading the job marker fails currency/hash checks; previously approved supported-ratio output remains historical rather than being claimed verified; a new attempt on an old deck requires the explicit contract transition. Existing 3:2 remains rejected.

## Finding 2 — Important: Receipt provenance and the example schema are incomplete

**Plan locations:** Section 0.6 receipt example (lines 134-149), Task 5 steps 1, 3-5.

The plan correctly says worker-authored JSON cannot claim adapter_verified. However, it describes a freely supplied --submission-receipt file and a verification string without specifying the trusted local state the recorder checks to distinguish adapter output from a worker assertion. A path or declared verification value alone is not evidence of the producer. This matters for honest executions too: a dry-run or an earlier attempt's receipt could be mistaken for a real submission.

The concrete receipt example also omits the attempt identity and candidate hash that the surrounding prose requires. A cold executor may implement the example as the schema and miss those bindings. The repository already has `dispatch.attempt_id`, a UUID created by record_slide_dispatch.py, so the plan should explicitly reuse it rather than leave identity design open.

**Correction to include:** Specify a complete receipt schema with dispatch.attempt_id, agent_id, job SHA, backend/tool, operation, ordered attachment hashes/roles, candidate path/hash, mechanism and evidence origin. In a real CLI execution, the adapter must register a completion/evidence record through the existing locked job-state pathway after provider success and dispatch revalidation. Result recording derives adapter_verified by matching that registered record against the current attempt and candidate, not by trusting the submitted JSON label. Native/bridge worker evidence remains agent_reported unless actual host evidence is inspected. Dry-run never registers successful execution. Preserve the explicitly stated limit that local shared-filesystem state is not a security boundary against a malicious executor; no signatures/service framework needed.

**Required tests:** Setting verification=adapter_verified in an unregistered receipt fails; registered dry-run fails; a receipt from a different attempt with identical job/candidate bytes fails; candidate substitution fails; failed/stale adapter execution never registers success; successful adapter registers and result recorder consumes the matching record.

## Finding 3 — Important: Unknown API capability policy mixes blocking and pass-through

**Plan locations:** Section 0.6 API capabilities (lines 114-130), Task 3 steps 1, 4-5.

Section 0.6 says unknown combinations require verification before proceeding. Task 3 also permits provider errors when no narrower rule is known and requires sufficient documented capabilities for new managed selections. The boundary is not explicit. One executor may require an extensive capability profile for all existing configured models, breaking the configured-model reuse promise; another may pass all unknown settings to the provider, undermining the preflight requirement. The plan does not state whether a missing capability field means unsupported or unknown.

**Correction to include:** Define unknown separately from supported/unsupported. Bind any recorded capability evidence to the actual model ID, provider/endpoint, and operation. Reuse the configured model; obtain documentation only for the settings/required image operation actually selected and missing from the recorded evidence, without repeating the user's model selection. New managed approval must not claim unknown required reference/quality/size capabilities are established. Keep structural CLI validation separate: a standalone explicitly requested API invocation may defer unknown provider-specific behavior to the provider, reporting failures honestly, but it cannot be used to manufacture a managed approval. Define omission semantics and make the exact CLI profile option/serialization executable in the plan.

**Required tests:** Missing profile facts remain unknown, not false or true; configured model is reused without a model-selection question; profile for model/provider A does not establish B; unknown required reference operation blocks managed production; explicit provider rejection is surfaced without substitution; known unsupported setting is rejected locally; native tools never require an API model profile.

This correction should not introduce automatic model discovery or a giant capability registry. The selected approach remains a small amount of method-specific documented metadata plus live native schemas.

## Finding 4 — Minor: Source map omits dispatch identity; search exclusions need exact paths

**Plan locations:** Section 0.5 source map and Task 8 step 3.

The map and task lists omit **scripts/record_slide_dispatch.py**, even though receipt binding should reuse its existing attempt_id. The executor would need an additional search to find the authoritative attempt identity. The verification command also excludes `plans/**` and `memory/**` although the historical folders actually live under `docs/`, so historical hits can obscure active guidance regressions.

**Correction:** Normalize the source map to repository-relative paths and add record_slide_dispatch.py with its existing attempt_id/agent_id/prompt SHA fields. Replace the active search exclusions with directory-aware globs such as `--glob '!docs/plans/**' --glob '!docs/memory/**'`; the current `!plans/**` and `!memory/**` patterns do not express the repository-relative paths intended. Historical negative fixtures should remain classified rather than blanket-deleted.

## What is sound

- The plan preserves all explicit decisions: capability-based native preference, configured API model first, no permanent native model assertion, and complete removal of 3:2/template.
- Ratio and resolution findings are accurately distinguished; no native 4K guarantee or universal 1.57 MP ceiling is claimed.
- Reference attachment is separated from actual figure fidelity and human image approval.
- The full evidence is embedded, with provenance of user-provided Cursor results clearly stated.
- RED/GREEN runtime and agent-pressure checks, translation parity, unchanged installed skill, and no commit/publish boundaries are specified.
- No automatic migration tool or unrelated template/style deletion is proposed.

## Review verification

Read the complete plan and checked the disputed sections against:

- skills/codex-ppt/scripts/prepare_slide_prompts.py:418-439 — managed compilation starts from approved spec and method.
- skills/codex-ppt/scripts/planning_contract.py:523-540 — compiled job/config/approval bindings.
- skills/codex-ppt/scripts/planning_contract.py:641 onward — assembly calls require_job_current for each slide.
- skills/codex-ppt/scripts/record_slide_result.py:178-199 — result recorder's dispatch/current-job boundary.
- skills/codex-ppt/scripts/record_slide_dispatch.py — authoritative dispatch.attempt_id already exists.
- skills/codex-ppt/scripts/generation_execution.py — existing control/provider parameter split.

These are plan-review findings, not claims that the proposed bugs exist in implemented code. No test suite was needed or run for production changes because no production changes were made. The plan and execute prompt have not been revised in this review; await the user's route choice.

## Authorized revision and second review — 2026-10-16

The user selected option 1 and explicitly instructed: "Patch the plan." The plan and its companion execute prompt were revised; the findings above remain as the historical first-review record.

1. **Finding 1 resolved:** Every revised compiler job/envelope has mandatory compiler-owned execution_contract_version=1, enforced by consumers. Optional author metadata cannot disable it. Historical files remain inspectable; new managed operations require the explicit approval/recompile/fresh-evidence transition. Old final-page records are not silently imported as new verified results.
2. **Finding 2 resolved:** The example now includes attempt_id, agent_id, candidate path/hash, operation, contract version, ordered attachments and evidence origin. The plan reuses dispatch.attempt_id and specifies locked slide.execution_completion registration by successful real CLI execution. The recorder derives adapter verification by matching registered state/receipt/candidate, rather than trusting a submitted label. Dry-run, stale and failed executions cannot register successful completion; replay/invalidation tests are explicit.
3. **Finding 3 resolved:** Missing facts mean unknown. Capability facts bind exact model/provider/operation and use a complete operations JSON wrapper. Managed required unknowns stop before production; explicitly requested standalone calls may defer unknowns to provider errors without creating approval. Configured model reuse does not repeat model selection. The exact --capabilities-file option and scratch serialization are specified.
4. **Finding 4 resolved:** Source map now includes record_slide_dispatch.py and explicit path interpretation. Verification globs exclude docs/plans and docs/memory by their actual repository-relative paths.

**Second-review method:** Main-agent contract consistency review and the available structured review tool. No subagent, production edit or paid generation was used.

**Fresh artifact checks:** Both JSON examples parsed successfully; the profile wrapper and required receipt fields were asserted; all four corrections, eight ordered tasks, Markdown fences and companion prompt references passed. git diff --check exited 0. git status showed only the intended memory/plan/prompt/review artifacts untracked; no production changes.

**Current verdict:** No unresolved issue from the four original findings remains in the revised handoff. The documents are ready for implementation review/execution by a fresh agent. This verdict concerns plan consistency only; implementation correctness, provider behavior and runtime test success remain to be established by executing the plan.
