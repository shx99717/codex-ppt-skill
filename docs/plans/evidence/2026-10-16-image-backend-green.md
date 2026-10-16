# Image backend capability GREEN behavioral evidence — 2026-10-16

## Scope and exposure limitation

The same evaluator that produced RED read the edited `skills/codex-ppt/SKILL.md`, `docs/backend-selection.md`, `docs/user-supplied-assets.md`, `docs/image-model-configuration.md`, `docs/image-submission-evidence.md`, and `prompts/slide-worker.md` (documentation/prompt paths relative to the skill directory). These are hypothetical responses to the same P1–P6 scenarios, not executed backend calls. The evaluator previously saw Appendix A's expected results adjacent to its prompts and remembers them; this is not a blinded or independent evaluation. No paid calls, image generation, network calls, or tests were performed for this GREEN behavior check. Only this evidence file was written.

## P1 — Actual hypothetical answer

> Recommend A) native `image_gen`, using the host-managed model. Its missing size parameter does not disqualify it for a 16:9 sample. B) the installed `codex-gpt-image` bridge is an alternative if a required capability cannot be met; inspect its actual input support rather than infer that from installation. Native input parameters are known from this scenario, but capacity still needs checking if reference inputs are required. Authentication/cost details beyond those actually known remain unknown.
>
> Lock the specific backend before generation. Proposed sample call after the required approvals, assuming this sample has no required image inputs:
>
> `image_gen({"prompt":"Generate the approved complete raster sample slide with a 16:9 aspect ratio. Preserve the approved visible copy, objects, relationships and style.","transparent_background":false})`
>
> Substitute the actual compiled approved slide content in that prompt; this illustrative call is not a complete production prompt. Do not add `size`, `aspect_ratio`, or `model` to this schema. Measure the original saved image and require relative ratio error ≤2%; obtain acceptance of the actual sample before production. If it fails, resolve the unmet capability rather than claiming the prompt proves compliance.

Assessment: GREEN. The edited selection rule explicitly keeps native recommended without inventing parameters or a native model ID. The installed bridge is not promoted for file/size convenience. Remaining uncertainty is actual sample output; it cannot be resolved by this hypothetical check.

## P2 — Actual hypothetical answer

> Recommend Cursor native `GenerateImage`. Its supplied live enum supports the requested 4:3 ratio, so the ratio argument is `aspect_ratio="4:3"`. Preserve other required parameters exactly as defined by the inspected live schema and use the approved slide prompt. Do not invent a size parameter or send a 3:2 workaround.
>
> For the repeated 16:9 case use `aspect_ratio="16:9"`.
>
> Check actual reference mechanism/capacity if the slide has inputs, then measure original saved pixels for each approved sample. The historical 3:2 observation does not override this live schema. Accept only ≤2% relative ratio error, inspect the actual slide, and obtain sample acceptance; a successful argument alone is not proof of the output ratio.

Assessment: GREEN. Current text explicitly retires the historical workaround and follows live 4:3/16:9 arguments. No alternative backend availability is fabricated. The scenario does not provide the rest of the tool schema, so a complete invented invocation would be unjustified.

## P3 — Actual hypothetical answer

> Preserve the explicitly configured API model `provider/future-image-v3`. API fallback was deliberately selected; do not replace its model with a fixed default or infer restrictions from the name.
>
> Bind capability evidence to that exact model, provider base URL and edit operation. Record the provider documentation source and checked date, supported image inputs, documented quality values and required size constraints; separately validate generate if it is used. The scenario establishes edit inputs and maximum quality support, but does not supply the actual quality enum or size limits. Verify those details rather than inventing them, and keep unknown required facts blocking managed approval until established. Use the provider's documented maximum-quality argument after validation.
>
> With no configured model, there is no default. Consult current official/provider documentation, recommend a documented model and obtain its selection before managed generation. Do not invent a latest alias, silently reuse an old default or make a generation call while the model is unspecified.

