# Medavis 3-Page Template, Overlay Logo, and 16:9 Hard Gates Implementation Plan

> **For the implementing agent:** Follow this plan task-by-task. Complete each step, verify it works, then move to the next.

**Goal:** Update medavis assembly for the new 3-page template (landing + blank content + ending), overlay `medavis-logo-small.png` on content pages, never stretch images, refuse non-16:9 at record and assemble time, and tighten skill docs so agents generate 16:9 and ask the landing title before `assemble_ppt.py`.

**Architecture:** Add a shared `slide_image_ratio.py` helper. `record_slide_result.py` and `assemble_ppt.py` fail closed on non-16:9. Medavis loads the 3-page bundled template, replaces `<PPT-Title>` run text, clones blank slide 2 for content (full-page uniform-scale picture + logo overlay), and keeps the ending page last. Skill/worker docs mandate `GenerateImage aspect_ratio=16:9` and `codex-gpt-image`/`image_gen.py --size 2560x1440`. Empirical probes this session lock actual pixel sizes.

**Tech Stack:** Python 3, `python-pptx`, Pillow, stdlib `unittest`, Markdown skill/docs (zh/en/ko), Cursor `GenerateImage`, `codex-gpt-image` CLI.

---

> **SELF-CONTAINED HANDOFF PLAN.** The executor needs no prior chat session or memory file and must not ask the user to re-explain context. All task context lives in this plan (and its appendices). Normal session-start rules still apply, but you may start fresh and rely on this document.

## Section 0: Full Context

### 0.1 Why / background

v1 medavis wrap assumed a 2-page template (landing + header-band content). The user replaced the bundled PPTX with a 3-page file: landing with a preformatted `<PPT-Title>` placeholder, a **blank** page 2 meant for full-page content, and a fixed ending page. They also added `medavis-logo-small.png` to overlay top-right on content pages (separate picture, not composited).

The last interactive smoke stretched images because (1) Cursor `GenerateImage` was called without `aspect_ratio=16:9` and returned **1536×1024 (3:2)**, and (2) `assemble_ppt.py` sets picture `width=slide_width` and `height=slide_height` independently. The user forbids that distortion for both medavis and no-template output.

The landing-title question belongs **immediately before** `assemble_ppt.py`, never after the PPTX exists. Current skill already says “before assembly,” but it is easy to skip or to ask after writing the file. Tighten the wording.

### 0.2 Confirmed decisions (do not re-litigate)

1. **3-page template:** slide 1 landing, slide 2 blank content master, slide 3 ending. Clone/reuse page 2 for every content image. Ending stays last, unmodified (no content image, no small logo, no `speech.md` notes).
2. **Title:** replace text in the existing shape whose text contains `<PPT-Title>`. Keep font weight and center alignment. Do **not** add a second title textbox. Do **not** use the old `MEDAVIS_TITLE_*` geometry/color constants.
3. **Logo overlay:** `skills/codex-ppt/assets/templates/medavis-logo-small.png` only (not `medavis-logo-original.png`). Separate `add_picture` on content pages after the content image. Top-right, **10px equal top and right margin** (10px at 96 dpi = **95250 EMU**). Native size from PNG pixels and 300 DPI: 447×90 → **1362456 × 274320 EMU**.
4. **No stretch:** never set picture width and height independently to the slide box. After a 16:9 gate passes, place with **one uniform scale** (contain). For exact 16:9 this fills the page.
5. **Hard 16:9 gate:** **2% relative** — `|width/height - 16/9| <= 0.02 * (16/9)` (≈ 0.0356 absolute). Equivalent: `|w/h / (16/9) - 1| <= 0.02`. 3:2 (`1.50`, ~16% off) must fail. 1792×1024 (`1.75`) may pass. Agent regenerates on fail. `record_slide_result.py` refuses to copy. `assemble_ppt.py` refuses to place. **No letterbox success path. No crop.** If a live 16:9 backend probe lands outside this window, STOP and ask — do not widen silently.
6. **Generation:** Cursor `GenerateImage` **must** pass `aspect_ratio="16:9"`. `codex-gpt-image` and `scripts/image_gen.py` **must** pass `--size 2560x1440` (exact 16:9; gpt-image-2 allows WIDTHxHEIGHT with multiples of 16). Write this as a hard rule in SKILL.md, worker prompt, and slide-generation docs.
7. **Empirical probes (this work):** generate one real image with Cursor GenerateImage 16:9 and one with `codex-gpt-image --size 2560x1440`. Record actual WxH. If a probe is **not** within the 2% relative 16:9 window, **STOP and ask the user** — do not weaken the gate and do not claim the backend works.
8. **Title timing:** keep the question at assembly (template mode + suggested title), then run `assemble_ppt.py`. Forbidden: writing the PPTX first, then asking for the title.
9. **CLI unchanged:** `--template none|medavis|both`, `--landing-title` required for medavis/both, outputs `{deck}.pptx` and/or `{deck}-medavis.pptx`.
10. **Approach:** shared ratio helper + fail-closed at record **and** assemble (not assemble-only; not PNG padding).

