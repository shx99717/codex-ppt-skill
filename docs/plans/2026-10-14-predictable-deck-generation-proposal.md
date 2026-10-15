# Approved Design: Predictable Codex PPT Generation

Date: 2026-10-14, Asia/Shanghai

Last updated: 2026-10-14 20:18, Asia/Shanghai

Scope: repository analysis, approved workflow design, and candidate implementation details for `D:/git/codex-ppt-skill`, on `feature/SQ5GEN-predictable-deck-generation`, created from `main` at the user's request. Two earlier documentation checkpoints were committed and pushed; this update records the completed design discussion. No skill implementation or installation changes have been made.

## Confirmed decisions and implementation status

The user restarted requirements clarification after the original proposal and confirmed the following:

- Approved facts, messages, visible wording, and visual structure must stay fixed, with minor rendering differences allowed.
- Quality comes first; review time depends on deck length and topic difficulty. There is no fixed review-time target.
- Input can be complete slide-by-slide Markdown, partial material, or only a topic/idea. Content readiness and visual readiness must be assessed separately; supplied structure, wording, and confirmed decisions should be reused.
- The selected approach is adaptive planning inside the PPT skill. Mandatory installation of other planning skills is not the chosen architecture.
- Input assessment is approved: identify reusable material and missing decisions, potentially per slide, and recommend an appropriate route.
- Content development is approved: understand the user's intention and resolve consequential context before expanding content; intelligently choose/order questions and treat audience/tone/etc. as examples rather than an exhaustive checklist.
- Preserve prepared content unless revisions are requested. Clearly distinguish proposed additions and missing facts/evidence. Develop the whole deck's content together and feed it into a combined content-and-visual plan without a mandatory separate content approval round for every input.
- Visual planning is approved: combine exact visible content with the proposed visual type, important objects and relationships, critical labels/data, and approximate layout. Reuse supplied designs and confirmed style decisions; recommend a cohesive style when needed. Review the whole plan by exception, with simple structural previews for complex visuals when a written description is insufficient.
- Deck-wide coherence is approved: treat each slide as an interconnected part of the deck. Plan narrative progression and transitions, preserve the identity and meaning of recurring visual elements and terminology, and keep numbering and cross-references consistent with the agreed scheme. These examples are not an exhaustive checklist or a requirement to display page numbers on every deck. Workers need shared references and relevant story context; QA must inspect the complete sequence as well as individual slides.

- Sample calibration is approved: after whole-deck plan approval, choose a representative content slide, reuse a suitable existing approved sample when available, and justify additional samples for substantially different visual approaches. Accepted samples establish shared visual references; feedback that changes approved decisions must update the affected plan before full generation.
- Production locking is approved: the approved plan is the source of truth. Scripts must check that full generation uses the current approved plan, assets, and accepted samples; missing or outdated approval stops production. Workers may repair rendering within the plan and must raise substantive changes. Revisions identify affected slides and shared dependencies and revisit affected decisions.
- Speaker-note boundaries are approved: notes may explain approved material and connect the story; new substantive claims require approval.
- Speaker-note voice and preparation are approved: use the presenter's natural voice, thought-sized beats with breathing space, everyday vocabulary, concrete explanations, and spoken transitions. Match the presentation language and intended speaking time. Draft notes alongside the slide plan, calibrate voice with a representative note, and review the whole talk by exception before expensive image generation. Reuse supplied notes and clearly flag proposed changes.
- Consolidated image review is approved as the revised skill's recommended default. State the chosen process in each deck's plan. Agent QA checks every slide and the complete sequence; the user reviews the deck together, approves it or names exceptions, and reviews corrections and affected connections. Final assembly requires real user approval of the current images, recorded separately from agent QA.
- Repair and final verification are approved: check the first production batch before the rest, pause repeated problems to address their shared cause, and allow one targeted automatic repair per isolated slide problem. Escalate failures with a recommendation and group independent unresolved issues where practical. Further attempts need user authorization; changes to approved content/design need confirmation. Before delivery, check slides, the complete sequence, counts, output format, note consistency, and current-image approval.

