# Memory: Predictable PPT Generation

**Generated**: 2026-10-14 11:23 Asia/Shanghai
**Last updated**: 2026-10-15, installed feature snapshot and pilot-prompt checkpoint, Asia/Shanghai
**Execution update**: All nine implementation tasks completed, independently reviewed, committed and pushed as d9f3be7864b6a31e66315ccf7edebe3f15235558. All three installed copies now match the79 tracked portable files from that feature snapshot; backups and installation verification are saved. The168-test suite and10 smoke tests passed before implementation publication; nine installation contract checks, three actual template commands, dependency imports and pip check passed after installation. See [delivery report](../plans/evidence/2026-10-15-predictable-deck-green.md) and [execution log](../plans/evidence/2026-10-15-predictable-deck-execution.md). The latest request authorizes this memory update, a copyable three-to-four-slide pilot prompt, and commit/push of these documents. Writing the prompt does not run the pilot. No merge or release is authorized. Named autonomous mode remains off.
**Project**: D:/git/codex-ppt-skill
**Focus**: Completed predictable-deck implementation and publication, verified three-IDE installation, and a separate-session pilot prompt.

**User briefing**: A [plain-language briefing](../plans/2026-10-15-predictable-deck-human-briefing.md) explains the five main changes and verification. The user subsequently authorized feature publication and installation in Codex, Claude Code and Cursor; both are complete. A [copyable four-slide pilot prompt](./memory-20261014-predictable-ppt-generation/sample-deck-pilot-PROMPT.md) is prepared for a separate session. No live deck has been generated.

## Goal & Scope

Improve the existing Codex PPT skill so users can agree on slide content and intended visuals before full image generation, reducing expensive surprises without tedious page-by-page interviews. The workflow must adapt to input readiness and use the agent's judgment to recommend useful content, structure, and visuals.

Requirements and all presented workflow sections are approved, including natural speaker-note voice and earlier preparation/review. The complete speaker-note input is preserved separately and embedded unchanged in the implementation handoff. All nine tasks are implemented, verified and published on the existing feature branch. The user then requested adapting the three-IDE installation guide to this unmerged feature version, including removal of stale installed files; installation is complete. Current work records that outcome and prepares a separate-session trial prompt, with explicit commit/push authorization.

The four Important handoff-review findings were corrected before execution; saved Appendix G passes again. Installation of this feature version in the three named IDEs was explicitly authorized and completed. Live image generation and creation of another chat are outside this memory/prompt checkpoint; the user will paste the prompt into a separate session. The baseline started on 2026-10-14 and its final verification crossed midnight into 2026-10-15.

## Key Decisions

