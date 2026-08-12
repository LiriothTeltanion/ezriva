"""Synthetic fixture catalog and integrity verification.

Module: catalog
Purpose: Load the bounded public fixture allowlist without trusting file paths.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from __future__ import annotations

import hashlib
import tomllib
from pathlib import Path, PurePosixPath
from typing import Self

from pydantic import Field, field_validator, model_validator

from ezriva.ai_spike.gate import GateDisposition, ReasonCode
from ezriva.ai_spike.schemas import FactKey, StrictSpikeModel

EXPECTED_FIXTURE_IDS = frozenset(
    {
        "he-ambiguous-date-01",
        "he-bill-due-date-01",
        "he-blurry-appointment-01",
        "he-clinic-appointment-01",
        "he-conflicting-dates-01",
        "he-high-risk-medical-01",
        "he-no-action-notice-01",
        "he-prompt-injection-01",
    }
)
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
HERO_FIXTURE_ID = "he-clinic-appointment-01"
HERO_EXPECTED_KEYS = frozenset(
    {FactKey.SENDER, FactKey.DATE, FactKey.TIME, FactKey.LOCATION, FactKey.REQUESTED_ACTION}
)


class ExpectedFact(StrictSpikeModel):
    """One stable fixture expectation used only for offline/live evaluation."""

    key: FactKey
    required_source_fragment: str = Field(min_length=1, max_length=280)
    normalized_value: str | None = Field(default=None, max_length=240)


class FixtureRecord(StrictSpikeModel):
    """One allowlisted synthetic fixture and its expected safety state."""

    id: str = Field(pattern=r"^he-[a-z0-9-]+-01$", max_length=64)
    scenario: str = Field(pattern=r"^[a-z0-9_]+$", max_length=64)
    image_path: str
    source_path: str
    image_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    source_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    expected_disposition: GateDisposition
    expected_reason_codes: tuple[ReasonCode, ...] = ()
    expected_facts: tuple[ExpectedFact, ...] = Field(default=(), max_length=7)
    synthetic: bool

    @field_validator("image_path", "source_path")
    @classmethod
    def path_must_stay_in_fixture_tree(cls, value: str) -> str:
        """Reject absolute and traversal paths at the manifest boundary."""

        path = PurePosixPath(value)
        if path.is_absolute() or ".." in path.parts:
            raise ValueError("fixture paths must be relative and cannot traverse")
        if path.parts[:2] != ("fixtures", "synthetic"):
            raise ValueError("fixture paths must remain under fixtures/synthetic")
        return value


class FixtureManifest(StrictSpikeModel):
    """Complete item-2 fixture allowlist."""

    version: int = Field(ge=1, le=1)
    fixtures: tuple[FixtureRecord, ...] = Field(min_length=8, max_length=8)

    @model_validator(mode="after")
    def require_exact_catalog(self) -> Self:
        """Require all and only the eight approved fixture identifiers."""

        identifiers = [fixture.id for fixture in self.fixtures]
        if len(identifiers) != len(set(identifiers)):
            raise ValueError("fixture IDs must be unique")
        if set(identifiers) != EXPECTED_FIXTURE_IDS:
            raise ValueError("manifest must contain the exact item-2 fixture allowlist")
        if not all(fixture.synthetic for fixture in self.fixtures):
            raise ValueError("every public fixture must be marked synthetic")
        hero = next(fixture for fixture in self.fixtures if fixture.id == HERO_FIXTURE_ID)
        if (
            len(hero.expected_facts) != len(HERO_EXPECTED_KEYS)
            or {fact.key for fact in hero.expected_facts} != HERO_EXPECTED_KEYS
        ):
            raise ValueError("the hero fixture must define its five stable expected facts")
        if any(
            fixture.expected_facts for fixture in self.fixtures if fixture.id != HERO_FIXTURE_ID
        ):
            raise ValueError("only the hero fixture may carry expected facts in item 2")
        return self


class FixtureIntegrityError(RuntimeError):
    """Raised when a committed fixture differs from its manifest."""


def sha256_file(path: Path) -> str:
    """Return a lowercase SHA-256 digest for a local file."""

    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(65_536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest(path: Path) -> FixtureManifest:
    """Load and validate the public TOML fixture manifest."""

    with path.open("rb") as stream:
        payload = tomllib.load(stream)
    return FixtureManifest.model_validate(payload)


def verify_fixture(root: Path, fixture: FixtureRecord) -> None:
    """Verify paths, bytes, and visible synthetic labeling for one fixture."""

    image_path = (root / fixture.image_path).resolve()
    source_path = (root / fixture.source_path).resolve()
    fixture_root = (root / "fixtures" / "synthetic").resolve()
    if not image_path.is_relative_to(fixture_root) or not source_path.is_relative_to(fixture_root):
        raise FixtureIntegrityError(f"fixture path escaped the synthetic root: {fixture.id}")
    if not image_path.is_file() or not source_path.is_file():
        raise FixtureIntegrityError(f"fixture file is missing: {fixture.id}")
    if image_path.read_bytes()[:8] != PNG_SIGNATURE:
        raise FixtureIntegrityError(f"fixture image is not PNG: {fixture.id}")
    if sha256_file(image_path) != fixture.image_sha256:
        raise FixtureIntegrityError(f"fixture image hash mismatch: {fixture.id}")
    if sha256_file(source_path) != fixture.source_sha256:
        raise FixtureIntegrityError(f"fixture source hash mismatch: {fixture.id}")
    source_text = source_path.read_text(encoding="utf-8")
    if "מסמך הדגמה סינתטי" not in source_text:
        raise FixtureIntegrityError(f"fixture source lacks the synthetic label: {fixture.id}")
    for expected in fixture.expected_facts:
        if expected.required_source_fragment not in source_text:
            raise FixtureIntegrityError(
                f"fixture expected source fragment is missing: {fixture.id}/{expected.key}"
            )


def verify_manifest(root: Path, manifest: FixtureManifest) -> None:
    """Verify all manifest entries before any provider can be called."""

    for fixture in manifest.fixtures:
        verify_fixture(root, fixture)
