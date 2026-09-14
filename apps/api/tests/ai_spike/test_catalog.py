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
    MAX_FIXTURE_IMAGE_BYTES,
    FixtureIntegrityError,
    FixtureRecord,
    load_manifest,
    sha256_file,
    verify_fixture,
    verify_manifest,
)
from ezriva.ai_spike.schemas import FactKey

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


def test_hero_fixture_uses_the_release_stable_future_date() -> None:
    """The public hero remains actionable beyond the 2026 submission sprint."""

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")
    hero = next(
        fixture for fixture in manifest.fixtures if fixture.id == "he-clinic-appointment-01"
    )
    date_fact = next(fact for fact in hero.expected_facts if fact.key is FactKey.DATE)

    assert date_fact.required_source_fragment == "18.04.2027"
    assert date_fact.normalized_value == "2027-04-18"


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


def _isolated_fixture_record(tmp_path: Path) -> tuple[Path, FixtureRecord]:
    """Copy the hero record into a temporary synthetic fixture root."""

    source_record = load_manifest(ROOT / "fixtures" / "manifest.toml").fixtures[0]
    fixture_root = tmp_path / "fixtures" / "synthetic"
    fixture_root.mkdir(parents=True)
    image_path = fixture_root / "hero.png"
    source_path = fixture_root / "hero.txt"
    image_path.write_bytes((ROOT / source_record.image_path).read_bytes())
    source_path.write_text(
        (ROOT / source_record.source_path).read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    payload = source_record.model_dump(mode="json")
    payload["image_path"] = "fixtures/synthetic/hero.png"
    payload["source_path"] = "fixtures/synthetic/hero.txt"
    payload["image_sha256"] = sha256_file(image_path)
    payload["source_sha256"] = sha256_file(source_path)
    return tmp_path, FixtureRecord.model_validate(payload)


def test_runtime_verifier_rejects_oversized_fixture(tmp_path: Path) -> None:
    """The provider boundary enforces the byte limit, not only a test assertion."""

    root, fixture = _isolated_fixture_record(tmp_path)
    image_path = root / fixture.image_path
    with image_path.open("ab") as stream:
        stream.write(b"\x00" * (MAX_FIXTURE_IMAGE_BYTES - image_path.stat().st_size + 1))

    with pytest.raises(FixtureIntegrityError, match="size limit"):
        verify_fixture(root, fixture)


def test_runtime_verifier_rejects_wrong_dimensions(tmp_path: Path) -> None:
    """The provider boundary reads PNG dimensions before any model call."""

    root, fixture = _isolated_fixture_record(tmp_path)
    image_path = root / fixture.image_path
    Image.new("RGB", (800, 500), "white").save(image_path, format="PNG")
    payload = fixture.model_dump(mode="json")
    payload["image_sha256"] = sha256_file(image_path)
    resized = FixtureRecord.model_validate(payload)

    with pytest.raises(FixtureIntegrityError, match="dimensions"):
        verify_fixture(root, resized)
