# Quick Start

## Who This Is For

Inputs can range from a topic to complete slide Markdown, including mixed readiness. The skill reuses ready copy and notes, clarifies consequential gaps, and approves exact content, visual meaning and natural presenter talk before expensive images. Consolidated current-image review is the default; strict batch review is available. Minor raster differences remain possible.

## Shortest Way to Get Started

First install the skill by following [Installation and Configuration](/en/installation.md). Then use the skill directly in Codex to create your presentation.

```text
Please use the codex-ppt skill to turn /path/to/article.md into a Chinese presentation of about 10 slides.
```

If you already know the intended style and use case, be more specific:

```text
Please use the codex-ppt skill to turn this technical article into a 12-slide Chinese presentation. Use a clean, professional style suitable for an internal technical talk. Slide 5 must use the architecture diagram I provided, and slide 8 must preserve the experiment results figure.
```

## Recommendations for Your First Use

- Speaker notes are drafted early in the presentation language, as the presenter's own warm, everyday speech: concrete scenes, thought-sized beats with blank-line pauses, natural connectors and purposeful transitions. Supplied notes are preserved; substantial additions need approval. Length follows speaking time and complexity.
- Do not skip sample-slide confirmation. Review one slide before generating the full deck.
- If one slide is unsatisfactory, revise only that slide instead of regenerating the entire deck.
- If you have a reference presentation, screenshot, or PDF, ask the agent to analyze its style before generating the new presentation.

## Generated Outputs

You will usually receive:

- `outline.md`: Presentation outline
- `origin_image/slide_XX.png`: Final image for each slide
- `speech.md`: Speaker notes for each slide
- `{presentation-name}.pptx`: Final PowerPoint file

## Adaptive review

Inputs can range from a topic to complete slide Markdown, including mixed readiness. The skill reuses ready copy and notes, clarifies consequential gaps, and approves exact content, visual meaning and natural presenter talk before expensive images. Consolidated current-image review is the default; strict batch review is available. Minor raster differences remain possible.

Managed v2 scripts enforce current plan/talk/policy decisions, source/sample bytes, compiled inputs, QA and actual current-image acceptance. Historical manual/image-only runs require explicit `--legacy-unmanaged`, which cannot bypass managed approval. CLI jobs use `run_slide_job.py` to forward every approved setting and image input.
