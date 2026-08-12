# Cursor + `codex-gpt-image` — FAST smoke + strict fix loop

Paste the fenced block below **verbatim** into a fresh Cursor agent chat.
This run is pinned to **Cursor** with backend locked to **`codex-gpt-image`**.
Do not self-detect another host. Do not fall back to `GenerateImage` for this variant.

Canonical skill source: `d:/git/codex-ppt-skill/skills/codex-ppt`
Installed skill this host must run: `~/.cursor/skills/codex-ppt`
Bridge skill required: `~/.cursor/skills/codex-gpt-image` (Codex OAuth image path)

See also:
[`RUN_PROMPT_cursor.md`](RUN_PROMPT_cursor.md) (Cursor / `GenerateImage` hard-pin),
[`RUN_PROMPT_claude.md`](RUN_PROMPT_claude.md) (Claude / `codex-gpt-image` hard-pin).

---

```
You are running the codex-ppt smoke-deck on CURSOR only, in FAST mode, with a
strict engineering fix loop, and with the image backend HARD-PINNED to
`codex-gpt-image`. Do not switch hosts. Do not use Cursor `GenerateImage`.
Do not commit or push unless I explicitly say so.

## Host pins (fixed)

| Item | Value |
|------|-------|
| Environment | Cursor |
| --host | cursor |
| Installed skill | ~/.cursor/skills/codex-ppt |
| Bridge skill | ~/.cursor/skills/codex-gpt-image |
| Locked selected_backend | codex-gpt-image |
| Fork repo root | d:/git/codex-ppt-skill |
| Canonical skill source | d:/git/codex-ppt-skill/skills/codex-ppt |

Verifier matrix for Cursor still accepts `GenerateImage` OR `codex-gpt-image`,
but **this variant must lock and use only** `codex-gpt-image` for sample + all
slides (T6 must report `selected_backend='codex-gpt-image'`). Unrequested
`scripts/image_gen.py` / CLI fallback is a failure unless I explicitly ask for
`--allow-cli-fallback`. Using `GenerateImage` in this run is a failure even if
it would pass the host matrix.

## Non-negotiable rules

1. **Installed skill must match the fork.** Before generating, and after every
   fix, sync:
   copy `d:/git/codex-ppt-skill/skills/codex-ppt` → `~/.cursor/skills/codex-ppt`
   (replace the destination; exclude `__pycache__` / `*.pyc`). Verify with a
   file-hash or file-list compare that the install matches the fork (especially
   `scripts/record_user_review.py`, `scripts/probe_image_backends.py`,
   `scripts/prepare_slide_prompts.py`, `SKILL.md`).
2. **Edits land only in the fork repo** under `d:/git/codex-ppt-skill`
   (skill code/docs/tests). Never “fix only” the installed copy.
3. **No commits, no push, no amend** unless I explicitly authorize it.
4. **No speculative refactors.** Fix the failing behavior; keep scope minimal.
5. On any error/bug/failed check: follow **systematic debugging** — root cause
   first, then fix. Prefer **TDD** for script/logic bugs: failing unit test →
   fix → green unit tests → re-sync install → re-run smoke.
6. Unit tests live at:
   `skills/codex-ppt/scripts/tests/`
   (`test_record_user_review.py`, `test_probe_image_backends.py`,
   `test_backend_family.py`, `test_slide_language.py`).
   Command from fork root:
   `python -m unittest discover -s skills/codex-ppt/scripts/tests -v`
7. **codex-gpt-image auth must work** before image generation. From
   `~/.cursor/skills/codex-gpt-image`, run
   `python scripts/codex_gpt_image.py auth-status`. If missing/expired, run
   `python scripts/codex_gpt_image.py login --open-browser` and wait for me to
   finish the device-code flow. Never print tokens from `~/.codex/auth.json`.

## Pass criteria for THIS fork run

- **BASELINE**: all checks must PASS (exit code of verify_deck.py).
- **TARGET**: T1 (review recorded), T2 (no hardcoded Chinese rule on EN slide),
  T3 (per-slide language), T6 (specific selected_backend — must be
  `codex-gpt-image`), and **T7** (no Unix-only `.venv/bin/python` in skill docs;
  scored on Windows when `--skill-root` is passed) must PASS — those goals are
  already implemented. Investigate any other TARGET miss (T4/T5); fix if it is
  a real skill defect; ask me if it looks environment-only (e.g. image width /
  host tooling). Note: this variant is especially useful for checking whether
  T5 improves vs Cursor `GenerateImage`.

## Procedure

### A. Preflight

1. `cd d:/git/codex-ppt-skill`
2. Sync fork → `~/.cursor/skills/codex-ppt` and confirm match.
3. Confirm `~/.cursor/skills/codex-gpt-image/SKILL.md` exists.
4. Run codex-gpt-image `auth-status` (see rule 7). Stop if auth cannot be fixed.
5. `python tests/smoke-deck/verify_deck.py --preflight`
   If deps missing, run the printed bootstrap, then re-check. Stop if bootstrap fails.
6. Ask me for `<build_dir>` (suggest
   `tests/smoke-deck/runs/<YYYYMMDD-HHMM>-cursor-codex-gpt-image`). Wait for my answer.

### B. Generate (FAST contract — do not deviate)

Use the **installed** codex-ppt skill to build from
`tests/smoke-deck/source.md`:

- Output base directory: `<build_dir>`
- Deck name: `coffee-extraction`
- Exactly 3 slides
- Slide 1 Chinese; slide 2 English; slide 3 mixed Chinese + Latin
- Visual style: built-in `清爽专业风` (do not offer style options)
- Aspect ratio: 16:9
- Titles / points / layout / composition: decide from the source

Gate handling:
- Outline: pre-approved — write `outline.md` and continue
- Style: pinned — do not offer options
- Sample: pre-approved — accept first sample and continue
- Image backend: probe callable backends in Cursor (prose-check `GenerateImage`,
  run `probe_image_backends.py`, confirm `codex-gpt-image` available). State what
  you checked, then **lock `selected_backend=codex-gpt-image`** and continue
  without waiting for confirmation. Do **not** lock `GenerateImage` in this run.
  Persist the lock into `deck_spec.json` / prepare with `--selected-backend
  codex-gpt-image`. Every final slide image must be produced via the
  `codex-gpt-image` skill/CLI path (same method for sample + remaining slides).
- Still honor skill rules that require recording user review / run-state for
  the pre-assembly review gate when the skill says to (FAST skips *waiting*,
  not required bookkeeping). If the skill requires a review marker before
  assemble, record approval via the skill’s review mechanism after slides are
  ready, without inventing a new protocol.

Generate speaker notes and assemble the `.pptx`.
For this smoke deck, ask template mode but **prefer both** unless I say otherwise:
produce `coffee-extraction.pptx` and `coffee-extraction-medavis.pptx`. Suggest a landing
title from the outline (or "Coffee Extraction"), confirm with me, then pass
`--template both --landing-title "..."`.

### C. Verify

```bash
python tests/smoke-deck/verify_deck.py <build_dir>/coffee-extraction \
  --host cursor \
  --skill-root ~/.cursor/skills/codex-ppt
