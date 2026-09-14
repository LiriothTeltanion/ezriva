"""Extraction-only schemas for the bounded Hebrew model spike.

Module: schemas
Purpose: Validate model observations without granting action authority.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from enum import StrEnum
from typing import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

HEBREW_PATTERN = re.compile(r"[\u0590-\u05ff]")
BIDI_CONTROLS = frozenset(
    {
        "\u061c",
        "\u200e",
        "\u200f",
        "\u202a",
        "\u202b",
        "\u202c",
        "\u202d",
        "\u202e",
        "\u2066",
        "\u2067",
        "\u2068",
        "\u2069",
    }
)


def _contains_bidi_control(value: object) -> bool:
    """Return whether nested untrusted model data contains a bidi control."""

    if isinstance(value, str):
        return any(character in BIDI_CONTROLS for character in value)
    if isinstance(value, Mapping):
        return any(_contains_bidi_control(item) for item in value.values())
    if isinstance(value, (list, tuple, set, frozenset)):
        return any(_contains_bidi_control(item) for item in value)
    return False


class LanguageCode(StrEnum):
    """Languages allowed in the item-2 candidate."""

    HEBREW = "he"
    SPANISH = "es"
    ENGLISH = "en"
    UNKNOWN = "unknown"


class DocumentType(StrEnum):
    """Small document taxonomy needed by the fixture gate."""

    APPOINTMENT = "appointment"
    BILL = "bill"
    NOTICE = "notice"
    HIGH_RISK = "high_risk"
    UNKNOWN = "unknown"


class Readability(StrEnum):
    """Observable image-readability states."""

    READABLE = "readable"
    PARTIAL = "partial"
    UNREADABLE = "unreadable"


class FactKey(StrEnum):
    """Evidence-backed fact keys accepted from the model."""

    SENDER = "sender"
    DATE = "date"
    TIME = "time"
    LOCATION = "location"
    AMOUNT = "amount"
    CONTACT = "contact"
    REQUESTED_ACTION = "requested_action"


class EvidenceStatus(StrEnum):
    """Non-numeric evidence states used by deterministic policy."""

    CONFIRMED = "confirmed"
    UNCERTAIN = "uncertain"
    CONFLICTING = "conflicting"
    NOT_FOUND = "not_found"


class RiskSignalKind(StrEnum):
    """Bounded risk signals; they never authorize a tool."""

    PROMPT_INJECTION = "prompt_injection"
    MEDICAL_DECISION = "medical_decision"
    LEGAL_DECISION = "legal_decision"
    PAYMENT_REQUEST = "payment_request"
    IDENTITY_REQUEST = "identity_request"
    FORM_SUBMISSION = "form_submission"


class StrictSpikeModel(BaseModel):
    """Base configuration for untrusted structured model output."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    @model_validator(mode="before")
    @classmethod
    def reject_bidi_controls(cls, value: object) -> object:
        """Reject invisible direction controls before nested validation."""

        if _contains_bidi_control(value):
            raise ValueError("structured text cannot contain bidi control characters")
        return value


class EvidenceFact(StrictSpikeModel):
    """One normalized fact tied to a short source excerpt."""

    key: FactKey
    normalized_value: str | None = Field(default=None, max_length=240)
    source_excerpt: str | None = Field(default=None, max_length=280)
    status: EvidenceStatus
    reason: str | None = Field(default=None, max_length=240)

    @model_validator(mode="after")
    def validate_status_contract(self) -> Self:
        """Require confirmed facts to carry a Hebrew citation and value."""

        if self.status is EvidenceStatus.CONFIRMED:
            if not self.normalized_value or not self.source_excerpt:
                raise ValueError("confirmed facts require a value and source excerpt")
            if HEBREW_PATTERN.search(self.source_excerpt) is None:
                raise ValueError("confirmed facts require Hebrew source evidence")
        if self.status is EvidenceStatus.NOT_FOUND and (
            self.normalized_value is not None or self.source_excerpt is not None
        ):
            raise ValueError("not_found facts cannot contain a value or source excerpt")
        return self


class Uncertainty(StrictSpikeModel):
    """A bounded uncertainty explanation."""

    field: FactKey
    reason: str = Field(min_length=3, max_length=240)
    source_excerpt: str | None = Field(default=None, max_length=280)


class RiskSignal(StrictSpikeModel):
    """A risk observation with optional source evidence."""

    kind: RiskSignalKind
    reason: str = Field(min_length=3, max_length=240)
    source_excerpt: str | None = Field(default=None, max_length=280)


class DocumentBriefCandidate(StrictSpikeModel):
    """Model candidate containing facts only, never an executable action."""

    detected_languages: tuple[LanguageCode, ...] = Field(min_length=1, max_length=3)
    target_language: LanguageCode = LanguageCode.SPANISH
    document_type: DocumentType
    readability: Readability
    readability_reason: str | None = Field(default=None, max_length=240)
    plain_summary: str = Field(min_length=20, max_length=700)
    facts: tuple[EvidenceFact, ...] = Field(min_length=1, max_length=14)
    uncertainties: tuple[Uncertainty, ...] = Field(default=(), max_length=8)
    risk_signals: tuple[RiskSignal, ...] = Field(default=(), max_length=8)
    suggested_next_step: str | None = Field(default=None, max_length=280)

    @model_validator(mode="after")
    def validate_candidate_contract(self) -> Self:
        """Keep the spike Spanish-targeted and free of duplicate risk labels."""

        if self.target_language is not LanguageCode.SPANISH:
            raise ValueError("the item-2 spike target language must be Spanish")
        risk_kinds = [signal.kind for signal in self.risk_signals]
        if len(risk_kinds) != len(set(risk_kinds)):
            raise ValueError("risk signal kinds must be unique")
        return self
