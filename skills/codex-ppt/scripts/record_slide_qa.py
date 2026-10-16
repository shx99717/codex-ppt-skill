#!/usr/bin/env python3
"""Record agent inspection separately from actual user image acceptance."""
from __future__ import annotations
import argparse
import json
import uuid
from planning_contract import (ContractError,build_manifest,consumer_lock,file_digest,inside_path,
    load_managed_spec,qa_is_current,require_job_current,require_plan_approval,sequence_binding)
from slide_run_state import deck_dir_from_target,find_slide,locked_jobs,now_iso,load_jobs,sync_user_review_run_state


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck")
    parser.add_argument("--slide")
    decisions=parser.add_mutually_exclusive_group(required=True)
    decisions.add_argument("--pass",dest="passed",action="store_true")
    decisions.add_argument("--needs-repair",action="store_true")
    decisions.add_argument("--blocked",action="store_true")
    decisions.add_argument("--deck-pass",action="store_true")
    parser.add_argument("--evidence",required=True)
    args=parser.parse_args()
    deck=deck_dir_from_target(args.deck)
    if not args.evidence.strip():
        parser.exit(1,"Agent QA evidence is required\n")
    with consumer_lock(deck),locked_jobs(deck) as jobs:
        spec=load_managed_spec(deck)
        manifest=build_manifest(spec,deck)
        if args.deck_pass:
            require_plan_approval(deck,manifest,list(manifest["slides"]))
            by_id={s["slide_id"]:s for s in jobs["slides"]}
            if set(by_id)!=set(manifest["slides"]):
                raise ContractError("Missing expected sequence slides")
            for sid,slide in by_id.items():
                require_job_current(deck,jobs,slide)
                if slide.get("status") not in {"recorded","accepted"} or not qa_is_current(deck,slide,manifest):
                    raise ContractError(f"Current per-slide QA required before deck QA: {sid}")
            jobs["deck_qa"]={"actor":"agent","status":"passed","binding":sequence_binding(deck,jobs,manifest),
                             "evidence":args.evidence,"timestamp":now_iso()}
            summary={"deck_qa":"passed"}
        else:
            if not args.slide:
                raise ContractError("Per-slide QA requires --slide")
            slide=find_slide(jobs,args.slide)
            job=require_job_current(deck,jobs,slide)
            if slide.get("status") not in {"recorded","accepted"}:
                raise ContractError("QA requires a recorded current image")
            from image_input_contract import require_recorded_submission
            require_recorded_submission(job,slide,inside_path(deck,slide["out"]))
            image=file_digest(inside_path(deck,slide["out"]))
            if image!=(slide.get("result") or {}).get("final_image_sha256"):
                raise ContractError("Image differs from recorded backend result")
            status="passed" if args.passed else "needs_repair" if args.needs_repair else "blocked"
            slide["qa"]={"actor":"agent","status":status,"image_sha256":image,
                         "visual_hash":slide["visual_hash"],"evidence":args.evidence,"timestamp":now_iso()}
            jobs.pop("deck_qa",None)
            first=jobs.get("first_batch")
            if first and first["ids"]:
                first["sealed"]=True
            if not args.passed:
                slide.pop("user_review",None)
                if args.needs_repair:
                    slide["repair_request"]={"id":str(uuid.uuid4()),"evidence":args.evidence,"visual_hash":slide["visual_hash"],
                                             "image_sha256":image,"render_phase":job["render_phase"]}
                    slide["status"]="pending_repair"
                    slide.pop("execution_completion",None)
                else:
                    slide["status"]="blocked"
            if first and first["ids"]:
                by_id={s["slide_id"]:s for s in jobs["slides"]}
                failures=[sid for sid in first["ids"] if (by_id[sid].get("qa") or {}).get("status") in {"needs_repair","blocked"}]
                if len(failures)>=2:
                    jobs["systemic_pause"]=True
                    jobs["pause_recommendation"]="Correct the common rendering cause; recalibrate or update the approved plan when needed."
                if all(qa_is_current(deck,by_id[sid],manifest) for sid in first["ids"]):
                    jobs["systemic_pause"]=False
            summary={"slide_id":slide["slide_id"],"qa":status}
    sync_user_review_run_state(deck,load_jobs(deck))
    print(json.dumps(summary))
    return 0


if __name__=="__main__":
    raise SystemExit(main())