1. **Predictability boundary**: Approved facts, messages, visible wording, and visual structure must stay fixed. Minor rendering differences are acceptable. The user selected this balance rather than allowing production to freely refine copy or requiring exact pixel placement.
2. **Rough-input expansion**: The agent may propose additions and explanations, clearly flag them, and ask the user for missing facts or important decisions. The user selected this over requiring the user to fill every gap or making research the default expansion route.
3. **Quality first, time second**: No fixed five-to-ten-minute review target. Review effort depends on deck length, topic difficulty, and unresolved decisions. Avoid repetition and lengthy interviews for each page; do not sacrifice quality to meet an arbitrary time budget.
4. **Input readiness is variable**: Prepared slide-by-slide Markdown should reuse the supplied structure and wording and require less preparation. Partial inputs need focused completion. Topic-only or idea-only inputs need a fuller guided process to agree on the story, slide content, and visuals.
5. **Separate content and visual readiness**: Complete content may lack design decisions; a visual reference may lack content. Do not treat every input as the same shape or automatically run the same preparation steps.
6. **Requirements before design**: The first proposal was drafted before the user had confirmed requirements. The user asked to restart with clarify-requirements and then brainstorming. The confirmed requirements above take precedence over defaults in that provisional proposal.
7. **Feature branch**: At the user's request, created feature/SQ5GEN-predictable-deck-generation from main and moved the proposal into the repository's plans folder. The requested feature/SQ5GEN prefix overrides the default codex/ prefix. At branch creation no new JIRA task number had been supplied; the later checkpoint task-ID confirmation is recorded below.
8. **Memory authorization and location**: The user confirmed the revised requirements, explicitly requested saving memory, and selected the PPT repository's memory folder from the two workspace roots. This session's memory location is D:/git/codex-ppt-skill.
9. **Selected approach**: The user chose adaptive planning inside the PPT skill over mandatory chaining of installed clarification/brainstorming skills or a separate presentation-planning skill. The workflow assesses gaps and handles them internally; other skills are not mandatory installation dependencies.
10. **Approved input assessment**: Assess content readiness separately from visual readiness, potentially per slide within a mixed-readiness deck. Briefly report what can be reused, what is missing, and recommended next steps. Reuse provided decisions and ready slide structure/wording; show suggested changes separately.
11. **Clarify intention before developing content**: Establish content-changing context before drafting or expanding around assumptions. Audience, purpose, prior knowledge, intended outcome, presentation context, tone, language, scope, and length are examples, not an exhaustive questionnaire. Extract known answers, intelligently choose and order topic-specific questions, recommend defaults, and confirm consequential assumptions.
12. **Approved content development**: Preserve prepared content unless revisions are requested. Propose concrete structure/wording for genuine gaps, clearly flag additions, and identify missing facts or evidence without inventing numerical values. Develop the whole deck's content and intended visible wording together, allow review by exception, and feed it into a combined content-and-visual plan without imposing a separate content approval round on every input.
13. **Documentation checkpoint authorized**: The user explicitly asked to continue, update memory, and commit and push on 2026-10-14. This supersedes the earlier no-commit/no-push restriction for the current planning-document checkpoint. There is no executable code change to publish and no completed implementation design; do not mistake this request for permission to implement unapproved design sections. At that point the task ID had not yet been supplied, so the agent asked rather than inferring it from older history.
14. **Commit task ID confirmed**: The user selected SQ5GEN-195 for the documentation checkpoint. Use the Conventional Commit message: [SQ5GEN-195] docs: record predictable deck planning decisions.
15. **Approved visual planning**: Combine intended exact visible copy with visual type, important objects and relationships, critical labels/data, and approximate layout in a whole-deck plan. Reuse supplied designs and confirmed style decisions; otherwise recommend a cohesive style with layouts suited to slide roles. Allow review by exception and simple structural previews for complex visuals when text alone is ambiguous.
16. **Approved deck-wide coherence**: Each slide is an interconnected part of the deck. Plan narrative progression, audience knowledge, and transitions; preserve recurring visual identities, terminology, symbols, colors, and diagram meanings. Numbering and cross-references follow the agreed scheme, including consecutive sequences spanning slides. The user's examples are not an exhaustive checklist or a blanket requirement for visible page numbers. Workers receive shared references and relevant story context; QA checks the complete sequence as well as individual slides. The user approved the expanded visual-planning section by selecting option one.
17. **Design-document update authorized**: The user explicitly requested updating the associated documents and memory, then returning to the discussion so they can choose the next step. Update the existing proposal with approved sections and clearly marked candidates. A separate implementation plan remains a later handoff after full design approval; do not implement pending design or infer sample approval from this document-update request.
18. **Follow-up publication authorized; review waived**: After the two-document update, the user explicitly requested committing and pushing and stated that no code review was needed. This authorizes publishing the updated proposal and memory on the existing feature branch and overrides the routine review gate for this checkpoint. It does not authorize implementation of pending design sections.
19. **Approved sample calibration**: After whole-deck plan approval, choose a representative content slide testing important visual requirements; reuse a suitable existing approved sample when it fits. Explain additional samples for substantially different visual approaches. Accepted samples establish shared typography, colors, visual language, and recurring elements while layouts vary by slide purpose. Feedback changing approved decisions updates the affected plan before full generation.
20. **Approved production locking and notes**: The approved plan is the source of truth for wording, facts, visuals, shared elements, and slide connections. Scripts check that full generation uses the current approved plan, assets, and accepted samples; missing/outdated approval stops production. Workers repair within the plan and raise substantive changes or fitting problems. Revisions identify affected slides/shared dependencies and revisit affected decisions, potentially the whole deck. Notes may explain approved material and transitions; new substantive claims require approval.
21. **Approved consolidated review default**: Recommend consolidated review for the revised skill and state the chosen process in each deck's plan. Agent QA checks each slide and the whole story/visual sequence; users review the deck together, approve it or name exceptions, then review corrections and affected connections. Final assembly needs real user approval of the current images, recorded separately from agent QA. Material deviations or repeated problems trigger an early stop. Strict batch review remains an alternative. This design approval does not approve any future deck or waive an existing live run's established gates.
22. **Approved repair and delivery checks**: Check the first batch before the remaining slides; pause repeated problems and correct their shared cause. Permit one targeted automatic repair per affected slide for isolated rendering problems, preserving approved facts, wording, and relationships. Escalate failures with a recommendation and group independent unresolved issues where practical. Further attempts need authorization when quality warrants them; content/design changes need confirmation. Before delivery, check slides, the whole sequence, counts, output format, note consistency, and current-image approval.
23. **Completed-design checkpoint requested**: The user approved repair/final checks by selecting option one and explicitly requested saving memory. Save all latest approvals, update the existing design record, then offer the implementation handoff. Saving memory does not select an implementation route or authorize a new publication.
24. **Follow-up checkpoint published**: The earlier authorized proposal/memory update was committed and pushed as 99fba3d3ea2d8f1d285cf40dbf44d8e32f05d126 with message [SQ5GEN-195] docs: record deck coherence design decisions. Local HEAD, upstream, and the remote feature branch matched; the working tree was clean and main remained dc65c44c8b8fcef60c3073e7203856cfa3598b2f immediately after publication.
25. **Approved natural speaker-note voice**: Treat the user's supplied style as a core note-authoring standard across presentation types. Use the presenter's own voice, natural first-person phrasing and warmth, thought-sized beats separated by breathing space, everyday vocabulary, introduced technical terms, concrete examples before abstractions, and explanations of meaning. Preserve spoken rhythm/connectors in the presentation language; include purposeful transitions, supplied-name handovers, and a natural close with questions. Length fits intended speaking time. The complete source takes precedence over this condensed description.
26. **Approved earlier note planning and review**: Draft notes alongside the slide plan, show a representative note for voice calibration, and review the complete talk by exception before expensive image generation. Reuse supplied notes and flag proposed changes. The previously approved factual boundary remains: notes may explain approved material and transitions; new substantive claims need approval. Review natural speech, pacing, and continuity across the deck.
27. **Verbatim-source preservation requested**: The user explicitly requested a separate Markdown file retaining every word of their speaker-note input and references to it so compaction cannot replace it with an incomplete summary. Preserve the entire original message, including its framing, all style bullets, English and Chinese examples, punctuation, and paragraph breaks. Read the linked source in full when resuming relevant work after compaction. Keep interpretations and derived guidance outside the original source body.
28. **Self-contained handoff selected**: The user chose option two from the implementation handoff menu: write a formal self-contained plan for another agent or new session. Use writing-plans handoff mode; do not ask the mode again, create a new chat, or start implementation from this choice alone.
29. **Handoff artifacts saved**: The plan contains full approved context, repository/branch/task conventions, concrete managed schema and gate design, nine implementation tasks, RED/GREEN authoring scenarios, acceptance checks, complete speaker-note source and project rules, and a companion prompt. It distinguishes plan-example verification from feature implementation, and records explicit legacy compatibility and immutable style-reference snapshots. The complete original source body remains 3,873 characters with the recorded SHA-256.
30. **Critical review selected and completed**: The user chose agent review before execution. Used think-mcp sequentialthinking plus executable reference-code/schema probes. Confirmed Important-1: full shared-registry prompt versus scoped visual hash; Important-2: factual slide changes leave stale note approval; Important-3: ledger example lacks the required policy/output fingerprint; Important-4: draft-relative asset paths change meaning after canonical installation. All four remain open in the linked review report, with evidence and regression criteria. At that review checkpoint no fixes were applied; resolution is recorded in decision 31 below.

