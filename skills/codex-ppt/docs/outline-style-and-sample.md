# Outline, Style, And Sample

Read [content planning](content-planning-and-approval.md) before draft preparation, and this guide before choosing reusable styles or calibrating imagery. For reusable style saving, read [style library](style-library.md).

## Plan content, visuals and talk together

Assess readiness, preserve ready source copy/notes, clarify consequential gaps, and develop the whole deck's story. Use exact visible text, critical labels/values, visual objects/relationships/approximate composition, asset/source/proposal status, shared identities, meaningful dependencies and transitions. Include per-slide language for multilingual decks. Do not impose 3–5 bullets or a typical slide-count formula.

Prepare deck_spec.draft.json and derived outline.draft.md/speech.draft.md; talk is drafted now using [the voice reference](speaker-notes-style.md). Show the whole plan with intelligent recommendations and review by exception. Keep substantive gaps visible; do not invent company measurements.

For source figures, show the actual renderable image with its slide/role/fidelity alongside the visual plan where helpful. Convert Markdown image references to normalized required_images objects before approval. A separate asset-mapping interview is unnecessary when the combined plan already makes the mapping clear.

## Confirm A Unified Visual Style

Before generating slide images, discuss the visual style with the user unless the user has already provided a clear style direction or reference material.

If the user has already specified a style, provided a style image, or provided a PDF/PPT/PPTX to use as style reference, do not force a 2-3 option style selection. Extract the usable style rules, briefly restate them, then proceed to backend confirmation and sample generation.

For PDF/PPT/PPTX style references, do not infer the visual system from document structure, outline text, XML, file metadata, or slide object hierarchy alone. First render or export representative pages/slides into real page images, inspect those rendered images, and derive the style from what is actually visible on the pages. If the file has multiple visual sections, inspect enough representative pages to capture the shared style and any section-specific variations.

When extracting style from reference material, separate content reuse from style reuse. Unless the user explicitly asks to reuse the source content, treat the provided image/PDF/PPT/PPTX as a style reference only.

If the user has not provided a clear style, prefer a multiple-choice question: offer 2-3 concrete style directions and mark one as your recommendation. Each style option should briefly specify:

- Color palette
- Layout system
- Typography direction
- Illustration or image treatment
- Decorative elements
- Density and whitespace rules

After the user chooses a style, create one final style direction and keep the visual identity consistent across all slide prompts. Keep color palette, typography, texture, icon/illustration language, and overall mood stable. Do not reuse the same layout on every page.

Reusable style references come from two locations:

- Built-in styles: the skill's `references/` directory, listed below. They ship with the skill and update with it.
- User custom styles: `${CODEX_PPT_HOME:-~/.codex-ppt-skill}/references/*.md`. They live outside the skill install so they survive skill updates and reinstalls.

Before offering or using reusable styles, list the user custom style directory (if it exists) and merge its `*.md` files with the built-in list below. User custom styles are discovered by scanning that directory; they are never registered in this document. If a user custom style has the same filename as a built-in style, the user custom file takes priority and replaces the built-in one.

Use style references as inspiration, not as rigid templates. Adapt the style to the topic and audience.

Important: a deck should have one coherent visual identity, not one repeated composition. Treat each reference as a style system: stable palette, typography, icon language, texture, and visual mood; variable page layout chosen from the slide's content role. `layout_blueprints` are candidate starting points only. Do not apply the same blueprint to every slide.

Available built-in references:

- `references/清爽专业风.md`
- `references/创意杂志风.md`
- `references/电子墨水杂志风.md`
- `references/数据仪表盘风.md`
- `references/科研答辩风.md`
- `references/复古扁平插画风.md`
- `references/手绘技术解释风.md`
- `references/手绘白板风.md`
- `references/温暖手工风.md`
- `references/麦肯锡风格.md`
- `references/党政红风格.md`
- `references/教学课件风.md`
- `references/medavis企业风.md`

This list only tracks built-in styles shipped with the skill. Do not add user custom styles here; they are saved to `${CODEX_PPT_HOME:-~/.codex-ppt-skill}/references/` via `docs/style-library.md` and discovered by directory scan, so they need no registration.

Example style confirmation:

```text
我建议用 A，因为它最适合这份内容的受众和表达目标。

A. 清爽专业风（推荐）：浅色背景、蓝绿强调色、结构清晰，适合汇报、答辩和技术分享。
B. 创意杂志风：大标题、强图片、留白更大胆，适合分享和传播。
C. 数据仪表盘风：指标卡、图表感布局，适合数据密集型报告。

你选哪个？也可以指定要调整的配色、布局或插画方向，或者上传一张喜欢的 PPT 风格图片让我参考。
```

## Representative calibration

After current content/visual/talk/policy approval, choose a representative content slide that tests the important typography, visual relationships and density. Reuse a suitable previously approved sample with matching current style/backend/ratio and recorded suitability. Explain extra samples only for materially different visual approaches. Samples do not authorize other slides' copy or layout.

The representative strategy is part of whole-plan approval. Sample phase needs explicit required IDs and current plan/talk approval, but not the sample it is about to produce:

```text
prepare_slide_prompts.py --spec DECK/deck_spec.json --out-dir DECK --phase sample --slides slide_02
```

Use the actual selected image tool/input path and locked ratio. Inspect the generated candidate, then show the full-resolution image and request acceptance of wording, visual meaning, typography, density and readability. Feedback changing approved content/design updates affected plan scopes before production.

Record the actual decision and consuming backend; never use a sample_approved boolean or pathname alone:

```text
record_plan_approval.py DECK --approve-sample slide_02 --image CANDIDATE.png --backend-used LABEL --evidence "Actual sample acceptance"
```

Approval preserves immutable bytes in references/approved_samples and separately binds the accepted final content slide. Explicit --style-only reuse does not accept that reference as a final page. A content-page rendering repair must not overwrite the shared style reference.

Lock the available backend/tool/mode/input preparation/model/config in planning.generation before approval; carry that contract into jobs. Check the actual tool path can attach every source/style image. Cursor records the legal tool_aspect_ratio_argument separately from the locked aspect_ratio and measured pixels. Changing a method or sample strategy requires a revised approved plan; never silently route around unsupported capabilities.

Production starts only after compatible required samples are accepted:

```text
prepare_slide_prompts.py --spec DECK/deck_spec.json --out-dir DECK --phase production
```

Keep one visual identity while layouts vary by slide role. Calibration is a meaningful shared check, not pixel-identical geometry or a per-page interview.
