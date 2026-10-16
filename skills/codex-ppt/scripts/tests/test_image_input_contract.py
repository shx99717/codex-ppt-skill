import copy
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from image_input_contract import make_receipt, validate_receipt
from planning_fixtures import fixture_image


class InputContractTests(unittest.TestCase):
    def test_order_attempt_candidate_and_trust_are_bound(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"candidate.png";fixture_image(path)
            job={"expected_backend":"image_gen","execution":{"operation":"generate"},"input_images":[]}
            slide={"job_sha256":"abc","dispatch":{"attempt_id":"attempt","agent_id":"agent"}}
            receipt=make_receipt(job,slide,path,"referenced_image_paths")
            self.assertEqual(validate_receipt(receipt,job,slide,path),"agent_reported")
            for field,value in (("attempt_id","other"),("evidence_origin","adapter_verified")):
                bad=copy.deepcopy(receipt);bad[field]=value
                with self.assertRaises(ValueError): validate_receipt(bad,job,slide,path)
            fixture_image(path,"blue")
            with self.assertRaises(ValueError):validate_receipt(receipt,job,slide,path)