**Rejected alternatives (do not reopen):**
- Letterbox as the success path
- Cover/crop
- Size no-template slides to each image’s native ratio (would make “both” mode two geometries)
- Add a new title textbox (v1 behavior)
- Header-band content (`MEDAVIS_CONTENT_TOP=700000`)
- Using `medavis-logo-original.png`
- Asking the landing title after the PPTX exists

### 0.3 Audience & assumptions

- Repo root: `D:/git/codex-ppt-skill`
- Edit `skills/codex-ppt/` plus repo docs/CHANGELOG/`.gitignore`/tests. Do **not** run collection install/uninstall scripts. Do **not** commit unless the user explicitly asks.
- The user already replaced `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx` (3 slides) and added the PNG logos. Do not copy from `D:\temp\...` unless the bundled file is missing.
- Python: run tests from `skills/codex-ppt/scripts` with `python -m unittest ...`. Shared runtime may be `~/.codex-ppt-skill/.venv`. If imports fail: `python skills/codex-ppt/scripts/codex_ppt_runtime.py bootstrap`.
- Cursor `GenerateImage` is available in this IDE. `codex-gpt-image` CLI lives at `C:/Users/raymond.shen/.cursor/skills/codex-gpt-image/scripts/codex_gpt_image.py` (or the user’s equivalent skill install). Check `auth-status` first.
- Old smoke deck `tests/smoke-deck/runs/20260812-1725-cursor-interactive/coffee-extraction/origin_image/*.png` is **3:2**. It must **fail** the new assemble gate. Do not “fix” that by stretching. Do not treat that run as a GREEN visual for the new assembler.

### 0.4 Project rules / conventions to honor

- `AGENTS.md`: changelog under `## Unreleased` in English; documentation changes update **all** language versions (`README.md`, `README_en.md`, `README_ko.md`, `docs/`, `docs/en/`, `docs/ko/`).
- Conventional Commits only if/when the user requests a commit. Task prefix `[SQ5GEN-195]` was used previously; ask if unknown.
- YAGNI: no generic template registry, no custom template path, no image compositing.
- TDD for scripts. Skill-doc changes need RED/GREEN pressure evidence (Appendix E).
- `writing-skills` for SKILL.md edits: do not change the skill `name`; keep description trigger-quality (third person, no workflow dump); add 16:9 / GenerateImage keywords only if they still fit the description length; detailed rules go in the body and `docs/`, not the YAML description.
- Verification before claiming done: run commands and read output.

### 0.5 Formats & reference material

See **Appendix A** (template + logo geometry), **Appendix B** (ratio helper + placement), **Appendix C** (implementation sketch), **Appendix D** (doc wording), **Appendix E** (skill pressure scenarios).

### 0.6 Hard guardrails

- Do **not** restore `MEDAVIS_CONTENT_TOP` header-band placement.
- Do **not** add a second landing title textbox.
- Do **not** independently set picture width and height to the slide box to “make it fit.”
- Do **not** overwrite the bundled template file.
- Do **not** put content images or the small logo on the ending page.
- Do **not** commit unless asked. Do not run install/uninstall scripts.

### 0.7 Plan revision (critical review, 2026-08-13)

Patches from `think-mcp` review — **do not skip**:

1. **`--aspect-ratio 4:3` (none mode):** Fail-closed against the **requested canvas ratio**, not always 16:9. Default none and all medavis: require 16:9 images (2% relative). `--aspect-ratio 4:3`: require 4:3 images with the same 2% relative window, then uniform-scale into the 4:3 slide. Do not stretch; do not letterbox as a success path. Medavis still ignores `--aspect-ratio` and always requires 16:9 images.
2. **`add_slide` object:** Keep the `Slide` returned by `add_slide`, reorder XML, then `add_picture` on **that same object**. Do not re-fetch `prs.slides[1+i]` to add shapes (stale-index footgun).
3. **GenerateImage probe is host-conditional:** If `GenerateImage` is not a callable tool in the executor session, record that in the probe evidence and **ask the user** — do not invent pixel sizes. Still run the `codex-gpt-image` probe when auth works.
4. **`record_slide_result` fixture:** Write a real `slide_jobs.json` on disk (file must exist for `locked_jobs`). Minimal dispatched slide + `selected_backend` matching `--backend-used`. Copy field names from `slide_run_state.find_slide` / `record_slide_result.main` — do not guess extra keys.
5. **Title tests:** Do **not** revive `MEDAVIS_TITLE_COLOR` / `MEDAVIS_TITLE_*` geometry asserts. Assert `<PPT-Title>` is gone and the confirmed title string is present. If `paragraph.alignment` is `None`, skip alignment assert.
6. **Picture size asserts:** Prefer `abs((pic.width/pic.height)/(16/9) - 1) <= 0.02` and `pic.left == 0` over `pic.height == slide_height` (integer rounding).
7. **gitignore:** `!*.png` will also un-ignore `medavis-logo-original.png`. That is OK (asset sits in the folder) but it is **not used** by assemble. Do not reference it in code.
8. **FAST / old smoke runs:** `verify_deck` 16:9 baseline will fail 3:2 decks. Document that in `tests/smoke-deck/README.md`. Do not weaken the gate to keep old runs green.
9. **Near-miss 16:9 vs letterbox:** Images inside the 2% relative window (e.g. 1792×1024) still use **uniform scale**. A sub-2% empty strip is leftover from a near-miss ratio, not a success path for 3:2. Do **not** independently set width and height to hide those strips.
10. **`image_gen.py` already defaults to `2560x1440`.** Skill/CLI text must still say to pass `--size 2560x1440` explicitly so agents do not pick legacy `1536x1024`. Do not change the script default in this work unless a probe proves it is wrong.
11. **Third review (2026-08-13):** no new Important/Critical items. Known residuals only: `prs.slides._sldIdLst` private API (caught by ending-last tests), placeholder run-formatting (do not revive v1 color asserts), GenerateImage host-conditional.

