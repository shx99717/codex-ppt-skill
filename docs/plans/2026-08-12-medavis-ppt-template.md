# Medavis PPT Template Assembly Implementation Plan

> **For the implementing agent:** Follow this plan task-by-task. Complete each step, verify it works, then move to the next.

**Goal:** Extend `codex-ppt` PPT assembly so the agent/user can choose no template, medavis corporate template, or both — bundling the medavis 16:9 template and wrapping generated slide images + speaker notes into it.

**Architecture:** Keep image generation unchanged. Extend `skills/codex-ppt/scripts/assemble_ppt.py` with `--template none|medavis|both` and `--landing-title`. Bundle the medavis `.pptx` under `skills/codex-ppt/assets/templates/`. Medavis mode opens that 2-slide template (landing + content-layout master), sets the landing title, builds N content slides from slide 2’s layout, places each `origin_image/slide_XX.png` in the white area under the header (logo remains visible), and maps `speech.md` notes to content slides. Skill docs teach the agent to ask the user for mode and confirm the landing title before assembly.

**Tech Stack:** Python 3, `python-pptx`, Pillow (already used), stdlib `unittest`, Markdown skill/docs (zh/en/ko).

---

> **SELF-CONTAINED HANDOFF PLAN.** The executor needs no prior chat session or memory file and must not ask the user to re-explain context. All task context lives in this plan (and its appendices). Normal session-start rules still apply, but you may start fresh and rely on this document.

## Section 0: Full Context

### 0.1 Why / background

`codex-ppt` generates each slide as one full-page AI image, then `assemble_ppt.py` builds a blank full-bleed image PPTX. medavis wants an optional corporate wrap: same images and notes, but inside their branded template (landing page + header/logo chrome on content pages). Assembly is simple (paste images + notes), so the right place for the choice is the assembly step — not image generation.

### 0.2 Confirmed decisions (do not re-litigate)

1. **Bundle** `medavis_ppt_template_2026_en_16-9.pptx` inside the skill repo (source to copy from: `D:\temp\2026.08\ppt_template\medavis_ppt_template_2026_en_16-9.pptx`). No per-run custom template path in this change. Prefer the `.pptx`, not the sibling `.potx`.
2. **User modes at assembly:** `none` | `medavis` | `both`.
3. **Landing title:** agent auto-suggests from outline/content, user confirms/edits, then pass `--landing-title`.
4. **Image placement:** white content area below gray header; **medavis logo must remain visible** (not full-bleed over the whole slide).
5. **Template structure:** exactly 2 slides — slide 1 landing, slide 2 is the reusable content layout master. Always rebuild content pages from that master layout (do not require N pre-made content slides in the file).
6. **Approach:** extend `assemble_ppt.py` (not a separate script; not a shared-library refactor).
7. **Outputs:**
   - `none` → `{deck_name}.pptx` (unchanged path/name)
   - `medavis` (alone or as part of both) → always `{deck_name}-medavis.pptx`
   - `both` → both files
8. **Notes:** `speech.md` Slide N → medavis **content** slide index N (PPT page N+1). Landing notes empty by default.
9. **Out of scope:** image gen changes; generic multi-template systems; custom template path override; hard-blocking review gates.

**Rejected alternatives (do not reopen):**
- Separate `assemble_medavis_ppt.py` only
- Shared-library + thin CLI refactor for this feature
- Full-bleed images covering the logo
- Medavis-only output named `{deck_name}.pptx` (no `-medavis` suffix)

### 0.3 Audience & assumptions

- Repo root: `D:/git/codex-ppt-skill`
- Edit the skill under `skills/codex-ppt/` only. Do **not** run collection install/uninstall scripts. Do **not** commit unless the user explicitly asks.
- Python available; run assembly tests via stdlib `unittest` (existing pattern in `skills/codex-ppt/scripts/tests/`).
- Shared runtime venv may exist at `~/.codex-ppt-skill/.venv` with `python-pptx` / Pillow; if imports fail, use that venv or `python3 skills/codex-ppt/scripts/codex_ppt_runtime.py bootstrap`.
- Windows paths are first-class; force UTF-8 stdout in scripts (already done in `assemble_ppt.py`).

