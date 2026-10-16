# Design Philosophy

Codex PPT Skill reflects some of my thinking about using AI to create presentations.

The most important thing about AI-generated presentations is not speed, but having a controllable process that produces usable results.

That is why I split the process into several steps:

1. Assess reusable content and visual readiness; reuse known decisions and clarify only consequential intent.
2. Draft exact copy, visuals, sources, shared identities, story/dependencies and natural presenter notes together. Label proposals and missing evidence. Select or reuse style, lock ratio and a capable backend with explicit settings/image-input operations, and define representative samples, output profile/title and review policy.
3. Approve the complete content/visual/talk/method/output plan by exception, then generate or reuse and accept the representative samples.
4. Compile approved jobs, generate the deck, inspect the first batch and the complete sequence. Allow one targeted automatic rendering repair; further attempts need authorization. Default to consolidated current-image user review; strict batch review is available.
5. Revalidate current inputs, images, talk and approvals, then assemble the already-approved plain/Medavis/both output. Plain has N content slides; Medavis has N+2 with content-note offsets. Optionally save a custom/adapted style.

## Why Generate an Image-Based Presentation First?

Not every scenario requires editability. For technical talks, course notes, book-sharing sessions, paper reviews, or less formal reports, a presentation made from full-slide images is often sufficient and offers better visual consistency.

If presentation generation and editable presentation conversion are tightly coupled from the beginning, the process becomes heavy. While the outline, style, and sample slide are still being revised, adding editable-structure reconstruction makes the workflow slower, more expensive, and harder to control.

That is why I split the process into two skills:

- One generates high-quality image-based presentations
- The other converts an image-only presentation into an editable presentation when needed

I believe it is more reliable to agree on the content and visual direction first, confirm that the generated results are under control, and only then decide whether editable conversion is necessary.

## Improvements Based on Community Feedback

This skill also includes several improvements based on community feedback:

- Supports the image-generation capability included with Codex subscriptions
- Also supports image-generation models through APIs
- Works in agent environments including Codex, Claude Code, and OpenClaw
- Supports parallel generation with sub-agents to speed up multi-slide presentation creation
- Includes guidance for multiple built-in styles, so you can get good results without writing advanced prompts
- Supports using reference images or existing presentations to generate a new presentation in a similar style
- Preserves user-provided source images such as paper figures, experiment result charts, and screenshots wherever possible, reducing the risk of AI redrawing them incorrectly

My goal is not to produce a 20-slide presentation with one click. It is to make AI presentation creation feel more like a real workflow: establish the structure, choose the style, approve a sample, then generate the complete deck and inspect the results.

Inputs can range from a topic to complete slide Markdown, including mixed readiness. The skill reuses ready copy and notes, clarifies consequential gaps, and approves exact content, visual meaning and natural presenter talk before expensive images. Consolidated current-image review is the default; strict batch review is available. Minor raster differences remain possible.

Speaker notes are drafted early in the presentation language, as the presenter's own warm, everyday speech: concrete scenes, thought-sized beats with blank-line pauses, natural connectors and purposeful transitions. Supplied notes are preserved; substantial additions need approval. Length follows speaking time and complexity.
