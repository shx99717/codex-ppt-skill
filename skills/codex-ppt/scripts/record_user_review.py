#!/usr/bin/env python3
"""Record per-slide user review for codex-ppt (full-res image approval).

Only slides with status ``recorded`` may be approved. Sample slides marked
``accepted`` are outside this gate — do not use this script for sample approval.
"""

from __future__ import annotations

import argparse
import json

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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck", help="Deck directory or slide_jobs.json")
    parser.add_argument("--slide", required=True, help="slide_01 or 1")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--approve", action="store_true")
    group.add_argument("--clear", action="store_true")
    args = parser.parse_args()

    deck_dir = deck_dir_from_target(args.deck)
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
