"""No network: exercise real CLI edit through fake SDK/HTTP transports."""
import base64
import io
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch
from contextlib import redirect_stdout
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import image_gen
from image_providers.openai_compatible import OpenAICompatibleImageProvider
from image_providers.atlascloud import AtlasCloudImageProvider,atlascloud_model_for_operation
from planning_fixtures import fixture_image


class ProviderInputBoundaryTests(unittest.TestCase):
    def test_explicit_atlas_routes_are_preserved_and_wrong_operation_rejected(self):
        self.assertEqual(atlascloud_model_for_operation("vendor/exact-route","edit"),"vendor/exact-route")
        self.assertEqual(atlascloud_model_for_operation("vendor/documented/edit","edit"),"vendor/documented/edit")
        with self.assertRaises(ValueError):atlascloud_model_for_operation("vendor/documented/text-to-image","edit")

    def test_atlas_unsupported_settings_fail_before_transport(self):
        transport=unittest.mock.Mock()
        provider=AtlasCloudImageProvider(api_key="synthetic",base_url=None,urlopen=transport)
        for key in ("background","input_fidelity","output_compression","moderation"):
            with self.subTest(key=key),self.assertRaises(ValueError):
                provider.generate({"model":"vendor/exact-route","prompt":"synthetic",key:"explicit"})
        transport.assert_not_called()

    def test_cli_edit_sends_every_ordered_image_to_sdk_and_http(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory=Path(tmp);images=[directory/"a.png",directory/"b.png"]
            fixture_image(images[0],"red");fixture_image(images[1],"blue")
            expected=[p.read_bytes() for p in images];encoded=base64.b64encode(expected[0]).decode()
            profile=directory/"capabilities.json"
            profile.write_text(json.dumps({"model":"vendor/exact-route","provider_base_url":"https://api.openai.com/v1",
                "operations":{"edit":{"supports_image_inputs":True,"qualities":["medium"],
                "size_constraints":{"max_edge":3840,"multiple":16,"min_pixels":655360,"max_pixels":8294400,"max_ratio":3},
                "source":"https://example.invalid/synthetic","checked_on":"2026-10-16"}}}))
            captured=[]
            def sdk_edit(**payload):
                captured.append([handle.read() for handle in payload["image"]])
                self.assertNotIn("capabilities",payload)
                return SimpleNamespace(data=[SimpleNamespace(b64_json=encoded)])
            sdk=OpenAICompatibleImageProvider(api_key="synthetic",base_url=None,
                client_factory=lambda:SimpleNamespace(images=SimpleNamespace(edit=sdk_edit)))
            class Response:
                def __init__(self,obj):self.obj=obj
                def __enter__(self):return self
                def __exit__(self,*args):pass
                def read(self):return json.dumps(self.obj).encode()
            def http(request,**kwargs):
                if request.method=="POST":
                    body=json.loads(request.data)
                    self.assertEqual(body["model"],"vendor/exact-route")
                    self.assertNotIn("capabilities",body)
                    captured.append([base64.b64decode(v.split(",",1)[1]) for v in body["images"]])
                    return Response({"id":"synthetic-prediction"})
                return Response({"status":"completed","outputs":["data:image/png;base64,"+encoded]})
            atlas=AtlasCloudImageProvider(api_key="synthetic",base_url=None,urlopen=http)
            for index,provider in enumerate((sdk,atlas)):
                argv=["image_gen.py","edit","--prompt","synthetic","--model","vendor/exact-route","--out",str(directory/f"out{index}.png"),"--capabilities-file",str(profile)]
                for path in images:argv += ["--image",str(path)]
                with patch.dict(os.environ,{"OPENAI_API_KEY":"synthetic-not-real","OPENAI_BASE_URL":"https://api.openai.com/v1","CODEX_PPT_HOME":str(directory)}),patch.object(image_gen,"create_image_provider",return_value=provider),patch.object(sys,"argv",argv),redirect_stdout(io.StringIO()):
                    image_gen.main()
            self.assertEqual(captured,[expected,expected])
