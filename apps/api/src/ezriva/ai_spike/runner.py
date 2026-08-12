"""Bounded sequential runner and content-safe evaluation report.

Module: runner
Purpose: Enforce the eight-attempt cap and retain only safe evaluation metrics.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal, Protocol

from pydantic import Field

from ezriva.ai_spike.catalog import FixtureManifest, verify_manifest
from ezriva.ai_spike.gate import GateDisposition, ReasonCode, evaluate_candidate
from ezriva.ai_spike.schemas import DocumentBriefCandidate, FactKey, StrictSpikeModel

LOGGER = logging.getLogger(__name__)
HERO_FIXTURE_ID = "he-clinic-appointment-01"
MAX_AUTHORIZED_INFERENCES = 8
TERMINAL_PROVIDER_FAILURES = frozenset(
    {
        "aws_credentials_missing",
        "aws_provider_error",
        "aws_session_expired",
        "bedrock_access_denied",
        "bedrock_provider_error",
        "bedrock_request_rejected",
        "model_invocation_failed",
        "model_not_found",
        "model_not_ready",
        "model_throttled_no_retry",
    }
)


class ProviderObservation(StrictSpikeModel):
    """Safe provider result; raw prompts/messages are deliberately absent."""

    candidate: DocumentBriefCandidate | None = None
    latency_ms: int = Field(ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    cycle_count: int = Field(default=0, ge=0, le=1)
    failure_code: str | None = Field(default=None, pattern=r"^[a-z0-9_]+$", max_length=80)


class FixtureAnalyzer(Protocol):
    """Provider boundary used by live Strands and offline fakes."""

    model_id: str
    region: str

    def analyze(self, image_bytes: bytes) -> ProviderObservation:
        """Analyze one image exactly once."""


class EvidenceReview(StrictSpikeModel):
    """Minimal synthetic evidence retained for Kevin's manual hero review."""

    key: FactKey
    normalized_value: str
    source_excerpt: str


class HeroReview(StrictSpikeModel):
    """Plain Spanish summary and Hebrew evidence for the synthetic hero only."""

    plain_summary: str
    evidence: tuple[EvidenceReview, ...]


class FixtureEvaluationRecord(StrictSpikeModel):
    """Content-minimized result for one fixture attempt."""

    fixture_id: str
    expected_disposition: GateDisposition
    expected_reason_codes: tuple[ReasonCode, ...] = ()
    observed_disposition: GateDisposition | None = None
    reason_codes: tuple[ReasonCode, ...] = ()
    schema_valid: bool
    expected_behavior_met: bool
    latency_ms: int = Field(ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    cycle_count: int = Field(default=0, ge=0, le=1)
    failure_code: str | None = None
    hero_review: HeroReview | None = None
    executable: Literal[False] = False


class EvaluationReport(StrictSpikeModel):
    """Sanitized report for one bounded Bedrock evaluation run."""

    schema_version: int = 1
    generated_at: datetime
    model_id: str
    region: str
    authorized_inference_cap: int = Field(ge=1, le=8)
    attempted_inferences: int = Field(ge=0, le=8)
    fixtures: tuple[FixtureEvaluationRecord, ...]
    raw_content_retained: bool = False
    action_tools_exposed: tuple[str, ...] = ()


def _hero_review(candidate: DocumentBriefCandidate) -> HeroReview:
    evidence = tuple(
        EvidenceReview(
            key=fact.key,
            normalized_value=fact.normalized_value,
            source_excerpt=fact.source_excerpt,
        )
        for fact in candidate.facts
        if fact.normalized_value is not None and fact.source_excerpt is not None
    )
    return HeroReview(plain_summary=candidate.plain_summary, evidence=evidence)


def run_evaluation(
    *,
    root: Path,
    manifest: FixtureManifest,
    analyzer: FixtureAnalyzer,
    inference_cap: int = MAX_AUTHORIZED_INFERENCES,
    clock: Callable[[], datetime] | None = None,
) -> EvaluationReport:
    """Run each allowlisted fixture once, sequentially, without retries.

    Args:
        root: Isolated Ezriva repository root.
        manifest: Validated eight-fixture allowlist.
        analyzer: Provider adapter with no action tools.
        inference_cap: Hard upper bound authorized for this run.
        clock: Injectable aware timestamp source for deterministic tests.

    Returns:
        A content-safe report with metrics and the synthetic hero review.

    Raises:
        ValueError: If the cap or manifest could exceed eight calls.
    """

    if not 1 <= inference_cap <= MAX_AUTHORIZED_INFERENCES:
        raise ValueError("inference cap must be between one and eight")
    if len(manifest.fixtures) > inference_cap:
        raise ValueError("fixture count exceeds the authorized inference cap")
    verify_manifest(root, manifest)

    records: list[FixtureEvaluationRecord] = []
    for fixture in manifest.fixtures:
        image_bytes = (root / fixture.image_path).read_bytes()
        source_text = (root / fixture.source_path).read_text(encoding="utf-8")
        LOGGER.info("fixture_id=%s | starting bounded analysis", fixture.id)
        try:
            observation = analyzer.analyze(image_bytes)
        except Exception:
            observation = ProviderObservation(latency_ms=0, failure_code="provider_boundary_error")

        candidate = observation.candidate
        if candidate is None:
            record = FixtureEvaluationRecord(
                fixture_id=fixture.id,
                expected_disposition=fixture.expected_disposition,
                expected_reason_codes=fixture.expected_reason_codes,
                schema_valid=False,
                expected_behavior_met=False,
                latency_ms=observation.latency_ms,
                input_tokens=observation.input_tokens,
                output_tokens=observation.output_tokens,
                total_tokens=observation.total_tokens,
                cycle_count=observation.cycle_count,
                failure_code=observation.failure_code or "structured_output_missing",
            )
        else:
            decision = evaluate_candidate(candidate, source_text)
            reasons_met = set(fixture.expected_reason_codes).issubset(decision.reason_codes)
            record = FixtureEvaluationRecord(
                fixture_id=fixture.id,
                expected_disposition=fixture.expected_disposition,
                expected_reason_codes=fixture.expected_reason_codes,
                observed_disposition=decision.disposition,
                reason_codes=decision.reason_codes,
                schema_valid=True,
                expected_behavior_met=(
                    decision.disposition is fixture.expected_disposition and reasons_met
                ),
                latency_ms=observation.latency_ms,
                input_tokens=observation.input_tokens,
                output_tokens=observation.output_tokens,
                total_tokens=observation.total_tokens,
                cycle_count=observation.cycle_count,
                failure_code=observation.failure_code,
                hero_review=_hero_review(candidate) if fixture.id == HERO_FIXTURE_ID else None,
            )
        records.append(record)
        LOGGER.info(
            "fixture_id=%s status=%s | bounded analysis finished",
            fixture.id,
            "met" if record.expected_behavior_met else "not_met",
        )
        if observation.failure_code in TERMINAL_PROVIDER_FAILURES:
            LOGGER.info("terminal provider failure | remaining fixtures were not attempted")
            break

    now = clock or (lambda: datetime.now(UTC))
    generated_at = now()
    if generated_at.tzinfo is None or generated_at.utcoffset() is None:
        raise ValueError("report clock must return an aware datetime")
    return EvaluationReport(
        generated_at=generated_at,
        model_id=analyzer.model_id,
        region=analyzer.region,
        authorized_inference_cap=inference_cap,
        attempted_inferences=len(records),
        fixtures=tuple(records),
    )
