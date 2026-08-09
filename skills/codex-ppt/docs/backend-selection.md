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

## Preference order by host

| Host | Prefer first | Then | Else |
|------|--------------|------|------|
| Cursor | `GenerateImage` (native) | `codex-gpt-image` if installed | `scripts/image_gen.py` |
| Codex | `image_gen` (native) | `scripts/image_gen.py` | — |
| Claude Code | `codex-gpt-image` if installed | `scripts/image_gen.py` | — (no native) |

## Menu requirements

When presenting options, annotate each available choice with resolution/capability notes, auth path, cost hints if known, and whether reference-image / edit mode works. Recommend one option; wait for the user to lock a **specific** label.

## Lock and persist

- Lock a **specific** `selected_backend` label such as `GenerateImage`, `image_gen`, `codex-gpt-image`, or `scripts/image_gen.py`.
- **Forbidden locks:** generic `"built-in image tool"`; OpenClaw / `image_generate`; invented Claude Code native names.
- After the user locks a label, write it into `deck_spec.json` *before* `prepare_slide_prompts.py` via `sample_generation_method` (`backend_used` / `tool_name`) and/or `selected_image_backend`. Prefer also passing `--selected-backend <exact label>` to prepare. That copies into `slide_jobs.json` → `selected_backend` / per-job `expected_backend`.
- Keep the lock for the whole deck. Subagents must not switch backends.

## When CLI is allowed

Use `scripts/image_gen.py` only when no preferred host-native/bridge path is available or usable, the preferred tool failed for a required capability, the user explicitly asks for API/CLI or a third-party provider, or the requested capability is unavailable on the preferred path.

Do not recommend CLI merely for `--out` paths, local file convenience, or automation ease.

CLI/API fallback loads `~/.codex-ppt-skill/.env` automatically. Ask for `OPENAI_API_KEY` only after CLI is intentionally selected and reports missing config, after auth/base URL/model errors, or when the user wants to change API settings. Configure with `scripts/codex_ppt_runtime.py config --api-key`.

If CLI/API fallback is selected, read `cli-api-fallback.md` before generating images. For API key, base URL, model, and `.env` settings, read `image-model-configuration.md` only after the fallback CLI reports missing/invalid config, or when the user explicitly wants to change those settings.

## Confirmation

Present the available options (A/B/C…) with a clear recommendation, then wait. Example shape:

```text
Host: Cursor. Probe + prose check found:
  A) GenerateImage (native, recommended)
  B) codex-gpt-image (installed bridge)
  C) scripts/image_gen.py (CLI; needs API key)
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
