# Slide Generation And Subagents

Read before compiling, dispatching, recording or repairing managed slide jobs. Use [workflow gates](workflow-gates-and-progress.md) and the [worker packet](../prompts/slide-worker.md).

## Approved production packet

The parent owns the canonical v2 deck_spec, approval ledger, derived outline/talk, prompts, state, images, QA and assembly. Compile with prepare_slide_prompts.py; never hand-author managed prompt JSON or mark statuses from chat.

```text
prepare_slide_prompts.py --spec DECK/deck_spec.json --out-dir DECK --phase production
slide_job_status.py DECK --json
```

Every packet contains the exact selected render context: deck story/goal/brief/style/language, local visible_copy and visual_plan, used shared meanings/appearances, reachable dependency context and approved source bytes. Unused shared definitions and full note text are excluded. Expand implicit references into meaningful dependencies/canonical terminology during planning; a worker cannot infer context held only in the parent chat.

Each job binds phase, visual scope, generation configuration, current immutable style references, byte-identical source snapshots, and recorded repair inputs. Preserve real image-input roles. Do not render metadata or source paths as slide text. Global context is shared; layout follows the local slide's purpose.

Changing a note does not recompile unchanged imagery. --force validates the complete selection before writing, preserves unchanged results and reviews, and refuses replacing a dispatched job. An old audit version can remain generation provenance when its scoped bindings are still current.

## Actual workers and state

After representative acceptance and full-production authorization, use one worker for each remaining image job whenever agents are available. If a required worker/tool/input is unavailable, record a blocker; do not silently replace the agreed production route with sequential/local rendering.

The parent prepares required images and context, spawns within capacity using preparation-only instructions, records the returned real agent ID, then releases the assigned packet for generation. A worker must not call the backend before its dispatch exists:

```text
record_slide_dispatch.py DECK --slide slide_03 --agent-id ACTUAL_ID
record_slide_result.py DECK --slide slide_03 --agent-id ACTUAL_ID --backend-used LABEL --selected-source GENERATED.png --qa-note "Actual worker result"
record_slide_qa.py DECK --slide slide_03 --pass --evidence "Actual parent inspection"
```

Dispatch rechecks current inputs and compiled SHA. Results recheck the dispatch prompt, selected agent/backend, source/style inputs and pixel ratio before copying to origin_image. Replaced images clear old QA/review. Do not overwrite an approved sample style snapshot when repairing its final page.

Inspect the first production batch before later jobs, then use consolidated or strict review as approved. Record a complete-sequence assessment before delivery. Do not make strict per-wave pauses the unconditional default.

A worker may repair rendering only within approved wording, values, objects and relationships. Report a fit/content blocker rather than rewriting. Parent records needs-repair evidence and compiles --phase repair; one automatic attempt, then actual extra-attempt authorization. A common first-batch problem pauses production and requires a shared-cause correction.

User changes require impact analysis across dependent copy, meanings, assets, numbering, paired layouts, adjacent transitions and talk. Report the affected scope and confirm material changes, reapprove affected plan cards, then regenerate only current invalidated imagery. Preserve unrelated results.

## Backend and asset fidelity

Every final image is a full-slide output of the selected actual backend; no local drawing/Pillow/SVG/HTML/canvas/native-PPT screenshots or manual overlays. Keep candidates outside origin_image until the parent records them. Reject more than 2% relative ratio error rather than stretching, letterboxing or cropping.

Read [backend selection](backend-selection.md) for actual schema checks and locked sizes. Follow the plan's generation method, compiled execution and image-input path. CLI jobs use [the managed adapter](cli-api-fallback.md), which forwards the approved operation/config and verified snapshot inputs, releases global locks for the provider call, and rejects a stale attempt afterward. A text-only generate call is insufficient for nonempty input_images. Never silently omit inputs, change model/backend, or pretend an unsupported mode is compatible.

Inspect local images via the host's image viewer and attach all approved snapshot files through the actual tool's input mechanism. Style references supply palette/typography/visual language, not another page's text/layout. Source figures retain labels/data/arrows/relationships and are inspected after generation.

For multilingual decks, set explicit slide language and render exact text in that language (CJK/Latin/both as needed). The locked ratio outranks a built-in style's example canvas.

## Compatibility

Legacy utility workflows use --legacy-unmanaged explicitly; they cannot act on managed markers. New skill runs always compile v2 jobs. Final naming remains origin_image/slide_01.png, slide_02.png, etc., with no missing, extra or duplicate official slide files. Rejected candidates and references stay elsewhere.
