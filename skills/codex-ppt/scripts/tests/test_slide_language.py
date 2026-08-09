#!/usr/bin/env python3
"""Unit tests for slide language helpers in prepare_slide_prompts.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prepare_slide_prompts import (
    _build_prompt,
    _normalize_language_kind,
    _resolve_slide_language,
    _text_quality_constraint,
)


class SlideLanguageTests(unittest.TestCase):
    def test_default_english_when_missing(self) -> None:
        display, kind = _resolve_slide_language({}, {})
        self.assertEqual(display, "English")
        self.assertEqual(kind, "en")
        line = _text_quality_constraint(kind, display)
        self.assertIn("English", line)
        self.assertNotIn("Render Chinese text", line)

    def test_deck_chinese_when_no_slide_language(self) -> None:
        display, kind = _resolve_slide_language({}, {"language": "Chinese"})
        self.assertEqual(display, "Chinese")
        self.assertEqual(kind, "zh")
        self.assertIn("Render Chinese text", _text_quality_constraint(kind, display))

    def test_slide_english_overrides_deck_chinese(self) -> None:
        display, kind = _resolve_slide_language(
            {"language": "English"},
            {"language": "Chinese"},
        )
        self.assertEqual(display, "English")
        self.assertEqual(kind, "en")
        line = _text_quality_constraint(kind, display)
        self.assertNotIn("Render Chinese text", line)

    def test_mixed(self) -> None:
        display, kind = _resolve_slide_language({"language": "mixed"}, {})
        self.assertEqual(kind, "mixed")
        line = _text_quality_constraint(kind, display)
        self.assertIn("CJK", line)
        self.assertIn("Latin", line)
        self.assertNotEqual(
            line.strip(),
            "- Render Chinese text exactly and legibly; avoid garbled characters.",
        )

    def test_other_language(self) -> None:
        display, kind = _resolve_slide_language({"language": "Deutsch"}, {})
        self.assertEqual(display, "Deutsch")
        self.assertEqual(kind, "other")
        line = _text_quality_constraint(kind, display)
        self.assertIn("Deutsch", line)

    def test_normalization(self) -> None:
        self.assertEqual(_normalize_language_kind("zh"), "zh")
        self.assertEqual(_normalize_language_kind("中文"), "zh")
        self.assertEqual(_normalize_language_kind("EN"), "en")
        self.assertEqual(_normalize_language_kind("zh-en"), "mixed")

    def test_whitespace_and_non_string_fallthrough(self) -> None:
        display, kind = _resolve_slide_language({"language": "   "}, {"language": "English"})
        self.assertEqual(display, "English")
        self.assertEqual(kind, "en")
        display2, kind2 = _resolve_slide_language({"language": 123}, {"language": "Chinese"})
        self.assertEqual(display2, "Chinese")
        self.assertEqual(kind2, "zh")
        display3, kind3 = _resolve_slide_language({"language": None}, {})
        self.assertEqual(display3, "English")
        self.assertEqual(kind3, "en")

    def test_build_prompt_wires_english_override(self) -> None:
        deck = {"language": "Chinese", "goal": "g", "style": {}}
        slide = {"title": "EN", "language": "English", "key_points": ["a"]}
        prompt = _build_prompt(
            deck=deck,
            slide=slide,
            number=2,
            global_style_reference=None,
            base_dir=Path("."),
        )
        self.assertNotIn("Render Chinese text", prompt)
        self.assertIn('"language": "English"', prompt)
        self.assertIn("Latin-script", prompt)


if __name__ == "__main__":
    unittest.main()
