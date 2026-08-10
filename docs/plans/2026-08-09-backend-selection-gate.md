# Backend / Image-Model Selection Gate Implementation Plan

> **For the implementing agent:** Follow this plan task-by-task. Complete each step, verify it works, then move to the next.

**Goal:** Replace the rubber-stamp two-backend confirmation with hybrid probe → real menu → deck-wide lock using specific tool labels; widen `_backend_family()` so `GenerateImage` / `codex-gpt-image` do not hard-fail; make smoke-deck TARGET **T6** achievable without breaking BASELINE.

**Architecture:** Prose checklist for *real* host-native tools only (Codex `image_gen`, Cursor `GenerateImage` — **never** invent a Claude Code native image tool). Script `probe_image_backends.py` for bridges/CLI/provider filesystem signals. Agent presents annotated menu (host-native first where it exists; Claude Code prefers `codex-gpt-image` when installed). Lock a specific `selected_backend` + `sample_generation_method`. Align `_backend_family()` with smoke-deck family order.

**Tech Stack:** Python 3 (existing scripts style), Markdown skill docs, unittest.

---

> **SELF-CONTAINED HANDOFF PLAN.** The executor needs no prior chat session or memory file and must not ask the user to re-explain context. All task context lives in this plan (and appendices). Normal session-start rules still apply; start fresh and rely on this document.

## Section 0: Full Context

### 0.1 Why / background

`codex-ppt` today only models two backends in docs: generic “built-in image tool” vs `scripts/image_gen.py`. The confirmation gate is a rubber stamp. Cursor’s `GenerateImage` and sibling skill `codex-gpt-image` are invisible. `_backend_family()` in `record_slide_result.py` only recognizes two families and returns `""` for those labels → recording can `SystemExit("Backend mismatch")`. Goal 1 (user review gate) is already implemented in this fork (uncommitted); do not regress it. This plan is **goal 2 only**.

### 0.2 Confirmed decisions (do not re-litigate)

1. **Host-native first** where a *real* native tool exists (Cursor `GenerateImage`, Codex `image_gen`).
2. **Hybrid probe:** prose for host-native tool presence; script for `codex-gpt-image` skill dirs, CLI/`image_gen.py`, doctor/`.env` hints.
3. **Claude / Claude Code has no native image generation** (fact-checked 2026-08-09 against Anthropic Vision FAQ and Claude Code guides). Do not list a fake native option for Claude Code.
4. **On Claude Code:** prefer `codex-gpt-image` when installed; else CLI/API.
5. **Approach 2:** docs + `probe_image_backends.py` + widen `_backend_family` + explicit `selected_backend` lock (not docs-only; not full provider registry).
6. **Keep mid-deck lock** — subagents may not switch backends.
7. **Specific labels required** for `selected_backend` (feeds T6); forbid locking the generic phrase `"built-in image tool"` as the deck selection.
8. **Drop OpenClaw / `image_generate` as a backend option** in skill backend docs, worker template, and `_backend_family` examples/matching for this gate. Claude Code options remain: `codex-gpt-image` (prefer when installed) else CLI. Do **not** strip OpenClaw from top-level README/install/FAQ in this plan.
9. **Do not commit** unless the user explicitly asks. Prefix `[SQ5GEN-195]` if committing.
10. **Out of scope:** goal 3 multilingual; content-skill boundary; assemble_ppt changes; contact sheet; full `image_providers/` UI catalog; wholesale OpenClaw product-doc purge.

**Rejected:** prose-only probe; script claiming to detect IDE native tools; treating OpenClaw/`image_generate` as a supported image backend (goal-2 drop — keep README/install product mentions elsewhere); inventing a Claude Code native image tool; preferring CLI over `codex-gpt-image` on Claude Code by default.

### 0.3 Audience & assumptions

- Repo: `d:/git/codex-ppt-skill`, branch `feature/SQ5GEN-195-improvement-2026-08-09`.
- Edit `skills/codex-ppt/` only (not `~/.*/skills` installs unless user asks).
- Goal 1 files may already exist in the working tree — leave them intact.
- Smoke-deck: `tests/smoke-deck/verify_deck.py` T6 checks `selected_backend` against `SPECIFIC_BACKEND_TOKENS`.

### 0.4 Conventions

- Match existing `record_*.py` CLI style and JSON stdout.
- ASCII in new code/docs unless editing existing non-ASCII strings.
- YAGNI: no full registry; optional providers only if probe finds config.
- Verify with commands before claiming done.

### 0.5 Reference material

See Appendices A–E.

---

### Task 1: RED — baseline (backend gate missing)

**Files:** Create `docs/plans/evidence/2026-08-09-backend-gate-red.md`

