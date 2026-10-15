"""Approval preflight regressions for the managed prompt compiler."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))

from planning_fixtures import managed_spec


class ManagedPreparationTests(unittest.TestCase):

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.deck=Path(self.tmp.name)/"deck"
        self.deck.mkdir()

    def prepare(self,*args):
        from planning_fixtures import run_cli
        return run_cli("prepare_slide_prompts.py","--spec",self.deck/"deck_spec.json",
                       "--out-dir",self.deck,*args)

    def approve(self,sample=False):
        from planning_fixtures import approve_fixture,approve_fixture_sample
        spec=approve_fixture(self.deck)
        if sample:
            approve_fixture_sample(self.deck)
        return spec

    def jobs(self):
        return json.loads((self.deck/"slide_jobs.json").read_text(encoding="utf-8"))

    def test_production_requires_sample_without_writes(self):
        self.approve()
        result=self.prepare()
        self.assertNotEqual(result.returncode,0)
        self.assertIn("sample",result.stderr.lower())
        self.assertFalse((self.deck/"prompts").exists())

    def test_sample_phase_compiles_only_explicit_selection(self):
        self.approve()
        result=self.prepare("--phase","sample","--slides","slide_02")
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertTrue((self.deck/"prompts/slide_02.json").exists())
        self.assertFalse((self.deck/"prompts/slide_01.json").exists())
        self.assertEqual(self.jobs()["workflow_version"],2)

    def test_sample_phase_requires_explicit_representative_selection(self):
        self.approve()
        for args in (("--phase","sample"),("--phase","sample","--slides","slide_01")):
            result=self.prepare(*args)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse((self.deck/"prompts").exists())

    def test_production_embeds_exact_copy_filtered_context_and_snapshots(self):
        self.approve(True)
        result=self.prepare()
        self.assertEqual(result.returncode,0,result.stderr)
        job=json.loads((self.deck/"prompts/slide_01.json").read_text(encoding="utf-8"))
        self.assertIn("One account, fewer access steps",job["prompt"])
        self.assertIn("visible_copy",job["prompt"])
        self.assertNotIn("Hi everyone.",job["prompt"])
        self.assertTrue(Path(job["input_images"][0]["path"]).resolve().is_relative_to(self.deck.resolve()))
        self.assertEqual(job["phase"],"production")

    def test_backend_override_cannot_conflict(self):
        self.approve(True)
        result=self.prepare("--selected-backend","other")
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.deck/"prompts").exists())

    def test_changed_sample_strategy_needs_actual_plan_approval(self):
        from planning_fixtures import write_spec
        spec=self.approve()
        spec["planning"]["sample_strategy"]["required_slides"]=["slide_01"]
        write_spec(self.deck/"deck_spec.json",spec)
        result=self.prepare("--phase","sample","--slides","slide_01")
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.deck/"prompts").exists())

    def test_note_only_approval_and_force_preserve_job_bytes_and_result(self):
        from planning_fixtures import approve_fixture
        spec=self.approve(True)
        self.assertEqual(self.prepare().returncode,0)
        before=(self.deck/"prompts/slide_01.json").read_bytes()
        jobs=self.jobs()
        entry=jobs["slides"][0]
        entry.update(status="recorded",result={"synthetic":True},user_review={"synthetic":True})
        (self.deck/"slide_jobs.json").write_text(json.dumps(jobs),encoding="utf-8")
        spec["slides"][1]["speaker_notes"]["text"]+="\n\nLet us pause."
        approve_fixture(self.deck,spec)
        result=self.prepare("--force")
        self.assertEqual(result.returncode,0,result.stderr)
        self.assertEqual((self.deck/"prompts/slide_01.json").read_bytes(),before)
        self.assertEqual(self.jobs()["slides"][0]["result"],{"synthetic":True})
        self.assertEqual(self.jobs()["slides"][0]["user_review"],{"synthetic":True})

    def test_dispatched_job_refuses_replacement_without_partial_writes(self):
        from planning_fixtures import approve_fixture
        spec=self.approve(True)
        self.assertEqual(self.prepare().returncode,0)
        jobs=self.jobs()
        jobs["slides"][1]["status"]="dispatched"
        (self.deck/"slide_jobs.json").write_text(json.dumps(jobs),encoding="utf-8")
        old={p.name:p.read_bytes() for p in (self.deck/"prompts").iterdir()}
        spec["slides"][0]["visible_copy"]["labels"].append("Changed")
        approve_fixture(self.deck,spec)
        result=self.prepare("--force")
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(old,{p.name:p.read_bytes() for p in (self.deck/"prompts").iterdir()})

    def test_legacy_cannot_bypass_managed_or_malformed_markers(self):
        self.approve(True)
        result=self.prepare("--legacy-unmanaged")
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.deck/"prompts").exists())

    def test_template_is_honest_unapproved_v2_draft(self):
        from planning_fixtures import run_cli
        path=self.deck/"template.json"
        result=run_cli("prepare_slide_prompts.py","--write-template",path)
        self.assertEqual(result.returncode,0,result.stderr)
        value=json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(value["workflow_version"],2)
        self.assertNotIn("approved_style_reference",value)
        self.assertFalse(any("sample_approved" in s for s in value["slides"]))
        self.assertTrue(value["planning"]["unresolved"])
    def test_managed_production_refuses_missing_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp) / "deck"
            deck.mkdir()
            spec_path = deck / "deck_spec.json"
            spec_path.write_text(json.dumps(managed_spec()), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "prepare_slide_prompts.py"),
                 "--spec", str(spec_path), "--out-dir", str(deck)],
                capture_output=True, text=True,
            )
            artifacts = sorted(p.relative_to(deck).as_posix()
                               for p in deck.rglob("*") if p.is_file())
            self.assertNotEqual(
                result.returncode, 0,
                f"Managed production succeeded without approval. "
                f"Artifacts: {artifacts}. Output: {result.stdout}{result.stderr}",
            )
            self.assertIn("approval", (result.stdout + result.stderr).lower())
            self.assertFalse((deck / "prompts").exists())


if __name__ == "__main__":
    unittest.main()

