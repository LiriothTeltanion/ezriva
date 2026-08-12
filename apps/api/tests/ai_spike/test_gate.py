"""Deterministic fixture gate tests.

Module: test_gate
Purpose: Prove unsafe or uncertain candidates remain non-executable.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from pathlib import Path

import pytest

from ezriva.ai_spike.gate import GateDisposition, ReasonCode, evaluate_candidate
from ezriva.ai_spike.schemas import DocumentBriefCandidate, EvidenceStatus
from tests.ai_spike.candidates import (
    ambiguous_candidate,
    bill_candidate,
    blurry_candidate,
    conflicting_candidate,
    hero_candidate,
    high_risk_candidate,
    injection_candidate,
    no_action_candidate,
)

ROOT = Path(__file__).resolve().parents[4]


def _source(identifier: str) -> str:
    return (ROOT / "fixtures" / "synthetic" / f"{identifier}.txt").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("identifier", "candidate", "expected"),
    (
        (
            "he-clinic-appointment-01",
            hero_candidate(),
            GateDisposition.ELIGIBLE_FOR_REMINDER_REVIEW,
        ),
        (
            "he-blurry-appointment-01",
            blurry_candidate(),
            GateDisposition.NEEDS_CLEARER_INPUT,
        ),
        ("he-ambiguous-date-01", ambiguous_candidate(), GateDisposition.NEEDS_CLARIFICATION),
        (
            "he-conflicting-dates-01",
            conflicting_candidate(),
            GateDisposition.NEEDS_CLARIFICATION,
        ),
        ("he-high-risk-medical-01", high_risk_candidate(), GateDisposition.BLOCKED_HIGH_RISK),
        (
            "he-bill-due-date-01",
            bill_candidate(),
            GateDisposition.ELIGIBLE_FOR_REMINDER_REVIEW,
        ),
        ("he-no-action-notice-01", no_action_candidate(), GateDisposition.READ_ONLY),
        (
            "he-prompt-injection-01",
            injection_candidate(),
            GateDisposition.BLOCKED_UNTRUSTED_CONTENT,
        ),
    ),
)
def test_all_eight_fixture_dispositions(
    identifier: str,
    candidate: DocumentBriefCandidate,
    expected: GateDisposition,
) -> None:
    """Each fixture reaches its expected safe state and never becomes executable."""

    decision = evaluate_candidate(candidate, _source(identifier))

    assert decision.disposition is expected
    assert decision.executable is False


def test_bill_can_only_reach_reminder_review() -> None:
    """A clear due date does not turn a payment request into payment authority."""

    decision = evaluate_candidate(bill_candidate(), _source("he-bill-due-date-01"))

    assert ReasonCode.PAYMENT_NOT_SUPPORTED in decision.reason_codes
    assert decision.executable is False


def test_ungrounded_hebrew_excerpt_invalidates_the_candidate() -> None:
    """Schema-valid invented evidence fails the deterministic source comparison."""

    payload = hero_candidate().model_dump(mode="json")
    payload["facts"][0]["source_excerpt"] = "מרכז שלא קיים במסמך"
    candidate = DocumentBriefCandidate.model_validate(payload)

    decision = evaluate_candidate(candidate, _source("he-clinic-appointment-01"))

    assert decision.disposition is GateDisposition.INVALID_EVIDENCE


def test_ambiguous_numeric_date_blocks_even_if_model_calls_it_confirmed() -> None:
    """A model-selected interpretation cannot bypass the numeric-date rule."""

    payload = ambiguous_candidate().model_dump(mode="json")
    payload["facts"][0]["status"] = EvidenceStatus.CONFIRMED.value
    payload["uncertainties"] = []
    candidate = DocumentBriefCandidate.model_validate(payload)

    decision = evaluate_candidate(candidate, _source("he-ambiguous-date-01"))

    assert decision.disposition is GateDisposition.NEEDS_CLARIFICATION
    assert ReasonCode.AMBIGUOUS_NUMERIC_DATE in decision.reason_codes


def test_injection_takes_precedence_over_an_otherwise_clear_date() -> None:
    """A date inside malicious text cannot produce reminder eligibility."""

    decision = evaluate_candidate(injection_candidate(), _source("he-prompt-injection-01"))

    assert decision.disposition is GateDisposition.BLOCKED_UNTRUSTED_CONTENT


def test_source_with_two_dates_blocks_even_if_model_selects_only_one() -> None:
    """Omitting the second visible date cannot make the fixture eligible."""

    payload = conflicting_candidate().model_dump(mode="json")
    payload["facts"] = [payload["facts"][0], payload["facts"][2], payload["facts"][3]]
    payload["facts"][0]["status"] = EvidenceStatus.CONFIRMED.value
    payload["uncertainties"] = []
    candidate = DocumentBriefCandidate.model_validate(payload)

    decision = evaluate_candidate(candidate, _source("he-conflicting-dates-01"))

    assert decision.disposition is GateDisposition.NEEDS_CLARIFICATION
    assert ReasonCode.MULTIPLE_ACTIONABLE_DATES in decision.reason_codes


def test_bidi_control_is_treated_as_untrusted_content() -> None:
    """Hidden direction controls cannot conceal action instructions."""

    source = _source("he-clinic-appointment-01") + "\u202e"

    decision = evaluate_candidate(hero_candidate(), source)

    assert decision.disposition is GateDisposition.BLOCKED_UNTRUSTED_CONTENT
    assert ReasonCode.BIDI_CONTROL in decision.reason_codes
