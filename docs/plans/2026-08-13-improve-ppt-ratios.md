# Multi-Ratio PPT Canvases (16:9 / 4:3 / 3:2) Implementation Plan

> **For the implementing agent:** Follow this plan task-by-task. Complete each step, verify it works, then move to the next.

**Goal:** Let the user pick the final PPT ratio (16:9, 4:3, or 3:2) before backend lock; filter image backends by that ratio; assemble none-mode and matching 3-page Medavis templates without stretching; fail-closed if saved images do not match the locked ratio.

**Architecture:** One ratio-keyed pipeline. Persist `aspect_ratio` in `deck_spec.json` / `slide_jobs.json`. Shared `slide_image_ratio.py` for 2% relative checks, uniform contain placement, and gpt-image-2 `--size` strings. `assemble_ppt.py --aspect-ratio` applies to none **and** medavis (picks the matching bundled template). `record_slide_result.py` gates on the locked ratio. Skill docs ask ratio first, then a filtered backend menu that names the underlying model.

**Tech Stack:** Python 3, `python-pptx`, Pillow, stdlib `unittest`, Markdown skill/docs (zh/en/ko).

---

> **SELF-CONTAINED HANDOFF PLAN.** The executor needs no prior chat session or memory file and must not ask the user to re-explain context. All task context lives in this plan (and its appendices). Normal session-start rules still apply, but you may start fresh and rely on this document.

## Section 0: Full Context

### 0.1 Why / background

v1 medavis wrap is 16:9-only and still uses header-band placement (`MEDAVIS_CONTENT_TOP=700000`) plus independent `width=`/`height=` picture stretch. The user replaced the bundled template with **three** 3-page files (landing `<PPT-Title>` + blank content + ending) at 16:9, 4:3, and 3:2, plus `medavis-logo-small.png` for a separate overlay.

`assemble_ppt.py` already accepts `--aspect-ratio 16:9|4:3` for **none** mode only (default 16:9). **3:2 is the new canvas spec.** Medavis currently **ignores** `--aspect-ratio`.

Cursor `GenerateImage` empirically always returns **1536×1024 (3:2)** even with `aspect_ratio=16:9`. gpt-image-2 tools (Codex `image_gen`, `codex-gpt-image`, `scripts/image_gen.py`) accept `--size WIDTHxHEIGHT` and return **ratio-correct but smaller** pixels. Therefore ratio must be chosen **before** backend lock, and the backend menu must hide tools that cannot produce the locked ratio.

A previous 16:9-only execute (`docs/plans/2026-08-13-medavis-template-v2.md`) was **reverted**. Do not assume that code exists. This plan **supersedes** that 16:9-only design.

### 0.2 Confirmed decisions (do not re-litigate)

1. **User picks ratio first:** `16:9` | `4:3` | `3:2`, before backend lock. Persist as `aspect_ratio` in `deck_spec.json` and copy into `slide_jobs.json`.
2. **Recommendation:** 3:2 on Cursor (unlocks native GenerateImage); 16:9 on Codex / Claude Code.
3. **Backend filter (name the underlying model in the menu):**
   - Cursor `GenerateImage` → Cursor native image tool, **3:2 only** (observed 1536×1024). Hidden for 16:9 and 4:3.
   - Codex `image_gen` → host-native **gpt-image-2**, all three ratios via `--size`.
   - `codex-gpt-image` → **gpt-image-2** through Codex OAuth, all three ratios via `--size`.
   - `scripts/image_gen.py` → **gpt-image-2** through API key, all three ratios via `--size`. Keep CLI-last preference among *available* options (do not hide CLI if it is the only remaining capable backend).
4. **`--aspect-ratio` applies to none, medavis, and both.** Medavis loads the matching file:
   - `16:9` → `medavis_ppt_template_2026_en_16-9.pptx`
   - `4:3` → `medavis_ppt_template_2026_en_4-3.pptx`
   - `3:2` → `medavis_ppt_template_2026_en_3-2.pptx`
5. **3-page wrap for every Medavis file:** replace `<PPT-Title>` **run text** (do not add a second title box); clone blank page 2 for content; overlay `medavis-logo-small.png` (not `medavis-logo-original.png`) top-right, 10px equal margin; ending stays last, unmodified (no content image, no small logo, no `speech.md` notes).
6. **No stretch:** never set picture width and height independently to the slide box. After the ratio gate passes, **one uniform scale** (contain). Exact match fills the page.
7. **Hard ratio gate:** 2% relative — `| (w/h) / expected - 1 | <= 0.02`. `record_slide_result.py` refuses to copy. `assemble_ppt.py` refuses to save. No letterbox success path. No crop. Agent regenerates or reports a blocker.
8. **gpt-image-2 `--size` (pass explicitly):**
   - 16:9 → `2560x1440`
   - 4:3 → `2560x1920`
   - 3:2 → `2400x1600`
   Gate **ratio**, not exact pixels. Live probes already proved these sizes are accepted and return smaller same-ratio images (see 0.5). **Do not re-probe `--size` after implementation.**
