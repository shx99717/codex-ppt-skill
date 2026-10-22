# Standard Workflow

## Adapt to the input

Start with a topic, rough notes, a report, prepared slide Markdown, or a mixture. The agent assesses content and visual readiness separately, reuses supplied decisions and exact prepared copy/notes, and asks only consequential questions before expanding content. Audience, purpose, prior knowledge, tone, setting, language, timing and scope can change the result; they are examples, not a fixed interview. Quality comes first.

## Plan the whole deck and talk

Before expensive images, review a compact whole-deck plan: story and page roles, exact visible wording and critical values, intended objects/relationships/composition, source assets and fidelity, recurring visual identities, numbering and dependencies. Proposed additions and missing evidence remain identifiable; company facts and measurements are never invented.

Draft speaker notes at this stage in the presentation language. They sound like the presenter explaining to people in the room: first-person warmth, concrete scenes, everyday words, thought-sized beats separated by blank lines, natural connectors and purposeful transitions. Length follows speaking time. Preserve supplied notes; flag significant proposed rewrites. A representative note can calibrate the voice before reviewing the whole talk by exception.

## Lock style, ratio and executable method

Choose from thirteen built-in styles, personal styles or a supplied reference; normally the agent recommends a small relevant shortlist. See [Styles and Personal Style Library](/en/styles.md). Keep recurring identities coherent while varying composition by page role.

Prefer callable Codex `image_gen` or Cursor `GenerateImage` using the live tool schema. Native model identity is host-managed. Codex can request 16:9 or 4:3 in the prompt without a size parameter; Cursor should pass the supported `aspect_ratio` value. Measure actual saved width/height (2% ratio tolerance); requested resolution is not proof of native 4K. API fallback reuses an explicitly configured provider model; if absent, select one using current documentation. There is no fixed model default. Attach every required source/style image through the actual input mechanism and record attempt-bound submission evidence. Native/bridge evidence is agent-reported; CLI adapter verification requires registered successful execution. Old project files remain readable, but new managed execution/assembly requires recompilation and fresh evidence. Only 16:9 and 4:3 decks are supported; no automatic conversion of old ratios.

The backend and full configuration stay approved. For the bundled CLI, explicitly approve a text-only generate operation and an image-conditioned edit operation when applicable; managed jobs use the adapter that forwards exact settings and all verified images, rather than text-only batch replay.

Style, ratio, backend/configuration, required sample strategy, output profile/title and review policy are settled in the draft before this combined approval. Approve content, visuals, talk, output profile/landing title and review policy together. Prepared material needs only its real gaps filled; there is no required bullet count or interview for every page. On revisions, review affected scopes and dependent pages instead of rebuilding everything.

## Calibrate before production

After plan/talk approval, generate or reuse an appropriate representative content sample. Accept its actual appearance and suitability before bulk production. Additional samples need a material visual reason. Accepted style-reference bytes remain immutable; repairing the sample's final content page does not replace the shared reference. A defective calibration sample can be repaired before acceptance.

## Generate, inspect and review

Compile approval-bound jobs. Use one slide worker per job when available; the parent owns canonical content, state, QA and final files. Workers preserve exact wording, values, assets and relationships; they report fit problems instead of rewriting content.

Inspect the first production batch before later production. Check every image and then the complete ordered story, numbering, shared visuals and talk transitions. One isolated rendering defect gets one targeted automatic repair under its current visual contract. Further attempts need actual authorization. Repeated first-batch failures pause production for their common cause.

Consolidated review is the default: routine successful batches continue, then the user reviews the current deck together and names exceptions. Strict review is available for approving each batch. Agent QA is separate from human image acceptance and cannot manufacture that acceptance.

## Assemble and deliver

The managed scripts require current scoped plan/talk/policy decisions, source and sample bytes, compiled inputs, completed results, per-slide/sequence QA and current-image user approval. Changed facts/source relationships also invalidate affected talk; note-only revisions retain current images. Final outline and talk derive from the approved plan.

Use the already-approved plain, Medavis or both profile and landing title. Plain has N content pages; Medavis uses the matching bundled three-page template with landing + N content + ending (N+2), and content notes are offset by one. Delivery includes actual paths, counts, backend, notes and limitations. The slide visuals are raster images, so text/charts are not separate editable objects.

Historical pre-v2 manual/image folders require explicit `--legacy-unmanaged`; the flag cannot bypass a managed deck. Custom/adapted styles may be saved in the personal style library after acceptance.
