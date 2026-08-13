# GREEN — GenerateImage schema vs pixels (2026-08-13)

After Tasks 2–7. Branch: `feature/SQ5GEN-195-improve-ppt-ratios`.

## Stale-instruction grep (live paths)

Command:

```bash
rg -n "pass aspect_ratio=.?3:2|pass \`aspect_ratio=\"3:2\"\`" skills/codex-ppt tests/smoke-deck/RUN_PROMPT_cursor.md README.md README_en.md README_ko.md docs/workflow.md docs/en/workflow.md docs/ko/workflow.md
```

Hits that **mandate** `3:2` with no enum fallback: **none**.

Remaining hits are the allowed **if-enum-includes-3:2** branch:

- `skills/codex-ppt/SKILL.md:49` — `if 3:2 is in the enum, pass aspect_ratio="3:2"; if not, pass ... 16:9`
- `skills/codex-ppt/prompts/slide-worker.md:29` — same + `Do not pass 3:2 when the schema rejects it`
- `skills/codex-ppt/docs/backend-selection.md:58` — same call recipe

`tests/smoke-deck/RUN_PROMPT_cursor.md`, READMEs, and workflow pages: **no** `Pass aspect_ratio="3:2"` mandate.

Frozen `docs/plans/2026-08-13-improve-ppt-ratios.md` was not edited (allowed to keep the old line).

## Positive greps

- `schema` present in `SKILL.md`, `backend-selection.md`, `slide-worker.md`
- `1536` present in `backend-selection.md` (table + call recipe + 16:9 hide example)
- Worker: `Do not switch to another backend because the enum lacks 3:2`
- Worker still: `If the parent locked 16:9 or 4:3, return a blocker`
- gpt-image-2 `--size` `2560x1440` still in zh/en/ko README and workflow pages
- `SKILL.md` YAML: `name: codex-ppt`; description unchanged (no workflow summary added)

## Appendix B / C mapping

| Scenario | New counter |
|----------|-------------|
| P1 enum lacks 3:2 → stall/switch | Worker + SKILL + smoke: pass legal landscape value, measure pixels, do not switch backends |
| P2 schema lists 4:3 → offer GI | SKILL overview + backend table: 4:3/16:9 args still 1536×1024; hide unless locked 3:2 |
| P3 worker passes 3:2 blindly | Worker: inspect enum; use `tool_aspect_ratio_argument` if set |
| P4 stretch | SKILL + call recipe: blocker, do not stretch/letterbox/crop |
| “Schema has 4:3 so pixels are 4:3” | backend-selection red flag + 2026-08-13 evidence |
| “Enum rejected 3:2 so GI unavailable” | “Enum rejects 3:2 ≠ GenerateImage is unavailable” |
| “Omit aspect_ratio, prompt only” | “prompt text is not enough” |
| “Switch to CLI” | “Do not switch to CLI just because the enum lacks 3:2” |

## Changelog

- Unreleased Fixes: do not instruct `aspect_ratio="3:2"` when schema rejects it
- Unreleased Documentation: schema-vs-pixels in skill/worker/smoke/README/workflow

Review follow-up (Important-1): `outline-style-and-sample.md` “Include at least” list and worker copy header now include `tool_aspect_ratio_argument` / `measured_size`; worker prefers the recorded tool argument when set.

## Not done (per plan)

- No Python helper, no new unit tests
- No commit
- Paused FAST smoke not resumed
- Install re-sync optional; not required for GREEN