Assessment: GREEN. Configured-model-first and no-default behavior are explicit. This exercise does not perform the documentation lookup and therefore does not claim a chosen replacement model or a fully verified capability profile. Missing required facts remain unknown rather than unsupported.

## P4 — Actual hypothetical answer

> Read the compiled ordered `input_images` contract and inspect every one of its six local snapshots; one previously viewed image does not cover the remaining five. Verify the approved snapshot paths, hashes, roles and fidelity, keeping the two style references distinct from the four strict figures.
>
> Submit all six snapshot paths through `referenced_image_paths`, in the compiled order, after checking that this live path mechanism has capacity for six. Do not also pass `num_last_images_to_include`. Each list index maps to the corresponding actual snapshot path/hash/role/fidelity in the job. Label images by these roles in the prompt and preserve strict figure data and labels. No snapshot filenames or hashes were supplied in the scenario, so I cannot fill them with invented values.
>
> After a real successful call, return a UTF-8 receipt with `schema_version=1`, `execution_contract_version=1`, the actual dispatch `attempt_id`/`agent_id`, current `job_sha256`, exact backend/tool, operation and actual path mechanism, candidate path/hash, and the ordered actual submitted attachments. Native evidence is `evidence_origin="agent_reported"`. Include a call reference only if one really exists. A receipt that merely copies the plan or a `view_image` history does not establish actual attachment; do not claim adapter verification.
>
> If the explicit-path mechanism also cannot carry all six and recent-context inclusion is limited to five, stop before generation with an insufficient-input-capacity blocker. Do not truncate, describe an omitted image in text, silently switch backends, or claim verified submission.

Assessment: GREEN. Edited guides provide the explicit all-path route and an honest attempt-bound trust label. No actual receipt is created for this hypothetical exercise. Agent-reported evidence remains a consistency/provenance record rather than independent proof of native internal inputs.

## P5 — Actual hypothetical answer

> Do not start a 30-slide native run when native 4K is required: the original sample is 1672×941, not 3840×2160. Its near-16:9 ratio does not satisfy the separate resolution requirement. Disclose those measured dimensions and resolve an actually capable approved route or a user-approved requirement change before production. API documentation about 4K does not establish native tool capability; switching paths also requires explicit selection and the affected approval updates.
>
> If 4K is only a preference, disclose 1672×941 and let the user accept the actual sample before the approved production run. Record measured and requested sizes separately. Do not upscale, crop, stretch or letterbox and describe the result as native 4K. This one sample also does not prove a universal native resolution maximum.

Assessment: GREEN. The current instructions separate required resolution from preference and retain the independent ratio measurement gate. No output property or acceptance is claimed from this hypothetical test.

## P6 — Actual hypothetical answer

> No. 3:2 is no longer supported for this managed rebuild, and the skill cannot silently relabel a saved project or stretch its images into 4:3.
>
> Preserve the old project and exported PPTX. Choose a supported ratio, 16:9 or 4:3, revise the affected approved plan/output method, and prepare appropriate new approved images. Historical approvals remain historical records; an old final-page acceptance cannot establish a new submission. Old managed files can be inspected, but current execution needs recompilation and fresh attempt evidence. Reapprove actually changed method/content scopes rather than manufacturing approval or treating old acceptance as a bypass. There is no automatic migration to invoke and no reason to delete the user's old deck.

Assessment: GREEN. Retired-ratio handling is now explicit, with no stretch, silent legacy acceptance, automatic migration or deletion. The response preserves history while acknowledging that the requested quick rebuild cannot execute unchanged.

## Overall assessment and limits

All six hypothetical responses align with the requested behaviors under the edited guidance. No new contradiction was found in the six inspected files for these scenarios. This is a same-evaluator, expectation-exposed behavioral exercise, not independent assurance or execution-level verification. In particular, backend capacity, real image attachments, provider capability facts, receipt validation and actual output dimensions require their own runtime evidence; this report does not promote hypothetical responses to verified calls.
