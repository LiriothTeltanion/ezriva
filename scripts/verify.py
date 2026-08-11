"""Portable setup and verification entry point.

Module: verify
Purpose: Run the same honest checks on Linux, macOS, Windows, and CI.
Author: Kevin Cusnir with Codex
Date: 2026-08-11 (Asia/Jerusalem)
"""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _environment() -> dict[str, str]:
    """Return a task-local environment with writable package caches."""

    environment = os.environ.copy()
    environment["NPM_CONFIG_CACHE"] = str(ROOT / ".cache" / "npm")
    environment["UV_CACHE_DIR"] = str(ROOT / ".cache" / "uv")
    return environment


def _run(command: Sequence[str]) -> None:
    """Run one command and stop at the first real failure.

    Args:
        command: Executable and arguments to run from the repository root.

    Raises:
        subprocess.CalledProcessError: When the command exits unsuccessfully.
    """

    print(f"\n▶ {' '.join(command)}", flush=True)
    subprocess.run(
        command,
        cwd=ROOT,
        env=_environment(),
        check=True,
    )


TASKS: dict[str, tuple[tuple[str, ...], ...]] = {
    "setup": (
        ("uv", "sync", "--frozen"),
        ("npm", "ci"),
    ),
    "lint": (
        ("uv", "lock", "--check"),
        ("uv", "run", "ruff", "check", "."),
        ("uv", "run", "ruff", "format", "--check", "."),
        ("npm", "run", "lint:web"),
    ),
    "typecheck": (
        ("uv", "run", "mypy", "apps/api/src", "apps/api/tests", "scripts"),
        ("npm", "run", "typecheck:web"),
    ),
    "test": (
        ("uv", "run", "pytest"),
        ("npm", "run", "test:web"),
    ),
    "build": (
        ("uv", "run", "python", "-m", "compileall", "-q", "apps/api/src"),
        ("npm", "run", "build:web"),
        ("npm", "ls", "--all"),
    ),
    "secret-scan": (
        ("uv", "run", "python", "scripts/check_repository.py"),
        ("uv", "run", "python", "scripts/check_secrets.py"),
    ),
}


def main(arguments: Sequence[str] | None = None) -> int:
    """Run a named verification task.

    Args:
        arguments: Optional CLI arguments, excluding the executable name.

    Returns:
        Zero when every requested command succeeds; non-zero otherwise.
    """

    values = list(sys.argv[1:] if arguments is None else arguments)
    task = values[0] if values else "verify"

    task_order: tuple[str, ...]
    if task == "verify":
        task_order = ("lint", "typecheck", "test", "build", "secret-scan")
    elif task in TASKS:
        task_order = (task,)
    else:
        choices = ", ".join((*TASKS, "verify"))
        print(f"Unknown task {task!r}. Choose one of: {choices}.", file=sys.stderr)
        return 2

    try:
        for task_name in task_order:
            print(f"\n=== {task_name} ===", flush=True)
            for command in TASKS[task_name]:
                _run(command)
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        print(f"\nVerification stopped: {error}", file=sys.stderr)
        return 1

    print("\nAll requested checks completed successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
