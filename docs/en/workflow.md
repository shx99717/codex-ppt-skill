# Standard Workflow

## Adapt to the input

Start with a topic, rough notes, a report, prepared slide Markdown, or a mixture. The agent assesses content and visual readiness separately, reuses supplied decisions and exact prepared copy/notes, and asks only consequential questions before expanding content. Audience, purpose, prior knowledge, tone, setting, language, timing and scope can change the result; they are examples, not a fixed interview. Quality comes first.

## Plan the whole deck and talk

Before expensive images, review a compact whole-deck plan: story and page roles, exact visible wording and critical values, intended objects/relationships/composition, source assets and fidelity, recurring visual identities, numbering and dependencies. Proposed additions and missing evidence remain identifiable; company facts and measurements are never invented.

Draft speaker notes at this stage in the presentation language. They sound like the presenter explaining to people in the room: first-person warmth, concrete scenes, everyday words, thought-sized beats separated by blank lines, natural connectors and purposeful transitions. Length follows speaking time. Preserve supplied notes; flag significant proposed rewrites. A representative note can calibrate the voice before reviewing the whole talk by exception.

## Lock style, ratio and executable method

Choose from twelve built-in styles, personal styles or a supplied reference; normally the agent recommends a small relevant shortlist. See [Styles and Personal Style Library](/en/styles.md). Keep recurring identities coherent while varying composition by page role.

Lock 16:9, 4:3 or 3:2 before selecting a backend that can actually express that ratio and attach required images. Inspect the live schema and measured pixels. Cursor GenerateImage is used only for 3:2 pixels; a legal landscape argument may be needed if its enum omits 3:2. gpt-image-2 paths use 2560x1440, 2560x1920 or 2400x1600 when their schema exposes size. Wrong-ratio images are rejected, never stretched or cropped.

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
