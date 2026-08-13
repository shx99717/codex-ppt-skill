# GenerateImage Schema-vs-Pixels Call Recipe Implementation Plan

> **For the implementing agent:** Follow this plan task-by-task. Complete each step, verify it works, then move to the next.

**Goal:** Stop instructing agents to pass `aspect_ratio="3:2"` to Cursor `GenerateImage` (the live schema rejects it), while keeping GenerateImage 3:2-only in policy and gating on measured pixels.

**Architecture:** Docs/worker/smoke/README-only. Inspect the live tool enum; if `3:2` is missing, pass a schema-legal landscape value (prefer `16:9`) and measure pixels against locked 3:2. Do not add Python helpers. Do not offer GenerateImage for 16:9 or 4:3. Do not stretch.

**Tech Stack:** Markdown skill docs (`SKILL.md`, `docs/backend-selection.md`, `prompts/slide-worker.md`), smoke prompt, zh/en/ko README + Docsify workflow pages, `CHANGELOG.md`.

---

**SELF-CONTAINED:** The executor needs no prior chat session or memory file and must not ask the user to re-explain context. All task context lives in this plan. Normal session-start rules still apply; start fresh and rely on this document.

---

## Section 0: Full Context

### 0.1 Why / background

Cursor `GenerateImage` is the native image tool on Cursor. The skill already hides it unless the deck is locked to **3:2**, because earlier probes showed `aspect_ratio=16:9` still returned **1536×1024 (exact 3:2)**.

On 2026-08-13 (UTC+8 evening) a FAST Cursor smoke run discovered a **new** host-contract break:

1. The live Cursor `GenerateImage` schema enum is `1:1 | 4:3 | 3:4 | 16:9 | 9:16`. Passing `aspect_ratio="3:2"` fails with `Invalid enum value`.
2. Passing `16:9` still returns **1536×1024 (3:2)** — sample slide `coffee-extraction-slide-02.png`.
3. Passing `4:3` (schema-legal) also returns **1536×1024 (3:2)** — dedicated test. Schema accepts 4:3; pixels do not honor it.

The skill still says “pass `aspect_ratio="3:2"`” in `SKILL.md`, `prompts/slide-worker.md`, `docs/backend-selection.md`, and `tests/smoke-deck/RUN_PROMPT_cursor.md`. An agent that follows the skill as written cannot generate the sample. An agent that trusts the schema’s `4:3` enum might offer GenerateImage for a 4:3 deck and silently produce 3:2 pixels.

We cannot make GenerateImage emit 4:3. The fix is the **call recipe**, not the backend menu policy.

### 0.2 Confirmed decisions (do not re-litigate)

1. **Approach A** — docs + worker + Cursor smoke prompt + public README/workflow language sync. No Python helper. No unit tests for a mapping function.
2. **Keep** GenerateImage **only** when locked ratio is 3:2. Never offer it for 16:9 or 4:3.
3. **Do not** omit GenerateImage merely because the schema enum lacks `3:2`. Native pixels are still 3:2 and the Cursor FAST pin depends on this backend.
4. **Do not** try to make GenerateImage emit 4:3.
5. **Call recipe:** prose-check the live enum → if `3:2` present, pass it; if missing, pass schema-legal landscape (`16:9` preferred) → measure pixels → 2% relative vs locked 3:2.
6. A successful `4:3` / `16:9` **argument is not proof** of that ratio.
7. If pixels ≠ locked ratio: **blocker**. Do not assemble, stretch, letterbox, crop, or switch backends unless the user says so.
8. Record the argument actually passed **and** the measured size on `sample_generation_method`, but **not** by overwriting `aspect_ratio`. `prepare_slide_prompts.py` sets `sample_generation_method.aspect_ratio` to the **locked deck** ratio (`3:2`). Put the GenerateImage **tool argument** in `tool_aspect_ratio_argument` (e.g. `"16:9"`) and measured pixels in `measured_size` (e.g. `"1536x1024"`). Extra keys pass through the existing dict copy; do not add Python.
9. Leave frozen history plans alone (`docs/plans/2026-08-13-improve-ppt-ratios.md` still says pass 3:2; do not rewrite it).
10. **Do not commit** unless the user explicitly asks. Prefix if they do: `[SQ5GEN-195]`.
11. Work on existing branch `feature/SQ5GEN-195-improve-ppt-ratios`. Do not create another branch.
12. Do **not** resume the paused FAST smoke (`tests/smoke-deck/runs/20260813-1945-cursor/`) in this plan. After GREEN, the user may start a new smoke; that is out of scope here.
13. Do **not** change `SKILL.md` YAML `name` / `description` (ASO: this is a body-only host-contract update; description already triggers on PPT generation).
14. No version bump. Changelog under `## Unreleased` only.

