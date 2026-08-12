# Codex — FAST smoke + strict fix loop

Paste the fenced block below **verbatim** into a fresh Codex session.
This run is pinned to **Codex** only (native `image_gen`). Do not self-detect another host.

See also Cursor / Claude bridge variants in [`RUN_PROMPT.md`](RUN_PROMPT.md).

Canonical skill source: `d:/git/codex-ppt-skill/skills/codex-ppt`
Installed skill this host must run: `~/.codex/skills/codex-ppt`

---

```
You are running the codex-ppt smoke-deck on CODEX only, in FAST mode, with a
strict engineering fix loop. Do not switch hosts. Do not commit or push unless
I explicitly say so.

## Host pins (fixed)

| Item | Value |
|------|-------|
| Environment | Codex CLI |
| --host | codex |
| Installed skill | ~/.codex/skills/codex-ppt |
| Fork repo root | d:/git/codex-ppt-skill |
| Canonical skill source | d:/git/codex-ppt-skill/skills/codex-ppt |

Acceptable backends for this host (verifier matrix): built-in `image_gen`.
Unrequested `scripts/image_gen.py` / CLI fallback is a failure unless I
explicitly ask for `--allow-cli-fallback`.

## Non-negotiable rules

1. **Installed skill must match the fork.** Before generating, and after every
   fix, sync:
   copy `d:/git/codex-ppt-skill/skills/codex-ppt` → `~/.codex/skills/codex-ppt`
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

## Pass criteria for THIS fork run

- **BASELINE**: all checks must PASS (exit code of verify_deck.py).
- **TARGET**: T1 (review recorded), T2 (no hardcoded Chinese rule on EN slide),
  T3 (per-slide language), T6 (specific selected_backend), and **T7** (no
  Unix-only `.venv/bin/python` in skill docs; scored on Windows when
  `--skill-root` is passed) must PASS — those goals are already implemented.
  Investigate any other TARGET miss (T4/T5); fix if it is a real skill defect;
  ask me if it looks environment-only (e.g. image width / host tooling).

## Procedure

### A. Preflight

1. `cd d:/git/codex-ppt-skill`
2. Sync fork → `~/.codex/skills/codex-ppt` and confirm match.
3. `python tests/smoke-deck/verify_deck.py --preflight`
   If deps missing, run the printed bootstrap, then re-check. Stop if bootstrap fails.
4. Ask me for `<build_dir>` (suggest
   `tests/smoke-deck/runs/<YYYYMMDD-HHMM>-codex`). Wait for my answer.

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
- Image backend: do NOT assume — probe callable backends in Codex (expect
  native `image_gen`), state what you checked and what you locked as
  `selected_backend`, then continue without waiting for confirmation
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
  --host codex \
  --skill-root ~/.codex/skills/codex-ppt
```

Show the full BASELINE and TARGET output verbatim.

### D. On failure — strict fix loop (repeat until green or blocked)

1. **Reproduce & isolate**: quote the failing check / error; name the layer
   (skill docs/prose, script, install drift, verifier, host tooling).
2. **Root cause**: inspect fork source (and unit tests). Do not patch symptoms.
3. **Failing test first** when the bug is in Python helpers/scripts:
   add or extend a unit test under `skills/codex-ppt/scripts/tests/`, see RED,
   then implement the smallest fix in the fork.
4. **Verify units**: full
   `python -m unittest discover -s skills/codex-ppt/scripts/tests -v` must be OK.
5. **Re-sync install** from fork → `~/.codex/skills/codex-ppt`; re-confirm match.
6. **Re-run smoke** from step B (new `<build_dir>` suffix like `-fix1` unless I
   say to reuse), then step C.
7. **Report** each cycle: root cause, files changed (fork paths only), unit
   result, smoke result. Then **stop and wait** — do not commit.

If you are blocked (missing credentials, ambiguous product decision, need a
commit), stop and ask me with options.

### E. Success report

When BASELINE is green and T1/T2/T3/T6/T7 pass: summarize backend used, deck path,
and any remaining TARGET notes. Remind me that changes are uncommitted until I
approve a commit.
```
