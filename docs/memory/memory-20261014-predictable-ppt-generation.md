# Memory: Predictable PPT Generation

**Generated**: 2026-10-14 11:23 Asia/Shanghai
**Last updated**: 2026-10-14 12:43 Asia/Shanghai
**Project**: D:/git/codex-ppt-skill
**Focus**: Confirmed requirements, selected approach, and approved design sections for making image-based presentation generation predictable.

## Goal & Scope

Improve the existing Codex PPT skill so users can agree on slide content and intended visuals before full image generation, reducing expensive surprises without tedious page-by-page interviews. The workflow must adapt to input readiness and use the agent's judgment to recommend useful content, structure, and visuals.

Requirements are confirmed. Brainstorming is in progress: the user selected adaptive planning inside the PPT skill and approved input assessment and content development. Visual planning, approval/production details, and review behavior still need design discussion and approval. Implementation has not been authorized through a completed design or execution handoff. The existing detailed proposal remains provisional except for the explicitly approved decisions listed here.

## Key Decisions

1. **Predictability boundary**: Approved facts, messages, visible wording, and visual structure must stay fixed. Minor rendering differences are acceptable. The user selected this balance rather than allowing production to freely refine copy or requiring exact pixel placement.
2. **Rough-input expansion**: The agent may propose additions and explanations, clearly flag them, and ask the user for missing facts or important decisions. The user selected this over requiring the user to fill every gap or making research the default expansion route.
3. **Quality first, time second**: No fixed five-to-ten-minute review target. Review effort depends on deck length, topic difficulty, and unresolved decisions. Avoid repetition and lengthy interviews for each page; do not sacrifice quality to meet an arbitrary time budget.
4. **Input readiness is variable**: Prepared slide-by-slide Markdown should reuse the supplied structure and wording and require less preparation. Partial inputs need focused completion. Topic-only or idea-only inputs need a fuller guided process to agree on the story, slide content, and visuals.
5. **Separate content and visual readiness**: Complete content may lack design decisions; a visual reference may lack content. Do not treat every input as the same shape or automatically run the same preparation steps.
6. **Requirements before design**: The first proposal was drafted before the user had confirmed requirements. The user asked to restart with clarify-requirements and then brainstorming. The confirmed requirements above take precedence over defaults in that provisional proposal.
7. **Feature branch**: At the user's request, created feature/SQ5GEN-predictable-deck-generation from main and moved the proposal into the repository's plans folder. The requested feature/SQ5GEN prefix overrides the default codex/ prefix. No new JIRA task number was supplied; do not invent one.
8. **Memory authorization and location**: The user confirmed the revised requirements, explicitly requested saving memory, and selected the PPT repository's memory folder from the two workspace roots. This session's memory location is D:/git/codex-ppt-skill.
9. **Selected approach**: The user chose adaptive planning inside the PPT skill over mandatory chaining of installed clarification/brainstorming skills or a separate presentation-planning skill. The workflow assesses gaps and handles them internally; other skills are not mandatory installation dependencies.
10. **Approved input assessment**: Assess content readiness separately from visual readiness, potentially per slide within a mixed-readiness deck. Briefly report what can be reused, what is missing, and recommended next steps. Reuse provided decisions and ready slide structure/wording; show suggested changes separately.
11. **Clarify intention before developing content**: Establish content-changing context before drafting or expanding around assumptions. Audience, purpose, prior knowledge, intended outcome, presentation context, tone, language, scope, and length are examples, not an exhaustive questionnaire. Extract known answers, intelligently choose and order topic-specific questions, recommend defaults, and confirm consequential assumptions.
12. **Approved content development**: Preserve prepared content unless revisions are requested. Propose concrete structure/wording for genuine gaps, clearly flag additions, and identify missing facts or evidence without inventing numerical values. Develop the whole deck's content and intended visible wording together, allow review by exception, and feed it into a combined content-and-visual plan without imposing a separate content approval round on every input.
13. **Documentation checkpoint authorized**: The user explicitly asked to continue, update memory, and commit and push on 2026-10-14. This supersedes the earlier no-commit/no-push restriction for the current planning-document checkpoint. There is no executable code change to publish and no completed implementation design; do not mistake this request for permission to implement unapproved design sections. At that point the task ID had not yet been supplied, so the agent asked rather than inferring it from older history.
14. **Commit task ID confirmed**: The user selected SQ5GEN-195 for the documentation checkpoint. Use the Conventional Commit message: [SQ5GEN-195] docs: record predictable deck planning decisions.

## Confirmed Assumptions

