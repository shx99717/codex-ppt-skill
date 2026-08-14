# GREEN evidence — multi-ratio PPT canvases (2026-08-13)

`--size` probes were done **during planning** (plan Appendix F). They were **not** repeated in this execute session.

python-pptx assertions from unit tests cover geometry. This file does not claim visual QA of rendered slides.

## Unit tests PASS

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_slide_image_ratio tests.test_assemble_ppt tests.test_record_slide_result_ratio tests.test_prepare_slide_ratio -v
```

Result: PASS (included in a 70-test `unittest discover -s tests -v` run, OK).

```bash
cd tests/smoke-deck
python -m unittest test_verify_deck_backends -v
```

Result: PASS (9 tests). Medavis assembled deck is 5 slides (`N+2` for 3 content pages).

## 3:2-into-16:9 assemble FAIL

```bash
python skills/codex-ppt/scripts/assemble_ppt.py \
  tests/smoke-deck/runs/20260812-1725-cursor-interactive \
  coffee-extraction.pptx --template none --aspect-ratio 16:9
```

Exit 1. Message includes `1536x1024` and `Do not stretch.` This invocation did not save a stretched PPTX.

`record_slide_result.py` refuses the same class of mismatch (`48x32` + jobs `aspect_ratio=16:9`) per `tests.test_record_slide_result_ratio`.

## Other gates

- `git check-ignore -v skills/codex-ppt/assets/templates/medavis-logo-small.png` last match is `!skills/codex-ppt/assets/templates/*.png`
- Bundled templates remain 3 slides; assemble mutation tests pass for 16:9 / 4:3 / 3:2 files
- Skill YAML `name: codex-ppt`; description unchanged (third-person trigger)
- No `--size` re-probe; no commit in this session