31. **Handoff revision authorized and verified**: The user accepted the recommendation to revise all four findings. Updated common `build_contexts` render/hash projection with sorted prompt JSON; talk fingerprints now include facts/evidence/source bytes/semantic relationships while excluding pure appearance/composition; ledger/policy gate/CLI now record actual policy-scoped events, approved output snapshot, and fingerprint; draft assets normalize before reviewed candidate fingerprint/installation with provenance, snapshots, and expected-plan-hash comparison. Fixed the missing-approval fixture to use a canonical in-deck spec. Updated Tasks 1–6, D9, acceptance, Appendix G, prompt, and review resolution. Saved reference checks pass for all four, including a Windows normalized-path fixture correction. Original speaker source and Appendix A remain unchanged. This is documentation/reference-code verification, not feature implementation or new publication authorization.

32. **Reversed: handoff-only route**: The user said, “I changed my mind. I decide now to execute the written implementation plan in this session,” and requested reloading both plan and prompt. Use executing-plans in this checkout; retain settled requirements and the corrected contracts. No repeated design interview or handoff-mode menu. Outward actions remain separately authorized.
33. **Task 1 baseline checkpoint saved**: Read the entire revised plan/prompt/source, reran Appendix G (four PASS records), ran the existing suite (75 passed), added a fresh complete fixture and missing-approval regression, and observed its real expected assertion failure. Full discovery now runs 76 tests with exactly that one intended RED. Three isolated unchanged-skill test agents produced nine D1–D8 runs (D5 both policies). Archive contains 114 byte-verified artifacts and 68 nested JSON files. Preserve passing input reuse, shared-change coherence, human/QA separation, and English/Chinese voice behavior. Actual gaps include absent compiler approval gate, late talk review, and unbounded retry behavior. Offline action traces are replay evidence, not tool-enforced conversations or physical content-authoring chronology. A semantic note check was corrected for Windows CRLF; source/archive bytes were not changed. Task 2 and later production work remain pending.

