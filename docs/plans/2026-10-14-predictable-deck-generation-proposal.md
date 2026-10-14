# Proposal: Make Codex PPT Results Predictable

Date: 2026-10-14, Asia/Shanghai

Scope: analysis and proposed design for the repository at `D:/git/codex-ppt-skill`, on `feature/SQ5GEN-predictable-deck-generation`, created from `main` at the user's request. The user authorized a planning-document commit/push checkpoint on 2026-10-14. No skill implementation or installation changes have been made.

## Confirmed decisions and draft status

The user restarted requirements clarification after the original proposal and confirmed the following:

- Approved facts, messages, visible wording, and visual structure must stay fixed, with minor rendering differences allowed.
- Quality comes first; review time depends on deck length and topic difficulty. There is no fixed review-time target.
- Input can be complete slide-by-slide Markdown, partial material, or only a topic/idea. Content readiness and visual readiness must be assessed separately; supplied structure, wording, and confirmed decisions should be reused.
- The selected approach is adaptive planning inside the PPT skill. Mandatory installation of other planning skills is not the chosen architecture.
- Input assessment is approved: identify reusable material and missing decisions, potentially per slide, and recommend an appropriate route.
- Content development is approved: understand the user's intention and resolve consequential context before expanding content; intelligently choose/order questions and treat audience/tone/etc. as examples rather than an exhaustive checklist.
- Preserve prepared content unless revisions are requested. Clearly distinguish proposed additions and missing facts/evidence. Develop the whole deck's content together and feed it into a combined content-and-visual plan without a mandatory separate content approval round for every input.

Visual-plan details, exact approval format, sample strategy, production validators, and generated-image review policy remain candidates for subsequent design discussion. The proposed checkpoint counts, schemas, and implementation changes below are not yet approved and must not become a fixed workflow for every input.

The authoritative record of approvals is [the session memory](../memory/memory-20261014-predictable-ppt-generation.md).

## Goal

Agree on the deck's message, each slide's visible content, its visual explanation, and its layout before committing to full image generation. Use the agent to propose good defaults and resolve routine choices, while keeping the user's review effort proportional to meaningful decisions rather than slide count. Avoid discovering a substantially different presentation after a long generation run.

Predictability here means conformance to an approved content and visual plan. It does not mean identical pixels across image generations. The existing architecture generates whole-slide images; precise typography, geometry, and unchanged chart pixels remain limitations of that architecture.

## Recommendation

The approved direction is to extend Codex PPT with self-contained adaptive planning that borrows the questioning and design principles of clarify-requirements and brainstorming. A combined content-and-visual plan and its production enforcement are proposed design mechanisms to develop in the remaining discussion.

Candidate checkpoints are a brief, a complete slide plan, and a representative sample; their application must adapt to existing input and confirmed decisions. No fixed count of questions or approval rounds is approved. A balanced review policy with one consolidated review of generated slides, alongside the existing strict review policy, remains a proposal. If adopted, the user must explicitly choose that production/review authorization; it must not be inferred from approving the sample.

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
| One sample validates one page type. | A simple sample can hide difficulties on dense diagrams or evidence slides. | Choose the most representative/risky page; add a second sample only when justified. |
| Planning approval is not bound to the actual production inputs. | Changes to the specification, prompt, or source assets can escape reapproval. | Record approval against normalized plan and asset hashes. |
| Every generated page requires review before the next wave by default. | Interaction count grows with deck size and runtime capacity. | Add an explicitly selected balanced policy and bulk approval, preserving strict review. |
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

## 4. Recommended user journey

### A. Assess the input and recommend a brief

The agent first classifies the source as sufficient, partial, or topic-only. It extracts what is already known, proposes sensible defaults, and identifies only gaps that could change the message or correctness.

Potential brief questions cover audience, desired outcome, scope, language, presentation length, slide-count target, visual direction, output profile, and review policy. These are examples: the agent must identify and order any additional questions that materially clarify intention, and avoid repeating already answered questions. Distinguish content-slide count from final slide count: eight generated content pages produce eight plain slides or ten Medavis slides.

For topic-only input, clarify whether the user wants a general explanation, externally researched material, or a presentation about their own organization. Company facts and missing measurements remain unresolved until supplied. Proposed arguments and illustrative examples may be drafted, but must be identifiable as proposals. Ordinary layout and wording choices can be recommended by the agent.

Ask about the highest-impact missing decision first. Avoid questions whose answers are already in the source. A target of a small number of clarification rounds is useful, but unresolved factual blockers must not be suppressed to meet an interaction budget.

### B. Propose the story and one complete storyboard

The agent recommends a narrative and provides alternatives only when they offer a meaningful trade-off. It then drafts the complete deck in one pass.

