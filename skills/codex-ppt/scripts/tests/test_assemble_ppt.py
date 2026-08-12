#!/usr/bin/env python3
"""Unit tests for assemble_ppt stdout/stderr encoding safety and medavis template mode."""

from __future__ import annotations

import io
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import assemble_ppt


def _run_main_with_gbk_stdout(argv: list[str]) -> tuple[int, str]:
    """Run assemble_ppt.main() with sys.argv set to argv and sys.stdout swapped
    for a stream whose *original* encoding is GBK (simulating a Chinese-locale
    Windows console), then return (exit_code, captured_output).

    The fix reconfigures the stream to UTF-8 before printing, so the bytes
    actually written are UTF-8 -- the caller must decode them as UTF-8, not GBK,
    to see the real content. Decoding as GBK would silently produce mojibake
    instead of failing, and an assertion against an ASCII-only substring
    wouldn't notice either way (ASCII bytes round-trip identically under both
    encodings) -- which is exactly the gap this helper exists to avoid.
    """
    buffer = io.BytesIO()
    gbk_stdout = io.TextIOWrapper(buffer, encoding="gbk", errors="strict")
    old_argv, old_stdout = sys.argv, sys.stdout
    try:
        sys.argv = argv
        sys.stdout = gbk_stdout
        with unittest.TestCase().assertRaises(SystemExit) as cm:
            assemble_ppt.main()
        exit_code = cm.exception.code
    finally:
        gbk_stdout.flush()
        sys.stdout = old_stdout
        sys.argv = old_argv
    buffer.seek(0)
    return exit_code, buffer.getvalue().decode("utf-8")


def _run_main(argv: list[str]) -> tuple[int, str]:
    buffer = io.StringIO()
    old_argv, old_stdout = sys.argv, sys.stdout
    try:
        sys.argv = argv
        sys.stdout = buffer
        with unittest.TestCase().assertRaises(SystemExit) as cm:
            assemble_ppt.main()
        exit_code = cm.exception.code
    finally:
        sys.stdout = old_stdout
        sys.argv = old_argv
    return exit_code, buffer.getvalue()


def _make_deck(tmp: str, name: str = "demo-deck", slides: int = 2, with_notes: bool = False) -> Path:
    from PIL import Image

    deck_dir = Path(tmp) / name
    origin = deck_dir / "origin_image"
    origin.mkdir(parents=True)
    for i in range(1, slides + 1):
        Image.new("RGB", (32, 18), color=(i * 40, 80, 120)).save(origin / f"slide_{i:02d}.png")
    if with_notes:
        (deck_dir / "speech.md").write_text(
            "## Slide 1: One\n\nNote for slide one.\n\n## Slide 2: Two\n\nNote for slide two.\n",
            encoding="utf-8",
        )
    return deck_dir


class InitStdoutEncodingTests(unittest.TestCase):
    def test_init_does_not_crash_on_gbk_console(self) -> None:
        """Windows consoles on a Chinese locale default to the GBK code page, which
        cannot encode the U+2713 check mark that --init prints alongside Chinese
        status text. A subprocess with stdout redirected through such a console
        must not crash with UnicodeEncodeError, and the printed status text must
        still be the real Chinese content, not silently-corrupted mojibake."""
        with tempfile.TemporaryDirectory() as tmp:
            exit_code, output = _run_main_with_gbk_stdout(
                ["assemble_ppt.py", tmp, "coffee-extraction.pptx", "--init"]
            )
        self.assertEqual(exit_code, 0)
        self.assertIn("✓ PPT 项目目录已准备好", output)
        self.assertIn("origin_image", output)


class AssembleStdoutEncodingTests(unittest.TestCase):
    def test_full_assembly_does_not_crash_on_gbk_console(self) -> None:
        """The non---init assembly path prints several more Chinese/check-mark
        status lines than --init alone (scan message, per-slide "already added"
        lines, final save summary). Exercise that path for real -- not just
        --init -- under the same simulated GBK console."""
        from PIL import Image

        with tempfile.TemporaryDirectory() as tmp:
            deck_dir = Path(tmp) / "coffee-extraction"
            origin_image_dir = deck_dir / "origin_image"
            origin_image_dir.mkdir(parents=True)
            Image.new("RGB", (16, 9), color="white").save(origin_image_dir / "slide_01.png")

            exit_code, output = _run_main_with_gbk_stdout(
                ["assemble_ppt.py", tmp, "coffee-extraction.pptx"]
            )

            self.assertEqual(exit_code, 0)
            self.assertTrue((deck_dir / "coffee-extraction.pptx").exists())
        self.assertIn("正在扫描", output)  # "正在扫描" (scanning...)
        self.assertIn("已保存", output)  # "已保存" (saved)
        self.assertIn("✓", output)