34. **Continuous execution completed**: User authorized “Continue to the end; pause only when you genuinely need my decision or input.” Completed Tasks2–9 without routine checkpoints or mode changes. Added semantic contracts/scoped decisions/immutable snapshots/compiler/lifecycle/QA/repair/bulk review/assembly, portable adaptive/voice guides, all three published language counterparts and changelog. Evidence-driven additions include executable CLI operation mapping and a minimal Windows candidate-directory race correction. All original core Important1–10 and guidance approval-order finding are resolved in independent follow-ups.
35. **Final verification and limits**:168 script tests pass (114.337s),10 smoke-verifier tests pass, synthetic managed plain2/branded4 with exact notes/offsets pass,165 links and114+7 original-byte hashes verified. Original speaker source/AppendixA unchanged. Twelve actual text application variants cover original cases plus mixed and voice pressure. Four incompatible schema drafts were preserved as RED, mapped using the real template, validated and exercised through real draft-view CLIs with exact content/talk preservation. Helpers reached a usage limit at this final representation check; primary executed the authored four-case replay. Publication preflight found that the guidance reviewer had already saved a completed independent supplementary schema-paragraph review before its final notification failed; that paragraph is independently reviewed. The four-case replay remains primary verification, not an independent fresh-agent retest. No live model pixels, timed speech or real approvals were tested.
36. **Implementation publication authorized**: On 2026-10-15 the user said, “Update memory, commit and push.” This supersedes the completed local-delivery publication restriction for the implementation, tests, synchronized documentation, plans/evidence and memory on `feature/SQ5GEN-predictable-deck-generation`. Use task ID `SQ5GEN-195`, an English Conventional Commit, and a normal push; preserve main. This memory records the reviewed snapshot and authorization before committing. Confirm the resulting commit and remote SHA after pushing; do not infer publication success from this file alone. No further approval is needed for these requested actions.
37. **Fresh publication verification**: Reran the complete script suite: 168 passed in 124.288 seconds, exit 0. Smoke-verifier suite: 10 passed in 0.268 seconds, exit 0. Artifact verification again passed original speaker-source/Appendix equality, portable voice digest, 114 baseline artifact hashes, 7 runner/audit hashes and 165 local Markdown links. Core adapter/regression file hashes match the independently reviewed snapshot. No production code changed during publication preparation.
38. **Staged scope inspected**: 166 intended task files, approximately 1.97 MB, no files over 1 MB and no private-key/API-token patterns found. The expanded staged whitespace check reports16 formatting notices in reviewed text: intentional Markdown hard-break spaces, generated empty dependency-line endings and extra final blank lines. These were inspected and retained rather than rewriting reviewed source/evidence for formatting alone. The earlier tracked-only whitespace check did not include new files; do not describe the full staged check as clean.
39. **Implementation published**: Commit d9f3be7864b6a31e66315ccf7edebe3f15235558, `[SQ5GEN-195] feat: add predictable deck planning and approval workflow`, was pushed successfully. Local HEAD, upstream and remote feature-branch SHA matched; working tree was clean and main remained dc65c44c8b8fcef60c3073e7203856cfa3598b2f.
40. **Three-IDE feature installation authorized and completed**: The user supplied D:/git/squad5-curated-ai-tooling-collection/production/github_collection/manual_install_codex-ppt-skill.txt and explicitly requested adapting installation/update for the unmerged feature branch, synchronizing removals. Used the clean local d9f3be7 snapshot instead of the guide's default-branch download. All79 tracked portable files, including required branded assets, were staged and hash-verified, then each entire codex-ppt directory was replaced with native PowerShell moves after validating absolute paths. Backups are outside IDE discovery folders. Each IDE received20 additions and22 updates; no old source file was absent from the new source tree. Two stale bytecode caches each in Claude Code and Cursor are absent from active copies. Codex had none. Untracked development caches were not copied.
41. **Installation verification and recovery**: Installed targets are C:/Users/raymond.shen/.codex/skills/codex-ppt, C:/Users/raymond.shen/.claude/skills/codex-ppt and C:/Users/raymond.shen/.cursor/skills/codex-ppt. Each has exactly79 source paths with identical SHA256 hashes and no extras; all three original backup manifests match. Three portable contract tests passed per installation (nine total); each installed compiler wrote an actual workflow-version-2 template, and all three outputs match. Shared dependency imports and pip check passed without upgrading dependencies. API configuration, personal styles and installer metadata hashes are unchanged; repository remained clean. Backups, local installation manifest and readable report are under C:/Users/raymond.shen/.codex-ppt-skill/installation-backups/20261015-102531-feature-d9f3be7/. Restart agents or start fresh sessions to reload instructions. Repeating a default-main install may replace this feature snapshot; until merge, use an explicit feature ref or the same verified synchronization.
42. **Pilot-prompt publication requested**: The user explicitly requested saving memory, committing/pushing, and generating a prompt to paste into another session for a three-to-four-page sample with this skill. In this PPT context, pages mean presentation slides. Prepared a four-total-slide plain PPTX prompt using a rough team-handover paragraph, English copy/notes, a coherent fictional example, clean professional style and preferred16:9. The new session verifies the installed feature copy, recommends real capable backend options, and retains genuine combined-plan, sample and final-image reviews. Speaker-note instructions link back to the installed complete voice guide. Output goes to a fresh ignored smoke-run directory. The prompt is an editable trial brief, not a newly approved slide plan or live-run authorization in this session. This document-only checkpoint does not change portable skill files or require reinstallation.
43. **Memory/prompt verification and review**: Fresh read-only verification rechecked all237 installed files against their79-file source snapshot, all10 Markdown links in these two documents, and the complete speaker-source/Appendix/portable-voice integrity. Existing artifact verification again passed114 baseline hashes,7 runner/audit hashes and165 local guide links. The focused independent document review returned0 Critical/0 Important/0 Minor, verified installation counts/actual installed hashes, approval boundaries and prompt usability, and confirmed the original3,873-character source digest. Staged whitespace check passes. Only this memory and its prompt companion are being published; no runtime code or installed files changed during this checkpoint.

