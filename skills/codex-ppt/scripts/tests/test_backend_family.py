#!/usr/bin/env python3
"""Unit tests for record_slide_result._backend_family (goal-2 backend gate)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from record_slide_result import (
    _backend_family,
    _matched_expected_backend,
    _validate_backend,
)


class BackendFamilyTests(unittest.TestCase):
    def test_cli_script(self) -> None:
        self.assertEqual(_backend_family("scripts/image_gen.py"), "cli-api-fallback")

    def test_codex_gpt_image_before_image_gen_substring(self) -> None:
        self.assertEqual(_backend_family("codex-gpt-image"), "codex-gpt-image")

    def test_generate_image(self) -> None:
        self.assertEqual(_backend_family("GenerateImage"), "generateimage")

    def test_codex_image_gen_and_generic_builtin(self) -> None:
        self.assertEqual(_backend_family("Codex image_gen"), "builtin-image-gen")
        self.assertEqual(_backend_family("built-in image tool"), "builtin-image-gen")

    def test_openclaw_image_generate_unsupported(self) -> None:
        self.assertEqual(_backend_family("image_generate"), "")
        self.assertEqual(_backend_family("OpenClaw image_generate"), "")

    def test_matched_generate_image(self) -> None:
        self.assertEqual(
            _matched_expected_backend("GenerateImage", ["GenerateImage"]),
            "GenerateImage",
        )

    def test_matched_codex_gpt_image(self) -> None:
        self.assertEqual(
            _matched_expected_backend("codex-gpt-image", ["codex-gpt-image"]),
            "codex-gpt-image",
        )

    def test_family_match_generate_image_variants(self) -> None:
        self.assertEqual(
            _matched_expected_backend("GenerateImage", ["Cursor GenerateImage"]),
            "Cursor GenerateImage",
        )

    def test_specific_builtin_family_match(self) -> None:
        self.assertEqual(
            _matched_expected_backend("image_gen", ["Codex image_gen"]),
            "Codex image_gen",
        )

    def test_generic_builtin_does_not_family_match_specific(self) -> None:
        with self.assertRaises(SystemExit):
            _matched_expected_backend("built-in image tool", ["Codex image_gen"])

    def test_openclaw_mismatches_generate_image(self) -> None:
        with self.assertRaises(SystemExit):
            _matched_expected_backend("image_generate", ["GenerateImage"])

    def test_validate_rejects_openclaw(self) -> None:
        with self.assertRaises(SystemExit):
            _validate_backend("image_generate")

    def test_validate_rejects_generic_builtin(self) -> None:
        with self.assertRaises(SystemExit):
            _validate_backend("built-in image tool")

    def test_validate_accepts_specific_labels(self) -> None:
        self.assertEqual(_validate_backend("GenerateImage"), "GenerateImage")
        self.assertEqual(_validate_backend("image_gen"), "image_gen")
        self.assertEqual(_validate_backend("codex-gpt-image"), "codex-gpt-image")


if __name__ == "__main__":
    unittest.main()
