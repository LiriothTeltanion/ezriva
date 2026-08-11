"""Fail when detect-secrets reports a candidate secret.

Module: check_secrets
Purpose: Parse the scanner result instead of treating a zero CLI exit as clean.
Author: Kevin Cusnir with Codex
Date: 2026-08-11 (Asia/Jerusalem)
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _commit_visible_files() -> list[str]:
    """Return non-ignored source paths while excluding generated lockfiles."""

    completed = subprocess.run(
        ("git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"),
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    excluded = {"package-lock.json", "uv.lock"}
    return [
        value.decode()
        for value in completed.stdout.split(b"\0")
        if value and value.decode() not in excluded
    ]


def main() -> int:
    """Run detect-secrets against commit-visible files and inspect its JSON."""

    files = _commit_visible_files()
    completed = subprocess.run(
        ("detect-secrets", "scan", "--no-verify", *files),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    results = payload.get("results", {})
    if results:
        print("detect-secrets found candidates:")
        for path, findings in results.items():
            print(f"- {path}: {len(findings)} candidate(s)")
        return 1

    print("detect-secrets found no candidates in commit-visible source files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
