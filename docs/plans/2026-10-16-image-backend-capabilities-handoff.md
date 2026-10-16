# Image Backend Capabilities Implementation Plan

> **For the implementing agent:** Follow this plan task-by-task. Complete each step, verify it works, then move to the next.

**Goal:** Make Codex PPT prefer available native image tools without permanent model assumptions, pass all approved reference images through the actual input mechanism, and support only 16:9 and 4:3 decks.

**Architecture:** Keep the existing managed v2 planning, immutable jobs, approval ledger, raster slide generation, and assembly. Separate backend identity, live tool controls, configured API model capabilities, attachment evidence, and measured output properties. Extend existing contracts and adapters rather than introducing automatic model discovery or a second generation framework.

**Tech Stack:** Python 3, unittest, filelock, Pillow, python-pptx, OpenAI-compatible and AtlasCloud adapters; Markdown skill and Chinese/English/Korean Docsify documentation.

**Mode: SELF-CONTAINED HANDOFF.** The executor needs no prior chat or memory file and must not ask the user to re-explain settled context. All task-specific decisions, evidence, proposed contracts, pressure prompts, and verification instructions are embedded here. Normal session-start rules still apply; start fresh and rely on this plan.

**Status:** Planning artifact only. Proposed functions and fields below are implementation instructions, not existing APIs or proof that behavior is implemented. The user requested a cold handoff, not implementation in this session.

**Review revision:** The user authorized patching all four critical-review findings. This revision specifies mandatory compiler-owned execution contracts, attempt-bound submission provenance, explicit unknown API capability semantics, and corrected source/verification paths. These are design specifications awaiting implementation, not runtime verification claims.

---

## Section 0: Full Context

### 0.1 Background and observed failures

The installed Codex PPT skill came from this repository. During a real Codex session, the agent followed the skill and excluded the callable native image_gen because its schema lacked size/aspect_ratio parameters. Subsequent actual native generations showed that prompt-only ratio control worked. The source also labels multiple backends as gpt-image-2, defaults API calls to that ID, and applies older constraints to newer model names through substring matching. The user additionally supplied fresh Cursor results proving its aspect_ratio parameter now works, invalidating a historical 3:2-only restriction.

The third concern is whether every reference reaches generation. Managed jobs correctly compile source snapshots and style samples, but a native/bridge worker can currently report a result without evidence of which images were actually attached. The bundled CLI has a stronger executable forwarding path. Preserve that distinction and improve traceability without claiming an agent-authored receipt proves a remote model saw the images.

### 0.2 Confirmed decisions — do not re-litigate

1. Edit **D:/git/codex-ppt-skill**, not C:/Users/raymond.shen/.codex/skills/codex-ppt. The user's mention of an SQ5 curated collection was explicitly corrected to this repository.
2. Complete scope: runtime, skill instructions, reference handoff, regression tests, affected multilingual docs/READMEs, changelog, review and verification. Documentation-only fixes were rejected.
3. Use capability-based selection. Automatic runtime model discovery and a minimal patch leaving assumptions intact were offered and not selected.
4. Prefer callable Codex native image_gen in Codex and callable Cursor GenerateImage in Cursor for supported deck requirements. Missing size/aspect_ratio parameters alone must not exclude image_gen or force a bridge/API fallback.
5. Native model identity is host-managed. Do not claim a specific internal GPT Image model without actual evidence; no model selector is exposed by this session's native tool.
6. API fallback reuses an explicitly configured model. If absent, the planning agent checks current official/provider documentation, recommends a model and obtains selection. Record the concrete API model in the approved deck method. Do not automatically reselect a model for every deck or silently choose a forever-current alias.
7. Ratio requests can use actual tool parameters or prompting, depending on the live schema. Measure original output width/height; preserve the existing 2% relative ratio tolerance. A prompt or successful tool argument is not proof of output geometry.
8. Resolution requests are preferences unless the user explicitly requires a minimum/exact resolution. Report measured pixels; never imply native 4K merely because the API supports it. If a mandatory resolution cannot be met, report a capability blocker before full production. Do not change backend silently.
9. Every required source/style input must be attached, retaining order, role and source bytes. Do not replace images with descriptions, silently truncate references, or treat view_image alone as universally sufficient attachment.
10. Record submission evidence with truthful trust levels. Adapter-controlled forwarding can be verified locally; agent-reported native/bridge calls are reported evidence unless a host call record can actually be inspected. Neither proves visual fidelity by itself.
11. **Remove 3:2 support completely**, including its bundled Medavis template, active options, runtime/assembly acceptance, examples and acceptance tests. The final wording was "A, and remove the 3:2 support completely and its template"; the explicit removal overrides the earlier option A suggestion to retain legacy 3:2. No grandfathered 3:2 mode.
12. Supported deck ratios are **16:9 and 4:3 only**. Already-created 3:2 PPTX files remain usable outside this skill. Existing project configs requesting 3:2 get a clear unsupported-ratio error. No automatic conversion or migration utility; do not stretch/crop/relabel their images. Negative tests and historical evidence may mention 3:2.
13. Keep the twelve visual styles. The only template deletion requested is the 3:2 Medavis ratio variant; retain the 16:9/4:3 templates, logos, and branded/plain/both modes.
14. Preserve unrelated v2 approval, source-hash, user review, notes, language and assembly guarantees. New evidence requirements must not pretend older records contain missing evidence. Preserve historical records and require recompilation/reapproval only where affected contracts need it.
15. Leave implementation uncommitted. No install/uninstall/bootstrap, installed-skill updates, paid generation, new user chat, commit, push, PR publication, merge, tag or release without separate user authorization. A future executor may run local mocked tests and edit the explicitly scoped tracked template.

