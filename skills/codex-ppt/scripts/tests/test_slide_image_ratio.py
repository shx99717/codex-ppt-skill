#!/usr/bin/env python3
"""Unit tests for slide_image_ratio helpers."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import slide_image_ratio


class SlideImageRatioTests(unittest.TestCase):
    def test_is_16_9_and_named_ratios(self) -> None:
        self.assertTrue(slide_image_ratio.is_16_9(2560, 1440))
        self.assertTrue(slide_image_ratio.is_ratio(32, 24, 4 / 3))
        self.assertTrue(slide_image_ratio.is_ratio(48, 32, 3 / 2))

    def test_mismatch_fixtures_are_outside_tolerance(self) -> None:
        # 1536x1024 is 3:2, not 16:9. 32x18 is exact 16:9 (and therefore not 3:2).
        self.assertFalse(slide_image_ratio.is_16_9(1536, 1024))
        self.assertFalse(slide_image_ratio.is_ratio(1536, 1024, 16 / 9))
        self.assertTrue(slide_image_ratio.is_ratio(32, 18, 16 / 9))
        self.assertFalse(slide_image_ratio.is_ratio(32, 18, 3 / 2))

    def test_require_image_ratio_raises_with_wxh(self) -> None:
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "slide.png"
            Image.new("RGB", (32, 18), color="white").save(path)
            with self.assertRaises(ValueError) as cm:
                slide_image_ratio.require_image_ratio(str(path), 3 / 2, "3:2")
            message = str(cm.exception)
            self.assertIn("32x18", message)
            self.assertIn("3:2", message)

    def test_gpt_image_size_table(self) -> None:
        self.assertEqual(slide_image_ratio.gpt_image_size("16:9"), "2560x1440")
        self.assertEqual(slide_image_ratio.gpt_image_size("4:3"), "2560x1920")
        self.assertEqual(slide_image_ratio.gpt_image_size("3:2"), "2400x1600")

    def test_uniform_picture_box_exact_16_9_fills_slide(self) -> None:
        left, top, width, height = slide_image_ratio.uniform_picture_box(
            2560, 1440, 9144000, 5143500
        )
        self.assertEqual(left, 0)
        self.assertEqual(top, 0)
        self.assertEqual(width, 9144000)
        self.assertEqual(height, 5143500)


if __name__ == "__main__":
    unittest.main()
