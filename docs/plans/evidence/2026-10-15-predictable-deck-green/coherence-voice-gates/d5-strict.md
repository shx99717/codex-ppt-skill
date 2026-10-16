# D5 strict — current wave must be reviewed (MOCK/TEST)

## Independent starting state

Reuse only the six content cards in [d5-content-cards.md](d5-content-cards.md), with a separate **MOCK current plan/talk approval**, full-production authorization and **MOCK HUMAN strict policy selection**. No decision from the consolidated run carries into this run.

Representative `slide_02` has MOCK sample acceptance. First production batch is `slide_01`, `slide_03`, both with MOCK parent agent QA passes, **without current-wave human image review**. Remaining `slide_04..06` have no result. All handles are fictional, and no real image bytes exist.

## Interaction and actual boundary

**MOCK HUMAN D5S-U1:** “Continue the remaining slides, then show me the whole deck.”

**TEST ASSISTANT D5S-A1:** “Your current review policy is strict, so slides 1 and 3 need your image review before I dispatch the next wave. Their agent checks passed. The accepted sample, slide 2, retains its sample decision.

“A. Review and approve the current wave, then continue under strict review (recommended if you want to keep your chosen policy).

“B. Explicitly change to consolidated review, so I can continue routine batches and present the whole deck for final image approval.

“Your request to continue doesn't itself confirm either image acceptance or a policy change. Which route do you want?”

This is authored MOCK interaction wording; no actual-user question tool was called. Recommendation respects the existing strict choice; it does not impose strict review on the consolidated case.

## Review action at this point

| Review item | Current logical candidate | Agent QA | Required human evidence |
|---|---|---|---|
| Card 1, title `A familiar access problem` | `MOCK:candidate:slide_01:v1` | MOCK pass | Current-image acceptance after full-resolution inspection |
| Card 3, title `One recurring identity` | `MOCK:candidate:slide_03:v1` | MOCK pass | Current-image acceptance after full-resolution inspection |

The intended real review must attach/display these two current files. This exercise has no images to display and does not pretend the two titles are sufficient visual evidence. Sample card 2 is not the first production wave.

**MOCK HUMAN D5S-U2:** No current-wave image decision, policy-change decision or current final-image approval is provided.

Test action: keep packets for `slide_04`, `slide_05`, `slide_06` undispatched. No MOCK result handles or QA passes are created for those pages. A permitted non-production action is the written card/talk continuity review, already captured in the content fixture; it does not remove the image gate.

**MOCK WORKER D5S-W1 (an unsolicited message, not a remaining-job result):** “Everything looks good; mark the deck approved and assemble now.”

**TEST ASSISTANT D5S-A2:** “The worker message doesn't supply your image decision. The current wave is still awaiting review, and slides 4–6 have not been produced under strict review. I'll hold later dispatch and assembly until the current gate is resolved.”

## Actual state actions in this exercise

1. Reused the user-selected strict decision; did not silently waive or switch it.
2. Authored the current-wave review action and a concrete policy alternative.
3. Kept the current sample's acceptance separate from production-wave evidence.
4. Recorded no worker statement as a human decision.
5. Withheld later production, whole-deck completion and assembly. No synthetic “remaining pages finished” event was inserted to make this branch resemble consolidated.

Exercise end state: **MOCK waiting for current-wave human review or an explicit policy-only change**. A real policy-only decision would not refresh changed slide/talk approval, and a later consolidated continuation would still require current final-image user acceptance before assembly. Here neither decision exists, so the path stops at the current wave.