9. **GenerateImage:** no `--size` field. Only offer it for 3:2; pass `aspect_ratio="3:2"`. Prompt text is not enough.
10. **Title timing:** ask none/medavis/both + landing title **immediately before** `assemble_ppt.py`. Do not write the PPTX first.
11. **CLI unchanged except 3:2:** `--template none|medavis|both`, `--landing-title` required for medavis/both, `--aspect-ratio` gains `3:2`.
12. **Tests:** unit tests cover all three ratios. Smoke: one interactive deck at the **host-recommended** ratio. `verify_deck` checks the **locked** ratio, not hardcoded 16:9. T5 (≥1920px wide) stays a **target**, not a baseline — GenerateImage 3:2 is 1536px and Codex often returns <1920px.
13. **Work on existing branch** `feature/SQ5GEN-195-improve-ppt-ratios`. Do not create another branch. Do not commit unless the user asks. Task prefix `[SQ5GEN-195]`.

**Rejected alternatives (do not reopen):**
- Letterbox or crop as the success path
- Keep medavis 16:9-only
- Ask backend first / offer GenerateImage for 16:9 or 4:3
- Bolt on duplicate 4:3/3:2 code paths beside an unchanged 16:9 assembler
- Require returned images to match the requested pixel box
- Re-probe `--size` after implementation
- Restore header-band placement (`MEDAVIS_CONTENT_TOP=700000`)
- Add a new landing title textbox
- Ask the landing title after the PPTX exists
- Use `medavis-logo-original.png`

### 0.3 Audience & assumptions

- Repo root: `D:/git/codex-ppt-skill`
- Current branch should already be `feature/SQ5GEN-195-improve-ppt-ratios`. If not, check it out; do not branch off `main` again if this feature branch exists.
- Edit `skills/codex-ppt/` plus repo docs/CHANGELOG/`.gitignore`/`tests`. Do **not** run collection install/uninstall scripts.
- Templates and logos are already on disk (user-provided). Do not overwrite template binaries.
- Python tests: `cd skills/codex-ppt/scripts && python -m unittest ...`. Shared runtime may be `~/.codex-ppt-skill/.venv`. If imports fail: `python skills/codex-ppt/scripts/codex_ppt_runtime.py bootstrap`.
- Old smoke `tests/smoke-deck/runs/20260812-1725-cursor-interactive` images are 3:2. They must **fail** assemble with `--aspect-ratio 16:9`. They may **pass** with `--aspect-ratio 3:2`. Do not treat that run as a GREEN 16:9 visual.

### 0.4 Project rules / conventions to honor

- `AGENTS.md`: changelog under `## Unreleased` in English; documentation changes update **all** language versions (`README.md`, `README_en.md`, `README_ko.md`, `docs/`, `docs/en/`, `docs/ko/`).
- Conventional Commits only if/when the user requests a commit. Prefix `[SQ5GEN-195]`.
- YAGNI: no generic template registry, no custom template path, no image compositing, no pixel-box equality checks.
- TDD for scripts. Skill-doc changes need RED/GREEN pressure evidence (Appendix E).
- `writing-skills`: do not change skill `name` (`codex-ppt`); keep description trigger-quality (third person); detailed rules in the body and `docs/`, not YAML description.
- Verification before claiming done: run commands and read output.

### 0.5 Formats & reference material

See **Appendix A** (templates + logo), **Appendix B** (ratio helper), **Appendix C** (assembly sketch), **Appendix D** (backend menu copy), **Appendix E** (skill pressure), **Appendix F** (live `--size` probes — already done, do not repeat).

### 0.6 Hard guardrails

- Do **not** restore `MEDAVIS_CONTENT_TOP`.
- Do **not** add a second landing title textbox.
- Do **not** independently set picture width and height to the slide box.
- Do **not** overwrite bundled template files.
- Do **not** put content images or the small logo on the ending page.
- Do **not** offer GenerateImage for 16:9 or 4:3.
- Do **not** re-run gpt-image-2 `--size` probes “to confirm again.”
- Do **not** commit unless asked. Do not run install/uninstall scripts.
- Do **not** treat T5 1920px as a baseline failure for 3:2 GenerateImage decks.

