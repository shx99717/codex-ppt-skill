# Cursor bridge managed smoke prompt

Paste the following into the intended host. See [smoke documentation](README.md) for verification limits and [portable prompt](RUN_PROMPT.md) for sibling variants. This is a live test request only when the user invokes it; saving this prompt does not authorize a run.

```text
Use codex-ppt to run the coffee smoke fixture end to end with consolidated image review.

Locate the repository (expected D:/git/codex-ppt-skill); ask only if absent.
Test skills/codex-ppt/SKILL.md and its guides from this repository explicitly, and report the tested root/version.
If using an installed copy instead, verify its source hashes against the intended repository first.
Do not install/synchronize skills, commit, push, merge or release without separate authorization.
Preserve existing edits and historical runs.

Host is cursor; do not switch hosts. Backend is pinned to codex-gpt-image. If unavailable or incompatible, report the blocker before proposing a separately approved fallback. Claude Code has no native image generation.
Ratio is 16:9. Inspect live tool schemas and reference-input support. On a supported gpt-image-2 path use the locked size: 2560x1440, 2560x1920 or 2400x1600. If the native schema cannot express it, report the blocker.
Wrong-ratio images fail; never stretch, crop or letterbox as success.
For a deliberately chosen CLI path, approve explicit model/size/quality and generate/reference-edit operations and use the managed run_slide_job.py adapter with every verified input.

Run python tests/smoke-deck/verify_deck.py --preflight.
Resolve a genuine runtime dependency failure before generating.
Ask for the output base once (suggest tests/smoke-deck/runs/<YYYYMMDD-HHMM>-<host>).

Fixed reusable requirements:
- Source tests/smoke-deck/source.md; deck name coffee-extraction.
- Exactly three content slides: Chinese, English, then mixed Chinese/Latin.
- Built-in 清爽专业风; do not ask for new style options.
- Audience: colleagues learning coffee extraction; purpose: explain the mechanism.
- Draft natural notes in the approved presentation/slide language with breathing beats and meaningful transitions.
- Recommend both plain and Medavis output with landing title Coffee Extraction in the combined plan; confirm or reuse my explicit choice.
- Internal IDs consecutive; visible numbering only if agreed.

Reuse these known decisions. Propose a coherent story, exact visible wording, objects/relationships/composition, shared visual identities, source mapping and complete talk. Mark additions/missing evidence. Review the whole content/visual/talk/output plan by exception before images; do not ask a fixed questionnaire or pad bullets.

Generate an appropriate representative content sample after current plan/talk approval; show actual sample pixels and wait for real acceptance.
Record actual decisions with truthful evidence. Do not pre-approve unseen images or turn agent QA into my approval.
After acceptance and production authorization, compile managed jobs and use one worker per remaining slide when available.
Inspect the first batch, then each slide and the complete ordered deck. Preserve exact approved labels/values/relationships and source fidelity.
Allow one targeted automatic repair for an isolated rendering defect; ask for additional attempts. Pause common first-batch failures.

Use consolidated review: continue routine successful batches after first-batch QA, then show the whole current deck and ask for actual approval or named exceptions.
Substantive changes return to affected-plan approval; unchanged notes-only changes retain valid images.
Assemble only when current managed plan/talk/policy/source/sample/job/result/QA/image-review gates pass. Reuse approved output choices.
Plain has three content slides; Medavis has five with notes only on the corresponding content pages.

Run python tests/smoke-deck/verify_deck.py <base>/coffee-extraction --host cursor --skill-root <tested-skill-root>.
Report full BASELINE/TARGET output, current managed readiness, backend/provenance, actual deck paths, notes mapping and limitations.
The physical verifier is supplemental and cannot establish user acceptance.

On a real defect, reproduce/root-cause first, add regression RED before a script change, apply the smallest fix in the repo, and verify GREEN.
Do not silently patch installed copies or generate unlimited paid retries.
Stop only for genuine missing input/decisions or actual required user reviews; no routine extra confirmations.
```