All presented workflow design sections are approved. The user selected self-contained handoff planning; concrete implementation choices are now documented in the separate plan below. This design record's technical sketches remain supporting context, and implementation has not started. No fixed count of questions or planning approval rounds is required for every input.

At the user's request, update this existing proposal as the design develops and keep the session memory aligned. A separate implementation plan can translate the fully approved design into file changes and verification tasks after the user chooses that handoff; this document is not an executable implementation plan.

Selected handoff: [the self-contained implementation plan](2026-10-14-predictable-deck-generation-handoff.md) and [its companion execute prompt](2026-10-14-predictable-deck-generation-handoff-PROMPT-execute.md). The plan embeds approved decisions, project rules, the complete speaker-note input, concrete tasks, and verification for another agent/session; no prior chat or memory is required. Execution/publication still requires the corresponding user instruction.

The authoritative record of approvals is [the session memory](../memory/memory-20261014-predictable-ppt-generation.md).

The user's complete speaker-note guidance is preserved in [the verbatim speaker-notes reference](../memory/memory-20261014-predictable-ppt-generation/speaker-notes-style-reference.md). Read that full source when resuming note planning, authoring, QA, or implementation of this addition, including after compaction; condensed descriptions in this design are navigation aids and must not replace the original wording and examples.

## Goal

Agree on the deck's message, each slide's visible content, its visual explanation, and its layout before committing to full image generation. Use the agent to propose good defaults and resolve routine choices, while keeping the user's review effort proportional to meaningful decisions rather than slide count. Avoid discovering a substantially different presentation after a long generation run.

Predictability here means conformance to an approved content and visual plan. It does not mean identical pixels across image generations. The existing architecture generates whole-slide images; precise typography, geometry, and unchanged chart pixels remain limitations of that architecture.

## Recommendation

The approved direction is to extend Codex PPT with self-contained adaptive planning that borrows the questioning and design principles of clarify-requirements and brainstorming. Combined planning, deck-wide continuity, sample calibration, production enforcement, consolidated review, and repair/delivery behavior are approved. Concrete file and schema changes belong in the subsequent implementation handoff.

Clarification, whole-deck planning, and samples adapt to existing input and confirmed decisions. Consolidated review is the approved recommended default for the revised skill, with strict batch review available as an alternative. State the chosen process in each deck's plan and record actual user decisions. Approval of this skill design does not approve a future deck's plan, samples, or images, and does not waive the unmodified skill's gates for an existing live run.

## 1. What the current skill already controls

The current instructions contain useful controls:

- Identify topic, audience, purpose, slide count, and included/excluded sections.
- Draft an outline containing a title, three to five key points, slide role, language, and required source images for each page.
- Stop for outline approval before downstream production.
- Confirm style, image proportions, image backend, and one representative sample.
- Give workers complete deck and slide context, including required assets and the approved sample as a style reference.
- Record worker dispatches, backend labels, image results, and user image approvals.
- Verify image proportions and invalidate image approval when the approved PNG changes.
- Inspect outputs, write speaker notes, and assemble plain and/or Medavis decks.

Evidence: [skill contract](D:/git/codex-ppt-skill/skills/codex-ppt/SKILL.md:72), [outline rules](D:/git/codex-ppt-skill/skills/codex-ppt/docs/outline-style-and-sample.md:9), [generation context](D:/git/codex-ppt-skill/skills/codex-ppt/docs/slide-generation-and-subagents.md:45), and [image approval validation](D:/git/codex-ppt-skill/skills/codex-ppt/scripts/slide_run_state.py:209).

## 2. Where surprises can enter

