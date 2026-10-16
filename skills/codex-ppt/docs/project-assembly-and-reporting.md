# Project Assembly And Reporting

Read before initialization, final checks, assembly, or delivery. Plan content and notes earlier using [content planning](content-planning-and-approval.md) and [presenter voice](speaker-notes-style.md).

## Project directory

```text
{base_dir}/{deck_name}/
├── assets/                       supplied originals, if project-local
├── references/sources/           approved byte-identical source snapshots
├── references/approved_samples/  immutable accepted style references
├── candidates/                   generated attempts awaiting parent validation
├── origin_image/slide_XX.png     current final content images only
├── prompts/slide_XX.json         compiler-owned approved inputs
├── deck_spec.json                canonical planning candidate
├── plan_approvals.json           actual scoped decisions
├── slide_jobs.json
├── slide_run_state.json
├── outline.md                    approved readable plan
├── speech.md                     approved talk, mapped by Slide N headings
└── {deck_name}.pptx              plain and/or -medavis output
```

Without a supplied destination, use the working directory or source directory. `{runtime_python}` is the shared `~/.codex-ppt-skill/.venv` interpreter (`Scripts/python.exe` on Windows; `bin/python` elsewhere); `{skill_root}` contains `SKILL.md`.

```bash
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx --init
```

If the shared runtime or dependencies are missing, run `python3 {skill_root}/scripts/codex_ppt_runtime.py bootstrap`. Ask for help only if setup cannot proceed. Initialization creates directories without asserting approval.

## Final checks

Inspect every current image against exact approved wording, values, labels, assets and relationships. Check readability, fitting, spacing, requested numbering and shared visual identity. Review the complete ordered deck for story continuity, sensible composition variety, consistent terminology, consecutive numbering and purposeful spoken transitions.

Record current per-slide and complete-sequence agent QA. Follow [workflow gates](workflow-gates-and-progress.md) for first-batch inspection, one automatic targeted repair, additional actual authorization and consolidated/strict user review. A repair of an accepted sample's final page does not alter its immutable shared style reference. A calibration repair does not require approving the defective sample first. Never rewrite copy or facts to disguise a rendering defect.

`outline.md` and `speech.md` derive from the approved canonical plan. Do not redraft notes at assembly. Preserve supplied approved talk and blank-line breathing beats. If pixels reveal a substantive change needed in copy, visuals or notes, propose the affected scope, obtain the real decision, and refresh its bindings before proceeding.

Speaker headings map internal content order:

```markdown
## Slide 1: Title

Hi everyone.

Let me show you why this matters.

## Slide 2: Next title

Now, here is the next part.
```

These are mapping examples, not a sentence or paragraph quota. Follow the complete [voice reference](speaker-notes-style.md); length follows intended speaking time and complexity.

## Assembly

Use the output profile, landing title and ratio already chosen in plan approval. Reuse explicit decisions; do not add a redundant last-minute template question. A changed output setting requires current policy approval even if slide pixels are unchanged.

```bash
# Approved plain profile
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx --aspect-ratio {locked_ratio}

# Approved Medavis or both profile
{runtime_python} {skill_root}/scripts/assemble_ppt.py {base_dir} {deck_name}.pptx \
  --template both --landing-title "Approved title" --aspect-ratio {locked_ratio}
```

Use `--template medavis` for branded-only output. `{base_dir}` is the parent of `{deck_name}`. File and project names must match. The managed gate enforces current plan, talk, policy, sources, sample configuration, compiled job SHAs, finished results, per-slide/sequence QA and actual current-image user decisions. Missing, extra, duplicate, stale, blocked or unapproved content refuses output. Images assemble in canonical plan order, regardless of job-state array order. Outputs are built from verified snapshots and installed only after revalidation.

Plain output has N content slides. Medavis has N+2:

- Landing page replaces the existing `<PPT-Title>` run; no second title box.
- Content pages use the bundled blank layout and one uniform image scale, with `medavis-logo-small.png` top right at equal 10px margins. Content notes map with an offset of one.
- Original ending page is unchanged, without a generated image, extra logo, or content notes.

The bundled three-page templates are `medavis_ppt_template_2026_en_16-9.pptx`, `_4-3.pptx`. `none`, `medavis` and `both` all support 16:9 and 4:3. The locked pixel ratio is checked within 2% relative tolerance. Wrong-ratio images need regeneration; stretching, cropping or letterboxing cannot count as success. Branded files always use `{deck_name}-medavis.pptx`; `both` delivers both separate files.

## Compatibility

Historical image folders and pre-v2 jobs use `--legacy-unmanaged` explicitly on supported CLIs. That flag cannot bypass an existing managed spec/ledger/jobs. Legacy assembly does not enforce the v2 approval contract; inspect and honestly describe its limitations. New decks use managed mode. Use [CLI fallback](cli-api-fallback.md) for executable managed generation; do not replay nested managed jobs through the old text-only batch CLI.

## Delivery

Report actual project/output/image/outline/speech/job paths and counts; backend and result provenance; note embedding; relevant repairs or remaining limitations; and the approved profile. Do not infer successful rendering or human approval from state labels alone. Slides are full raster images: wording, charts and diagrams are not separately editable PowerPoint objects.

For a custom or adapted style, offer once to save it in the personal style library. If accepted, read [style library](style-library.md). Skip this offer for an unchanged built-in style. Do not let style reuse replace current content, talk or image approval.

See [submission evidence](image-submission-evidence.md) for contract versions, native input mapping, adapter completion and measured output records.