Each slide card contains:

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

### C. Record the approved plan and check one sample

Before approval, use an explicitly draft specification. After approval, make the structured specification the source of truth and generate the readable outline from it. Do not maintain independently editable versions of the same slide content.

Generate one representative content slide, preferably the page that tests the hardest important visual requirement. Reuse the approved sample as its final page. If the deck contains genuinely different high-risk visual types, propose a second sample and explain why it is worth the extra call.

Sample feedback may calibrate typography, spacing, palette, or illustration treatment. Changes to approved meaning, visible claims, or diagram relationships must be shown as storyboard changes. Update the plan before producing the remaining deck.

### D. Produce within the approved contract

Compile jobs from the approved specification. Include the locked content, visual brief, relevant background, assets, sample, and supported generation settings. Workers may execute the design and repair rendering problems; they must request a plan change when the approved content cannot fit or needs substantive revision.

Agree on the production/review policy at the brief stage:

- Strict: retain per-wave user inspection of full-resolution images. Support one bulk decision, such as approve the wave except two named slides.
- Balanced: after storyboard and sample approval, authorize production within that plan. The agent checks every output, stops on material deviations, and presents one consolidated gallery for user review before final assembly. Routine successful waves do not each require a user turn.

Balanced mode changes the current mandatory wave gate and therefore needs an explicit new policy in both instructions and state. Agent QA must be recorded separately from user approval. It must never fabricate per-slide user-review markers.

### E. Check conformance and stop early on systematic problems

Check the first production wave before continuing. A repeated text, style, or diagram problem should trigger a pause and calibration instead of consuming the remaining image budget.

Use structural checks for ratios, expected files/counts, backend labels, plan versions, and review status. Use visual inspection, optionally assisted by OCR, for visible text, critical numbers, relationships, asset fidelity, and style. Low-confidence readings become exceptions; OCR is not proof that a chart or image preserved its meaning.

Set an agreed repair budget, for example one automatic repair per slide before escalation. Missing capabilities or a systematic mismatch should stop the run early. Report actual generation progress and repair count; do not promise an exact runtime without evidence.

Finalize speaker notes using the approved factual content and speaking purpose. Notes may elaborate explanation and transitions, but may not silently introduce new substantive claims.

## 5. Implementation changes

### Instructions and schema

Extend the main skill contract and add a focused supporting guide for content planning and storyboard approval. Update the outline, generation, asset, progress, assembly, and worker instructions to reference the same production contract.

Extend the deck specification with brief, review policy, claim/source status, slide visible copy, visual brief, speaking intent, unresolved blockers, and approval evidence. Keep detailed technical state out of the user-facing approval cards.

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
| `slide_run_state.py` | Plan version, selected review policy, separate agent QA and human approval. |
| `record_slide_dispatch.py` | Validate plan/job version and record exact dispatch inputs. |
| `record_slide_result.py` | Check prompt-version consistency and retain generation evidence. |
| `record_user_review.py` | Bulk approval/clear operations following a real user decision. |
| `assemble_ppt.py` | Enforce readiness for managed decks and expected output counts. |
| Worker prompt | Preserve approved content and visual relationships; escalate substantive changes. |
| Smoke fixtures and tests | Verify the new behavior under thin inputs, drift, pressure, and normal use. |

Repository documentation changes must synchronize the Chinese, English, and Korean READMEs and usage pages. User-visible changes need an English Unreleased changelog entry and the eventual PR reference.

## 6. Tests and pilot criteria

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
11. Balanced mode without an explicit user selection: retain the existing strict review behavior.
12. Planning wireframes: never use them as final generated slide images.

Pilot the revised workflow on a topic-only deck, a prepared slide-by-slide deck, partial/mixed-readiness material, and a deck with supplied figures. Measure substantive corrections after generation, clarification/review turns, repairs, image calls, and time to the first useful preview. Quality is the priority; review effort and checkpoints must adapt to the source and topic rather than meet a fixed time or interaction count.

## 7. Practical next step

Approve or revise the compact brief/storyboard/sample approach before implementation. Then implement it incrementally: first content planning and approval validation; next production-version checks and managed assembly validation; then balanced/bulk review and behavior pilots. Keep the current strict review path available throughout the rollout.

The work delivered here is the analysis, confirmed requirements, and partially approved design. At the user's request, the proposal was moved into `docs/plans/` on `feature/SQ5GEN-predictable-deck-generation`. The user subsequently authorized committing and pushing this planning-document checkpoint; publication status is recorded by Git history/upstream. No skill implementation files have been changed, no skills installed, and no slide images generated. The `main` branch remains unchanged.
