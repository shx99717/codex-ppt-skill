"""Compiled image prompts obey exactly the scoped visual projection."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
SCRIPTS=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(SCRIPTS))
from planning_contract import build_contexts,build_manifest
from planning_fixtures import managed_spec
from prepare_slide_prompts import approved_prompt_blocks


def reverse(value):
    if isinstance(value,dict):
        return {k:reverse(v) for k,v in reversed(list(value.items()))}
    if isinstance(value,list):
        return [reverse(v) for v in value]
    return value


class PromptContractTests(unittest.TestCase):
    def test_prompt_is_exact_filtered_context_with_order_invariance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            spec=managed_spec()
            context=build_contexts(spec,root)[1]["slide_02"]
            before=approved_prompt_blocks(context)
            self.assertEqual(before,approved_prompt_blocks(build_contexts(reverse(spec),root)[1]["slide_02"]))
            changed=copy.deepcopy(spec)
            changed["planning"]["shared_visuals"]["unused"]={"meaning":"Unrelated","appearance":"Red"}
            changed["slides"][0]["speaker_notes"]["text"]+="Never put this talk in image instructions"
            self.assertEqual(before,approved_prompt_blocks(build_contexts(changed,root)[1]["slide_02"]))
            self.assertNotIn("Never put this",before)
            changed["slides"][0]["visible_copy"]["labels"].append("Exact 10")
            self.assertNotEqual(before,approved_prompt_blocks(build_contexts(changed,root)[1]["slide_02"]))
            self.assertIn("Exact 10",approved_prompt_blocks(build_contexts(changed,root)[1]["slide_02"]))
