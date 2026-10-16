"""Regression cases for native selection, retired ratios and execution evidence."""
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from planning_fixtures import managed_spec, compile_fixture, dispatch_fixture, fixture_image, run_cli


class BackendCapabilityContractTests(unittest.TestCase):
    def test_supported_ratio_set_and_removed_template(self):
        from slide_image_ratio import RATIO_BY_LABEL
        self.assertEqual(set(RATIO_BY_LABEL), {"16:9", "4:3"})
        self.assertFalse((SCRIPTS.parent / "assets/templates/medavis_ppt_template_2026_en_3-2.pptx").exists())

    def test_new_template_uses_supported_ratio(self):
        from prepare_slide_prompts import _write_template
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)/"draft.json"
            _write_template(path)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8'))["aspect_ratio"], "16:9")

    def test_new_jobs_always_have_compiler_owned_version_and_explicit_ratio(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp)
            compile_fixture(deck)
            jobs = json.loads((deck/"slide_jobs.json").read_text(encoding='utf-8'))
            job = json.loads((deck/"prompts/slide_01.json").read_text(encoding='utf-8'))
            self.assertEqual(jobs.get("execution_contract_version"), 1)
            self.assertEqual(job.get("execution_contract_version"), 1)
            self.assertIn("16:9", job["prompt"])

    def test_result_without_submission_evidence_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            deck = Path(tmp)
            compile_fixture(deck)
            self.assertEqual(dispatch_fixture(deck).returncode, 0)
            candidate = deck/"candidate-final.png"
            fixture_image(candidate)
            result = run_cli("record_slide_result.py", deck, "--slide", "1",
                "--agent-id", "fixture-agent", "--backend-used", "scripts/image_gen.py",
                "--selected-source", candidate, "--qa-note", "synthetic inspection")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("submission", (result.stdout+result.stderr).lower())

    def test_native_execution_needs_no_api_model_or_size(self):
        from generation_execution import execution_contract
        config = {"mode":"generate", "backend_used":"image_gen", "tool_name":"image_gen",
                  "aspect_ratio":"16:9", "output_requirements":{"min_width":100}}
        result = execution_contract(config, [], "image_gen")
        self.assertEqual(result["parameters"], {})


if __name__ == "__main__":
    unittest.main()