## Confirmed Assumptions

- The goal is predictable content and visual intent within the existing presentation workflow, not identical generated pixels.
- Users need intelligent recommendations and visibility into proposed additions before approval.
- Ready-made slide content must not be rebuilt unnecessarily.
- Asking about real missing facts or important decisions is appropriate; repeated minor decisions are not.
- Requirements were explicitly confirmed after the user added the variable-input constraint.
- The original branch/proposal request alone did not authorize publication. The user's later explicit instruction now authorizes committing and pushing the planning-document checkpoint.
- The selected approach and all presented workflow sections are approved. Their concrete schemas/interfaces/tasks are in the revised self-contained plan. Execution is completed; the latest user instruction authorizes feature-branch commit/push.
- General clarification questions are adaptive and may extend beyond the example fields discussed.
- Brainstorming, handoff planning, critical review and revision are complete. Do not repeat answered design questions or the plan-mode selection. Execute from the current task checkpoint.
- Treat the deck as the unit of design; consistency within an individual slide is insufficient to establish coherence across the presentation.
- Spoken delivery is a core quality requirement. The speaker-note source's example topics and names guide voice and rhythm; future decks use their own approved facts and speaker names.

## Speaker-Notes Source: Read in Full After Compaction

The [verbatim speaker-note input](./memory-20261014-predictable-ppt-generation/speaker-notes-style-reference.md) preserves the user's complete original message, including all examples. Read the full file before continuing speaker-note planning, authoring, QA, or implementation of these requirements, including after loading this memory following compaction. This memory and the design contain condensed navigation aids; they do not replace the source. Preserve the original body verbatim and write derived guidance separately.

