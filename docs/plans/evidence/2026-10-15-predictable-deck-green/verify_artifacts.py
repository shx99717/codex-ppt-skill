"""Recheck portable/source/link/archive evidence without a live model call."""
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent


def body(path,marker):
    text=path.read_text(encoding="utf-8")
    return text.split(f"<!-- BEGIN {marker} -->",1)[1].split(f"<!-- END {marker} -->",1)[0].strip()


def sha(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


source=body(ROOT/"docs/memory/memory-20261014-predictable-ppt-generation/speaker-notes-style-reference.md","VERBATIM USER INPUT")
appendix=body(ROOT/"docs/plans/2026-10-14-predictable-deck-generation-handoff.md","ORIGINAL SPEAKER-NOTES MESSAGE")
voice=body(ROOT/"skills/codex-ppt/docs/speaker-notes-style.md","VOICE REFERENCE")
assert source==appendix
assert len(source)==3873 and sha(source)=="9a1a64e2825cdc729fe13ccb3207f8ffbf6703ce206bec190c2077a5998a9980"
assert sha(voice)=="f50bce332df057b51ad6da7ba9251369ea0534c61c4bc64e44193465b2b04dde"

baseline=ROOT/"docs/plans/evidence/2026-10-14-predictable-deck-baseline"
meta=json.loads((baseline/"metadata.json").read_text(encoding="utf-8"))
runner_count=0
for item in meta["runners_and_audits"].values():
    assert sha(item["content"])==item["sha256"]
    runner_count+=1
archived=0
for case in meta["case_ids"]:
    data=json.loads((baseline/(case+".json")).read_text(encoding="utf-8"))
    for item in data["artifacts"].values():
        assert sha(item["content"])==item["sha256"],case
        archived+=1
assert archived==114

skill=ROOT/"skills/codex-ppt"
pages=[skill/"SKILL.md",*(skill/"docs").glob("*.md"),*(skill/"prompts").glob("*.md"),
       *(ROOT/"tests/smoke-deck").glob("*.md"),*(ROOT).glob("README*.md")]
for locale in ("","en/","ko/"):
    pages.extend(ROOT/("docs/"+locale+name+".md") for name in
                 ("README","design","faq","prompts","quickstart","workflow"))
links=0
for page in pages:
    text=re.sub(r"```.*?```","",page.read_text(encoding="utf-8"),flags=re.S)
    for target in re.findall(r"\]\(([^)]+)\)",text):
        if target.startswith(("https://","http://","#","mailto:")):
            continue
        target=unquote(target.split("#",1)[0].strip("<>"))
        resolved=(ROOT/"docs"/target.lstrip("/")) if target.startswith("/") else page.parent/target
        assert resolved.is_file(),(str(page.relative_to(ROOT)),target)
        if page.is_relative_to(skill):
            assert resolved.resolve().is_relative_to(skill.resolve())
        links+=1

report={"original_source_chars":len(source),"original_source_sha256":sha(source),
        "appendix_exact_equal":True,"portable_voice_sha256":sha(voice),
        "baseline_original_byte_hashes_verified":archived,"markdown_local_links_checked":links,
        "baseline_runner_and_audit_hashes_verified":runner_count,
        "remote_urls_and_fragment_rendering_tested":False}
(HERE/"artifact-verification.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report))
