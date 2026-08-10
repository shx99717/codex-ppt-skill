# RED evidence — backend selection gate (2026-08-09)

## Baseline commands

```text
rg -n "built-in image tool|image_generate|GenerateImage|codex-gpt-image|probe_image" \
  skills/codex-ppt/docs/backend-selection.md skills/codex-ppt/prompts/slide-worker.md
```

Observed: two-backend world only — Codex `image_gen` / OpenClaw `image_generate` vs CLI.
`GenerateImage` / `codex-gpt-image` / `probe_image` absent from the decision menu.
No `probe_image_backends.py`.

```text
python -c "from record_slide_result import _backend_family as f; ..."
```

Observed families:

| Label | Family today |
|-------|----------------|
| `GenerateImage` | `''` |
| `codex-gpt-image` | `''` |
| `scripts/image_gen.py` | `cli-api-fallback` |
| `image_generate` | `built-in-image-tool` (OpenClaw still treated as builtin) |

Empty family for Cursor / bridge labels → `record_slide_result` can `SystemExit("Backend mismatch")`.

## Rationalizations to defeat

- **R1:** “We’re in Cursor so built-in must be Codex `image_gen` (or leftover OpenClaw `image_generate`).”
- **R2:** “Claude Code has a built-in image tool.”
- **R3:** “Confirming ‘use built-in’ is enough; no need to name GenerateImage / codex-gpt-image.”
- **R4:** “Worker can return `built-in image tool` regardless of what parent locked.”

Stop: no skill product edits in this RED step.
