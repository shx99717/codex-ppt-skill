#!/usr/bin/env python3
"""Record a blocker that prevents a codex-ppt slide job from completing."""

from __future__ import annotations

import argparse
from planning_contract import consumer_lock,require_job_current

from slide_run_state import (
    deck_dir_from_target,
    find_slide,
    locked_jobs,
    now_iso,
    set_run_status,
    update_jobs_run_status,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", help="Deck directory or slide_jobs.json")
    parser.add_argument("--slide", required=True, help="slide_01 or 1")
    parser.add_argument("--reason", required=True)
    parser.add_argument("--agent-id")
    parser.add_argument("--legacy-unmanaged", action="store_true")
    args = parser.parse_args()

    deck_dir = deck_dir_from_target(args.deck)
    with consumer_lock(deck_dir,args.legacy_unmanaged) as managed, locked_jobs(deck_dir) as jobs:
        slide = find_slide(jobs, args.slide)
        if managed:
            require_job_current(deck_dir,jobs,slide)
        if slide.get("status") in {"recorded", "accepted"}:
            raise SystemExit(f"{slide['slide_id']} is already complete; refusing to mark it blocked.")
        slide["blocker"] = {
            "agent_id": args.agent_id,
            "reason": args.reason,
            "blocked_at": now_iso(),
        }
        slide["status"] = "blocked"
        update_jobs_run_status(jobs)
        jobs["run_status"] = "blocked"
        slide_id = slide["slide_id"]
    set_run_status(deck_dir, "blocked", f"{slide_id}: {args.reason}")
    print(f"{slide_id} -> blocked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