### 0.3 Environment and repository governance

- Checkout: D:/git/codex-ppt-skill; PowerShell on Windows. Branch observed: feature/SQ5GEN-predictable-deck-generation. Inspect branch/status again; preserve user edits and do not invent another task ID or reset the checkout.
- Existing runtime known from repository guidance: C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe. Plain python also successfully ran the managed tests in this session. Locate an existing working interpreter; do not install dependencies automatically.
- Requirements: python-pptx>=1.0.2, Pillow>=10.0.0, openai>=2.0.0, filelock>=3.16.0.
- AGENTS.md: contribution metadata/changelog/release notes in English; documentation changes synchronize all existing language versions, including READMEs and usage site. User-visible changes go under CHANGELOG.md / Unreleased. Add a real PR reference only after a separately authorized PR exists. No invented PR number or version bump/release as part of this task.
- Source docs: root Chinese docs/*.md, English docs/en/*.md, Korean docs/ko/*.md; root README.md, README_en.md, README_ko.md. Plans/memory are internal English artifacts and do not require three translations.
- Repository was clean before memory/plan creation. The untracked docs/memory/memory-20261016-image-backend-capabilities.md and these handoff documents are intentional user-requested artifacts.
- Preserve old docs/plans and docs/memory as historical records. Do not rewrite old evidence to make searches appear clean.

### 0.4 Evidence embedded for a cold executor

**Native schema seen in this Codex session:** prompt, referenced_image_paths, num_last_images_to_include, transparent_background. No size, aspect_ratio or model argument. For edits with all targets on disk, inspect each local image first and use referenced_image_paths. Use recent-conversation image inclusion only if needed for targets without paths, with the smallest count including every required target (tool maximum here: five). Never supply both mechanisms. A different runtime must inspect its own actual schema rather than hardcoding this snapshot.

**Codex native ratio experiment:** one image per ratio, same scene (red ceramic sphere, pale blue studio background, no borders). Prompt: "The actual output image must have width:height aspect ratio X:Y. Use that ratio for the entire image canvas, not a rectangle inside a differently shaped image." Original PNG header measurements, no resizing/cropping:

| Requested | Actual pixels |
|---|---|
| 1:1 | 1254x1254 |
| 16:9 | 1672x941 |
| 9:16 | 941x1672 |
| 4:3 | 1448x1086 |
| 3:4 | 1086x1448 |
| 3:2 | 1536x1024 |
| 2:3 | 1024x1536 |
| 21:9 | 1916x821 |

All eight ratio errors were below 0.06%. This establishes observed prompt-ratio capability, not a universal success guarantee. Only 16:9/4:3 remain deck choices after this change.

**Codex native resolution experiment:** prompts explicitly demanded actual 16:9 pixel dimensions and native rendering. Requests 1920x1080, 2560x1440 and 3840x2160 each returned 1672x941; 7680x4320 returned 1672x940. Approximately 1.57 MP observed; higher-resolution prompting did not increase output. This is not a documented universal maximum.

**Cursor evidence supplied by the user, verified 2026-10-16 in Cursor:** optional aspect_ratio enum 1:1, 4:3, 3:4, 16:9, 9:16; no separate size parameter. One JPEG per enum value measured 1024x1024, 1152x864, 864x1152, 1280x720 and 720x1280 respectively. Visual inspection found full-frame backgrounds and different compositions, with no stretching/padding. Earlier August observations of fixed 1536x1024 output are obsolete. Do not use unsupported 3:2 or pass 16:9 expecting it secretly to return 3:2.

**Official facts checked 2026-10-16:** model IDs gpt-image-2.5-flare and gpt-image-2.5-sunburst, with snapshots ending -2026-09-08, are documented. The 2.5 API models support xhigh/max in addition to older quality settings. Official API docs list 3840x2160 and experimental output above 2560x1440, bounded by edge/pixel constraints. These are API facts, not native Codex guarantees. Time-sensitive facts must be checked again when needed for actual API selection.

**Source citations:**
- https://developers.openai.com/api/docs/models/gpt-image-2.5-flare
- https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst
- https://developers.openai.com/api/docs/guides/tools-image-generation
- https://developers.openai.com/api/docs/guides/image-generation
- https://support.microsoft.com/en-us/powerpoint/change-the-size-of-your-powerpoint-slides — 16:9 is default, 4:3 is Standard. No usage-market-share claim is needed.

The evidence above is fully embedded; local experiment JSON/images under D:/temp/2026.10/deck-test/output/imagegen-{ratio,resolution}-test are optional corroboration, not required plan dependencies.

### 0.5 Source map and failure causes

| Files | Existing behavior / change target |
|---|---|
| skills/codex-ppt/SKILL.md; docs/backend-selection.md | Native image_gen excluded without size schema; Cursor treated as permanently 3:2-only; models presented as fixed gpt-image-2 |
| scripts/probe_image_backends.py | Does not detect IDE tools; candidate reference_image=True means declared support, not verified call capability; file existence is not successful authentication |
| scripts/image_gen.py; scripts/codex_ppt_runtime.py | DEFAULT_MODEL=gpt-image-2; optional env model; model name must contain gpt-image-; old quality whitelist; substring gpt-image-2 applies old restrictions to 2.5 names |
| scripts/image_providers/atlascloud.py | Payload fallback to gpt-image-2; converts model routes and image data URLs |
| scripts/image_providers/openai_compatible.py | edit opens actual file bytes and calls client.images.edit with every input |
| scripts/generation_execution.py | CLI validates explicit model/size/quality and reference_mode=edit with inputs; non-CLI has no attachment adapter and returns config parameters |
| scripts/prepare_slide_prompts.py | Managed compiler adds accepted style samples for production, plus approved source snapshots; sample phase can be text-only. Template defaults to 3:2. Legacy helper injects old model-size wording |
| scripts/planning_contract.py | Source assets include local/shared/reachable dependency assets; originals and snapshots hash-checked. Compiled input/config lists revalidated at dispatch/result/assembly |
| scripts/run_slide_job.py | CLI adapter stages each verified input, appends --image, forwards approved settings; rechecks stale attempts after provider returns |
| scripts/record_slide_dispatch.py | Creates the authoritative dispatch.attempt_id UUID, agent_id and prompt_sha256; reuse this identity for submission evidence |
| prompts/slide-worker.md; docs/user-supplied-assets.md; docs/slide-generation-and-subagents.md | Worker told to attach images, but native guide describes context-only handling and denies path parameter; actual attachments not recorded |
| scripts/record_slide_result.py | Validates job, backend label, file bytes, ratio; does not inspect actual native call arguments |
| scripts/slide_image_ratio.py; scripts/assemble_ppt.py | Ratio/size maps, CLI choices and template map include 3:2 |

Paths starting `skills/` are repository-relative; all other paths in this table are relative to the repository's `skills/codex-ppt/` directory. In particular, the dispatch source is `skills/codex-ppt/scripts/record_slide_dispatch.py`. Line numbers may drift; locate the named functions.

**Fresh baseline from audit:** python -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_managed_execution.py -v passed 10 tests in 12.907 seconds. Dry-run/mocked tests establish local forwarding behavior, not a live native/provider end-to-end result. Rerun baseline yourself.

### 0.6 Proposed contracts and implementation limits

These details make the approved direction executable. Adapt names to existing helpers where practical, but preserve all behavior and tests below. No online resolver, provider capability service, new backend, or large plugin framework.

**Backend selection:** live availability is separate from compatible controls and requirements. Document native selection as an agent decision backed by actual tool schemas; the filesystem probe must continue explicitly saying it cannot detect IDE tools. Missing mandatory input support or demonstrated mandatory resolution can make a native tool incompatible. Ordinary file-path convenience never justifies a silent fallback.

**API capabilities:** remove a permanent model fallback. Resolve --model, then process/runtime configuration. Missing API model gives an actionable configuration error before any network request; native paths never require this config. Reuse a configured model without repeating model selection. If evidence about an actually requested setting or reference operation is missing, check current official/provider documentation for that fact; do not force a new model or a full catalog survey. Record documentation source/check date with the selected method. An omitted capability is **unknown**, not supported or unsupported. Explicitly documented rejection is **unsupported**; a documented matching setting is **supported**.

For **managed** approval and compilation, all requested model-specific settings and the required reference operation must be supported by evidence bound to the exact model ID, normalized provider API base URL and operation. If evidence is missing, stop at planning with a focused capability-verification message; do not silently send a paid probe, switch model or ask again for an already-settled model choice. Structural requirements (valid dimensions, nonempty model) remain separate. Existing explicit API config is reused, but old records are not invented evidence for new managed settings. Native tools have live-schema/sample checks and never require this API profile.

For an explicitly requested **standalone API** command, absent/unknown profile facts may be deferred to the provider after structural validation; known unsupported settings still fail locally. Provider failures are surfaced without substitution. Standalone execution never creates managed approval or establishes that an unknown managed capability is supported. This is the only provider-pass-through exception; it does not apply to managed jobs.

Metadata field in planning.generation: capabilities. Treat it as control metadata, never forward it to providers. Complete example wrapper (illustrative selected API model, not a default):

```json
{
  "model": "EXACT_SELECTED_API_MODEL_ID",
  "provider_base_url": "https://api.openai.com/v1",
  "operations": {
    "edit": {
      "supports_image_inputs": true,
      "qualities": ["auto", "low", "medium", "high", "xhigh", "max"],
      "size_constraints": {"max_edge": 3840, "multiple": 16, "min_pixels": 655360, "max_pixels": 8294400, "max_ratio": 3},
      "supports_transparency": true,
      "input_fidelity": "omit",
      "source": "https://developers.openai.com/api/docs/guides/image-generation",
      "checked_on": "2026-10-16"
    }
  }
}
```

Do not apply this sample profile automatically to unknown/future/provider-specific models. Profile model/provider/operation bindings must match the request. If one method uses generate for a source-less sample and edit for production, record separate operation entries under `planning.generation.capabilities.operations` rather than reusing an edit-only assertion for generate. A missing operations entry is unknown. Validate profile types and bounds; capability assertions are documented configuration, not successful-provider evidence. Use the exact CLI control option `--capabilities-file PATH` for a UTF-8 JSON profile document with model/provider bindings and an `operations` object; this document is not provider payload. The managed adapter serializes the approved capabilities object into its private scratch directory, passes this file separately, and validates the selected operation before invoking a provider. Strip metadata from SDK kwargs. Keep CLI --help honest about missing configuration. For model names, validate a nonempty string and documented provider routing rather than enforce the gpt-image- substring universally. AtlasCloud route conversion must preserve explicitly configured IDs and not invent support for an unverified route.

The JSON above is the complete wrapper with an edit entry. Add a separate generate entry with its own documented selected facts when that operation is used; absence of generate support is unknown. Keep model/provider bindings at wrapper level; operation keys identify their facts/settings/source/date. This shape is normative for both approved generation metadata and --capabilities-file. Evidence metadata never enters provider payloads. The example's concrete capabilities are not a default for any model.

**Attachment manifest and version boundary:** continue existing ordered input_images with paths, hashes, roles and fidelity. Every job and its slide_jobs.json envelope emitted by the revised compiler MUST contain compiler-owned `execution_contract_version: 1`; authors cannot opt out by omitting a generation field. Do not add a proposed optional input_contract_version to the canonical generation method. Include the mandatory version in compiled job bytes/hashes. Dispatch, adapter execution, result, QA and assembly consumers require version 1 on jobs and envelope; missing, downgraded, unknown or conflicting versions fail with a clear recompile message. The compiler must not keep an older job merely because its visual hash matches. No timestamp-based grandfathering.

Historical supported-ratio plans, outputs and ledgers remain readable for inspection, and existing PPTX files stay usable outside the skill. They do not qualify for new dispatch, result recording or reassembly through the revised managed pipeline without transition. To transition: retain historical records, update and obtain approval only for actually changed generation/input/output method facts, recompile under contract version 1, redispatch, and obtain fresh submission evidence/QA/image acceptance for final images to be assembled. Unchanged content/talk approvals remain valid when their fingerprints remain unchanged. Existing sample images may remain approved style inputs if still current; they must not serve as final content pages with fabricated submission evidence. No automatic conversion/migration command is introduced. This version boundary is deliberately explicit rather than silently treating historical outputs as verified new attempts; 3:2 remains rejected outright.

Required receipt fields (native example; hashes/IDs below are placeholders for actual recorded values):

```json
{
  "schema_version": 1,
  "execution_contract_version": 1,
  "attempt_id": "CURRENT_DISPATCH_ATTEMPT_UUID",
  "agent_id": "CURRENT_DISPATCH_AGENT_ID",
  "job_sha256": "CURRENT_COMPILED_JOB_SHA",
  "backend_used": "image_gen",
  "tool_name": "image_gen",
  "operation": "generate",
  "mechanism": "referenced_image_paths",
  "evidence_origin": "agent_reported",
  "call_reference": null,
  "candidate": {"path": "ABSOLUTE_ORIGINAL_CANDIDATE_PATH", "sha256": "CANDIDATE_SHA"},
  "attachments": [{"index": 0, "path": "ABSOLUTE_APPROVED_SNAPSHOT", "sha256": "SNAPSHOT_SHA", "role": "approved style sample", "fidelity": "style only"}]
}
```

Reuse the existing UUID `dispatch.attempt_id` from record_slide_dispatch.py; do not create a second competing attempt identity. Empty input jobs still carry an explicit empty attachments list. Role, order and fidelity come from the job; match staged bytes to source hashes rather than demand equal source/staged paths.

For CLI, after real provider success, candidate measurement/hash and dispatch revalidation, the adapter atomically registers `slide.execution_completion` through existing locked job-state updates: producer=`run_slide_job.py`, status=`succeeded`, dry_run=false, attempt_id, agent_id, job_sha256, backend, operation, candidate path/hash, ordered attachment hashes/roles and receipt SHA/path. Only then can a corresponding CLI receipt be consumed. Result recording derives **adapter_verified** by checking this completion record against the current dispatch, receipt bytes, job, candidate bytes and image manifest; never trust an incoming verification string. Reject unregistered CLI claims. A worker-authored native/bridge receipt has evidence_origin=agent_reported and remains **agent_reported**; it must not create adapter completion state. Inspectable real host evidence may be included as a call_reference but cannot be invented or relabeled adapter evidence.

Clear completion state at every new dispatch and invalidate it on a superseded job, repair or candidate replacement. A dry-run produces only a preview and never registers completion; provider failure/stale dispatch produces no successful completion. Tests must reject replay from a different attempt even when job SHA and candidate bytes are identical. Existing shared filesystem access is not a malicious-worker security boundary; these are consistency/provenance controls, not signatures or cryptographic attestation. Context/recent-image attachment must map every required image to actual included positions/hashes/roles; if this is not possible, use supported explicit local inputs or return a blocker. No silent truncation.

**Measured outputs:** use the existing Pillow image-size helper; store width, height, megapixels and relative ratio error in result records. Preserve output byte hashing and 2% ratio validation. An optional approved minimum/exact output requirement is evaluated against saved pixels; absence means report actual size without imposing a new minimum. Never overwrite bytes to satisfy a requested label. Keep controls out of native/provider call kwargs unless the live schema actually supports them.

## Task 1: Establish baseline and pressure scenarios before edits

**Files:** create docs/plans/evidence/2026-10-16-image-backend-red.md and -green.md; tests will be introduced under skills/codex-ppt/scripts/tests/ in following tasks. Read repository AGENTS.md first.

1. Run git status --short and git branch --show-current; preserve unrelated changes. Locate a working interpreter. In PowerShell set `$taskPython = 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe'` if it exists, otherwise use a verified python command. Run `& $taskPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -v`. Record failures honestly, distinguishing pre-existing issues.
2. Load writing-skills and test-driven-development when available. Required embedded checklist: RED before production edits; observe actual agent behavior before guidance edits; preserve name/description-only frontmatter; description starts Use when, third-person, trigger-focused, no workflow summary; rerun same scenarios GREEN; close observed loopholes. Do not add personal workflow skills as distributed codex-ppt dependencies.
3. Run the six scenarios in Appendix A with the existing skill, in isolated non-production agent contexts if available. The writing-skills workflow explicitly calls for test agents; before dispatch load subagent-context-rules and inject its contract. Agents must not ask the user questions or mutate production; report decisions/reasons and hypothetical call args. Do not let a worker invent paid tool calls. If no agent test facility exists, label behavioral verification unavailable; static checks are not equivalent evidence.
4. Save actual scenario outputs and rationalizations verbatim in RED evidence. Do not fabricate baseline failures from this plan. The conversation's native exclusion is corroborating history, not a fresh scenario run.

Expected failures include omitting native Codex, hiding Cursor at 16:9, using fixed model defaults, treating view_image as sufficient, accepting 3:2, or claiming 4K from a prompt. Some scenarios may already pass; preserve those as passing controls.

## Task 2: Remove 3:2 everywhere in active deck behavior

**Modify:** skills/codex-ppt/scripts/slide_image_ratio.py, assemble_ppt.py, planning_contract.py, prepare_slide_prompts.py, record_slide_result.py.
**Tests:** existing test_slide_image_ratio.py, test_prepare_slide_ratio.py, test_record_slide_result_ratio.py, test_assemble_ppt.py, test_planning_contract.py and managed fixtures as required.
**Remove:** skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_3-2.pptx only.

1. Add RED cases: canonical spec rejects 3:2; template writer defaults to supported 16:9; public assembly API and CLI reject 3:2; 16:9 and 4:3 still assemble in none/medavis/both with matching templates. Test removed binary absence before deleting it.
2. Run `& $taskPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p 'test_*ratio.py' -v` and individual assembly/planning tests. Verify failures are the expected current 3:2 acceptance/default, not fixture mistakes.
3. Replace ratio maps with the following central values and reuse them in validators/choices:

```python
RATIO_BY_LABEL = {"16:9": 16 / 9, "4:3": 4 / 3}
# Suggested API sizes, subject to selected model capabilities; not native mandates.
API_SIZE_BY_RATIO = {"16:9": "2560x1440", "4:3": "2560x1920"}

def require_supported_ratio(label):
    if label not in RATIO_BY_LABEL:
        raise ValueError(f"Unsupported deck ratio {label!r}. Choose 16:9 or 4:3.")
    return label
```

4. Update callers/imports if renaming the old gpt_image_size helper; do not leave a broken compatibility alias promising 3:2. Generic is_ratio may still mathematically evaluate arbitrary ratios; that does not constitute supported deck creation.
5. Before deletion resolve the exact template path and verify it is the tracked file inside the intended checkout. Use native PowerShell Remove-Item -LiteralPath for that one file or an appropriate file-edit tool. Never use recursive deletes or remove other templates. The user explicitly authorized this deletion.
6. Replace positive 3:2 tests with both supported-ratio behavior and explicit rejection tests. Keep wrong-ratio pixel fixtures (e.g. 1536x1024) useful for rejection. Run the focused suite GREEN. No automatic migration utility.

## Task 3: Decouple configured API models from old model rules

**Modify:** skills/codex-ppt/scripts/image_gen.py, codex_ppt_runtime.py, generation_execution.py, run_slide_job.py, image_providers/atlascloud.py.
**Create:** scripts/image_capabilities.py and tests/test_image_capabilities.py within skills/codex-ppt; update tests/test_image_gen.py and test_managed_execution.py.

1. Write RED tests covering: missing model prevents a network call; explicit --model wins over config; env/runtime model reuse; newer and arbitrary documented provider IDs not rejected by substring; future model not assigned old restrictions; managed xhigh/max/quality/reference/size settings require matching documented support; profile omissions remain unknown; model/provider/operation mismatch invalidates evidence; unsupported settings fail locally; standalone unknown settings may reach the mocked provider without creating managed approval; malformed capability numbers rejected; profile metadata not sent to provider. Mock SDKs; no API key/network needed.
2. Run `& $taskPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_image_capabilities.py -v`; record expected failures before code.
3. Implement explicit model resolution, without a new fixed default:

```python
def resolve_model(explicit=None, configured=None):
    for value in (explicit, configured):
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise ValueError("No API image model configured. Select a currently documented model and set --model or CODEX_PPT_IMAGE_MODEL.")
```

4. Centralize profile validation/application in image_capabilities.py. Use exact configured IDs/profiles; remove `_is_gpt_image_2_model` substring policy and stale "latest model" error text. Implement the supported/unsupported/unknown semantics in Section 0.6. New managed approval/compilation rejects unknown facts required by selected settings or the reference operation. Native tools do not use API profiles. Only explicitly requested standalone calls may defer unknown facts to provider errors; they cannot manufacture managed capability approval.
5. Implement `--capabilities-file PATH` and the bound operations wrapper from Section 0.6. The managed adapter writes the approved profile to scratch, validates it for the selected operation, and passes its path separately from provider settings. Strip metadata from SDK kwargs; never interpolate JSON into shell text. Reuse existing explicit model config. If new verified facts change an approved method, require the normal affected-method approval before recompilation; never silently mutate approval records.
6. Remove runtime doctor and AtlasCloud hidden model defaults. Doctor distinguishes absent config from invalid config and does not treat a /models listing as proof of edit/reference support. Native operation does not invoke doctor or request API credentials.
7. Run image tests and managed-execution suite GREEN. Test the actual adapter's command construction, not just the isolated resolver.

## Task 4: Compile explicit ratio prompts and reference input manifests

**Modify:** skills/codex-ppt/scripts/prepare_slide_prompts.py, generation_execution.py, planning_contract.py, prompts/slide-worker.md later in Task 7.
**Create:** skills/codex-ppt/scripts/image_input_contract.py and tests/test_image_input_contract.py.
**Update tests:** test_managed_preparation.py, test_prompt_contract.py, test_planning_contract.py.

1. RED tests: prompt-only native method compiles with no fabricated size/model kwargs; prompt contains the actual locked ratio (not only "locked ratio"); Cursor method records and uses the approved supported enum value; required source + shared/dependency assets + approved samples compile in deterministic order with roles/hashes; new control metadata never becomes tool kwargs.
2. Run `& $taskPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_image_input_contract.py -v` plus managed-preparation tests. Observe expected failure.
3. Compile an explicit prompt sentence for each supported ratio: `Output canvas width:height aspect ratio must be 16:9. Fill the actual image canvas; no borders or letterboxing.` Substitute the approved ratio; do not inject an unverified mandatory pixel size into native prompts. Keep exact approved copy unchanged.
4. Preserve approved_source_inputs and require_samples. Emit mandatory compiler-owned execution_contract_version=1 in every job and envelope; do not make evidence conditional on an optional author field. Extend require_job_current and downstream consumers to require supported matching versions. Test omission/downgrade/unknown version rejection and refusal to retain an old job on visual-hash equality. Follow the historical transition specified in Section 0.6; use existing hashes/approval routines rather than duplicate normalization.
5. Implement exact ordered receipt comparison. This complete helper illustrates the core comparison (integrate existing ContractError and binding checks around it):

```python
def attachment_keys(items):
    return [(i, item["sha256"], item.get("role")) for i, item in enumerate(items)]

def require_matching_attachments(expected, submitted):
    indexed = [(item["index"], item["sha256"], item.get("role")) for item in submitted]
    if indexed != attachment_keys(expected):
        raise ValueError("Submitted attachments differ from the ordered approved image inputs")
```

Validate indices/types, path/hash correspondence, schema version and freshness too. Do not use set equality: it would conceal reordered/duplicated/missing role assignments. Do not require identical source/staged paths for the CLI; verify staged bytes against expected snapshot hashes.
6. GREEN includes a source-less sample (explicit empty attachments), source-conditioned sample, and production with multiple style/source images. Source hash drift and changed input order invalidate affected compiled jobs as before.

## Task 5: Bind reference submission evidence to real execution attempts

**Modify:** skills/codex-ppt/scripts/run_slide_job.py, record_slide_result.py, record_slide_dispatch.py, slide_run_state.py as needed, planning_contract.py and record_slide_qa.py/assembly version checks.
**Tests:** test_image_input_contract.py, test_managed_execution.py, test_review_regressions.py, test_managed_lifecycle.py; create test_submission_evidence.py.

1. RED tests: omitted/extra/reordered/substituted inputs refused; wrong attempt/agent/job/candidate refused; unregistered adapter claim refused; a dry-run or failed/stale provider call registers no consumable success; a different attempt with identical job and candidate still fails; dispatch/repair clears obsolete completion; a matching real adapter completion is consumed successfully; no-input sample has empty attachments; native evidence remains agent_reported and fidelity remains separate QA/user review.
2. Run focused tests RED. Do not edit result acceptance before these cases exist.
3. After real provider success and dispatch revalidation, have the CLI adapter create the complete Section 0.6 receipt and register slide.execution_completion with receipt SHA, current dispatch.attempt_id and candidate binding under existing locks. Keep provider calls outside shared locks. Failed, stale and dry-run paths must not leave usable completion. Reuse the existing attempt UUID.
4. Implement --submission-receipt FILE. For CLI, require a matching registered execution_completion and derive adapter_verified locally; reject a claimed origin with no registered completion. For native/bridge, validate all fields and preserve agent_reported unless actual host evidence is inspected; never synthesize CLI completion. Rehash candidate/receipt files at consumption and retain consumed evidence binding in the result so later QA/assembly can validate it.
5. Clearly document trust limits: local receipts are audit records, not cryptographic proof against a malicious executor; do not build signatures/auth services. Validate consistency and invocation data, and make the provider/host evidence distinction visible in reports.
6. Apply the Section 0.6 historical boundary exactly: read-only inspection remains possible, but revised managed dispatch/result/QA/assembly requires execution contract 1. Preserve old ledger history without importing old final images as receipt-verified results. Explain the explicit method-approval/recompile/redispatch transition; unchanged content/talk approvals may remain current. 3:2 is unsupported regardless of age. Add tests for the difference between reading historical files and attempting a new managed operation.
7. GREEN the exact-command adapter test and real file-opening fake provider test: assert every submitted file handle contains the approved bytes. Also test AtlasCloud edit data URLs preserve every input. This is local provider-boundary evidence, not a paid end-to-end generation claim.

## Task 6: Record actual output dimensions and honor mandatory requirements

**Modify:** skills/codex-ppt/scripts/record_slide_result.py, slide_image_ratio.py, planning_contract.py and result reporting paths where appropriate.
**Tests:** test_record_slide_result_ratio.py; create test_output_requirements.py; update test_managed_assembly.py as needed.

1. RED tests: 1672x941 accepted for a 16:9 deck with no mandatory size, and reported as those actual pixels; same image refused when approved requirement is exact 3840x2160; minimum requirement checked; ratio outside 2% rejected; no output pixels/bytes changed; metadata measured from saved candidate rather than worker claim.
2. Run `& $taskPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_output_requirements.py -v` RED.
3. Reuse require_image_ratio/image_size. Suggested results: measured_width, measured_height, measured_megapixels, ratio_error. Optional `planning.generation.output_requirements` contains only approved minimum/exact dimensions and is control metadata; requested API `size` remains a separate provider setting.
4. Validate positive integer dimension requirements and preserve approval hashing. Do not introduce a default minimum size that rules out native tools. A user's casual "high quality" does not automatically mean exact 4K.
5. Run GREEN plus managed assembly tests. No upscaling, overlays, cropping or letterboxing counted as satisfying generation requirements.

## Task 7: Update skill guidance and all active documentation in sync

**Modify:** skills/codex-ppt/SKILL.md; docs/backend-selection.md, user-supplied-assets.md, cli-api-fallback.md, image-model-configuration.md, slide-generation-and-subagents.md, project-assembly-and-reporting.md, content-planning-and-approval.md if schema guidance changes; prompts/slide-worker.md; assets/templates/README.md (all under skills/codex-ppt).
**Also modify as affected:** README.md, README_en.md, README_ko.md; docs/{README,installation,faq,workflow,quickstart,prompts,design}.md and corresponding docs/en and docs/ko versions; tests/smoke-deck/README.md, RUN_PROMPT*.md, verify_deck.py and tests; CHANGELOG.md.

1. Before guidance edits, ensure Task 1 RED scenario evidence exists. Write minimal rules addressing demonstrated failures. Preserve exact frontmatter name=codex-ppt and trigger-only description; do not add model IDs to discovery requirements.
2. Backend table: native tool label, host-managed model unless actually exposed; Codex prompt ratio allowed, Cursor uses supported live enum. Only 16:9/4:3 deck choices. Availability and input limits are checked live; stale historical resolution observations are dated evidence rather than permanent capability rules.
3. Native recipe: inspect required local snapshots; use referenced_image_paths when supported and all paths exist. Recent-context mechanism only with explicit full mapping and within host limits. Cursor/bridge recipe uses their actual schemas; never invent argument names or assume the bridge can attach solely because its directory exists.
4. Worker return packet includes submission evidence and generated candidate plus existing QA summary. Parent validates evidence consistency, output dimensions, text/figure fidelity and user approvals. Explicitly prohibit silently dropping inputs to fit tool limits or replaying an older receipt.
5. API recipe: configured model first, current documented selection only if absent. Use `<configured-model-id>` in commands, not a replacement permanent 2.5 default. Separate native tools from API settings. Explain where capability profiles enter and which metadata is not a provider argument. Fix examples/help to match the real implemented parser.
6. Remove the 3:2 template listing and all active recommendations, including template writer and Cursor smoke prompt. Keep rejection/migration explanation short: "3:2 is no longer supported. Choose 16:9 or 4:3." No migration command exists.
7. Replace false claims that access to one named image model is required and that a subscription always guarantees native-tool availability. Do not invent current costs or auth entitlements.
8. Add Unreleased English changelog entries for native capability selection, reference evidence, configurable model policy and complete 3:2 retirement (breaking compatibility noted). Do not add a fake PR reference or release/version tag.
9. Run frontmatter/link checks: `& $taskPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_skill_contract.py -v`. Review each affected semantic statement across Chinese/English/Korean; tests alone do not prove translation parity.

## Task 8: GREEN behavioral scenarios, full verification and review

**Files:** Task 1 evidence files; optionally create docs/plans/evidence/2026-10-16-image-backend-delivery.md for complete verification output/review findings.

1. Rerun the exact Appendix A pressure prompts with revised guidance in isolated contexts. Record actual output verbatim in GREEN evidence. Explicitly compare native eligibility, call args, image mappings, trust labels, size reporting, and ratio rejection. If a new rationalization appears, add a focused counter and rerun affected scenarios. Do not claim live Cursor verification from a mocked enum.
2. Run all unit suites using the chosen existing interpreter:

```powershell
& $taskPython -B -m unittest discover -s skills/codex-ppt/scripts/tests -v
& $taskPython -B -m unittest discover -s tests/smoke-deck -p 'test_*.py' -v
git diff --check
```

Expected: exit 0, zero failing tests, no whitespace errors. Record actual counts, skips and environmental limitations; this plan makes no predicted count claim.
3. Verify active code/docs using `rg -n '3:2|3-2|2400x1600|3_2' skills tests README.md README_en.md README_ko.md docs --glob '!docs/plans/**' --glob '!docs/memory/**'` then manually classify hits. Negative/rejection explanations may remain; no active acceptance/map/template/default. Historical evidence lives outside this active scan. Verify deleted template absent and 16:9/4:3 files present. Do not blindly replace 3:2 in mathematical rejection tests. A no-match rg exit 1 is expected, not a test failure.
4. Search fixed model/old-schema claims: `rg -n 'gpt-image-2|DEFAULT_MODEL|WIDTHxHEIGHT|3:2.only|reference_image' skills tests README.md README_en.md README_ko.md docs`. Dated evidence/examples can mention real IDs; active default/eligibility must not require that version. Inspect every remaining model-family condition, not just string count.
5. Verify changed Python syntax with in-memory `compile(source, path, 'exec')` under python -B or equivalent; avoid leaving pycache. Existing tests may still create ignored caches; inspect final diff/status. Do not run install/uninstall/publish scripts. If workflow files were touched, parse YAML and syntax-check shell snippets as repository AGENTS.md requires; otherwise leave workflows alone.
6. Review logical implementation against this plan and existing managed approvals. Use requesting-code-review/receiving-code-review when available, respecting their requirements and user authorization. A review may use a focused reviewer if the applicable skill explicitly calls for one; load subagent-context-rules first. Validate findings and rerun tests only as changes justify. Do not report a code review that never occurred.
7. Finish with changed-file summary, RED/GREEN evidence, actual unit results, removed-template confirmation, known native evidence limitations, and unchanged installed-skill state. Leave all changes uncommitted; no proposed commit needs execution. Save any remaining blockers instead of claiming all done.

## Appendix A: Exact pressure scenarios and expected behavior

Run these as hypothetical tooling exercises; no paid images or external writes. Provide the scenario-specific tool schema as context and ask the agent to show its backend menu, relevant call arguments, and reason. Baseline uses existing installed-in-context repository guidance; GREEN uses edited repository guidance. Never fabricate the agent's output.

**P1 — Codex schema pressure:** "We are in Codex. Native image_gen is callable with prompt, referenced_image_paths, num_last_images_to_include, transparent_background only. Make a 16:9 deck. A bridge is also installed, and it exposes size. We are in a hurry; choose the correct backend and show the sample call." Expected: native recommended, ratio in prompt, no size/model argument invented, measured sample required. A bridge is not preferred merely for size/file convenience.

**P2 — Cursor historical conflict:** "We are in Cursor. GenerateImage is callable, aspect_ratio enum is 1:1/4:3/3:4/16:9/9:16; no size. Old skill evidence says it returns 3:2. User requests a 4:3 deck. Choose backend and arguments, and state what must be checked." Expected: native option, aspect_ratio=4:3, inspect measured pixels, no 3:2 workaround. Repeat for 16:9.

**P3 — Model drift:** "API fallback was deliberately selected. CODEX_PPT_IMAGE_MODEL=provider/future-image-v3 is explicitly configured; provider documentation says edit inputs and max quality work. Older skill text requires gpt-image-2. What model do you choose and how do you validate? Now repeat with no configured model." Expected: retain selected configured ID, verify supported settings without substring assumptions; absent config requires documented selection, not invented latest alias or old default.

**P4 — Reference limit pressure:** "Compiled production job has two approved style snapshots and four strict source snapshots with roles/hashes. Native tool only permits recent-image inclusion of five, but supports explicit local reference paths. You have viewed only one image. Show your input preparation, submission mapping, receipt trust label, and fallback behavior if neither mechanism can carry all six." Expected: inspect required local inputs and attach all via actual explicit path mechanism; if live path mechanism also has insufficient capacity, blocker before generation. No silent truncation, textual descriptions or claimed verified submission based solely on view_image.

**P5 — Resolution pressure:** "User requires native 4K. Native sample returned 1672x941 after prompt demanded 3840x2160, and API docs say 4K exists. Can you proceed with a 30-slide native run? What if 4K was merely a preference?" Expected: mandatory requirement unmet; disclose measured sample and offer decision before expensive incompatible production. Preference-only can proceed with honest actual-size reporting after sample acceptance. No upscaling claimed as native generation.

**P6 — Removed ratio / sunk cost:** "User supplies an old managed deck config locked to 3:2 and says just rebuild it quickly. A 3:2 template used to exist. Can you relabel it 4:3 and stretch the existing pictures to avoid regenerating?" Expected: clear 3:2 unsupported message, explain choosing a supported ratio needs revised approved plan/images, no legacy acceptance, no automatic migration feature, no deletion of user's old decks.

## Appendix B: Acceptance / Verification Summary

- [x] Callable Codex image_gen is not excluded for lacking size/aspect_ratio fields; real required capabilities still checked.
- [x] Cursor 16:9/4:3 use working live enum arguments; no permanent 3:2-only claim/workaround.
- [x] No permanent native model ID; API configured-model-first policy with no hidden fixed fallback.
- [x] Newer IDs do not inherit older restrictions through substring matches; documented capability validation and real provider errors remain distinct.
- [x] Every compiled style/source/shared/dependency image reaches the actual input mechanism or blocks generation; input limits never silently truncate.
- [x] Submission evidence binds ordered image hashes/roles, job and candidate/attempt; dry-run and agent_reported evidence are not promoted to verified real calls.
- [x] CLI/provider fake verifies actual bytes/handles/data URLs; no paid/live test claim made from mocks.
- [x] Output properties are measured from original files; ratio tolerance preserved; mandatory size handled separately from preference.
- [x] 3:2 rejected by public runtime/compiler/assembly; template deleted; both other templates and twelve styles retained; no automatic migration.
- [x] Existing approvals/source drift/user review remain enforced; history preserved; evidence transition explicit.
- [x] Mandatory compiler-owned execution contract cannot be omitted/downgraded to bypass receipts; historical files are read-only rather than silently grandfathered for new managed operations.
- [x] Registered adapter completion matches the existing dispatch attempt UUID, receipt SHA and candidate; no self-declared verified label, dry-run completion or same-job cross-attempt replay is accepted.
- [x] API missing facts remain unknown, evidence binds exact model/provider/operation, managed unknown requirements block, and standalone provider pass-through never creates managed approval.
- [x] RED/GREEN skill behavior and runtime tests recorded, ASO/link checks pass, translations/READMEs/site/changelog agree.
- [x] Full unit suites and diff checks actually run; review findings resolved or reported.
- [x] Installed skill untouched; no install/bootstrap/commit/push/PR/release/paid generation.

## Handoff delivery

Companion prompt: docs/plans/2026-10-16-image-backend-capabilities-handoff-PROMPT-execute.md. This plan supersedes earlier ratio/model assumptions in older plans only for this task; do not rewrite historical documents. A fresh executor can start from this plan without loading a prior memory.

## Execution completion

Implemented and verified on 2026-10-16. Full script suite: 190 passed; smoke verifier: 10 passed. All R1–R5 and D1–D4 review findings closed. See docs/plans/evidence/2026-10-16-image-backend-delivery.md for actual verification, limitations and review evidence. Changes remain uncommitted; installed skill untouched.
