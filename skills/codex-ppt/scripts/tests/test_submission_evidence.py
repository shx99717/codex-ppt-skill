"""Actual adapter boundary, receipt replay and compiler downgrade regressions."""
import copy
import io
import json
from contextlib import redirect_stdout
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from planning_fixtures import compile_fixture,dispatch_fixture,fixture_image,run_cli,write_spec
from image_input_contract import validate_receipt,make_receipt
import run_slide_job


class SubmissionEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.deck=Path(self.tmp.name).resolve()
        compile_fixture(self.deck)
        self.assertEqual(dispatch_fixture(self.deck).returncode,0)
        self.out=self.deck/"candidates/attempt.png"

    def state(self):
        jobs=json.loads((self.deck/"slide_jobs.json").read_text(encoding="utf-8"))
        slide=next(v for v in jobs["slides"] if v["slide_id"]=="slide_01")
        job=json.loads((self.deck/slide["job"]).read_text(encoding="utf-8"))
        return jobs,slide,job

    def test_real_adapter_registers_and_result_consumes_exact_attempt(self):
        _,_,job=self.state()
        def provider(command,**kwargs):
            paths=[command[i+1] for i,v in enumerate(command) if v=="--image"]
            self.assertEqual([Path(p).read_bytes() for p in paths],
                             [Path(v["path"]).read_bytes() for v in job["input_images"]])
            self.assertIn("--capabilities-file",command)
            fixture_image(self.out)
            return subprocess.CompletedProcess(command,0)
        with patch.object(run_slide_job.subprocess,"run",side_effect=provider),redirect_stdout(io.StringIO()):
            run_slide_job.execute_job(SimpleNamespace(deck=str(self.deck),slide="1",out=str(self.out),agent_id="fixture-agent",dry_run=False))
        jobs,slide,job=self.state()
        receipt=json.loads(self.out.with_suffix(".submission.json").read_text(encoding="utf-8"))
        self.assertEqual(validate_receipt(receipt,job,slide,self.out),"adapter_verified")
        replay=copy.deepcopy(slide);replay["dispatch"]["attempt_id"]="other-attempt"
        with self.assertRaises(ValueError): validate_receipt(receipt,job,replay,self.out)
        no_registration=copy.deepcopy(slide);no_registration.pop("execution_completion")
        with self.assertRaises(ValueError): validate_receipt(receipt,job,no_registration,self.out)
        dry=copy.deepcopy(slide);dry["execution_completion"]["dry_run"]=True
        with self.assertRaises(ValueError): validate_receipt(receipt,job,dry,self.out)
        result=run_cli("record_slide_result.py",self.deck,"--slide","1","--agent-id","fixture-agent",
            "--backend-used","scripts/image_gen.py","--selected-source",self.out,
            "--submission-receipt",self.out.with_suffix(".submission.json"),"--qa-note","SYNTHETIC provider-boundary test")
        self.assertEqual(result.returncode,0,result.stderr)

    def test_failed_provider_does_not_register_completion(self):
        with patch.object(run_slide_job.subprocess,"run",return_value=subprocess.CompletedProcess([],1)):
            code=run_slide_job.execute_job(SimpleNamespace(deck=str(self.deck),slide="1",out=str(self.out),agent_id="fixture-agent",dry_run=False))
        self.assertEqual(code,1)
        self.assertNotIn("execution_completion",self.state()[1])
        self.assertFalse(self.out.with_suffix(".submission.json").exists())

    def test_envelope_downgrade_is_not_an_opt_out(self):
        jobs,_,_=self.state();jobs.pop("execution_contract_version")
        write_spec(self.deck/"slide_jobs.json",jobs)
        result=run_cli("run_slide_job.py",self.deck,"--slide","1","--out",self.out,"--dry-run")
        self.assertNotEqual(result.returncode,0)
        self.assertIn("recompile",result.stderr)

    def test_native_receipt_rejects_missing_reordered_and_substituted_inputs(self):
        _,slide,job=self.state();job=copy.deepcopy(job)
        job["expected_backend"]="image_gen";job["generation_config"]["tool_name"]="image_gen"
        other=self.deck/"other.png";fixture_image(other,"blue")
        from image_input_contract import sha256
        job["input_images"].append({"path":str(other),"sha256":sha256(other),"role":"strict source","fidelity":"faithful"})
        fixture_image(self.out)
        receipt=make_receipt(job,slide,self.out,"referenced_image_paths")
        self.assertEqual(validate_receipt(receipt,job,slide,self.out),"agent_reported")
        for attachments in (receipt["attachments"][:-1],list(reversed(receipt["attachments"])),[] ):
            bad=copy.deepcopy(receipt);bad["attachments"]=attachments
            with self.assertRaises(ValueError):validate_receipt(bad,job,slide,self.out)
        bad=copy.deepcopy(receipt);bad["attachments"][0]["sha256"]="0"*64
        with self.assertRaises(ValueError):validate_receipt(bad,job,slide,self.out)
