#!/usr/bin/env python3
"""Record per-slide user review for codex-ppt (full-res image approval).

Only slides with status ``recorded`` may be approved. Sample slides marked
``accepted`` are outside this gate — do not use this script for sample approval.
"""

from __future__ import annotations

import argparse
import json
from filelock import FileLock

from slide_run_state import (
    deck_dir_from_target,
    final_image_path,
    find_slide,
    load_jobs,
    locked_jobs,
    now_iso,
    review_is_valid,
    sha256_file,
    sync_user_review_run_state,
)

# Re-export for tests that import review_is_valid from this module.
__all__ = ["main", "review_is_valid"]



def record_managed_review(deck,args) -> dict:
    from planning_contract import (ContractError,accepted_sample_is_current,build_manifest,consumer_lock,
        file_digest,inside_path,load_ledger,load_managed_spec,require_job_current,selection)
    from record_plan_approval import atomic_group,user_event
    with consumer_lock(deck),FileLock(str(deck/".slide_jobs.json.lock")):
        jobs=load_jobs(deck)
        spec=load_managed_spec(deck)
        manifest=build_manifest(spec,deck)
        expected=list(manifest["slides"])
        by_id={s["slide_id"]:s for s in jobs["slides"]}
        if len(by_id)!=len(jobs["slides"]) or set(by_id)!=set(expected):
            raise ContractError("Bulk review must include the expected planned set")
        if args.all:
            selected=expected
        else:
            selected=selection(args.slides or args.slide,expected)
        exceptions=selection(args.exceptions,expected) if args.exceptions else []
        if exceptions and not args.all:
            raise ContractError("--except applies only to --all")
        ledger=load_ledger(deck)
        bindings={}
        for sid in selected:
            if sid in exceptions:
                continue
            slide=by_id[sid]
            if args.approve:
                require_job_current(deck,jobs,slide)
                if slide.get("status")=="accepted":
                    if not accepted_sample_is_current(deck,sid,manifest,ledger):
                        raise ContractError(f"Stale accepted sample: {sid}")
                    continue
                if slide.get("status")!="recorded":
                    raise ContractError(f"Included slide must be recorded: {sid}")
                sha=file_digest(inside_path(deck,slide["out"]))
                if sha!=(slide.get("result") or {}).get("final_image_sha256"):
                    raise ContractError(f"Image differs from recorded backend result: {sid}")
                bindings[sid]={"sha256":sha,"visual_hash":manifest["slides"][sid]["visual_hash"]}
        event=None
        if args.approve:
            event=user_event(args.evidence,["image"],slide_ids=list(bindings),image_bindings=bindings,
                             exceptions=exceptions)
            ledger["events"].append(event)
        for sid in selected:
            slide=by_id[sid]
            if sid in exceptions or args.clear:
                slide.pop("user_review",None)
            elif sid in bindings:
                slide["user_review"]={"actor":"user","status":"user_reviewed","reviewed_at":now_iso(),
                    "image_sha256":bindings[sid]["sha256"],"visual_hash":bindings[sid]["visual_hash"],
                    "event_id":event["id"]}
        payload={"plan_approvals.json":(json.dumps(ledger,ensure_ascii=False,indent=2)+"\n").encode("utf-8"),
                 "slide_jobs.json":(json.dumps(jobs,ensure_ascii=False,indent=2)+"\n").encode("utf-8")}
        # locked_jobs would save after exit; group commit handles both files now.
        atomic_group(deck,payload)
        summary={"action":"user_reviewed" if args.approve else "review_cleared",
                 "slides":list(bindings) if args.approve else selected,"exceptions":exceptions,
                 "event_id":event["id"] if event else None}
    sync_user_review_run_state(deck,load_jobs(deck))
    return summary

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", help="Deck directory or slide_jobs.json")
    selector=parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--slide", help="slide_01 or 1")
    selector.add_argument("--slides", help="Comma-separated slide IDs")
    selector.add_argument("--all", action="store_true")
    parser.add_argument("--except", dest="exceptions")
    parser.add_argument("--evidence", default="")
    parser.add_argument("--legacy-unmanaged", action="store_true")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--approve", action="store_true")
    group.add_argument("--clear", action="store_true")
    args = parser.parse_args()

    deck_dir = deck_dir_from_target(args.deck)
    from planning_contract import require_legacy_allowed, ContractError
    if not args.legacy_unmanaged:
        print(json.dumps(record_managed_review(deck_dir,args),ensure_ascii=False))
        return 0
    require_legacy_allowed(deck_dir)
    if not args.slide or args.exceptions:
        raise ContractError("Legacy review supports a single --slide")
    with locked_jobs(deck_dir) as jobs:
        slide = find_slide(jobs, args.slide)
        slide_id = slide["slide_id"]
        if args.approve:
            if slide.get("status") != "recorded":
                raise SystemExit(
                    f"{slide_id} must be recorded before user review; got {slide.get('status')}"
                )
            path = final_image_path(deck_dir, slide)
            if not path.is_file():
                raise SystemExit(f"Final image missing for {slide_id}: {path}")
            slide["user_review"] = {
                "status": "user_reviewed",
                "reviewed_at": now_iso(),
                "image_sha256": sha256_file(path),
            }
        else:
            slide.pop("user_review", None)

    # Sync run state AFTER releasing the jobs lock (avoid nested file locks on Windows).
    sync_user_review_run_state(deck_dir, load_jobs(deck_dir))

    action = "user_reviewed" if args.approve else "review_cleared"
    print(json.dumps({"slide_id": slide_id, "action": action}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
