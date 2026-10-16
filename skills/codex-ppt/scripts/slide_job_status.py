#!/usr/bin/env python3
"""Print codex-ppt slide generation job status."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict

from slide_run_state import (
    active_slides,
    deck_dir_from_target,
    dispatch_slots_available,
    dispatchable_slides,
    load_jobs,
    load_run_state,
    max_concurrent_slides,
    slide_ids,
)


def main() -> int:
    # Windows consoles on a non-UTF-8 locale can't encode arbitrary non-ASCII
    # deck paths this script prints; force UTF-8 so the process doesn't crash
    # regardless of the ambient console code page.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", help="Deck directory or slide_jobs.json")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--legacy-unmanaged", action="store_true")
    args = parser.parse_args()

    deck_dir = deck_dir_from_target(args.deck)
    jobs = load_jobs(deck_dir)
    from planning_contract import require_legacy_allowed, load_managed_spec
    if args.legacy_unmanaged:
        require_legacy_allowed(deck_dir)
    elif jobs.get("workflow_version") != 2:
        load_managed_spec(deck_dir)
    state = load_run_state(deck_dir)
    by_status = defaultdict(list)
    for slide in jobs.get("slides", []):
        by_status[slide.get("status", "unknown")].append(slide.get("slide_id"))
    summary = {
        "deck_dir": str(deck_dir),
        "run_status": state.get("status"),
        "slide_count": len(jobs.get("slides", [])),
        "selected_backend": jobs.get("selected_backend"),
        "max_concurrent_slides": max_concurrent_slides(jobs),
        "active_dispatches": slide_ids(active_slides(jobs)),
        "dispatch_slots_available": dispatch_slots_available(jobs),
        "dispatchable_slides": slide_ids(dispatchable_slides(jobs)),
        "counts": dict(Counter(slide.get("status", "unknown") for slide in jobs.get("slides", []))),
        "slides": dict(sorted(by_status.items())),
    }

    if jobs.get("workflow_version")==2:
        from planning_contract import (build_manifest,load_managed_spec,qa_is_current,
                                       require_job_current,ContractError)
        from slide_run_state import review_is_valid
        stale=[]
        pending_qa=[]
        pending_review=[]
        try:
            manifest=build_manifest(load_managed_spec(deck_dir),deck_dir)
            for slide in jobs["slides"]:
                sid=slide["slide_id"]
                try:
                    require_job_current(deck_dir,jobs,slide)
                except (ContractError,OSError):
                    stale.append(sid)
                if slide.get("status") in {"recorded","accepted"} and not qa_is_current(deck_dir,slide,manifest):
                    pending_qa.append(sid)
                if slide.get("status")=="recorded" and not review_is_valid(deck_dir,slide):
                    pending_review.append(sid)
        except ContractError as exc:
            summary["managed_error"]=str(exc)
            stale=[s["slide_id"] for s in jobs["slides"]]
        summary.update(stale_scope_ids=stale,pending_qa=pending_qa,pending_review=pending_review,
            pending_exceptions=[s["slide_id"] for s in jobs["slides"] if s.get("status") in {"pending_repair","blocked"}],
            first_batch=jobs.get("first_batch"),systemic_pause=jobs.get("systemic_pause",False),
            repair_counts={s["slide_id"]:s.get("repair_counts",{}) for s in jobs["slides"]})
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0

    print(f"deck_dir={summary['deck_dir']}")
    print(f"run_status={summary['run_status']}")
    print(f"selected_backend={summary['selected_backend'] or '-'}")
    print(f"max_concurrent_slides={summary['max_concurrent_slides']}")
    print(f"active_dispatches={', '.join(summary['active_dispatches']) if summary['active_dispatches'] else '-'}")
    print(f"dispatch_slots_available={summary['dispatch_slots_available']}")
    print(f"dispatchable_slides={', '.join(summary['dispatchable_slides']) if summary['dispatchable_slides'] else '-'}")
    for status, slides in summary["slides"].items():
        print(f"{status}: {', '.join(slides) if slides else '-'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