---

### Task 1: Un-ignore logo PNG and confirm the 3-page template

**Files:**
- Modify: `.gitignore`
- Confirm present: `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx`
- Confirm present: `skills/codex-ppt/assets/templates/medavis-logo-small.png`
- Modify: `skills/codex-ppt/assets/templates/README.md`

**Step 1: Add gitignore negation for template PNGs**

Root `.gitignore` already has:

```gitignore
!skills/codex-ppt/assets/templates/
!skills/codex-ppt/assets/templates/*.pptx
```

After those lines add:

```gitignore
!skills/codex-ppt/assets/templates/*.png
```

**Step 2: Verify tracking**

```bash
git check-ignore -v skills/codex-ppt/assets/templates/medavis-logo-small.png || echo "not ignored (good)"
git check-ignore -v skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx || echo "not ignored (good)"
```

Expected: neither path is ignored (or the last matching rule is the `!` negation).

**Step 3: Confirm template facts**

```bash
python - <<'PY'
from pptx import Presentation
p = Presentation("skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx")
assert len(p.slides) == 3, len(p.slides)
assert p.slide_width == 9144000 and p.slide_height == 5143500
texts = []
for sh in p.slides[0].shapes:
    if sh.has_text_frame:
        texts.append(sh.text_frame.text)
assert any("<PPT-Title>" in t for t in texts), texts
assert len(p.slides[1].shapes) == 0
print("template ok")
PY
```

Expected: `template ok`. If slide count is not 3, **stop**.

**Step 4: README one-liner**

Update `skills/codex-ppt/assets/templates/README.md` to mention: 3-page medavis 16:9 template (landing / blank content / ending) plus `medavis-logo-small.png` overlay asset. Do not edit the binaries casually.

---

### Task 2: RED — ratio helper tests (write first, watch fail)

**Files:**
- Create: `skills/codex-ppt/scripts/tests/test_slide_image_ratio.py`
- Create later: `skills/codex-ppt/scripts/slide_image_ratio.py` (not yet)

**Step 1: Write failing tests**

```python
#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from PIL import Image


class SlideImageRatioTests(unittest.TestCase):
    def test_16_9_fixture_passes(self) -> None:
        import slide_image_ratio as r

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "ok.png"
            Image.new("RGB", (32, 18), color="white").save(path)
            self.assertTrue(r.is_16_9_image(str(path)))
            self.assertEqual(r.require_16_9_image(str(path)), (32, 18))

    def test_3_2_fixture_fails(self) -> None:
        import slide_image_ratio as r

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.png"
            Image.new("RGB", (1536, 1024), color="white").save(path)
            self.assertFalse(r.is_16_9_image(str(path)))
            with self.assertRaises(ValueError) as cm:
                r.require_16_9_image(str(path))
            self.assertIn("1536", str(cm.exception))
            self.assertIn("1024", str(cm.exception))

    def test_tolerance_rejects_far_ratios(self) -> None:
        import slide_image_ratio as r

        self.assertTrue(r.is_16_9(2560, 1440))
        self.assertTrue(r.is_16_9(1792, 1024))  # 1.75 is within 2% relative of 16/9
        self.assertFalse(r.is_16_9(1536, 1024))  # 3:2


if __name__ == "__main__":
    unittest.main()
```

**Step 2: Run to verify RED**

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_slide_image_ratio -v
```

Expected: FAIL (`ModuleNotFoundError: slide_image_ratio` or missing functions).

**Step 3: Record RED evidence**

Create `docs/plans/evidence/2026-08-13-medavis-v2-red.md` with the failing command output (abbreviated) and the predicted skill rationalizations from Appendix E.

---

### Task 3: GREEN — implement `slide_image_ratio.py`

**Files:**
- Create: `skills/codex-ppt/scripts/slide_image_ratio.py`

**Step 1: Minimal implementation** (Appendix B). Do not add CLI.

**Step 2: Re-run tests**

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_slide_image_ratio -v
```

Expected: PASS.

---

### Task 4: RED — assemble_ppt tests for 3-page wrap, no-stretch, refuse 3:2

**Files:**
- Modify: `skills/codex-ppt/scripts/tests/test_assemble_ppt.py`

**Step 1: Keep `_make_deck` 16:9 fixtures (`32x18`). Add a helper for 3:2 decks.**

