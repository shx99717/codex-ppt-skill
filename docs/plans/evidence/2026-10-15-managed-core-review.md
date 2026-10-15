# Managed core review — Tasks 2–6

Snapshot: `C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-core-review-1d5apjke/after/codex-ppt`. Base: `99fba3d3ea2d8f1d285cf40dbf44d8e32f05d126`. Reviewed against the frozen `implementation-plan.md`. All locations below are relative to that snapshot and remain stable. No source files were edited.

## Scope and strengths

The changeset is coherent with Tasks 2–6: it adds the semantic contract, approval ledger and views, managed compilation/lifecycle/QA, bulk review, and assembly gates. The explicit legacy test adaptations support the intended compatibility boundary. No unrelated scope drift was found. Skill, documentation, localization, and changelog edits are pending Tasks 7–8 and are excluded from findings.

The common render projection is a sound implementation: prompts and visual fingerprints use the same filtered context; unused shared definitions do not enter the per-slide render context; declared dependencies propagate content and source changes. The talk projection separates semantic meaning from composition, color, and typography. Separate visual/talk event IDs, an explicit output-policy event, and calibration-strategy fingerprints preserve decision scope. Hash-named source/style snapshots, original-source drift checks, explicit managed-versus-legacy gates, and dispatch/result prompt checks are valuable safeguards. Assembly revalidates the approved originals after building temporary outputs and uses a grouped output transaction, which correctly protects prior output on the covered source-drift scenario.

These strengths do not eliminate the verified workflow and persistence failures below.

## Findings

### Important-1 — An accepted sample cannot enter its required repair dispatch

**File:line:** `scripts/prepare_slide_prompts.py:500` (also lines 501–504).

**What's wrong:** A compiled repair job gets `status="accepted"` whenever the existing sample's accepted-final bytes still match, even after agent QA recorded `needs_repair`. Its result is repopulated from the old accepted sample. Dispatch requires `pending`, so the repair cannot run.

**Why it matters:** The approved workflow explicitly requires an accepted sample's final content page to be repairable without replacing its immutable shared style reference. This ordinary path is blocked. The current sample regression only modifies the final PNG externally and checks style-reference survival; it does not exercise the repair lifecycle.

**Executable evidence:** `review/probes.py`, probe `accepted_sample_repair`: compile a deck with an accepted sample; record `--needs-repair` for `slide_02`; compile `--phase repair --slides slide_02 --force`. Compilation succeeds with `phase="repair", status="accepted"`; dispatch exits 1 with `slide_02 must be pending before dispatch; got accepted`.

**How to fix:** Compiled repairs must always become pending attempts and must not be short-circuited into an accepted-final result. Preserve the immutable sample style reference while letting the normal dispatch/result/QA/current-image approval path own the repaired final page. Add a full CLI regression for this sequence.

### Important-2 — A failed first calibration sample has no authorized repair path

**File:line:** `scripts/prepare_slide_prompts.py:436`; consumer counterpart `scripts/planning_contract.py:549`.

**What's wrong:** Every repair phase requires already-approved representative samples. Before the first calibration sample is approved, agent QA can mark it `needs_repair`, but its repair compilation then fails on that missing approval. Recompiling as sample is also refused by the phase-bypass guard.

**Why it matters:** The user cannot repair an unsatisfactory calibration sample within the managed workflow. Approving its defective pixels solely to unlock a repair would misrepresent the actual user decision. The same dead end affects multi-sample calibration when one sample has not yet been accepted.

**Executable evidence:** `review/probes.py`, probe `unapproved_sample_repair`: approve only the plan, compile/dispatch/result a sample job, record `--needs-repair`. Repair compilation exits 1 with `Missing sample approval for slide_02`; sample recompilation exits 1 with `Recorded repair requires --phase repair; production/sample cannot bypass the repair limit`.

**How to fix:** Bind a repair request to the operation it repairs. A calibration-sample repair should retain sample prerequisites and representative-selection checks without requiring the sample it is producing; a production repair should retain production sample prerequisites. Apply this distinction in both compiler and consumer gates, and keep the same bounded repair accounting.

### Important-3 — Deleting the prompt lets production bypass a recorded repair budget

**File:line:** `scripts/prepare_slide_prompts.py:465` (repair guard only runs inside the existing-file branch at lines 469–477).

**What's wrong:** The compiler enforces an existing repair request only if its tracked prompt file still exists. If the file is missing, it creates a production job, preserves the repair counter, and marks the slide pending. Dispatch then takes the production path and does not consume or check its exhausted repair allowance.

**Why it matters:** A missing compiled artifact must fail closed or be reconstructed from the recorded operation. It must not allow another rendering attempt without the required extra user authorization. This bypass also affects sample/production phase integrity after cleanup or external file deletion.

**Executable evidence:** `review/probes.py`, probe `deleted_prompt_bypasses_repair`: after a later production slide fails its initial rendering and one automatic repair, delete `prompts/slide_03.json`; compile production for that slide with `--force`; dispatch exits 0 with `phase="production"` and its existing repair count still equal to 1. No extra-repair event was recorded.

