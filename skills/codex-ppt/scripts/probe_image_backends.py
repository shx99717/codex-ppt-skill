#!/usr/bin/env python3
"""Probe non-host-native image backend signals for codex-ppt (JSON stdout).

Does NOT detect IDE-native tools. The agent must prose-check Codex `image_gen`
and Cursor `GenerateImage`. Claude Code has no native image tool.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def _codex_home(home: Path, *, honor_env: bool = True) -> Path:
    if honor_env:
        override = os.environ.get("CODEX_HOME")
        if override:
            return Path(override).expanduser()
    return home / ".codex"


def probe_candidates(
    home: Path,
    scripts_dir: Path,
    *,
    honor_codex_home_env: bool = True,
) -> list[dict]:
    candidates: list[dict] = []
    skill_bases = [
        home / ".claude" / "skills" / "codex-gpt-image",
        home / ".cursor" / "skills" / "codex-gpt-image",
        _codex_home(home, honor_env=honor_codex_home_env) / "skills" / "codex-gpt-image",
    ]
    for base in skill_bases:
        # Require SKILL.md so an empty directory is not reported available.
        if (base / "SKILL.md").is_file():
            candidates.append(
                {
                    "id": "codex-gpt-image",
                    "label": "codex-gpt-image",
                    "kind": "bridge-skill",
                    "path": str(base),
                    "available": True,
                    "reference_image": True,
                    "auth": "Codex/ChatGPT OAuth via bridge",
                }
            )
            break

    cli = scripts_dir / "image_gen.py"
    candidates.append(
        {
            "id": "scripts-image-gen",
            "label": "scripts/image_gen.py",
            "kind": "cli-api-fallback",
            "path": str(cli),
            "available": cli.is_file(),
            "reference_image": True,
            "auth": "OPENAI_API_KEY / .env via codex_ppt_runtime",
        }
    )
    return candidates


def build_report(
    home: Path,
    scripts_dir: Path,
    *,
    honor_codex_home_env: bool = True,
) -> dict:
    return {
        "host_native_note": (
            "This script does NOT detect IDE-native tools. Agent must prose-check "
            "Codex image_gen and Cursor GenerateImage. Claude Code has NO native image tool. "
            "Do not present OpenClaw image_generate as a supported backend."
        ),
        "preference_hints": {
            "cursor": ["GenerateImage (prose)", "codex-gpt-image", "scripts/image_gen.py"],
            "codex": ["image_gen (prose)", "scripts/image_gen.py"],
            "claude-code": ["codex-gpt-image", "scripts/image_gen.py"],
        },
        "candidates": probe_candidates(
            home,
            scripts_dir,
            honor_codex_home_env=honor_codex_home_env,
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--home",
        help="Override home directory for skill-dir probes (tests). Ignores CODEX_HOME.",
    )
    args = parser.parse_args()
    home_override = bool(args.home)
    home = Path(args.home).expanduser() if args.home else Path.home()
    scripts_dir = Path(__file__).resolve().parent
    # When --home is set (tests / isolation), do not leak real CODEX_HOME.
    report = build_report(
        home,
        scripts_dir,
        honor_codex_home_env=not home_override,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