```python
def _make_deck_ratio(tmp: str, size: tuple[int, int], name: str = "demo-deck", slides: int = 2, with_notes: bool = False) -> Path:
    from PIL import Image
    deck_dir = Path(tmp) / name
    origin = deck_dir / "origin_image"
    origin.mkdir(parents=True)
    for i in range(1, slides + 1):
        Image.new("RGB", size, color=(i * 40, 80, 120)).save(origin / f"slide_{i:02d}.png")
    if with_notes:
        lines = []
        for i in range(1, slides + 1):
            lines.append(f"## Slide {i}: S{i}\n\nNote for slide {i}.\n")
        (deck_dir / "speech.md").write_text("\n".join(lines), encoding="utf-8")
    return deck_dir
```

Keep `_make_deck(...)` as a wrapper around `_make_deck_ratio(..., (32, 18), ...)`.

**Step 2: Change existing assertions that encode v1 geometry**

| Test | Old assertion | New assertion |
|---|---|---|
| `test_medavis_writes_suffix_file_only` | `len(slides)==3` | `len(slides)==4` (landing + 2 content + ending) |
| `test_medavis_landing_title_and_color` | `MEDAVIS_TITLE_*` + RGB constant | landing text contains `"Demo Title"` and does **not** contain `"<PPT-Title>"`; first matching paragraph `alignment` is center if exposed |
| `test_medavis_content_image_placement` | `pic.top >= 700000`, `pic.top != 0` | content picture `left==0`, `top==0`, `width==slide_width`; `abs((pic.width/pic.height)/(16/9) - 1) <= 0.02`; second picture is the logo (see Appendix A) |
| `test_medavis_notes_mapping` | notes on slides 1 and 2 | landing notes empty; content slides `[1]` and `[2]` have notes; **last** slide notes empty |

**Step 3: Add new tests**

- `test_none_refuses_3_2_image` — `_make_deck_ratio(..., (1536, 1024))`, `--template none`, exit != 0, no pptx.
- `test_medavis_refuses_3_2_image` — same for medavis.
- `test_none_16_9_picture_is_uniform_full_page` — pic left/top 0; `pic.width == prs.slide_width`; `abs((pic.width/pic.height)/(16/9) - 1) <= 0.02`.
- `test_medavis_ending_stays_last` — last slide has 4 shapes (template ending); no full-slide content picture with `top==0` and `width==slide_width` **and** a small logo overlay. Simpler: last slide text still contains `"Thank You"` / `"Vielen Dank"`; logo overlay count on last slide is 0 of the small-logo size.
- `test_medavis_logo_geometry` — on each content slide, a picture with `top == MEDAVIS_LOGO_MARGIN_EMU` and `left + width == slide_width - MEDAVIS_LOGO_MARGIN_EMU` (tolerance 2 EMU).
- Keep `test_medavis_does_not_mutate_bundled_template`.
- Keep landing-title required tests.
- `test_none_16_9_image_rejected_for_aspect_4_3` — 32×18 fixture + `--template none --aspect-ratio 4:3` exits non-zero.
- `test_none_4_3_image_accepted_for_aspect_4_3` — 32×24 fixture + `--template none --aspect-ratio 4:3` exits 0; picture uses uniform scale (ratio matches 4:3, not independent full-bleed stretch of a 16:9 image).

**Step 4: Run RED**

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_assemble_ppt -v
```

Expected: FAIL on slide count / title constants / header-band placement / new refuse tests (assemble still stretches and uses 2-page logic). Append failures to the RED evidence file.

Do **not** implement assemble changes until this RED run is recorded.

---

### Task 5: GREEN — rewrite medavis/none placement in `assemble_ppt.py`

**Files:**
- Modify: `skills/codex-ppt/scripts/assemble_ppt.py`

**Step 1: Remove v1 constants** `MEDAVIS_CONTENT_*`, `MEDAVIS_LOGO_BAND_BOTTOM`, `MEDAVIS_TITLE_*`.

**Step 2: Import helper and add logo constants** from Appendix A/B.

**Step 3: Implement functions** from Appendix C:

- `uniform_picture_box(image_w, image_h, box_w, box_h)` → `(left, top, width, height)` using min scale, centered. After `require_16_9_image`, the box is the full slide, so this fills a true 16:9 image.
- `set_medavis_landing_title(slide, title)` — find `<PPT-Title>`, replace **run text** (do not assign `paragraph.text`, which wipes formatting).
- `add_content_picture(slide, image_path, prs)` — `require_16_9_image`; `add_picture` with uniform box.
- `add_medavis_logo(slide, prs)` — overlay small logo.
- `move_slide(prs, old_index, new_index)` — reorder `prs.slides._sldIdLst`.
- `create_medavis_presentation` — require `len(prs.slides)==3`; set title; for i, image: if i==0 use slides[1] else `add_slide(blank_layout)` then `move_slide` so new slide is at index `1+i` (before ending); add picture + logo + notes; never save onto the template path.
- `create_presentation` (none) — `require_image_ratio` against the **requested** `--aspect-ratio` (16:9 default, or 4:3). Then `uniform_picture_box` into that canvas. Medavis always `require_16_9_image` and ignores `--aspect-ratio`. Add one unit test: 16:9 fixture + `--aspect-ratio 4:3` exits non-zero (ratio mismatch). Another: 4:3 fixture `(32, 24)` + `--aspect-ratio 4:3` succeeds without independent width/height stretch.

**Step 4: Run tests**

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_slide_image_ratio tests.test_assemble_ppt -v
```