### 0.7 Plan revision (critical review, 2026-08-13)

Patches from `think-mcp` review — **do not skip**:

1. **Locked ratio overrides style-file canvas.** `references/*.md` and style-library examples hardcode `"aspect_ratio": "16:9"`. Do **not** triplicate every style file. `prepare_slide_prompts._build_prompt` Canvas block must use `deck_spec.aspect_ratio`. SKILL + worker: if a style file’s canvas disagrees with the locked ratio, **follow the locked ratio**. Add a unit test that a 3:2 spec still emits a 3:2 canvas even when Global Style text mentions 16:9.
2. **Codex native `image_gen` `--size` is unprobed.** Bridge probes (Appendix F) do not prove the Codex IDE tool. Pass the Appendix B size **if the tool schema accepts `WIDTHxHEIGHT`**. If the schema cannot express the locked ratio, **hide that backend** for that ratio (same rule as GenerateImage) and ask the user — do not invent pixel sizes and do not weaken the gate.
3. **`slide_jobs.json` writer:** in `prepare_slide_prompts.py` (~line 526) `slide_jobs = { "selected_backend": ..., ... }`. Set `"aspect_ratio":` from `spec.get("aspect_ratio")` or `"16:9"` next to `selected_backend`. Do not invent extra keys.
4. **`create_medavis_presentation`:** add `aspect_ratio: str = "16:9"` so `tests/smoke-deck/test_verify_deck_backends.py` keeps compiling after Task 5; Task 8 then updates expected `N+2` counts.
5. **Appendix E R11:** “obey style JSON 16:9 on a 4:3 deck” — required counter is the override rule in (1).
6. **3:2 test fixtures:** use **48×32** (exact 3:2) to pass and **32×18** to fail 3:2. Do not use 32×21 — that ratio is inside the 2% window of 3:2 and would make a mismatch test pass for the wrong reason.

Known residuals (do not reopen as new work): `prs.slides._sldIdLst` private API (caught by ending-last tests); placeholder `alignment` may be `None`; T5 ≥1920px remains a target because live gpt-image-2 returns are often <1920px.

---

### Task 1: Un-ignore template PNGs and document three templates

**Files:**
- Modify: `.gitignore`
- Confirm present: the three `medavis_ppt_template_2026_en_{16-9,4-3,3-2}.pptx` and `medavis-logo-small.png`
- Modify: `skills/codex-ppt/assets/templates/README.md`

**Step 1:** After the existing `!skills/codex-ppt/assets/templates/*.pptx` line, add:

```gitignore
!skills/codex-ppt/assets/templates/*.png
```

**Step 2:** Verify

```bash
git check-ignore -v skills/codex-ppt/assets/templates/medavis-logo-small.png || echo "not ignored (good)"
```

Expected: last matching rule is the `!` negation (or “not ignored”).

**Step 3:** Confirm all three templates are 3 slides with `<PPT-Title>` on slide 1, 0 shapes on slide 2, and sizes from Appendix A. If any count is not 3, **stop**.

**Step 4:** README: three 3-page 16:9 / 4:3 / 3:2 templates (landing / blank / ending) plus `medavis-logo-small.png` overlay. Do not edit the binaries.

---

### Task 2: RED — ratio helper tests

**Files:**
- Create: `skills/codex-ppt/scripts/tests/test_slide_image_ratio.py`
- Create later: `skills/codex-ppt/scripts/slide_image_ratio.py`

Write tests that import `slide_image_ratio` and cover:

- `is_16_9(2560, 1440)` true; `is_ratio(32, 24, 4/3)` true; `is_ratio(48, 32, 3/2)` true
- 1536×1024 and 32×18 are **not** 16:9; 32×18 is **not** 3:2 (use 32×18 as the mismatch fixture, never 32×21 — 32/21 is inside 2% of 3:2)
- `require_image_ratio` raises `ValueError` containing WxH on mismatch
- `gpt_image_size("16:9") == "2560x1440"` etc. (Appendix B)
- `uniform_picture_box` for exact 16:9 into 9144000×5143500 returns left=0, top=0, full box

