"""SHA-bound agent QA, actual first-batch checks, and bounded repairs."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
SCRIPTS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRIPTS))
from planning_fixtures import (managed_spec,compile_fixture,dispatch_fixture,result_fixture,
                               qa_fixture,run_cli,fixture_image)


class SlideQATests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.deck=Path(self.tmp.name).resolve()
        self.spec=managed_spec()
        third=copy.deepcopy(self.spec["slides"][0])
        third["number"]=3
        third["depends_on"]=[]
        self.spec["slides"].append(third)
        compile_fixture(self.deck,self.spec,1)

    def jobs(self):
        return json.loads((self.deck/"slide_jobs.json").read_text(encoding="utf-8"))

    def record(self,sid="slide_01"):
        r=dispatch_fixture(self.deck,sid)
        self.assertEqual(r.returncode,0,r.stderr)
        r=result_fixture(self.deck,sid)
        self.assertEqual(r.returncode,0,r.stderr)

    def repair(self,sid="slide_01"):
        return run_cli("prepare_slide_prompts.py","--spec",self.deck/"deck_spec.json",
                       "--out-dir",self.deck,"--phase","repair","--slides",sid,"--force")

    def test_first_batch_requires_agent_qa_before_next_dispatch(self):
        self.record()
        result=dispatch_fixture(self.deck,"slide_03")
        self.assertNotEqual(result.returncode,0)
        self.assertIn("batch",result.stderr.lower())
        self.assertEqual(qa_fixture(self.deck).returncode,0)
        self.assertEqual(dispatch_fixture(self.deck,"slide_03").returncode,0)
        self.assertEqual(self.jobs()["first_batch"]["ids"],["slide_01"])

    def test_qa_is_agent_only_and_image_bound(self):
        self.record()
        result=qa_fixture(self.deck)
        self.assertEqual(result.returncode,0,result.stderr)
        qa=self.jobs()["slides"][0]["qa"]
        self.assertEqual(qa["actor"],"agent")
        self.assertNotIn("user_review",self.jobs()["slides"][0])
        fixture_image(self.deck/"origin_image/slide_01.png","red")
        status=run_cli("slide_job_status.py",self.deck,"--json")
        self.assertEqual(status.returncode,0,status.stderr)
        self.assertIn("slide_01",json.loads(status.stdout)["pending_qa"])

    def test_one_repair_then_explicit_extra_attempt_event(self):
        self.record()
        self.assertEqual(qa_fixture(self.deck,decision="--needs-repair").returncode,0)
        r=self.repair()
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(dispatch_fixture(self.deck).returncode,0)
        self.assertEqual(result_fixture(self.deck).returncode,0)
        self.assertEqual(qa_fixture(self.deck,decision="--needs-repair").returncode,0)
        self.assertEqual(self.repair().returncode,0)
        before=(self.deck/"slide_jobs.json").read_bytes()
        r=dispatch_fixture(self.deck)
        self.assertNotEqual(r.returncode,0)
        self.assertIn("repair limit reached",r.stderr.lower())
        self.assertEqual((self.deck/"slide_jobs.json").read_bytes(),before)
        r=run_cli("record_plan_approval.py",self.deck,"--authorize-repair","slide_01",
                  "--additional-attempts","1","--evidence","SYNTHETIC TEST extra attempt decision")
        self.assertEqual(r.returncode,0,r.stderr)
        r=dispatch_fixture(self.deck)
        self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(self.jobs()["slides"][0]["repair_counts"][self.jobs()["slides"][0]["visual_hash"]],2)

    def test_repeated_first_batch_failure_pauses_production(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck=Path(tmp).resolve()
            spec=copy.deepcopy(self.spec)
            fourth=copy.deepcopy(spec["slides"][0]);fourth["number"]=4
            spec["slides"].append(fourth)
            compile_fixture(deck,spec,2)
            for sid in ("slide_01","slide_03"):
                self.assertEqual(dispatch_fixture(deck,sid).returncode,0)
            for sid in ("slide_01","slide_03"):
                self.assertEqual(result_fixture(deck,sid).returncode,0)
                self.assertEqual(qa_fixture(deck,sid,"--needs-repair").returncode,0)
            state=json.loads((deck/"slide_jobs.json").read_text(encoding="utf-8"))
            self.assertTrue(state["systemic_pause"])
            self.assertNotEqual(dispatch_fixture(deck,"slide_04").returncode,0)

    def test_production_phase_cannot_bypass_later_slide_repair_budget(self):
        self.record()
        self.assertEqual(qa_fixture(self.deck).returncode,0)
        self.record("slide_03")
        self.assertEqual(qa_fixture(self.deck,"slide_03","--needs-repair").returncode,0)
        self.assertEqual(self.repair("slide_03").returncode,0)
        self.assertEqual(dispatch_fixture(self.deck,"slide_03").returncode,0)
        self.assertEqual(result_fixture(self.deck,"slide_03").returncode,0)
        self.assertEqual(qa_fixture(self.deck,"slide_03","--needs-repair").returncode,0)
        before=(self.deck/"slide_jobs.json").read_bytes()
        result=run_cli("prepare_slide_prompts.py","--spec",self.deck/"deck_spec.json",
                       "--out-dir",self.deck,"--phase","production","--slides","slide_03","--force")
        self.assertNotEqual(result.returncode,0)
        self.assertEqual((self.deck/"slide_jobs.json").read_bytes(),before)

    def test_deck_qa_needs_current_per_slide_qa(self):
        self.record()
        result=run_cli("record_slide_qa.py",self.deck,"--deck-pass","--evidence","SYNTHETIC TEST sequence QA")
        self.assertNotEqual(result.returncode,0)
