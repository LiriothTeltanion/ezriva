"""Repository privacy, provenance, and metadata guardrail.

Module: check_repository
Purpose: Catch obvious private-file, secret, and license mistakes before commit.
Author: Kevin Cusnir with Codex
Date: 2026-08-11 (Asia/Jerusalem)
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PATH_WORDS = {
    "enrollment",
    "private-agreement",
    "passport",
    "project_sources",
    "private_document",
}
FORBIDDEN_SUFFIXES = {".key", ".p12", ".pfx", ".pem"}
ALLOWED_BINARY_PATHS = {
    "fixtures/synthetic/he-ambiguous-date-01.png",
    "fixtures/synthetic/he-bill-due-date-01.png",
    "fixtures/synthetic/he-blurry-appointment-01.png",
    "fixtures/synthetic/he-clinic-appointment-01.png",
    "fixtures/synthetic/he-conflicting-dates-01.png",
    "fixtures/synthetic/he-high-risk-medical-01.png",
    "fixtures/synthetic/he-no-action-notice-01.png",
    "fixtures/synthetic/he-prompt-injection-01.png",
}
SECRET_PATTERNS = {
    "AWS access-key-shaped value": re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b"),
    "private key marker": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token-shaped value": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b"),
}


def _repository_files() -> list[Path]:
    """Return tracked and untracked files that are not ignored by Git."""

    completed = subprocess.run(
        ("git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"),
        cwd=ROOT,
        check=True,
        capture_output=True,
    )
    return [ROOT / value.decode() for value in completed.stdout.split(b"\0") if value]


def _read_text(path: Path) -> str | None:
    """Read a reasonably sized text file or return None for binary content."""

    if path.stat().st_size > 5_000_000:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def main() -> int:
    """Validate repository boundaries and public metadata."""

    failures: list[str] = []
    git_root = subprocess.run(
        ("git", "rev-parse", "--show-toplevel"),
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if Path(git_root).resolve() != ROOT:
        failures.append(f"Git root {git_root!r} is not the isolated Ezriva directory.")

    for path in _repository_files():
        relative = path.relative_to(ROOT)
        normalized = relative.as_posix().lower()
        if relative.name.startswith(".env") and relative.name != ".env.example":
            failures.append(f"Private environment file is commit-visible: {relative}")
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            failures.append(f"Private key/certificate file is commit-visible: {relative}")
        if any(word in normalized for word in FORBIDDEN_PATH_WORDS):
            failures.append(f"Private-source-shaped path is commit-visible: {relative}")
        text = _read_text(path)
        if text is None:
            if relative.as_posix() not in ALLOWED_BINARY_PATHS:
                failures.append(f"Binary file is outside the synthetic-only allowlist: {relative}")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                failures.append(f"{label} found in {relative}")

    package_metadata = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    if package_metadata.get("license") != "MIT":
        failures.append("package.json license is not MIT.")
    if 'license = "MIT"' not in pyproject:
        failures.append("pyproject.toml license is not MIT.")
    if "Permission is hereby granted, free of charge" not in license_text:
        failures.append("LICENSE is not the canonical MIT text.")

    if failures:
        print("Repository guardrail found issues:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print(
        "Repository guardrail passed: isolated Git root, no obvious private paths or "
        "secret-shaped values, and consistent MIT metadata."
    )
    print("This heuristic is a guardrail, not proof that every possible PII value is absent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