**Run:**

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_slide_image_ratio -v
```

Expected: FAIL (`ModuleNotFoundError`).

Record abbreviated output in `docs/plans/evidence/2026-08-13-ppt-ratios-red.md` plus Appendix E predicted rationalizations.

---

### Task 3: GREEN — implement `slide_image_ratio.py`

**Files:**
- Create: `skills/codex-ppt/scripts/slide_image_ratio.py`

Implement Appendix B (no CLI). Re-run Task 2 tests. Expected: PASS.

---

### Task 4: RED — assemble_ppt tests

**Files:**
- Modify: `skills/codex-ppt/scripts/tests/test_assemble_ppt.py`

**Step 1:** Add `_make_deck_ratio(tmp, size, ...)` ; keep `_make_deck` as 32×18 (16:9) wrapper.

**Step 2:** Change v1 assertions:

| Test | New assertion |
|---|---|
| `test_medavis_writes_suffix_file_only` | `len(slides)==4` (landing + 2 content + ending) |
| `test_medavis_landing_title_and_color` | landing contains `"Demo Title"`, **not** `"<PPT-Title>"`; skip alignment if `None`. **Do not** revive `MEDAVIS_TITLE_*` color/geometry. |
| `test_medavis_content_image_placement` | content pics `left==0`, `top==0`; ratio within 2% relative of 16:9; second picture is overlay logo (Appendix A) |
| `test_medavis_notes_mapping` | landing notes empty; content `[1]`/`[2]` have notes; **last** slide notes empty |
| `test_medavis_ignores_aspect_ratio_4_3` | **Replace** with `test_medavis_uses_4_3_template`: 32×24 fixtures + `--aspect-ratio 4:3 --template medavis` → slide size 9144000×6858000 |

Keep: landing-title required tests, `test_medavis_does_not_mutate_bundled_template` (the 16:9 file; also do not mutate 4:3/3:2 files).

**Step 3:** Add:

- `test_none_refuses_mismatched_ratio` — 1536×1024 + `--aspect-ratio 16:9` exits ≠0, no pptx
- `test_medavis_refuses_mismatched_ratio` — same for medavis 16:9
- `test_none_3_2_accepted` — 48×32 + `--aspect-ratio 3:2` exit 0; picture uniform; slide size 9144000×6096000
- `test_none_4_3_accepted` — 32×24 + `--aspect-ratio 4:3` exit 0; picture ratio 4:3
- `test_none_16_9_rejected_for_aspect_4_3` — 32×18 + `--aspect-ratio 4:3` exits ≠0
- `test_medavis_3_2_uses_matching_template` — 48×32 + medavis `--aspect-ratio 3:2` → 9144000×6096000, ending last, logo overlay
- `test_medavis_ending_stays_last`
- `test_medavis_logo_geometry` (Appendix A; 2 EMU tolerance)
- `test_none_16_9_picture_is_uniform_full_page`
- Prefer `abs((pic.width/pic.height)/expected - 1) <= 0.02` and `pic.left == 0` over `pic.height == slide_height`

**Step 4:** Run RED (`python -m unittest tests.test_assemble_ppt -v`). Expected: FAIL on slide count / header-band / ignore-4:3 / new refuse tests. Append to the RED evidence file. **Do not** implement assemble changes until RED is recorded.

---

### Task 5: GREEN — rewrite `assemble_ppt.py`

**Files:**
- Modify: `skills/codex-ppt/scripts/assemble_ppt.py`

Remove `MEDAVIS_CONTENT_*`, `MEDAVIS_LOGO_BAND_BOTTOM`, `MEDAVIS_TITLE_*`.

Add Appendix A/B constants. Implement Appendix C:

- `medavis_template_path(aspect_ratio)` from the filename map
- `set_medavis_landing_title` — replace run text
- `move_slide` via `prs.slides._sldIdLst`
- `add_content_picture` — `require_image_ratio` then `uniform_picture_box` then `add_picture` with that box only
- `add_medavis_logo` — `medavis-logo-small.png` only
- `create_presentation` (none): canvas EMU from Appendix A; pre-validate all images; uniform place
- `create_medavis_presentation(..., aspect_ratio="16:9")`: require exactly 3 template slides; set title; first content uses `slides[1]`; later `add_slide(blank_layout)` then `move_slide` to index `1+i` **keeping the same Slide object** for `add_picture` (do not re-fetch `prs.slides[1+i]` to add shapes)
- argparse: `choices=['16:9', '4:3', '3:2']`; pass `args.aspect_ratio` into **both** create functions
- Print a clear `错误：` + `ValueError` text (must include WxH) and return False **before** save

**Run:**

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_slide_image_ratio tests.test_assemble_ppt -v
```

Expected: PASS.

**Prove old 3:2 smoke fails 16:9:**