### 0.4 Project rules / conventions to honor

- `AGENTS.md`: changelog under `## Unreleased` in English; documentation changes update **all** language versions in sync (`README.md`, `README_en.md`, `README_ko.md`, and Docsify trees `docs/`, `docs/en/`, `docs/ko/` where assembly is mentioned).
- Conventional Commits if/when committing (user must request commit). PR titles same style.
- YAGNI: only medavis bundled template; no plugin template registry.
- TDD for script behavior; skill-doc changes need RED/GREEN pressure evidence (see tasks).
- Verification before claiming done: run commands and read output.

### 0.5 Formats & reference material

See **Appendix A** (template facts + placement constants), **Appendix B** (CLI contract), **Appendix C** (implementation sketch), **Appendix D** (doc wording targets), **Appendix E** (skill pressure scenarios).

### 0.6 Plan revision (critical review, 2026-08-12)

Patches applied after `think-mcp` review — **do not skip**:

1. Root `.gitignore` has `*.pptx` — must add a negation so the bundled template is trackable.
2. Landing title textbox must use medavis blue `#42637B` and fully cover layout “Insert title here”.
3. Content image must start just below the logo band and fill to the slide bottom so layout title/body ghost text is covered (still not covering the logo).
4. Visual smoke is **mandatory** when the coffee-extraction (or any) deck images exist.
5. Docs task starts with `rg assemble_ppt` for a complete multilingual touch list.
6. Medavis mode assumes **16:9** deck images (skill default); document that.

---

### Task 1: Bundle the medavis template asset

**Files:**
- Create dir: `skills/codex-ppt/assets/templates/`
- Create: `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx`
- Modify: `.gitignore` (add pptx negation for the bundled template)
- Optional create: `skills/codex-ppt/assets/templates/README.md` (one short paragraph: what the file is, do not edit casually)

**Step 1: Copy the source file**

```bash
mkdir -p skills/codex-ppt/assets/templates
cp "D:/temp/2026.08/ppt_template/medavis_ppt_template_2026_en_16-9.pptx" \
   skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx
```

If the source path is missing, stop and ask the user for the file — do not substitute the `.potx`. This path is machine-local to the authoring environment.

**Step 2: Un-ignore the bundled template in `.gitignore`**

Root `.gitignore` contains a blanket `*.pptx` rule. After the existing `!assets/good-skill-design.pptx` exceptions, add:

```gitignore
!skills/codex-ppt/assets/templates/
!skills/codex-ppt/assets/templates/*.pptx
```

Verify git can see the file:

```bash
git check-ignore -v skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx || echo "not ignored (good)"
git status --short skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx
```

Expected: not ignored; status shows `??` or `A`/`M` for the pptx (not silent).

**Step 3: Verify template opens**

```bash
python -c "from pptx import Presentation; p=Presentation('skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx'); assert len(p.slides)==2; print(p.slide_width, p.slide_height, 'ok')"
```

Expected: `9144000 5143500 ok`

**Step 4: Stop** — do not modify `assemble_ppt.py` until Task 2 failing tests exist.

---

### Task 2: RED — failing unit tests for template assembly

**Files:**
- Modify or extend: `skills/codex-ppt/scripts/tests/test_assemble_ppt.py`
  (prefer adding new test classes in this file; create `test_assemble_ppt_medavis.py` only if the file becomes unwieldy)

**Step 1: Write failing tests** covering at least:

