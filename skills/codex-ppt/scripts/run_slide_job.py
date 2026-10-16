#!/usr/bin/env python3
"""Execute a managed CLI job with verified snapshots and no long-held global locks."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from filelock import FileLock
from generation_execution import is_cli_backend
from planning_contract import consumer_lock, ContractError, inside_path, require_job_current
from record_plan_approval import snapshot_file
from slide_run_state import deck_dir_from_target, find_slide, load_jobs


def execute_job(args) -> int:
    deck = deck_dir_from_target(args.deck)
    # Serialize shared-directory creation with path resolution. On Windows a
    # parent appearing mid-realpath can retain a namespace prefix and make a
    # legitimate child fail containment. Provider work still runs unlocked.
    with consumer_lock(deck):
        out = inside_path(deck, args.out)
        if not out.is_relative_to(deck / "candidates") or out.suffix.lower() != ".png":
            raise ContractError("Output must be a new PNG under candidates; final images and references are parent-owned")
        out.parent.mkdir(parents=True, exist_ok=True)
    # Per-candidate ownership does not block other jobs or their state writers.
    with FileLock(str(out.with_name("." + out.name + ".lock"))), \
            tempfile.TemporaryDirectory(prefix=".execution-", dir=deck) as scratch:
        with consumer_lock(deck), FileLock(str(deck / ".slide_jobs.json.lock")):
            jobs = load_jobs(deck)
            slide = find_slide(jobs, args.slide)
            job = require_job_current(deck, jobs, slide)
            if not is_cli_backend(job["expected_backend"]):
                raise ContractError("This adapter executes only the approved bundled CLI backend")
            if out.exists():
                raise ContractError("Candidate output already exists; choose a new attempt path")
            if not args.dry_run and (slide.get("status") != "dispatched" or not args.agent_id
                    or (slide.get("dispatch") or {}).get("agent_id") != args.agent_id):
                raise ContractError("Execution requires this agent's current recorded dispatch")
            dispatch = copy.deepcopy(slide.get("dispatch"))
            job_sha = slide["job_sha256"]
            sid = slide["slide_id"]
            execution = job["execution"]
            prompt = Path(scratch) / "prompt.txt"
            prompt.write_text(job["prompt"], encoding="utf-8")
            command = [sys.executable, "-B", str(Path(__file__).with_name("image_gen.py")),
                execution["operation"], "--prompt-file", str(prompt), "--out", str(out), "--no-augment"]
            capabilities=job["generation_config"].get("capabilities")
            if capabilities is not None:
                capability_path=Path(scratch)/"capabilities.json"
                capability_path.write_text(json.dumps(capabilities),encoding="utf-8")
                command += ["--capabilities-file",str(capability_path)]
            for key, value in execution["parameters"].items():
                if value is not None:
                    command += ["--" + key.replace("_", "-"), str(value)]
            for index, image in enumerate(job["input_images"]):
                staged = Path(scratch) / (str(index) + "-" + image["sha256"] + Path(image["path"]).suffix)
                snapshot_file(Path(image["path"]), staged, image["sha256"])
                command += ["--image", str(staged)]
            if args.dry_run:
                command.append("--dry-run")
        # Provider work may overlap across workers; global state updates stay free.
        result = subprocess.run(command, check=False)
        if result.returncode:
            return result.returncode
        with consumer_lock(deck), FileLock(str(deck / ".slide_jobs.json.lock")):
            current_jobs=load_jobs(deck)
            current = find_slide(current_jobs, sid)
            require_job_current(deck, current_jobs, current)
            if current["job_sha256"] != job_sha:
                raise ContractError("Compiled job changed during backend execution")
            if not args.dry_run and (current.get("status") != "dispatched"
                    or current.get("dispatch") != dispatch):
                raise ContractError("Dispatched attempt changed during backend execution")
            if not args.dry_run:
                from slide_image_ratio import RATIO_BY_LABEL, require_image_ratio
                if not out.is_file():
                    raise ContractError("Backend returned without a candidate image")
                try:
                    from image_input_contract import measured_output
                    measured_output(out,jobs["aspect_ratio"],job["generation_config"].get("output_requirements"))
                except ValueError as exc:
                    raise ContractError(str(exc)) from exc
                from image_input_contract import make_receipt,sha256
                from record_plan_approval import atomic_group
                receipt=make_receipt(job,current,out,"cli_image_files",origin="adapter")
                receipt_path=out.with_suffix(".submission.json")
                receipt_bytes=(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n").encode("utf-8")
                import hashlib
                current["execution_completion"]={"producer":"run_slide_job.py","status":"succeeded","dry_run":False,
                    "receipt":receipt,"receipt_path":str(receipt_path),"receipt_sha256":hashlib.sha256(receipt_bytes).hexdigest()}
                atomic_group(deck,{receipt_path.relative_to(deck).as_posix():receipt_bytes,
                    "slide_jobs.json":(json.dumps(current_jobs,ensure_ascii=False,indent=2)+"\n").encode("utf-8")})
        print(json.dumps({"slide_id": sid, "operation": execution["operation"],
            "backend_used": job["expected_backend"], "candidate": str(out),
            "dry_run": args.dry_run, "job_sha256": job_sha}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("deck")
    parser.add_argument("--slide", required=True)
    parser.add_argument("--out", required=True, help="New candidate PNG inside deck/candidates")
    parser.add_argument("--agent-id", help="Required for execution; must match current dispatch")
    parser.add_argument("--dry-run", action="store_true")
    return execute_job(parser.parse_args())


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContractError as exc:
        raise SystemExit(str(exc)) from exc
