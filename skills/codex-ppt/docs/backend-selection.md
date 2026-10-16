# Backend Selection

Select the deck ratio (16:9 or 4:3) before a specific backend. Inspect the actual callable tools and their current schemas; a filesystem probe cannot detect host tools.

## Prefer native tools

| Host | Recommended when callable | Alternatives when needed and available |
|---|---|---|
| Codex | `image_gen` | installed `codex-gpt-image`, then explicitly selected `scripts/image_gen.py` |
| Cursor | `GenerateImage` | installed `codex-gpt-image`, then explicitly selected `scripts/image_gen.py` |
| Claude Code | installed `codex-gpt-image` | explicitly selected `scripts/image_gen.py` |

Native tools use the host-managed image model. Do not assign them a permanent API model name or invent a model selector. Claude Code has no native image generation. OpenClaw `image_generate` is not a supported backend here.

Run `python scripts/probe_image_backends.py` for filesystem bridge/CLI candidates only. Script or skill-file presence is availability evidence, not authentication, reference capacity or a successful generation test.

## Ratios and resolution

Codex `image_gen` may expose no size/aspect_ratio arguments. **Keep callable image_gen as the recommended option**: request the locked ratio in its prompt, generate the approved sample and measure saved pixels. Missing size parameters alone are not a reason to omit it or prefer a bridge. Never invent parameters.

For Cursor `GenerateImage`, pass the requested ratio through its actual `aspect_ratio` enum when supported. User tests on 2026-10-16 found working 16:9 (1280x720) and 4:3 (1152x864) output. Earlier fixed-ratio observations are outdated; do not use the old landscape-argument workaround. Inspect each runtime's current schema and saved pixels.

Require at most 2% relative ratio error. Record measured width/height and requested size separately. Native prompt-only resolution tests did not establish exact pixel control: 1080p/1440p/4K requests returned 1672x941 in one session. This is dated evidence, not a universal maximum. A resolution preference may be accepted after disclosing the actual sample; an explicit minimum/exact requirement must be met before production. No resize/crop/letterbox substitute.

3:2 decks are no longer supported. Choose 16:9 or 4:3; existing exported PPTX files remain usable, but the skill does not silently convert saved projects.

## Inputs and menu

Before recommending a backend, check its actual reference input mechanism and capacity for all source/style images. See [source assets](user-supplied-assets.md) and [submission evidence](image-submission-evidence.md). A filename mentioned in a prompt or an image opened with view_image is not proof of attachment.

Explain each available option's input support, auth route, measured/known resolution limits and cost only when known. Recommend one and wait for the user's specific backend choice. Do not offer an unavailable path. A real unavailable tool, failed required capability, insufficient reference capacity or mandatory output requirement may justify another option; local file convenience does not.

## API model selection

Only after API fallback is intentionally selected, reuse its explicitly configured model. If no model is configured, consult current official/provider documentation, recommend a model and obtain selection. Do not replace a configured model automatically or maintain a fixed latest-model assumption. API model IDs do not identify the native model.

Record exact backend/tool, ratio, operation/input policy and API model/settings/capability evidence (when applicable) in `planning.generation` before plan approval. The approved method stays locked across the deck; no silent backend/model/mode change. Read [API fallback](cli-api-fallback.md) for execution and [configuration](image-model-configuration.md) only when config is missing/invalid or the user asks to change it.
