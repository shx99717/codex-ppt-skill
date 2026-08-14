Execute the implementation plan at `docs/plans/2026-08-13-medavis-template-v2.md` in this repository (`D:/git/codex-ppt-skill`).

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
   - Do NOT skip Section 0.7 review patches (4:3 canvas gate, keep add_slide object, host-conditional GenerateImage probe, real slide_jobs fixture, no v1 title-color asserts).
   - Do NOT restore header-band placement (`MEDAVIS_CONTENT_TOP=700000`) or add a second landing title textbox.
   - Do NOT stretch images by setting picture width and height independently to the slide box.
   - Do NOT letterbox or crop as a success path; refuse non-16:9 and regenerate.
   - Do NOT treat `tests/smoke-deck/runs/20260812-1725-cursor-interactive` 3:2 images as a GREEN assemble (they must fail the new gate).
   - Do NOT use `medavis-logo-original.png`.
   - Do NOT overwrite the bundled template file.
   - If a GenerateImage or codex-gpt-image 16:9 probe is not actually 16:9 within **2% relative**, STOP and ask — do not weaken the gate.
   - Do NOT commit unless I explicitly ask.
   - Do NOT run collection install/uninstall scripts; edit only `skills/codex-ppt/` (+ repo docs/CHANGELOG/`.gitignore`/tests as the plan requires).
5. When done and verification is green, report results and offer a code review.

If something is genuinely ambiguous or you hit a blocker, ask via the question channel; otherwise
proceed autonomously through the whole plan.
