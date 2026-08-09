# Multilingual Deck Support (EN / ZH / Mixed) Implementation Plan

> **For the implementing agent:** Follow this plan task-by-task. Complete each step, verify it works, then move to the next.

**Goal:** Make slide prompt generation language-aware (EN / ZH / mixed) so English slides are not forced through a hardcoded Chinese text-quality rule; support per-slide `language` with deck fallback and default **English**; unlock smoke-deck TARGET **T2** and **T3**.

**Architecture:** Small helpers in `prepare_slide_prompts.py` resolve and normalize language, then inject the matching Universal Constraints line. Update worker/docs that assume Chinese QA for every slide. Unit tests cover EN/ZH/mixed/default. No style-reference rewrite; no deep speech.md overhaul.

**Tech Stack:** Python 3, Markdown skill docs, unittest.

---

> **SELF-CONTAINED HANDOFF PLAN.** The executor needs no prior chat session or memory file and must not ask the user to re-explain context. All task context lives in this plan (and appendices). Normal session-start rules still apply; start fresh and rely on this document.

## Section 0: Full Context

### 0.1 Why / background

`prepare_slide_prompts.py` currently:

1. Uses `deck.get("language", "Chinese")` for every slide’s Canvas block (ignores per-slide language).
2. Always appends: `Render Chinese text exactly and legibly; avoid garbled characters.`

Smoke-deck TARGET **T2** fails while that string appears in the English slide (`slide_02`) prompt. TARGET **T3** expects every `deck_spec` slide to carry a `language` field (docs + agent behavior). Goals 1–2 are already implemented in this fork (uncommitted) — do not regress them. This plan is **goal 3 v1 only**.

### 0.2 Confirmed decisions (do not re-litigate)

1. **Scope = core fix (v1):** language-aware prompt building + per-slide `language` + worker/docs that hardcode Chinese QA. Not a rewrite of the 12 style-reference files. Not a deep speech.md redesign.
2. **Resolve order:** `slide["language"]` if non-empty → else `deck["language"]` → else **`"English"`**.
3. **Normalize** (case-insensitive, strip):
   - `chinese`, `zh`, `zh-cn`, `zh-tw`, `中文` → kind `zh`
   - `english`, `en`, `en-us`, `en-gb` → kind `en`
   - `mixed`, `zh-en`, `en-zh`, `bilingual` → kind `mixed`
   - anything else → kind `other` (still emit the raw label in Canvas)
4. **Text-quality lines** (Universal Constraints bullet):
   - `zh`: `Render Chinese text exactly and legibly; avoid garbled characters.`
   - `en`: `Render English (Latin-script) text exactly and legibly; avoid garbled characters.`
   - `mixed`: `Render both Chinese (CJK) and Latin-script text exactly and legibly; avoid garbled characters.`
   - `other`: `Render text in {display_language} exactly and legibly; avoid garbled characters.`
5. **Canvas.language** uses the **resolved display string** (the chosen slide/deck/default label), not only deck default.
6. **Do not commit** unless the user explicitly asks. Prefix `[SQ5GEN-195]` if committing.
7. **Out of scope:** style `references/*.md` Chinese-centric copy; content-skill boundary; `assemble_ppt.py`; OpenClaw/backend work (already done); requiring explicit language (user chose default English instead).

**Rejected:** keep Chinese as default; require language or fail prepare; Approach B (only strip Chinese rule without normalization); full i18n registry; rewriting all style references in v1.

### 0.3 Audience & assumptions

- Repo: `d:/git/codex-ppt-skill`, branch `feature/SQ5GEN-195-improvement-2026-08-09`.
- Edit skill product under `skills/codex-ppt/` (+ evidence under `docs/plans/evidence/`). Do not sync `~/.*/skills` unless asked.
- Goals 1–2 files may exist uncommitted — leave intact.
- Smoke-deck: `tests/smoke-deck/verify_deck.py` T2 greps `Render Chinese text` in `prompts/slide_02.json`; T3 checks every slide has `language`.

### 0.4 Conventions

- Match existing script style; prefer helpers near `_build_prompt`.
- ASCII in new code/docs unless editing existing non-ASCII.
- TDD: failing tests first for helpers / prompt strings.
- Verify with commands before claiming done.

### 0.5 Reference material

See Appendices A–D.

---

### Task 1: RED — baseline (Chinese hardcoded)

**Files:** Create `docs/plans/evidence/2026-08-10-multilingual-red.md`

