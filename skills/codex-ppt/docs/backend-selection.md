# Backend Selection

Read this before confirming the image backend or generating the first sample slide.

## Facts

- **Claude Code has no native image generation** (vision only). Do not invent a Claude Code native option.
- **Do not** present OpenClaw / `image_generate` as a supported image backend for this skill.
- Host-native tools that *do* exist: Codex `image_gen`, Cursor `GenerateImage`.
- Bridge: `codex-gpt-image` (when installed under `~/.claude/skills`, `~/.cursor/skills`, or `~/.codex/skills`).
- CLI/API fallback: `scripts/image_gen.py`.

## Hybrid probe

1. **Prose-check host-native tools** in the current runtime (Codex `image_gen`, Cursor `GenerateImage` only). The probe script cannot see IDE tools.
2. Run the probe for bridges/CLI signals:

```bash
python scripts/probe_image_backends.py
```

3. Build the menu from:
   - prose-detected host-native tools (when actually callable), plus
   - probe `candidates` with `"available": true` only.
4. Do not list unavailable CLI/bridge entries as choosable defaults.

## Preference order by host and locked ratio

Filter first: **do not list a backend that cannot produce the locked ratio.** Name the underlying model on every option.

| Backend | Underlying model | Shown when |
|---|---|---|
| `GenerateImage` | Cursor native image tool (no gpt-image-2 size API; pixels observed 1536×1024 even when argument is `16:9` or `4:3`; schema may lack `3:2`) | **3:2 only** |
| `image_gen` | Codex native gpt-image-2 | all ratios **if** the tool schema accepts `WIDTHxHEIGHT`; pass `--size` `2560x1440` / `2560x1920` / `2400x1600`. If the schema cannot express the locked ratio, **omit** `image_gen` from that menu and ask the user — do not invent pixel sizes. |
| `codex-gpt-image` | gpt-image-2 via Codex OAuth | all ratios; `--size` from the table above |
| `scripts/image_gen.py` | gpt-image-2 via API key | all ratios; `--size` from the table; last among *available* options |

| Host | Locked ratio | Prefer first | Then | Else |
|------|--------------|--------------|------|------|
| Cursor | 3:2 | `GenerateImage` (native) | `codex-gpt-image` if installed | `scripts/image_gen.py` |
| Cursor | 16:9 or 4:3 | `codex-gpt-image` if installed | `scripts/image_gen.py` | — (no GenerateImage) |
| Codex | any | `image_gen` if schema accepts `--size` | `scripts/image_gen.py` | — |
| Claude Code | any | `codex-gpt-image` if installed | `scripts/image_gen.py` | — (no native) |

## Menu requirements

When presenting options, annotate each available choice with resolution/capability notes, auth path, cost hints if known, and whether reference-image / edit mode works. Recommend one option; wait for the user to lock a **specific** label.

## Lock and persist

- Lock a **specific** `selected_backend` label such as `GenerateImage`, `image_gen`, `codex-gpt-image`, or `scripts/image_gen.py`.
- **Forbidden locks:** generic `"built-in image tool"`; OpenClaw / `image_generate`; invented Claude Code native names.
- Record the exact `selected_image_backend`, `aspect_ratio` and complete `planning.generation` method before combined plan approval. Runtime sample decisions belong to `plan_approvals.json`, not authored `sample_generation_method` or approval booleans in the spec. The compiler binds the approved method into jobs; a conflicting `--selected-backend` override is rejected.
- For the bundled CLI, explicitly approve model, size, quality and the operation policy. A text-only calibration may use `mode: generate`; image-conditioned production/source calibration uses `reference_mode: edit`. This keeps one approved backend with an explicit input-dependent endpoint policy. Replaying generate without references or silently changing to edit is forbidden. The managed adapter validates supported fields and forwards every verified input.
- Keep the lock for the whole deck. Subagents must not switch backends.

## GenerateImage call recipe

Cursor `GenerateImage` is 3:2-only in pixels. Offer it only when the locked ratio is 3:2. It has no gpt-image-2 `--size` API. Prose-check the live `GenerateImage` schema enum. If `3:2` is in the enum, pass `aspect_ratio="3:2"`. If not, pass a schema-legal landscape value (prefer `16:9`) and measure pixels. Do not pass `3:2` when the schema rejects it. A successful `4:3` or `16:9` argument is not proof of that ratio (2026-08-13: both returned 1536×1024). Gate `|(w/h)/1.5 - 1| <= 0.02`. If pixels are wrong: blocker. Do not assemble, stretch, letterbox, crop, or switch backends unless the user says so.

Keep `planning.generation.aspect_ratio` as the locked deck ratio (`3:2`). Store the approved tool argument in that configuration as `tool_aspect_ratio_argument`; record observed pixels as result/sample inspection evidence. Never add invented parameters to a live native tool schema.

Red flags:

- Schema lists `4:3` ≠ pixels are 4:3.
- Enum rejects `3:2` ≠ GenerateImage is unavailable for a 3:2 deck.
- Do not omit `aspect_ratio` and put 3:2 only in the prompt — prompt text is not enough.
- Do not switch to CLI just because the enum lacks `3:2`.
- Do not stretch 3:2 pixels onto a 4:3/16:9 canvas.

## When CLI is allowed

Use `scripts/image_gen.py` only when no preferred host-native/bridge path is available or usable, the preferred tool failed for a required capability, the user explicitly asks for API/CLI or a third-party provider, or the requested capability is unavailable on the preferred path.

Do not recommend CLI merely for `--out` paths, local file convenience, or automation ease.

CLI/API fallback loads `~/.codex-ppt-skill/.env` automatically. Ask for `OPENAI_API_KEY` only after CLI is intentionally selected and reports missing config, after auth/base URL/model errors, or when the user wants to change API settings. Configure with `scripts/codex_ppt_runtime.py config --api-key`.

If CLI/API fallback is selected, read `cli-api-fallback.md` before generating images. For API key, base URL, model, and `.env` settings, read `image-model-configuration.md` only after the fallback CLI reports missing/invalid config, or when the user explicitly wants to change those settings.

## Confirmation

Present the available options (A/B/C…) with a clear recommendation, then wait. Example shape:

```text
Host: Cursor. Locked ratio: 16:9. Probe + prose check found:
  A) codex-gpt-image (gpt-image-2 via Codex OAuth; pass --size 2560x1440; recommended)
  B) scripts/image_gen.py (gpt-image-2 via API key; pass --size 2560x1440)
GenerateImage is hidden (3:2 only; probes returned 1536×1024).
I recommend A. Which backend should we lock for this deck?
```

Cursor 3:2 example:

```text
Host: Cursor. Locked ratio: 3:2. Probe + prose check found:
  A) GenerateImage (Cursor native image tool; 3:2 pixels; if schema has no 3:2, pass 16:9 then measure; recommended)
  B) codex-gpt-image (gpt-image-2 via Codex OAuth; pass --size 2400x1600)
  C) scripts/image_gen.py (gpt-image-2 via API key; pass --size 2400x1600)
I recommend A. Which backend should we lock for this deck?
```

Claude Code example:

```text
Host: Claude Code (no native image tool). Probe found:
  A) codex-gpt-image (installed, recommended)
  B) scripts/image_gen.py (CLI; needs API key)
I recommend A. Which backend should we lock for this deck?
```

Wait for confirmation before generating the sample slide. If the user questions the backend, resolve that before continuing.
