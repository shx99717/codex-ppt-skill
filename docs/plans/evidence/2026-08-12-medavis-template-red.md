# RED evidence: medavis template assembly

**Date:** 2026-08-12

## Baseline before implementation

- `assemble_ppt.py` had no `--template` / `--landing-title` flags.
- Docs had no template-mode user choice gate.
- Bundled template path did not exist before Task 1.

## Predicted agent rationalizations (Appendix E)

- R1: Assembly unchanged — run assemble_ppt without asking about templates.
- R2: Outline/sample already approved — no need to confirm landing title.
- R3: Medavis mode can overwrite `{deck}.pptx` instead of `-medavis.pptx`.
- R4: Full-bleed covering the logo is OK.
- R5: Both mode only needs one file.

## Unit test RED (before implementation)

`python -m unittest tests.test_assemble_ppt -v` failed with argparse exit code 2 on unknown `--template`, plus missing `medavis_template_path` / helpers. Existing GBK encoding tests still passed.
