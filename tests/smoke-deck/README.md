# codex-ppt smoke deck

A small, repeatable end-to-end test fixture for the codex-ppt skill.

It is deliberately two things at once:

- a **regression smoke test** — re-run it after a change and confirm nothing broke;
- a **progress signal** — a second tier of assertions describes behavior the skill does *not* have yet,
  and turns green as improvements land.

Every pass generates **exactly 3 images**.

## What it covers

- The full 7-phase workflow, end to end, producing a valid `.pptx`
- Subagent dispatch, result recording, and the slide state machine (guaranteed: 3 slides = 1 sample + 2 dispatched)
- Backend detection, asserted against a per-host expectation matrix
- Multilingual decks: slide 1 Chinese, slide 2 English, slide 3 mixed CJK+Latin
- Layout variation (the "don't repeat the same blueprint" rule)
- Speaker-note mapping from `speech.md` into the PPT

## What it does not cover

Cross-model quality benchmarking, required source images (strict input assets), the sample rejection
loop, and custom styles from the personal style library. All are out of scope by design — see
"Known coverage gap" below for the one that is a deliberate trade rather than simple omission.

## Quick start

For repeated runs (e.g. re-checking after every change to the skill), see [`RUN_PROMPT.md`](RUN_PROMPT.md)
— a single copy-paste prompt that works unedited in Codex, Claude Code, or Cursor. It self-detects the
host, asks where to put the output, and reports the verifier's result at the end. The manual steps below
are for when you need more control (e.g. walking the gates by hand in GATED mode).

---

## 0. Preflight

Run before invoking the agent. It resolves the shared-runtime interpreter for your platform and checks
that the assembly dependencies are importable.

```bash
python tests/smoke-deck/verify_deck.py --preflight
```

If it reports missing dependencies, it prints the exact bootstrap command to run. Do not start a test
run until preflight is clean — otherwise the run will fail at the final assembly step for reasons that
have nothing to do with what you changed.

---

## 1. Pick a run id

Each run gets its own directory so you can diff before/after a change instead of clobbering:

```
tests/smoke-deck/runs/<run-id>/coffee-extraction/
```

Use a timestamp, e.g. `20260809-1630`. `runs/` is gitignored.

---

## 2. Choose a mode

### FAST mode

Use this after most code changes. Every gate that the skill permits skipping is pre-approved, so the
run is close to unattended.

**Backend detection is deliberately NOT pre-answered.** The agent must still probe and choose for real —
only the human confirmation is skipped. The verifier then checks the choice against the host matrix, so
FAST still catches a wrong backend without you watching.

Invocation prompt (copy verbatim, replacing `<run-id>`):

```text
Use the codex-ppt skill to build a deck from tests/smoke-deck/source.md.

Fixed contract for this deck — do not deviate:
- Output base directory: tests/smoke-deck/runs/<run-id>
- Deck name: coffee-extraction
- Exactly 3 slides
- Slide 1 must be written in Chinese
- Slide 2 must be written in English
- Slide 3 must mix Chinese and Latin script on the same slide
- Visual style: use the built-in style 清爽专业风
- Aspect ratio: 16:9

Titles, key points, layout roles and composition are yours to decide from the source content.

Gate handling for this run:
- Outline: pre-approved. Write outline.md and continue without waiting for my confirmation.
- Style: already pinned above. Do not offer style options.
- Sample slide: pre-approved. Accept the first sample and continue without waiting.
- Image backend: do NOT assume. Actively check which image generation backends are callable in this
  environment, state what you checked and what you selected, then proceed without waiting for my
  confirmation.

Generate speaker notes, assemble the .pptx, and report the deck directory when done.
```

### GATED mode

Use this when you are actively working on the review gate or the backend selection menu. Nothing is
pre-approved; you walk every gate.

Invocation prompt (copy verbatim, replacing `<run-id>`):

```text
Use the codex-ppt skill to build a deck from tests/smoke-deck/source.md.

Fixed contract for this deck — do not deviate:
- Output base directory: tests/smoke-deck/runs/<run-id>
- Deck name: coffee-extraction
- Exactly 3 slides
- Slide 1 must be written in Chinese
- Slide 2 must be written in English
- Slide 3 must mix Chinese and Latin script on the same slide
- Visual style: use the built-in style 清爽专业风
- Aspect ratio: 16:9

Titles, key points, layout roles and composition are yours to decide from the source content.

Stop at every approval gate and wait for me.
```

#### Gate checklist

| Gate | What you are checking |
|---|---|
| **Outline** | `outline.md` written at `runs/<run-id>/coffee-extraction/`, 3 slides, per-slide language honored — and it **stops** before creating `deck_spec.json`, `speech.md`, or `prompts/` |
| **Backend** | Did it actually probe, or assume from the agent name? Does it name a host-correct backend (see matrix)? Does its stated reasoning match reality? *This is where the Cursor detection bug surfaces.* |
| **Sample** | Text legible, especially CJK. Style matches 清爽专业风. 16:9. No stray slide number. |
| **Pre-assembly review** | *Placeholder — this gate does not exist yet. Target assertion T1 fails until it does.* |

---

## 3. Backend expectation matrix

| Host | Acceptable `backend_used` |
|---|---|
| Codex | built-in `image_gen` |
| Claude Code | `codex-gpt-image` |
| Cursor | `GenerateImage` **or** `codex-gpt-image` |

**An unrequested fallback to `scripts/image_gen.py` is a failure on every host.** `codex-gpt-image` is
expected to be installed on all three, so falling through to the CLI/API path without being asked can
only mean backend detection failed.

If you *deliberately* want to test the CLI/API path, pass `--allow-cli-fallback` to the verifier.

---

## 4. Verify

```bash
python tests/smoke-deck/verify_deck.py tests/smoke-deck/runs/<run-id>/coffee-extraction \
  --host cursor \
  --skill-root ~/.cursor/skills/codex-ppt
```

`--host` is required and must be one of `codex`, `claude-code`, `cursor`.
`--skill-root` is optional; it enables the cross-platform docs check (T7).

### Pass/fail semantics

The script always runs both tiers and prints two sections.

- **BASELINE** — must pass against the unmodified skill. **The exit code reflects baseline only.**
  A non-zero exit means something regressed.
- **TARGET** — describes behavior the skill does not have yet. Reported as a progress counter
  (`TARGET 0/7 satisfied`). Target failures never affect the exit code; they are the roadmap.

---

## Known coverage gap

Pinning the style keeps the visual baseline stable across runs — the approved sample slide is the deck's
style anchor, so a floating style would move the baseline every time. The cost is that the 2-3 option
**style menu never renders** in either mode.

To exercise the style menu, delete the `Visual style:` line from the invocation prompt. That run is then
not baseline-comparable, so treat it as a one-off rather than a regression pass.
