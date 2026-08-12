# Project Assembly And Reporting

Read this before initializing the project directory, writing speaker notes, assembling the PPT, or sending the final report.

## Project Directory

Use this output structure:

```text
{base_dir}/{deck_name}/
├── origin_image/
│   ├── slide_01.png
│   ├── slide_02.png
│   └── ...
├── prompts/
│   ├── slide_01.json
│   └── ...
├── slide_jobs.json
├── slide_run_state.json
├── deck_spec.json
├── outline.md
├── speech.md
└── {deck_name}.pptx
```

If the user did not specify a destination, use the current working directory or the directory that contains the source file.

Let `{runtime_python}` mean the shared venv interpreter under `~/.codex-ppt-skill/.venv` (Windows: `Scripts/python.exe`; Unix/macOS: `bin/python`). You may initialize the directory structure with:

```bash
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx --init
```

## Quality Check And Repair

Before assembling the PPT, inspect every slide image. Check:

- Text is readable and not garbled.
- Slide content matches the outline.
- Title and key points are not truncated.
- Visual style is consistent across slides.
- No page number appears unless the user requested one.
- Important elements do not overlap.

If a slide has severe text or layout issues, regenerate it with a more constrained prompt. If a slide is mostly correct but has a localized issue, use the selected backend's edit capability when available. In CLI/API fallback mode, use `scripts/image_gen.py edit --image {slide_path} --prompt ... --out {new_slide_path}` and replace the final slide only after validating the edited output.

## Speaker Notes

Make sure `outline.md` reflects the final confirmed deck outline. Do not recreate it from scratch here.

Create `speech.md` as presenter notes that a speaker can use directly. Do not write a brief summary of visible slide text. Write in the presentation language; for Chinese decks, speaker notes should be in Chinese.

For each slide, write only the spoken talk track directly under the slide heading, without an extra label. It is the script the presenter can read or closely follow. It should connect the slide to the deck's main story, explain the point the audience should take away, and include a natural transition at the end when useful.

Before writing the slide notes, choose a delivery style based on the deck content, audience, and purpose. The delivery style is not a label added after writing; it should shape the actual talk track, including how direct the claim is, how much background is explained, which examples are used, how quickly the speaker moves, and how transitions are phrased.

Common delivery styles:

- Technical explainer: patient, definition-first, example-driven, with careful visual walkthroughs.
- Research or paper reading: evidence-led, method/result/limitation oriented, with clear claims about what the audience should learn from each figure.
- Product or pitch deck: outcome-first, persuasive, focused on user pain, value, proof, and the next action.
- Training or workshop: step-by-step, checkpoint-driven, with small prompts for audience reflection or practice.
- Executive report: conclusion-first, concise, focused on decisions, risks, tradeoffs, and recommended actions.

Keep one deck-level delivery style consistent, but adapt the tone by slide role. For example, an opening slide can be more framing-oriented, a dense diagram slide can slow down for explanation, and a closing slide can become more action-oriented.

Length guidance:

- Title, agenda, and section-divider slides can be 1-2 short paragraphs.
- Normal content slides should usually be 2-5 short paragraphs, or roughly 150-400 Chinese characters for Chinese decks.
- Dense concept, architecture, data, or paper-explanation slides may need more, but split long material if the audience would lose the thread.

Use basic presentation craft in the talk track:

- Lead with the claim before the details.
- Explain visuals in the order the audience should look at them.
- Add examples, contrast, caveats, and "so what" implications instead of rereading the slide.
- Close with a natural bridge to the next slide when useful.

Write the talk track from the presenter's point of view, facing the audience. Avoid generic AI-style phrasing, canned summaries, and phrases that sound detached from the actual talk. The script should sound like a person explaining this specific deck in the room:

- Use natural first-person or speaker-facing phrasing when appropriate, such as "这里我想强调的是..." or "我们先看左边这个结构...".
- Ground each paragraph in the current slide's content and the surrounding deck narrative.
- Prefer concrete explanations, examples, and audience-oriented transitions over broad filler like "本页主要介绍了..." or "综上所述...".
- Do not mention that the notes were generated, inferred, or prepared by an AI.

Use headings that the assembly script can map back to slide numbers:

```markdown
## Slide 1: {Title}

{Presenter talk track for slide 1. For Chinese decks, write this in Chinese. Include an optional transition sentence at the end when useful.}

## Slide 2: {Title}

{Presenter talk track for slide 2}
```

## Assembly

Before running `scripts/assemble_ppt.py` or the CLI/API fallback scripts, make sure the shared runtime exists. If `{runtime_python}` is missing, or if importing script dependencies fails, create or refresh the environment:

```bash
python3 {skill_root}/scripts/codex_ppt_runtime.py bootstrap
```

This is an internal setup step for the skill. Do not ask the user to run these commands unless dependency installation fails and user approval or troubleshooting is required.

Run:

```bash
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx --aspect-ratio 16:9
```

### Template mode (required user choice)