Integrity record for the original-message body between the file's markers, using UTF-8 and normalized LF line endings: 3,873 characters; SHA-256 `9a1a64e2825cdc729fe13ccb3207f8ffbf6703ce206bec190c2077a5998a9980`.

## Constraints & Non-Goals

- Prior documentation and implementation publication checkpoints were explicitly authorized and completed. The latest request authorizes memory/pilot-prompt commit and push on the same feature branch. PR/merge, release and direct main changes are not requested in this checkpoint.
- All three installed skills were explicitly updated to the verified d9f3be7 portable feature snapshot. Shared API settings, runtime and personal styles remain preserved. Synthetic tests and mocked behavior do not count as real deck/image approval or paid generation.
- Execute the revised written plan and prompt on the existing feature branch, following verified checkpoints. Preserve all pre-existing planning/source edits.
- Do not interpret topic-only input as permission to invent organization-specific facts or numerical evidence.
- No blanket external-research requirement was selected.
- No fixed review deadline.
- Preserve existing capabilities unless an approved design explicitly changes them.
- For eventual shipped changes: synchronize existing Chinese, English, and Korean documentation; add an English Unreleased changelog entry; follow the repository's PR and verification rules.

## Key Discoveries

The behavior and gaps below describe the original audited skill unless stated otherwise. The implemented controls and current verification are summarized in the execution update and delivery report; do not treat historical gaps as unfinished implementation.

- The skill generates complete slide images and packages them into PowerPoint. Generated slide text, charts, and shapes are not independently editable. Speaker notes are written by the main agent and embedded by assembly.
- The repository has twelve built-in visual styles. Visual style is separate from plain versus Medavis output-template selection. Personal custom styles live outside the installation and can override matching built-in names.
- Supported deck ratios are 16:9, 4:3, and 3:2, with a 2% relative pixel-ratio check. Actual tool capabilities must be checked; documentation alone does not establish runtime support.
- The main agent owns the source/outline/specification, prompt jobs, state, QA, notes, and assembly. After sample approval, slide workers produce individual candidates using the selected backend.
- Existing image approval is bound to the current PNG hash. The unmodified skill requires per-wave image review, with an explicit waiver needed to skip it. Consolidated review is now approved as the revised skill's recommended default; it has not been implemented and is not a waiver for an existing live run.
- Content clarification is broad; the skill does not explicitly invoke the personal clarify-requirements skill or require a detailed content interview. Per-slide plans contain titles, key points, roles, language, and required assets.
- A temporary audit fixture successfully prepared a prompt job without an approval record, layout, claim source, backend lock, or approved sample method. These prerequisites currently rely substantially on agent instructions.
- Dispatch records a prompt hash. Result recording does not compare the current prompt with that dispatch hash. Managed-workflow approval/version validation is a possible improvement, not yet implemented.
- Assembly validates image ratios but does not enforce the user-review ledger; the agent is currently responsible for that gate.
- Required figures are instructed to preserve labels/data and use real image inputs. Whole-slide generation still needs visual verification for fidelity.
- Analysis, approved workflow, and candidate technical details are preserved in [the design record](../plans/2026-10-14-predictable-deck-generation-proposal.md). Architecture and workflow are approved; concrete representation/tasks need the selected planning/execution handoff. No fixed question, review-time, or approval-round quota was selected.
- The existing notes guide already requests presenter language, natural transitions, deck context, and presentation-language matching. The new source adds explicit breathing beats, concrete-first explanation, everyday vocabulary, spoken rhythm, timing, and earlier note review. Preserve purpose-specific emphasis while making natural delivery the common baseline.

## Runtime Evidence

