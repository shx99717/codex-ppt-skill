---
name: codex-ppt
description: Use when a user needs a PowerPoint or PPTX presentation from articles, reports, papers, notes, prepared slide content, outlines, or a topic or idea.
---

# Codex PPT

Create a coherent image-based presentation with an approved content, visual and talk plan. Each content slide is one complete generated image; text, charts and shapes are not separately editable. Keep the locked ratio: 16:9 or 4:3.

## Adaptive workflow

Read [content planning](docs/content-planning-and-approval.md) first. Assess reusable content and visual readiness separately, including mixed readiness. Extract known answers; clarify only consequential gaps before expansion. Recommend concrete choices, label proposals and missing evidence, and preserve prepared copy and notes.

Develop the complete story, exact visible copy, intended visuals, source mapping, recurring identities, meaningful slide dependencies, output profile and talk together. Read [speaker-note style](docs/speaker-notes-style.md) before drafting notes. Calibrate a representative note when useful; review the complete plan and talk by exception before expensive images.

Read [style and sample](docs/outline-style-and-sample.md) and [backend selection](docs/backend-selection.md). Lock ratio before a specific capable backend. Reuse supplied style and compatible approved samples; otherwise choose a representative content sample. Additional samples need a material visual reason, not a per-page approval ritual.

After current plan/talk approval, compile explicit sample jobs; accept the actual sample, then compile production. Read [gates and progress](docs/workflow-gates-and-progress.md), [generation](docs/slide-generation-and-subagents.md) and the [worker handoff](prompts/slide-worker.md). Inspect the first production batch before continuing. Apply the chosen consolidated or strict review policy; agent QA never substitutes for user image approval.

Before delivery, validate the complete image/talk sequence and current user approvals, then use [assembly and reporting](docs/project-assembly-and-reporting.md). Plain has N pages; Medavis has landing + N content + ending (N+2). The output profile and landing title are approved in planning, not first introduced after production.

## Hard constraints

- New runs use workflow_version 2. Drafts and simple structural planning previews are allowed before approval; final imagery is generated only after its phase's approval. Never manufacture approval booleans or invent decision evidence.
- Current facts, exact visible wording/critical values, visual objects/relationships, source bytes and shared identities are the production contract. Minor raster variation is acceptable. Fit problems or substantive changes require an affected-plan revision, not a worker rewrite.
- Notes explain approved material in the presenter's voice and language. New substantive claims need approval. No invented company metrics, presenter experience, real customers or speaker names.
- All final images use the selected actual image backend. Local drawing, Pillow, SVG/HTML/canvas screenshots, native PPT layout screenshots and manual overlays are not final-image fallbacks. Structural previews remain labeled planning artifacts.
- Inspect actual tool schemas and local images. A prompt requesting a ratio is not proof. Measure saved pixels; reject more than 2% relative ratio error rather than stretching, cropping or letterboxing.
- Prefer callable Codex image_gen and Cursor GenerateImage using live capabilities. Codex ratios may be prompt-only; Cursor uses supported aspect_ratio values. No permanent native model ID or invented size parameter. Measure original pixels and distinguish resolution preferences from mandatory requirements.
- Require current execution-contract and attempt-bound [submission evidence](docs/image-submission-evidence.md) for managed results; native/bridge evidence remains agent-reported.
- Preserve required figures through real image inputs; inspect supplied labels/data and generated fidelity. Read [source assets](docs/user-supplied-assets.md). No text-only substitute for an unattached image.
- After sample acceptance and full-production authorization, use one slide worker per remaining job when agents are available. The parent owns specs, jobs, state, QA, notes, final images and assembly. Workers use only their assigned packet and never edit parent files.
- Current script approvals and immutable compiled jobs are required at preparation, dispatch, result and assembly. Do not hand-edit job state/prompts, silently fall back to legacy, or use QA as human approval.
- An isolated rendering problem gets one automatic repair within its approved visual contract. Further attempts need recorded actual user authorization. Pause common first-batch failures and fix their shared cause; never drop labels to claim success.
- Revisions include story, visual and talk impact analysis. Reapprove affected scopes; unchanged note-only or unrelated edits do not force image regeneration.

## References and compatibility

Use [CLI/API fallback](docs/cli-api-fallback.md) only after choosing it; [image configuration](docs/image-model-configuration.md) only for an actual configuration problem. A CLI text-only generate path cannot attach required images: confirm an input-capable path in the plan, or raise a blocker before making the call.

The twelve built-in styles and personal style discovery remain in [style and sample](docs/outline-style-and-sample.md). Personal styles live outside installation; same-name personal files take priority. Read [style library](docs/style-library.md) when saving styles, and offer to save a custom/adapted final style.

Legacy manual/image-only CLIs require explicit --legacy-unmanaged. They refuse decks with managed markers. Legacy public assembly/image utilities remain usable. Never use legacy to bypass missing or stale v2 approvals.

Report actual paths/counts, locked backend, approval/QA state, revisions and limitations. Script checks prevent input/state drift; real visual inspection and human acceptance remain necessary for rendered lettering, figure fidelity and delivery quality.
