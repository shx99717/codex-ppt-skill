Execute the implementation plan at `docs/plans/2026-08-13-generateimage-schema-workaround.md` in this repository (`D:/git/codex-ppt-skill`).

The plan is fully SELF-CONTAINED: it carries every decision, convention, project rule, and
verification step you need. You do NOT need any prior chat session or memory file, and you do
NOT need me to re-explain anything — start fresh and rely on the plan.

Please:
1. Read the entire plan first (especially Section 0 "Full Context" and any appendices).
2. Execute it task-by-task. If you have the `executing-plans` skill available, use it to drive
   the execution; otherwise just follow the tasks in order. After each task, run the verification
   it specifies.
3. The end state must satisfy the plan's "Verification Summary" / acceptance checklist.
4. Hard guardrails for this task:
   - Work on existing branch `feature/SQ5GEN-195-improve-ppt-ratios`. Do not create another branch.
   - Docs/worker/smoke/README/CHANGELOG only. Do NOT add a Python helper or new unit tests.
   - Do NOT change `SKILL.md` YAML `name` / `description`.
   - Do NOT offer or document GenerateImage as valid for 16:9 or 4:3 locks.
   - Do NOT omit GenerateImage for 3:2 decks just because the schema enum lacks `3:2`.
   - Do NOT rewrite frozen `docs/plans/2026-08-13-improve-ppt-ratios.md`.
   - Do NOT resume or assemble the paused FAST smoke at `tests/smoke-deck/runs/20260813-1945-cursor/`.
   - Do NOT stretch, letterbox, or crop as a success path.
   - Do NOT commit unless I explicitly ask (`[SQ5GEN-195]` if I do).
   - Do NOT run collection install/uninstall scripts. Optional re-sync of `skills/codex-ppt` → `~/.cursor/skills/codex-ppt` only after GREEN if I will continue a Cursor deck.
5. When done and verification is green, report results and offer a code review.

If something is genuinely ambiguous or you hit a blocker, ask via the question channel; otherwise
proceed autonomously through the whole plan.