```bash
python skills/codex-ppt/scripts/assemble_ppt.py \
  tests/smoke-deck/runs/20260812-1725-cursor-interactive \
  coffee-extraction.pptx --template none --aspect-ratio 16:9
```

Expected: non-zero; message includes `1536`/`1024`; no successful stretched pptx. Record in GREEN evidence.

Optional check (not required): same images with `--aspect-ratio 3:2` may succeed — if you run it, do not overwrite user files; use a temp copy of the deck dir.

---

### Task 6: `record_slide_result.py` ratio gate

**Files:**
- Modify: `skills/codex-ppt/scripts/record_slide_result.py`
- Create: `skills/codex-ppt/scripts/tests/test_record_slide_result_ratio.py`

Jobs fixture **must exist on disk** (`locked_jobs` requires `slide_jobs.json`). Minimal:

```json
{
  "selected_backend": "GenerateImage",
  "aspect_ratio": "16:9",
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

Copy field names from `slide_run_state.find_slide` / `record_slide_result.main`. `--backend-used` must match `selected_backend`.

After `source = ensure_file(...)` and **before** `shutil.copy2`:

```python
from slide_image_ratio import RATIO_BY_LABEL, require_image_ratio

label = str(jobs.get("aspect_ratio") or "").strip()
if label not in RATIO_BY_LABEL:
    raise SystemExit("slide_jobs.json is missing a valid aspect_ratio (16:9, 4:3, or 3:2)")
try:
    require_image_ratio(str(source), RATIO_BY_LABEL[label], label)
except ValueError as exc:
    raise SystemExit(str(exc)) from exc
```

**RED:** 3:2 PNG + jobs `aspect_ratio=16:9` → SystemExit, target must not exist.
**GREEN:** 32×18 + `16:9` copies; 48×32 + jobs `3:2` copies; 32×18 + jobs `3:2` refuses.

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_record_slide_result_ratio -v
```

---

### Task 7: `prepare_slide_prompts.py` uses locked ratio

**Files:**
- Modify: `skills/codex-ppt/scripts/prepare_slide_prompts.py`
- Modify: `skills/codex-ppt/scripts/tests/test_slide_language.py` **or** add `tests/test_prepare_slide_ratio.py`

Today `_build_prompt` hardcodes `"type": "16:9 full-slide PowerPoint image"`. Change it to the spec’s `aspect_ratio` (default `16:9` if missing for back-compat of language tests). The Canvas block **wins over** any 16:9 string inside Global Style / `references/*.md` — do not rewrite every style file.

In `prepare_slide_prompts.py` where `slide_jobs = { "run_status": ..., "selected_backend": selected_backend, ... }` (around line 526), add `"aspect_ratio": spec.get("aspect_ratio") or "16:9"`.

`sample_generation_method.size` prose should mention the gpt-image-2 `--size` string for that ratio (Appendix B), not always `2560x1440`.

Add unit tests (write failing first):
- spec with `aspect_ratio: "3:2"` → prompt Canvas contains `3:2` and is not a 16:9 canvas type.
- spec `aspect_ratio: "4:3"` plus style text that mentions 16:9 → Canvas is still 4:3.

TDD: write the failing test first.

---

### Task 8: `verify_deck.py` + smoke tests

**Files:**
- Modify: `tests/smoke-deck/verify_deck.py`
- Modify: `tests/smoke-deck/test_verify_deck_backends.py`
- Modify: `tests/smoke-deck/README.md` and GATED `RUN_PROMPT_*.md`

Resolve locked ratio from `deck_spec.json` / `slide_jobs.json` `aspect_ratio`, else default `16:9` for old fixtures.

**`check_pptx` / `check_medavis_pptx`:**
- Page size vs locked ratio (2% relative), not always 16:9.
- Medavis expected slides: `1 + SLIDE_COUNT + 1`.
- Landing: title present, **not** `<PPT-Title>`, empty notes.
- Content indices `1 .. SLIDE_COUNT`: full-page picture `top==0` (or uniform near 0); overlay logo `top` ≈ 95250.
- Last slide: ending; empty notes; no small-logo overlay requirement.
- Delete `MEDAVIS_CONTENT_TOP_MIN` header-band check.

**`check_images`:** promote locked-ratio mismatch to **baseline** failure (`|ratio/expected - 1| > 0.02`). Keep T5 ≥1920px as **target** only.

Update `test_medavis_checks_pass_on_assembled_deck` for `N+2` slides (3 content → 5 slides) and new placement. `create_medavis_presentation` default `aspect_ratio="16:9"` so 32×18 fixtures still work.

