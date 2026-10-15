# D2 actual text-only interaction path

Every user acceptance below is SCRIPTED MOCK/TEST, not a real approval.

## Supplied fixed material

Audience/purpose: “Internal technical discussion; decide what to investigate next.” English. The user asks for clean diagrams and fixes the copy and notes.

Slide 1 title: “Access today”. Body: “Separate accounts”. Notes exactly: “Hi everyone.\n\nLet me start with the access problem.”

Slide 2 title: “A shared account”. Body: “One account across providers”. Notes exactly: “Now, here is the proposal.\n\nThe same account connects these providers.”

Slide 3 title: “What we need to decide”. Body: “Ownership and rollout”. Notes exactly: “So, those are the two decisions.\n\nWhat questions do you have?”

The \n markers above describe literal note newlines. The JSON strings and speech.draft.md contain the actual newlines.

ASSISTANT: “Your three titles, body lines and note paragraphs are already ready. I will retain them exactly. The remaining work is visual: separate account/provider pairs on slide 1, one shared account connected to the same providers on slide 2, and ownership plus staged-rollout concepts on slide 3. The three provider tiles are illustrative, not a claimed provider count. I recommend simple white-background diagrams, blue account symbols and teal provider tiles, using only your supplied words as visible text. Does that visual meaning fit?”

MOCK/TEST USER: “Yes, use those visual connections and keep every supplied word and note unchanged.”

ASSISTANT: “I recommend 16:9. Shall we use it?”

MOCK/TEST USER: “Yes.”

ASSISTANT: “The only available backend in the MOCK/TEST fixture is codex-gpt-image, gpt-image-2 via Codex OAuth at 2560×1440, with reference-image inputs. Native image_gen lacks an explicit size parameter here; no live probe or generation occurred. Shall I lock this fixture backend?”

MOCK/TEST USER: “Yes, for this test.”

ASSISTANT: “I recommend plain output, no visible numbering and consolidated review. Slide 2 is the representative sample because it tests the shared account and provider relationships. Please review the whole visual plan by exception alongside the exact supplied copy and talk. Approve these visual/default choices, or name changes?”

MOCK/TEST USER: “For this test, approve that whole visual plan, sample strategy, plain output and consolidated review. The supplied talk remains fixed.”

ASSISTANT ACTION: Produced the three-page draft and the exact supplied talk. No audience re-interview, new style menu, note rewrite or per-page approval conversation. Exact notes are separately retained in supplied_notes.json and checked against the draft. Real sample generation and image acceptance are still pending; no approval ledger or managed job was manufactured.
