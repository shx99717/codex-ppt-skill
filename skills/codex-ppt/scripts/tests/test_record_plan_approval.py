"""Actual scoped decision recording, snapshots, and rejected-mutation behavior."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRIPTS))
from planning_fixtures import (managed_spec, run_cli, write_spec, fixture_image,
                               approve_fixture, approve_fixture_sample)
from planning_contract import (ContractError, build_manifest, load_managed_spec,
                               require_plan_approval, require_samples, file_digest)
import record_plan_approval


class PlanApprovalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.deck=Path(self.tmp.name)/"deck"
        self.deck.mkdir()
        self.spec=managed_spec()

    def ledger(self):
        return json.loads((self.deck/"plan_approvals.json").read_text(encoding="utf-8"))

    def record(self,spec=None,scope="all",slides=None,evidence="SYNTHETIC TEST decision",expected=None):
        spec=self.spec if spec is None else spec
        draft=self.deck/"draft.json"
        write_spec(draft,spec)
        args=[self.deck,"--spec",draft,"--approve","--scope",scope,"--expected-plan-hash",
              expected or build_manifest(spec,draft.parent)["plan_hash"],"--evidence",evidence]
        if slides:
            args+=["--slides",slides]
        return run_cli("record_plan_approval.py",*args)

    def test_whole_plan_records_actual_scopes_and_policy_hash(self):
        result=self.record()
        self.assertEqual(result.returncode,0,result.stderr)
        spec=load_managed_spec(self.deck)
        m=build_manifest(spec,self.deck)
        ledger=require_plan_approval(self.deck,m,list(m["slides"]))
        self.assertEqual(ledger["policy"]["policy_hash"],m["policy_hash"])
        self.assertEqual(set(ledger["events"][0]["scopes"]),{"visual","talk","policy"})
        self.assertEqual(ledger["events"][0]["actor"],"user")
        self.assertTrue((self.deck/"speech.md").is_file())

    def test_evidence_and_reviewed_hash_are_required(self):
        for evidence,expected in (("","wrong"),("Decision","wrong")):
            result=self.record(evidence=evidence,expected=expected)
            self.assertNotEqual(result.returncode,0)
            self.assertFalse((self.deck/"deck_spec.json").exists())
            self.assertFalse((self.deck/"plan_approvals.json").exists())

    def test_changed_draft_refuses_without_altering_existing_state(self):
        self.assertEqual(self.record().returncode,0)
        before={n:(self.deck/n).read_bytes() for n in ("deck_spec.json","plan_approvals.json")}
        expected=build_manifest(self.spec,self.deck)["plan_hash"]
        revised=copy.deepcopy(self.spec)
        revised["slides"][0]["visible_copy"]["labels"].append("Changed")
        self.assertNotEqual(self.record(revised,expected=expected).returncode,0)
        self.assertEqual(before,{n:(self.deck/n).read_bytes() for n in before})

    def test_scoped_edit_preserves_unaffected_events_and_stales_dependents(self):
        self.assertEqual(self.record().returncode,0)
        before=self.ledger()
        revised=copy.deepcopy(self.spec)
        revised["slides"][0]["visible_copy"]["labels"].append("New fact")
        self.assertEqual(self.record(revised,scope="slides",slides="slide_01").returncode,0)
        after=self.ledger()
        self.assertEqual(before["slides"]["slide_02"],after["slides"]["slide_02"])
        self.assertEqual(before["policy"],after["policy"])
        m=build_manifest(revised,self.deck)
        require_plan_approval(self.deck,m,["slide_01"])
        with self.assertRaises(ContractError):
            require_plan_approval(self.deck,m,["slide_02"])

    def test_note_only_revision_retains_visual_event(self):
        self.assertEqual(self.record().returncode,0)
        before=self.ledger()
        revised=copy.deepcopy(self.spec)
        revised["slides"][1]["speaker_notes"]["text"]+="\n\nLet me pause."
        self.assertEqual(self.record(revised,scope="slides",slides="slide_02").returncode,0)
        after=self.ledger()
        self.assertEqual(before["slides"]["slide_02"]["visual_event_id"],after["slides"]["slide_02"]["visual_event_id"])
        self.assertNotEqual(before["slides"]["slide_02"]["talk_event_id"],after["slides"]["slide_02"]["talk_event_id"])

    def test_partial_approval_does_not_publish_unapproved_dependent_talk(self):
        self.assertEqual(self.record().returncode,0)
        before=(self.deck/"speech.md").read_bytes()
        revised=copy.deepcopy(self.spec)
        revised["slides"][0]["speaker_notes"]["text"]+="\n\nA revised explanation."
        self.assertEqual(self.record(revised,scope="slides",slides="slide_01").returncode,0)
        self.assertEqual((self.deck/"speech.md").read_bytes(),before)
        self.assertIn("A revised explanation.",(self.deck/"speech.draft.md").read_text(encoding="utf-8"))

    def test_slide_approval_cannot_refresh_changed_output_policy(self):
        self.assertEqual(self.record().returncode,0)
        old=self.ledger()["policy"]
        revised=copy.deepcopy(self.spec)
        revised["planning"]["review_policy"]="strict"
        self.assertEqual(self.record(revised,scope="slides",slides="slide_01").returncode,0)
        self.assertEqual(self.ledger()["policy"],old)
        m=build_manifest(revised,self.deck)
        with self.assertRaises(ContractError):
            require_plan_approval(self.deck,m,["slide_01"])
        draft=self.deck/"policy.json"
        write_spec(draft,revised)
        result=run_cli("record_plan_approval.py",self.deck,"--spec",draft,"--approve-policy",
                       "--expected-plan-hash",m["plan_hash"],"--evidence","SYNTHETIC TEST policy decision")
        self.assertEqual(result.returncode,0,result.stderr)
        require_plan_approval(self.deck,m,["slide_01","slide_02"])

    def test_outside_draft_assets_are_normalized_and_snapshotted(self):
        source=self.deck.parent/"input"
        source.mkdir()
        asset=source/"figure.png"
        fixture_image(asset,"blue")
        fixture_image(self.deck/"figure.png","red")
        self.spec["slides"][0]["required_images"]=[{"path":"figure.png","role":"source figure","fidelity":"preserve"}]
        self.spec["planning"]["shared_visuals"]["account"]["asset_path"]="figure.png"
        draft=source/"draft.json"
        write_spec(draft,self.spec)
        m=build_manifest(self.spec,source)
        result=run_cli("record_plan_approval.py",self.deck,"--spec",draft,"--approve",
                       "--expected-plan-hash",m["plan_hash"],"--evidence","SYNTHETIC TEST source decision")
        self.assertEqual(result.returncode,0,result.stderr)
        canonical=load_managed_spec(self.deck)
        self.assertEqual(canonical["slides"][0]["required_images"][0]["path"],asset.resolve().as_posix())
        self.assertEqual(m,build_manifest(canonical,self.deck))
        ledger=self.ledger()
        self.assertEqual(ledger["events"][0]["asset_provenance"][0]["declared_path"],"figure.png")
        snapshot=ledger["assets"][asset.resolve().as_posix()]
        self.assertEqual(file_digest(self.deck/snapshot["path"]),file_digest(asset))

    def test_snapshot_failure_leaves_prior_spec_and_ledger(self):
        approve_fixture(self.deck)
        before={n:(self.deck/n).read_bytes() for n in ("deck_spec.json","plan_approvals.json")}
        draft=self.deck/"replacement.json"
        write_spec(draft,self.spec)
        with patch.object(record_plan_approval,"snapshot_assets",side_effect=OSError("Synthetic copy failure")):
            with self.assertRaises(OSError):
                record_plan_approval.record_plan(self.deck,draft,scope="all",slides=None,
                    approve_policy=True,expected_plan_hash=build_manifest(self.spec,self.deck)["plan_hash"],
                    evidence="SYNTHETIC TEST decision")
        self.assertEqual(before,{n:(self.deck/n).read_bytes() for n in before})

    def test_immutable_sample_survives_final_page_repair(self):
        approve_fixture(self.deck)
        candidate=approve_fixture_sample(self.deck)
        ledger=self.ledger()
        ref=self.deck/ledger["samples"]["slide_02"]["image"]
        self.assertEqual(ref.read_bytes(),candidate.read_bytes())
        original=ref.read_bytes()
        fixture_image(self.deck/"origin_image/slide_02.png","red")
        spec=load_managed_spec(self.deck)
        require_samples(self.deck,spec,build_manifest(spec,self.deck),self.ledger())
        self.assertEqual(ref.read_bytes(),original)
        self.assertNotEqual(file_digest(self.deck/"origin_image/slide_02.png"),ledger["samples"]["slide_02"]["accepted_final"]["image_sha256"])

    def test_sample_drift_style_change_backend_and_ratio_fail(self):
        approve_fixture(self.deck)
        approve_fixture_sample(self.deck)
        ledger=self.ledger()
        spec=load_managed_spec(self.deck)
        m=build_manifest(spec,self.deck)
        require_samples(self.deck,spec,m,ledger)
        ref=self.deck/ledger["samples"]["slide_02"]["image"]
        ref.write_bytes(b"corrupt sample")
        with self.assertRaises(ContractError):
            require_samples(self.deck,spec,m,ledger)

    def test_wrong_sample_backend_rejected_before_copy(self):
        approve_fixture(self.deck)
        candidate=self.deck/"candidate.png"
        fixture_image(candidate)
        result=run_cli("record_plan_approval.py",self.deck,"--approve-sample","slide_02",
                       "--image",candidate,"--backend-used","other","--evidence","SYNTHETIC TEST")
        self.assertNotEqual(result.returncode,0)
        self.assertFalse((self.deck/"references/approved_samples").exists())

    def test_interrupted_install_is_fail_closed(self):
        approve_fixture(self.deck)
        (self.deck/".planning_transaction.json").write_text("{}",encoding="utf-8")
        with self.assertRaises(ContractError):
            load_managed_spec(self.deck)