**Step 1:** Confirm current docs still describe only two backends:

```bash
rg -n "built-in image tool|image_generate|GenerateImage|codex-gpt-image|probe_image" skills/codex-ppt/docs/backend-selection.md skills/codex-ppt/prompts/slide-worker.md
```

Expected: old two-backend world; `GenerateImage` / `codex-gpt-image` absent or not in the decision menu; no `probe_image_backends.py`.

**Step 2:** Show `_backend_family` fails new labels:

```bash
cd skills/codex-ppt/scripts
python -c "from record_slide_result import _backend_family as f; print(repr(f('GenerateImage')), repr(f('codex-gpt-image')), repr(f('scripts/image_gen.py')))"
```

Expected today: `''`, `''`, `'cli-api-fallback'` (or similar empty for the first two).

**Step 3:** Write RED evidence with rationalizations to defeat:

- R1: “We’re in Cursor so built-in must be Codex `image_gen` (or leftover OpenClaw `image_generate`).”
- R2: “Claude Code has a built-in image tool.”
- R3: “Confirming ‘use built-in’ is enough; no need to name GenerateImage / codex-gpt-image.”
- R4: “Worker can return `built-in image tool` regardless of what parent locked.”

Stop before editing skill product files.

---

### Task 2: Unit tests for `_backend_family` (fail first)

**Files:** Create `skills/codex-ppt/scripts/tests/test_backend_family.py`

**Cases:**

1. `scripts/image_gen.py` → `cli-api-fallback`
2. `codex-gpt-image` → `codex-gpt-image` (must not fall into builtin via substring `image_gen`)
3. `GenerateImage` → `generateimage`
4. `Codex image_gen` / `built-in image tool` → `builtin-image-gen` (or agreed family name — **use the same strings as smoke-deck `backend_family`**: `builtin-image-gen`, `generateimage`, `codex-gpt-image`, `cli-api-fallback`)
5. `image_generate` / OpenClaw-style → `""` (unsupported; must not map via substring `imagegen` inside normalized `imagegenerate`)
6. `_matched_expected_backend("GenerateImage", ["GenerateImage"])` ok
7. `_matched_expected_backend("codex-gpt-image", ["codex-gpt-image"])` ok
8. Family match: worker `GenerateImage` vs expected `Cursor GenerateImage` if both normalize/family-match per implementation

Run:

```bash
cd skills/codex-ppt/scripts
python -m unittest discover -s tests -p 'test_backend_family.py' -v
```

Expect FAIL until Task 3.

---

### Task 3: Widen `_backend_family` (+ validation message)

**Files:** Modify `skills/codex-ppt/scripts/record_slide_result.py`

**Replace `_backend_family`** with order-safe logic aligned to smoke-deck (Appendix A). Critical: detect `codex-gpt-image` / `codexgptimage` **before** bare `image_gen`.

**Update `_validate_backend` error text** to cite specific examples (`GenerateImage`, `codex-gpt-image`, `scripts/image_gen.py`) instead of only generic built-in.

Optional: if `"generateimage"` lacks substring `"image"` wait — GenerateImage contains “image”. `codex-gpt-image` contains “image”. OK.

Re-run Task 2 tests → PASS.

---

### Task 4: Implement `probe_image_backends.py`

**Files:** Create `skills/codex-ppt/scripts/probe_image_backends.py` (Appendix B)

Behavior:

- Print JSON to stdout (pretty, ensure_ascii=False)
- Check skill dirs for `codex-gpt-image` under `~/.claude/skills`, `~/.cursor/skills`, `~/.codex/skills` (and `CODEX_HOME` if relevant)
- Check `scripts/image_gen.py` exists relative to skill root / this file’s parent
- Optionally call lightweight doctor hints (file exists; do not require network success)
- Include `notes`: Claude Code has no native image tool; host-native must be probed by the agent
- Exit 0 always (empty candidates OK)

**Tests:** `tests/test_probe_image_backends.py` with tempfile home overrides if you add `CODEX_PPT_PROBE_HOME` or pass `--home` for testability. Prefer a `--home` flag for unit tests.

---

### Task 5: Docs + worker template (GREEN prose)

**Files:**

- Rewrite `skills/codex-ppt/docs/backend-selection.md` (Appendix C outline)
- Update `skills/codex-ppt/SKILL.md` overview/backend bullet: run probe; host-native first; Claude Code no native; prefer codex-gpt-image there
- Update `skills/codex-ppt/prompts/slide-worker.md`:
  - `Selected image backend: <exact locked label from parent>`
  - Return `backend_used=<exact locked label>` — **remove** `built-in image tool OR scripts/image_gen.py`
  - tool_name examples include `GenerateImage`, `codex-gpt-image`, `image_gen`, `scripts/image_gen.py` — **not** `image_generate`
