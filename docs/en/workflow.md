# Standard Workflow

## Overview

The Codex PPT workflow emphasizes staged confirmation. Instead of immediately generating the entire presentation, it first confirms the outline, style, PPT ratio, image backend, and sample slide to reduce rework.

## Stage 1: Review the Source Material

The agent first determines:

- The topic and central argument
- The target audience
- The presentation objective
- The required slide count
- Content that must be included or excluded
- Whether any image assets are required

## Stage 2: Confirm the Outline

The agent generates `outline.md`, which usually includes:

- Slide number
- Slide title
- 3-5 key points per slide
- The role of each slide, such as cover, agenda, concept explanation, process, comparison, data evidence, or summary
- Optional visual ideas
- Required image assets and how they will be used

No final slide images, `speech.md`, or `.pptx` file should be generated before the outline is approved.

## Stage 3: Confirm the Visual Style

The agent proposes 2-3 style directions and recommends one. Candidates come from the 12 built-in styles, including clean professional, scientific defense, hand-drawn technical explanation, McKinsey-style, party and government red, and teaching courseware, as well as your personal style library. The agent can also reproduce a style from screenshots, a PDF, or a presentation you provide. See [Styles and Personal Style Library](/en/styles.md) for complete style previews.

After a style is selected, the entire presentation should maintain a consistent visual language, while individual slide layouts may vary according to the content.

## Stage 4: Confirm PPT Ratio, Then the Image-Generation Backend

The agent asks you to pick the final PPT ratio (`16:9` / `4:3` / `3:2`; recommend 3:2 on Cursor, 16:9 on Codex / Claude Code) **before** locking a backend, then only offers tools that can produce that ratio. Cursor `GenerateImage` is 3:2-only. gpt-image-2 tools must pass `--size` `2560x1440` (16:9), `2560x1920` (4:3), or `2400x1600` (3:2).

Once the image backend is confirmed, the entire presentation should use the same backend without switching midway.

## Stage 5: Generate and Confirm a Sample Slide

Generate one sample slide first and check:

- Whether the text is clear
- Whether the style matches expectations
- Whether the information density is appropriate
- Whether the colors and layout are stable
- Whether the design can scale to the full presentation

Generate the full deck only after the sample slide is approved.

## Stage 6: Batch Generation

After the sample slide is approved, the agent generates `origin_image/slide_XX.png` one slide at a time. In environments that support sub-agents, one sub-agent generates each slide in parallel to speed up multi-slide production. Every slide follows the same style and image-generation backend approved for the sample.

## Stage 7: Quality Review and Fixes

Before assembly, the agent reviews every slide for text clarity, consistency with the outline, clipped content, visual consistency, unnecessary page numbers, and overlapping elements. Slides with serious issues are regenerated using stricter prompts, while minor local issues are preferably corrected with targeted image-editing tools.

## Stage 8: Speaker Notes and Assembly

The agent generates the speaker notes in `speech.md`, then asks which PPT output to build (**no template** / **medavis template** / **both**). For medavis or both, it suggests a landing-page title, confirms it with you **before** this run's PPTX exists, and runs `assemble_ppt.py` with `--template`, `--landing-title`, and the locked `--aspect-ratio`. Medavis uses the matching 3-page template (landing + content + ending, `N+2` slides). Speaker notes go on content slides only. Mismatched-ratio images are refused; they are not stretched.

## Stage 9 (Optional): Save the Style

If the presentation uses a custom or adjusted style, the agent notes in the final report that you can save it to your personal style library and reuse it by name in the future. See [Styles and Personal Style Library](/en/styles.md).
