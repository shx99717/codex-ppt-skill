# Four-Slide Pilot: Copyable Prompt

Paste the text below into a fresh Codex, Claude Code or Cursor session on this computer. This requests a PowerPoint deck, using the feature version installed on 2026-10-15. Creating this prompt does not start a deck run. The topic is deliberately a rough idea so the trial exercises planning as well as rendering; replace the rough paragraph if you prefer another topic.

```text
Use the installed codex-ppt skill to create a four-slide sample PowerPoint deck with speaker notes.

This is a trial of the modified feature version, implementation commit d9f3be7, already installed for Codex, Claude Code and Cursor. Read its SKILL.md and linked planning, speaker-note, backend and approval guides. Confirm which installed root you are using and compare its skill files with D:/git/codex-ppt-skill/skills/codex-ppt. If they differ, explain the mismatch before proceeding. Do not reinstall from main or modify the skill.

Here is my rough input:
"When a teammate takes over a task, useful information can be scattered across chat messages. I want to explain how a short handover can make the next step clearer: what changed, what is blocked, and who does what next. Use one clearly fictional example to make this easy to follow. Finish with something the audience can try in their next handover."

Audience: software engineers and team leads. Purpose: explain a practical approach and encourage trying it. Language: English for slides and notes. Tone: warm, clear and conversational. Output: exactly four total slides in a plain PPTX, with no extra branded opening or ending pages. Prefer 16:9 and a clean professional style. Recommend the specific visual treatment; do not repeat questions already answered here.

Treat the paragraph as rough source material. Propose the storyline, exact on-slide wording, intended visuals and full notes. Identify additions and assumptions; do not invent company facts, statistics, real customer stories or presenter experience. Keep the fictional example explicit. Ask only consequential unanswered questions, with a recommendation.

Make the four slides one connected story. Reuse the same fictional people, symbols, colors and terminology where helpful, with clear transitions. Keep visible wording concise. Write notes as me explaining the point to people in the room: first-person warmth, concrete examples, everyday words, blank lines between thought-sized beats, and natural transitions. Aim for roughly three to four minutes of speaking overall.

Before images, assess actual available backends and ratio/reference-image support. Reuse existing shared configuration; explain the capable choice, any known cost and settings, then get my actual backend choice. If 16:9 is unavailable, recommend a supported alternative and ask. Never silently switch ratio or backend.

Follow the managed workflow: show one combined content/visual/talk plan for review by exception, then wait for my approval. Generate one representative content sample and wait for my acceptance and full-production authorization. The accepted sample should count toward the four final slides when eligible. Use consolidated final image review, with agent QA kept separate from my approval. Preserve approved wording and meaning, check the first production batch, allow one targeted automatic rendering repair, and ask before further attempts or substantive changes. Do not fabricate approval records or bypass gates.

Use a new timestamped folder under D:/git/codex-ppt-skill/tests/smoke-deck/runs/; ask for an alternative only if inaccessible. Deliver the four-slide PPTX, outline.md, speech.md and managed planning/approval artifacts. Verify slide count, ratio, coherent sequence, readable wording and exact note-to-slide mapping before delivery. Report actual paths and any remaining limitations.

Work through the skill to delivery, pausing for genuine missing decisions and the actual plan, sample and final-image reviews. This prompt does not approve unseen content or images. Do not commit, push, merge, reinstall skills or generate a deck in any other location without resolving that choice with me.
```
