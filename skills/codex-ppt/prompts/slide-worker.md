# Slide Worker Prompt

Use this template when dispatching a slide subagent after the sample slide is approved and full-deck generation is authorized.

```text
Generate slide <N> for this codex-ppt deck.

Deck dir: <absolute deck dir>
Slide job file: <absolute deck dir>/prompts/slide_<NN>.json
Output target owned by parent: <absolute deck dir>/origin_image/slide_<NN>.png
Selected image backend: <exact locked label from parent>
Sample generation method copied from the approved sample:
- backend_used: <exact backend label recorded by parent>
- tool_name: <GenerateImage OR image_gen OR codex-gpt-image OR scripts/image_gen.py>
- mode: <generate OR edit>
- model/config: <model, size, quality, or "built-in default" if not exposed>
- prompt_source: <approved sample prompt source>
- input_context_preparation: <how local images were made visible or attached>
- approved_sample_path: <absolute path to approved origin_image/slide_XX.png>
- handoff_rule: use this same backend/tool/mode; return a blocker if unavailable
Input images already prepared by the parent:
- <absolute path> - approved sample slide style reference; match style only, do not copy layout
- <absolute path> - strict input asset; preserve labels/data/arrows/content

Read the JSON job file, then follow its `prompt` field exactly. Use the selected image backend and the recorded sample generation method only.
You must produce the final slide candidate by calling the selected image generation backend:
- Use the exact locked tool/label from the parent (for example Cursor GenerateImage, Codex image_gen, codex-gpt-image, or scripts/image_gen.py).
- The locked backend must emit the **locked PPT ratio** from `deck_spec.json` / `slide_jobs.json` (`aspect_ratio`). Gate 2% relative ratio, not exact pixels.
- Cursor GenerateImage: only when locked ratio is 3:2; pass `aspect_ratio="3:2"`. Prompt text is not enough. If the parent locked 16:9 or 4:3, return a blocker instead of calling GenerateImage.
- gpt-image-2 tools (`image_gen`, `codex-gpt-image`, `scripts/image_gen.py`): pass `--size` `2560x1440` (16:9), `2560x1920` (4:3), or `2400x1600` (3:2). Do not use `auto`.
- If a style or `references/*.md` file says 16:9 but `deck_spec.aspect_ratio` is 4:3 or 3:2, follow the spec Canvas / locked ratio.
- CLI/API fallback mode: use `scripts/image_gen.py` with the saved job prompt, required image inputs, and the ratio `--size`.
- If the tool cannot produce the locked ratio, stop and return `blocker=<reason>` instead of stretching, letterboxing, or cropping.

Forbidden for final slide image creation:
- local drawing or rendering scripts
- Pillow-generated slides
- SVG, HTML/CSS, or canvas screenshots
- python-pptx/PptxGenJS/native PPT layout screenshots
- manually composited text, card, chart, or image overlays
- switching to a different backend than the parent locked (including OpenClaw image_generate)

If you cannot use the selected image backend, stop and return `blocker=<reason>` instead of creating a lower-quality replacement.
If you cannot follow the recorded sample generation method, stop and return `blocker=<reason>` instead of switching tools.
Do not edit slide job files, origin_image, speech.md, or assemble the PPT.

Before returning, visually check:
- text in the slide's locked language is readable and not garbled (for mixed slides: both CJK and Latin)
- style matches the approved sample slide
- required source images are visibly included and not replaced by a similar redraw
- no overlapping or truncated important content

Return only:
backend_used=<exact locked label from parent>
selected_source=/absolute/path/to/$CODEX_HOME/generated_images/.../ig_*.png
qa_note=<one sentence>
```
