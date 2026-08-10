Execute the implementation plan at `docs/plans/2026-08-09-pre-assembly-user-review-gate.md` in this repository (`d:/git/codex-ppt-skill`).

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
   - Do NOT modify `skills/codex-ppt/scripts/assemble_ppt.py`.
   - Do NOT implement a contact sheet, backend-selection gate, or multilingual fixes.
   - Do NOT commit unless I explicitly ask (if committing: Conventional Commits prefixed with `[SQ5GEN-195]`).
   - Do NOT run collection install/uninstall scripts; edit only the fork under `skills/codex-ppt/`.
   - Do not re-litigate decisions in Section 0.2.
5. When done and verification is green, report results and offer a code review.

If something is genuinely ambiguous or you hit a blocker, ask via the question channel; otherwise
proceed autonomously through the whole plan.
