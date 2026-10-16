"""Dry-run the real bundled CLI; no provider or paid generation calls."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
import io
import os
from unittest.mock import patch
from filelock import FileLock,Timeout
SCRIPTS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRIPTS))
from planning_fixtures import (managed_spec,approve_fixture,compile_fixture,
                              dispatch_fixture,fixture_image,run_cli,write_spec)
import run_slide_job


class ManagedExecutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.deck=Path(self.tmp.name).resolve()
        self.spec=managed_spec()
        self.spec["planning"]["generation"].update(reference_mode="edit",model="gpt-image-2",
            size="3840x2160",quality="high",output_format="png",n=1)

    def run_job(self,sid="slide_01"):
        return run_cli("run_slide_job.py",self.deck,"--slide",sid,"--out",
                       self.deck/f"candidates/{sid}.png","--dry-run")

    def preview(self,result):
        self.assertEqual(result.returncode,0,result.stdout+result.stderr)
        start=result.stdout.index("{")
        return json.JSONDecoder().raw_decode(result.stdout[start:])[0]

    def test_production_forwards_locked_config_and_every_image_input(self):
        source=self.deck/"source.png";fixture_image(source,"blue")
        self.spec["slides"][0]["required_images"]=[{"path":str(source),"role":"approved source","fidelity":"faithful"}]
        compile_fixture(self.deck,self.spec)
        job=json.loads((self.deck/"prompts/slide_01.json").read_text(encoding="utf-8"))
        preview=self.preview(self.run_job())
        self.assertEqual(preview["endpoint"],"/v1/images/edits")
        payload=preview
        for field in ("model","size","quality","output_format","n"):
            self.assertEqual(payload[field],self.spec["planning"]["generation"][field])
        self.assertEqual(len(payload["image"]),len(job["input_images"]))
        for staged,original in zip(payload["image"],job["input_images"]):
            self.assertIn(original["sha256"],Path(staged).name)
        self.assertEqual(payload["prompt"],job["prompt"])
        self.assertFalse((self.deck/"candidates/slide_01.png").exists())

    def test_text_only_calibration_uses_approved_generate_operation(self):
        approve_fixture(self.deck,self.spec)
        result=run_cli("prepare_slide_prompts.py","--spec",self.deck/"deck_spec.json",
            "--out-dir",self.deck,"--phase","sample","--slides","slide_02")
        self.assertEqual(result.returncode,0,result.stderr)
        preview=self.preview(self.run_job("slide_02"))
        self.assertEqual(preview["endpoint"],"/v1/images/generations")
        self.assertNotIn("image",preview)

    def test_missing_reference_operation_and_unknown_fields_fail_before_dispatch(self):
        for field in ("reference_mode","unknown_option"):
            with self.subTest(field=field),tempfile.TemporaryDirectory() as tmp:
                deck=Path(tmp).resolve();spec=copy.deepcopy(self.spec)
                if field=="reference_mode":
                    spec["planning"]["generation"].pop(field)
                else:
                    spec["planning"]["generation"][field]=True
                # Either approval validation or compilation must reject, never dispatch.
                draft=deck/"input.json";write_spec(draft,spec)
                from planning_contract import build_manifest,ContractError
                try:
                    approve_fixture(deck,spec)
                except (AssertionError,ContractError):
                    continue
                from planning_fixtures import approve_fixture_sample
                try:
                    approve_fixture_sample(deck)
                except AssertionError as exc:
                    self.assertEqual(field,"unknown_option")
                    self.assertIn("Unsupported CLI generation fields: unknown_option",str(exc))
                    self.assertFalse((deck/"slide_jobs.json").exists())
                    continue
                result=run_cli("prepare_slide_prompts.py","--spec",deck/"deck_spec.json","--out-dir",deck)
                if result.returncode==0:
                    self.assertNotEqual(dispatch_fixture(deck).returncode,0)

    def test_output_cannot_overwrite_owned_final_or_immutable_input(self):
        compile_fixture(self.deck,self.spec)
        target=self.deck/"origin_image/slide_01.png"
        fixture_image(target,"blue");before=target.read_bytes()
        result=run_cli("run_slide_job.py",self.deck,"--slide","slide_01","--out",target,"--dry-run")
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(target.read_bytes(),before)

    def test_noninteger_cli_parameters_are_rejected_before_dispatch(self):
        for field,value in (("n",1.0),("n",True),("n","1"),
                            ("output_compression",50.5),("output_compression",True),
                            ("output_compression","50")):
            with self.subTest(field=field,value=value),tempfile.TemporaryDirectory() as tmp:
                deck=Path(tmp).resolve();spec=copy.deepcopy(self.spec)
                spec["planning"]["generation"][field]=value
                approve_fixture(deck,spec)
                from planning_fixtures import approve_fixture_sample
                try:
                    approve_fixture_sample(deck)
                except AssertionError as exc:
                    expected="Managed slide execution requires n=1" if field=="n" else "output_compression must be an integer"
                    self.assertIn(expected,str(exc))
                    self.assertFalse((deck/"slide_jobs.json").exists())
                    continue
                result=run_cli("prepare_slide_prompts.py","--spec",deck/"deck_spec.json","--out-dir",deck)
                self.assertNotEqual(result.returncode,0,result.stderr)
                self.assertFalse((deck/"slide_jobs.json").exists())

    def test_generation_releases_global_locks_and_uses_verified_snapshots(self):
        compile_fixture(self.deck,self.spec)
        self.assertEqual(dispatch_fixture(self.deck).returncode,0)
        job=json.loads((self.deck/"prompts/slide_01.json").read_text(encoding="utf-8"))
        seen=[]
        def backend(command,**kwargs):
            for name in (".planning.lock",".slide_jobs.json.lock"):
                with FileLock(str(self.deck/name),timeout=0):
                    seen.append(name)
            actual=[command[i+1] for i,arg in enumerate(command) if arg=="--image"]
            self.assertEqual(len(actual),len(job["input_images"]))
            for path,original in zip(actual,job["input_images"]):
                self.assertEqual(Path(path).read_bytes(),Path(original["path"]).read_bytes())
            fixture_image(Path(command[command.index("--out")+1]),"blue")
            return subprocess.CompletedProcess(command,0)
        import subprocess
        with patch.object(sys,"argv",["run_slide_job.py",str(self.deck),"--slide","1",
            "--agent-id","fixture-agent","--out",str(self.deck/"candidates/attempt.png")]), \
            patch.object(run_slide_job.subprocess,"run",side_effect=backend),redirect_stdout(io.StringIO()):
            run_slide_job.main()
        self.assertEqual(seen,[".planning.lock",".slide_jobs.json.lock"])

    def test_stale_attempt_is_refused_after_backend_returns(self):
        compile_fixture(self.deck,self.spec)
        self.assertEqual(dispatch_fixture(self.deck).returncode,0)
        def backend(command,**kwargs):
            path=self.deck/"slide_jobs.json"
            state=json.loads(path.read_text(encoding="utf-8"))
            state["slides"][0]["dispatch"]["agent_id"]="different-worker"
            write_spec(path,state)
            fixture_image(Path(command[command.index("--out")+1]),"blue")
            return subprocess.CompletedProcess(command,0)
        import subprocess
        from planning_contract import ContractError
        with patch.object(sys,"argv",["run_slide_job.py",str(self.deck),"--slide","1",
            "--agent-id","fixture-agent","--out",str(self.deck/"candidates/stale.png")]), \
            patch.object(run_slide_job.subprocess,"run",side_effect=backend),redirect_stdout(io.StringIO()):
            with self.assertRaises((ContractError,SystemExit)):
                run_slide_job.main()

    def test_two_provider_calls_overlap_without_global_state_locks(self):
        from concurrent.futures import ThreadPoolExecutor
        from types import SimpleNamespace
        import threading
        import subprocess
        spec=copy.deepcopy(self.spec)
        third=copy.deepcopy(spec["slides"][0]);third["number"]=3
        spec["slides"].append(third)
        compile_fixture(self.deck,spec,capacity=2)
        for sid in ("slide_01","slide_03"):
            self.assertEqual(dispatch_fixture(self.deck,sid).returncode,0)
        barrier=threading.Barrier(2)
        calls=[]
        def backend(command,**kwargs):
            calls.append(command)
            barrier.wait(timeout=10)  # Both calls must enter before either returns.
            with FileLock(str(self.deck/".planning.lock"),timeout=1), \
                 FileLock(str(self.deck/".slide_jobs.json.lock"),timeout=1):
                # Independent state inspection/update can run while provider work overlaps.
                path=self.deck/"slide_jobs.json"
                state=json.loads(path.read_text(encoding="utf-8"))
                state["mock_status_probe"]="updated while generating"
                write_spec(path,state)
            fixture_image(Path(command[command.index("--out")+1]),"blue")
            return subprocess.CompletedProcess(command,0)
        with patch.object(run_slide_job.subprocess,"run",side_effect=backend), \
             redirect_stdout(io.StringIO()),ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(run_slide_job.execute_job,SimpleNamespace(deck=str(self.deck),
                slide=sid,out=str(self.deck/f"candidates/{sid}.png"),
                agent_id="fixture-agent",dry_run=False)) for sid in ("slide_01","slide_03")]
            self.assertEqual([f.result(timeout=15) for f in futures],[0,0])
        self.assertEqual(len(calls),2)

    def test_repair_and_integer_optional_config_use_same_executable_policy(self):
        from planning_fixtures import result_fixture,qa_fixture
        self.spec["planning"]["generation"]["output_compression"]=50
        compile_fixture(self.deck,self.spec)
        self.assertEqual(dispatch_fixture(self.deck).returncode,0)
        self.assertEqual(result_fixture(self.deck).returncode,0)
        self.assertEqual(qa_fixture(self.deck,decision="--needs-repair").returncode,0)
        result=run_cli("prepare_slide_prompts.py","--spec",self.deck/"deck_spec.json",
            "--out-dir",self.deck,"--phase","repair","--slides","slide_01","--force")
        self.assertEqual(result.returncode,0,result.stderr)
        preview=self.preview(self.run_job())
        self.assertEqual(preview["endpoint"],"/v1/images/edits")
        self.assertEqual(preview["output_compression"],50)
        self.assertEqual(preview["quality"],"high")

    @unittest.skipUnless(os.name=="nt","Windows native final-path namespace regression")
    def test_candidate_parent_creation_cannot_race_windows_resolution(self):
        import ntpath
        import subprocess
        from types import SimpleNamespace
        compile_fixture(self.deck,self.spec)
        out=self.deck/"candidates/new.png"
        native=ntpath._getfinalpathname
        attempted=[]
        def concurrent_creator(path):
            try:
                return native(path)
            except OSError:
                if str(path)==str(out) and not attempted:
                    attempted.append(True)
                    # A second managed worker may create the shared parent only
                    # while holding its planning lock, just like real adapters.
                    try:
                        with FileLock(str(self.deck/".planning.lock"),timeout=0):
                            out.parent.mkdir(exist_ok=True)
                    except Timeout:
                        pass
                raise
        with patch.object(ntpath,"_getfinalpathname",side_effect=concurrent_creator), \
             patch.object(run_slide_job.subprocess,"run",return_value=subprocess.CompletedProcess([],0)), \
             redirect_stdout(io.StringIO()):
            self.assertEqual(run_slide_job.execute_job(SimpleNamespace(deck=str(self.deck),
                slide="slide_01",out=str(out),agent_id=None,dry_run=True)),0)
        self.assertTrue(attempted)
