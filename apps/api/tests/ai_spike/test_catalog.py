"""Synthetic catalog integrity tests.

Module: test_catalog
Purpose: Prove the public allowlist is complete, synthetic, and immutable.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from pathlib import Path

import pytest
from PIL import Image
from pydantic import ValidationError

from ezriva.ai_spike.catalog import (
    EXPECTED_FIXTURE_IDS,
    FixtureRecord,
    load_manifest,
    verify_manifest,
)

ROOT = Path(__file__).resolve().parents[4]


def test_manifest_contains_exactly_eight_verified_fixture_pairs() -> None:
    """The item-2 allowlist has no missing or extra scenario."""

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")

    verify_manifest(ROOT, manifest)
    assert {fixture.id for fixture in manifest.fixtures} == EXPECTED_FIXTURE_IDS
    assert len(manifest.fixtures) == 8
    hero = next(
        fixture for fixture in manifest.fixtures if fixture.id == "he-clinic-appointment-01"
    )
    assert {fact.key.value for fact in hero.expected_facts} == {
        "sender",
        "date",
        "time",
        "location",
        "requested_action",
    }


def test_all_fixture_images_have_consistent_safe_dimensions() -> None:
    """Committed fixture images are bounded PNGs suitable for Bedrock input."""

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")

    for fixture in manifest.fixtures:
        with Image.open(ROOT / fixture.image_path) as image:
            assert image.format == "PNG"
            assert image.size == (1_600, 1_000)
        assert (ROOT / fixture.image_path).stat().st_size < 3_670_016


def test_manifest_rejects_path_traversal() -> None:
    """A manifest entry cannot escape the synthetic fixture tree."""

    valid = load_manifest(ROOT / "fixtures" / "manifest.toml").fixtures[0].model_dump(mode="json")
    valid["image_path"] = "fixtures/synthetic/../../project_sources/private.png"

    with pytest.raises(ValidationError):
        FixtureRecord.model_validate(valid)


def test_prompt_injection_is_public_synthetic_text() -> None:
    """The adversarial fixture is explicit test data, not an executable instruction."""

    source = (ROOT / "fixtures/synthetic/he-prompt-injection-01.txt").read_text(encoding="utf-8")

    assert "מסמך הדגמה סינתטי" in source
    assert "Ignore previous instructions" in source
    assert "אסור לבצע אותו" in source