**Rejected alternatives:**

- **B** — tiny `generateimage_aspect_arg()` helper + unit tests. Extra code for a host quirk that may change again.
- **C** — omit GenerateImage when schema has no `3:2`, force gpt-image-2. Abandons a backend that still produces usable 3:2 pixels and breaks the Cursor FAST pin.

### 0.3 Audience & assumptions

- Executor: a fresh agent in `D:/git/codex-ppt-skill` on branch `feature/SQ5GEN-195-improve-ppt-ratios`.
- Edits land only in the **fork** (`skills/codex-ppt/` plus repo README/docs/CHANGELOG/smoke prompt). Never “fix only” `~/.cursor/skills/codex-ppt`. After skill-doc edits, re-sync install if the user will continue a Cursor run later (optional last step; do not treat install sync as the definition of done).
- Live GenerateImage re-probes are **optional**. Tonight’s pixel evidence is authoritative for this plan (Appendix A). Do not burn image quota unless the schema enum in the current session differs from Appendix A.

### 0.4 Project rules / conventions to honor

- `AGENTS.md`: user-visible docs must update **all language versions in sync** (root README zh/en/ko and Docsify `docs/` / `docs/en/` / `docs/ko/`). Changelog entries in English under `## Unreleased`.
- Contribution: non-trivial changes go through a PR; this plan does **not** open a PR or commit.
- Do not stretch, letterbox, or crop as a success path (already encoded in assemble/record scripts; do not weaken those gates).
- `writing-skills` RED/GREEN/VERIFY applies to this skill-doc change. Pressure scenarios are in Appendix B. Do not skip RED evidence.

### 0.5 Formats & reference material

Canonical call-recipe paragraph (use this wording, or an equivalent that keeps every MUST):

```text
Cursor GenerateImage is 3:2-only in pixels. Offer it only when the locked
ratio is 3:2. It has no gpt-image-2 --size API. Prose-check the live
GenerateImage schema enum. If 3:2 is in the enum, pass aspect_ratio="3:2".
If not, pass a schema-legal landscape value (prefer 16:9) and measure
pixels. Do not pass 3:2 when the schema rejects it. A successful 4:3 or
16:9 argument is not proof of that ratio (2026-08-13: both returned
1536×1024). Gate |(w/h)/1.5 - 1| <= 0.02. If pixels are wrong: blocker.
Do not assemble, stretch, letterbox, crop, or switch backends unless the
user says so. Keep sample_generation_method.aspect_ratio as the locked
deck ratio (3:2). Store the GenerateImage tool argument in
tool_aspect_ratio_argument and pixels in measured_size.
```

---

## Task 1: RED — record baseline (stale instruction + live evidence)

**Files:**

- Create: `docs/plans/evidence/2026-08-13-generateimage-schema-red.md`

**Step 1: Grep the stale must-pass instruction**

From repo root:

```bash
rg -n "pass aspect_ratio=.?3:2|pass \`aspect_ratio=\"3:2\"\`|pass aspect_ratio=3:2" skills/codex-ppt tests/smoke-deck/RUN_PROMPT_cursor.md
```

Expected (baseline RED — these hits **must exist** before you edit):

| Path | What is wrong |
|------|----------------|
| `skills/codex-ppt/SKILL.md` (~line 49) | Hard constraint: pass `aspect_ratio="3:2"` |
| `skills/codex-ppt/prompts/slide-worker.md` (~line 29) | Worker: pass `aspect_ratio="3:2"` |
| `skills/codex-ppt/docs/backend-selection.md` (~line 82) | Example: `pass aspect_ratio=3:2` |
| `tests/smoke-deck/RUN_PROMPT_cursor.md` (~line 108) | FAST pin: Pass `aspect_ratio="3:2"` |

**Step 2: Write the RED evidence file** using Appendix A (do not invent new numbers). Include the grep hits verbatim (path + line). State the agent failure modes from Appendix B as “would-fail without this change”.

