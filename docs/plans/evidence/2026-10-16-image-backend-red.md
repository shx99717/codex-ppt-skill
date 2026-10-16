# Image backend capability RED evidence — 2026-10-16

## Behavioral baseline

Read all five assigned current files: `skills/codex-ppt/SKILL.md`, `docs/backend-selection.md`, `docs/user-supplied-assets.md`, `docs/image-model-configuration.md`, and `prompts/slide-worker.md` (the latter four relative to the skill directory). No edits, network calls, image generation, or paid calls occurred during the behavioral baseline. This evidence file was subsequently saved at the parent's request.

Exposure limitation: Appendix A places each expected result on the same line as its prompt, so I could not isolate prompts from expectations; the answers below apply current instructions explicitly.

**P1 — Actual hypothetical answer**

> Native `image_gen` cannot express size in this schema, so current backend-selection guidance requires me to omit it for this 16:9 deck.
>
> Available confirmed choice:
> A) `codex-gpt-image` — gpt-image-2 via Codex OAuth; `--size 2560x1440`; installed bridge, recommended. Reference/edit support must be checked before image-conditioned slides.
>
> Lock `codex-gpt-image` before the sample. Proposed sample invocation: use the bridge’s inspected command with the approved prompt and `--size 2560x1440`. I cannot invent its remaining command syntax without inspecting its interface. Measure the saved sample and reject relative ratio error above 2%.

Rationale/conflict: Current instructions explicitly exclude this native schema. The SKILL.md hard constraint says size is required only when exposed, but backend-selection.md gives the more specific exclusion. That exclusion conflicts with the desired native-first behavior. I would follow the explicit selection rule and report its inconsistency rather than pretend current instructions already permit native.

**P2 — Actual hypothetical answer**

> For the requested 4:3 deck, current instructions hide Cursor `GenerateImage`: they classify it as 3:2-only despite its live enum.
>
> I need the bridge/CLI probe results before presenting available alternatives. If installed, recommend `codex-gpt-image` with `--size 2560x1920`; otherwise an available `scripts/image_gen.py` path uses `--size 2560x1920`. Confirm the specific backend before sampling.
>
> For 16:9, the same exclusion applies; alternative size is `2560x1440`.
>
> Measure actual saved dimensions and require relative ratio error ≤2%. Do not stretch, crop, or letterbox a mismatched result.

Rationale/conflict: Current documentation makes historical 3:2 output a permanent restriction. It does not permit the desired `aspect_ratio="4:3"` / `"16:9"` native trials. No probe results were supplied, so I cannot honestly claim either alternative is available.

**P3 — Actual hypothetical answer**

> Retain `provider/future-image-v3`: it is the explicitly configured provider model. The configuration reference permits provider-specific names, and the worker must preserve the approved model.
>
> Validate the provider’s documented edit-input and quality settings for that exact model, approve those settings and the operation policy, and use edit mode for image-conditioned work. Do not silently change the model or invent unsupported arguments. Real authentication, permission, endpoint, or model errors require resolution.
>
> With no configured model, current documentation selects its stated default, `gpt-image-2`, through the intentionally selected API fallback. Approve the model, size, quality, and operation policy before generation.

Rationale/conflict: The configured-model case can already succeed under current configuration instructions; claiming it necessarily overwrites the configured ID would fabricate a failure. The missing-model case conflicts with the desired documented-selection policy because current guidance supplies a fixed default. These five files do not specify a capability-evidence protocol or prohibit substring-based implementation assumptions.

**P4 — Actual hypothetical answer**

> Inspect all six compiled local snapshots, including the five not yet viewed. Preserve their compiled roles and hashes; keep style-only snapshots distinct from strict source figures.
>
> Submit all six through `referenced_image_paths`, using the compiled order: each actual snapshot path maps to its approved role/hash. Omit `num_last_images_to_include`; its five-image limit cannot carry this job. In the prompt identify which images are style references and which are strict assets whose labels/data must remain unchanged.
>
> Viewing an image prepares inspection; it does not prove that the image was attached to the generation call.
>
> Receipt trust label: these current documents define no receipt trust-label vocabulary or verified-submission mechanism. My report would be agent-reported preparation/submission information, with actual call arguments where available; I would not claim independently verified submission.
>
> If neither actual input mechanism can carry all six, return a blocker before generation. Do not truncate, replace images with descriptions, or silently switch backend.

Rationale/conflict: The worker already requires actual attachment of every required image and a blocker when that is impossible. Native source-asset prose overemphasizes conversation visibility and lacks the explicit-path recipe, but it does not require me to discard a working live path mechanism. The major desired addition is enforceable submission receipts, not a genuine baseline inclination to truncate.

**P5 — Actual hypothetical answer**

> Do not start the 30-slide run when native 4K is mandatory. The measured sample is 1672×941, so it does not satisfy the requested 3840×2160 output despite the prompt. Disclose that result and resolve a capable generation path and affected approvals first. API documentation saying 4K exists does not prove this native path produces it.
>
> If 4K is only a preference, disclose the measured size and obtain acceptance of the actual sample before proceeding under the approved plan. The sample’s ratio is within the current 2% tolerance. Do not represent an upscaled image as native 4K.

Rationale/conflict: Current docs explicitly demand actual pixel measurement and sample acceptance. Although they lack a dedicated mandatory-size versus preferred-size policy, the user’s mandatory requirement still governs. A fabricated “current skill would blindly run 30 slides” failure would be unjustified. The desired policy makes this distinction explicit.

**P6 — Actual hypothetical answer**

> No: I cannot relabel the deck 4:3 and stretch its existing images. Current guidance supports a locked 3:2 deck, so a rebuild can preserve 3:2 if its current managed approvals and compiled jobs remain valid.
>
> Inspect the old configuration and approval state first; do not manufacture approval or bypass managed gates. Changing to 4:3 changes the approved output contract and requires the affected plan and images to be revised and approved. Preserve the user’s old deck.

Rationale/conflict: Stretching and silent relabeling are already prohibited. The genuine mismatch is that current guidance explicitly supports 3:2; it would not give the desired “3:2 unsupported” response. The assigned current files do not authorize automatic migration or deleting old decks.

## Parent-provided runtime baseline

The parent supplied the following actual runtime observations. This subagent did not run or independently reproduce these tests:

- Before edits, the full suite passed: **168 tests in 102.998s**.
- The new `test_backend_capability_contract` produced five RED failures: the ratio set includes 3:2; the 3:2 template exists; the execution version is missing; result recording accepts no submission; and output policy leaks into native parameters.
- New tests for `image_capabilities`, `input_contract`, and `output_requirements` initially failed import because those modules were not implemented.

No further tests or generation were performed while saving this evidence. No paid calls were made.
