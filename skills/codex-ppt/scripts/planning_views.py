#!/usr/bin/env python3
"""Produce readable draft or approved views of the canonical deck plan."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from planning_contract import (ContractError,build_manifest,load_managed_spec,normalize_asset_paths,
                               planning_lock,read_contract_json,require_plan_approval,validate_spec)
from slide_run_state import write_json


def speech_markdown(spec: dict) -> str:
    blocks=[]
    for slide in spec["slides"]:
        text=slide["speaker_notes"]["text"].replace("\r\n","\n").strip()
        blocks.append(f"## Slide {slide['number']}: {slide['title']}\n\n{text}")
    return "\n\n".join(blocks)+"\n"


def outline_markdown(spec: dict, draft: bool = False) -> str:
    p=spec["planning"]
    lines=["# Deck plan"+(" — draft" if draft else ""),""]
    lines += [f"- {k}: {v}" for k,v in p["brief"].items()]
    lines += ["",f"Story: {p['story']}",f"Input readiness: {json.dumps(p['readiness'],ensure_ascii=False)}",
              f"Review: {p['review_policy']}",f"Shared identities: {json.dumps(p['shared_visuals'],ensure_ascii=False)}",""]
    for s in spec["slides"]:
        lines += [f"## Slide {s['number']}: {s['title']}","",
                  f"Purpose ({s['role']}): {s['intent']}",
                  "Exact visible copy: "+json.dumps(s["visible_copy"],ensure_ascii=False),
                  "Visual: "+json.dumps(s["visual_plan"],ensure_ascii=False),
                  "Sources / proposals: "+json.dumps(s["claim_sources"],ensure_ascii=False),
                  "Source assets: "+json.dumps(s["required_images"],ensure_ascii=False),
                  "Shared elements: "+", ".join(s["shared_visual_ids"]),
                  "Depends on: "+", ".join(s["depends_on"]),
                  f"Spoken time: {s['speaker_notes']['speaking_time_seconds']} seconds",
                  f"Transition: {s['speaker_notes']['transition']}",""]
    lines += ["Unresolved: "+json.dumps(p["unresolved"],ensure_ascii=False),""]
    return "\n".join(lines)


def write_views(deck: Path,spec: dict,draft: bool=False) -> None:
    from record_plan_approval import atomic_bytes
    suffix=".draft" if draft else ""
    atomic_bytes(deck/f"outline{suffix}.md",outline_markdown(spec,draft).encode("utf-8"))
    atomic_bytes(deck/f"speech{suffix}.md",speech_markdown(spec).encode("utf-8"))


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--spec")
    parser.add_argument("--deck",required=True)
    parser.add_argument("--draft",action="store_true")
    args=parser.parse_args()
    deck=Path(args.deck).resolve()
    try:
        if args.draft:
            if not args.spec:
                raise ContractError("Draft views require --spec")
            path=Path(args.spec).resolve()
            source=read_contract_json(path,"draft spec")
            validate_spec(source)
            spec,provenance=normalize_asset_paths(source,path.parent)
            manifest=build_manifest(spec,deck)
            deck.mkdir(parents=True,exist_ok=True)
            with planning_lock(deck):
                write_views(deck,spec,True)
        else:
            with planning_lock(deck):
                spec=load_managed_spec(deck)
                manifest=build_manifest(spec,deck)
                require_plan_approval(deck,manifest,list(manifest["slides"]))
                provenance=[]
                write_views(deck,spec)
        print(json.dumps({"plan_hash":manifest["plan_hash"],"asset_provenance":provenance,
                          "draft":args.draft},ensure_ascii=False))
        return 0
    except (ContractError,OSError) as exc:
        parser.exit(1,f"Error: {exc}\n")


if __name__=="__main__":
    raise SystemExit(main())
