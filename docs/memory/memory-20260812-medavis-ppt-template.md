# Memory: Medavis PPT Template Assembly Option

**Generated**: 2026-08-12 15:08 UTC+8
**Last updated**: 2026-08-12 15:50 UTC+8
**Project**: D:/git/codex-ppt-skill
**Focus**: Add optional medavis corporate PPT template wrapping at assembly time

---

## Goal & Scope (required)

Improve `codex-ppt-skill` so PPT assembly offers none / medavis / both, using a bundled medavis 16:9 template (landing + content white-area images + notes).

---

## Key Decisions (required)

1. Bundle medavis template; extend `assemble_ppt.py` with `--template` / `--landing-title`.
2. Outputs: `{deck}.pptx` and/or `{deck}-medavis.pptx`.
3. Placement: `MEDAVIS_CONTENT_TOP=700000`; logo preserved; title `#42637B`.
4. First review I1–M5 all fixed; follow-up review clean (zero new findings).
5. Commit with `[SQ5GEN-195]` Conventional Commits prefix (user confirmed).

---

## Confirmed Assumptions (required)

- Image gen unchanged.
- Do not push unless asked.

---

## Key Discoveries (required)

- Root `*.pptx` gitignore needs `!skills/codex-ppt/assets/templates/*.pptx`.
- Follow-up reviewer: `3f2973b4-6540-4d52-a496-1435cb697333` — I1–M5 FIXED; 12/12 tests OK.

---

## Current State (required)

- **Working**: Feature + review fixes complete; follow-up review clean
- **Pending**: Commit in progress with `[SQ5GEN-195]`
- **Blocked**: none

---

## Next Steps (required)

1. [x] Follow-up code review clean
2. [ ] Commit (then PR only if user asks)
3. [ ] Push only if user asks

---

## References (required)

- `docs/plans/2026-08-12-medavis-ppt-template.md`
- `skills/codex-ppt/scripts/assemble_ppt.py`
- `skills/codex-ppt/assets/templates/medavis_ppt_template_2026_en_16-9.pptx`

---

**Confirmed at**: 2026-08-12