- Saved Appendix G rerun: exit 0, four PASS records. Reference expectations only; no implemented gate evidence.
- Fresh existing suite before new regression: 75 tests passed, exit 0.
- New `test_managed_preparation.py`: one expected assertion failure, exit 1; compiler incorrectly exits 0 and creates two prompt JSONs plus job/run state without an approval ledger. Canonical in-deck spec exists and is a valid complete synthetic fixture.
- Full discovery after adding the test: 76 tests, exactly one intentional missing-approval failure; all 75 original tests pass. Task 4 must turn it GREEN. Existing “Calling Image API” log uses the unit-test fake provider; no real image API call occurred.
- Nine archived baseline runs: D1/D2/D3/D4/D5-consolidated/D5-strict/D6/D7/D8. 114 artifact SHA checks, 68 nested JSON parses, 59 original skill-source hashes, two new test AST parses, thirteen report links, and original speaker-source SHA passed.
- D2 supplied copy and notes match with blank-line beats after newline normalization. Initial raw LF-vs-CRLF containment failure was diagnosed and the verification comparison corrected; archived bytes retain original hashes.
- Actual operations: baseline reads, temporary text/JSON writes, backend probes, deterministic prompt compilation. Image/worker/user-decision/QA actions in traces are simulated. No audio timing, model images, live-quality proof, PPTX, installed-skill modification or new publication.

## Open Risks

- Hash/version checks can prevent accidental drift in production inputs; they cannot guarantee correct image-model rendering.
- Exact visible copy, critical labels, numerical values, and source-figure fidelity require appropriate visual QA and repair.
- Do not confuse separate agent QA with a real user image approval.
- The current native image tool schema lacks an explicit size parameter while repository rules require checking ratio capability. Recheck live schemas before a future image-generation pilot.
- The approved workflow and concrete schemas/interfaces/tasks are implemented and tested. Image-model fidelity remains a limitation even with approved inputs and script enforcement.
- The four Important plan defects and all later reported runtime/guidance findings are resolved. Executable production/lifecycle/assembly, transaction and concurrency regressions pass; these checks cannot guarantee model rendering or a presenter's natural speech.

## Current State

- **Branch/task**: feature/SQ5GEN-predictable-deck-generation / SQ5GEN-195. Implementation commit d9f3be7864b6a31e66315ccf7edebe3f15235558 was verified on local HEAD/upstream/remote before this new document checkpoint; main remains dc65c44c8b8fcef60c3073e7203856cfa3598b2f. Inspect Git for the subsequent memory/prompt commit.
- **Done**: All nine implementation tasks, independent review corrections, feature publication and three-IDE installation. The [written delivery](../plans/evidence/2026-10-15-predictable-deck-green.md) and all original sources/evidence are saved. The copyable four-slide pilot prompt is prepared.
- **Current publication scope**: Only this memory and its new pilot-prompt companion. Portable skill files are unchanged, so all three installations remain current for the implementation. Complete speaker-note source remains unchanged; preserve historical evidence/reports.
- **Evidence**: [Archived metadata/runners](../plans/evidence/2026-10-14-predictable-deck-baseline/metadata.json) indexes nine case bundles with original-byte SHA records. Mock/replay boundaries and incidental temporary bytecode caches are disclosed. Source snapshot remains unchanged.
- **Pending at memory save**: Verify and publish the explicitly requested memory/prompt checkpoint, confirming local/remote SHA and clean tree. The user can then paste the prompt into a fresh IDE session for the live pilot; no deck generation has started here.
- **Checkpoint**: User explicitly authorized these document updates and commit/push. Do not repeat settled design or publication questions. Actual future deck content, sample and image approvals remain real decisions in the pilot session.
- **Blocked**: None. No implementation background work remains. Real model rendering, source-figure fidelity, spoken pacing and actual user acceptance remain live-pilot validation rather than claims established by offline tests.

## Brainstorming Checklist

- [x] Explore the repository context and existing controls.
- [x] Clarify and explicitly confirm requirements.
- [x] Compare three approaches with trade-offs; user selected adaptive planning inside the PPT skill.
- [x] Approve input assessment, including separate content/visual readiness.
- [x] Approve adaptive intention clarification and content development.
- [x] Approve visual planning and whole-deck review by exception.
- [x] Approve expanded deck-wide coherence, shared references, and sequence QA.
- [x] Agree on sample calibration.
- [x] Agree on production locking and speaker-note boundaries.
- [x] Agree on consolidated image review as the recommended default.
- [x] Agree on repair behavior and final delivery checks.
- [x] Approve natural speaker-note voice and earlier preparation/review; preserve the complete user reference separately.
- [x] Present the workflow design in manageable sections and obtain approval.
- [x] Obtain the user's implementation-plan handoff choice: self-contained handoff.
- [x] Write the self-contained plan and companion execute prompt with embedded context/source and verification.

## Next Steps

