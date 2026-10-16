"""Portable skill discovery, links and full verbatim speaking guidance."""
import hashlib
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[2]


class SkillContractTests(unittest.TestCase):
    def test_frontmatter_is_trigger_only_codex_skill_contract(self):
        text=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        front=text.split("---",2)[1]
        keys=re.findall(r"^([A-Za-z_]+):",front,re.M)
        self.assertEqual(keys,["name","description"])
        name=re.search(r"^name: (.+)$",front,re.M).group(1)
        self.assertRegex(name,r"^[a-zA-Z0-9-]{1,64}$")
        description=re.search(r"^description: (.+)$",front,re.M).group(1)
        self.assertTrue(description.startswith("Use when a user"))
        self.assertLessEqual(len(description),1024)
        for word in ("PowerPoint","PPTX","notes","topic"):
            self.assertIn(word,description)

    def test_complete_voice_guidance_examples_are_portable_and_unchanged(self):
        text=(ROOT/"docs/speaker-notes-style.md").read_text(encoding="utf-8")
        body=text.split("<!-- BEGIN VOICE REFERENCE -->",1)[1].split("<!-- END VOICE REFERENCE -->",1)[0].strip()
        self.assertEqual(hashlib.sha256(body.encode("utf-8")).hexdigest(),"f50bce332df057b51ad6da7ba9251369ea0534c61c4bc64e44193465b2b04dde")

    def test_local_guides_resolve_inside_the_distributable_skill(self):
        entry=(ROOT/"SKILL.md").read_text(encoding="utf-8")
        self.assertIn("docs/content-planning-and-approval.md",entry)
        self.assertIn("docs/speaker-notes-style.md",entry)
        for path in [ROOT/"SKILL.md",*(ROOT/"docs").glob("*.md"),*(ROOT/"prompts").glob("*.md")]:
            text=path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)]+)\)",text):
                if target.startswith(("http://","https://","#")):
                    continue
                target=target.split("#")[0]
                resolved=(path.parent/target).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT.resolve()),(path,target))
                self.assertTrue(resolved.is_file(),(path,target))
