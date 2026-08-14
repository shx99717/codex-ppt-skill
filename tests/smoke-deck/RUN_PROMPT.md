# Portable run prompt

A single, copy-paste prompt for running the smoke-deck regression test. Paste it as-is into a
fresh Codex, Claude Code, or Cursor session — no editing needed. It self-detects which of the
three it's running in, asks you where to put the output, then generates and verifies the deck
and reports BASELINE/TARGET results.

Use this the same way before and after any change to the skill: it always runs against whatever
version of `codex-ppt` is currently installed for that host.

**Host-pinned smoke + strict fix loop** (recommended when chasing bugs across agents one by one;
keeps fork and installed skill in sync; no commits without your OK):

| Host | Prompt file |
|------|-------------|
| Cursor (`GenerateImage` hard-pin) | [`RUN_PROMPT_cursor.md`](RUN_PROMPT_cursor.md) |
| Cursor + `codex-gpt-image` hard-pin | [`RUN_PROMPT_cursor_codex-gpt-image.md`](RUN_PROMPT_cursor_codex-gpt-image.md) |
| Claude Code (`codex-gpt-image` FAST) | [`RUN_PROMPT_claude.md`](RUN_PROMPT_claude.md) |
| Claude Code (`codex-gpt-image` GATED / interactive) | [`RUN_PROMPT_claude_interactive.md`](RUN_PROMPT_claude_interactive.md) |
| Codex (`image_gen`) | [`RUN_PROMPT_codex.md`](RUN_PROMPT_codex.md) |

See also [`../../docs/fork/DESIGN_PROMPT.md`](../../docs/fork/DESIGN_PROMPT.md) for resuming the *design* work on
the fork's improvement goals — use that one to pick up a conversation, this one to check a
result.

---

```
Use the codex-ppt skill to run its smoke-deck regression test end to end, then report the result.

## Setup

1. Locate the codex-ppt-skill repository (expected at d:/git/codex-ppt-skill; if not found
   there, search for a directory containing tests/smoke-deck/source.md, or ask me for the path).
   All paths below are relative to its root.
2. Identify which environment you are running in, and use it to set --host and --skill-root for
   later:

   | Environment | --host        | --skill-root                  |
   |-------------|---------------|--------------------------------|
   | Codex CLI   | codex         | ~/.codex/skills/codex-ppt      |
   | Claude Code | claude-code   | ~/.claude/skills/codex-ppt     |
   | Cursor      | cursor        | ~/.cursor/skills/codex-ppt     |

3. Run: python tests/smoke-deck/verify_deck.py --preflight
   If it reports missing dependencies, run the bootstrap command it prints, then re-check. If
   bootstrap itself fails, stop and show me the error instead of continuing.
4. Ask me where to put the build folder for this run (suggest a default like
   tests/smoke-deck/runs/<today's date>-<time>, e.g. tests/smoke-deck/runs/20260809-1630, but
   use whatever I answer). Call this <build_dir> below.

## Generate the deck

Use the codex-ppt skill to build a deck from tests/smoke-deck/source.md.

Fixed contract for this deck -- do not deviate:
- Output base directory: <build_dir>
- Deck name: coffee-extraction
- Exactly 3 slides
- Slide 1 must be written in Chinese
- Slide 2 must be written in English
- Slide 3 must mix Chinese and Latin script on the same slide
- Visual style: use the built-in style 清爽专业风
- Aspect ratio: 16:9 is the default locked ratio unless the run recorded another in `deck_spec.json` / `slide_jobs.json`. Old 3:2 image folders fail the 16:9 baseline.

Titles, key points, layout roles, and composition are yours to decide from the source content.

Gate handling for this run:
- Outline: pre-approved. Write outline.md and continue without waiting for my confirmation.
- Style: already pinned above. Do not offer style options.
- Sample slide: pre-approved. Accept the first sample and continue without waiting.
- Image backend: do NOT assume. Actively check which image generation backends are callable in
  this environment, state what you checked and what you selected, then proceed without waiting
  for my confirmation.

Generate speaker notes and assemble the .pptx.
Template mode: pre-approved **no template** (`--template none`). Do not ask; plain `{deck}.pptx` only.

## Verify and report

Run:
python tests/smoke-deck/verify_deck.py <build_dir>/coffee-extraction --host <detected host> --skill-root <detected skill root>

Show me the full BASELINE and TARGET output verbatim, and tell me in one or two sentences
whether this run passed or regressed compared to the unmodified skill.
```