Expected: PASS.

**Step 5: Prove old 3:2 smoke images fail closed**

```bash
python skills/codex-ppt/scripts/assemble_ppt.py \
  tests/smoke-deck/runs/20260812-1725-cursor-interactive \
  coffee-extraction.pptx --template none
```

Expected: non-zero exit, message includes `1536`/`1024` or ratio, **no** overwrite of a “fixed” stretched pptx as success. Record this as GREEN-for-the-gate in the evidence file.

---

### Task 6: `record_slide_result.py` 16:9 gate

**Files:**
- Modify: `skills/codex-ppt/scripts/record_slide_result.py`
- Create: `skills/codex-ppt/scripts/tests/test_record_slide_result_ratio.py`

There is **no** existing `record_slide_result` unit test file. Add a focused test that calls `require_16_9_image` through a tiny wrapper or by invoking `main` with a temp deck.

**Minimal jobs fixture** (write under tempfile):

```json
{
  "selected_backend": "GenerateImage",
  "slides": [
    {
      "slide_id": "slide_01",
      "status": "dispatched",
      "out": "origin_image/slide_01.png",
      "dispatch": {"agent_id": "t1"}
    }
  ]
}
```

**RED:** 3:2 source PNG → `main` SystemExit before copy; target must not exist.

**GREEN:** 32×18 PNG → copy succeeds.

Insert the ratio check in `main` **after** `source = ensure_file(...)` and **before** `shutil.copy2`.

```python
from slide_image_ratio import require_16_9_image

try:
    require_16_9_image(str(source))
except ValueError as exc:
    raise SystemExit(str(exc)) from exc
```

Run:

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_record_slide_result_ratio -v
```

Expected after implementation: PASS.

---

### Task 7: Empirical 16:9 probes (GenerateImage + codex-gpt-image)

**Files:**
- Create: `docs/plans/evidence/2026-08-13-medavis-v2-backend-probes.md`
- Do **not** commit generated probe PNGs.

**Step 1: Cursor GenerateImage**

If `GenerateImage` is **not** in the callable tool list (e.g. Codex/Claude handoff session), write that fact into the probe evidence file and **ask the user** before continuing. Do not invent WxH.

If it is callable, call `GenerateImage` with:

- `description`: a simple solid-color 16:9 slide saying `RATIO-PROBE` (no medavis branding needed)
- `aspect_ratio`: `"16:9"`
- `filename`: `ratio-probe-generateimage.png`

Then:

```bash
python - <<'PY'
from PIL import Image
im = Image.open("ratio-probe-generateimage.png")  # resolve actual tool output path
print(im.size, round(im.size[0]/im.size[1], 6))
PY
```

Record WxH and ratio. Assert `|ratio/(16/9) - 1| <= 0.02`. If it fails, **STOP and ask the user**.

**Step 2: codex-gpt-image**

```bash
python "C:/Users/raymond.shen/.cursor/skills/codex-gpt-image/scripts/codex_gpt_image.py" auth-status
```

If auth is missing, **STOP and ask** (do not skip). If ok:

```bash
python "C:/Users/raymond.shen/.cursor/skills/codex-gpt-image/scripts/codex_gpt_image.py" generate \
  --prompt "Solid white 16:9 slide with the text RATIO-PROBE-CODEX centered, no extra decoration" \
  --size 2560x1440 \
  --output-format png \
  --out ratio-probe-codex-gpt-image.png
