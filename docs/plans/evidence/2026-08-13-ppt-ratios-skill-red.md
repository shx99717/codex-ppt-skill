# Skill RED — multi-ratio PPT (2026-08-13)

Table-top quotes from skill/docs **before** Task 9 GREEN edits. These lines allow Appendix E R1–R4 (and related) rationalizations.

## R1 — Call GenerateImage for a 16:9 deck

`skills/codex-ppt/SKILL.md` Overview:

> Prefer a real host-native image tool when one exists (Cursor `GenerateImage`, Codex `image_gen`).

`skills/codex-ppt/docs/backend-selection.md` preference table and Cursor example:

> Cursor | `GenerateImage` (native) | `codex-gpt-image` if installed | `scripts/image_gen.py`
>
> A) GenerateImage (native, recommended)

No rule hides GenerateImage when the locked ratio is 16:9 or 4:3.

## R2 — Skip `--size` on gpt-image-2

`skills/codex-ppt/docs/cli-api-fallback.md`:

> The fallback CLI defaults to 2K 16:9 landscape output, `2560x1440`

Worker prompt does not require passing `--size` from a ratio table. Prompt-only 16:9 is treated as enough.

## R3 — Stretch 3:2 into 16:9 PPT

`skills/codex-ppt/SKILL.md` Stage 11 / Overview: “Each slide is a complete 16:9 generated image” with no refuse-on-mismatch / no-stretch rule.

`skills/codex-ppt/docs/project-assembly-and-reporting.md`:

> Full-bleed content images over the medavis logo / header band

Implies filling the page; no hard fail if pixels are 3:2.

## R4 — Ask title after PPTX written

Stage 11 says ask template mode before assembly, but does not say the PPTX of this run must not exist yet.

## Related (R5–R11) current gaps

- R5/R6/R7: assembly doc still describes header-band placement, 16:9-only medavis, ignore `--aspect-ratio`.
- R11: style `references/*.md` hardcode `"aspect_ratio": "16:9"` with no SKILL/worker override to `deck_spec.aspect_ratio`.
