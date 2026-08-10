# Design-continuation prompt

A copy-paste prompt for resuming the fork-improvement design work in a fresh AI session (Codex,
Claude Code, or Cursor) — no prior conversation needed. It condenses the context a new session
would otherwise have to rebuild from scratch: the three committed goals, what's already known
about the skill's architecture, and what "done" looks like for each goal.

See also [`tests/smoke-deck/RUN_PROMPT.md`](../../tests/smoke-deck/RUN_PROMPT.md) for re-running the
regression test — use that one when you want to *check* a change; use this one when you want to
*design* one.

---

```
You are picking up fork-improvement work on the codex-ppt skill (an image-based PowerPoint
generator: each slide is one full-page AI-generated image, assembled into a .pptx by a local
script). This is a personal fork, currently on branch
feature/SQ5GEN-195-improvement-2026-08-09. The skill's own code/docs (under skills/codex-ppt/)
are still byte-identical to upstream -- nothing has been changed yet. The only fork-specific
addition so far is a test fixture at tests/smoke-deck/ (see below).

Read this whole brief before doing anything. Where it names a specific file or line number,
verify it against the actual current source before relying on it -- this brief may be slightly
stale by the time you read it.

## The three committed goals (design not yet chosen for any of them)

1. Pre-assembly user review gate (top priority). Today the skill has 5 approval gates --
   source reading, outline, visual style, image backend, sample slide -- and ALL of them happen
   before any full-deck image exists. Sample-slide approval is the LAST one; after it, full
   generation runs straight through QA (agent-performed only) and assembly with no user review
   of the final images before the .pptx is built. Design options already on the table: a
   doc-only prose gate vs. a state-enforced one (e.g. a user_reviewed status checked in
   slide_run_state.py, enforced by a check added to assemble_ppt.py -- which today does not
   read slide_jobs.json at all, it just assembles whatever PNGs are in origin_image/). Also
   considered: a contact-sheet script so reviewing 10-12 slides is one glance instead of opening
   each file.

2. Backend / image-model selection gate rework. Today's gate is a rubber-stamp confirmation,
   not a real choice, and its taxonomy only models two backends: "built-in image tool"
   (generic; example names historically included Codex image_gen / OpenClaw image_generate —
   fork goal 2 drops OpenClaw as a backend option) and local CLI/API fallback
   (scripts/image_gen.py). It does not know about Cursor's native GenerateImage tool (confirmed
   backed by Google's Nano Banana Pro / Gemini 3 Pro Image) or about sibling bridge skills like
   codex-gpt-image (confirmed installed at both ~/.claude/skills/codex-gpt-image and
   ~/.cursor/skills/codex-gpt-image on this machine -- but the codex-ppt skill's own docs never
   mention it anywhere). New input: the fork's own CHANGELOG.md shows upstream deprecated a
   "codex-gpt-image pairing tip" in favor of recommending direct gpt-image-2 API/CLI
   configuration -- so don't assume "prefer codex-gpt-image" is even upstream's current intent;
   that's a decision to make deliberately, not inherit. Code landmine to know about:
   _backend_family() in scripts/record_slide_result.py only recognizes two families and
   hard-fails (SystemExit("Backend mismatch")) on label drift. Rough shape discussed so far:
   probe -> present a real menu -> lock the choice for the whole deck. Open question: should
   backend probing be prose-only (same silent-skip failure mode that already hides Cursor's
   GenerateImage today) or script-driven?

3. Multilingual deck support (EN / ZH / mixed). Concrete defects already located:
   scripts/prepare_slide_prompts.py defaults language to "Chinese" when absent, and
   unconditionally injects "Render Chinese text exactly and legibly; avoid garbled characters."
   into every slide's prompt regardless of the deck's actual language. There is no per-slide
   language field today, only a deck-level one.

Explicitly NOT a goal right now: the boundary between this skill and a separate
content-generation skill the user runs upstream of it. That's parked -- the user will revisit
it later when improving that other skill. Do not propose or design against it unless the user
raises it first.

## Background reading (condensed here; full depth in these files on this machine)

- D:\git\squad5-curated-ai-tooling-collection\docs\memory\memory-20260809-codex-ppt-skill.md
  -- full decision history, discoveries, current state
- D:\git\squad5-curated-ai-tooling-collection\docs\memory\memory-20260809-codex-ppt-skill\architecture-notes.md
  -- deep structural analysis (outline generation, visual-consistency mechanism, style system,
  state machine, full gate inventory with file:line references)
- D:\git\squad5-curated-ai-tooling-collection\docs\memory\memory-20260809-codex-ppt-skill\test-design.md
  -- the approved design behind tests/smoke-deck/

Condensed architecture facts, so you're not starting from zero even without reading those files:

- Outline generation is 100% prose-driven: no script anywhere reads or parses the input source.
  outline.md -> deck_spec.json is hand-written by the agent too.
- Visual consistency across slides comes from 3 stacked layers, not a layout engine: (1) the
  style JSON brief copied verbatim into every prompt, (2) the approved sample slide injected as
  a literal input image into every later job -- the strongest lever, (3) a frozen
  sample_generation_method contract that pins the backend/tool/mode. There is no algorithmic
  consistency check anywhere -- QA is manual eyeballing.
- Style selection is phase 3 of 7, a hard gate showing only 2-3 agent-preselected candidates
  (not all 12 built-ins); naming a style up front skips the menu. Styles are documented as pure
  text -- the agent never sees a rendered example; the repo's 12 preview PNGs are human-facing
  only and stripped at install.
- The personal style library (~/.codex-ppt-skill/references/*.md) is also text-only and
  explicitly forbids image dependencies; no script reads that directory, discovery is
  prose-only.
- State machine: slide_run_state.py + record_slide_dispatch.py / record_slide_result.py /
  record_slide_blocker.py. TERMINAL_SLIDE_STATUSES = {"recorded", "accepted", "blocked"}.
- assemble_ppt.py is stateless -- it never reads slide_jobs.json, it just assembles whatever
  slide_XX.png files exist in origin_image/. That's actually helpful: review-after-assembly and
  single-slide regeneration are cheap.

## Verification tooling already exists -- use it as the acceptance test

tests/smoke-deck/ in this repo is a twice-reviewed, fix-verified regression + progress-tracking
test (see tests/smoke-deck/README.md). Several of its TARGET-tier assertions map directly onto
these three goals and are currently failing on purpose:
- T1 (pre-assembly review recorded in run state) -- goal 1
- T2 (English slide prompt free of the hardcoded Chinese-text rule) and T3 (per-slide language
  field present) -- goal 3
- T6 (selected_backend names a specific tool, not a generic phrase) -- goal 2

Turning these from FAIL to PASS, without breaking any BASELINE check, is a concrete, checkable
definition of done for each goal. Re-run it with tests/smoke-deck/RUN_PROMPT.md (a separate
portable prompt) after any change.

## How to work

Nothing under skills/codex-ppt/ has been touched yet -- don't start editing it. Before writing
any code: discuss the approach for whichever goal we're tackling, propose 2-3 options with
tradeoffs where there's a real design choice, and get explicit approval before implementing.
Don't commit anything without being told to -- branch
feature/SQ5GEN-195-improvement-2026-08-09 already exists in this repo for this work; if you end
up committing, use Conventional Commits prefixed with [SQ5GEN-195].

Ask me which of the three goals to focus on first, unless I've already told you in the same
message as this prompt.
```
