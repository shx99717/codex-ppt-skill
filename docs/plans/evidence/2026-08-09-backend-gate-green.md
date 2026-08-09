# GREEN evidence — backend selection gate (2026-08-09)

## Family classification

```text
python -c "from record_slide_result import _backend_family as f; ..."
```

| Label | Family |
|-------|--------|
| `GenerateImage` | `generateimage` |
| `codex-gpt-image` | `codex-gpt-image` |
| `scripts/image_gen.py` | `cli-api-fallback` |
| `Codex image_gen` | `builtin-image-gen` |
| `image_generate` | `''` (unsupported OpenClaw) |

## Probe

`python scripts/probe_image_backends.py` returns JSON with `host_native_note`, `preference_hints`, and `candidates` (`available` flags). Host-native tools are prose-only.

## T6 token check

`GenerateImage` → normalized `generateimage` contains token `generateimage` → T6-compatible.

Note: `image_generate` → `imagegenerate` also contains T6 token `imagegen`; **smoke-deck now excludes OpenClaw** via `is_specific_backend_label()` / `backend_family` → `unknown`. Skill-side still hard-rejects at `_validate_backend`.

## Guards

- `assemble_ppt.py` unmodified
- Goal 1 `record_user_review.py` still present; 7/7 review tests OK
- Unit tests: `test_backend_family` 8/8, `test_probe_image_backends` 4/4, total script tests 19/19 OK

## R1–R4 mapped to docs

| R | Defeat |
|---|--------|
| R1 Cursor ≠ Codex/OpenClaw | `backend-selection.md` preference table; Cursor prefers `GenerateImage` |
| R2 Claude native | Explicit “Claude Code has no native image generation” |
| R3 generic lock | Forbidden locks include `"built-in image tool"`; require specific label |
| R4 worker drift | `slide-worker.md` returns `backend_used=<exact locked label>` |

Minimal `slide_jobs.json` shape for T6:

```json
{
  "selected_backend": "GenerateImage",
  "slides": []
}
```
