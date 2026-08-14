# Claude Code — INTERACTIVE (GATED) smoke + strict fix loop

Paste the fenced block below **verbatim** into a fresh Claude Code session.
This run is pinned to **Claude Code** only. Do not self-detect another host.
Claude Code has no native image tool; this run expects **`codex-gpt-image`**.

This is the **interactive** sibling of
[`RUN_PROMPT_claude.md`](RUN_PROMPT_claude.md) (FAST / unattended gates).
Same host pins, same pass criteria, same fix loop — but **stop and wait at
every gate**. Work with me; do not auto-continue.

Canonical skill source: `d:/git/codex-ppt-skill/skills/codex-ppt`
Installed skill this host must run: `~/.claude/skills/codex-ppt`
Bridge skill required: `~/.claude/skills/codex-gpt-image` (Codex OAuth image path)

---

```
You are running the codex-ppt smoke-deck on CLAUDE CODE only, in INTERACTIVE
(GATED) mode, with a strict engineering fix loop, and with the image backend
HARD-PINNED to `codex-gpt-image` once I confirm the lock. Do not switch hosts.
Do not invent a Claude Code native image tool. Do not commit or push unless I
explicitly say so.

If `tests/smoke-deck/RUN_PROMPT_claude.md` is also in context, IGNORE its FAST
gate handling. This interactive contract wins for how you talk to me. Keep that
file only as the sibling reference for host pins, pass criteria, and the fix loop.

## Interaction rules (non-negotiable)

1. **Stop and wait** at every gate in Procedure B. Do not pre-approve, do not
   skip waiting, do not "FAST" anything.
2. After each gate, show what you did, then ask me with **A/B/C options**
   (plus Other when useful). Wait for my reply before the next step.
3. Do not create `deck_spec.json`, prompt jobs, slide images, or `.pptx` before
   the matching gate is approved.
4. Do not auto-accept the sample. Do not auto-record `record_user_review.py
   --approve` until I say the slide is OK.
5. Ask only real decisions. Routine progress can be a short status line, then
   the next gate question.
6. If you are blocked (auth, missing bridge, ambiguous product choice), stop
   and ask with options. Do not silently fall back to CLI.

## Host pins (fixed)

| Item | Value |
|------|-------|
| Environment | Claude Code |
| --host | claude-code |
| Installed skill | ~/.claude/skills/codex-ppt |
| Bridge skill | ~/.claude/skills/codex-gpt-image |
| Locked selected_backend (after I confirm) | codex-gpt-image |
| Fork repo root | d:/git/codex-ppt-skill |
| Canonical skill source | d:/git/codex-ppt-skill/skills/codex-ppt |
| Source article | tests/smoke-deck/source.md |

Acceptable backends for this host (verifier matrix): `codex-gpt-image`
(preferred / required for this run). Claude Code has no native image tool for
this skill. **This variant must lock and use only** `codex-gpt-image` for
sample + all slides (T6 must report `selected_backend='codex-gpt-image'`).
Unrequested `scripts/image_gen.py` / CLI fallback is a failure unless I
explicitly ask for `--allow-cli-fallback`.

## Non-negotiable engineering rules

1. **Installed skill must match the fork.** Before generating, and after every
   fix, sync:
   copy `d:/git/codex-ppt-skill/skills/codex-ppt` → `~/.claude/skills/codex-ppt`
   (replace the destination; exclude `__pycache__` / `*.pyc`). Verify with a
   file-hash or file-list compare that the install matches the fork (especially
   `scripts/record_user_review.py`, `scripts/probe_image_backends.py`,
   `scripts/prepare_slide_prompts.py`, `SKILL.md`).
2. **Edits land only in the fork repo** under `d:/git/codex-ppt-skill`
   (skill code/docs/tests). Never "fix only" the installed copy.
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
   `~/.claude/skills/codex-gpt-image`, run
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
  host tooling).

## Procedure

### A. Preflight (then ask — do not generate yet)

1. `cd d:/git/codex-ppt-skill`
2. Sync fork → `~/.claude/skills/codex-ppt` and confirm match.
3. Confirm `~/.claude/skills/codex-gpt-image/SKILL.md` exists.
4. Run codex-gpt-image `auth-status` (see rule 7). Stop if auth cannot be fixed.
5. `python tests/smoke-deck/verify_deck.py --preflight`
   If deps missing, run the printed bootstrap, then re-check. Stop if bootstrap fails.
6. **Gate — build_dir:** Ask me for `<build_dir>` (suggest
   `tests/smoke-deck/runs/<YYYYMMDD-HHMM>-claude-interactive`). Wait for my
   answer. Do not create the deck folder until I pick one.

### B. Generate (INTERACTIVE contract — stop at every gate)

Use the **installed** codex-ppt skill to build from
`tests/smoke-deck/source.md`.

Fixed deck contract (do not deviate unless I explicitly change it):

- Output base directory: `<build_dir>`
- Deck name: `coffee-extraction`
- Exactly 3 slides
- Slide 1 Chinese; slide 2 English; slide 3 mixed Chinese + Latin
- Visual style: built-in `清爽专业风` (do not offer a style menu — smoke baseline)
- Titles / points / layout / composition: decide from the source, then show me

#### Gate 1 — Outline

Write `outline.md` only (no `deck_spec.json`, no prompts, no images, no PPTX).
Show the 3-slide outline with per-slide language, role, and key points.
Ask me to approve / edit. Wait.

#### Gate 2 — PPT ratio

Ask `16:9` / `4:3` / `3:2` **before** backend lock. Recommend **16:9** on
Claude Code. Wait. Persist the locked `aspect_ratio`. gpt-image-2 `--size`
must match: `2560x1440` (16:9), `2560x1920` (4:3), `2400x1600` (3:2).

#### Gate 3 — Image backend

Probe callable backends in Claude Code (no native image tool; confirm
`codex-gpt-image` via probe + prose-check). State what you checked.
Recommend locking `selected_backend=codex-gpt-image`. Ask me to confirm.
Do **not** lock until I reply. If I pick CLI, stop and confirm
`--allow-cli-fallback` before using it. Persist the lock into
`deck_spec.json` / prepare with `--selected-backend codex-gpt-image`.
Every final slide image must use that locked path.

#### Gate 4 — Sample slide

Generate **exactly one** representative sample (prefer a content slide, not
only a cover). Show me the full-res image and measured WxH vs locked ratio
(2% relative). Ask me to accept / reject / regenerate. Wait.
After I accept: record `sample_generation_method` (backend, tool, mode,
`--size`, approved path) and mark that slide `sample_approved`.

#### Gate 5 — Remaining slides + review

Prepare jobs, dispatch remaining slides (subagents if available). After each
wave is recorded: **stop**. Show each new full-res `origin_image/slide_XX.png`.
On my approve, run `record_user_review.py --approve` for that slide. Do not
start the next wave (or assemble) until the current wave is reviewed.
FAST skip-waiting is forbidden in this run.

#### Gate 6 — Template + landing title (before any PPTX exists)

Ask template mode: **no template** / **medavis** / **both**.
For this smoke deck, **prefer both** unless I say otherwise:
`coffee-extraction.pptx` and `coffee-extraction-medavis.pptx`.
Suggest a landing title from the outline (or "Coffee Extraction"). Confirm
with me **before** any PPTX of this run exists, then pass
`--template both --landing-title "..." --aspect-ratio <locked>`.
Medavis wrap is N+2 slides (landing + content + ending).

Write `speech.md`, then assemble only after Gate 6 is answered.

### C. Verify

```bash
python tests/smoke-deck/verify_deck.py <build_dir>/coffee-extraction \
  --host claude-code \
  --skill-root ~/.claude/skills/codex-ppt
