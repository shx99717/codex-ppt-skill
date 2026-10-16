"""Semantic plan bindings and fail-closed approval contracts."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from planning_fixtures import managed_spec
from planning_contract import (ContractError, build_contexts, build_manifest,
                               normalize_asset_paths, validate_spec,
                               require_policy_approval, require_plan_approval,
                               load_managed_spec, require_legacy_allowed)


def reordered(value):
    if isinstance(value, dict):
        return {k: reordered(v) for k, v in reversed(list(value.items()))}
    if isinstance(value, list):
        return [reordered(v) for v in value]
    return value


def ledger_for(manifest):
    return {
        "workflow_version": 2,
        "events": [{"id": "fixture-user-1", "actor": "user",
                    "scopes": ["visual", "talk", "policy"],
                    "evidence": "SYNTHETIC TEST approval, not a real user decision",
                    "timestamp": "2026-10-15T00:00:00Z"}],
        "policy": {"value": manifest["policy"]["review_policy"],
                   "output_profile": manifest["policy"]["output_profile"],
                   "landing_title": manifest["policy"]["landing_title"],
                   "policy_hash": manifest["policy_hash"], "event_id": "fixture-user-1"},
        "slides": {sid: dict(binding, event_id="fixture-user-1")
                   for sid, binding in manifest["slides"].items()},
        "samples": {}, "extra_repairs": {},
        "calibration": {"strategy_hash":manifest["calibration_hash"],"event_id":"fixture-user-1"},
    }


class PlanningContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.spec = managed_spec()

    def manifest(self, spec=None):
        return build_manifest(self.spec if spec is None else spec, self.base)

    def changed(self, mutate):
        candidate = copy.deepcopy(self.spec)
        mutate(candidate)
        return self.manifest(candidate)

    def test_dictionary_order_is_irrelevant(self):
        self.assertEqual(self.manifest(), self.manifest(reordered(self.spec)))
        self.assertEqual(build_contexts(self.spec, self.base),
                         build_contexts(reordered(self.spec), self.base))

    def test_local_change_affects_reachable_dependents_only(self):
        third = copy.deepcopy(self.spec["slides"][0])
        third["number"] = 3
        third["shared_visual_ids"] = []
        self.spec["slides"].append(third)
        before = self.manifest()
        after = self.changed(lambda s: s["slides"][0]["visible_copy"]["labels"].append("10 minutes"))
        for sid in ("slide_01", "slide_02"):
            for field in ("visual_hash", "notes_hash"):
                self.assertNotEqual(before["slides"][sid][field], after["slides"][sid][field])
        self.assertEqual(before["slides"]["slide_03"], after["slides"]["slide_03"])

    def test_unused_registry_does_not_change_render_or_talk(self):
        before = self.manifest()
        candidate = copy.deepcopy(self.spec)
        candidate["planning"]["shared_visuals"]["unused"] = {"meaning": "Unused", "appearance": "Red"}
        self.assertEqual(before["slides"], self.manifest(candidate)["slides"])
        self.assertEqual(build_contexts(self.spec, self.base)[1:],
                         build_contexts(candidate, self.base)[1:])
        self.assertNotEqual(before["plan_hash"], self.manifest(candidate)["plan_hash"])

    def test_note_only_change_leaves_render_context_valid(self):
        candidate = copy.deepcopy(self.spec)
        candidate["slides"][0]["speaker_notes"]["text"] += "\n\nLet me pause."
        self.assertEqual(build_contexts(self.spec, self.base)[1],
                         build_contexts(candidate, self.base)[1])
        before, after = self.manifest(), self.manifest(candidate)
        self.assertNotEqual(before["slides"]["slide_02"]["notes_hash"],
                            after["slides"]["slide_02"]["notes_hash"])

    def test_facts_claims_relationships_and_shared_meaning_stale_talk(self):
        mutations = [
            lambda s: s["slides"][0]["visible_copy"]["labels"].append("20 minutes"),
            lambda s: s["slides"][0]["claim_sources"][0].update(source="Different evidence"),
            lambda s: s["slides"][0]["visual_plan"].update(subject="Different subject"),
            lambda s: s["planning"]["shared_visuals"]["account"].update(meaning="Different meaning"),
        ]
        before = self.manifest()
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                after = self.changed(mutate)
                for sid in before["slides"]:
                    self.assertNotEqual(before["slides"][sid]["notes_hash"],
                                        after["slides"][sid]["notes_hash"])

    def test_style_and_layout_do_not_stale_talk(self):
        mutations = [
            lambda s: s["style"].update(typography="Different font"),
            lambda s: s["slides"][0]["visual_plan"].update(composition="Vertical"),
            lambda s: s["planning"]["shared_visuals"]["account"].update(appearance="Blue"),
        ]
        before = self.manifest()
        for mutate in mutations:
            after = self.changed(mutate)
            for sid in before["slides"]:
                self.assertEqual(before["slides"][sid]["notes_hash"], after["slides"][sid]["notes_hash"])
                self.assertNotEqual(before["slides"][sid]["visual_hash"], after["slides"][sid]["visual_hash"])

    def test_story_and_audience_change_are_global_context(self):
        before = self.manifest()
        for mutate in (
            lambda s: s["planning"].update(story="Different narrative"),
            lambda s: s["planning"]["brief"].update(audience="Operations colleagues"),
        ):
            after = self.changed(mutate)
            for sid in before["slides"]:
                self.assertNotEqual(before["slides"][sid]["visual_hash"], after["slides"][sid]["visual_hash"])
                self.assertNotEqual(before["slides"][sid]["notes_hash"], after["slides"][sid]["notes_hash"])

    def test_capacity_is_not_render_input(self):
        candidate = copy.deepcopy(self.spec)
        candidate["max_concurrent_slides"] = 1
        self.assertEqual(self.manifest()["slides"], self.manifest(candidate)["slides"])
        self.assertEqual(build_contexts(self.spec, self.base)[1], build_contexts(candidate, self.base)[1])

    def test_cycles_are_stable_reachable_context(self):
        self.spec["slides"][0]["depends_on"] = ["slide_02"]
        result = self.manifest()
        self.assertEqual(set(result["slides"]), {"slide_01", "slide_02"})
        self.assertEqual(result, self.manifest())

    def test_outside_draft_asset_identity_survives_relocation(self):
        draft, deck = self.base / "input", self.base / "deck"
        (draft / "assets").mkdir(parents=True)
        (deck / "assets").mkdir(parents=True)
        asset = draft / "assets/source.png"
        asset.write_bytes(b"hash-only source fixture")
        (deck / "assets/source.png").write_bytes(b"wrong destination")
        self.spec["slides"][0]["required_images"] = [
            {"path": "assets/source.png", "role": "Evidence", "fidelity": "Exact labels"}]
        self.spec["planning"]["shared_visuals"]["account"]["asset_path"] = "assets/source.png"
        original = copy.deepcopy(self.spec)
        canonical, provenance = normalize_asset_paths(self.spec, draft)
        self.assertEqual(self.spec, original)
        self.assertEqual(canonical["slides"][0]["required_images"][0]["path"], asset.resolve().as_posix())
        self.assertTrue(all(p["draft_root"] == draft.resolve().as_posix() for p in provenance))
        before = build_manifest(self.spec, draft)
        self.assertEqual(before, build_manifest(canonical, deck))
        asset.write_bytes(b"changed source evidence")
        after = build_manifest(canonical, deck)
        for sid in before["slides"]:
            self.assertNotEqual(before["slides"][sid], after["slides"][sid])
        asset.unlink()
        with self.assertRaises(ContractError):
            build_manifest(canonical, deck)

    def test_invalid_specs_are_rejected(self):
        mutations = [
            lambda s: s.update(workflow_version=1),
            lambda s: s.update(selected_image_backend=None),
            lambda s: s.update(aspect_ratio="1:1"),
            lambda s: s.update(goal=float("nan")),
            lambda s: s.update(slides={}),
            lambda s: s["slides"][1].update(number=1),
            lambda s: s["slides"][0].update(depends_on=["slide_99"]),
            lambda s: s["slides"][0].update(shared_visual_ids=["missing"]),
            lambda s: s["slides"][0].update(sample_approved=True),
            lambda s: s.update(approved_style_reference={}),
            lambda s: s["planning"].update(unresolved=["Need a fact"]),
            lambda s: s["slides"][0]["claim_sources"][0].update(status="needs_input"),
            lambda s: s["slides"][0]["speaker_notes"].update(speaking_time_seconds=-1),
            lambda s: s["slides"][0]["visible_copy"].update(body="not a list"),
            lambda s: s["slides"][1]["visual_plan"]["relationships"][0].update(to="unknown"),
            lambda s: s["planning"]["generation"].update(backend_used="other"),
            lambda s: s["planning"]["brief"].update(output_profile="medavis", landing_title=None),
        ]
        for mutate in mutations:
            candidate = copy.deepcopy(self.spec)
            mutate(candidate)
            with self.subTest(candidate=candidate), self.assertRaises(ContractError):
                validate_spec(candidate)

    def test_policy_binding_requires_values_and_actual_scoped_event(self):
        manifest = self.manifest()
        ledger = ledger_for(manifest)
        require_policy_approval(manifest, ledger)
        mutations = [
            lambda l: l["policy"].pop("policy_hash"),
            lambda l: l["policy"].update(output_profile="both"),
            lambda l: l["policy"].update(event_id="ghost"),
            lambda l: l["events"][0].update(actor="agent"),
            lambda l: l["events"][0].update(scopes=["visual", "talk"]),
            lambda l: l["events"][0].update(evidence=""),
            lambda l: l["events"][0].update(scopes="policy"),
        ]
        for mutate in mutations:
            candidate = copy.deepcopy(ledger)
            mutate(candidate)
            with self.subTest(candidate=candidate), self.assertRaises(ContractError):
                require_policy_approval(manifest, candidate)

    def test_policy_changes_do_not_silently_change_slide_scope(self):
        before = self.manifest()
        ledger = ledger_for(before)
        for mutate in (
            lambda s: s["planning"].update(review_policy="strict"),
            lambda s: s["planning"]["brief"].update(output_profile="medavis", landing_title="Model"),
            lambda s: s["planning"]["brief"].update(landing_title="Different title"),
        ):
            after = self.changed(mutate)
            self.assertEqual(before["slides"], after["slides"])
            with self.assertRaises(ContractError):
                require_policy_approval(after, ledger)

    def test_plan_gate_refuses_missing_stale_and_agent_decisions(self):
        manifest = self.manifest()
        ledger = ledger_for(manifest)
        self.base.joinpath("plan_approvals.json").write_text(json.dumps(ledger), encoding="utf-8")
        require_plan_approval(self.base, manifest, ["slide_01", "slide_02"])
        ledger["slides"]["slide_01"]["notes_hash"] = "stale"
        self.base.joinpath("plan_approvals.json").write_text(json.dumps(ledger), encoding="utf-8")
        with self.assertRaises(ContractError):
            require_plan_approval(self.base, manifest, ["slide_01"])

    def test_no_implicit_legacy_fallback(self):
        with self.assertRaises(ContractError):
            load_managed_spec(self.base)
        require_legacy_allowed(self.base)
        self.base.joinpath("deck_spec.json").write_text(json.dumps(self.spec), encoding="utf-8")
        with self.assertRaises(ContractError):
            require_legacy_allowed(self.base)
        self.base.joinpath("deck_spec.json").write_text("{", encoding="utf-8")
        with self.assertRaises(ContractError):
            require_legacy_allowed(self.base)

