#!/usr/bin/env python3
"""Unit tests for record_user_review.py (and dispatch clear of user_review)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

# Minimal 1x1 PNG
PNG_1X1 = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000a49444154789c63000100000500010d0a2db40000000049454e44ae426082"
)


def _write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _make_deck(tmp: Path, status: str = "recorded") -> Path:
    deck = tmp / "deck"
    img = deck / "origin_image" / "slide_02.png"
    img.parent.mkdir(parents=True, exist_ok=True)
    img.write_bytes(PNG_1X1)
    prompt = deck / "prompts" / "slide_02.json"
    _write_json(prompt, {"slide_id": "slide_02", "prompt": "test"})
    _write_json(
        deck / "slide_jobs.json",
        {
            "slides": [
                {
                    "slide_id": "slide_02",
                    "number": 2,
                    "status": status,
                    "job": "prompts/slide_02.json",
                    "out": "origin_image/slide_02.png",
                }
            ]
        },
    )
    _write_json(deck / "slide_run_state.json", {"status": "created", "history": []})
    return deck


def _run_review(deck: Path, *extra: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "record_user_review.py"), str(deck), *extra],
        capture_output=True,
        text=True,
    )


class RecordUserReviewTests(unittest.TestCase):
    def test_approve_writes_user_review_and_run_state_marker(self) -> None:
        from record_user_review import review_is_valid
        from slide_run_state import load_jobs, load_run_state, sha256_file

        with tempfile.TemporaryDirectory() as tmp:
            deck = _make_deck(Path(tmp), "recorded")
            img = deck / "origin_image" / "slide_02.png"
            proc = _run_review(deck, "--slide", "slide_02", "--approve")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            jobs = load_jobs(deck)
            slide = jobs["slides"][0]
            review = slide["user_review"]
            self.assertEqual(review["status"], "user_reviewed")
            self.assertIn("reviewed_at", review)
            self.assertEqual(review["image_sha256"], sha256_file(img))
            self.assertTrue(review_is_valid(deck, slide))
            state = load_run_state(deck)
            blob = json.dumps(state, ensure_ascii=False).lower()
            self.assertIn("user_reviewed", blob)
            self.assertEqual(state["user_review"]["marker"], "user_reviewed")

    def test_approve_rejects_non_recorded(self) -> None:
        for status in ("pending", "dispatched", "blocked"):
            with self.subTest(status=status):
                with tempfile.TemporaryDirectory() as tmp:
                    deck = _make_deck(Path(tmp), status)
                    proc = _run_review(deck, "--slide", "slide_02", "--approve")
                    self.assertNotEqual(proc.returncode, 0)

    def test_approve_rejects_accepted_sample(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            deck = _make_deck(Path(tmp), "accepted")
            proc = _run_review(deck, "--slide", "slide_02", "--approve")
            self.assertNotEqual(proc.returncode, 0)

    def test_clear_removes_review_and_sticky_marker(self) -> None:
        from slide_run_state import load_jobs, load_run_state

        with tempfile.TemporaryDirectory() as tmp:
            deck = _make_deck(Path(tmp), "recorded")
            self.assertEqual(_run_review(deck, "--slide", "2", "--approve").returncode, 0)
            proc = _run_review(deck, "--slide", "slide_02", "--clear")
            self.assertEqual(proc.returncode, 0, proc.stderr)
            slide = load_jobs(deck)["slides"][0]
            self.assertNotIn("user_review", slide)
            state = load_run_state(deck)
            blob = json.dumps(state, ensure_ascii=False).lower()
            self.assertNotIn("user_reviewed", blob)
            self.assertNotIn("marker", state.get("user_review") or {})

    def test_review_is_valid_false_after_png_rewrite(self) -> None:
        from record_user_review import review_is_valid
        from slide_run_state import load_jobs

        with tempfile.TemporaryDirectory() as tmp:
            deck = _make_deck(Path(tmp), "recorded")
            self.assertEqual(_run_review(deck, "--slide", "slide_02", "--approve").returncode, 0)
            img = deck / "origin_image" / "slide_02.png"
            img.write_bytes(PNG_1X1 + b"\x00")  # corrupt / change bytes
            slide = load_jobs(deck)["slides"][0]
            self.assertFalse(review_is_valid(deck, slide))

    def test_dispatch_clears_user_review(self) -> None:
        from slide_run_state import load_jobs, load_run_state, write_json

        with tempfile.TemporaryDirectory() as tmp:
            deck = _make_deck(Path(tmp), "recorded")
            self.assertEqual(_run_review(deck, "--slide", "slide_02", "--approve").returncode, 0)
            jobs = load_jobs(deck)
            jobs["slides"][0]["status"] = "pending"
            write_json(deck / "slide_jobs.json", jobs)
            proc = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "record_slide_dispatch.py"),
                    str(deck),
                    "--slide",
                    "slide_02",
                    "--agent-id",
                    "agent-test",
                    "--prompt-file",
                    "prompts/slide_02.json",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr + proc.stdout)
            slide = load_jobs(deck)["slides"][0]
            self.assertEqual(slide["status"], "dispatched")
            self.assertNotIn("user_review", slide)
            state = load_run_state(deck)
            blob = json.dumps(state, ensure_ascii=False).lower()
            self.assertNotIn("user_reviewed", blob)
            self.assertNotIn("marker", state.get("user_review") or {})

    def test_multi_slide_clear_keeps_marker_until_last(self) -> None:
        from slide_run_state import load_jobs, load_run_state, write_json

        with tempfile.TemporaryDirectory() as tmp:
            deck = _make_deck(Path(tmp), "recorded")
            # Add slide_03
            img3 = deck / "origin_image" / "slide_03.png"
            img3.write_bytes(PNG_1X1)
            _write_json(deck / "prompts" / "slide_03.json", {"slide_id": "slide_03"})
            jobs = load_jobs(deck)
            jobs["slides"].append(
                {
                    "slide_id": "slide_03",
                    "number": 3,
                    "status": "recorded",
                    "job": "prompts/slide_03.json",
                    "out": "origin_image/slide_03.png",
                }
            )
            write_json(deck / "slide_jobs.json", jobs)
            self.assertEqual(_run_review(deck, "--slide", "slide_02", "--approve").returncode, 0)
            self.assertEqual(_run_review(deck, "--slide", "slide_03", "--approve").returncode, 0)
            state = load_run_state(deck)
            self.assertEqual(state["user_review"]["marker"], "user_reviewed")
            self.assertTrue(state["user_review"]["all_recorded_slides_approved"])
            self.assertEqual(_run_review(deck, "--slide", "slide_02", "--clear").returncode, 0)
            state = load_run_state(deck)
            self.assertEqual(state["user_review"]["marker"], "user_reviewed")
            self.assertEqual(state["user_review"]["approved_slide_ids"], ["slide_03"])
            self.assertFalse(state["user_review"]["all_recorded_slides_approved"])
            self.assertEqual(_run_review(deck, "--slide", "slide_03", "--clear").returncode, 0)
            state = load_run_state(deck)
            blob = json.dumps(state, ensure_ascii=False).lower()
            self.assertNotIn("user_reviewed", blob)


if __name__ == "__main__":
    unittest.main()
