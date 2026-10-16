# Content Planning And Approval

Read this before expanding source material or preparing a managed deck. This workflow is self-contained; personal clarification/brainstorming skills are not installation dependencies.

## Assess reusable input first

Content and visual readiness are independent, and can vary across a deck. Prepared slide Markdown may already settle wording and talk while lacking diagrams. A style image may settle the look while leaving audience/purpose open. Say briefly what is reusable, what is missing, and the recommended next step. Preserve ready decisions and note paragraphs; show suggested revisions separately.

Clarify consequential intention before expanding content. Audience, prior knowledge, purpose, desired outcome, presentation setting, scope, tone, language, timing and length are examples, not a mandatory questionnaire. Topic-specific risks or decisions may matter more. Extract answers already supplied, order the real gaps intelligently, and recommend defaults with reasons. Quality comes first; effort depends on topic and deck, with no question/time/slide/bullet quota.

For a topic-only input, establish the intended outcome, propose a concrete whole-deck story and explain what you would add. Ask for missing organization facts or approve omission/qualitative treatment; never invent measurements. For prepared Markdown, retain exact supplied wording/talk and fill only visual/connection gaps. In a mixed deck, reuse ready pages and focus attention on unfinished ones.

## One combined deck plan

Use deck_spec.draft.json with workflow_version 2 and derived outline.draft.md/speech.draft.md. Each slide defines purpose/role, exact visible_copy (title/body/critical labels/values), visual_plan (type/subject/objects/relationships/approximate composition), source/proposal status, required_images with role/fidelity, shared_visual_ids, depends_on, and speaker_notes with text, speaking time or null, and transition. Explicit per-slide language is required for multilingual decks.

At deck level record audience/purpose/delivery intent, reusable readiness, story, canonical terminology, shared visual identities, style, backend/tool/input method and ratio, required representative samples, output profile/landing title, and review_policy (recommend consolidated; strict is available). Complete factual blockers before approval. Each claim's provided/proposed/external_source status and evidence stay identifiable.

Treat the deck as the design unit. Plan what the audience knows before/after each page, logical transitions, recurring characters/symbols/colors, shared definitions, and cross-references. Distinguish internal file order 1..N from visible numbering. Continue a sequence at the correct next number; do not add visible page numbers unless chosen. Update meaningful dependencies when a definition or story changes.

Show exact copy and intended visual meaning together. Use simple labeled structural previews when text is ambiguous; these are not final rendering substitutes. Draft the talk now using [the full voice guidance](speaker-notes-style.md). Show a representative note for voice calibration when useful, then review all talk by exception. Notes explain meaning rather than reciting the slide; new substantive claims require approval.

Approve the complete plan/talk once by exception, or only affected scopes on revisions. Do not run interviews for every page or repeat confirmations already supplied. Ask about substantive assumptions and unresolved choices; say what is proposed rather than silently guessing.

## Draft view and actual decision recording

The parent uses the existing runtime interpreter. Technical hashes remain in script summaries, not spoken approval cards.

Start machine-readable drafts from the bundled schema, rather than inventing a nested `deck` wrapper or alternate slide fields:

```text
prepare_slide_prompts.py --write-template INPUT/deck_spec.draft.json
```

Reuse its exact field structure while replacing placeholder values with the developed plan. Top-level fields include `deck_name`, `language`, `aspect_ratio`, `selected_image_backend`, `goal`, `deck_context`, `style`, `planning` and `slides`. Each slide uses `number`, `title`, `intent`, `role`, `key_points`, `visible_copy`, `visual_plan`, `shared_visual_ids`, `depends_on`, `claim_sources`, `required_images` and `speaker_notes`. Relationships are objects with existing `from`/`to` IDs, not prose strings. Preserve approved content while mapping it into those fields. Resolve real blockers before passing the complete candidate to draft-view/approval scripts; the honest template itself is not an approved plan. Use `--help` for CLI flags. A readable card artifact may precede the complete JSON, but do not label an incompatible shape as a runnable managed draft.

```text
planning_views.py --spec INPUT/deck_spec.draft.json --deck DECK --draft
record_plan_approval.py DECK --spec INPUT/deck_spec.draft.json --approve --scope all --expected-plan-hash HASH --evidence "Actual user's approval wording or interaction reference"
```

Draft view resolves relative assets against the original input parent and returns the reviewed candidate hash/provenance. Recording rechecks that hash and source bytes before installing normalized absolute original paths and byte-identical hash-named snapshots. A destination file with the same name is not the source.

The approval ledger separates human visual/talk/policy/calibration/sample/image/extra-repair evidence. Whole-plan visual approval also binds the representative-sample strategy. A missing/stale record refuses production. An actual policy-only decision records policy only; it must not refresh changed slide/talk approval.

```text
record_plan_approval.py DECK --spec DRAFT --approve --scope slides --slides slide_02,slide_03 --expected-plan-hash HASH --evidence "Actual affected-plan decision"
record_plan_approval.py DECK --spec DRAFT --approve-policy --expected-plan-hash HASH --evidence "Actual output/review-policy decision"
planning_views.py --deck DECK
```

The canonical spec is the single content source; outline.md and speech.md are derived approved views. Partial approvals with stale dependents produce draft views while preserving the last fully approved views. Reapprove the affected scope before finalization.

## Impact-aware revisions

Compare affected facts, exact labels, source bytes, relationships, shared meanings and story links. Revisit dependent visuals and talk; a global narrative/audience change may affect the whole deck. Pure color/typography/composition changes do not stale unchanged talk. Talk-only changes do not stale image jobs, but require current talk approval and renewed complete-sequence QA. Output-profile/review-policy/title changes have a separate approval fingerprint.

Rendering corrections stay inside approved copy and relationships. Record QA and compile repair inputs; never edit JSON prompts manually. Preserve unchanged successful results and actual decision IDs. Samples are immutable style references; repairing a sample's final content page does not mutate that reference. An outdated sample can be style-only when still suitable; it cannot silently serve as an approved final content page.

Review source fidelity and spoken continuity as well as individual images. Hashes do not establish factual truth, hidden dependencies or natural speech.