**How to fix:** Validate current repair state independently of prompt-file existence, before deciding the requested phase. Refuse a missing tracked immutable prompt or rebuild the current repair request while preserving dispatch integrity and authorization checks. Add a missing-file phase-bypass regression.

### Important-4 — Approved revisions deadlock first-batch regeneration

**File:line:** `scripts/planning_contract.py:593` (lines 593–596).

**What's wrong:** A sealed first batch demands current QA for every original member before any production dispatch, including redispatch of that member after an approved visual/content revision. Recompilation correctly clears its old QA and makes it pending, so the prerequisite cannot be satisfied until the dispatch that the gate refuses.

**Why it matters:** Revising an approved fact or layout on an early slide is a normal whole-deck review outcome. The implementation propagates stale bindings correctly but cannot render the approved replacement without manually changing state or using an unrelated phase.

**Executable evidence:** `review/probes_additional.py`, probe `first_batch_revision_deadlock`: complete first-batch QA; approve a new visible phrase on `slide_01`; recompile production with `--force`. The slide is pending, first batch is `{"ids":["slide_01"],"sealed":true}`, and redispatch exits 1 with `First production batch needs current agent QA before later dispatch`.

**How to fix:** Bind batch membership/checks to the relevant production attempt or scoped visual versions. Permit regeneration of stale first-batch members while continuing to block later members until the current first-batch images pass QA. Do not reset batch safeguards merely for capacity tuning or note-only changes.

### Important-5 — Assembly can reorder approved images while leaving notes in plan order

**File:line:** `scripts/assemble_ppt.py:510`; validation counterpart `scripts/planning_contract.py:642`.

**What's wrong:** Ready preflight verifies the job ID set but does not enforce or normalize its array order. Sequence QA is correctly bound in canonical plan order, but assembly iterates `jobs["slides"]` in its stored order. Speaker notes remain keyed by canonical content numbers.

**Why it matters:** A reordered job-state array can pass all visual/image/talk approvals and complete-sequence QA, then produce the wrong story sequence with the wrong notes attached to the slide pixels. The resulting file differs from the approved ordered deck.

**Executable evidence:** `review/probes.py`, probe `reordered_jobs_assemble`: create a red first image and white accepted second sample, complete QA and actual fixture image review, then reverse the job array. `require_managed_ready` accepts it and assembly exits 0. The first PPTX image pixel is white `[255,255,255]` rather than the expected first-image red `[255,0,0]`; first-page notes still contain slide 1's opening text.

**How to fix:** Construct the assembly image list from canonical spec/manifest order using a validated job-ID lookup, or reject noncanonical ordering before output. Use the same ordered projection for sequence QA and assembly. Add a job-array reordering regression that checks actual image blobs and note offsets.

### Important-6 — Result copy failures corrupt the previous final image

**File:line:** `scripts/record_slide_result.py:213`.

**What's wrong:** `shutil.copy2` writes directly over the owned final image before job-state persistence. A partial copy failure leaves old job JSON intact while replacing the previous image with incomplete bytes. A later metadata/write failure can likewise leave image and state out of sync.

**Why it matters:** Task 5 explicitly requires rejected/failed mutations to preserve target image bytes and job state. The existing image is a user-visible artifact and may be the previous approved revision. Fail-closed consumers detect the corruption later, but the artifact has already been lost.

**Executable evidence:** `review/probes.py`, probe `failed_result_copy`: start with a blue prior image and a dispatched red result; inject an `OSError` after `copy2` writes partial destination bytes. The operation fails; jobs are byte-identical; `previous_image_preserved=false`; target bytes are `incomplete copy`.

**How to fix:** Copy to a temporary candidate, verify ratio and source/candidate hashes, then install final image and job-state changes with rollback or a fail-closed grouped transaction. Preserve the previous image on copy, revalidation, and state-write failure. Test both partial-copy and state-write failure.

### Important-7 — Failed multi-job compilation leaves unrecoverable prompt/state mismatch

**File:line:** `scripts/prepare_slide_prompts.py:509` (lines 508–515).

**What's wrong:** Prevalidation covers the whole selection, but changed prompt files are then written one at a time before `slide_jobs.json` is saved. If a later prompt write fails, earlier prompts remain changed while their externally stored SHAs remain old. No transaction marker or rollback is used.

**Why it matters:** Subsequent compilation rejects the first file as `Job was edited outside compiler`; ordinary I/O failure turns a valid deck into a state requiring manual recovery. The user asked for predictable fail-closed transitions that preserve existing artifacts.

**Executable evidence:** `review/probes_additional.py`, probe `failed_compiler_write`: approve a change affecting both slides; inject failure on writing `slide_02.json`. Compilation raises; jobs are unchanged, `first_prompt_preserved=false`, and `transaction_marker=false`.

**How to fix:** Stage all prompt payloads and their updated jobs state, then use a grouped transaction with rollback/interruption detection. Reuse the existing grouped installation mechanism or provide an equivalent transaction appropriate for compiled jobs. Add first/second-prompt and jobs-write failure regressions.

### Important-8 — Managed CLI jobs are not executable with their locked configuration and image inputs

