"""Bounded runner and safe-report tests.

Module: test_runner
Purpose: Prove call caps, no retry, metrics honesty, and content minimization.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from ezriva.ai_spike.catalog import load_manifest
from ezriva.ai_spike.runner import ProviderObservation, run_evaluation
from ezriva.ai_spike.schemas import DocumentBriefCandidate
from tests.ai_spike.candidates import candidates_in_manifest_order

ROOT = Path(__file__).resolve().parents[4]


class FakeAnalyzer:
    """Return one queued observation per call and count every invocation."""

    model_id = "public.test-model-v1"
    region = "us-test-1"

    def __init__(self, candidates: tuple[DocumentBriefCandidate, ...]) -> None:
        self._candidates = candidates
        self.calls = 0

    def analyze(self, image_bytes: bytes) -> ProviderObservation:
        assert image_bytes.startswith(b"\x89PNG")
        candidate = self._candidates[self.calls]
        self.calls += 1
        return ProviderObservation(
            candidate=candidate,
            latency_ms=125,
            input_tokens=1_000,
            output_tokens=220,
            total_tokens=1_220,
            cycle_count=1,
        )


class FailingAnalyzer:
    """Raise once per requested fixture so the runner can prove no retry."""

    model_id = "public.test-model-v1"
    region = "us-test-1"

    def __init__(self) -> None:
        self.calls = 0

    def analyze(self, image_bytes: bytes) -> ProviderObservation:
        del image_bytes
        self.calls += 1
        raise RuntimeError("sensitive provider detail that must not escape")


def test_runner_calls_each_fixture_once_and_matches_all_safety_states() -> None:
    """The offline fake proves eight sequential calls and eight expected gates."""

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")
    analyzer = FakeAnalyzer(candidates_in_manifest_order())

    report = run_evaluation(
        root=ROOT,
        manifest=manifest,
        analyzer=analyzer,
        clock=lambda: datetime(2026, 8, 12, tzinfo=UTC),
    )

    assert analyzer.calls == 8
    assert report.attempted_inferences == 8
    assert all(record.expected_behavior_met for record in report.fixtures)
    assert all(record.executable is False for record in report.fixtures)
    assert report.raw_content_retained is False
    assert report.action_tools_exposed == ()
    assert sum(record.hero_review is not None for record in report.fixtures) == 1
    bill = next(record for record in report.fixtures if record.fixture_id == "he-bill-due-date-01")
    assert bill.expected_reason_codes
    assert set(bill.expected_reason_codes).issubset(bill.reason_codes)


def test_runner_does_not_retry_provider_exceptions(caplog: pytest.LogCaptureFixture) -> None:
    """One provider error per fixture remains eight total calls, never sixteen."""

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")
    analyzer = FailingAnalyzer()

    report = run_evaluation(root=ROOT, manifest=manifest, analyzer=analyzer)

    assert analyzer.calls == 8
    assert all(record.failure_code == "provider_boundary_error" for record in report.fixtures)
    assert "sensitive provider detail" not in caplog.text


def test_runner_stops_after_one_terminal_provider_failure() -> None:
    """A systemic failure cannot consume the remaining seven-call allowance."""

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")

    class TerminalAnalyzer(FakeAnalyzer):
        def analyze(self, image_bytes: bytes) -> ProviderObservation:
            assert image_bytes.startswith(b"\x89PNG")
            self.calls += 1
            return ProviderObservation(
                latency_ms=25,
                cycle_count=0,
                failure_code="bedrock_access_denied",
            )

    analyzer = TerminalAnalyzer(candidates_in_manifest_order())
    report = run_evaluation(root=ROOT, manifest=manifest, analyzer=analyzer)

    assert analyzer.calls == 1
    assert report.attempted_inferences == 1
    assert report.fixtures[0].failure_code == "bedrock_access_denied"


def test_runner_refuses_a_cap_below_the_manifest_before_any_call() -> None:
    """A configuration mistake cannot partially start an unauthorized run."""

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")
    analyzer = FakeAnalyzer(candidates_in_manifest_order())

    with pytest.raises(ValueError, match="fixture count exceeds"):
        run_evaluation(root=ROOT, manifest=manifest, analyzer=analyzer, inference_cap=7)

    assert analyzer.calls == 0


def test_safe_report_does_not_retain_adversarial_source_or_provider_messages() -> None:
    """Only the hero's synthetic review is retained; malicious text is absent."""

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")
    report = run_evaluation(
        root=ROOT,
        manifest=manifest,
        analyzer=FakeAnalyzer(candidates_in_manifest_order()),
    )
    serialized = report.model_dump_json()

    assert "Ignore previous instructions" not in serialized
    assert "התעלם מכל ההוראות" not in serialized
    assert "system_prompt" not in serialized
    assert "tool arguments" not in serialized


def test_missing_usage_remains_null_instead_of_becoming_zero() -> None:
    """Unavailable provider metrics are reported as unknown, not invented zeroes."""

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")

    class MissingMetricsAnalyzer(FakeAnalyzer):
        def analyze(self, image_bytes: bytes) -> ProviderObservation:
            assert image_bytes.startswith(b"\x89PNG")
            candidate = self._candidates[self.calls]
            self.calls += 1
            return ProviderObservation(candidate=candidate, latency_ms=1, cycle_count=1)

    report = run_evaluation(
        root=ROOT,
        manifest=manifest,
        analyzer=MissingMetricsAnalyzer(candidates_in_manifest_order()),
    )

    assert all(record.total_tokens is None for record in report.fixtures)