| Gap | Consequence | Proposed control |
|---|---|---|
| Content clarification is a broad instruction with no readiness criteria. | A thin paragraph can be expanded differently by different agents. | Classify missing information and resolve material gaps before planning. |
| Added claims need no recorded source or assumption status. | The user may approve a plausible outline without noticing unsupported facts. | Track facts, proposed interpretations, and unresolved information explicitly. |
| Outline bullets can remain broader than the visible slide wording. | Wording, density, emphasis, or numerical labels can change during prompt preparation. | Approve intended visible copy and critical labels in the storyboard. |
| Detailed composition and visual elements are prepared after the main outline approval. | A correct topic may become an unexpected chart, metaphor, or diagram. | Approve visual type, subject, relationships, and composition before generation. |
| Shared style and deck context alone do not specify every cross-slide relationship. | Individually reasonable slides may repeat, contradict, renumber, or redraw shared concepts inconsistently. | Plan the narrative and recurring-element relationships for the deck, pass relevant context to workers, and check the complete sequence. |
| One sample validates one page type. | A simple sample can hide difficulties on dense diagrams or evidence slides. | Choose the most representative/risky page; add a second sample only when justified. |
| Planning approval is not bound to the actual production inputs. | Changes to the specification, prompt, or source assets can escape reapproval. | Record approval against normalized plan and asset hashes. |
| Every generated page requires review before the next wave by default. | Interaction count grows with deck size and runtime capacity. | State consolidated review in the approved deck plan and support bulk approval, preserving strict review as an alternative. |
| Assembly relies on agent discipline for review readiness. | Direct assembly can bypass the intended managed workflow. | Validate production and review state for skill-managed assembly. |
| Template selection occurs immediately before assembly. | The final count and branded opening/ending can surprise the user late. | Agree on output profile and total slide count in the brief; ask later only if unresolved. |
| Speaker notes are elaborated after planning. | Notes can introduce explanations or claims the user never reviewed. | Approve the speaking purpose per slide; restrict final notes to approved facts and narrative. |

The three-to-five-point outline rule should also become role-dependent. A cover or conclusion need not contain three points, and thin source material should not be padded simply to meet a fixed slide count.

### Verification of these findings

All 75 existing script unit tests passed using the shared Python runtime. This confirms the current tested behavior; it does not validate the proposed workflow or visual model quality.

A separate temporary fixture called the real prompt-preparation entry point with a one-slide specification containing no approval record, layout, claim source, backend lock, or sample method. It returned exit code 0 and wrote a prompt job. Its expected backend and sample method were null. The fixture generated no slide image and was removed automatically. This demonstrates that these preconditions currently depend on the agent following instructions rather than script validation.

Dispatch records a prompt hash, but result recording does not compare the current prompt to that dispatch hash. Assembly reads the image folder and notes; its entry point does not validate the job/review ledger. Existing image review validation is stronger: it checks the approval against the current PNG hash.

Evidence: [prompt preparation](D:/git/codex-ppt-skill/skills/codex-ppt/scripts/prepare_slide_prompts.py:423), [dispatch recording](D:/git/codex-ppt-skill/skills/codex-ppt/scripts/record_slide_dispatch.py:50), [result recording](D:/git/codex-ppt-skill/skills/codex-ppt/scripts/record_slide_result.py:163), [assembly entry point](D:/git/codex-ppt-skill/skills/codex-ppt/scripts/assemble_ppt.py:494), and [current review policy](D:/git/codex-ppt-skill/skills/codex-ppt/docs/workflow-gates-and-progress.md:25).

## 3. Three approaches

| Approach | Benefit | Cost and limitation | Recommendation |
|---|---|---|---|
| Extend Codex PPT with compact planning and enforced approvals. | Controls content and visual intent; remains portable; supports approval of the whole deck. | Requires documentation, schema, script, and behavior-test changes. Images still vary. | Recommended for the stated goal. |
| Require full clarify-requirements and brainstorming workflows before Codex PPT. | Reuses existing questioning and design processes. | Adds dependencies and potentially repeated confirmations. General clarification does not itself produce a complete slide contract or prevent production drift. | Optional integration for this workspace, not a mandatory dependency for all users. |
| Render text, charts, and layouts deterministically as native slide objects. | Stronger control over exact copy, positioning, and data fidelity; editable output. | Changes the current full-slide-image architecture and its rendering rules. | Consider if exact geometry or strict chart fidelity becomes essential. |

