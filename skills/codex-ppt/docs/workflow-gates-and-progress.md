# Workflow Gates And Progress

Read before advancing phases or reporting completion. [Content planning](content-planning-and-approval.md) defines adaptive preparation; these are dependencies, not a fixed number of interviews.

## Managed gates

1. Assess content/visual readiness and clarify genuine consequential gaps.
2. Review the complete content/visual plan and drafted talk by exception. Resolve factual blockers, source mappings, style/backend/ratio, sample strategy, output profile/title and review policy.
3. Record actual user approval against the reviewed draft hash. Draft views are allowed earlier; approved canonical content and final views need current scope evidence.
4. Compile explicit sample-phase jobs, generate/reuse compatible representative samples, and record actual sample acceptance.
5. Compile production jobs from current approved contexts and immutable image inputs. Dispatch/result helpers reject stale plans/assets/samples or changed prompt files.
6. Inspect the first production batch before later dispatch; samples alone are not that batch. Pause common failures and correct their shared cause.
7. Apply the chosen human image-review policy and recorded repair limits.
8. Validate complete-sequence/talk QA and current actual image acceptance, then assemble the already approved output profile.

Do not invent approvals, relabel agent QA as a user decision, hand-edit prompts/state, or bypass metadata with a legacy flag. Changes have affected-scope analysis and reapproval; note-only edits retain unchanged images but stale talk/sequence QA.

## Consolidated or strict image review

Recommend consolidated for each new deck and record that actual choice. Agent QA checks every current image and the story/shared-visual/talk sequence. Continue routine subsequent batches after the first-batch check; show the full deck in order, provide full-resolution views for inspection, and let the user approve it or name exceptions. Record one real bulk decision, then review corrections and affected connections. Do not fabricate individual conversations.

Strict policy requires current-wave human image review before later production dispatch. The chosen policy is in the plan; it is not an implicit waiver for an existing run. Both policies still require current actual final-image approval before assembly.

```text
record_slide_qa.py DECK --slide slide_01 --pass --evidence "Actual agent inspection of text/assets/relationships"
record_slide_qa.py DECK --deck-pass --evidence "Actual full story, shared-visual and talk assessment"
record_user_review.py DECK --all --except slide_03 --approve --evidence "Actual whole-deck decision with this exception"
record_user_review.py DECK --slides slide_03 --approve --evidence "Actual correction acceptance"
```

An accepted current sample carries its actual sample evidence; do not invent a second human decision. A named exception clears any previous current-image approval. Bulk selections validate before mutation. New or changed image bytes invalidate QA/review.

## Repair and escalation

A rendering-only issue preserves approved copy, values, objects and relationships. Record needs-repair QA, compile --phase repair, then dispatch. One automatic attempt per affected visual contract is allowed; counters increment at dispatch. More attempts require an actual scoped user authorization with a count. A production/sample phase or raw prompt edit cannot bypass that limit.

```text
record_slide_qa.py DECK --slide slide_03 --needs-repair --evidence "Actual missing required label; preserve its exact wording"
prepare_slide_prompts.py --spec DECK/deck_spec.json --out-dir DECK --phase repair --slides slide_03 --force
record_plan_approval.py DECK --authorize-repair slide_03 --additional-attempts 1 --evidence "Actual extra-attempt authorization"
```

Repeated first-batch failures pause later production. Present the shared cause and recommendation; recalibrate or revise the plan if needed. Group independent unresolved issues where useful. Impatience is not unlimited retry authorization, and a retry limit does not permit delivering unresolved errors.

## Visible progress and evidence

Keep a concise checklist with one active phase: assess/plan/talk; approve plan; calibrate samples; compile/produce; inspect/repair; chosen image review; final sequence/assembly. Avoid displaying technical hashes in human approval cards.

Use actual files and script evidence. slide_job_status reports capacity, dispatch state, stale scopes, QA/review exceptions, actual first-batch IDs and repair counts. It never advances an approval by being queried. Complete delivery needs exact expected images, current plan/talk/sample/policy, SHA-bound agent QA/user evidence, final speech matching the canonical talk, and a verified PPTX. Missing metadata fails closed rather than silently becoming legacy.

Legacy manual/image-only commands require explicit --legacy-unmanaged and refuse managed markers; this is a compatibility route, not a production gate waiver.