1. `create_presentation` / CLI `none` still writes `{deck}.pptx` with N full-bleed slides (regression).
2. CLI `--template medavis --landing-title "Demo Title"` writes `{deck}-medavis.pptx` (not `{deck}.pptx`), slide count `1 + N`, and does **not** require `{deck}.pptx`.
3. CLI `--template both --landing-title "Demo Title"` writes both `{deck}.pptx` and `{deck}-medavis.pptx`.
4. Medavis landing slide contains the landing title string somewhere in slide-1 shapes text; title shape geometry covers the layout title box (same constants as Appendix A); font color is medavis blue RGB `(0x42, 0x63, 0x7B)` when asserted via python-pptx.
5. Medavis content slides: each has at least one picture; picture `top` is **>=** `MEDAVIS_CONTENT_TOP` and **>** logo band bottom (`627534`); picture height reaches the slide bottom (`top + height == slide_height`); picture does not use `top==0` full-bleed (logo band must remain uncovered).
6. With a tiny `speech.md` (`## Slide 1: ...` / `## Slide 2: ...`), notes on medavis content slide 1 (PPT slide 2) match speech slide 1; landing notes empty or blank.
7. `--template medavis` without `--landing-title` exits non-zero.
8. Existing GBK stdout encoding tests still apply to `none` path (do not break them).
9. Saving medavis output must not overwrite/mutate the bundled template file on disk (compare template mtime/size before vs after).

Use temp dirs + tiny PNGs via Pillow (same pattern as existing tests). Prefer calling library functions where easier; also exercise `main()` / argv for CLI flags.

**Step 2: Run tests — expect FAIL** (flags/functions missing)

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_assemble_ppt -v
```

If import path fails, run from `scripts` with `PYTHONPATH=.` or follow how other tests in that folder are invoked.

Expected: FAIL on missing `--template` / medavis helpers.

**Step 3: Record RED evidence**

Create `docs/plans/evidence/2026-08-12-medavis-template-red.md` noting failing test names and that docs currently have no template-mode gate (Appendix E rationalizations).

---

### Task 3: Implement medavis assembly in `assemble_ppt.py`

**Files:**
- Modify: `skills/codex-ppt/scripts/assemble_ppt.py`

**Step 1: Minimal implementation** (see Appendix C for sketch; match existing style)

Required behaviors:

- Resolve bundled template path relative to the skill root:
  `Path(__file__).resolve().parents[1] / "assets/templates/medavis_ppt_template_2026_en_16-9.pptx"`
- CLI:
  - `--template {none,medavis,both}` default `none`
  - `--landing-title TEXT` required when template is `medavis` or `both`
- `none`: existing `create_presentation(...)` → `{deck_name}.pptx`
- `medavis`: `create_medavis_presentation(...)` → `{deck_name}-medavis.pptx`
- `both`: run both
- Medavis build algorithm:
  1. `Presentation(bundled_template_path)` (keeps masters/layouts). Never `save()` back to the template path.
  2. Set landing title on slide 1 **without editing the shared layout** — add a text box at the layout title geometry from Appendix A. Font size ~32pt, color RGB `(0x42, 0x63, 0x7B)`. The textbox must fully cover the layout’s “Insert title here” placeholder region (same geometry).
  3. Let `content_layout = prs.slides[1].slide_layout`
  4. For `i, image` in enumerate(images):
     - Use existing slide 2 for `i==0`; for `i>0` call `prs.slides.add_slide(content_layout)`
     - Compress image if needed (reuse `compress_image_if_needed`)
     - `add_picture(image, left=CONTENT_LEFT, top=CONTENT_TOP, width=slide_width, height=slide_height - CONTENT_TOP)` so the picture covers layout title/body chrome below the logo band
     - Write speaker notes from `speaker_notes.get(i+1)` onto that content slide
  5. Save to output path only
- Do **not** change full-bleed geometry for `none`.
- For medavis output, ignore `--aspect-ratio` (template is 16:9). Still honor `--aspect-ratio` for `none`.
- **Assumption:** medavis mode is for **16:9** generated slide images (skill default). Do not silently letterbox/crop for 4:3 in v1; docs must state the assumption.

**Step 2: Run unit tests — expect PASS**

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_assemble_ppt -v
```

Expected: all PASS.

**Step 3: Manual smoke (MANDATORY if deck images exist)**

If `tests/smoke-deck/runs/20260812-1406-cursor-interactive/coffee-extraction/origin_image/slide_01.png` (or any complete deck) exists, assemble it:

```bash
# adjust python to runtime venv if needed
python skills/codex-ppt/scripts/assemble_ppt.py \
  tests/smoke-deck/runs/20260812-1406-cursor-interactive \
  coffee-extraction.pptx \
  --template both \
  --landing-title "Coffee Extraction"
```

Open `{deck}-medavis.pptx` and visually confirm **all** of:

1. medavis logo visible in the header (not covered)
2. no layout ghost text (“Edit title…”, “Insert title here”) showing on content slides
3. images fill the white area under the header
4. landing title readable in medavis blue, not duplicated with “Insert title here”
5. notes present on content slides

If visual box is wrong, adjust `MEDAVIS_CONTENT_*` constants only; re-run tests + smoke. Record a one-line result in the final report (or in GREEN evidence). If no deck images exist, note that smoke was skipped and rely on unit tests.

---

### Task 4: Skill docs GREEN — assembly workflow + SKILL pointers

**Step 0: Discover every doc that mentions assembly**

```bash
rg -n "assemble_ppt|Assembly|\.pptx" skills/codex-ppt README.md README_en.md README_ko.md docs --glob '*.md' | head -n 200
```

Use the hit list to decide which user-facing files need a template-mode mention. Keep languages in sync per `AGENTS.md`.

**Files (modify as needed from the rg hit list; typical set):**
- `skills/codex-ppt/docs/project-assembly-and-reporting.md`
- `skills/codex-ppt/SKILL.md` (short pointer / gate mention if assembly steps are summarized there)
- `skills/codex-ppt/docs/workflow-gates-and-progress.md` if it lists assembly gates
- Repo docs if they describe assembly CLI: `docs/workflow.md`, `docs/en/workflow.md`, `docs/ko/workflow.md`, and any README sections that document assemble-only behavior
- `CHANGELOG.md` under `## Unreleased` → `### Features` (English). Leave `(#NN)` out until a PR exists; follow-up commit can add it per AGENTS.md
- README language versions only if they document assembly outputs / features list in a way that would otherwise be wrong

**Step 1: Insert agent-facing rules** (Appendix D)

Must teach the agent to:

1. Before assembly, ask the user: no template / medavis / both.
2. If medavis or both: suggest a landing title from `outline.md` / deck topic; ask user to confirm or edit.
3. Invoke `assemble_ppt.py` with the matching `--template` and `--landing-title`.
4. Report output path(s), including `-medavis.pptx` when applicable.
5. Defeat rationalizations in Appendix E.
6. State that medavis mode expects **16:9** slide images (skill default).

**Step 2: RED/GREEN skill pressure**

- Baseline already in Task 2 evidence (docs lacked gate).
- After doc edits, write `docs/plans/evidence/2026-08-12-medavis-template-green.md` quoting the new mandatory steps and mapping each Appendix E rationalization to the counter-instruction.

**Step 3: ASO / skill description check (lightweight)**

- Do **not** stuff a workflow summary into `SKILL.md` description frontmatter.
- If you touch frontmatter `description`, keep third-person trigger-oriented wording; otherwise leave frontmatter unchanged and only update body/docs.

---

### Task 5: Verification Summary + cleanup