Clarify-requirements and brainstorming are already available in this session. Installation is not required to use them here. A distributed Codex PPT skill should not assume every host has this personal skill collection.

## 4. Approved workflow design

### A. Assess the input and clarify intention (approved principles)

The agent assesses content readiness separately from visual readiness, potentially per slide for mixed inputs. Prepared content can lack a visual design, and a visual reference can lack content. Extract what is already known, identify reusable material, recommend the route, and ask only about genuine gaps that could change the message or correctness. Resolve consequential context before drafting or expanding around assumptions.

Potential brief questions cover audience, desired outcome, scope, language, presentation length, slide-count target, visual direction, output profile, and review policy. These are examples: the agent must identify and order any additional questions that materially clarify intention, and avoid repeating already answered questions. Distinguish content-slide count from final slide count: eight generated content pages produce eight plain slides or ten Medavis slides.

For topic-only input, clarify whether the user wants a general explanation, externally researched material, or a presentation about their own organization. Company facts and missing measurements remain unresolved until supplied. Proposed arguments and illustrative examples may be drafted, but must be identifiable as proposals. Ordinary layout and wording choices can be recommended by the agent.

Ask about the highest-impact missing decision first. Avoid questions whose answers are already in the source. The user selected quality first and flexible review time; unresolved factual blockers must not be suppressed to meet an interaction budget. Extract or confirm each deck's output profile and review process rather than guessing them during final assembly.

### B. Propose the story and combined content-and-visual plan (approved principles)

The agent recommends a narrative and provides alternatives only when they offer a meaningful trade-off. Develop the deck's content and visual intent together, preserving prepared wording unless revisions are requested and clearly flagging additions or missing evidence. Reuse supplied designs and confirmed style choices; otherwise recommend a cohesive style, with layouts suited to each slide's role. Review the complete plan by exception without imposing an extra content approval round on every input.

Visible-copy and visual-intent requirements and the speaker-note factual boundary are approved. The following slide-card format is a candidate representation; exact schema and presentation details belong in implementation planning:

- Its purpose and one main takeaway.
- The intended visible title, short body copy, and exact critical labels/values.
- The facts or source material supporting substantive claims.
- The visual type and subject: diagram, source figure, illustration, screenshot, comparison, or table.
- Important objects, relationships, arrows, axes, or legends.
- Approximate composition and density, such as a process on the left and its outcomes on the right.
- Required assets, clearly separated from style references.
- The intended spoken explanation and transition in one or two sentences.
- Any unresolved information requiring the user, rather than being silently filled in.

Exact pixel coordinates are not promised by an image-generation workflow. For a complex visual, an optional simple wireframe may make its structure easier to review. Such previews must be labelled planning artifacts and kept separate from final slide images; they do not become a local-rendering fallback for production.

The user approves the whole storyboard or names exceptions: for example, approve everything except slide four, which should explain the process rather than compare products. The agent revises only affected cards, summarizes the changes, and asks about those exceptions. No slide-by-slide interview is required.

#### Deck-wide continuity (approved)

The deck is the unit of design. Every slide has a role in the overall argument or story, builds on what the audience has already learned, and connects reasonably to the next slide. Check for gaps, contradictions, unnecessary repetition, and abrupt transitions across the sequence.

Recurring objects, terms, symbols, colors, and diagrams must retain their identity and meaning wherever reused. Related visuals should build on the same agreed representation when appropriate, so audiences can recognize a concept as the story develops. Keep numbering and cross-references coherent across slide boundaries according to the intended scheme, including consecutive numbering for sequences that continue on another slide. The user's examples do not prescribe an exhaustive checklist or mandatory visible page numbers; identify other deck relationships that matter for the specific presentation.

