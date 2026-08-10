#!/usr/bin/env python3
"""Unit tests for smoke-deck backend classification helpers (OpenClaw / T6)."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def _load_verify_deck():
    path = Path(__file__).resolve().parent / "verify_deck.py"
    spec = importlib.util.spec_from_file_location("smoke_verify_deck", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VerifyDeckBackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.v = _load_verify_deck()

    def test_openclaw_family_unknown(self) -> None:
        self.assertEqual(self.v.backend_family("image_generate"), "unknown")
        self.assertEqual(self.v.backend_family("OpenClaw image_generate"), "unknown")

    def test_openclaw_not_specific_for_t6(self) -> None:
        self.assertFalse(self.v.is_specific_backend_label("image_generate"))
        self.assertFalse(self.v.is_specific_backend_label("OpenClaw image_generate"))

    def test_generic_builtin_not_specific_for_t6(self) -> None:
        self.assertFalse(self.v.is_specific_backend_label("built-in image tool"))
        self.assertEqual(self.v.backend_family("built-in image tool"), "builtin-image-gen")

    def test_generateimage_specific(self) -> None:
        self.assertEqual(self.v.backend_family("GenerateImage"), "generateimage")
        self.assertTrue(self.v.is_specific_backend_label("GenerateImage"))

    def test_codex_image_gen_specific(self) -> None:
        self.assertEqual(self.v.backend_family("Codex image_gen"), "builtin-image-gen")
        self.assertTrue(self.v.is_specific_backend_label("Codex image_gen"))
        self.assertTrue(self.v.is_specific_backend_label("image_gen"))

    def test_codex_gpt_image_specific(self) -> None:
        self.assertEqual(self.v.backend_family("codex-gpt-image"), "codex-gpt-image")
        self.assertTrue(self.v.is_specific_backend_label("codex-gpt-image"))

    def test_cli_family(self) -> None:
        self.assertEqual(self.v.backend_family("scripts/image_gen.py"), "cli-api-fallback")
        self.assertTrue(self.v.is_specific_backend_label("scripts/image_gen.py"))


if __name__ == "__main__":
    unittest.main()