**Step 1: Run full relevant tests**

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_assemble_ppt -v
```

Expected: PASS.

**Step 2: Confirm asset tracked (not gitignored)**

```bash
git check-ignore -v skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx || echo "not ignored (good)"
git status --short skills/codex-ppt/assets/templates skills/codex-ppt/scripts/assemble_ppt.py skills/codex-ppt/docs CHANGELOG.md .gitignore
```

Expected: template **not** ignored; binary + script/docs/changelog/gitignore modified. No secrets.

**Step 3: Self-check against Acceptance checklist below**

**Step 4: Report results to the user; offer code review (`requesting-code-review`). Do not commit unless asked.**

---

## Acceptance / Verification Summary

- [ ] Bundled template exists at `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx` and opens with 2 slides, 10"×5.625"
- [ ] `.gitignore` negation added; `git check-ignore` confirms template is **not** ignored
- [ ] `--template none` behavior/output name unchanged
- [ ] `--template medavis --landing-title ...` writes only `{deck}-medavis.pptx` with `1+N` slides
- [ ] `--template both --landing-title ...` writes both PPTX files
- [ ] Landing title visible on medavis slide 1 in medavis blue; layout “Insert title here” covered
- [ ] Content images sit below header (`top >= MEDAVIS_CONTENT_TOP`); logo band not covered; layout ghost text not visible on content slides
- [ ] Speaker notes map speech Slide N → content slide N
- [ ] Missing `--landing-title` for medavis/both fails closed
- [ ] Bundled template file on disk is not mutated by assembly runs
- [ ] Unit tests green; GBK encoding regression still green
- [ ] Mandatory visual smoke done when deck images exist (or explicitly skipped with reason)
- [ ] Skill/assembly docs instruct mode choice + title confirm + 16:9 assumption; RED/GREEN evidence files written
- [ ] `rg assemble_ppt` hit list used; multilingual user docs / CHANGELOG updated per AGENTS.md
- [ ] No commit unless user asked

---

## Appendix A — Template facts & placement constants

Measured from source template `medavis_ppt_template_2026_en_16-9.pptx`:

| Fact | Value |
|------|-------|
| `slide_width` | `9144000` EMU (10 in) |
| `slide_height` | `5143500` EMU (5.625 in) |
| Slide count | 2 |
| Slide 1 layout | `2_Titelfolie` (landing). Title hint on **layout**: shape `Inhaltsplatzhalter 2` at `left=-14853, top=2850965, width=9152438, height=728897`, text `Insert title here` |
| Slide 2 layout | `3_Überschrift_Untertitel_Text` (content master) |
| Logo on master | `Grafik 3` at `left=7236296, top=195486, width=1656184, height=432048` → logo band bottom ≈ `627534` EMU |
| Important | Slide-level `shapes` / `placeholders` are **empty** on both slides; chrome and placeholder text live on layouts/masters. Do **not** mutate shared layouts to set the title. |
| Ghost text risk | Content layout still has layout-level title (~`top=200944`) and body placeholders. Slide pictures paint above layout, so a full-width image from just below the logo band to the slide bottom covers them. If `CONTENT_TOP` is too large, layout title text can peek above the image — treat that as a visual-smoke failure. |
| Title color | Medavis blue used in template chrome: `#42637B` / RGB `(66, 99, 123)` |

**Recommended constants** (tune only if visual smoke fails):

```python
MEDAVIS_TEMPLATE_REL = ("assets", "templates", "medavis_ppt_template_2026_en_16-9.pptx")
# Content image box: full width, below logo band, fills to bottom (covers layout title/body)
MEDAVIS_CONTENT_LEFT = 0
MEDAVIS_CONTENT_TOP = 700000  # EMUs; must stay > ~627534 so master logo remains visible
# width = prs.slide_width
# height = prs.slide_height - MEDAVIS_CONTENT_TOP

# Landing title textbox geometry (match layout title placeholder; covers "Insert title here")
MEDAVIS_TITLE_LEFT = -14853
MEDAVIS_TITLE_TOP = 2850965
MEDAVIS_TITLE_WIDTH = 9152438
MEDAVIS_TITLE_HEIGHT = 728897
MEDAVIS_TITLE_COLOR = (0x42, 0x63, 0x7B)
```

Content-slide construction: `add_slide(prs.slides[1].slide_layout)` is enough (slide 2 has no slide-level shapes to deep-copy). First content image reuses the existing slide 2 instance.

---

## Appendix B — CLI contract

```bash
# none (default) — unchanged
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx --aspect-ratio 16:9

# medavis only
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx \
  --template medavis --landing-title "Confirmed Title Here"

# both
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx \
  --template both --landing-title "Confirmed Title Here"
```

Outputs inside `{base_dir}/{deck_name}/`:

- `none` → `{deck_name}.pptx`
- `medavis` → `{deck_name}-medavis.pptx`
- `both` → both

---

## Appendix C — Implementation sketch (guidance, not paste-blindly)