- The goal is predictable content and visual intent within the existing presentation workflow, not identical generated pixels.
- Users need intelligent recommendations and visibility into proposed additions before approval.
- Ready-made slide content must not be rebuilt unnecessarily.
- Asking about real missing facts or important decisions is appropriate; repeated minor decisions are not.
- Requirements were explicitly confirmed after the user added the variable-input constraint.
- The original branch/proposal request alone did not authorize publication. The user's later explicit instruction now authorizes committing and pushing the planning-document checkpoint.
- Only the selected approach and the input-assessment/content-development sections are approved. The rest of the original proposal is a candidate, not permission to implement.
- General clarification questions are adaptive and may extend beyond the example fields discussed.
- Brainstorming is active and must continue with the remaining design sections.

## Constraints & Non-Goals

- Committing and pushing the current planning documents is explicitly authorized. No merge or direct changes to main are authorized.
- No skill implementation or installation changes yet.
- Do not silently use the existing proposal as an approved implementation plan.
- Do not interpret topic-only input as permission to invent organization-specific facts or numerical evidence.
- No blanket external-research requirement was selected.
- No fixed review deadline.
- Preserve existing capabilities unless an approved design explicitly changes them.
- For eventual shipped changes: synchronize existing Chinese, English, and Korean documentation; add an English Unreleased changelog entry; follow the repository's PR and verification rules.

## Key Discoveries

- The skill generates complete slide images and packages them into PowerPoint. Generated slide text, charts, and shapes are not independently editable. Speaker notes are written by the main agent and embedded by assembly.
- The repository has twelve built-in visual styles. Visual style is separate from plain versus Medavis output-template selection. Personal custom styles live outside the installation and can override matching built-in names.
- Supported deck ratios are 16:9, 4:3, and 3:2, with a 2% relative pixel-ratio check. Actual tool capabilities must be checked; documentation alone does not establish runtime support.
- The main agent owns the source/outline/specification, prompt jobs, state, QA, notes, and assembly. After sample approval, slide workers produce individual candidates using the selected backend.
- Existing image approval is bound to the current PNG hash. The default workflow requires per-wave review of non-sample images, with an explicit waiver needed to skip it. A balanced or bulk review policy is still a design choice, not a confirmed requirement or current waiver.
- Content clarification is broad; the skill does not explicitly invoke the personal clarify-requirements skill or require a detailed content interview. Per-slide plans contain titles, key points, roles, language, and required assets.
- A temporary audit fixture successfully prepared a prompt job without an approval record, layout, claim source, backend lock, or approved sample method. These prerequisites currently rely substantially on agent instructions.
- Dispatch records a prompt hash. Result recording does not compare the current prompt with that dispatch hash. Managed-workflow approval/version validation is a possible improvement, not yet implemented.
- Assembly validates image ratios but does not enforce the user-review ledger; the agent is currently responsible for that gate.
- Required figures are instructed to preserve labels/data and use real image inputs. Whole-slide generation still needs visual verification for fidelity.
- The detailed analysis and alternatives are preserved in [the provisional proposal](../plans/2026-10-14-predictable-deck-generation-proposal.md). Its recommended number of checkpoints and architecture are unapproved; its time-target discussion must be interpreted in light of the confirmed quality-first requirement.

## Runtime Evidence

- Read and checked the main skill, phase docs, worker prompt, preparation/state/result/review scripts, assembly, and existing smoke outputs.
- Ran: shared runtime Python, -B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_*.py. Result: 75 tests passed. This tests existing code; it does not validate the proposed workflow or current live image generation.
- A temporary one-slide prompt-preparation fixture returned exit 0; expected backend and sample method were null. It generated no real slide image.
- Inspected the saved Codex coffee example: plain output has three slides, each with one picture and speaker notes; Medavis output has five slides. Recorded non-sample image approvals matched their image hashes.
- Before memory creation, branch was feature/SQ5GEN-predictable-deck-generation; HEAD remained dc65c44c8b8fcef60c3073e7203856cfa3598b2f; only the proposal was an untracked repository change. No commits were made.

## Open Risks

- Hash/version checks can prevent accidental drift in production inputs; they cannot guarantee correct image-model rendering.
- Exact visible copy, critical labels, numerical values, and source-figure fidelity require appropriate visual QA and repair.
- Do not confuse separate agent QA with a real user image approval.
- The current native image tool schema lacks an explicit size parameter while repository rules require checking ratio capability. Recheck live schemas before a future image-generation pilot.
- The overall approach is approved: adaptive planning inside the PPT skill. Visual-plan details, approval/version validation, review policy, and implementation scope still need design approval.

## Current State

