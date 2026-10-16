# Final guidance follow-up review — Tasks 7–8

Reviewed: 2026-10-15 (Asia/Shanghai). Branch/task: `feature/SQ5GEN-predictable-deck-generation` / `SQ5GEN-195`.

## Scope and strengths

The correction is coherent with the original finding and approved plan. All three README/design counterparts now settle approval-bound visual/method inputs during draft planning, then obtain combined approval before sample calibration. All three workflow pages state this dependency explicitly. No unrelated change was found in the follow-up scope.

The added worker preparation/dispatch instructions make ownership and attempt authorization clearer. The offline synthetic helper is a reasonable way to reproduce state/assembly evidence: its fixtures, decisions and limitations are labeled as synthetic, and it does not invoke a provider. This review did not expand into another general runtime review.

## Stable finding status

| Finding | Status | Evidence |
|---|---|---|
| **Important-1** — Combined approval previously preceded visual/method locks | **Resolved** | `README.md:212`, `README_en.md:212` and `README_ko.md:212` now draft copy/visuals/talk and settle style, ratio, capable backend/configuration/image operations, representative strategy, output/title and review policy. Their line 213 then approves the complete plan before generating/reusing samples. The same corrected steps appear at `docs/design.md:10`, `docs/en/design.md:10` and `docs/ko/design.md:10`, followed by approval/calibration at line 11. The workflow triplets choose style/method at lines 13–19 and explicitly settle sample/output/review choices before combined approval at `docs/workflow.md:21`, `docs/en/workflow.md:21`, `docs/ko/workflow.md:21`; sample calibration follows at line 25. |

The portable backend requirement (`skills/codex-ppt/docs/backend-selection.md:53`), planning guide, managed gates and published counterparts now agree: draft and lock all consequential inputs → combined approval → representative sample acceptance → production. Searches and semantic reading of the corresponding README/design/workflow, other requested usage pages, portable guides and smoke prompts found no leftover instruction that repeats the original conflicting order.

No new Critical, Important or Minor finding was identified.

## Worker and adapter alignment

- `skills/codex-ppt/docs/slide-generation-and-subagents.md:24` now spawns workers with preparation-only instructions, records the returned real agent ID, then releases the packet for generation. `skills/codex-ppt/prompts/slide-worker.md:9` requires the matching dispatch before calling a backend. This matches the pending-to-dispatched recorder and the adapter's current status/agent check.
- The guide at line 44 and worker packet at line 23 direct bundled CLI work through `run_slide_job.py`, consuming compiled execution rather than replaying nested jobs through `generate-batch`. `generation_execution.py` validates explicit model/size/quality and the approved image-dependent operation policy; the adapter forwards that policy/settings and every verified image.
- The adapter stages prompt/image snapshots under its planning/jobs locks, runs the provider subprocess outside global locks, and revalidates current job/dispatch/input bindings afterward. The candidate remains worker-owned under `candidates/`; final files, repairs, QA and user acceptance remain parent-owned. The new prose matches these boundaries without claiming native tools enforce the CLI adapter's checks automatically.

## Fresh evidence

- Ran `-B -m unittest discover -s skills/codex-ppt/scripts/tests -p test_skill_contract.py -v` with the existing shared interpreter: **3 passed**, exit 0. Portable frontmatter, voice reference digest and local guide links remain valid, including the added adapter link.
- A read-only order check passed for all **six README/design** counterparts and all **three workflow** counterparts. The check was accompanied by semantic reading of the Chinese, English and Korean text.
- Scoped `git diff --check` returned exit 0 for the tracked follow-up guidance corrections.
- Parsed `tests/smoke-deck/run_managed_synthetic.py` with `ast.parse`: passed. Inspection of its imported fixture helpers confirms that PNGs are created with Pillow, approval/QA evidence is `SYNTHETIC TEST`, and the invoked CLIs compile/record/assemble state rather than call an image provider. The helper was **not executed by this reviewer**.
- Independently opened both existing PPTX files described by `tests/smoke-deck/runs/20261015-managed-synthetic-verified/managed-two-slides/TEST-inspection.json`. Their SHA-256 values match the inspection record. Plain contains **2** slides with note offset **0**; Medavis contains **4** slides with content-note offset **1**. Both content notes exactly match the canonical spec/recorded notes and preserve blank-line beats; the branded ending has no content talk. Both final fixture PNGs are **1600×900**. These are physical mapping/fixture checks only.
- The original guidance review report is retained unchanged, SHA-256 `5b60bbd5bf84b087a82bbf380a1a7896c1eb0bdf23eacb852ee0903732706e03`.

## Counts and readiness

| Category | Open findings |
|---|---:|
| Critical | 0 |
| Important | 0 |
| Minor | 0 |

**Tasks 7–8 guidance/localization are ready in the reviewed scope. Important-1 is resolved.** The original report remains the historical record; this follow-up supplies the final status.

Only this follow-up report was written. No implementation, installed skill, existing evidence, live image model/provider, commit/push/PR/merge or publication was changed. The synthetic artifacts and text checks do not demonstrate rendered lettering/figure fidelity, natural spoken performance, timed rehearsal or real human approval, and this report makes none of those claims.

## Supplementary schema-starting guidance check — 2026-10-15

The observed draft/schema RED in `2026-10-15-behavior-schema-red.md` concerns executable field shape, not the approved content/visual design. The added paragraph and command at `skills/codex-ppt/docs/content-planning-and-approval.md:29` are a focused, correct correction: `prepare_slide_prompts.py --write-template INPUT/deck_spec.draft.json` is supported by the parser at `prepare_slide_prompts.py:554` and returns after writing the example at line 571. `_write_template` at line 350 supplies the documented top-level and per-slide keys, with `workflow_version: 2`, no nested `deck` wrapper and unresolved placeholders rather than runtime approvals.

The relationship explanation matches `planning_contract.py:268`: each relationship is an object with nonempty `from`/`to`, and both endpoints must name members of that slide's `visual_plan.objects`. The paragraph preserves supplied content while mapping fields, requires resolving actual blockers before draft-view/approval, and explicitly distinguishes a readable planning card from a runnable JSON candidate. It does not claim the template is already approved or that structural validation proves factual/rendered quality.

A narrow in-memory check captured the **actual template** by mocking only its file writer; it confirmed every documented top-level/slide key, rejected the uncompleted template with `Unresolved approval blockers`, accepted a structural candidate with valid object endpoints, and rejected prose relationships and unknown endpoints. No file, approval, provider call or content revision was created by this check. Reapplication of the four original behavioral cases is separate evidence and was not claimed complete here.

No new guidance finding: open counts remain **0 Critical / 0 Important / 0 Minor**, with **Important-1 resolved**. This addition is consistent with the prior covered guidance readiness. Earlier report sections are preserved; broader Task 9 behavior verification, rendered quality, timing and real human approval remain outside this supplemental check.