Before running `assemble_ppt.py`, ask the user which PPT output to build:

- **No template** — current behavior: full-bleed slide images only (`{deck_name}.pptx`)
- **Medavis template** — corporate wrap using the bundled medavis 16:9 template (`{deck_name}-medavis.pptx`)
- **Both** — generate both files

If the user chooses medavis or both:

1. Suggest a landing-page title from `outline.md` / the deck topic.
2. Ask the user to confirm or edit that title.
3. Pass `--template medavis|both` and `--landing-title "..."` to `assemble_ppt.py`.

Medavis output structure:

- Slide 1 = landing page with the confirmed title
- Slides 2..N+1 = content pages cloned from the template’s content layout; each generated image is placed in the white area under the header so the medavis logo remains visible; speaker notes from `speech.md` Slide K are written on content slide K

Medavis mode assumes the deck’s generated images are **16:9** (the skill default). Do not use medavis wrapping for a 4:3 deck in v1 without an explicit user decision to regenerate at 16:9.

Do not skip the template-mode question by assuming “no template”. Do not invent a custom template path in v1 — use the bundled medavis asset only.

Do not:

- Write the medavis deck over `{deck_name}.pptx` (always use `{deck_name}-medavis.pptx`)
- Full-bleed content images over the medavis logo / header band
- Treat “both” as a single file — always produce both `{deck_name}.pptx` and `{deck_name}-medavis.pptx`

Example commands:

```bash
# none (default)
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx --aspect-ratio 16:9

# medavis only
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx \
  --template medavis --landing-title "Confirmed Title Here"

# both
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx \
  --template both --landing-title "Confirmed Title Here"
```

Important:

- `{base_dir}` is the parent directory of `{deck_name}/`.
- `{deck_name}.pptx` must match the project folder name.
- The script reads images from `{base_dir}/{deck_name}/origin_image/`.
- The script only reads final images named like `slide_01.png`, `slide_02.png`, etc.; drafts and sample files are ignored.
- Before running assembly, `slide_jobs.json` should show every generated slide as `recorded` with a valid `user_review` (status `user_reviewed` and `image_sha256` matching the current `origin_image/slide_XX.png`), and every approved sample slide as `accepted`. If any slide is `pending`, `dispatched`, or `blocked`, or any non-sample recorded slide lacks valid user review, stop and report that state. `assemble_ppt.py` does not enforce the user-review marker — the agent must.
- Do not regenerate only a named slide without impact analysis (other slides / planned narrative / visuals) and user confirmation when scope expands.
- If `{base_dir}/{deck_name}/speech.md` exists and uses `Slide N` headings, the script writes those notes into the corresponding PPT speaker notes.
- For `--template none` (default), the script writes `{base_dir}/{deck_name}/{deck_name}.pptx`.
- For `--template medavis`, the script writes `{base_dir}/{deck_name}/{deck_name}-medavis.pptx`.
- For `--template both`, the script writes both files.

`assemble_ppt.py` supports `16:9` and `4:3` for `--template none` only. Use `16:9` unless the user requests otherwise. Medavis mode always uses the bundled 16:9 template and ignores `--aspect-ratio`. `image_gen.py` loads `~/.codex-ppt-skill/.env` automatically for `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `CODEX_PPT_IMAGE_MODEL`. Run `python3 {skill_root}/scripts/codex_ppt_runtime.py doctor --check-api` when troubleshooting API access.

## Final Report

Report:

- Project directory
- PPT file path(s) — include `{deck_name}.pptx` and/or `{deck_name}-medavis.pptx` for every file actually generated
- For a medavis deck, also note slide count as landing + content (`1 + N`)
- Slide image directory
- `outline.md` path
- `speech.md` path
- `slide_jobs.json` path
- Number of slides (for none: N content slides; for medavis: `1 + N`)
- Confirm which image backend was used and that every non-sample slide result was recorded with `record_slide_result.py`.
- Confirm that speaker notes from `speech.md` were written into the PPT, if applicable
- Any slides that were regenerated, blocked, or still have known limitations
- If the deck's style is custom or noticeably adapted (extracted from user references, tuned during sampling, or otherwise not an unmodified built-in style), end with a one-sentence tip that the style can be saved to the personal style library for future reuse, for example: "如果你喜欢这套风格，可以说「保存这个风格」，我会把它存入个人风格库（`~/.codex-ppt-skill/references/`），以后可以直接复用，更新 skill 也不会丢失。" If the user agrees, read `docs/style-library.md`. Skip this tip when the deck used an unmodified built-in style.

## Prompting Principles

- Keep one global visual style fixed across the deck.
- Vary slide composition by page role; style consistency does not mean repeating the same layout.
- Use `layout_blueprints` as candidate patterns, not mandatory templates.
- Generate one slide per image request.
- Prefer concrete visual direction over generic words like "beautiful" or "professional".
- For dense content, split across more slides instead of crowding one slide.
- Prioritize clarity over decoration.
