# Memory: Image Backend Capabilities and Reference Handoff

**Generated**: 2026-10-16 00:45 Asia/Shanghai
**Last updated**: 2026-10-16 10:10 Asia/Shanghai
**Project**: D:\git\codex-ppt-skill
**Focus**: Confirmed requirements and audit evidence for model-independent native backend selection and reliable image-reference handoff.

## Device mode

- **Mode**: mobile
- **Switched**: 2026-10-16 01:30

## Goal & Scope

Carefully fix backend selection, model assumptions, native ratio handling, and reference-image handoff in the source repository. The installed skill under C:\Users\raymond.shen\.codex\skills\codex-ppt is not the edit target. Scope includes runtime code, regression tests, instructions, affected documentation/language versions, changelog, review, and verification. The user subsequently authorized commit, push and pull-request creation on 2026-10-16.

The user explicitly invoked clarify-requirements, selected the complete implementation scope, added Cursor ratio evidence, and confirmed the complete understanding summary. They explicitly requested this memory in the codex-ppt repository. The complete design and cold handoff plan were approved. The user then requested execution through completion until a substantive user decision is needed.

## Key Decisions

1. **Repository**: D:\git\codex-ppt-skill. The user's earlier mention of an SQ5 curated tool collection was a mistake, explicitly corrected to this repository.
2. **Full scope**: Fix all three audited issues plus Cursor native ratio handling across instructions, runtime, tests, affected documentation and changelog. Documentation-only fixes were offered and not selected because runtime defaults and attachment gaps would remain.
3. **Model independence**: Native backend selection must not permanently name or require a particular GPT Image model. The host manages its native model. API executions still need an explicit configurable model recorded for each deck.
4. **Codex native preference**: Offer/recommend callable native image_gen without requiring dedicated size or aspect_ratio parameters. Prompt-based ratio requests are allowed, followed by measured output validation. Missing parameters alone must not force bridge/API fallback.
5. **Resolution honesty**: Distinguish requested resolution from actual observed dimensions; do not promise exact resolution or native 4K support based on Image API documentation.
6. **Cursor correction**: Remove obsolete 3:2-only behavior and use live GenerateImage aspect_ratio enums. Treat user-provided 2026-10-16 results as dated evidence. The user subsequently explicitly removed 3:2 support and its bundled template; supported deck ratios are 16:9 and 4:3.
7. **References**: Strengthen handoff so required source and style images reach the actual backend input mechanism, with explicit unsupported-input handling and verifiable attachment evidence where possible.
8. **Change boundaries**: Review and verify; no commit, push, merge, installed-skill update, or PR publication is currently authorized.
9. **Memory**: User explicitly selected this repository for session memory. Keep separate from prior memories about Medavis templates and the predictable-generation work.
10. **Design approach approved**: Capability-based backend selection, rather than minimal targeted patches or automatic runtime model discovery.
11. **API model selection approved**: Reuse the explicitly configured model. If none exists, consult current official/provider documentation, recommend a model, and obtain the user's choice. Record the selected model per deck. Do not reselect automatically for every deck when configuration already exists.
12. **Complete removal of 3:2 explicitly requested**: The user's exact instruction was "A, and remove the 3:2 support completely and its template". The explicit removal instruction takes precedence over the option label A, which had proposed retaining legacy support. New supported deck ratios will be 16:9 and 4:3 only. Remove the 3:2 template, runtime/assembly support, menu choices, documentation, and corresponding active tests. Existing 3:2 exported PPTX files remain usable outside the skill; new managed operations require a supported ratio and freshly approved work. No automatic migration feature is included; do not silently relabel/stretch/crop old images. The twelve visual styles are not ratio-specific templates and are not to be removed on this basis.
13. **Reversed: proposed legacy 3:2 compatibility**: Retaining 3:2 support/template for old decks was an assistant recommendation, not the final user choice. User explicitly requested complete removal. This narrows the earlier general compatibility goal; preserve unrelated deck behavior and reject unsupported 3:2 inputs clearly.

## Confirmed Assumptions

- The user wants resilient capability-based behavior, rather than replacing every old model string with another soon-obsolete fixed model string.
- Preserve managed workflow approvals, immutable jobs, source fidelity checks, and output ratio validation.
- Native image tools and API image models are distinct interfaces; API documentation alone cannot establish native model identity or native resolution limits.
- Cursor evidence below was provided by the user from another environment; this session did not independently call Cursor GenerateImage.