```

Show the full BASELINE and TARGET output verbatim. Confirm T6 reports
`selected_backend='codex-gpt-image'` (or an equivalent specific label that
normalizes to the codex-gpt-image family — not `GenerateImage`).

### D. On failure — strict fix loop (repeat until green or blocked)

1. **Reproduce & isolate**: quote the failing check / error; name the layer
   (skill docs/prose, script, install drift, verifier, host tooling, bridge auth).
2. **Root cause**: inspect fork source (and unit tests). Do not patch symptoms.
3. **Failing test first** when the bug is in Python helpers/scripts:
   add or extend a unit test under `skills/codex-ppt/scripts/tests/`, see RED,
   then implement the smallest fix in the fork.
4. **Verify units**: full
   `python -m unittest discover -s skills/codex-ppt/scripts/tests -v` must be OK.
5. **Re-sync install** from fork → `~/.cursor/skills/codex-ppt`; re-confirm match.
6. **Re-run smoke** from step B (new `<build_dir>` suffix like `-fix1` unless I
   say to reuse), then step C.
7. **Report** each cycle: root cause, files changed (fork paths only), unit
   result, smoke result. Then **stop and wait** — do not commit.

If you are blocked (missing credentials, ambiguous product decision, need a
commit), stop and ask me with options.

### E. Success report

When BASELINE is green and T1/T2/T3/T6/T7 pass: summarize backend used
(`codex-gpt-image`), deck path, image sizes (note T5), and any remaining TARGET
notes. Remind me that changes are uncommitted until I approve a commit.
```