**Step 3: Optional Cursor schema check** (only if `GenerateImage` is callable in this session). Read the tool enum. If it still lacks `3:2`, note “schema unchanged”. If `3:2` is now present, **stop** and ask the user — the workaround branch of the recipe is still required as a fallback, but the “do not pass 3:2” hard line would be wrong as a universal must.

**Verification:** `docs/plans/evidence/2026-08-13-generateimage-schema-red.md` exists and quotes the four stale lines plus Appendix A pixel table.

---

## Task 2: GREEN — `SKILL.md` body (not frontmatter)

**Files:**

- Modify: `skills/codex-ppt/SKILL.md` (Overview paragraph that currently says “observed 1536×1024 even with `aspect_ratio=16:9`”; Hard Constraints bullet that currently says “only for 3:2, and pass `aspect_ratio="3:2"`”).

**ASO checks (executable):**

- Do **not** edit YAML `name` or `description`.
- After edit: `name` still hyphen-safe, `description` still third-person “Use when…”, no new workflow summary stuffed into description.

**Step 1: Replace the Overview sentence** (the GenerateImage clause only) with:

```markdown
Cursor `GenerateImage` is 3:2-only in **pixels** (observed 1536×1024 even when the tool argument is `16:9` or `4:3`) — do not offer it for 16:9 or 4:3. The live Cursor schema may omit `3:2` from the enum; follow the Hard Constraints call recipe (inspect enum, pass a legal landscape value if needed, measure pixels).
```

Keep the surrounding sentences about gpt-image-2 / Claude Code / probe script.

**Step 2: Replace the Hard Constraints backend-menu bullet** so GenerateImage is no longer “and pass `aspect_ratio="3:2"`”. Split if needed. Required content:

- GenerateImage **only** for locked 3:2.
- No gpt-image-2 `--size` on GenerateImage.
- Enum check + fallback `16:9` + pixel gate (Section 0.5).
- gpt-image-2 tools still **must** pass `--size` `2560x1440` / `2560x1920` / `2400x1600`.
- Codex `image_gen` schema honor/hide rule unchanged.

**Step 3: Grep this file**

```bash
rg -n "pass \`aspect_ratio=\"3:2\"\`|pass aspect_ratio=\"3:2\"" skills/codex-ppt/SKILL.md
```

Expected: **no matches**. The file may still mention `3:2` as the locked ratio and as an enum value to pass **when present**.

---

## Task 3: GREEN — `docs/backend-selection.md`

**Files:**

- Modify: `skills/codex-ppt/docs/backend-selection.md`

**Step 1: Update the GenerateImage table row** (currently “observed 1536×1024” / “**3:2 only**”) to:

```markdown
| `GenerateImage` | Cursor native image tool (no gpt-image-2 size API; pixels observed 1536×1024 even when argument is `16:9` or `4:3`; schema may lack `3:2`) | **3:2 only** |
```

**Step 2: After “Lock and persist” (or before “Confirmation”), add a short subsection** titled `GenerateImage call recipe` containing the Section 0.5 paragraph (not a Python function). Include red flags:

- Schema lists `4:3` ≠ pixels are 4:3.
- Enum rejects `3:2` ≠ GenerateImage is unavailable for a 3:2 deck.
- Do not switch to CLI just because the enum lacks `3:2`.
- Do not stretch 3:2 pixels onto a 4:3/16:9 canvas.

**Step 3: Replace the Cursor 3:2 confirmation example** (currently `pass aspect_ratio=3:2`) with:

```text
Host: Cursor. Locked ratio: 3:2. Probe + prose check found:
  A) GenerateImage (Cursor native image tool; 3:2 pixels; if schema has no 3:2, pass 16:9 then measure; recommended)
  B) codex-gpt-image (gpt-image-2 via Codex OAuth; pass --size 2400x1600)
  C) scripts/image_gen.py (gpt-image-2 via API key; pass --size 2400x1600)
I recommend A. Which backend should we lock for this deck?
```

Keep the Cursor 16:9 example that **hides** GenerateImage.

**Verification:**

```bash
rg -n "pass aspect_ratio=3:2" skills/codex-ppt/docs/backend-selection.md
```

Expected: no matches.

---

## Task 4: GREEN — `prompts/slide-worker.md`

**Files:**

- Modify: `skills/codex-ppt/prompts/slide-worker.md` (~line 29)

**Step 1: Replace the GenerateImage bullet** with:

```text
- Cursor GenerateImage: only when locked ratio is 3:2. Prompt text is not enough. Inspect the live schema enum. If it includes `3:2`, pass `aspect_ratio="3:2"`. If not, pass `aspect_ratio="16:9"` (or another schema-legal landscape value) and verify the saved file is 3:2 within 2% relative (observed 1536×1024). Do not pass `3:2` when the schema rejects it. `sample_generation_method.aspect_ratio` is the locked deck ratio, not the tool argument — if `tool_aspect_ratio_argument` is set, pass that. If the parent locked 16:9 or 4:3, return a blocker instead of calling GenerateImage. Do not switch to another backend because the enum lacks `3:2`.
```

Keep the gpt-image-2 `--size` bullet and the “if the tool cannot produce the locked ratio, return blocker” bullet.

**Verification:** worker no longer contains a standalone “pass `aspect_ratio="3:2"`” with no enum fallback.

---

## Task 5: GREEN — Cursor FAST smoke prompt

**Files:**

- Modify: `tests/smoke-deck/RUN_PROMPT_cursor.md` (the fenced procedure block, backend gate ~line 104–109)

**Step 1: Replace** `Pass \`aspect_ratio="3:2"\` on GenerateImage` **with:**

```text
Prose-check the live GenerateImage schema. If `3:2` is in the enum, pass
it. If not, pass `aspect_ratio="16:9"` (do not pass `3:2` — the tool
rejects it). Measure the first sample: pixels must be 3:2 within 2%
relative (observed 1536×1024 even for 16:9 and 4:3 arguments). Persist
locked deck `aspect_ratio` as 3:2. On `sample_generation_method`, keep
`aspect_ratio` as the locked 3:2; set `tool_aspect_ratio_argument` to the
value actually passed (often `16:9`) and `measured_size` to e.g. `1536x1024`.
Every final slide
image must still be produced via Cursor `GenerateImage` (same method
for sample + remaining slides). Do not switch to `codex-gpt-image` or
CLI because the enum lacks `3:2`.
```

Do **not** change `RUN_PROMPT_cursor_codex-gpt-image.md` (different backend pin).

**Verification:** `rg "Pass \`aspect_ratio=\"3:2\"\`" tests/smoke-deck/RUN_PROMPT_cursor.md` → no matches.

---

## Task 6: GREEN — public docs language sync

**Files:**

- Modify: `README.md` (~lines 208, 220)
- Modify: `README_en.md` (matching bullets)
- Modify: `README_ko.md` (matching bullets)
- Modify: `docs/workflow.md` (Stage 4 / GenerateImage sentence)
- Modify: `docs/en/workflow.md`
- Modify: `docs/ko/workflow.md`

**Step 1: Splice a clause into the existing GenerateImage sentence.** Do **not** replace the whole tip bullet. The current zh/en/ko README tip is one bullet that also contains the gpt-image-2 `--size` table and the no-stretch sentence — those must remain.

`README.md` currently:

```text
Codex 会员默认会优先使用内置生图工具。Cursor `GenerateImage` 实际为 3:2，不能用于 16:9 / 4:3。需要匹配比例时，请用 gpt-image-2（`codex-gpt-image` / `image_gen.py`）并传入 `--size`：16:9=`2560x1440`，4:3=`2560x1920`，3:2=`2400x1600`。组装时不会拉伸；比例不对会拒绝保存。
```

After (only the GenerateImage sentence changes):

```text
Codex 会员默认会优先使用内置生图工具。Cursor `GenerateImage` 像素实际为 3:2（传入 `16:9` / `4:3` 仍可能得到 1536×1024）；工具枚举可能没有 `3:2`，锁定 3:2 时请检查 schema，必要时改传合法横图参数并量像素。不能用于 16:9 / 4:3 锁定。需要匹配比例时，请用 gpt-image-2（`codex-gpt-image` / `image_gen.py`）并传入 `--size`：16:9=`2560x1440`，4:3=`2560x1920`，3:2=`2400x1600`。组装时不会拉伸；比例不对会拒绝保存。
```

`README_en.md` currently includes “Cursor `GenerateImage` is 3:2 in practice and must not be used for 16:9 / 4:3.” Replace **that sentence only** with:

```text
Cursor `GenerateImage` is 3:2 in **pixels** (a `16:9` or `4:3` argument may still return 1536×1024). The tool enum may omit `3:2`; for a 3:2-locked deck, inspect the schema, pass a legal landscape value if needed, and measure pixels. Do not use it for 16:9 / 4:3 locks.
```