```

(Use the CLI’s actual output-path flags from `codex_gpt_image.py -h` if names differ.)

Measure WxH. Must be 16:9 within 2% relative (expect **2560×1440**). If not, **STOP and ask**.

**Step 3: Lock skill size strings**

If GenerateImage’s actual pixels are e.g. 1920×1080 or 1536×864 (still 16:9), document that in the evidence file and in skill text: “pass `aspect_ratio=16:9`; accept whatever pixel size the tool returns **only if** the ratio check passes.” Do not require 2560×1440 from GenerateImage. Do require `--size 2560x1440` for the bridge/CLI.

---

### Task 8: `verify_deck.py` + smoke tests

**Files:**
- Modify: `tests/smoke-deck/verify_deck.py`
- Modify: `tests/smoke-deck/test_verify_deck_backends.py`
- Modify: `tests/smoke-deck/README.md` and GATED `RUN_PROMPT_*.md` (not FAST `RUN_PROMPT.md` beyond a one-line 16:9 note if it mentions assembly)

**Changes to `check_medavis_pptx`:**

- Expected slide count: `1 + SLIDE_COUNT + 1` (landing + N content + ending).
- Landing: has title text, **not** `<PPT-Title>`, empty notes.
- Content slides: indices `1 .. SLIDE_COUNT` (not including last). Full-page content picture `top==0` (or uniform-scale near 0); overlay logo picture with `top` ≈ 95250.
- Last slide: ending; empty notes; do **not** require a full-page generated content image.
- Delete `MEDAVIS_CONTENT_TOP_MIN` header-band check.

**Changes to `check_images`:**

- Promote 16:9 from INFO flag to a **baseline** failure when `|ratio/(16/9) - 1| > 0.02`.

**Update `test_medavis_checks_pass_on_assembled_deck`** so it still passes with the new assembler (32×18 fixtures).

Run:

```bash
python -m unittest tests.smoke-deck.test_verify_deck_backends
# if that import path fails:
cd tests/smoke-deck && python -m unittest test_verify_deck_backends -v
```

Expected: PASS.

Do **not** run `verify_deck.py` against the old 3:2 interactive run expecting BASELINE PASSED.

---

### Task 9: Skill RED / GREEN (writing-skills)

**Files:**
- Modify: `skills/codex-ppt/SKILL.md`
- Modify: `skills/codex-ppt/prompts/slide-worker.md`
- Modify: `skills/codex-ppt/docs/slide-generation-and-subagents.md`
- Modify: `skills/codex-ppt/docs/project-assembly-and-reporting.md`
- Modify: `skills/codex-ppt/docs/cli-api-fallback.md`
- Modify: `skills/codex-ppt/docs/backend-selection.md` if it mentions size/ratio
- Evidence: `docs/plans/evidence/2026-08-13-medavis-v2-skill-red.md` and `-skill-green.md`

**RED (before editing skill body):**

Table-top is enough: quote current SKILL.md / worker prompt gaps that allow the Appendix E rationalizations. Do not change YAML `name`. Description may stay as-is unless you add a short 16:9 phrase without turning it into a workflow dump.

**GREEN skill wording (must appear, once each, in the owning file — do not duplicate long procedures):**

SKILL.md Hard Constraints (new bullets):

- Every final slide image **must** be 16:9. Cursor `GenerateImage` calls **must** set `aspect_ratio` to `16:9`. `codex-gpt-image` and `scripts/image_gen.py` **must** pass `--size 2560x1440`. After the file is saved, verify pixel ratio `|w/h / (16/9) - 1| <= 0.02` (or run `record_slide_result.py`, which refuses otherwise). If the ratio is wrong, regenerate — do not assemble. Do not stretch, letterbox, or crop to “fix” it.
- Template mode + landing title: ask **immediately before** `assemble_ppt.py`. Do not write the PPTX first. Do not skip the question. Do not ask after the file exists.

SKILL.md Stage 11: keep ask-then-assemble order; add “then run assemble_ppt.py in the same step; the PPTX must not exist yet as the output of this run.”

`prompts/slide-worker.md`: add a hard-rules line: locked backend must emit 16:9 (`GenerateImage` `aspect_ratio=16:9` or CLI `--size 2560x1440`). Return a blocker if the tool cannot.

`docs/slide-generation-and-subagents.md`: same 16:9 rule next to the existing `"aspect_ratio": "16:9"` JSON example; state that the JSON field is **not enough** — the actual tool call must pass the flag.

`docs/project-assembly-and-reporting.md`: replace header-band placement with: landing title via `<PPT-Title>` replacement; content = blank page 2 full-page image + overlay logo; ending last; slide count `N+2`; `assemble_ppt.py` refuses non-16:9.

**VERIFY GREEN:** Re-read the same Appendix E scenarios against the new text. Each rationalization must have an explicit counter. Record in the GREEN evidence file.

**ASO checks:** skill name `codex-ppt` unchanged; description still third-person trigger; no new workflow essay in YAML.

---

### Task 10: Multilingual docs + CHANGELOG

**Step 1:** Discover remaining mentions:

```bash
rg -n "header band|logo band|MEDAVIS_CONTENT|landing \\+ content|assemble_ppt|--template|landing-title|<PPT-Title>" \
  README.md README_en.md README_ko.md docs docs/en docs/ko \
  skills/codex-ppt tests/smoke-deck CHANGELOG.md
```

Update **every** language version that describes assembly/template/slide count.

**Step 2: CHANGELOG.md `## Unreleased`**

- Features or Improvements: 3-page medavis wrap, overlay logo, 16:9 hard gates.
- Fixes: do not stretch images to the slide; replace `<PPT-Title>` instead of adding a box.
- Do not add a PR number until a PR exists.

**Step 3: Smoke GATED prompts** still prefer **both** + confirm landing title **then** assemble. Add: GenerateImage `aspect_ratio=16:9`; verifier expects `N+2` slides.

---

### Task 11: GREEN evidence + visual check

**Files:**
- Create: `docs/plans/evidence/2026-08-13-medavis-v2-green.md`

Include:

- unittest commands + PASS
- 3:2 smoke assemble FAIL (gate)
- backend probe WxH
- A **16:9 fixture** assemble (temp deck, 2 slides) opened via python-pptx assertions already in unit tests. Optional: if PowerPoint COM preview is easy on this machine, export landing/content/ending screenshots; otherwise unit tests + python-pptx dump of shapes is enough. Do not claim visual QA you did not look at.