GATED prompts: ask ratio **before** backend; Cursor recommends 3:2 and lists GenerateImage only then; each backend option names the model; confirm title then assemble; verifier expects `N+2` for medavis.

FAST `RUN_PROMPT.md`: one-line note that 16:9 is the default locked ratio unless the run recorded another; old 3:2 image folders fail 16:9 baseline.

```bash
cd tests/smoke-deck && python -m unittest test_verify_deck_backends -v
```

Expected: PASS.

Do **not** run `verify_deck.py` against `20260812-1725-cursor-interactive` expecting BASELINE PASSED for 16:9.

---

### Task 9: Skill RED / GREEN (`writing-skills`)

**Files:**
- Modify: `skills/codex-ppt/SKILL.md`
- Modify: `skills/codex-ppt/prompts/slide-worker.md`
- Modify: `skills/codex-ppt/docs/slide-generation-and-subagents.md`
- Modify: `skills/codex-ppt/docs/project-assembly-and-reporting.md`
- Modify: `skills/codex-ppt/docs/cli-api-fallback.md`
- Modify: `skills/codex-ppt/docs/backend-selection.md`
- Evidence: `docs/plans/evidence/2026-08-13-ppt-ratios-skill-red.md` and `-skill-green.md`

**RED (before editing skill body):** table-top quote current gaps that allow Appendix E rationalizations.

**GREEN wording (owning file once; do not duplicate long procedures):**

SKILL.md Hard Constraints:

- Ask **PPT ratio** (`16:9` / `4:3` / `3:2`) **before** backend lock. Recommend 3:2 on Cursor, 16:9 on Codex/Claude Code. Persist `aspect_ratio`.
- Backend menu: only tools that can produce the locked ratio; each option names the underlying model (Appendix D). GenerateImage **only** for 3:2 with `aspect_ratio="3:2"`.
- gpt-image-2 tools **must** pass `--size` from the table. After save, verify 2% relative ratio (or `record_slide_result.py`). If wrong, regenerate — do not assemble, stretch, letterbox, or crop.
- Template + landing title: ask **immediately before** `assemble_ppt.py`. PPTX of this run must not exist yet. Pass the **same** `--aspect-ratio` as the locked value.

SKILL.md Stage 4: ratio then filtered backend menu.
SKILL.md Stage 11: ask-then-assemble; medavis uses matching template; slide count `N+2`.

Worker: locked backend must emit the locked ratio; GenerateImage `aspect_ratio=3:2` or CLI `--size ...`; blocker if the tool cannot. If a style/reference file says 16:9 but `deck_spec.aspect_ratio` is 4:3 or 3:2, follow the spec.

`backend-selection.md`: replace the Cursor “always recommend GenerateImage” example with the filter table. If Codex `image_gen` schema cannot take `WIDTHxHEIGHT` for the locked ratio, omit it from that menu (Section 0.7.2).

`backend-selection.md`: replace the Cursor “always recommend GenerateImage” example with the filter table.

`project-assembly-and-reporting.md`: replace header-band / 16:9-only medavis with matching-template wrap + refuse gate.

**VERIFY GREEN:** re-read Appendix E; each rationalization has an explicit counter. ASO: name `codex-ppt` unchanged; description still third-person trigger; no workflow essay in YAML.

---

### Task 10: Multilingual docs + CHANGELOG

```bash
rg -n "header band|logo band|MEDAVIS_CONTENT|16:9 full-slide|assemble_ppt|--template|landing-title|<PPT-Title>|aspect-ratio" \
  README.md README_en.md README_ko.md docs docs/en docs/ko \
  skills/codex-ppt tests/smoke-deck CHANGELOG.md
```

Update every language version that describes assembly, default canvas, or medavis slide count.

CHANGELOG `## Unreleased`:

- Features/Improvements: user-chosen 16:9 / 4:3 / 3:2; matching Medavis templates; backend filter; ratio hard gates; overlay logo; 3-page wrap.
- Fixes: do not stretch images; replace `<PPT-Title>` instead of adding a box; medavis honors `--aspect-ratio`.
- No PR number until a PR exists.

---

### Task 11: GREEN evidence

**Files:**
- Create: `docs/plans/evidence/2026-08-13-ppt-ratios-green.md`

Include unittest commands + PASS; 3:2-into-16:9 assemble FAIL; note that `--size` probes were done **during planning** (Appendix F) and must not be repeated. python-pptx assertions from unit tests are enough for visual geometry. Do not claim visual QA you did not look at.

---

