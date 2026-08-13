# Memory: Medavis PPT Template Assembly Option

**Generated**: 2026-08-12 15:08 UTC+8
**Last updated**: 2026-08-13 19:15 UTC+8
**Project**: D:/git/codex-ppt-skill
**Focus**: User-chosen PPT ratio (16:9 / 4:3 / 3:2), matching Medavis templates, backend filter, no stretch, ratio hard gates

---

## Goal & Scope (required)

Let the user pick the final PPT ratio (16:9, 4:3, or 3:2) before backend lock. Filter image backends by that ratio (Cursor GenerateImage is 3:2-only). Drive none-mode canvas and the matching 3-page Medavis template from the same ratio. Never stretch. Hard-gate saved images against the locked ratio (2% relative). Adapt script unit tests and `tests/` (smoke = one deck at the host-recommended ratio).

---

## Key Decisions (required)

1. Bundle medavis template; extend `assemble_ppt.py` with `--template` / `--landing-title`.
2. Outputs: `{deck}.pptx` and/or `{deck}-medavis.pptx`.
3. Placement: `MEDAVIS_CONTENT_TOP=700000`; logo preserved; title `#42637B`.
4. First review I1–M5 all fixed; follow-up review clean (zero new findings).
5. Commit with `[SQ5GEN-195]` Conventional Commits prefix (user confirmed).
6. **Reversed: header-band content placement**: New template is 3 pages. Use blank page 2 as the full-page content clone; keep ending page last unmodified. Do not leave a thick header-only logo band.
7. **Reversed: add a new title text box**: Replace text in the existing `<PPT-Title>` placeholder; keep its font weight and center alignment.
8. Overlay `medavis-logo-small.png` as a separate picture (not composited), content pages only, top-right, 10px (~0.10 in) equal top/right margin, native 300 DPI size (~1.49 in × 0.30 in). Do not use `medavis-logo-original.png`.
9. **Reversed: always require 16:9**: User picks 16:9, 4:3, or 3:2. Hard-gate saved images against the **locked** ratio with a **2% relative** window. Never stretch, letterbox, or crop as a success path.
10. **Reversed: GenerateImage can be instructed to 16:9**: Cursor GenerateImage is 3:2-only in practice (1536×1024 even with `aspect_ratio=16:9`). Do not offer it for 16:9 or 4:3.
11. Landing title stays an assembly-time question (template mode + title), then run `assemble_ppt.py`. Never ask after the PPTX is written.
12. Last smoke images were 1536×1024 (3:2); independent width/height in `assemble_ppt.py` caused distortion on a 16:9 canvas.
13. **Superseded: 16:9-only v2 design / execute**: The 2026-08-13 v2 handoff plan assumed GenerateImage 16:9. Execute was cleaned up; plan files kept as history. New work is multi-ratio on branch `feature/SQ5GEN-195-improve-ppt-ratios`.
14. Ask **ratio first**, then only offer backends that can produce it. Recommend **3:2 on Cursor** (unlocks GenerateImage); **16:9 on Codex / Claude Code**.
15. Backend × model: GenerateImage = Cursor native, 3:2 only. Codex `image_gen` / `codex-gpt-image` / `scripts/image_gen.py` = gpt-image-2, all three ratios. Menu options must name the underlying model.
16. `--aspect-ratio` applies to none, medavis, and both. Medavis loads the matching bundled template (16-9 / 4-3 / 3-2). Same 3-page wrap + small-logo overlay for all three.
17. gpt-image-2 tools must pass `--size`: 16:9 → **2560x1440**, 4:3 → **2560x1920**, 3:2 → **2400x1600**. Gate on ratio, not exact pixels. GenerateImage has no `--size`.
18. No post-implementation size re-probe; live probes already proved those `--size` values are accepted (smaller same-ratio pixels).
19. Unit tests cover all 3 ratios. Smoke stays one interactive deck at the host-recommended ratio.
20. **Approved design (approach A):** one ratio-keyed pipeline. `aspect_ratio` in `deck_spec.json`/`slide_jobs.json` is the single source of truth for canvas EMU, Medavis file, prompt canvas, gpt-image-2 `--size`, and record/assemble gates. Shared `slide_image_ratio.py`. Filtered backend menu names the underlying model. 3-page wrap + logo overlay on every matching template. T5 ≥1920px stays a smoke *target*, not a baseline.
21. **Handoff plan:** `docs/plans/2026-08-13-improve-ppt-ratios.md` + `docs/plans/2026-08-13-improve-ppt-ratios-PROMPT-execute.md`.
23. **Execute session 2026-08-13:** Implemented the multi-ratio plan on `feature/SQ5GEN-195-improve-ppt-ratios` without commit. User confirmed review focus (plan alignment, pipeline, tests, no-stretch gates, skill-doc counters).

---

## Confirmed Assumptions (required)

- Do not push unless asked.
- Do not overwrite bundled template files when assembling.
- none / medavis / both CLI choices stay.
- Ending page: no content image, no small logo, no speaker notes from `Slide N`.
- Scope includes tests, smoke verifier, changelog, multilingual docs, gitignore so template PNGs are tracked.
- 3:2 is the new canvas spec; none-mode already had 16:9 and 4:3; medavis was 16:9-only.

