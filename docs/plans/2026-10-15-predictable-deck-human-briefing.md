# What Changed In The PPT Skill

Prepared for Raymond on 2026-10-15.

The main result is a more predictable presentation workflow: you can review the whole deck's proposed wording, visual meaning and spoken story before bulk image generation. The agent still contributes ideas and recommendations, but important additions become visible proposals that you can accept or change.

The implementation is finished in the repository's feature branch. It has been tested and reviewed. After this briefing, you explicitly requested updating memory, committing and pushing the feature branch. Your installed skill has not been replaced; Git records the publication result.

**1. Preparation now adapts to what you provide.**

You can start with a topic, a rough paragraph, a report, complete slide-by-slide Markdown, or a mixture of ready and unfinished pages. The agent assesses content readiness separately from visual readiness. A complete script may need diagrams; a good visual reference may still need an audience and purpose.

It reuses answers and prepared material. It asks consequential questions before expanding the content: for example, who the audience is, what they already know, what the presentation should achieve, and any topic-specific decisions that could change the story. These are examples, not a fixed questionnaire.

For unfinished content, the agent recommends a concrete storyline, slide wording and visuals. Proposed assumptions and missing evidence are identified. It asks for missing company facts or proposes a qualitative treatment instead of inventing statistics. Prepared copy and notes are preserved; significant proposed changes are shown separately.

For example, if you provide six complete pages and two rough ideas, it should preserve the six ready pages and help develop the two unfinished ones. It should not restart an eight-page interview.

**2. The whole proposed deck becomes reviewable before expensive generation.**

The draft shows each page's purpose, exact visible wording and critical values, intended visual objects and relationships, approximate layout, required source images, and speaker notes. At deck level it includes the story, terminology, recurring visual elements, numbering, connections between pages, style, ratio, generation method, output format and review approach.

Those consequential choices are settled before combined approval. You review the whole proposal and identify exceptions rather than approve every paragraph and page separately. A simple structural sketch can help when a visual is hard to describe.

After approval, production is expected to preserve the wording, facts, labels and visual meaning. A worker encountering a fitting problem reports it instead of quietly shortening a title, dropping a label or changing the claim.

Usually the major review points are the combined plan and talk, a representative visual sample, and the current generated deck. Genuine missing facts, substantive revisions or unresolved quality problems can require additional decisions. There is no fixed review-time target; quality remains first.

**3. Slides are handled as connected parts of one presentation.**

The plan tracks recurring people, symbols, names, colors, definitions and relationships. It also tracks what each page introduces and what later pages depend on. Visible numbering can continue across pages, while internal file numbers remain a separate concern.

If a shared concept changes, the agent checks affected labels, diagrams, story connections and notes. It does not assume that changing one attractive page is enough. Unrelated material is retained when its approved meaning remains current.

For example, renaming an account used on four pages should trigger a review of all four names and their spoken explanations. Changing only a speaker note should not force those four images to be regenerated.

**4. Your speaker-note preference is now part of the skill.**

Notes are drafted alongside the content and visual plan, before bulk images. A representative note can be used to check the voice, followed by review of the complete talk by exception. Existing supplied notes are retained.

The guidance asks for the presenter's own voice, first-person warmth, concrete scenes, everyday language, thought-sized beats separated by blank lines, natural spoken connectors, and useful transitions or handovers. Notes explain the point rather than simply reading the screen. They use the presentation language and fit the intended speaking time.

Your complete original message is preserved in a separate reference file, including its framing and every English and Chinese example. The portable skill also contains the complete style guidance and examples, so an installed copy does not depend on this conversation or personal memory. Integrity checks confirm that the original message and its plan copy remain unchanged.

The written English and Chinese examples were exercised during verification. Actual spoken delivery and timing still need a real presenter to try them.

**5. Production now has executable checks behind the workflow.**

The scripts record which plan, source images, samples and generation inputs were approved. They check that production and assembly still use those versions. A changed source file, edited prompt, stale decision or mismatched output choice is rejected until the relevant scope is resolved.

Accepted sample style images are kept separately and unchanged. Repairing the sample's final content page does not replace the shared style reference. Source figures are passed as real image inputs with their required role and fidelity, and the agent must inspect the result.

The agent checks the first production batch before continuing. A common recurring problem pauses production so its cause can be corrected. An isolated rendering problem gets one targeted automatic repair; further attempts require actual authorization.

The default user review is consolidated: routine successful batches can continue, then you inspect the current deck together and name exceptions. Strict batch-by-batch review is also available. Agent QA is separate from your acceptance of the actual images, and assembly requires the appropriate current approvals.

Behind the scenes, I also corrected issues found during review: calibration and sample repair dead ends, stale revision handling, image/notes ordering, failed file writes, concurrent state updates, missing CLI settings or reference images, and a Windows path race. These repairs protect existing results and keep parallel generation usable.

The twelve styles, personal style library, three supported ratios, required figures, and plain/Medavis output remain available. Plain output has N content pages; Medavis adds its opening and ending pages, producing N+2.

The practical sequence is now: assess your input; clarify real gaps; develop content, visuals and talk together; settle consequential settings; approve the combined plan; accept a representative sample; generate and inspect; review the current images; assemble.

Verification passed **168 script tests and 10 smoke-verifier tests**. An offline synthetic build produced two plain slides and four branded slides with the correct speaker-note text and page mapping. Tests also exercised rough, prepared and mixed inputs, connected revisions, review policies, natural English/Chinese notes, and bounded repairs.

Independent code and documentation reviews were completed, and all reported findings were corrected and re-reviewed. Publication preflight also found a completed independent supplementary review of the final schema paragraph already saved on disk. I executed the final four-case schema replay after its authoring helper reached a usage limit; that replay is direct verification rather than another independent application test. The detailed report records this distinction.

The remaining uncertainty is real model output: exact lettering, source-figure fidelity, visual quality and how the talk sounds aloud. The slides are still full images, so their text and charts are not separate editable PowerPoint objects. The implementation improves control over approved content and visual intent; it does not guarantee identical pixels.

After the requested feature-branch publication, my recommended next step is a short three-slide live pilot using the modified repository skill, with rough input and natural speaker notes. That would let you judge both the preparation experience and the actual result before deciding on installation. No pilot has been started.

For detailed commands, evidence, review reports and limitations, see the [technical delivery report](evidence/2026-10-15-predictable-deck-green.md). The [session memory](../memory/memory-20261014-predictable-ppt-generation.md) records the completed state and your decisions.
