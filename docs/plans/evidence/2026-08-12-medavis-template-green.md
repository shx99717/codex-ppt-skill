# GREEN evidence: medavis template assembly

**Date:** 2026-08-12

## Unit tests

```text
cd skills/codex-ppt/scripts
python -m unittest tests.test_assemble_ppt -v
# Ran 10 tests ... OK
```

## Smoke

```text
python skills/codex-ppt/scripts/assemble_ppt.py \
  tests/smoke-deck/runs/20260812-1406-cursor-interactive \
  coffee-extraction.pptx --template both --landing-title "Coffee Extraction"
```

Outputs:

- `coffee-extraction.pptx` (3 slides)
- `coffee-extraction-medavis.pptx` (4 slides = 1 landing + 3 content)

PowerPoint COM export previews under `.../medavis_smoke_preview/`:

- Landing shows “Coffee Extraction” in medavis blue; logo + copyright visible; no “Insert title here”
- Content slides keep medavis header logo; generated image fills white area; no layout ghost titles observed

## Rationalization counters

| ID | Rationalization | Counter |
|----|-----------------|---------|
| R1 | Skip template question | `SKILL.md` step 11 + `project-assembly-and-reporting.md` “Template mode (required user choice)” |
| R2 | Skip landing title confirm | Same docs: suggest then confirm/edit before `--landing-title` |
| R3 | Overwrite `{deck}.pptx` for medavis | Docs + CLI: always `{deck}-medavis.pptx` |
| R4 | Full-bleed OK | Placement constants keep `top >= 700000`; logo band uncovered |
| R5 | Both = one file | Docs + CLI: both writes plain and `-medavis` |

## gitignore

`!skills/codex-ppt/assets/templates/*.pptx` added; template shows as untracked/`??` (not ignored).
