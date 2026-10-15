"""Managed consumers reject stale state before mutating or copying images."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
SCRIPTS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRIPTS))
from planning_fixtures import (managed_spec,compile_fixture,dispatch_fixture,result_fixture,
                               run_cli,write_spec,approve_fixture,fixture_image)


class ManagedLifecycleTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.deck=Path(self.tmp.name).resolve()
        self.spec=compile_fixture(self.deck)

    def jobs(self):
        return json.loads((self.deck/"slide_jobs.json").read_text(encoding="utf-8"))

    def test_stale_plan_rejects_dispatch_and_preserves_state(self):
        before=(self.deck/"slide_jobs.json").read_bytes()
        spec=copy.deepcopy(self.spec)
        spec["slides"][0]["visible_copy"]["labels"].append("Unapproved")
        write_spec(self.deck/"deck_spec.json",spec)
        result=dispatch_fixture(self.deck)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual((self.deck/"slide_jobs.json").read_bytes(),before)

    def test_changed_prompt_after_dispatch_rejects_result_before_copy(self):
        self.assertEqual(dispatch_fixture(self.deck).returncode,0)
        path=self.deck/"prompts/slide_01.json"
        job=json.loads(path.read_text(encoding="utf-8"))
        job["prompt"]+="Silent mutation"
        path.write_text(json.dumps(job),encoding="utf-8")
        before=(self.deck/"slide_jobs.json").read_bytes()
        result=result_fixture(self.deck)
        self.assertNotEqual(result.returncode,0)
        self.assertIn("prompt",result.stderr.lower())
        self.assertFalse((self.deck/"origin_image/slide_01.png").exists())
        self.assertEqual((self.deck/"slide_jobs.json").read_bytes(),before)

    def test_changed_approved_style_snapshot_refuses_dispatch(self):
        ledger=json.loads((self.deck/"plan_approvals.json").read_text(encoding="utf-8"))
        (self.deck/ledger["samples"]["slide_02"]["image"]).write_bytes(b"Changed")
        before=(self.deck/"slide_jobs.json").read_bytes()
        self.assertNotEqual(dispatch_fixture(self.deck).returncode,0)
        self.assertEqual((self.deck/"slide_jobs.json").read_bytes(),before)

    def test_current_result_preserves_provenance_and_clears_qa_review(self):
        self.assertEqual(dispatch_fixture(self.deck).returncode,0)
        jobs=self.jobs()
        jobs["slides"][0]["qa"]={"old":True}
        jobs["slides"][0]["user_review"]={"old":True}
        (self.deck/"slide_jobs.json").write_text(json.dumps(jobs),encoding="utf-8")
        result=result_fixture(self.deck)
        self.assertEqual(result.returncode,0,result.stderr)
        slide=self.jobs()["slides"][0]
        self.assertNotIn("user_review",slide)
        self.assertNotIn("qa",slide)
        self.assertEqual(slide["result"]["visual_hash"],slide["visual_hash"])
        self.assertEqual(slide["result"]["selected_source_sha256"],slide["result"]["final_image_sha256"])

    def test_note_only_reapproval_keeps_dispatchable_visual_job(self):
        revised=copy.deepcopy(self.spec)
        revised["slides"][1]["speaker_notes"]["text"]+="\n\nPause."
        approve_fixture(self.deck,revised)
        result=dispatch_fixture(self.deck)
        self.assertEqual(result.returncode,0,result.stderr)

    def test_sample_phase_can_dispatch_before_sample_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck=Path(tmp)
            approve_fixture(deck)
            r=run_cli("prepare_slide_prompts.py","--spec",deck/"deck_spec.json","--out-dir",deck,
                      "--phase","sample","--slides","slide_02")
            self.assertEqual(r.returncode,0,r.stderr)
            result=dispatch_fixture(deck,"slide_02")
            self.assertEqual(result.returncode,0,result.stderr)

    def test_legacy_flag_cannot_bypass_managed_dispatch(self):
        result=run_cli("record_slide_dispatch.py",self.deck,"--slide","slide_01",
                       "--agent-id","fixture-agent","--legacy-unmanaged")
        self.assertNotEqual(result.returncode,0)

    def test_missing_metadata_cannot_silently_dispatch_legacy(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck=Path(tmp)
            (deck/"prompts").mkdir()
            (deck/"prompts/slide_01.json").write_text("{}",encoding="utf-8")
            jobs={"slides":[{"slide_id":"slide_01","number":1,"status":"pending","job":"prompts/slide_01.json"}]}
            (deck/"slide_jobs.json").write_text(json.dumps(jobs),encoding="utf-8")
            self.assertNotEqual(dispatch_fixture(deck).returncode,0)