Give each slide worker shared references and relevant narrative and cross-slide context. QA examines the complete sequence as well as individual slides. The technical representation of shared elements belongs in implementation planning; the approved review process is described below.

### C. Lock the approved plan and calibrate samples (approved)

The sample strategy and production-locking principles are approved. The approved plan is the source of truth for wording, facts, visuals, shared elements, and slide connections. Scripts check that full generation uses the current approved plan, assets, and accepted samples; missing or outdated approval stops production. Exact approval encoding and hashing remain technical planning choices.

A candidate implementation uses a draft specification before approval, then generates the readable outline from the approved structured specification. Avoid independently editable records that can diverge from the same approved plan.

Normally generate one representative content slide, preferably the page that tests the hardest important visual requirement. Reuse the accepted sample as its final page, or reuse a suitable existing approved sample when it fits the current deck. If the deck contains substantially different visual approaches, explain why an additional sample would help; sample count should depend on design risk rather than a fixed quota.

Sample feedback may calibrate typography, spacing, palette, or illustration treatment. Accepted typography, colors, visual language, and recurring elements become shared references for production while layouts vary by slide purpose. Changes to approved meaning, visible claims, or diagram relationships must be shown as storyboard changes. Update affected decisions before producing the remaining deck. Samples test rendering; complete-deck continuity still needs the sequence checks approved above.

### D. Produce within the approved contract and review the deck (approved)

Compile jobs from the approved specification, including locked content, visual brief, background, assets, sample, shared references, and cross-slide context. Workers may repair rendering while preserving the plan. If content cannot fit or a relationship needs changing, raise that decision before changing it. Revisions identify affected slides and shared dependencies and revisit affected decisions; a deck-wide change can affect every slide.

State the chosen production/review process in each deck's plan:

- Consolidated (recommended default): after plan and sample approval, the agent checks every generated slide against the plan and checks the complete story, recurring elements, terminology, numbering, and cross-slide consistency. Present the deck together for approval or named exceptions. After corrections, review changed slides and affected connections. Routine successful batches do not each require a user turn.
- Strict batch review (alternative): retain per-wave user inspection of full-resolution images before the next batch. Support one bulk decision, such as approve the batch except two named slides.

Consolidated review changes the current mandatory wave gate and needs an explicit policy in instructions and state. Final assembly requires real user approval of the current images. Record agent QA separately from user approval; a bulk decision identifies its current image set rather than fabricating individual review conversations. Material deviations or repeated generation problems trigger an early stop of affected work.

### E. Repair and verify final delivery (approved)

Check the first production batch before the remaining slides. A repeated problem triggers a pause to address its shared cause before spending the remaining generation budget.

For an isolated rendering problem, attempt one targeted automatic repair per affected slide while preserving approved wording, facts, and relationships. If it fails, explain the problem and recommend the next action. Group independent unresolved issues into one exception report where practical. Further attempts remain available with user authorization when quality warrants them. Content/design changes require confirmation of affected decisions; the retry limit is not permission to deliver unresolved errors.

Use structural checks for ratios, expected files/counts, backend labels, plan versions, and review status. Use visual inspection, optionally assisted by OCR, for visible text, critical numbers, relationships, asset fidelity, and style. Low-confidence readings become exceptions; OCR is not proof that a chart or image preserved its meaning.

Before delivery, check slides, the complete sequence, final counts, output format/profile, speaker-note consistency, and approval of the current images. Missing capabilities or a systematic mismatch stop affected work early. Report actual progress and repair count; do not promise an exact runtime without evidence. Specific QA tooling and state fields remain implementation-planning choices.

Finalize speaker notes using the approved factual content and speaking purpose. Notes may elaborate explanation and transitions, but may not silently introduce new substantive claims.

