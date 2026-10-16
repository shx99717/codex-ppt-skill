"""Capabilities belong to a selected provider/model/operation, never a substring."""
import os
from pathlib import Path
import sys
import unittest
import json
import tempfile
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from image_capabilities import resolve_model, validate_capabilities


def profile():
    return {"model":"provider/future-v3", "provider_base_url":"https://api.example/v1",
        "operations":{"edit":{"supports_image_inputs":True,"qualities":["max"],
            "source":"https://api.example/docs","checked_on":"2026-10-16"}}}


class ImageCapabilitiesTests(unittest.TestCase):
    def test_no_hidden_default_and_explicit_precedence(self):
        with self.assertRaises(ValueError): resolve_model(None, None)
        self.assertEqual(resolve_model("explicit", "configured"), "explicit")
        self.assertEqual(resolve_model(None, "configured"), "configured")

    def test_bound_profile_supports_selected_future_model(self):
        validate_capabilities(profile(), "provider/future-v3", "https://api.example/v1/", "edit", {"quality":"max"}, True)

    def test_mismatch_and_unknown_block_managed(self):
        for model,operation in (("other", "edit"),("provider/future-v3", "generate")):
            with self.assertRaises(ValueError):
                validate_capabilities(profile(), model, "https://api.example/v1", operation, {"quality":"max"}, operation=="edit")
        with self.assertRaises(ValueError):
            validate_capabilities(None, "future", None, "edit", {}, True)

    def test_standalone_unknown_is_deferred_but_known_unsupported_fails(self):
        validate_capabilities(None, "future", None, "generate", {"quality":"max"}, False, managed=False)
        with self.assertRaises(ValueError):
            validate_capabilities(profile(), "provider/future-v3", "https://api.example/v1", "edit", {"quality":"low"}, True, managed=False)

    def test_managed_provider_is_resolved_from_runtime_env_before_validation(self):
        import image_gen
        from generation_execution import execution_contract
        facts=profile()
        facts["operations"]["edit"]["size_constraints"]={"multiple":1,"max_edge":1000,"min_pixels":1,"max_pixels":1000000,"max_ratio":3}
        config={"mode":"generate","reference_mode":"edit","model":facts["model"],"quality":"max",
            "size":"160x90","aspect_ratio":"16:9","capabilities":facts}
        with tempfile.TemporaryDirectory() as tmp:
            envfile=Path(tmp)/".env"
            envfile.write_text("OPENAI_BASE_URL=https://api.example/v1\n",encoding="utf-8")
            with patch.dict(os.environ,{},clear=True),patch.object(image_gen,"_runtime_env_path",return_value=envfile):
                execution_contract(config,[{}],"scripts/image_gen.py")

    def test_batch_supported_overrides_replace_unused_defaults(self):
        import image_gen
        facts=profile();facts["operations"]["generate"]={"qualities":["max"],
            "size_constraints":{"max_edge":1000,"multiple":1,"min_pixels":1,"max_pixels":1000000,"max_ratio":3},
            "source":"https://api.example/docs","checked_on":"2026-10-16"}
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);cap=directory/"cap.json";cap.write_text(json.dumps(facts))
            jobs=directory/"jobs.jsonl"
            jobs.write_text(json.dumps({"prompt":"synthetic","quality":"max","size":"160x90"})+"\n")
            argv=["image_gen.py","generate-batch","--model",facts["model"],"--capabilities-file",str(cap),
                "--input",str(jobs),"--out-dir",str(directory/"out"),"--dry-run"]
            with patch.dict(os.environ,{"OPENAI_BASE_URL":"https://api.example/v1"}),patch.object(sys,"argv",argv),patch.object(image_gen,"create_image_provider") as provider:
                self.assertEqual(image_gen.main(),0)
                provider.assert_not_called()

    def test_batch_overrides_are_validated_before_provider(self):
        import image_gen
        facts=profile();facts["operations"]["generate"]={"qualities":["medium"],
            "size_constraints":{"max_edge":3840,"multiple":1,"min_pixels":100000,"max_pixels":8294400,"max_ratio":3},
            "supports_transparency":False,"source":"https://api.example/docs","checked_on":"2026-10-16"}
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);cap=directory/"cap.json";cap.write_text(json.dumps(facts))
            jobs=directory/"jobs.jsonl"
            for override in ({"model":"wrong"},{"quality":"low"},{"size":"32x18"},{"background":"transparent"}):
                jobs.write_text(json.dumps({"prompt":"synthetic",**override})+"\n")
                argv=["image_gen.py","generate-batch","--model",facts["model"],"--size","1600x900","--quality","medium",
                    "--capabilities-file",str(cap),"--input",str(jobs),"--out-dir",str(directory/"out"),"--dry-run"]
                with self.subTest(override=override),patch.dict(os.environ,{"OPENAI_BASE_URL":"https://api.example/v1"}),patch.object(sys,"argv",argv),patch.object(image_gen,"create_image_provider") as provider:
                    with self.assertRaises((ValueError,SystemExit)):image_gen.main()
                    provider.assert_not_called()
