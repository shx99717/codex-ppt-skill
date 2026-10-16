#!/usr/bin/env python3
"""Unit tests for record_slide_result.py locked-ratio gate."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_jobs_deck(tmp: Path, aspect_ratio: str) -> Path:
    deck = tmp / "deck"
    deck.mkdir()
    (deck / "origin_image").mkdir()
    _write_json(
        deck / "slide_jobs.json",
        {
            "selected_backend": "GenerateImage",
            "aspect_ratio": aspect_ratio,
            "slides": [
                {
                    "slide_id": "slide_01",
                    "status": "dispatched",
                    "out": "origin_image/slide_01.png",
                    "dispatch": {"agent_id": "t1"},
                }
            ],
        },
    )
    _write_json(deck / "slide_run_state.json", {"status": "created", "history": []})
    return deck


def _png(path: Path, size: tuple[int, int]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", size, color="white").save(path)
    return path


def _record(deck: Path, source: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "record_slide_result.py"),
            str(deck),
            "--legacy-unmanaged",
            "--slide",
            "slide_01",
            "--agent-id",
            "t1",
            "--backend-used",
            "GenerateImage",
            "--selected-source",
            str(source),
            "--qa-note",
            "ok",
        ],
        capture_output=True,
        text=True,
    )


class RecordSlideResultRatioTests(unittest.TestCase):
    def test_refuses_3_2_image_when_jobs_locked_16_9(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            deck = _make_jobs_deck(root, "16:9")
            source = _png(root / "candidate.png", (48, 32))
            target = deck / "origin_image" / "slide_01.png"
            proc = _record(deck, source)
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertFalse(target.exists())
            combined = proc.stdout + proc.stderr
            self.assertIn("48x32", combined)

    def test_copies_32x18_when_jobs_locked_16_9(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            deck = _make_jobs_deck(root, "16:9")
            source = _png(root / "candidate.png", (32, 18))
            target = deck / "origin_image" / "slide_01.png"
            proc = _record(deck, source)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertTrue(target.exists())

    def test_rejects_retired_3_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            deck = _make_jobs_deck(root, "3:2")
            source = _png(root / "candidate.png", (48, 32))
            target = deck / "origin_image" / "slide_01.png"
            proc = _record(deck, source)
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertFalse(target.exists())

    def test_refuses_32x18_when_jobs_locked_3_2(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            deck = _make_jobs_deck(root, "3:2")
            source = _png(root / "candidate.png", (32, 18))
            target = deck / "origin_image" / "slide_01.png"
            proc = _record(deck, source)
            self.assertNotEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertFalse(target.exists())


if __name__ == "__main__":
    unittest.main()
