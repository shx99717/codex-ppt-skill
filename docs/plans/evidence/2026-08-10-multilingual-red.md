# RED evidence — multilingual deck support (2026-08-10)

## Baseline

```text
rg -n "Render Chinese text|language.*, \"Chinese\"|deck.get(\"language\"" skills/codex-ppt/scripts/prepare_slide_prompts.py
```

Observed:

- `:208` `deck.get("language", "Chinese")` — deck-only, Chinese default; ignores per-slide language
- `:262` unconditional `Render Chinese text exactly and legibly; avoid garbled characters.`

Worker/docs:

- `slide-worker.md` — `Chinese text is readable and not garbled`
- `slide-generation-and-subagents.md` — example `"language": "Chinese"`

## Rationalizations to defeat

- **R1:** “Default Chinese is fine for all decks.”
- **R2:** “The Chinese render line is harmless on English slides.”
- **R3:** “Deck-level language is enough; no per-slide field.”

Stop: no product edits in this RED step.