class MedavisTemplateAssemblyTests(unittest.TestCase):
    def test_none_still_writes_plain_pptx(self) -> None:
        from pptx import Presentation
        from pptx.enum.shapes import MSO_SHAPE_TYPE

        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=2)
            exit_code, _ = _run_main(
                ["assemble_ppt.py", tmp, "demo-deck.pptx", "--template", "none"]
            )
            self.assertEqual(exit_code, 0)
            plain = Path(tmp) / "demo-deck" / "demo-deck.pptx"
            medavis = Path(tmp) / "demo-deck" / "demo-deck-medavis.pptx"
            self.assertTrue(plain.exists())
            self.assertFalse(medavis.exists())
            prs = Presentation(str(plain))
            self.assertEqual(len(prs.slides), 2)
            for idx in range(len(prs.slides)):
                slide = prs.slides[idx]
                pictures = [s for s in slide.shapes if s.shape_type == MSO_SHAPE_TYPE.PICTURE]
                self.assertTrue(pictures)
                pic = pictures[0]
                self.assertEqual(pic.left, 0)
                self.assertEqual(pic.top, 0)
                self.assertEqual(pic.width, prs.slide_width)
                self.assertEqual(pic.height, prs.slide_height)

    def test_medavis_writes_suffix_file_only(self) -> None:
        from pptx import Presentation

        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=2)
            exit_code, _ = _run_main(
                [
                    "assemble_ppt.py",
                    tmp,
                    "demo-deck.pptx",
                    "--template",
                    "medavis",
                    "--landing-title",
                    "Demo Title",
                ]
            )
            self.assertEqual(exit_code, 0)
            plain = Path(tmp) / "demo-deck" / "demo-deck.pptx"
            medavis = Path(tmp) / "demo-deck" / "demo-deck-medavis.pptx"
            self.assertFalse(plain.exists())
            self.assertTrue(medavis.exists())
            prs = Presentation(str(medavis))
            self.assertEqual(len(prs.slides), 3)  # landing + 2 content

    def test_both_writes_plain_and_medavis(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=1)
            exit_code, _ = _run_main(
                [
                    "assemble_ppt.py",
                    tmp,
                    "demo-deck.pptx",
                    "--template",
                    "both",
                    "--landing-title",
                    "Demo Title",
                ]
            )
            self.assertEqual(exit_code, 0)
            self.assertTrue((Path(tmp) / "demo-deck" / "demo-deck.pptx").exists())
            self.assertTrue((Path(tmp) / "demo-deck" / "demo-deck-medavis.pptx").exists())

    def test_medavis_landing_title_and_color(self) -> None:
        from pptx import Presentation

        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=1)
            exit_code, _ = _run_main(
                [
                    "assemble_ppt.py",
                    tmp,
                    "demo-deck.pptx",
                    "--template",
                    "medavis",
                    "--landing-title",
                    "Demo Title",
                ]
            )
            self.assertEqual(exit_code, 0)
            prs = Presentation(str(Path(tmp) / "demo-deck" / "demo-deck-medavis.pptx"))
            landing = prs.slides[0]
            title_shapes = [
                s for s in landing.shapes if s.has_text_frame and "Demo Title" in s.text_frame.text
            ]
            self.assertTrue(title_shapes, "landing title text missing")
            shape = title_shapes[0]
            self.assertEqual(shape.left, assemble_ppt.MEDAVIS_TITLE_LEFT)
            self.assertEqual(shape.top, assemble_ppt.MEDAVIS_TITLE_TOP)
            self.assertEqual(shape.width, assemble_ppt.MEDAVIS_TITLE_WIDTH)
            self.assertEqual(shape.height, assemble_ppt.MEDAVIS_TITLE_HEIGHT)
            color = shape.text_frame.paragraphs[0].font.color.rgb
            self.assertEqual((color[0], color[1], color[2]), assemble_ppt.MEDAVIS_TITLE_COLOR)

    def test_medavis_content_image_placement(self) -> None:
        from pptx import Presentation
        from pptx.enum.shapes import MSO_SHAPE_TYPE

        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=2)
            exit_code, _ = _run_main(
                [
                    "assemble_ppt.py",
                    tmp,
                    "demo-deck.pptx",
                    "--template",
                    "medavis",
                    "--landing-title",
                    "Demo Title",
                ]
            )
            self.assertEqual(exit_code, 0)
            prs = Presentation(str(Path(tmp) / "demo-deck" / "demo-deck-medavis.pptx"))
            for idx in range(1, len(prs.slides)):
                slide = prs.slides[idx]
                pictures = [s for s in slide.shapes if s.shape_type == MSO_SHAPE_TYPE.PICTURE]
                self.assertTrue(pictures)
                pic = pictures[0]
                self.assertGreaterEqual(pic.top, assemble_ppt.MEDAVIS_CONTENT_TOP)
                self.assertGreater(pic.top, assemble_ppt.MEDAVIS_LOGO_BAND_BOTTOM)
                self.assertNotEqual(pic.top, 0)
                self.assertEqual(pic.left, assemble_ppt.MEDAVIS_CONTENT_LEFT)
                self.assertEqual(pic.width, prs.slide_width)
                self.assertEqual(pic.top + pic.height, prs.slide_height)

    def test_medavis_notes_mapping(self) -> None:
        from pptx import Presentation

        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=2, with_notes=True)
            exit_code, _ = _run_main(
                [
                    "assemble_ppt.py",
                    tmp,
                    "demo-deck.pptx",
                    "--template",
                    "medavis",
                    "--landing-title",
                    "Demo Title",
                ]
            )
            self.assertEqual(exit_code, 0)
            prs = Presentation(str(Path(tmp) / "demo-deck" / "demo-deck-medavis.pptx"))
            landing_notes = prs.slides[0].notes_slide.notes_text_frame.text.strip()
            self.assertEqual(landing_notes, "")
            content1 = prs.slides[1].notes_slide.notes_text_frame.text
            self.assertIn("Note for slide one", content1)
            content2 = prs.slides[2].notes_slide.notes_text_frame.text
            self.assertIn("Note for slide two", content2)

    def test_medavis_requires_landing_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=1)
            exit_code, _ = _run_main(
                ["assemble_ppt.py", tmp, "demo-deck.pptx", "--template", "medavis"]
            )
            self.assertNotEqual(exit_code, 0)
            self.assertFalse((Path(tmp) / "demo-deck" / "demo-deck-medavis.pptx").exists())

    def test_both_requires_landing_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=1)
            exit_code, _ = _run_main(
                ["assemble_ppt.py", tmp, "demo-deck.pptx", "--template", "both"]
            )
            self.assertNotEqual(exit_code, 0)
            self.assertFalse((Path(tmp) / "demo-deck" / "demo-deck.pptx").exists())
            self.assertFalse((Path(tmp) / "demo-deck" / "demo-deck-medavis.pptx").exists())

    def test_medavis_ignores_aspect_ratio_4_3(self) -> None:
        from pptx import Presentation

        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=1)
            exit_code, _ = _run_main(
                [
                    "assemble_ppt.py",
                    tmp,
                    "demo-deck.pptx",
                    "--template",
                    "medavis",
                    "--landing-title",
                    "Demo Title",
                    "--aspect-ratio",
                    "4:3",
                ]
            )
            self.assertEqual(exit_code, 0)
            prs = Presentation(str(Path(tmp) / "demo-deck" / "demo-deck-medavis.pptx"))
            self.assertEqual(prs.slide_width, 9144000)
            self.assertEqual(prs.slide_height, 5143500)

    def test_medavis_does_not_mutate_bundled_template(self) -> None:
        template = Path(assemble_ppt.medavis_template_path())
        self.assertTrue(template.exists())
        before_stat = template.stat()
        with tempfile.TemporaryDirectory() as tmp:
            _make_deck(tmp, slides=1)
            exit_code, _ = _run_main(
                [
                    "assemble_ppt.py",
                    tmp,
                    "demo-deck.pptx",
                    "--template",
                    "medavis",
                    "--landing-title",
                    "Demo Title",
                ]
            )
            self.assertEqual(exit_code, 0)
        after_stat = template.stat()
        self.assertEqual(before_stat.st_size, after_stat.st_size)
        self.assertEqual(before_stat.st_mtime_ns, after_stat.st_mtime_ns)


if __name__ == "__main__":
    unittest.main()