**Step 1:** Show the hardcoded line and Chinese default:

```bash
rg -n "Render Chinese text|language.*, \"Chinese\"|deck.get\(\"language\"" skills/codex-ppt/scripts/prepare_slide_prompts.py
rg -n "Chinese text is readable|Render Chinese|language.: .Chinese" skills/codex-ppt/prompts/slide-worker.md skills/codex-ppt/docs/slide-generation-and-subagents.md skills/codex-ppt/docs/outline-style-and-sample.md
```

**Step 2:** Rationalizations to defeat:

- R1: “Default Chinese is fine for all decks.”
- R2: “The Chinese render line is harmless on English slides.”
- R3: “Deck-level language is enough; no per-slide field.”

Stop before product edits.

---

### Task 2: Unit tests (fail first)

**Files:** Create `skills/codex-ppt/scripts/tests/test_slide_language.py`

**Prefer testing the helpers directly** (`_resolve_slide_language`, `_normalize_language_kind`, `_text_quality_constraint`). Use `_build_prompt` only as a light integration check in Task 5 — full `_build_prompt` pulls image helpers and is a heavier fixture.

**Required cases:**

1. No language on slide/deck → display `"English"`, kind `en`; `_text_quality_constraint` is English line; does **not** contain `Render Chinese text`
2. Deck `Chinese`, no slide language → kind `zh`; Chinese constraint present
3. Slide `English` overrides deck `Chinese` → kind `en`; no Chinese rule
4. Slide `mixed` → kind `mixed`; mixed constraint (not Chinese-only)
5. Slide `Deutsch` / unknown → kind `other`; generic line mentions `Deutsch`
6. Normalization: `zh`, `中文`, `EN` map correctly (keep the `中文` exact-match **before** alnum stripping — CJK is stripped by `[^a-z0-9]` and would otherwise become empty)

Run:

```bash
cd skills/codex-ppt/scripts
python -m unittest discover -s tests -p 'test_slide_language.py' -v
```

Expect FAIL until Task 3.

---

### Task 3: Implement helpers + wire `_build_prompt`

**Files:** Modify `skills/codex-ppt/scripts/prepare_slide_prompts.py`

Add helpers (Appendix A). In `_build_prompt`:

- `display_lang, kind = _resolve_slide_language(slide, deck)`
- Canvas `"language": display_lang`
- Universal Constraints: use `_text_quality_constraint(kind, display_lang)` instead of the hardcoded Chinese line

Also update `_write_template` default `"language": "English"` and add `"language"` on each example slide (e.g. one Chinese, one English) so the template teaches T3.

Re-run Task 2 tests → PASS.

---

### Task 4: Docs + worker (GREEN prose)

**Files:**

- `skills/codex-ppt/prompts/slide-worker.md` — replace unconditional `Chinese text is readable and not garbled` with language-aware QA (e.g. “text in the slide’s locked language is readable and not garbled; for mixed slides, both CJK and Latin”).
- `skills/codex-ppt/docs/slide-generation-and-subagents.md`:
  - Example JSON: show **per-slide** `language` (or clear deck + slide examples); do not leave a single canvas `"language": "Chinese"` as the only pattern.
  - Change example `text_quality` so it is not Chinese-only for every deck.
  - Change the closing “For Chinese decks…” into language-conditional guidance.
  - **T3 prose:** state that for multilingual/mixed decks every slide in `deck_spec.json` must include a `language` field (Chinese / English / mixed / …) — smoke TARGET T3.
- `skills/codex-ppt/docs/outline-style-and-sample.md` — when drafting the outline/`deck_spec`, require per-slide language for mixed decks; sample confirmation asks for “text quality for the slide language” instead of always “Chinese text quality”.
- `SKILL.md`: only touch if it still implies Chinese-only prompts (grep may show none — skip if clean). Do not dump workflow into YAML description.

Defeat R1–R3 with explicit Do-not lines where useful.

---

### Task 5: VERIFY GREEN + T2/T3 proof

**Files:** Create `docs/plans/evidence/2026-08-10-multilingual-green.md`

1. Re-run unit tests (Task 2) — PASS
2. Synthetic prompt check:

```bash
cd skills/codex-ppt/scripts
python - <<'PY'
from prepare_slide_prompts import _build_prompt
deck = {"language": "Chinese", "goal": "g", "style": {}}
slide_en = {"title": "EN", "language": "English", "key_points": ["a"]}
p = _build_prompt(deck=deck, slide=slide_en, number=2, global_style_reference=None, base_dir=__import__('pathlib').Path('.'))
assert "Render Chinese text" not in p
assert "English" in p or "Latin" in p
print("T2-shaped check OK")
PY
```

