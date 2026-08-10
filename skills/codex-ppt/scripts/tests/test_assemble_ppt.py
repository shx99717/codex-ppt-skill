#!/usr/bin/env python3
"""Unit tests for assemble_ppt stdout/stderr encoding safety on non-UTF-8 consoles."""

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


if __name__ == "__main__":
    unittest.main()
