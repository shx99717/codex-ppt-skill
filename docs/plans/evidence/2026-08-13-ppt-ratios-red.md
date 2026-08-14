# RED evidence — multi-ratio PPT canvases (2026-08-13)

## Task 4 — assemble_ppt tests vs header-band assembler

**Command:** `python -m unittest tests.test_assemble_ppt -v`

**Result:** 11 FAIL / 21 run. Failures match the plan:

- slide count / ending-last: `test_medavis_ending_stays_last` (thank-you not on last slide); notes mapped onto the ending page
- header-band: content placement has 1 picture, no overlay logo; `<PPT-Title>` still present beside the added title box
- ignore-4:3: `test_medavis_uses_4_3_template` height `5143500 != 6858000`
- refuse tests: 3:2-into-16:9 and 16:9-into-4:3 still exit 0; `3:2` argparse invalid choice

`test_medavis_writes_suffix_file_only` already sees 4 slides because the new 3-page template plus one `add_slide` yields four pages with the ending in the middle.

---

## Task 2 — `slide_image_ratio` missing

**Command:**

```bash
cd skills/codex-ppt/scripts
python -m unittest tests.test_slide_image_ratio -v
```

**Result:** FAIL (`ModuleNotFoundError: No module named 'slide_image_ratio'`).

```
ImportError: Failed to import test module: test_slide_image_ratio
...
    import slide_image_ratio
ModuleNotFoundError: No module named 'slide_image_ratio'
FAILED (errors=1)
```

Expected: tests cannot import production helper until Task 3 creates it.

## Appendix E predicted rationalizations (skill docs, Task 9)

These are the current likely excuses the skill text still allows. Quoted counters belong in skill GREEN evidence after Task 9.

| ID | Predicted rationalization |
|---|---|
| R1 | Native GenerateImage is preferred on Cursor; `aspect_ratio=16:9` will fix 3:2 pixels |
| R2 | Prompt already says 16:9; skip `--size` / use `auto` |
| R3 | Stretch 3:2 into 16:9 so the page has no gaps |
| R4 | Ask landing title after PPTX exists; user can rename in PowerPoint |
| R5 | Add a new title textbox (v1 path) |
| R6 | `add_slide` appends after ending; leave ending in the middle |
| R7 | Use the 16:9 Medavis file for a 4:3/3:2 deck |
| R8 | Letterbox/crop a wrong-ratio image as a success path |
| R9 | Composite the logo into the PNG |
| R10 | Require exact `2560x1440` pixels because `--size` was passed |
| R11 | Obey style JSON `"aspect_ratio": "16:9"` on a 4:3/3:2 deck |