---

## Verification Summary

Executor may claim done only when **all** are true:

- [ ] `git check-ignore` does not ignore `medavis-logo-small.png`
- [ ] Bundled template still 3 slides; file not mutated by assemble
- [ ] `python -m unittest tests.test_slide_image_ratio tests.test_assemble_ppt tests.test_record_slide_result_ratio -v` PASS (from `skills/codex-ppt/scripts`)
- [ ] smoke `test_verify_deck_backends` PASS
- [ ] 3:2 image: assemble and record_slide_result both non-zero
- [ ] 16:9 image: none pptx full-page uniform; medavis pptx = landing + N content + ending; title replaced; logo top-right; ending last
- [ ] GenerateImage 16:9 probe and codex-gpt-image 2560x1440 probe recorded; both within 2% relative of 16:9 (or user was asked)
- [ ] SKILL/worker/docs forbid missing aspect_ratio, stretching, and asking title after PPTX
- [ ] zh/en/ko docs + CHANGELOG updated
- [ ] No commit unless the user asked

---

## Appendix A — Template and logo geometry (measured 2026-08-13)

| Item | Value |
|---|---|
| Template path | `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx` |
| Slide size | 9144000 × 5143500 EMU (exact 16:9) |
| Slide 1 | layout `2_Titelfolie`; placeholder text `<PPT-Title>` (shape name may be `Inhaltsplatzhalter 3`, **match by text not name**) |
| Slide 2 | layout `Blank`; **0 shapes** |
| Slide 3 | ending; pictures + “Thank You For Your Patience” / “Vielen Dank für Ihre Geduld” |
| Logo file | `skills/codex-ppt/assets/templates/medavis-logo-small.png` |
| Logo pixels | 447 × 90, RGBA, 300 DPI |
| Logo EMU | `int(447/300*914400)=1362456` × `int(90/300*914400)=274320` |
| Margin | 10 px at 96 dpi = `int(10/96*914400)=95250` EMU |
| Logo left | `slide_width - logo_w - 95250` |
| Logo top | `95250` |

```python
EMU_PER_INCH = 914400
MEDAVIS_LOGO_MARGIN_EMU = 95250
MEDAVIS_LOGO_WIDTH_EMU = 1362456
MEDAVIS_LOGO_HEIGHT_EMU = 274320
PPT_TITLE_TOKEN = "<PPT-Title>"
RATIO_16_9 = 16 / 9
RATIO_RELATIVE_TOLERANCE = 0.02  # 2% relative
```

---

## Appendix B — Ratio helper

```python
# skills/codex-ppt/scripts/slide_image_ratio.py
from __future__ import annotations

RATIO_16_9 = 16 / 9
RATIO_4_3 = 4 / 3
RATIO_RELATIVE_TOLERANCE = 0.02  # 2% relative: |ratio/expected - 1| <= 0.02


def is_ratio(width: int, height: int, expected: float, relative_tolerance: float = RATIO_RELATIVE_TOLERANCE) -> bool:
    if height <= 0 or width <= 0 or expected <= 0:
        return False
    return abs((width / height) / expected - 1.0) <= relative_tolerance


def is_16_9(width: int, height: int, relative_tolerance: float = RATIO_RELATIVE_TOLERANCE) -> bool:
    return is_ratio(width, height, RATIO_16_9, relative_tolerance)


def image_size(path: str) -> tuple[int, int]:
    from PIL import Image

    with Image.open(path) as im:
        return im.size


def is_16_9_image(path: str, relative_tolerance: float = RATIO_RELATIVE_TOLERANCE) -> bool:
    width, height = image_size(path)
    return is_16_9(width, height, relative_tolerance)


def require_16_9_image(path: str, relative_tolerance: float = RATIO_RELATIVE_TOLERANCE) -> tuple[int, int]:
    return require_image_ratio(path, RATIO_16_9, "16:9", relative_tolerance)


def require_image_ratio(
    path: str,
    expected: float,
    label: str,
    relative_tolerance: float = RATIO_RELATIVE_TOLERANCE,
) -> tuple[int, int]:
    width, height = image_size(path)
    if not is_ratio(width, height, expected, relative_tolerance):
        ratio = (width / height) if height else 0.0
        raise ValueError(
            f"Slide image must be {label} (2% relative): {path} is {width}x{height} "
            f"(ratio {ratio:.4f}, expected {expected:.4f}). Do not stretch."
        )
    return width, height


def uniform_picture_box(
    image_w: int, image_h: int, box_w: int, box_h: int
) -> tuple[int, int, int, int]:
    """Contain-scale into box; centered. Do not set width and height independently."""
    scale = min(box_w / image_w, box_h / image_h)
    width = int(image_w * scale)
    height = int(image_h * scale)
    left = (box_w - width) // 2
    top = (box_h - height) // 2
    return left, top, width, height
```

---

## Appendix C — Assembly sketch