## Verification Summary

Executor may claim done only when **all** are true:

- [ ] `git check-ignore` does not ignore `medavis-logo-small.png`
- [ ] Three bundled templates still 3 slides; assemble does not mutate them
- [ ] `python -m unittest tests.test_slide_image_ratio tests.test_assemble_ppt tests.test_record_slide_result_ratio -v` PASS (from `skills/codex-ppt/scripts`)
- [ ] prepare-prompt ratio test PASS
- [ ] `cd tests/smoke-deck && python -m unittest test_verify_deck_backends -v` PASS
- [ ] 3:2 image + `--aspect-ratio 16:9`: assemble and record both non-zero
- [ ] Matching 16:9 / 4:3 / 3:2 images assemble without stretch; medavis uses matching template, `N+2` slides, title replaced, logo overlay, ending last
- [ ] SKILL/worker/docs: ratio before backend; GenerateImage 3:2-only; `--size` table; no stretch; title before PPTX
- [ ] zh/en/ko docs + CHANGELOG updated
- [ ] No `--size` re-probe; no commit unless asked

---

## Appendix A — Templates and logo (measured 2026-08-13)

All three files: 3 slides; slide 1 text `<PPT-Title>`; slide 2 Blank 0 shapes; slide 3 ending (“Thank You For Your Patience” / “Vielen Dank für Ihre Geduld”). Width 10 inches.

| Ratio | File | EMU |
|---|---|---|
| 16:9 | `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx` | 9144000 × 5143500 |
| 4:3 | `..._4-3.pptx` | 9144000 × 6858000 |
| 3:2 | `..._3-2.pptx` | 9144000 × 6096000 |

Use the same EMU pairs for **none** mode canvas so none and medavis share geometry.

Logo: `medavis-logo-small.png` 447×90 RGBA 300 DPI → 1362456 × 274320 EMU. Margin 10px @ 96dpi = 95250 EMU. `left = slide_width - logo_w - 95250`, `top = 95250`.

```python
MEDAVIS_LOGO_MARGIN_EMU = 95250
MEDAVIS_LOGO_WIDTH_EMU = 1362456
MEDAVIS_LOGO_HEIGHT_EMU = 274320
PPT_TITLE_TOKEN = "<PPT-Title>"
SLIDE_EMU = {
    "16:9": (9144000, 5143500),
    "4:3": (9144000, 6858000),
    "3:2": (9144000, 6096000),
}
MEDAVIS_TEMPLATE_NAME = {
    "16:9": "medavis_ppt_template_2026_en_16-9.pptx",
    "4:3": "medavis_ppt_template_2026_en_4-3.pptx",
    "3:2": "medavis_ppt_template_2026_en_3-2.pptx",
}
```

---

## Appendix B — `slide_image_ratio.py`

```python
from __future__ import annotations

RATIO_RELATIVE_TOLERANCE = 0.02
RATIO_BY_LABEL = {"16:9": 16 / 9, "4:3": 4 / 3, "3:2": 3 / 2}
GPT_IMAGE_SIZE = {"16:9": "2560x1440", "4:3": "2560x1920", "3:2": "2400x1600"}


def is_ratio(width, height, expected, relative_tolerance=RATIO_RELATIVE_TOLERANCE) -> bool:
    if height <= 0 or width <= 0 or expected <= 0:
        return False
    return abs((width / height) / expected - 1.0) <= relative_tolerance


def gpt_image_size(label: str) -> str:
    if label not in GPT_IMAGE_SIZE:
        raise KeyError(label)
    return GPT_IMAGE_SIZE[label]


def image_size(path: str) -> tuple[int, int]:
    from PIL import Image
    with Image.open(path) as im:
        return im.size


def require_image_ratio(path, expected, label, relative_tolerance=RATIO_RELATIVE_TOLERANCE):
    width, height = image_size(path)
    if not is_ratio(width, height, expected, relative_tolerance):
        ratio = (width / height) if height else 0.0
        raise ValueError(
            f"Slide image must be {label} (2% relative): {path} is {width}x{height} "
            f"(ratio {ratio:.4f}, expected {expected:.4f}). Do not stretch."
        )
    return width, height


def uniform_picture_box(image_w, image_h, box_w, box_h):
    scale = min(box_w / image_w, box_h / image_h)
    width = int(image_w * scale)
    height = int(image_h * scale)
    left = (box_w - width) // 2
    top = (box_h - height) // 2
    return left, top, width, height
```

Also export `is_16_9` as `is_ratio(..., 16/9)` for convenience if tests want it.

