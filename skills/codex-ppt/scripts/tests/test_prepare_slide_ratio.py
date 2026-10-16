#!/usr/bin/env python3
"""Locked-ratio canvas tests for prepare_slide_prompts._build_prompt."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from prepare_slide_prompts import (
    _build_prompt,
    _sample_generation_method,
    _write_template,
    main,
)


def _minimal_spec(**overrides):
    spec = {
        "deck_name": "demo",
        "language": "English",
        "goal": "g",
        "style": {},
        "slides": [{"title": "T", "key_points": ["a"]}],
    }
    spec.update(overrides)
    return spec


class PrepareSlideRatioTests(unittest.TestCase):
    def test_canvas_uses_spec_4_3_not_16_9(self) -> None:
        deck = {"language": "English", "goal": "g", "style": {}, "aspect_ratio": "4:3"}
        slide = {"title": "T", "key_points": ["a"]}
        prompt = _build_prompt(
            deck=deck,
            slide=slide,
            number=1,
            global_style_reference=None,
            base_dir=Path("."),
        )
        self.assertIn("4:3", prompt)
        self.assertNotIn("16:9 full-slide PowerPoint image", prompt)

    def test_locked_4_3_overrides_style_text_16_9(self) -> None:
        deck = {
            "language": "English",
            "goal": "g",
            "aspect_ratio": "4:3",
            "style": {"canvas": "always use aspect_ratio 16:9 in the style JSON"},
        }
        slide = {"title": "T", "key_points": ["a"]}
        prompt = _build_prompt(
            deck=deck,
            slide=slide,
            number=1,
            global_style_reference=None,
            base_dir=Path("."),
        )
        canvas_end = prompt.find("## Deck Goal")
        canvas = prompt[: canvas_end if canvas_end >= 0 else len(prompt)]
        self.assertIn("4:3", canvas)
        self.assertNotIn("16:9 full-slide PowerPoint image", canvas)

    def test_unknown_aspect_ratio_rejected(self) -> None:
        from io import StringIO

        deck = {"language": "English", "goal": "g", "style": {}, "aspect_ratio": "16:10"}
        slide = {"title": "T", "key_points": ["a"]}
        with patch("sys.stderr", new=StringIO()) as err:
            with self.assertRaises(SystemExit):
                _build_prompt(
                    deck=deck,
                    slide=slide,
                    number=1,
                    global_style_reference=None,
                    base_dir=Path("."),
                )
            self.assertIn("aspect_ratio", err.getvalue())

    def test_slide_jobs_persists_aspect_ratio_next_to_backend(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            spec_path = Path(tmp) / "deck_spec.json"
            out_dir = Path(tmp) / "demo"
            spec_path.write_text(
                json.dumps(
                    _minimal_spec(
                        aspect_ratio="16:9",
                        selected_image_backend="GenerateImage",
                    )
                ),
                encoding="utf-8",
            )
            with patch.object(
                sys,
                "argv",
                ["prepare_slide_prompts.py", "--spec", str(spec_path), "--out-dir", str(out_dir), "--legacy-unmanaged"],
            ):
                self.assertEqual(main(), 0)
            jobs = json.loads((out_dir / "slide_jobs.json").read_text(encoding="utf-8"))
            self.assertEqual(jobs["aspect_ratio"], "16:9")
            self.assertEqual(jobs["selected_backend"], "GenerateImage")
            keys = list(jobs.keys())
            self.assertEqual(keys.index("aspect_ratio"), keys.index("selected_backend") + 1)

    def test_generateimage_sample_method_records_ratio_not_gpt_size(self) -> None:
        method = _sample_generation_method(
            {
                "aspect_ratio": "16:9",
                "sample_generation_method": {
                    "backend_used": "GenerateImage",
                    "tool_name": "GenerateImage",
                    "mode": "generate",
                },
            },
            base_dir=Path("."),
        )
        self.assertIsNotNone(method)
        self.assertEqual(method["aspect_ratio"], "16:9")
        size = method.get("size")
        if size is not None:
            self.assertNotIn("API --size", str(size))

    def test_api_sample_method_sets_table_size(self) -> None:
        method = _sample_generation_method(
            {
                "aspect_ratio": "4:3",
                "sample_generation_method": {
                    "backend_used": "scripts/image_gen.py",
                    "tool_name": "scripts/image_gen.py",
                },
            },
            base_dir=Path("."),
        )
        self.assertEqual(method["size"], "API --size 2560x1920")

    def test_write_template_includes_aspect_ratio(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "example.json"
            _write_template(path)
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data.get("aspect_ratio"), "16:9")
            self.assertEqual(data.get("selected_image_backend"), "GenerateImage")
            self.assertEqual(data["workflow_version"], 2)
            self.assertTrue(data["planning"]["unresolved"])
            method = data["planning"]["generation"]
            self.assertEqual(method.get("backend_used"), "GenerateImage")
            self.assertEqual(method.get("aspect_ratio"), "16:9")
            self.assertNotIn("size", method)


if __name__ == "__main__":
    unittest.main()