**File:line:** `scripts/prepare_slide_prompts.py:402` (lines 400–404); consumer evidence in `scripts/image_gen.py:614`–`624`, `673`, and `941`.

**What's wrong:** The compiler stores model/config fields only inside `generation_config` and `sample_generation_method`. The bundled batch CLI consumes only flat payload keys and silently ignores `input_images`. Every production job contains approved style-image inputs, but the sample's default locked `mode="generate"` maps to the CLI's text-only generation endpoint. The CLI can attach images through `edit --image`, which changes the recorded operation. There is no bundled adapter that enforces/translates the managed job contract.

**Why it matters:** CLI/API fallback is a required retained backend. A valid approved managed plan can dispatch and record a result whose backend label and ratio match while the actual call used different approved quality/size/model parameters and omitted every approved style/source image. Blind job replay is therefore unsafe, while strict adherence to the locked sample operation can make production impossible for a text-only sample followed by image-conditioned production.

**Executable evidence:** `review/probes_additional.py`, probe `compiled_job_batch_dry_run`: a compiled production job with `mode="generate"`, `size="3840x2160"`, `quality="high"`, and one immutable sample input is converted unchanged to one-line JSONL and passed to bundled `generate-batch --dry-run`. It exits 0 but previews `/v1/images/generations`, `size="2560x1440"`, `quality="medium"`, and no attached image. A separate explicit `edit --image SNAPSHOT --size 3840x2160 --dry-run` proves the underlying CLI can consume the snapshot, but its endpoint is `/v1/images/edits` while the job locks `generate`.

**How to fix:** Provide a validated managed-job execution adapter, or a deliberately approved operation policy that maps the logical generation action to the available image-input endpoint. Forward every supported compiled config field and all verified image inputs; reject unsupported fields/operations before dispatch. Cover text-only calibration, image-conditioned production, and repair with dry-run/provider mocks. Do not silently downgrade to text-only generate-batch. This finding concerns the code contract; pending documentation edits are not counted as findings.

### Important-9 — The compiler can overwrite a concurrent worker blocker

**File:line:** `scripts/prepare_slide_prompts.py:440` and `515`; integration counterpart `scripts/record_slide_blocker.py:26`.

**What's wrong:** The compiler reads and replaces `slide_jobs.json` under only `.planning.lock`, without the existing jobs lock. The still-bundled blocker CLI acquires only the jobs lock and can update the same managed file while compilation holds the planning lock. The compiler then saves its older in-memory copy over the new blocker.

**Why it matters:** A worker's unavailable-backend or substantive-fit failure can disappear during an otherwise unchanged compilation/capacity adjustment. Status becomes pending again and the actual unresolved exception is lost. This violates the required planning→jobs lock coordination.

**Executable evidence:** `review/probe_lock.py`: invoke the real blocker CLI immediately before the compiler saves its previously loaded jobs. The blocker exits 0 and the intermediate status is `blocked`; compilation finishes with final status `pending` and `blocker=null`. No fabricated JSON edits are needed.

**How to fix:** Use the established planning→jobs lock order for managed job mutations and include the blocker CLI in that convention. Hold the jobs lock across compiler read/validate/grouped save; release it before run-state synchronization. Add an interleaving regression for blocker and compiler writes.

## Evidence and decisions

Independent verification commands (all exited 0 after a scratch-only UTF-8 correction in the additional probe script):

```powershell
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B 'C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-core-review-1d5apjke/review/probes.py'
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B 'C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-core-review-1d5apjke/review/probes_additional.py'
& 'C:/Users/raymond.shen/.codex-ppt-skill/.venv/Scripts/python.exe' -B 'C:/Users/raymond.shen/AppData/Local/Temp/codex-ppt-core-review-1d5apjke/review/probe_lock.py'
```

All probe decks, synthetic PNGs, transient outputs, and injected filesystem failures were confined to `review/` scratch directories, which the probes remove on completion. No live API or image generation call was made. The existing 145-test GREEN result was reported by the parent; it was not independently rerun because these targeted additional scenarios directly demonstrate the uncovered failures.

Review choices: preserve the requesting agent's technical improvements when they satisfy the user goal; do not require literal reference-code copying; distinguish a supported manual CLI edit from executable replay of the compiled managed contract; treat missing artifacts and permitted job-state rewrites as consumer-boundary cases; exclude pending Tasks 7–8; do not infer actual user decisions, truthful content, readable model pixels, or natural spoken delivery from synthetic fixtures.

## Readiness assessment

Severity counts: **Critical 0; Important 9; Minor 0.** No scope finding.

**Not ready to merge as a production-ready managed workflow.** The architecture and covered gates are promising, but the sample-repair paths and normal approved-revision path currently deadlock; missing prompts can bypass retry authorization; final output order can diverge from approved sequence; failed/concurrent writes can destroy or lose state; and the retained CLI backend lacks an executable managed-job mapping. Resolve these findings and verify the complete repair/revision/assembly and backend dry-run paths before claiming Tasks 2–6 complete. This is an internal read-only review, not publication authorization.