```python
def skill_root_dir() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def medavis_template_path() -> str:
    return os.path.join(skill_root_dir(), "assets", "templates",
                        "medavis_ppt_template_2026_en_16-9.pptx")


def set_medavis_landing_title(slide, title: str) -> None:
    from pptx.util import Pt
    from pptx.dml.color import RGBColor
    box = slide.shapes.add_textbox(
        MEDAVIS_TITLE_LEFT, MEDAVIS_TITLE_TOP,
        MEDAVIS_TITLE_WIDTH, MEDAVIS_TITLE_HEIGHT,
    )
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(32)
    p.font.color.rgb = RGBColor(0x42, 0x63, 0x7B)
    # Geometry must cover layout "Insert title here"; do not edit the shared layout.


def add_content_image(slide, image_path: str, prs) -> None:
    slide.shapes.add_picture(
        image_path,
        left=MEDAVIS_CONTENT_LEFT,
        top=MEDAVIS_CONTENT_TOP,
        width=prs.slide_width,
        height=prs.slide_height - MEDAVIS_CONTENT_TOP,
    )


def create_medavis_presentation(image_files, output_path, landing_title, speaker_notes=None) -> bool:
    from pptx import Presentation
    template = medavis_template_path()
    if not os.path.exists(template):
        print(f"错误：未找到 medavis 模板: {template}")
        return False
    prs = Presentation(template)
    set_medavis_landing_title(prs.slides[0], landing_title)
    content_layout = prs.slides[1].slide_layout
    speaker_notes = speaker_notes or {}
    temp_files = []
    try:
        for i, image_path in enumerate(image_files):
            slide = prs.slides[1] if i == 0 else prs.slides.add_slide(content_layout)
            compressed = compress_image_if_needed(image_path, max_size_mb=2.0)
            image_to_use = compressed or image_path
            if compressed:
                temp_files.append(compressed)
            add_content_image(slide, image_to_use, prs)
            note = speaker_notes.get(i + 1)
            if note:
                nf = slide.notes_slide.notes_text_frame
                nf.clear()
                nf.text = note
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        prs.save(output_path)
        return True
    finally:
        for t in temp_files:
            try:
                os.remove(t)
            except OSError:
                pass
```

Wire `main()` to branch on `--template` and compute:

```python
plain_out = os.path.join(ppt_project_dir, f"{ppt_name}.pptx")
medavis_out = os.path.join(ppt_project_dir, f"{ppt_name}-medavis.pptx")
```

---

## Appendix D — Doc wording to insert (English base; translate for ko / adapt zh)

Insert into `project-assembly-and-reporting.md` under **Assembly** (adapt tone to match file; Chinese file may stay Chinese — follow the file’s existing language):

```markdown
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

Do not skip the template-mode question by assuming “no template”. Do not invent a custom template path in v1 — use the bundled medavis asset only.

Medavis mode assumes the deck’s generated images are **16:9** (the skill default). Do not use medavis wrapping for a 4:3 deck in v1 without an explicit user decision to regenerate at 16:9.
```

Also show example commands from Appendix B.

---

## Appendix E — Skill pressure scenarios (RED rationalizations to defeat)

Record these as baseline failures / rationalizations, then counter them in docs:

- R1: “Assembly is unchanged — just run `assemble_ppt.py` without asking about templates.”
- R2: “User already approved the outline/sample; no need to confirm a landing title.”
- R3: “Medavis mode can overwrite `{deck_name}.pptx` instead of writing `-medavis.pptx`.”
- R4: “Full-bleed images on the template look fine; covering the logo is OK.”
- R5: “If template mode is both, only one file is enough.”

GREEN docs must explicitly forbid each of the above.

---

## Appendix F — writing-skills checklist (skill deliverable)

This plan changes skill behavior docs. Executor must:

1. RED baseline evidence (Task 2/4) before relying on new instructions
2. Minimal doc/script change to defeat observed gaps
3. GREEN evidence with same pressure list
4. No workflow dump in skill description frontmatter
5. Repo verification: changelog + multilingual docs sync; do not run installers
