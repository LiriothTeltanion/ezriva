"""Extraction-only schema tests.

Module: test_schemas
Purpose: Prove that model output cannot smuggle executable fields.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

import json

import pytest
from pydantic import ValidationError

from ezriva.ai_spike.schemas import DocumentBriefCandidate, EvidenceFact, EvidenceStatus, FactKey
from tests.ai_spike.candidates import hero_candidate


def test_schema_contains_no_action_authority_fields() -> None:
    """The JSON schema cannot ask a model for a tool, payload, or approval."""

    serialized = json.dumps(DocumentBriefCandidate.model_json_schema(), sort_keys=True)
    forbidden = (
        "action_payload",
        "approval",
        "destination",
        "execute",
        "idempotency_key",
        "owner_id",
        "tool_name",
    )

    assert all(value not in serialized for value in forbidden)


def test_schema_rejects_an_extra_execute_field() -> None:
    """Strict Pydantic validation rejects an action-shaped model addition."""

    payload = hero_candidate().model_dump(mode="json")
    payload["execute"] = True

    with pytest.raises(ValidationError):
        DocumentBriefCandidate.model_validate(payload)


def test_confirmed_fact_requires_hebrew_evidence() -> None:
    """A normalized value without Hebrew evidence is not confirmed."""

    with pytest.raises(ValidationError):
        EvidenceFact(
            key=FactKey.DATE,
            normalized_value="2026-08-18",
            source_excerpt="Date: 18 August 2026",
            status=EvidenceStatus.CONFIRMED,
        )


def test_not_found_fact_cannot_carry_a_guessed_value() -> None:
    """The model cannot hide a guess under the not-found state."""

    with pytest.raises(ValidationError):
        EvidenceFact(
            key=FactKey.TIME,
            normalized_value="10:30",
            source_excerpt=None,
            status=EvidenceStatus.NOT_FOUND,
        )
