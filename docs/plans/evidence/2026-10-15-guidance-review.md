# Final guidance and localization review — Tasks 7–8

Reviewed: 2026-10-15 (Asia/Shanghai). Branch/task: `feature/SQ5GEN-predictable-deck-generation` / `SQ5GEN-195`.

## Scope verification

The reviewed changeset is coherent with the approved purpose. The portable entry/guides, worker prompt, three README languages, six documentation triplets, English Unreleased changelog and smoke Markdown prompts describe adaptive content/visual/talk planning and managed production. The CLI adapter guidance is a justified addition that explains the executable path needed to preserve approved settings and actual image inputs. No unrelated change or missing planned documentation file was found in this scope.

The requirements were Section 0.2 and Tasks 7–8 of `docs/plans/2026-10-14-predictable-deck-generation-handoff.md`. The complete archived speaker message was read from `docs/memory/memory-20261014-predictable-ppt-generation/speaker-notes-style-reference.md`. Runtime Tasks 2–6 were already independently cleared; scripts were read here only to verify the guidance's commands, operation policy and approval prerequisites.

Finding IDs below are local to this guidance report, separate from the managed-core review's Important-1 through Important-10.

## What is implemented well

- The entry is concise and phase-linked. Its frontmatter exactly matches the approved trigger-only contract: only `name` and `description`, valid `codex-ppt` name and 148-character discovery description. Portable links stay within the distributable skill; the installed workflow does not require repository memory or personal planning skills.
- The planning guide distinguishes content and visual readiness, preserves prepared copy/notes, handles topic-only and mixed inputs, asks consequential questions before expansion, labels proposals and missing evidence, and makes the deck's story/shared identities/terminology/dependencies the planning unit. Exact visible copy, critical values, object relationships, multilingual language and intended numbering are explicit.
- Notes are drafted and approved before expensive images, with representative calibration when useful and complete-talk exception review. The portable voice excerpt retains every guidance paragraph and English/Chinese example verbatim. It preserves first-person warmth, concrete scenes, everyday vocabulary, breathing beats and transitions, and keeps example names/topics separate from future deck facts.
- Output profile/title and review policy are early plan decisions. Consolidated and strict review are distinguished, QA remains separate from actual current-image acceptance, the first production batch must be inspected, and one automatic rendering repair is followed by scoped authorization for further attempts. Fit problems return to the parent instead of authorizing a worker rewrite.
- Source snapshots and accepted sample style bytes are immutable. The guides distinguish style-only reuse from an accepted final page, preserve original-source drift checks, and describe impact-aware visual/talk reapproval. Explicit legacy flags cannot bypass managed markers.
- Backend instructions inspect actual schemas/input support and measure saved pixels. CLI guidance requires approved model/size/quality and an explicit input-dependent operation policy, directs managed execution through `run_slide_job.py`, and forbids text-only batch replay. The script's preflight stages verified byte-identical images under global locks, provider generation runs outside those locks, and postflight revalidates current inputs/attempts. No discrepancy was found between these claims and `generation_execution.py` / `run_slide_job.py`.
- Chinese, English and Korean changes have semantic parity across the requested triplets. They retain twelve styles, ratios, personal-library precedence, raster/editability limits, plain N / branded N+2 counts and content-note offsets. Smoke prompts require real plan/sample/image decisions and explicitly distinguish offline synthetic evidence from live model quality and human acceptance.

## Findings

### Important-1 — Published workflow approves before selecting approval-bound visual/method inputs

**File:line:** `README_en.md:212` and `README_en.md:213`; corresponding `README.md:212`, `README_ko.md:212`; `docs/en/design.md:10` and `docs/en/design.md:11`, with `docs/design.md:10`, `docs/ko/design.md:10`; `docs/en/workflow.md:13` followed by `docs/en/workflow.md:15`, with `docs/workflow.md:13`, `docs/ko/workflow.md:13`.

**What's wrong:** The numbered README/design flows approve the combined plan/talk at step 2, then select style and lock ratio/backend/settings/image-input operations at step 3. The workflow triplets likewise place combined approval before the following section chooses these inputs. This conflicts with the portable planning/backend contract: `skills/codex-ppt/docs/backend-selection.md:53` explicitly requires the backend, ratio and complete generation method **before** combined plan approval. The published ordering is synchronized across languages, so parity alone does not catch it.

**Why it matters:** These are approved visual inputs, not post-approval administrative choices. Managed validation requires a nonempty style, supported ratio, selected backend and generation method (`planning_contract.py:211`–`235`), and its common visual context includes the style/spec plus generation configuration (`planning_contract.py:105`–`109`). Following the published order either leaves the first approval candidate incomplete or changes the approved visual context immediately afterward, creating a stale approval and unnecessary second review before sampling. This defeats the promised one combined review and conflicts with Section 0.2's approved-input production rule.

**How to fix:** Move style/ratio/capability/configuration and representative-sample strategy selection into draft planning, before combined approval. Then generate/reuse and accept the sample. For example: assess input → draft copy/visuals/talk **and lock style/ratio/backend/input operations/output/review/sample strategy** → approve combined plan/talk → calibrate samples → production. Update the same flow in all README/design/workflow counterparts; no runtime change is needed.

No Critical or Minor findings were identified. Other older overview/FAQ wording was checked for the specifically prohibited late-note, assembly-time-template and unconditional wave-review instructions; no additional substantive conflict was found in this review scope.

## Verification evidence

- Ran the existing shared interpreter with `-B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_skill_contract.py -v`: **3 tests passed**, exit 0. These cover entry frontmatter, portable reference digest and distributable local links.
- Independently extracted the portable `BEGIN VOICE REFERENCE` body and compared it directly with the `Speaker notes style` guidance through its last Chinese example in the **full archived original message**: exact equality after stripping outer separator whitespace. SHA-256: `f50bce332df057b51ad6da7ba9251369ea0534c61c4bc64e44193465b2b04dde`. The original introduction/conclusion remain in the archived source; the portable excerpt contains the complete requested guidance/examples.
- Checked **165 local Markdown link paths** across portable entry/guides/prompts and changed public/smoke documents: no missing path, and no portable link escapes the skill root. Docsify `/en/...` and `/ko/...` routes were resolved relative to `docs/`. This checks file destinations, not remote URLs or fragment anchor rendering.
- Ran scoped `git diff --check`: exit 0, no whitespace errors reported.
- Read adapter policy/arguments and staging/lock/revalidation boundaries against documentation. Existing managed-core verification remains the authority for broader runtime readiness; its suite was not redundantly re-reviewed here.

## Counts and readiness

| Category | Open findings |
|---|---:|
| Critical | 0 |
| Important | 1 |
| Minor | 0 |

Tasks 7–8 are substantially aligned with the plan. Correct the single published ordering issue before declaring the guidance/localization task complete. The correction is a routine documentation alignment within the approved scope and requires no new user design decision. The portable skill, voice reference, links and executable CLI guidance passed this review's covered checks.

## Limits

This was a read-only content review with only this report artifact written. No installed skills, live/native image tools, provider APIs, commit/push/PR/merge/release actions or implementation files were changed. Text rules, unit fixtures, hashes and physical file checks do not establish rendered lettering/figure fidelity, actual natural spoken delivery, timed rehearsal or real human approval. Those limitations are described honestly in the portable reporting and smoke documentation; this review does not introduce a hypothetical live-quality approval gate.
