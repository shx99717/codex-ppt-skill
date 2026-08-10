#!/usr/bin/env python3
"""Unit tests for image_gen.py stdout encoding safety."""

from __future__ import annotations

import base64
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import image_gen


def _tiny_png_b64() -> str:
    from PIL import Image

    buf = io.BytesIO()
    Image.new("RGB", (1, 1), color="white").save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode("ascii")


class _FakeProvider:
    def __init__(self, image_b64: str) -> None:
        self._image_b64 = image_b64

    def generate(self, payload: dict) -> list[str]:
        return [self._image_b64]


class GenerateStdoutEncodingTests(unittest.TestCase):
    def test_chinese_out_path_does_not_crash_on_non_cjk_console(self) -> None:
        """`_decode_and_write`/`_decode_write_and_downscale` print(f"Wrote {out_path}")
        with no encoding guard, where out_path comes straight from the caller-supplied
        --out argument -- a deck/output directory name that can be non-ASCII. Must not
        crash a subprocess whose stdout console can't represent CJK text (see the
        matching note in test_slide_job_status.py for why GBK alone wouldn't reproduce
        this: GBK can represent ordinary Chinese text fine, cp1252 genuinely cannot)."""
        image_b64 = _tiny_png_b64()
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "咖啡萃取的三个变量" / "slide_01.png"

            buffer = io.BytesIO()
            cp1252_stdout = io.TextIOWrapper(buffer, encoding="cp1252", errors="strict")
            old_argv, old_stdout = sys.argv, sys.stdout
            old_api_key = os.environ.get("OPENAI_API_KEY")
            old_provider = image_gen.create_image_provider
            try:
                sys.argv = [
                    "image_gen.py",
                    "generate",
                    "--prompt",
                    "test prompt",
                    "--out",
                    str(out_path),
                ]
                sys.stdout = cp1252_stdout
                os.environ["OPENAI_API_KEY"] = "test-key-not-real"
                image_gen.create_image_provider = lambda **_kwargs: _FakeProvider(image_b64)
                exit_code = image_gen.main()
            finally:
                cp1252_stdout.flush()
                sys.stdout = old_stdout
                sys.argv = old_argv
                image_gen.create_image_provider = old_provider
                if old_api_key is None:
                    os.environ.pop("OPENAI_API_KEY", None)
                else:
                    os.environ["OPENAI_API_KEY"] = old_api_key

            self.assertEqual(exit_code, 0)
            self.assertTrue(out_path.exists())

        buffer.seek(0)
        output = buffer.getvalue().decode("utf-8")
        self.assertIn("咖啡萃取的三个变量", output)


if __name__ == "__main__":
    unittest.main()