1. Read the complete speaker-note source when resuming related work after compaction; preserve its exact archived body.
2. Use the completed [Task 1 evidence](../plans/evidence/2026-10-14-predictable-deck-red.md) and revised [implementation plan](../plans/2026-10-14-predictable-deck-generation-handoff.md). Do not rerun the baseline unless a new concern warrants it.
3. Read the final delivery report for completed scope and exact verification. Do not restart implementation, baseline scenarios or the requirements interview.
4. Complete the authorized memory/pilot-prompt commit/push checkpoint and verify publication through Git. Give the user the complete copyable prompt; do not start the deck or create a new task here. The later pilot uses the actual skill's approval gates. PR/merge and release remain separate actions.

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

- ./memory-20261014-predictable-ppt-generation/sample-deck-pilot-PROMPT.md -- Copyable four-slide live-pilot request for another IDE session; writing it does not execute it.
- C:/Users/raymond.shen/.codex-ppt-skill/installation-backups/20261015-102531-feature-d9f3be7/installation-report.md -- Three-IDE installation results, original backup paths and rollback instructions.
- C:/Users/raymond.shen/.codex-ppt-skill/installation-backups/20261015-102531-feature-d9f3be7/installation-manifest.json -- Per-file source/backup hashes and actual installation verification.
- D:/git/squad5-curated-ai-tooling-collection/production/github_collection/manual_install_codex-ppt-skill.txt -- User-supplied three-IDE installation guide, adapted to the unmerged feature snapshot without changing the guide.

- ../plans/2026-10-15-predictable-deck-human-briefing.md -- Plain-language account of the completed changes, practical workflow, verification and remaining limits.

- D:/git/codex-ppt-skill/AGENTS.md -- repository contribution and documentation rules.
- D:/git/codex-ppt-skill/skills/codex-ppt/SKILL.md -- current orchestration contract.
- D:/git/codex-ppt-skill/skills/codex-ppt/docs/outline-style-and-sample.md -- current content and sample planning.
- D:/git/codex-ppt-skill/skills/codex-ppt/docs/workflow-gates-and-progress.md -- current approval gates.
- D:/git/codex-ppt-skill/skills/codex-ppt/docs/slide-generation-and-subagents.md -- job context, production, and revision rules.
- D:/git/codex-ppt-skill/skills/codex-ppt/scripts/prepare_slide_prompts.py -- deterministic prompt compilation.
- D:/git/codex-ppt-skill/skills/codex-ppt/scripts/slide_run_state.py -- job state and image-approval hashes.
- D:/git/codex-ppt-skill/skills/codex-ppt/scripts/assemble_ppt.py -- image-based PPT assembly and Medavis wrapper.
- D:/git/codex-ppt-skill/tests/smoke-deck/README.md -- end-to-end fixture and coverage gaps.
- ../plans/2026-10-14-predictable-deck-generation-proposal.md -- approved workflow design, analysis, and candidate implementation/testing details.
- ./memory-20261014-predictable-ppt-generation/speaker-notes-style-reference.md -- complete verbatim speaker-note input; authoritative style source to reread after compaction.
- ../plans/2026-10-14-predictable-deck-generation-handoff.md -- self-contained nine-task implementation plan with embedded approved context and speaker source.
- ../plans/2026-10-14-predictable-deck-generation-handoff-PROMPT-execute.md -- companion prompt to paste into the executor session.
- ../plans/2026-10-14-predictable-deck-generation-handoff-review.md -- completed review and resolution of four Important plan findings, historical probes, regression criteria, and corrected reference-check results.
- ../plans/evidence/2026-10-14-predictable-deck-red.md -- Task 1 checklist, exact reference/script RED evidence and evaluated baseline behaviors.
- ../plans/evidence/2026-10-14-predictable-deck-baseline/metadata.json -- immutable source manifest, archived raw scenario artifacts/runners and mock boundaries.
- C:/Users/raymond.shen/.codex/skills/executing-plans/SKILL.md -- active execution/checkpoint workflow.
- C:/Users/raymond.shen/.codex/skills/clarify-requirements/SKILL.md -- clarification workflow used.
- C:/Users/raymond.shen/.codex/skills/brainstorming/SKILL.md -- completed design approval and pending handoff workflow.
- C:/Users/raymond.shen/.codex/skills/managing-session-memory/SKILL.md -- memory lifecycle and session selections.

**Requirements confirmed at**: 2026-10-14 11:23 Asia/Shanghai
**Latest design approvals recorded at**: 2026-10-14 19:33 Asia/Shanghai