Keep the following gpt-image-2 `--size` / assembly-refuse sentences. Korean `README_ko.md`: same splice, same remainder.

**Step 2:** Mirror the same clause in `docs/workflow.md`, `docs/en/workflow.md`, `docs/ko/workflow.md` Stage 4 (currently “Cursor `GenerateImage` is 3:2-only” / zh/ko equivalents). Headings and surrounding workflow steps stay equivalent across languages.

Skip `docs/en/README.md` / `docs/ko/README.md` unless a grep shows they mention GenerateImage (as of 2026-08-13 they do not).

**Verification:** each language still says (a) hide GenerateImage for 16:9/4:3 locks, (b) schema ≠ pixels, (c) gpt-image-2 `--size` table **unchanged** in the same bullet.

---

## Task 7: CHANGELOG

**Files:**

- Modify: `CHANGELOG.md` under `## Unreleased`

**Step 1: Add under `### Fixes`:**

```markdown
- Cursor `GenerateImage`: do not instruct `aspect_ratio="3:2"` when the live schema rejects it; inspect the enum, pass a legal landscape value if needed, and gate on measured 3:2 pixels (schema `4:3`/`16:9` still returned 1536×1024).
```

**Step 2: Add under `### Documentation`:**

```markdown
- Document GenerateImage schema-vs-pixels (enum may lack `3:2`; 4:3/16:9 arguments are not pixel proof) in skill docs, worker prompt, Cursor smoke prompt, and zh/en/ko README plus usage workflow pages.
```

Keep English. Do not add a `(#N)` PR number until a PR exists.

---

## Task 8: VERIFY GREEN + loophole closure

**Step 1: Repo-wide stale-instruction grep** (must be clean in **live** skill/smoke/README paths; historical `docs/plans/2026-08-13-improve-ppt-ratios.md` may still contain the old line — that is allowed):

```bash
rg -n "pass aspect_ratio=.?3:2|pass \`aspect_ratio=\"3:2\"\`" skills/codex-ppt tests/smoke-deck/RUN_PROMPT_cursor.md README.md README_en.md README_ko.md docs/workflow.md docs/en/workflow.md docs/ko/workflow.md
```

Expected: **zero** hits that order the agent to pass `3:2` with no enum fallback.

**Step 2: Positive greps** (must exist):

```bash
rg -n "schema" skills/codex-ppt/SKILL.md skills/codex-ppt/docs/backend-selection.md skills/codex-ppt/prompts/slide-worker.md
rg -n "1536" skills/codex-ppt/docs/backend-selection.md
rg -n "do not switch" skills/codex-ppt/prompts/slide-worker.md
```

Worker must still say: if parent locked 16:9 or 4:3, return a blocker.

**Step 3: Write GREEN evidence** `docs/plans/evidence/2026-08-13-generateimage-schema-green.md` with:

- Grep results from steps 1–2
- Appendix B pressure scenarios: for each, quote the **new** sentence that blocks the old rationalization (Appendix C)

**Step 4: ASO re-check** — `SKILL.md` frontmatter untouched.

**Step 5: Do not run** collection `Install-to-*.ps1`. Optional: copy `skills/codex-ppt` → `~/.cursor/skills/codex-ppt` excluding `__pycache__` / `*.pyc` if the user will continue a Cursor deck in this clone; hash-compare `SKILL.md` and `prompts/slide-worker.md`. Not required for plan GREEN.

---

## Verification Summary

The plan is done when all of the following are true:

- [ ] RED evidence file exists with the four stale-line quotes and Appendix A pixel table
- [ ] `SKILL.md` Hard Constraints no longer mandate passing `3:2` when the schema rejects it; YAML frontmatter unchanged
- [ ] `backend-selection.md` table + call-recipe subsection + Cursor 3:2 example updated; 16:9 example still hides GenerateImage
- [ ] `slide-worker.md` has enum fallback + pixel gate + no backend switch + still blocks GenerateImage for 16:9/4:3 parent locks
- [ ] `RUN_PROMPT_cursor.md` FAST pin uses the workaround; sibling `codex-gpt-image` prompt untouched
- [ ] zh/en/ko README and workflow pages carry the schema-vs-pixels clause
- [ ] `CHANGELOG.md` Unreleased has Fix + Documentation bullets
- [ ] GREEN grep: no live “must pass 3:2” instruction; GREEN evidence file maps each Appendix B loophole to a counter
- [ ] No new Python helper, no unit tests added for this, no commit, no resume of the paused smoke run
- [ ] Frozen `docs/plans/2026-08-13-improve-ppt-ratios.md` left unchanged

