#!/usr/bin/env python3
"""Unit tests for probe_image_backends.py."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from probe_image_backends import build_report, probe_candidates


class ProbeImageBackendsTests(unittest.TestCase):
    def test_cli_always_listed_with_available_flag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            cands = probe_candidates(home, SCRIPTS, honor_codex_home_env=False)
            cli = next(c for c in cands if c["id"] == "scripts-image-gen")
            self.assertTrue(cli["available"])
            self.assertEqual(cli["label"], "scripts/image_gen.py")
            self.assertFalse(any(c["id"] == "codex-gpt-image" for c in cands))

    def test_finds_codex_gpt_image_under_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            skill = home / ".cursor" / "skills" / "codex-gpt-image"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# bridge\n", encoding="utf-8")
            cands = probe_candidates(home, SCRIPTS, honor_codex_home_env=False)
            bridge = next(c for c in cands if c["id"] == "codex-gpt-image")
            self.assertTrue(bridge["available"])
            self.assertEqual(bridge["label"], "codex-gpt-image")

    def test_empty_bridge_dir_without_skill_md_not_available(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            skill = home / ".cursor" / "skills" / "codex-gpt-image"
            skill.mkdir(parents=True)
            cands = probe_candidates(home, SCRIPTS, honor_codex_home_env=False)
            self.assertFalse(any(c["id"] == "codex-gpt-image" for c in cands))

    def test_home_override_ignores_codex_home_env(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fake_codex = root / "codex_home" / "skills" / "codex-gpt-image"
            fake_codex.mkdir(parents=True)
            (fake_codex / "SKILL.md").write_text("# bridge\n", encoding="utf-8")
            empty_home = root / "empty_home"
            empty_home.mkdir()
            previous = os.environ.get("CODEX_HOME")
            os.environ["CODEX_HOME"] = str(root / "codex_home")
            try:
                leaked = probe_candidates(empty_home, SCRIPTS, honor_codex_home_env=True)
                self.assertTrue(any(c["id"] == "codex-gpt-image" for c in leaked))
                isolated = probe_candidates(empty_home, SCRIPTS, honor_codex_home_env=False)
                self.assertFalse(any(c["id"] == "codex-gpt-image" for c in isolated))
                proc = subprocess.run(
                    [
                        sys.executable,
                        str(SCRIPTS / "probe_image_backends.py"),
                        "--home",
                        str(empty_home),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                    env={**os.environ},
                )
                self.assertEqual(proc.returncode, 0, proc.stderr)
                data = json.loads(proc.stdout)
                self.assertFalse(
                    any(c["id"] == "codex-gpt-image" for c in data["candidates"])
                )
            finally:
                if previous is None:
                    os.environ.pop("CODEX_HOME", None)
                else:
                    os.environ["CODEX_HOME"] = previous

    def test_cli_json_stdout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / "probe_image_backends.py"), "--home", tmp],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            data = json.loads(proc.stdout)
            self.assertIn("candidates", data)
            self.assertIn("preference_hints", data)
            self.assertIn("Claude Code", data["host_native_note"])
            self.assertIn("image_generate", data["host_native_note"])

    def test_build_report_claude_preference(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            report = build_report(Path(tmp), SCRIPTS, honor_codex_home_env=False)
            self.assertEqual(
                report["preference_hints"]["claude-code"],
                ["codex-gpt-image", "scripts/image_gen.py"],
            )


if __name__ == "__main__":
    unittest.main()