- Update `skills/codex-ppt/docs/outline-style-and-sample.md` tool_name examples — drop `image_generate`
- In `skills/codex-ppt/docs/image-model-configuration.md` / runtime comments: do **not** require deleting “OpenClaw as an agent host” product wording; only remove any implication that `image_generate` is a preferred built-in backend for this skill

Defeat R1–R4 with explicit Do-not lines.

Do **not** dump a workflow summary into YAML `description` frontmatter.

**Critical plan-review patches (must land in docs):**

1. **Persistence path (Important):** After the user locks a specific label, write it into `deck_spec.json` *before* `prepare_slide_prompts.py` via `sample_generation_method` (with `backend_used` / `tool_name`) and/or `selected_image_backend`. Prefer also passing `--selected-backend <exact label>` to prepare. `prepare_slide_prompts.py` already copies into `slide_jobs.json` → `selected_backend` / per-job `expected_backend`. No new recorder script required (YAGNI) — but the write point must be explicit so T6 does not depend on hand-editing `slide_jobs.json` after prepare.
2. **Menu filter (Important):** Only offer probe candidates with `available: true`, plus prose-detected host-native tools. Do not list unavailable CLI/bridge as choosable defaults.
3. **No OpenClaw backend (Important):** Remove OpenClaw / `image_generate` from backend-selection examples, preference tables, confirmation copy, and `slide-worker` `tool_name` examples. Do not invent a Claude Code native entry. (README/install OpenClaw product mentions are out of scope.)
4. **Rename / OpenClaw-tool sweep (Important):** After widening `_backend_family`, `rg` for `built-in-image-tool` and update callers. `rg` under `skills/codex-ppt/` for `image_generate` in **tool/backend** contexts and clear those. Leave generic “OpenClaw can load SKILL.md” install/runtime mentions alone (option A).
5. **T6 does not reject OpenClaw (Important):** Normalized `image_generate` → `imagegenerate` still contains T6 token `imagegen`. Smoke-deck T6 alone will not fail an OpenClaw lock. Enforcement = docs ban + family `""` + Task 7 explicit ban of locking `image_generate` / OpenClaw as `selected_backend`. Do not rely on T6 for this drop.

---

### Task 6: VERIFY GREEN + T6 proof

**Files:** Create `docs/plans/evidence/2026-08-09-backend-gate-green.md`

1. Re-run the python `_backend_family` one-liner — non-empty families for GenerateImage / codex-gpt-image
2. Run probe script; paste sample JSON
3. Show a minimal `slide_jobs.json` snippet with `"selected_backend": "GenerateImage"` (or `codex-gpt-image`) and note T6 token match via:

```bash
python -c "import re; n=re.sub(r'[^a-z0-9]+','','GenerateImage'.lower()); print(n, any(t in n for t in ('imagegen','generateimage','codexgptimage')))"
```

4. Confirm `assemble_ppt.py` untouched; goal-1 review scripts still present if they were
5. Map R1–R4 → doc sentences

---

### Task 7: Optional loophole closure

If docs still allow locking `"built-in image tool"` as `selected_backend`, add an explicit ban. If Claude Code native is still implied anywhere, delete that implication. Explicitly ban locking `image_generate` / OpenClaw as the deck backend (T6 will not catch it — see Task 5 item 5).

---

## Verification Summary

- [ ] `probe_image_backends.py` exists and returns JSON
- [ ] `_backend_family` classifies GenerateImage / codex-gpt-image / CLI correctly (order-safe)
- [ ] Unit tests for family (+ probe if added) PASS
- [ ] `backend-selection.md` + SKILL + slide-worker updated; no Claude Code native claim
- [ ] T6-compatible specific `selected_backend` documented and token-check shown
- [ ] RED + GREEN evidence written
- [ ] `assemble_ppt.py` diff empty
- [ ] No commit unless user asked

---

## Appendix A — Target `_backend_family` (align with smoke-deck)

Mirror the spirit of `tests/smoke-deck/verify_deck.py` `backend_family()`:

```python
def _backend_family(value: str) -> str:
    n = re.sub(r"[^a-z0-9]+", "", value.lower())
    if "imagegenpy" in n or "scriptsimagen" in n or "scriptsimagegen" in n:
        return "cli-api-fallback"
    if "codexgptimage" in n:
        return "codex-gpt-image"
    if "generateimage" in n:
        return "generateimage"
    # OpenClaw `image_generate` → "imagegenerate" would otherwise match "imagegen" below.
    # Unsupported backend in this fork gate — do not map to builtin-image-gen.
    if "imagegenerate" in n:
        return ""
    if "imagegen" in n or "builtin" in n or "builtinimage" in n:
        return "builtin-image-gen"
    # legacy free-text
    lowered = value.lower()
    if "cli" in lowered or "api" in lowered or "fallback" in lowered:
        return "cli-api-fallback"
    if "built-in" in lowered or "builtin" in lowered:
        return "builtin-image-gen"
    return ""
```