- **Working**: Existing skill and scripts; source analysis; confirmed requirements; selected approach; approved input-assessment and content-development sections.
- **Branch**: feature/SQ5GEN-predictable-deck-generation, created from main.
- **Planning artifacts**: Provisional proposal in docs/plans/ and this session memory file, reviewed for the user-authorized documentation checkpoint. Consult Git history/upstream for publication status.
- **Documentation review**: Independent review found zero Critical, Important, or Minor issues. Focused checks validated all eleven local Markdown links, the approval/draft distinction, and staged diff whitespace. No new implementation behavior was tested.
- **Commit task ID**: SQ5GEN-195, explicitly confirmed by the user.
- **Pending design**: Continue brainstorming visual planning and approval/production/review behavior, then choose an execution handoff after full design approval.
- **Blocked**: None. No implementation is running while waiting for remaining design decisions.

## Brainstorming Checklist

- [x] Explore the repository context and existing controls.
- [x] Clarify and explicitly confirm requirements.
- [x] Compare three approaches with trade-offs; user selected adaptive planning inside the PPT skill.
- [x] Approve input assessment, including separate content/visual readiness.
- [x] Approve adaptive intention clarification and content development.
- [ ] Present the design in manageable sections and obtain approval.

## Next Steps

1. Check Git history/upstream for the reviewed documentation checkpoint before resuming. If publication is pending, finish the explicitly authorized commit/push using SQ5GEN-195; do not repeat an already published checkpoint.
2. Continue the next design section: how intended visuals and layouts join the exact visible content in one reviewable plan, adapted to input readiness.
3. Agree on sample calibration, production validation, and generated-image review behavior; remaining parts of the earlier proposal are candidates.
4. After the full design is approved, offer the appropriate execution/implementation-plan handoff. Do not merge or modify main without an explicit instruction.

## Device mode

- **Mode**: mobile
- **Switched**: 2026-10-13 19:54

## Session State

- Question channel: plain-chat, resolved at session start. Only synchronous tools callable in the active mode qualify; the asynchronous question tool was excluded.
- Autonomous mode: off, the default; the user has not switched it on.
- Startup memory choice: start fresh. The old Medavis-template memory was not loaded.
- Memory location: D:/git/codex-ppt-skill, explicitly selected by the user.
- No worktree-role or working-directory selection command was run.
- Keep mobile presentation until the user invokes the device-mode switch, even when voice ends.
- The user cannot always see the screen and requested complete wording, including every question and option, without spoken summaries dropping content.
- Voice repeatedly delivered progress phrases while completed written questions existed. Do not imply background work is running when the task is waiting for a user decision. No voice-playback control is available in this task.
- Ordinary typed messages use normal output. Only genuine realtime delegations use their requested status/completion prefixes. Transcript-tail flushes are archival; do not redo handled work.

## References

- D:/git/codex-ppt-skill/AGENTS.md -- repository contribution and documentation rules.
- D:/git/codex-ppt-skill/skills/codex-ppt/SKILL.md -- current orchestration contract.
- D:/git/codex-ppt-skill/skills/codex-ppt/docs/outline-style-and-sample.md -- current content and sample planning.
- D:/git/codex-ppt-skill/skills/codex-ppt/docs/workflow-gates-and-progress.md -- current approval gates.
- D:/git/codex-ppt-skill/skills/codex-ppt/docs/slide-generation-and-subagents.md -- job context, production, and revision rules.
- D:/git/codex-ppt-skill/skills/codex-ppt/scripts/prepare_slide_prompts.py -- deterministic prompt compilation.
- D:/git/codex-ppt-skill/skills/codex-ppt/scripts/slide_run_state.py -- job state and image-approval hashes.
- D:/git/codex-ppt-skill/skills/codex-ppt/scripts/assemble_ppt.py -- image-based PPT assembly and Medavis wrapper.
- D:/git/codex-ppt-skill/tests/smoke-deck/README.md -- end-to-end fixture and coverage gaps.
- ../plans/2026-10-14-predictable-deck-generation-proposal.md -- detailed provisional analysis, options, and test proposals.
- C:/Users/raymond.shen/.codex/skills/clarify-requirements/SKILL.md -- clarification workflow used.
- C:/Users/raymond.shen/.codex/skills/brainstorming/SKILL.md -- next design workflow.
- C:/Users/raymond.shen/.codex/skills/managing-session-memory/SKILL.md -- memory lifecycle and session selections.

**Requirements confirmed at**: 2026-10-14 11:23 Asia/Shanghai
**Latest design approvals recorded at**: 2026-10-14 11:43 Asia/Shanghai