## Constraints & Non-Goals

- Repository AGENTS.md: contribution metadata/changelog in English; documentation updates synchronize existing language versions and usage site; user-visible changes get an Unreleased changelog entry; nontrivial publication follows PR flow. A future PR number is only added after one actually exists.
- Native call schemas are authoritative: never invent size/aspect_ratio/model parameters.
- Real output dimensions and fidelity must be inspected. No stretching/cropping/letterboxing to disguise a failed ratio.
- Do not weaken approval gates or silently omit image inputs to make a path work.
- No broad changes to unrelated decks or installed skill files.

## Key Discoveries

### Repository audit

- skills/codex-ppt/docs/backend-selection.md:34 explicitly omits image_gen if its schema cannot express the locked ratio via WIDTHxHEIGHT. Line 42 repeats the size-schema requirement in the Codex preference table. This is the concrete cause of excluding a working native backend in this session.
- SKILL.md:29, worker guidance, smoke prompts and backend documentation contain model/size assumptions that need coordinated review.
- scripts/image_gen.py:31 and scripts/codex_ppt_runtime.py:26 default to gpt-image-2; image_providers/atlascloud.py also has an old fallback.
- image_gen.py:286-287 identifies the family by substring gpt-image-2, which also matches gpt-image-2.5-* and applies old model-specific constraints. ALLOWED_QUALITIES only supports low/medium/high/auto.
- probe_image_backends.py cannot see native IDE tools; the agent must inspect the live tool list. Bridge availability currently means its SKILL.md exists; reference_image=True is declared, not a live attachment capability test. The CLI candidate similarly checks its script's existence rather than successful auth/provider readiness.

### Reference pipeline

- prepare_slide_prompts.py:473-482 compiles sample jobs with source inputs; production jobs add all required approved style samples plus approved_source_inputs.
- planning_contract.py:471-494 collects local/shared assets and reachable dependency assets, resolves approved snapshots, and verifies both original and snapshot hashes.
- planning_contract.py:553-563 revalidates job sample/input/config lists against the current approved contract.
- run_slide_job.py:48-56 stages every compiled image with verified bytes and appends a separate --image argument. Its adapter only executes the bundled CLI backend.
- generation_execution.py enforces explicit CLI reference_mode=edit when images exist and forbids a text-only operation with image inputs. Non-CLI paths merely return an operation and configuration; they have no equivalent executable attachment adapter.
- image_providers/openai_compatible.py edit opens actual image files and passes them to client.images.edit; atlascloud.py edit serializes all images as data URLs.
- prompts/slide-worker.md requires inspecting and attaching every input, but actual native/bridge execution still depends on the agent following those instructions.
- record_slide_result.py checks job currency, backend label, output bytes and ratio. It does not prove that a real native/bridge call attached every declared input or used every claimed parameter.
- docs/user-supplied-assets.md:25-26 describes native reference inclusion via view_image/context and says it is not a filename parameter. This conflicts with this session's live native schema, which exposes referenced_image_paths and num_last_images_to_include.
- Current native schema: prompt; referenced_image_paths; num_last_images_to_include; transparent_background. No size, aspect_ratio, or model selector. Use referenced_image_paths when all target inputs have local paths; use the recent-image count only when appropriate, and do not supply both mechanisms. Inspect local input images before editing.

### Official model facts checked 2026-10-16

- Official current API model IDs include gpt-image-2.5-flare and gpt-image-2.5-sunburst, with dated snapshots ending -2026-09-08. These establish API names, not the internal model behind native image_gen.
- Official guidance describes Sunburst for precise editing and Flare for fast high-quality generation. The 2.5 API models support xhigh/max quality in addition to older quality settings.
- API resolution documentation includes 3840x2160 and experimental status above 2560x1440; it is not a documented native Codex limit.

## Runtime Evidence

### Codex native tests performed in this conversation

All calls used the native image_gen tool with prompt instructions, not API/CLI fallback. One generated image per requested ratio; original PNG header dimensions measured without resizing/cropping. Same simple scene: red ceramic sphere on pale blue studio background, no borders or letterboxing.

