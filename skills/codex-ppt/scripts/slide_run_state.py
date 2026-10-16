#!/usr/bin/env python3
"""State helpers for codex-ppt slide generation runs."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

from filelock import FileLock


ACTIVE_SLIDE_STATUSES = {"dispatched"}
DISPATCHABLE_SLIDE_STATUSES = {"pending"}
TERMINAL_SLIDE_STATUSES = {"recorded", "accepted", "blocked"}
DEFAULT_MAX_CONCURRENT_SLIDES = 6


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def read_json(path: Path, default: Any = None) -> Any:
    path = Path(path)
    if not path.exists():
        if default is not None:
            return default
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    body = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


@contextmanager
def locked_json(path: Path, default: Any = None):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock_path = path.with_name(f".{path.name}.lock")
    with FileLock(str(lock_path)):
        data = read_json(path, default=default)
        try:
            yield data
        except Exception:
            raise
        else:
            write_json(path, data)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def deck_dir_from_target(target: str) -> Path:
    path = Path(target).expanduser().resolve()
    if path.is_dir():
        return path
    if path.name == "slide_jobs.json":
        return path.parent
    raise ValueError(f"Expected deck directory or slide_jobs.json: {target}")


def slide_jobs_path(deck_dir: Path) -> Path:
    return Path(deck_dir) / "slide_jobs.json"


def run_state_path(deck_dir: Path) -> Path:
    return Path(deck_dir) / "slide_run_state.json"


def load_jobs(deck_dir: Path) -> Dict[str, Any]:
    return read_json(slide_jobs_path(deck_dir))


def save_jobs(deck_dir: Path, jobs: Dict[str, Any]) -> None:
    write_json(slide_jobs_path(deck_dir), jobs)


def locked_jobs(deck_dir: Path):
    return locked_json(slide_jobs_path(deck_dir))


def load_run_state(deck_dir: Path) -> Dict[str, Any]:
    return read_json(run_state_path(deck_dir), default={"status": "created", "history": []})


def save_run_state(deck_dir: Path, state: Dict[str, Any]) -> None:
    write_json(run_state_path(deck_dir), state)


def locked_run_state(deck_dir: Path) -> Any:
    return locked_json(run_state_path(deck_dir), default={"status": "created", "history": []})


def set_run_status(deck_dir: Path, status: str, note: str | None = None) -> Dict[str, Any]:
    with locked_run_state(deck_dir) as state:
        if state.get("status") != status:
            state.setdefault("history", []).append(
                {"from": state.get("status"), "to": status, "at": now_iso(), "note": note}
            )
        state["status"] = status
        state["updated_at"] = now_iso()
    return state


def normalize_slide_id(value: Any) -> str:
    text = str(value).strip()
    if text.startswith("slide_"):
        suffix = text.removeprefix("slide_")
        if suffix.isdigit():
            return f"slide_{int(suffix):02d}"
    if text.isdigit():
        return f"slide_{int(text):02d}"
    raise ValueError(f"Invalid slide id: {value}")


def find_slide(jobs: Dict[str, Any], slide: Any) -> Dict[str, Any]:
    slide_id = normalize_slide_id(slide)
    for entry in jobs.get("slides", []):
        if entry.get("slide_id") == slide_id or str(entry.get("number")) == str(slide):
            return entry
    raise KeyError(f"Slide not found in slide_jobs.json: {slide_id}")


def resolve_deck_path(deck_dir: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = Path(deck_dir) / path
    return path.resolve()


def rel_to_deck(deck_dir: Path, value: Path) -> str:
    return Path(value).resolve().relative_to(Path(deck_dir).resolve()).as_posix()


def ensure_file(path: Path, label: str) -> Path:
    path = Path(path)
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Missing {label}: {path}")
    return path


def active_slides(jobs: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [slide for slide in jobs.get("slides", []) if slide.get("status") in ACTIVE_SLIDE_STATUSES]


def dispatchable_slides(jobs: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [slide for slide in jobs.get("slides", []) if slide.get("status") in DISPATCHABLE_SLIDE_STATUSES]


def max_concurrent_slides(jobs: Dict[str, Any]) -> int:
    value = jobs.get("max_concurrent_slides", DEFAULT_MAX_CONCURRENT_SLIDES)
    try:
        value = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Invalid max_concurrent_slides: {value}") from exc
    if value < 1:
        raise ValueError("max_concurrent_slides must be >= 1")
    return value


def dispatch_slots_available(jobs: Dict[str, Any]) -> int:
    return max(0, max_concurrent_slides(jobs) - len(active_slides(jobs)))


def update_jobs_run_status(jobs: Dict[str, Any]) -> None:
    slides = jobs.get("slides", [])
    if slides and all(slide.get("status") in {"dispatched", "recorded", "accepted"} for slide in slides):
        jobs["run_status"] = "slides_dispatched"
    if slides and all(slide.get("status") in {"recorded", "accepted"} for slide in slides):
        jobs["run_status"] = "slides_recorded"
    if slides and all(slide.get("status") in TERMINAL_SLIDE_STATUSES for slide in slides):
        if any(slide.get("status") == "blocked" for slide in slides):
            jobs["run_status"] = "blocked"
    jobs["updated_at"] = now_iso()


def slide_ids(slides: Iterable[Dict[str, Any]]) -> List[str]:
    return [str(slide.get("slide_id")) for slide in slides]


def final_image_path(deck_dir: Path, slide: Dict[str, Any]) -> Path:
    out_ref = slide.get("out") or f"origin_image/{slide['slide_id']}.png"
    return resolve_deck_path(deck_dir, out_ref)


def review_is_valid(deck_dir: Path, slide: Dict[str, Any]) -> bool:
    """True when slide.user_review is present, marked user_reviewed, and sha matches the PNG."""
    review = slide.get("user_review")
    if not isinstance(review, dict):
        return False
    if review.get("status") != "user_reviewed":
        return False
    path = final_image_path(deck_dir, slide)
    if not path.is_file():
        return False
    if review.get("image_sha256") != sha256_file(path):
        return False
    spec_path=Path(deck_dir)/"deck_spec.json"
    if (Path(deck_dir)/"plan_approvals.json").exists() or spec_path.exists():
        try:
            spec=read_json(spec_path)
            if spec.get("workflow_version")==2:
                from planning_contract import approval_event,build_manifest,load_ledger
                manifest=build_manifest(spec,Path(deck_dir))
                sid=slide["slide_id"]
                expected=manifest["slides"][sid]["visual_hash"]
                if review.get("actor")!="user" or review.get("visual_hash")!=expected:
                    return False
                event=approval_event(load_ledger(Path(deck_dir)),review.get("event_id"),"image")
                return (event.get("image_bindings") or {}).get(sid)=={
                    "sha256":review["image_sha256"],"visual_hash":expected}
        except (OSError,ValueError,KeyError,TypeError):
            return False
    return True


def sync_user_review_run_state(deck_dir: Path, jobs: Dict[str, Any]) -> None:
    """Refresh slide_run_state.json user_review summary from current jobs.

    Emits marker \"user_reviewed\" only while at least one recorded slide still
    has a valid approval (no sticky T1 marker after clear/re-dispatch).
    """
    approved: List[str] = []
    pending: List[str] = []
    for slide in jobs.get("slides", []):
        if slide.get("status") == "accepted":
            continue
        if slide.get("status") != "recorded":
            continue
        sid = str(slide.get("slide_id"))
        if review_is_valid(deck_dir, slide):
            approved.append(sid)
        else:
            pending.append(sid)
    with locked_run_state(deck_dir) as state:
        summary: Dict[str, Any] = {
            "approved_slide_ids": approved,
            "pending_recorded_slide_ids": pending,
            "all_recorded_slides_approved": bool(approved) and not pending,
            "updated_at": now_iso(),
        }
        if approved:
            summary["marker"] = "user_reviewed"
        state["user_review"] = summary
