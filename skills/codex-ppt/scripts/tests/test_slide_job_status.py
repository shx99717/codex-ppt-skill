#!/usr/bin/env python3
"""Unit tests for slide_job_status.py stdout encoding safety."""

from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import slide_job_status


class DeckDirEncodingTests(unittest.TestCase):
    def test_chinese_deck_path_does_not_crash_on_non_cjk_console(self) -> None:
        """deck_dir is a caller-supplied path resolved with Path.resolve() and
        printed verbatim (print(f"deck_dir={...}")). A Chinese-named deck
        folder must not crash a subprocess whose stdout console can't
        represent CJK text.

        Note: GBK (the code page a Chinese-locale Windows console actually
        uses) can represent ordinary Chinese text fine -- it's the encoding
        Windows uses *for* Chinese, so a ✓-free Chinese path alone doesn't
        reproduce a crash there (verified: encoding this path as GBK
        succeeds). cp1252 (a common non-Chinese-locale Windows default) is
        used here instead because it genuinely cannot encode CJK at all,
        which is the real-world case this print statement is unguarded
        against: a Chinese-named deck directory opened on a non-CJK-locale
        machine."""
        with tempfile.TemporaryDirectory() as tmp:
            deck_dir = Path(tmp) / "咖啡萃取的三个变量"
            deck_dir.mkdir()
            (deck_dir / "slide_jobs.json").write_text(
                json.dumps({"slides": [], "selected_backend": None}), encoding="utf-8"
            )

            buffer = io.BytesIO()
            cp1252_stdout = io.TextIOWrapper(buffer, encoding="cp1252", errors="strict")
            old_argv, old_stdout = sys.argv, sys.stdout
            try:
                sys.argv = ["slide_job_status.py", str(deck_dir), "--legacy-unmanaged"]
                sys.stdout = cp1252_stdout
                exit_code = slide_job_status.main()
            finally:
                cp1252_stdout.flush()
                sys.stdout = old_stdout
                sys.argv = old_argv

        self.assertEqual(exit_code, 0)
        buffer.seek(0)
        output = buffer.getvalue().decode("utf-8")
        self.assertIn("咖啡萃取的三个变量", output)


if __name__ == "__main__":
    unittest.main()