| Requested ratio | Measured pixels |
|---|---|
| 1:1 | 1254x1254 |
| 16:9 | 1672x941 |
| 9:16 | 941x1672 |
| 4:3 | 1448x1086 |
| 3:4 | 1086x1448 |
| 3:2 | 1536x1024 |
| 2:3 | 1024x1536 |
| 21:9 | 1916x821 |

All eight ratio errors were below 0.06%. These demonstrate prompt-based ratio capability, not universal reliability.

Explicit resolution prompts at 16:9 returned:

| Requested pixels | Measured pixels |
|---|---|
| 1920x1080 | 1672x941 |
| 2560x1440 | 1672x941 |
| 3840x2160 | 1672x941 |
| 7680x4320 | 1672x940 |

Observed output is approximately 1.57 megapixels; these tests did not establish exact resolution control or a universal upper limit. Earlier assistant statements equating prompt ratio success with prompt resolution support must not be repeated.

### User-provided Cursor verification, 2026-10-16

GenerateImage has optional aspect_ratio with enum 1:1, 4:3, 3:4, 16:9, 9:16, and no separate size parameter. One generation per enum value yielded JPEG dimensions and visual framing as follows:

| Requested ratio | Measured pixels |
|---|---|
| 1:1 | 1024x1024 |
| 4:3 | 1152x864 |
| 3:4 | 864x1152 |
| 16:9 | 1280x720 |
| 9:16 | 720x1280 |

The user inspected all five: full-frame backgrounds, different compositions, no padding/stretching. Older observations that GenerateImage ignored its ratio parameter are outdated. Pass supported requested enum values and measure output; do not preserve a permanent 3:2-only restriction.

### Repository verification

python -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_managed_execution.py -v: all 10 tests passed (12.907 seconds). Includes every-image forwarding, verified staging bytes, text-only calibration, invalid reference operations, stale attempts, and concurrency. These are dry-run/mocked provider tests, not real image-provider end-to-end proof.

Repository git status was clean before this memory was created. The approved implementation is now present as uncommitted source changes; see the delivery evidence referenced below.

## Execution checkpoint

- Approved plan: docs/plans/2026-10-16-image-backend-capabilities-handoff.md. The user selected option one to patch the self-contained plan, then explicitly requested execution through the end until a real decision is needed.
- Implemented native preference, prompt-based ratio handling, configured API model selection, exact model/provider/operation capability evidence, strict ordered input receipts and adapter completion registration, measured output requirements, complete 3:2 retirement, and synchronized guidance/translations/changelog.
- Native/bridge evidence is agent_reported, not independently verified model invocation. CLI adapter evidence requires a successful registered current attempt and matching receipt/candidate bytes.
- Both supported templates and all twelve visual styles retained. Old smoke-run artifacts preserved as historical evidence; installed skill untouched.
- Reviews: original R1–R5 runtime and D1–D4 guidance/test findings all closed after targeted corrections and reviewer follow-up. Review evidence preserves original findings and closure.
- Final verification results and limitations are recorded in docs/plans/evidence/2026-10-16-image-backend-delivery.md.

## Open Risks and Limits

- Native exact resolution control and a universal maximum remain unestablished; inspect actual saved pixels. API documentation does not establish native tool identity or limits.
- Cursor evidence is the user's dated experiment, not a live Cursor call in this implementation run.
- Provider tests use fake SDK/HTTP transports; no paid live-provider tests were run.
- Behavioral RED/GREEN scenarios used the same evaluator exposed to expected results; they are regression evidence, not a blinded independent experiment.
- Required input capacity remains a real backend eligibility condition; never silently truncate.
- Historical managed artifacts require recompilation and fresh execution evidence for new operations; they are not silently grandfathered.

## Current State

- Implementation, review corrections and final verification are complete: 190 script tests and 10 smoke tests passed; separate skill/link checks passed; changed Python syntax and git diff checks passed. Delivery report saved.
- Implementation and review delivery preceded publication. The user subsequently requested commit, push and PR creation; publication status is recorded below. No merge or installed-skill update is requested.
- No substantive user decision blocks source delivery. Any future installation or publication is separate work.

## Next Steps