---

## Appendix A — Live evidence (2026-08-13 UTC+8)

| Call | Schema | Pixels | Ratio |
|------|--------|--------|-------|
| `aspect_ratio="3:2"` | **rejected** (`Invalid enum value. Expected '1:1' \| '4:3' \| '3:4' \| '16:9' \| '9:16'`) | — | — |
| `aspect_ratio="16:9"` (sample slide) | accepted | **1536×1024** | exact 3:2 |
| `aspect_ratio="4:3"` (dedicated test) | accepted | **1536×1024** | exact 3:2 |

Sample path (paused smoke, do not delete): `tests/smoke-deck/runs/20260813-1945-cursor/coffee-extraction/origin_image/slide_02.png` (copied from Cursor assets `coffee-extraction-slide-02.png`).

4:3 test path (Cursor project assets, may not be in this git repo): `C:\Users\raymond.shen\.cursor\projects\d-git-todo-list\assets\generateimage-ratio-test-4x3.png`. Do not commit that file unless the user asks. The table above is sufficient evidence.

Locked deck ratio for the Cursor FAST pin remains **3:2**. T5 (≥1920px wide) stays a smoke **target**; 1536px is expected for GenerateImage.

---

## Appendix B — Pressure scenarios (RED expected / GREEN required)

Use these as documentation tests. Do not spawn extra image jobs unless Task 1 optional schema check applies.

**P1 — 3:2 deck, schema lacks `3:2`.** Agent must still lock GenerateImage if that is the pin/user choice, pass a legal landscape value, measure 3:2 pixels. Must **not** abort or switch to `codex-gpt-image` / CLI solely because the enum rejected `3:2`.

Baseline failure: skill says pass `3:2` → tool error → stall or backend switch.

**P2 — 4:3 deck, schema lists `4:3`.** Agent must **not** offer GenerateImage. Must not treat a successful 4:3 argument as 4:3 pixels.

Baseline failure: “the tool supports 4:3 in the schema, so it is valid for a 4:3 lock.”

**P3 — Worker after sample.** Subagent must not pass `3:2` when the schema rejects it. Must not switch backends. Must blocker if parent locked 16:9/4:3.

Baseline failure: worker template line “pass `aspect_ratio="3:2"`” with no fallback.

**P4 — Stretch temptation.** 3:2 pixels on a 4:3 canvas. Agent must refuse assemble, not set picture width and height independently.

Baseline: already gated in scripts; skill text must not re-open it as a workaround for GenerateImage.

---

## Appendix C — Loophole counters (must appear in GREEN docs)

| Rationalization | Counter (must be explicit in skill text) |
|-----------------|------------------------------------------|
| “Schema has 4:3, so GenerateImage can do 4:3.” | Argument ≠ pixels; 2026-08-13 4:3 call was 1536×1024; hide GenerateImage unless locked 3:2. |
| “Enum rejected 3:2, so GenerateImage is unavailable.” | Still native 3:2 pixels; pass legal landscape value and measure. |
| “I’ll omit `aspect_ratio` and put 3:2 only in the prompt.” | Prompt text is not enough; pass a schema-legal aspect_ratio argument. |
| “I’ll switch to CLI because 3:2 was rejected.” | Forbidden unless the user asks; enum miss is not a capability miss. |
| “I’ll stretch 1536×1024 onto the 4:3/16:9 slide box.” | Forbidden; blocker and regenerate with a backend that can produce the locked ratio. |

---

## Appendix D — `writing-skills` checklist for this change

This is an **edit** of an existing skill, not a new skill. Apply:

- RED before GREEN (Task 1 before Tasks 2–7).
- Minimal body change addressing observed failures only.
- ASO: do not alter description; do not put a workflow summary into frontmatter.
- VERIFY with the same pressure scenarios (Task 8 + Appendix B).
- Close loopholes (Appendix C) in worker + backend-selection, not only in SKILL.md.
- Repository: changelog, zh/en/ko docs, no install-script runs, no version bump.

Do not create a new skill file. Do not add `scripts/generateimage_aspect_arg.py`.
