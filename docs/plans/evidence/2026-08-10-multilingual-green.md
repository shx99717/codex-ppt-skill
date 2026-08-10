# GREEN evidence — multilingual deck support (2026-08-10)

## Unit tests (pasted)

```text
test_build_prompt_wires_english_override (test_slide_language.SlideLanguageTests.test_build_prompt_wires_english_override) ... ok
test_deck_chinese_when_no_slide_language (test_slide_language.SlideLanguageTests.test_deck_chinese_when_no_slide_language) ... ok
test_default_english_when_missing (test_slide_language.SlideLanguageTests.test_default_english_when_missing) ... ok
test_mixed (test_slide_language.SlideLanguageTests.test_mixed) ... ok
test_normalization (test_slide_language.SlideLanguageTests.test_normalization) ... ok
test_other_language (test_slide_language.SlideLanguageTests.test_other_language) ... ok
test_slide_english_overrides_deck_chinese (test_slide_language.SlideLanguageTests.test_slide_english_overrides_deck_chinese) ... ok
test_whitespace_and_non_string_fallthrough (test_slide_language.SlideLanguageTests.test_whitespace_and_non_string_fallthrough) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.001s

OK
```

## Full scripts suite (pasted)

```text
----------------------------------------------------------------------
Ran 35 tests in 3.800s

OK
```

## T2-shaped `_build_prompt` (pasted)

```text
T2-shaped check OK
```

## T3

- Outline docs require per-slide `language` for multilingual/mixed decks.
- `slide-generation-and-subagents.md` requires every `deck_spec` slide to include `language` (TARGET T3).
- Prepare template example slides carry `language` fields; deck default is `English`.

## Guards

- `assemble_ppt.py` unmodified
- Hardcoded unconditional Chinese render line removed from Universal Constraints
- Worker QA language-aware
- Template typography no longer Chinese-only

## R1–R3 mapped

| R | Defeat |
|---|--------|
| R1 Chinese default | Default is English when language missing |
| R2 Chinese line on EN | EN/mixed/other get their own constraints; EN has no Chinese rule |
| R3 deck-only language | Slide overrides deck; docs require per-slide language for mixed decks |