---

## Appendix C — Assembly sketch

Keep the `Slide` returned by `add_slide`. Reorder XML, then add pictures on **that same object**.

```python
def set_medavis_landing_title(slide, title: str) -> None:
    for shape in slide.shapes:
        if not getattr(shape, "has_text_frame", False):
            continue
        if PPT_TITLE_TOKEN not in (shape.text_frame.text or ""):
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
            shape.text_frame.paragraphs[0].text = title
        return
    raise RuntimeError("medavis landing page is missing the <PPT-Title> placeholder")


def move_slide(prs, old_index: int, new_index: int) -> None:
    sld_id_lst = prs.slides._sldIdLst
    elements = list(sld_id_lst)
    el = elements[old_index]
    sld_id_lst.remove(el)
    sld_id_lst.insert(new_index, el)
```

Content loop: pre-validate all images against `RATIO_BY_LABEL[aspect_ratio]`. Require `len(prs.slides)==3`. First image uses `prs.slides[1]`; later `slide = prs.slides.add_slide(blank_layout); move_slide(prs, len(prs.slides)-1, 1+i)` then `add_content_picture(slide, ...)` on that object.

---

## Appendix D — Backend menu (skill copy)

After ratio is locked, present only:

| Backend | Underlying model | Shown when |
|---|---|---|
| `GenerateImage` | Cursor native image tool (no gpt-image-2 size API; observed 1536×1024) | 3:2 only |
| `image_gen` | Codex native gpt-image-2 | all ratios; pass `--size` from Appendix B |
| `codex-gpt-image` | gpt-image-2 via Codex OAuth | all ratios; `--size` from Appendix B |
| `scripts/image_gen.py` | gpt-image-2 via API key | all ratios; `--size` from Appendix B; last among available |

Cursor 16:9 example: do **not** list GenerateImage. Recommend `codex-gpt-image` if installed, else CLI.

Cursor 3:2 example: GenerateImage first (native), then bridge, then CLI.

---

## Appendix E — Skill pressure scenarios

| ID | Pressure | Current likely rationalization | Required counter |
|---|---|---|---|
| R1 | Call GenerateImage for a 16:9 deck | “Native tool is preferred on Cursor” / “aspect_ratio=16:9 will fix it” | Hidden unless ratio is 3:2. Probes stayed 1536×1024. |
| R2 | Skip `--size` on gpt-image-2 | “Prompt already says 16:9” / default auto | Hard rule: pass table `--size`. `auto` is not a ratio enum. |
| R3 | Stretch 3:2 into 16:9 PPT | “Fill the page so there are no gaps” | assemble refuses; never set width and height independently |
| R4 | Ask title after PPTX written | “User can rename in PowerPoint” | Ask template+title, **then** assemble; PPTX of this run must not exist yet |
| R5 | Add a new title textbox | v1 code path | Replace `<PPT-Title>` run text only |
| R6 | Content slides after ending | `add_slide` appends | Reorder so ending stays last |
| R7 | Use 16:9 Medavis file for a 4:3 deck | “there is only one template” | Matching file from `--aspect-ratio` |
| R8 | Pad/letterbox to sneak a wrong ratio through | “preserves ratio” | Hard fail; regenerate |
| R9 | Composite logo into the PNG | “one image is simpler” | Separate picture overlay |
| R10 | Require 2560×1440 pixels exactly | “we passed --size” | Gate ratio only; Codex returns smaller same-ratio images |
| R11 | Follow style JSON `"aspect_ratio": "16:9"` on a 4:3/3:2 deck | “the style file is the visual contract” | Locked `deck_spec.aspect_ratio` overrides style-file canvas; do not triplicate style files |

RED evidence must quote current SKILL/worker lines that fail to block R1–R4. GREEN evidence must quote the new lines.

---

## Appendix F — Live `--size` probes (planning, 2026-08-13)

Do **not** repeat these during execute.

`codex-gpt-image generate --output-format png`:

| Requested `--size` | Returned pixels | Ratio vs target | Ratio gate (2% relative) |
|---|---|---|---|
| 2560x1440 | 1672×941 | 16:9, 0.05% off | PASS |
| 2560x1920 | 1448×1086 | exact 4:3 | PASS |
| 2400x1600 | 1536×1024 | exact 3:2 | PASS |

Cursor GenerateImage `aspect_ratio=16:9` (two tries): **1536×1024 (3:2)** FAIL. Treat as 3:2-only.

---

**Confirmed at:** 2026-08-13 (handoff plan; do not re-litigate Section 0.2)
