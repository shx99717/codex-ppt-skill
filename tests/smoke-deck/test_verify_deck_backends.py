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

    def test_ratio_constants_come_from_shared_helper(self) -> None:
        import sys
        from pathlib import Path

        scripts = Path(__file__).resolve().parents[1] / ".." / "skills" / "codex-ppt" / "scripts"
        scripts = scripts.resolve()
        if str(scripts) not in sys.path:
            sys.path.insert(0, str(scripts))
        import slide_image_ratio

        self.assertIs(self.v.RATIO_BY_LABEL, slide_image_ratio.RATIO_BY_LABEL)
        self.assertEqual(self.v.RATIO_RELATIVE_TOLERANCE, slide_image_ratio.RATIO_RELATIVE_TOLERANCE)


class VerifyDeckMedavisChecksTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.v = _load_verify_deck()

    def test_medavis_checks_skipped_when_file_absent(self) -> None:
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp)
            r = self.v.Report()
            self.v.check_medavis_pptx(deck, r)
            self.assertEqual(r.baseline_failed, 0)
            self.assertTrue(any("not present" in note for note in r.info))

    def test_medavis_checks_pass_on_assembled_deck(self) -> None:
        import sys
        import tempfile
        from pathlib import Path

        from PIL import Image

        scripts = Path(__file__).resolve().parents[1] / ".." / "skills" / "codex-ppt" / "scripts"
        scripts = scripts.resolve()
        if str(scripts) not in sys.path:
            sys.path.insert(0, str(scripts))
        import assemble_ppt

        for stream in (sys.stdout, sys.stderr):
            if hasattr(stream, "reconfigure"):
                stream.reconfigure(encoding="utf-8", errors="replace")

        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp) / "coffee-extraction"
            origin = deck / "origin_image"
            origin.mkdir(parents=True)
            for i in range(1, 4):
                Image.new("RGB", (32, 18), color=(i * 40, 80, 120)).save(origin / f"slide_{i:02d}.png")
            (deck / "speech.md").write_text(
                "## Slide 1: A\n\nNote one.\n\n## Slide 2: B\n\nNote two.\n\n## Slide 3: C\n\nNote three.\n",
                encoding="utf-8",
            )
            ok = assemble_ppt.create_medavis_presentation(
                [str(origin / f"slide_{i:02d}.png") for i in range(1, 4)],
                str(deck / "coffee-extraction-medavis.pptx"),
                "Coffee Extraction",
                assemble_ppt.load_speaker_notes(str(deck)),
                "16:9",
            )
            self.assertTrue(ok)
            r = self.v.Report()
            self.v.check_medavis_pptx(deck, r)
            self.assertEqual(r.baseline_failed, 0, r.baseline)


if __name__ == "__main__":
    unittest.main()