```

Show the full BASELINE and TARGET output verbatim. Confirm T6 reports
`selected_backend='codex-gpt-image'` (or an equivalent specific label that
normalizes to the codex-gpt-image family). Use **absolute paths** in the
success report for the deck folder and both PPTX files.

### D. On failure — strict fix loop (repeat until green or blocked)

1. **Reproduce & isolate**: quote the failing check / error; name the layer
   (skill docs/prose, script, install drift, verifier, host tooling, bridge auth).
2. **Root cause**: inspect fork source (and unit tests). Do not patch symptoms.
3. **Failing test first** when the bug is in Python helpers/scripts:
   add or extend a unit test under `skills/codex-ppt/scripts/tests/`, see RED,
   then implement the smallest fix in the fork.
4. **Verify units**: full
   `python -m unittest discover -s skills/codex-ppt/scripts/tests -v` must be OK.
5. **Re-sync install** from fork → `~/.claude/skills/codex-ppt`; re-confirm match.
6. **Re-run smoke** from step B (new `<build_dir>` suffix like `-fix1` unless I
   say to reuse), still INTERACTIVE — do not switch to FAST. Then step C.
7. **Report** each cycle: root cause, files changed (fork paths only), unit
   result, smoke result. Then **stop and wait** — do not commit.

If you are blocked (missing credentials, ambiguous product decision, need a
commit), stop and ask me with options.

### E. Success report

When BASELINE is green and T1/T2/T3/T6/T7 pass: summarize backend used
(`codex-gpt-image`), **absolute** deck path, image sizes, PPTX paths, and any
remaining TARGET notes. Remind me that changes are uncommitted until I approve
a commit.
```
