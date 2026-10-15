"""Derived plan/talk views expose intended content without false approvals."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
SCRIPTS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRIPTS))
from planning_fixtures import managed_spec,write_spec,run_cli,approve_fixture
from planning_contract import build_manifest
from planning_views import speech_markdown


class PlanningViewsTests(unittest.TestCase):
    def test_speech_preserves_blank_line_beats_and_slide_mapping(self):
        spec=managed_spec()
        speech=speech_markdown(spec)
        for slide in spec["slides"]:
            self.assertIn(slide["speaker_notes"]["text"],speech)
            self.assertIn(f"## Slide {slide['number']}: {slide['title']}",speech)

    def test_draft_views_do_not_install_spec_or_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            draft=root/"source/input.json"
            spec=managed_spec()
            write_spec(draft,spec)
            deck=root/"deck"
            result=run_cli("planning_views.py","--spec",draft,"--deck",deck,"--draft")
            self.assertEqual(result.returncode,0,result.stderr)
            summary=json.loads(result.stdout)
            self.assertEqual(summary["plan_hash"],build_manifest(spec,draft.parent)["plan_hash"])
            self.assertTrue((deck/"outline.draft.md").is_file())
            self.assertTrue((deck/"speech.draft.md").is_file())
            self.assertFalse((deck/"deck_spec.json").exists())
            self.assertFalse((deck/"plan_approvals.json").exists())
            text=(deck/"outline.draft.md").read_text(encoding="utf-8")
            for term in ("proposed","Account on the left","slide_01","30"):
                self.assertIn(term,text)
            self.assertNotIn(summary["plan_hash"],text)

    def test_final_views_refuse_stale_talk_without_rewriting_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck=Path(tmp)
            spec=approve_fixture(deck)
            before=(deck/"speech.md").read_bytes()
            spec["slides"][0]["speaker_notes"]["text"]+=" Changed."
            write_spec(deck/"deck_spec.json",spec)
            result=run_cli("planning_views.py","--deck",deck)
            self.assertNotEqual(result.returncode,0)
            self.assertEqual((deck/"speech.md").read_bytes(),before)

