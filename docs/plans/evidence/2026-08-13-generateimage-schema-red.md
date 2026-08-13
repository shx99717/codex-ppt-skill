# RED — GenerateImage schema vs pixels (2026-08-13)

Baseline before the call-recipe docs fix. Stale skill text still orders agents to pass `aspect_ratio="3:2"`.

## Grep hits (must exist before GREEN edits)

```
skills/codex-ppt/docs/backend-selection.md:82:
  A) GenerateImage (Cursor native image tool; pass aspect_ratio=3:2; recommended)

skills/codex-ppt/prompts/slide-worker.md:29:
- Cursor GenerateImage: only when locked ratio is 3:2; pass `aspect_ratio="3:2"`. Prompt text is not enough. If the parent locked 16:9 or 4:3, return a blocker instead of calling GenerateImage.

skills/codex-ppt/SKILL.md:49:
- Backend menu: ... Cursor `GenerateImage` ... **only** for 3:2, and pass `aspect_ratio="3:2"`. ...

tests/smoke-deck/RUN_PROMPT_cursor.md:108:
  GenerateImage`. Pass `aspect_ratio="3:2"` on GenerateImage. Every final slide image must be produced via Cursor
```

## Live pixel / schema evidence (Appendix A)

| Call | Schema | Pixels | Ratio |
|------|--------|--------|-------|
| `aspect_ratio="3:2"` | **rejected** (`Invalid enum value. Expected '1:1' \| '4:3' \| '3:4' \| '16:9' \| '9:16'`) | — | — |
| `aspect_ratio="16:9"` (sample slide) | accepted | **1536×1024** | exact 3:2 |
| `aspect_ratio="4:3"` (dedicated test) | accepted | **1536×1024** | exact 3:2 |

Optional schema re-check this execute session: not re-probed with a new image; the same Cursor `GenerateImage` tool descriptor in this chat still lists enum `1:1 | 4:3 | 3:4 | 16:9 | 9:16` (no `3:2`). Unchanged from Appendix A.

## Would-fail without this change (Appendix B)

- **P1:** Agent follows SKILL/worker/smoke “pass 3:2” → tool error → stall or switch to `codex-gpt-image` / CLI.
- **P2:** Agent trusts schema `4:3` and offers GenerateImage for a 4:3 lock → silent 3:2 pixels.
- **P3:** Subagent copies worker line with no enum fallback.
- **P4:** Stretch 1536×1024 onto a non-3:2 canvas to “fix” the mismatch.

Branch: `feature/SQ5GEN-195-improve-ppt-ratios`
