# Slide Worker Prompt

Use this packet for one managed sample/production/repair job. The parent owns final state/files and actual user decisions.

```text
Generate the single local output slide from <DECK>/prompts/slide_<NN>.json.

Read its prompt, generation_config/sample_generation_method, compiled execution,
phase and input_images. Wait for the parent to record your matching actual dispatch
before calling the backend; preparation alone does not authorize an attempt.
The approved render context contains exact visible_copy, intended visual objects and
relationships, relevant shared identities and dependency background. Dependencies
are context only, not additional output pages. Preserve every approved word,
critical value, symbol meaning and relationship. Metadata/source paths are not text.
A sample reference supplies style only; do not copy its content or composition.

Use the exact selected backend/tool and approved input path/configuration.
Inspect local source/style snapshots and attach every required image through
the actual image tool. A CLI text-only generate path cannot consume image inputs;
return a blocker if the approved path cannot attach them. Do not silently
change backend/model/mode, omit inputs, or use a lower-quality substitute.

For scripts/image_gen.py, use run_slide_job.py DECK --slide ID --agent-id YOUR_ID
--out DECK/candidates/NEW_ATTEMPT.png. This consumes the compiled operation policy
(generate without inputs; explicitly approved reference_mode=edit with inputs),
exact settings and every verified image. Do not replay managed JSON with generate-batch.

Ratio is the locked 16:9 or 4:3. For native Codex image_gen, use the explicit ratio in the prompt even if no size/ratio parameter exists. For Cursor pass the supported aspect_ratio value. Never invent parameters or a model ID. Measure original output pixels; reject more than 2% relative ratio error. No stretch/crop/letterbox substitute. Exact/minimum output sizes apply only if approved as requirements.

Attach every input through the live tool mechanism. Inspect local snapshots first, then use explicit reference paths when supported; context-only inclusion needs complete mapping and adequate capacity. Return a blocker if any input cannot be attached. Return an actual submission receipt described in docs/image-submission-evidence.md, bound to dispatch.attempt_id, current job and original candidate bytes. Native/bridge evidence_origin is agent_reported. The bundled CLI emits its own registered receipt after successful execution; do not synthesize one or reuse a different attempt.

Generate one complete raster slide through that backend. Forbidden:
local drawing, Pillow-generated slides, SVG/HTML/CSS/canvas screenshots,
python-pptx/PptxGenJS layout screenshots, manual text/card/chart overlays,
and changing to OpenClaw image_generate or another backend.

Inspect exact text in the slide language, critical labels/data, source-image
inclusion/fidelity, shared identity, relationships, overlaps and truncation.
Repair only rendering within the assigned compiled request. Do not rewrite
approved copy or remove a required label when it cannot fit: return a blocker.

Do not edit the job, spec, approval ledger, other jobs, origin_image, speech,
outline, or final PPTX. Parent alone records results, QA, repairs and acceptance.
Keep your selected original backend-generated candidate outside origin_image.

Return:
backend_used=<actual locked label>
selected_source=<absolute original generated candidate path>
submission_receipt=<absolute actual attempt receipt path>
qa_note=<actual inspection summary>
or blocker=<specific unavailable input/tool/fit/quality issue and evidence>
```
