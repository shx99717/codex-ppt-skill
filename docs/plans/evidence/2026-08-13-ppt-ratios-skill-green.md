# Skill GREEN — multi-ratio PPT (2026-08-13)

Re-read Appendix E. Each rationalization now has an explicit counter. ASO: skill `name` remains `codex-ppt`; YAML `description` is still third-person trigger text; no workflow essay in YAML.

| ID | Counter (quoted home) |
|---|---|
| R1 | SKILL Hard Constraints: GenerateImage **only** for 3:2. `backend-selection.md`: Cursor 16:9 example hides GenerateImage. Worker: return blocker if parent locked 16:9/4:3. |
| R2 | SKILL: gpt-image-2 **must** pass table `--size`. Worker + `cli-api-fallback.md`: do not use `auto`. |
| R3 | SKILL: do not assemble, stretch, letterbox, or crop. `project-assembly-and-reporting.md`: refuse 2% relative; never set width and height independently. |
| R4 | SKILL Stage 11 + Hard Constraints: ask template+title **immediately before** assemble; PPTX of this run must not exist yet. |
| R5 | SKILL / assembly doc: replace `<PPT-Title>` run text; do not add a second title box. |
| R6 | Assembly doc: ending stays last, unmodified. |
| R7 | Matching template filenames from `--aspect-ratio`. |
| R8 | Hard fail; regenerate. |
| R9 | Overlay `medavis-logo-small.png` as a separate picture on content pages only. |
| R10 | Gate 2% relative ratio, not exact pixels. |
| R11 | SKILL + worker + `slide-generation-and-subagents.md`: locked `deck_spec.aspect_ratio` overrides style-file 16:9 canvas. |

## Quoted GREEN lines

SKILL.md Hard Constraints:

> Ask **PPT ratio** (`16:9` / `4:3` / `3:2`) **before** backend lock.

> Cursor `GenerateImage` ... **only** for 3:2

> If wrong, regenerate — do not assemble, stretch, letterbox, or crop.

> PPTX of this run must not exist yet.

`docs/backend-selection.md` Cursor 16:9 example:

> GenerateImage is hidden (3:2 only; probes returned 1536×1024).

Worker:

> If a style or `references/*.md` file says 16:9 but `deck_spec.aspect_ratio` is 4:3 or 3:2, follow the spec Canvas / locked ratio.