3. Note T3: docs + template require per-slide `language`; agent must write it into `deck_spec.json` (smoke T3).
4. Confirm `assemble_ppt.py` untouched; goal 1/2 tests still pass:

```bash
python -m unittest discover -s skills/codex-ppt/scripts/tests -p 'test_*.py' -v
```

5. Map R1–R3 → doc/code sentences

---

### Task 6: Optional loophole closure

If any skill doc under `skills/codex-ppt/docs/` or `prompts/` still says to always inject the Chinese render line, fix it. Do **not** rewrite `references/*.md` style packs in this plan.

---

## Verification Summary

- [ ] Helpers resolve slide → deck → English default
- [ ] EN prompt has no `Render Chinese text` line (T2-shaped)
- [ ] ZH / mixed / other constraints correct
- [ ] Template + docs teach per-slide `language` (T3)
- [ ] Worker QA language-aware
- [ ] Unit tests PASS; full `scripts/tests` still PASS
- [ ] RED + GREEN evidence written
- [ ] `assemble_ppt.py` diff empty
- [ ] No commit unless user asked

---

## Appendix A — Helper sketches

```python
def _resolve_slide_language(slide: Dict[str, Any], deck: Dict[str, Any]) -> tuple[str, str]:
    raw = slide.get("language")
    if not (isinstance(raw, str) and raw.strip()):
        raw = deck.get("language")
    if not (isinstance(raw, str) and raw.strip()):
        raw = "English"
    display = raw.strip()
    return display, _normalize_language_kind(display)


def _normalize_language_kind(value: str) -> str:
    stripped = value.strip()
    n = re.sub(r"[^a-z0-9]+", "", stripped.lower())
    # Exact CJK label BEFORE alnum fold — `中文`.lower() stays CJK and would be stripped to "".
    if stripped in {"中文"} or n in {"chinese", "zh", "zhcn", "zhtw"}:
        return "zh"
    if n in {"english", "en", "enus", "engb"}:
        return "en"
    if n in {"mixed", "zhen", "enzh", "bilingual"}:
        return "mixed"
    return "other"


def _text_quality_constraint(kind: str, display: str) -> str:
    if kind == "zh":
        return "- Render Chinese text exactly and legibly; avoid garbled characters.\n"
    if kind == "en":
        return "- Render English (Latin-script) text exactly and legibly; avoid garbled characters.\n"
    if kind == "mixed":
        return (
            "- Render both Chinese (CJK) and Latin-script text exactly and legibly; "
            "avoid garbled characters.\n"
        )
    return f"- Render text in {display} exactly and legibly; avoid garbled characters.\n"
```

Wire into Universal Constraints:

```python
display_lang, lang_kind = _resolve_slide_language(slide, deck)
# Canvas language = display_lang
# Constraints include _text_quality_constraint(lang_kind, display_lang)
```

Import `re` if not already imported in the module (`prepare_slide_prompts.py` already imports `re` today).

---

## Appendix B — Smoke-deck acceptance mapping

| Target | Meaning | This plan |
|--------|---------|-----------|
| T2 | English `slide_02` prompt free of `Render Chinese text` | Helpers + EN constraint |
| T3 | Every `deck_spec` slide has `language` | Docs + template; agent must populate (prose) |

BASELINE already checks mixed-language *content* ratios in deck_spec when languages are set — do not weaken that.

---

## Appendix C — Files to touch

| Path | Role |
|------|------|
| `skills/codex-ppt/scripts/prepare_slide_prompts.py` | Core fix |
| `skills/codex-ppt/scripts/tests/test_slide_language.py` | NEW tests |
| `skills/codex-ppt/prompts/slide-worker.md` | QA wording |
| `skills/codex-ppt/docs/slide-generation-and-subagents.md` | Examples + guidance |
| `skills/codex-ppt/docs/outline-style-and-sample.md` | Sample confirmation wording |
| `docs/plans/evidence/2026-08-10-multilingual-{red,green}.md` | Evidence |

Do not touch: `assemble_ppt.py`, `references/*.md`, goal-1/2 scripts unless a test import breaks (fix carefully).

---

## Appendix D — Related goals (do not regress)

- Goal 1: `record_user_review.py`, wave review docs
- Goal 2: `probe_image_backends.py`, `_backend_family`, backend-selection docs