1. Read the delivery report for final test results and review closure.
2. If further deployment or publication is requested, obtain the applicable explicit authorization; do not infer it from implementation completion.

## References

- D:\git\codex-ppt-skill\AGENTS.md -- repository contribution requirements.
- D:\git\codex-ppt-skill\skills\codex-ppt\docs\backend-selection.md -- native exclusion and preference rules.
- D:\git\codex-ppt-skill\skills\codex-ppt\docs\user-supplied-assets.md -- current reference instructions.
- D:\git\codex-ppt-skill\skills\codex-ppt\scripts\prepare_slide_prompts.py -- compiled inputs.
- D:\git\codex-ppt-skill\skills\codex-ppt\scripts\planning_contract.py -- immutable contract and asset checks.
- D:\git\codex-ppt-skill\skills\codex-ppt\scripts\generation_execution.py -- operation/config validation.
- D:\git\codex-ppt-skill\skills\codex-ppt\scripts\run_slide_job.py -- executable CLI image forwarding.
- D:\git\codex-ppt-skill\skills\codex-ppt\scripts\record_slide_result.py -- result validation and attachment-evidence gap.
- D:\temp\2026.10\deck-test\output\imagegen-ratio-test\results.json -- native ratio measurements, prompts, and image paths.
- D:\temp\2026.10\deck-test\output\imagegen-resolution-test\results.json -- native resolution measurements, prompts, and image paths.
- https://developers.openai.com/api/docs/models/gpt-image-2.5-flare -- official model ID.
- https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst -- official model ID.
- https://developers.openai.com/api/docs/guides/tools-image-generation -- API model selection and quality settings.
- https://developers.openai.com/api/docs/guides/image-generation -- API resolution constraints.

**Confirmed at**: 2026-10-16, user selected A and requested saving memory in codex-ppt.

## Implementation evidence

- docs/plans/evidence/2026-10-16-image-backend-delivery.md
- docs/plans/evidence/2026-10-16-image-backend-red.md
- docs/plans/evidence/2026-10-16-image-backend-green.md
- docs/plans/evidence/2026-10-16-image-backend-runtime-review.md
- docs/plans/evidence/2026-10-16-image-backend-guidance-review.md

## Working directories

- **Active**:
  - `D:\temp\2026.10`
- **Updated**: 2026-10-16 08:09


## Publication authorization and live rendering follow-up

- On 2026-10-16 the user explicitly requested: "Commit and push. by the way, have you create a pull request for it? if not, please also make a pull request."
- Source branch: feature/SQ5GEN-predictable-deck-generation; task ID SQ5GEN-195 follows the existing branch commits. Target: origin/main in shx99717/codex-ppt-skill. No PR existed at the initial check.
- Separately, the user authorized two unattended three-slide rendering tests in D:\temp\2026.10\image-backend-deck-comparison-20261016. Native image_gen and codex-gpt-image bridge both produced 1672x941 outputs; bridge requested 1536x864 and did not report actual model identity. Slides 2/3 in each deck attached their own opening slide as a style-only reference. One native caption repair succeeded.
- Test PPTX files, PDFs and actual PPTX renders were inspected; embedded image bytes, notes and current submission records checked. These are explicitly review-pending preview decks, with no fabricated human image acceptance. Generated deliverables remain outside the source repository.
- The user's concern about three-point layouts was checked against source guidance: there is no bullet quota and the skill explicitly forbids imposing 3–5 bullets. The repeated three-part layout was the agent's sample design choice, not a skill rule.

## Publication result — 2026-10-16

- Implementation commit: 55a973defb41fba41d6d5cc19ad36e2ded3457d0, pushed to origin/feature/SQ5GEN-predictable-deck-generation.
- Pull request: https://github.com/shx99717/codex-ppt-skill/pull/3, open against main. It includes the earlier approval-bound deck-planning commits already on this branch.
- Fresh prepublication verification: 190 script tests passed in 163.325 seconds; 10 smoke tests passed; 30 changed/new Python files parsed; staged whitespace check passed after removing trailing formatting whitespace from new review evidence and one extra EOF blank line. Seven capability tests rerun after that formatting correction passed.
- Follow-up publication commit adds PR #3 references to previously unreferenced Unreleased entries and records this status. No merge, installed-skill update or generated test-deck publication performed.
