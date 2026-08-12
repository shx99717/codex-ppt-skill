Execute the implementation plan at `docs/plans/2026-08-12-medavis-ppt-template.md` in this repository (`D:/git/codex-ppt-skill`).

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
   - Do NOT re-litigate decisions in Section 0.2.
   - Do NOT skip Section 0.6 review patches (gitignore negation, title color/cover, visual smoke, rg docs list, 16:9 note).
   - Do NOT add a separate assembler script or a shared-library refactor.
   - Do NOT introduce a custom/user template path override in this change.
   - Do NOT cover the medavis logo with full-bleed images.
   - Do NOT leave layout ghost title/body text visible on content slides.
   - Do NOT commit unless I explicitly ask.
   - Do NOT run collection install/uninstall scripts; edit only `skills/codex-ppt/` (+ repo docs/CHANGELOG/`.gitignore` as the plan requires).
5. When done and verification is green, report results and offer a code review.

If something is genuinely ambiguous or you hit a blocker, ask via the question channel; otherwise
proceed autonomously through the whole plan.