### F. Plan and author the spoken presentation (approved)

Natural spoken delivery is a core quality requirement across presentation types, including technical, research, training, product, and executive decks. The user's verbatim reference above defines the desired voice and rhythm. Its topics and names illustrate the style; each deck's factual content and speaker names come from its own approved material.

- Use the presenter's own voice, speaking directly to the audience with appropriate first-person phrasing, warmth, and small natural asides.
- Write thought-sized beats with blank lines where the speaker breathes. A beat can contain one or several sentences; it follows one thought rather than a fixed paragraph quota.
- Use everyday workplace vocabulary. Introduce an exact technical term in the same breath when the audience needs it. Ground explanations in concrete situations before abstract concepts and explain the slide's meaning.
- Use spoken connectors and a natural speech rhythm in the presentation language. Retain conversational phrasing rather than smoothing it into formal written prose.
- Connect the whole talk: openings, progression between slides, questions answered by the next slide, supplied-name speaker handovers, and a close with an invitation for questions. Fit note length to intended speaking time and review pacing and continuity across the deck.

Draft notes alongside the slide plan rather than treating them only as a final assembly task. Show a representative note to calibrate the voice, and review the complete talk by exception before expensive image generation, without a mandatory per-slide interview. Reuse supplied notes and clearly flag proposed revisions. Finalization checks consistency with the accepted slides and approved narrative; new substantive claims need approval. Preserve the existing slide-to-note mapping in PowerPoint assembly.

The current notes guide already requires presenter language, deck context, transitions, and presentation-language matching. Implementation should strengthen those rules with the source's beats, concrete-first explanations, everyday vocabulary, speech rhythm, timing, and earlier review. Natural delivery is the common baseline; presentation purpose determines emphasis and detail. Specific timing data, note-state fields, QA tooling, and packaged reference layout remain implementation-planning choices.

## 5. Candidate implementation changes (not yet authorized)

### Instructions and schema

Extend the main skill contract and add focused supporting guidance for content planning/storyboard approval and natural speaker-note authoring. Update the outline, generation, asset, progress, assembly, and worker instructions to reference the same production contract. The implementation plan must read the full verbatim speaker-note source and preserve it separately from derived portable skill guidance.

Extend the deck specification with brief, review policy, claim/source status, slide visible copy, visual brief, deck narrative, shared references, cross-slide dependencies, speaking intent, unresolved blockers, repair-attempt state, and approval evidence. Keep detailed technical state out of the user-facing approval cards.

### Approval and validation

Add an approval-recording helper and a shared validator. Normalize the approved plan, excluding transient bookkeeping fields, and bind approval to its hash. Bind strict assets to their content hashes, not only filenames. Record sample approval against the approved image and visual settings.

Prompt preparation should refuse a managed production run with unresolved blockers or stale/missing plan/sample approval. Dispatch should validate the compiled job against the approved plan. Result recording should validate the dispatched prompt version and store the plan version used. Assembly should validate the expected image set, production version, review policy, and actual review/QA evidence.

Changing substantive slide copy, a critical figure, or an approved relationship invalidates the affected approval and downstream jobs. Pure rendering repairs that preserve the plan need image review under the selected policy, without restarting the whole planning process.

If legacy image-only assembly must remain supported, make it a clearly explicit path. Missing managed-workflow metadata must not silently become an escape from validation.

### Existing components to change

| Component | Proposed responsibility |
|---|---|
| Main skill and content-planning docs | Input readiness, compact brief, storyboard, and user decision boundaries. |
| `prepare_slide_prompts.py` | Compile approved copy and visuals; validate approval and blockers before jobs. |
| `slide_run_state.py` | Plan version, selected review policy, repair attempts, separate agent QA and human approval. |
| `record_slide_dispatch.py` | Validate plan/job version and record exact dispatch inputs. |
| `record_slide_result.py` | Check prompt-version consistency and retain generation evidence. |
| `record_user_review.py` | Bulk approval/clear operations following a real user decision. |
| `assemble_ppt.py` | Enforce readiness for managed decks and expected output counts. |
| Worker prompt | Preserve approved content and visual relationships; escalate substantive changes. |
| Smoke fixtures and tests | Verify the new behavior under thin inputs, drift, pressure, and normal use. |

