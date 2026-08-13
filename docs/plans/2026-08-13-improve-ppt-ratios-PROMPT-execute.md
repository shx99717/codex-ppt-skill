Execute the implementation plan at `docs/plans/2026-08-13-improve-ppt-ratios.md` in this repository (`D:/git/codex-ppt-skill`).

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
   - Do NOT skip Section 0.7 review patches (style-file 16:9 override, unprobed Codex image_gen schema, slide_jobs aspect_ratio next to selected_backend).
   - Do NOT restore header-band placement (`MEDAVIS_CONTENT_TOP=700000`) or add a second landing title textbox.
   - Do NOT stretch images by setting picture width and height independently to the slide box.
   - Do NOT letterbox or crop as a success path; refuse ratio mismatch and regenerate.
   - Do NOT offer Cursor GenerateImage for 16:9 or 4:3 decks.
   - Do NOT require returned images to match the requested pixel box; gate 2% relative ratio only.
   - Do NOT re-probe gpt-image-2 `--size` (already done in Appendix F).
   - Do NOT treat `tests/smoke-deck/runs/20260812-1725-cursor-interactive` 3:2 images as a GREEN 16:9 assemble.
   - Do NOT use `medavis-logo-original.png`.
   - Do NOT overwrite bundled template files.
   - Do NOT commit unless I explicitly ask.
   - Do NOT run collection install/uninstall scripts; edit only `skills/codex-ppt/` (+ repo docs/CHANGELOG/`.gitignore`/tests as the plan requires).
5. When done and verification is green, report results and offer a code review.

If something is genuinely ambiguous or you hit a blocker, ask via the question channel; otherwise
proceed autonomously through the whole plan.