---

## Constraints & Non-Goals

- No template art redesign.
- No cropping or letterbox as a success path.
- Do not change the slide size baked into each Medavis template file; pick the matching file instead.
- Do not ask the landing title after PPTX exists.
- Do not offer GenerateImage for 16:9 or 4:3.
- Do not require returned images to match the requested pixel box.
- Do not re-probe `--size` after implementation.

---

## Key Discoveries (required)

- Root `*.pptx` gitignore needs `!skills/codex-ppt/assets/templates/*.pptx`.
- Follow-up reviewer: `3f2973b4-6540-4d52-a496-1435cb697333` — I1–M5 FIXED; 12/12 tests OK.
- Three 3-page templates (2026-08-13): landing `<PPT-Title>`, blank content, ending. Sizes EMU: 16:9 `9144000×5143500`, 4:3 `9144000×6858000`, 3:2 `9144000×6096000`.
- `medavis-logo-small.png`: 447×90 RGBA, 300 DPI. Need `!skills/codex-ppt/assets/templates/*.png`.
- `python-pptx` `add_slide` appends after the ending page; extra content slides must be reordered before the last slide.
- Setting `paragraph.text` in python-pptx can wipe placeholder formatting; prefer replacing run text.
- Cursor GenerateImage (two probes, including stronger 16:9 prompt): always **1536×1024 (3:2)**.
- `codex-gpt-image --size` live lock probes (2026-08-13): `2560x1440` → 1672×941 (16:9, 0.05% off); `2560x1920` → 1448×1086 (exact 4:3); `2400x1600` → 1536×1024 (exact 3:2). API accepts the size; returned pixels are smaller; ratio matches.
- User research images: `ratio-test-codex-gpt-image-20260813.png` 1672×941; `-4x3-` 1448×1086; `-3x2-` 1536×1024.
- `scripts/image_gen.py` default is already `2560x1440` if `--size` is omitted. `codex-gpt-image` default is `auto`. GenerateImage has no pixel size field.
- `assemble_ppt.py --aspect-ratio` now applies to none and medavis; matching 3-page templates; uniform contain; 2% relative refuse gate.
- Bundled ending page already has 2 pictures (full-bleed + small art); ending-last tests must not require `pictures == []`.
- `!skills/codex-ppt/assets/templates/*.png` also un-ignores `medavis-logo-original.png` (do not use it in assemble).
- Direct `create_medavis_presentation()` prints `✓` and can fail on GBK stdout; CLI `main()` reconfigures UTF-8. Smoke test reconfigures stdout before calling the function.

---

## Current State (required)

- **Working**: Multi-ratio pipeline on `feature/SQ5GEN-195-improve-ppt-ratios` (uncommitted). Review findings Important-1..4 and Minor-1,2,3,5,6,7 applied. 75 script tests + 10 smoke verifier tests PASS.
- **Pending**: User accepted current state after two review-fix cycles. Commit only if asked (`[SQ5GEN-195]`)
- **Blocked**: none

---

## Next Steps (required)

1. [x] Confirm multi-ratio requirements
2. [x] Brainstorming: pick approach and approve design
3. [x] Write handoff plan `docs/plans/2026-08-13-improve-ppt-ratios.md`
4. [x] Implement on `feature/SQ5GEN-195-improve-ppt-ratios`
5. [x] Finish code review / receiving-code-review if findings exist (applied ACCEPTED set; Minor-4 rejected)
6. [x] Follow-up review of applied fixes if user confirms
7. [ ] Commit only if user asks (`[SQ5GEN-195]`)

---

## Notes for Next Session

- User wrote “2560x1400” once; locked value is **2560x1440** for 16:9.
- Do not restore `MEDAVIS_CONTENT_TOP=700000`.
- Title question still immediately before `assemble_ppt.py`.
- v2 execute was cleaned up; keep `docs/plans/2026-08-13-medavis-template-v2.md` as history only.

---

## References (required)

- `docs/plans/2026-08-13-improve-ppt-ratios.md` — current handoff plan
- `docs/plans/2026-08-13-improve-ppt-ratios-PROMPT-execute.md` — paste into a new session
- `docs/plans/2026-08-13-medavis-template-v2.md` — superseded 16:9-only handoff (history)
- `docs/plans/2026-08-13-medavis-template-v2-PROMPT-execute.md` — history
- `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx`
- `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_4-3.pptx`
- `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_3-2.pptx`
- `skills/codex-ppt/assets/templates/medavis-logo-small.png`
- `skills/codex-ppt/scripts/assemble_ppt.py`
- `skills/codex-ppt/scripts/slide_image_ratio.py`
- `skills/codex-ppt/SKILL.md`
- `tests/smoke-deck/verify_deck.py`
- `docs/plans/evidence/2026-08-13-ppt-ratios-green.md` — execute GREEN evidence

---

**Confirmed at**: 2026-08-13 19:15 UTC+8