```python
def set_medavis_landing_title(slide, title: str) -> None:
    for shape in slide.shapes:
        if not getattr(shape, "has_text_frame", False):
            continue
        text = shape.text_frame.text or ""
        if PPT_TITLE_TOKEN not in text:
            continue
        replaced = False
        for paragraph in shape.text_frame.paragraphs:
            runs = paragraph.runs
            if not runs:
                continue
            if not replaced:
                runs[0].text = title
                replaced = True
                for extra in runs[1:]:
                    extra.text = ""
            else:
                for run in runs:
                    run.text = ""
        if not replaced:
            shape.text_frame.paragraphs[0].text = title  # last resort
        return
    raise RuntimeError("medavis landing page is missing the <PPT-Title> placeholder")


def move_slide(prs, old_index: int, new_index: int) -> None:
    sld_id_lst = prs.slides._sldIdLst
    elements = list(sld_id_lst)
    el = elements[old_index]
    sld_id_lst.remove(el)
    sld_id_lst.insert(new_index, el)


def add_content_picture(slide, image_path: str, prs) -> None:
    from slide_image_ratio import require_16_9_image, uniform_picture_box

    img_w, img_h = require_16_9_image(image_path)
    left, top, width, height = uniform_picture_box(
        img_w, img_h, int(prs.slide_width), int(prs.slide_height)
    )
    slide.shapes.add_picture(image_path, left, top, width, height)


def add_medavis_logo(slide, prs) -> None:
    logo = os.path.join(skill_root_dir(), "assets", "templates", "medavis-logo-small.png")
    if not os.path.exists(logo):
        raise FileNotFoundError(logo)
    left = int(prs.slide_width) - MEDAVIS_LOGO_WIDTH_EMU - MEDAVIS_LOGO_MARGIN_EMU
    top = MEDAVIS_LOGO_MARGIN_EMU
    slide.shapes.add_picture(
        logo, left, top, MEDAVIS_LOGO_WIDTH_EMU, MEDAVIS_LOGO_HEIGHT_EMU
    )
```

Content loop:

```python
prs = Presentation(template)
if len(prs.slides) != 3:
    print("错误：medavis 模板必须是 3 页（落地页 + 空白内容页 + 结束页）")
    return False
set_medavis_landing_title(prs.slides[0], landing_title)
blank_layout = prs.slides[1].slide_layout
for i, image_path in enumerate(image_files):
    if i == 0:
        slide = prs.slides[1]
    else:
        slide = prs.slides.add_slide(blank_layout)
        # add_slide appends after ending; move to index 1+i (before last)
        move_slide(prs, len(prs.slides) - 1, 1 + i)
        slide = prs.slides[1 + i]
    add_content_picture(slide, image_to_use, prs)
    add_medavis_logo(slide, prs)
    # notes: speaker_notes.get(i+1) on this content slide; do not write notes on ending
```

Keep the `Slide` object from `add_slide`. Reorder XML with `move_slide`, then add pictures on **that same object**:

```python
slide = prs.slides.add_slide(blank_layout)
move_slide(prs, len(prs.slides) - 1, 1 + i)
add_content_picture(slide, image_to_use, prs)
add_medavis_logo(slide, prs)
```

---

## Appendix D — Doc wording targets

Medavis output structure:

- Slide 1 = landing; `<PPT-Title>` replaced with the confirmed title
- Slides 2 .. N+1 = content (blank page clone); 16:9 image full page; small logo overlay top-right
- Slide N+2 = ending page from the template, unchanged
- Notes: `speech.md` Slide K → content slide K (PPT index K+1). Landing and ending notes empty

Forbidden:

- Stretching images to the slide
- Assembling non-16:9 images
- Asking the landing title after the PPTX exists
- Covering the ending page with content
- Adding a second title box

GenerateImage example (skill/worker):

```
GenerateImage(description=..., aspect_ratio="16:9")
```

Bridge/CLI:

```
python scripts/codex_gpt_image.py generate --size 2560x1440 ...
python scripts/image_gen.py ... --size 2560x1440
```

---

## Appendix E — Skill pressure scenarios

| ID | Pressure | Current likely rationalization | Required counter |
|---|---|---|---|
| R1 | Skip `aspect_ratio=16:9` on GenerateImage | “The prompt already says 16:9 full-slide” | Hard constraint: the **tool argument** must be set; prompt text is not enough. Last smoke produced 1536×1024. |
| R2 | Stretch 3:2 into 16:9 PPT | “Fill the page so there are no gaps” | assemble refuses; never set width and height independently |
| R3 | Ask title after PPTX written | “User can rename the title in PowerPoint” / “images are already the PPT” | Ask template+title, **then** run assemble_ppt.py; PPTX of this run must not exist yet |
| R4 | Add a new title textbox | v1 code path | Replace `<PPT-Title>` run text only |
| R5 | Content slides after ending | `add_slide` appends | Reorder so ending stays last |
| R6 | Pad/letterbox to sneak 3:2 through | “preserves ratio” | Hard fail; regenerate |
| R7 | Composite logo into the PNG | “one image is simpler” | Separate picture overlay |

RED evidence must quote current SKILL.md/worker lines that fail to block R1–R3. GREEN evidence must quote the new lines that block them.

---

**Confirmed at:** 2026-08-13 (handoff plan; do not re-litigate Section 0.2)