Repository documentation changes must synchronize the Chinese, English, and Korean READMEs and usage pages. User-visible changes need an English Unreleased changelog entry and the eventual PR reference.

## 6. Candidate tests and pilot criteria

Add unit tests for missing/stale approvals, plan and asset hash changes, modified prompts after dispatch, review-policy handling, bulk approval, exact image sets, and Medavis counts/notes mapping.

Add behavior scenarios that check the agent's actual decisions:

1. A rough company paragraph with missing metrics: ask for facts or leave explicit blockers; do not invent percentages.
2. A sufficiently detailed report: extract content and recommend a brief without an unnecessary interview.
3. A ten-slide deck: offer one complete storyboard and accept exceptions without ten approval conversations.
4. An instruction to start images before content approval: preserve the approved workflow boundary.
5. A named-slide edit affecting another page: show the affected set and update only its approvals/jobs.
6. A changed source figure or visible title after approval: reject stale production inputs.
7. A worker trying to add labels, simplify a relationship, or switch the backend: escalate or reject.
8. A poor first wave: stop before generating the rest; use the agreed repair budget.
9. An OCR result with low confidence or a possibly altered chart: flag an exception rather than claiming certainty.
10. Speaker notes introducing a new claim: require content approval or remove the unsupported addition.
11. Consolidated review: state the process in the deck plan, keep agent QA separate, and require actual user approval of the current final image set. Existing live runs retain their established policy unless explicitly changed.
12. Planning wireframes: never use them as final generated slide images.
13. A concept reused across several slides: preserve its name, visual identity, and meaning while the explanation develops.
14. A numbered sequence spanning slides: preserve the agreed numbering and cross-references without accidental resets or duplicates.
15. Individually plausible slides with a contradictory or incomplete story: identify the deck-level problem before treating the sequence as ready.
16. A suitable previously approved sample: reuse it when it fits the current deck and its approval is valid; justify additional samples by the visual requirements.
17. An isolated rendering failure: allow one targeted automatic repair, then escalate unresolved issues; further attempts need authorization and preserve approved decisions.
18. A recurring first-batch problem: pause and correct its shared cause before producing the remaining deck.
19. Speaker notes across presentation types and languages: preserve presenter voice, breathing beats, concrete explanation, natural connectors, transitions, and intended pacing without inventing facts or personal experiences.
20. Prepared notes: reuse their content and voice, flag proposed revisions, and review the talk by exception rather than rebuilding it or requiring an interview for every slide.

Pilot the revised workflow on a topic-only deck, a prepared slide-by-slide deck, partial/mixed-readiness material, and a deck with supplied figures. Measure substantive corrections after generation, clarification/review turns, repairs, image calls, and time to the first useful preview. Quality is the priority; review effort and checkpoints must adapt to the source and topic rather than meet a fixed time or interaction count.

## 7. Practical next step

The workflow design and speaker-note addition are approved. The user selected a self-contained handoff plan for another agent/session; that plan and its companion prompt are saved and linked above. The next route is critical plan review, requested execution, user review/use elsewhere, or deferral. Do not repeat the handoff-mode question or begin implementation merely because the planning files exist.

The work delivered here is the analysis, confirmed requirements, and approved workflow design, saved by updating the existing proposal in place. Earlier checkpoints were committed and pushed as `ae15e634d6a9630422082de2904364be979faca5` and `99fba3d3ea2d8f1d285cf40dbf44d8e32f05d126`; this subsequent design/memory update is saved locally. No skill implementation files have been changed, no skills installed, and no slide images generated. The `main` branch remains unchanged.