Tune until Task 2 tests and smoke-deck family names agree. Prefer returning the **same family id strings** smoke-deck uses (`builtin-image-gen` not `built-in-image-tool`) so parent/worker matching stays coherent — update any callers that compared to the old string `built-in-image-tool`.

**Grep** for `built-in-image-tool` after the change and update.

---

## Appendix B — `probe_image_backends.py` sketch

```python
#!/usr/bin/env python3
"""Probe non-host-native image backend signals for codex-ppt (JSON stdout)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", help="Override home directory for skill-dir probes (tests).")
    args = parser.parse_args()
    home = Path(args.home).expanduser() if args.home else Path.home()
    skill_root = Path(__file__).resolve().parent.parent
    candidates = []
    for base in (
        home / ".claude" / "skills" / "codex-gpt-image",
        home / ".cursor" / "skills" / "codex-gpt-image",
        home / ".codex" / "skills" / "codex-gpt-image",
    ):
        if (base / "SKILL.md").is_file() or base.is_dir():
            candidates.append(
                {
                    "id": "codex-gpt-image",
                    "label": "codex-gpt-image",
                    "kind": "bridge-skill",
                    "path": str(base),
                    "available": True,
                    "reference_image": True,
                    "auth": "Codex/ChatGPT OAuth via bridge",
                }
            )
            break
    cli = Path(__file__).resolve().parent / "image_gen.py"
    candidates.append(
        {
            "id": "scripts-image-gen",
            "label": "scripts/image_gen.py",
            "kind": "cli-api-fallback",
            "path": str(cli),
            "available": cli.is_file(),
            "reference_image": True,
            "auth": "OPENAI_API_KEY / .env via codex_ppt_runtime",
        }
    )
    report = {
        "host_native_note": (
            "This script does NOT detect IDE-native tools. Agent must prose-check "
            "Codex image_gen and Cursor GenerateImage. Claude Code has NO native image tool."
        ),
        "preference_hints": {
            "cursor": ["GenerateImage (prose)", "codex-gpt-image", "scripts/image_gen.py"],
            "codex": ["image_gen (prose)", "scripts/image_gen.py"],
            "claude-code": ["codex-gpt-image", "scripts/image_gen.py"],
        },
        "candidates": candidates,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
```

Deduplicate / refine as needed; keep JSON schema stable enough for docs to reference fields.

---

## Appendix C — `backend-selection.md` outline

1. Title + when to read
2. **Fact:** Claude Code has no native image generation (vision only). Claude Code choices: `codex-gpt-image` (prefer when installed) else CLI.
3. **Do not** present OpenClaw / `image_generate` as a backend option (goal-2 drop).
4. Hybrid probe procedure (run script; prose-check natives: Codex `image_gen`, Cursor `GenerateImage` only)
5. Preference order by host (table)
6. Menu requirements (resolution / auth / cost / reference-image); **only `available: true` probe candidates + prose natives**
7. Lock specific `selected_backend`; ban generic locked label
8. **Persistence:** write `sample_generation_method` / `selected_image_backend` on `deck_spec.json` before `prepare_slide_prompts.py`; optionally `--selected-backend`
9. When CLI is allowed
10. Confirmation: present options A/B/C from *available* list + recommendation; wait for user choice
11. Pointers to cli-api-fallback / image-model-configuration

---

## Appendix D — T6 tokens (smoke-deck)

From `tests/smoke-deck/verify_deck.py`:

```python
SPECIFIC_BACKEND_TOKENS = ("imagegen", "generateimage", "codexgptimage")
```

Labels like `GenerateImage`, `codex-gpt-image`, `Codex image_gen` normalize to contain these tokens. Generic `built-in image tool` → `builtinimagetool` does **not** contain them → T6 fails (intentional).

---

## Appendix E — Related paths

| Path | Role |
|------|------|
| `skills/codex-ppt/docs/backend-selection.md` | Primary rewrite |
| `skills/codex-ppt/SKILL.md` | Orchestration pointer |
| `skills/codex-ppt/prompts/slide-worker.md` | Exact label return |
| `skills/codex-ppt/scripts/record_slide_result.py` | `_backend_family` landmine |
| `skills/codex-ppt/scripts/probe_image_backends.py` | NEW |
| `tests/smoke-deck/verify_deck.py` | T6 / family reference |
| Goal 1 files | Do not regress |
