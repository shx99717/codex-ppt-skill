#!/usr/bin/env python3
"""Record a transcribed actual user decision against a reviewed managed plan."""
from __future__ import annotations
import argparse
import copy
import json
import os
from pathlib import Path
import shutil
import tempfile
import uuid
from planning_contract import (ContractError,approval_event,build_manifest,digest,file_digest,
    load_ledger,load_managed_spec,normalize_asset_paths,planning_lock,read_contract_json,
    require_plan_approval,selection,slide_id,validate_spec,validate_plan_records)
from slide_run_state import now_iso,write_json
from slide_image_ratio import RATIO_BY_LABEL,require_image_ratio


def atomic_bytes(path: Path, body: bytes) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(prefix=f".{path.name}.",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as stream:
            stream.write(body)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name,path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def snapshot_file(source: Path,target: Path,expected: str) -> None:
    if file_digest(source)!=expected:
        raise ContractError("Source changed before snapshot")
    if target.exists():
        if file_digest(target)!=expected:
            raise ContractError("Immutable snapshot was modified")
    else:
        atomic_bytes(target,source.read_bytes())
    if file_digest(target)!=expected or file_digest(source)!=expected:
        raise ContractError("Source changed during snapshot")


def snapshot_assets(deck: Path,provenance: list[dict]) -> dict:
    snapshots={}
    for item in provenance:
        original=Path(item["source_path"])
        suffix=original.suffix.lower() or ".bin"
        reference=f"references/sources/{item['sha256']}{suffix}"
        snapshot_file(original,deck/reference,item["sha256"])
        snapshots[item["source_path"]]={"path":reference,"sha256":item["sha256"]}
    return snapshots


def user_event(evidence: str,scopes: list[str],**extra) -> dict:
    if not isinstance(evidence,str) or not evidence.strip():
        raise ContractError("Actual user decision evidence is required")
    return dict(id=str(uuid.uuid4()),actor="user",evidence=evidence.strip(),
                scopes=scopes,timestamp=now_iso(),**extra)


def empty_ledger() -> dict:
    return {"workflow_version":2,"events":[],"slides":{},"samples":{},"extra_repairs":{},"assets":{}}


def atomic_group(deck: Path,payload: dict[str,bytes]) -> None:
    before={name:(deck/name).read_bytes() if (deck/name).exists() else None for name in payload}
    marker=deck/".planning_transaction.json"
    write_json(marker,{"files":list(payload),"started_at":now_iso()})
    try:
        for name,body in payload.items():
            atomic_bytes(deck/name,body)
    except BaseException:
        for name,body in before.items():
            path=deck/name
            if body is None:
                path.unlink(missing_ok=True)
            else:
                atomic_bytes(path,body)
        marker.unlink(missing_ok=True)
        raise
    marker.unlink()

def install_plan(deck: Path,spec: dict,ledger: dict) -> None:
    from planning_views import outline_markdown,speech_markdown
    manifest=build_manifest(spec,deck)
    try:
        validate_plan_records(manifest,ledger,list(manifest["slides"]))
        suffix=""
    except ContractError:
        suffix=".draft"
    payload={
        "deck_spec.json":(json.dumps(spec,ensure_ascii=False,indent=2)+"\n").encode("utf-8"),
        "plan_approvals.json":(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n").encode("utf-8"),
        f"outline{suffix}.md":outline_markdown(spec,bool(suffix)).encode("utf-8"),
        f"speech{suffix}.md":speech_markdown(spec).encode("utf-8"),
    }
    atomic_group(deck,payload)


def record_plan(deck: Path,draft: Path,*,scope: str,slides: str|None,
                approve_policy: bool,expected_plan_hash: str,evidence: str) -> dict:
    with planning_lock(deck):
        source=read_contract_json(draft,"draft spec")
        validate_spec(source)
        spec,provenance=normalize_asset_paths(source,draft.parent)
        manifest=build_manifest(spec,deck)
        if manifest["plan_hash"]!=expected_plan_hash:
            raise ContractError("Reviewed plan hash changed; review current content/assets")
        ids=list(manifest["slides"])
        chosen=selection(slides,ids) if scope=="slides" else ids if scope=="all" else []
        if scope=="slides" and not slides:
            raise ContractError("Slide-scoped approval requires --slides")
        scopes=(["visual","talk"] if chosen else [])+(["policy"] if approve_policy else [])
        event=user_event(evidence,scopes,slide_ids=chosen,asset_provenance=provenance,
                         reviewed_plan_hash=manifest["plan_hash"])
        ledger=load_ledger(deck) if (deck/"plan_approvals.json").exists() else empty_ledger()
        ledger=copy.deepcopy(ledger)
        assets=snapshot_assets(deck,provenance)
        if build_manifest(spec,deck)!=manifest:
            raise ContractError("Source changed during approval recording")
        ledger["assets"]=dict(ledger.get("assets",{}),**assets)
        ledger["events"].append(event)
        if scope=="all" and (ledger.get("calibration") or {}).get("strategy_hash")!=manifest["calibration_hash"]:
            ledger["calibration"]={"strategy_hash":manifest["calibration_hash"],"event_id":event["id"]}
        for sid in chosen:
            previous=ledger["slides"].get(sid,{})
            record=dict(previous)
            for field,kind in (("visual_hash","visual"),("notes_hash","talk")):
                if previous.get(field)!=manifest["slides"][sid][field]:
                    record[field]=manifest["slides"][sid][field]
                    record[f"{kind}_event_id"]=event["id"]
                else:
                    record.setdefault(f"{kind}_event_id",previous.get("event_id"))
            ledger["slides"][sid]=record
        if approve_policy:
            previous=ledger.get("policy",{})
            if previous.get("policy_hash")!=manifest["policy_hash"]:
                ledger["policy"]={"value":manifest["policy"]["review_policy"],
                    "output_profile":manifest["policy"]["output_profile"],
                    "landing_title":manifest["policy"]["landing_title"],
                    "policy_hash":manifest["policy_hash"],"event_id":event["id"]}
        install_plan(deck,spec,ledger)
        return {"event_id":event["id"],"plan_hash":manifest["plan_hash"],"slides":chosen,"scopes":scopes}


def record_sample(deck: Path,sid: str,image: Path,backend: str,evidence: str,
                  style_only: bool=False) -> dict:
    with planning_lock(deck):
        spec=load_managed_spec(deck)
        manifest=build_manifest(spec,deck)
        sid=selection(sid,list(manifest["slides"]))[0]
        ledger=require_plan_approval(deck,manifest,list(manifest["slides"]))
        if backend!=spec["selected_image_backend"]:
            raise ContractError("Sample backend conflicts with approved generation configuration")
        require_image_ratio(str(image),RATIO_BY_LABEL[spec["aspect_ratio"]],spec["aspect_ratio"])
        sha=file_digest(image)
        event=user_event(evidence,["sample"],slide_ids=[sid])
        reference=f"references/approved_samples/{sha}.png"
        snapshot_file(image,deck/reference,sha)
        by_id={slide_id(s):s for s in spec["slides"]}
        record={"image":reference,"image_sha256":sha,"style_hash":manifest["style_hash"],
                "visual_family":by_id[sid]["visual_plan"]["type"],"backend":backend,
                "aspect_ratio":spec["aspect_ratio"],"event_id":event["id"]}
        if not style_only:
            final=f"origin_image/{sid}.png"
            # This explicit sample decision accepts that slide's content as well.
            atomic_bytes(deck/final,(deck/reference).read_bytes())
            record["accepted_final"]={"path":final,"image_sha256":sha,
                                      "visual_hash":manifest["slides"][sid]["visual_hash"]}
        ledger["events"].append(event)
        ledger["samples"][sid]=record
        write_json(deck/"plan_approvals.json",ledger)
        return {"event_id":event["id"],"slide_id":sid,"sample":record}


def authorize_repair(deck: Path,sid: str,count: int,evidence: str) -> dict:
    if count<1:
        raise ContractError("Additional attempts must be positive")
    with planning_lock(deck):
        spec=load_managed_spec(deck)
        manifest=build_manifest(spec,deck)
        sid=selection(sid,list(manifest["slides"]))[0]
        ledger=require_plan_approval(deck,manifest,[sid])
        event=user_event(evidence,["repair"],slide_ids=[sid],additional_attempts=count,
                         visual_hash=manifest["slides"][sid]["visual_hash"])
        ledger["events"].append(event)
        ledger["extra_repairs"].setdefault(sid,[]).append({
            "event_id":event["id"],"visual_hash":event["visual_hash"],"attempts":count})
        write_json(deck/"plan_approvals.json",ledger)
        return {"event_id":event["id"],"slide_id":sid,"additional_attempts":count}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck")
    parser.add_argument("--spec")
    parser.add_argument("--approve",action="store_true")
    parser.add_argument("--approve-policy",action="store_true")
    parser.add_argument("--scope",choices=["all","slides"],default="all")
    parser.add_argument("--slides")
    parser.add_argument("--expected-plan-hash")
    parser.add_argument("--approve-sample")
    parser.add_argument("--image")
    parser.add_argument("--backend-used")
    parser.add_argument("--style-only",action="store_true")
    parser.add_argument("--authorize-repair")
    parser.add_argument("--additional-attempts",type=int,default=1)
    parser.add_argument("--evidence",required=True)
    args=parser.parse_args()
    deck=Path(args.deck).resolve()
    try:
        actions=int(bool(args.approve or args.approve_policy))+int(bool(args.approve_sample))+int(bool(args.authorize_repair))
        if actions!=1:
            raise ContractError("Choose exactly one decision group")
        if args.approve or args.approve_policy:
            if not args.spec or not args.expected_plan_hash:
                raise ContractError("Plan/policy approval requires reviewed --spec and --expected-plan-hash")
            summary=record_plan(deck,Path(args.spec).resolve(),
                scope=args.scope if args.approve else "policy",slides=args.slides,
                approve_policy=args.approve_policy or (args.approve and args.scope=="all"),
                expected_plan_hash=args.expected_plan_hash,evidence=args.evidence)
        elif args.approve_sample:
            if not args.image or not args.backend_used:
                raise ContractError("Sample approval requires --image and --backend-used")
            summary=record_sample(deck,args.approve_sample,Path(args.image).resolve(),
                                  args.backend_used,args.evidence,args.style_only)
        else:
            summary=authorize_repair(deck,args.authorize_repair,args.additional_attempts,args.evidence)
        print(json.dumps(summary,ensure_ascii=False))
        return 0
    except (ContractError,OSError,ValueError) as exc:
        parser.exit(1,f"Error: {exc}\n")


if __name__=="__main__":
    raise SystemExit(main())
