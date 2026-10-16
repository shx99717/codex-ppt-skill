import tempfile
from pathlib import Path
import sys
import unittest
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from image_input_contract import measured_output


class OutputRequirementsTests(unittest.TestCase):
    def test_invalid_policy_fails_during_compilation_before_generation(self):
        from generation_execution import execution_contract
        for invalid in ({"min_width":False},{"min_height":0},{"unknown":2},[],"4K"):
            with self.subTest(policy=invalid),self.assertRaises(ValueError):
                execution_contract({"mode":"generate","output_requirements":invalid},[],"image_gen")

    def test_measured_pixels_not_prompt_and_no_rewrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"image.png"
            Image.new("RGB", (1672,941)).save(path)
            before=path.read_bytes()
            self.assertEqual(measured_output(path,"16:9",{})["measured_width"],1672)
            with self.assertRaises(ValueError): measured_output(path,"16:9",{"exact_width":3840,"exact_height":2160})
            with self.assertRaises(ValueError): measured_output(path,"16:9",{"min_width":2000})
            self.assertEqual(before,path.read_bytes())
            with self.assertRaises(ValueError): measured_output(path,"16:9",{"min_width":True})
