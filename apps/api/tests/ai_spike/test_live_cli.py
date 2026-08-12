"""Live item-2 command and attempt-ledger tests without AWS calls.

Module: test_live_cli
Purpose: Prove metering, safe configuration errors, and process exit semantics.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest

from ezriva.ai_spike.runner import ProviderObservation
from tests.ai_spike.candidates import candidates_in_manifest_order

ROOT = Path(__file__).resolve().parents[4]
LIVE_EVAL_SPEC = spec_from_file_location(
    "ezriva_live_eval_script",
    ROOT / "scripts" / "run_ai_fixture_eval.py",
)
if LIVE_EVAL_SPEC is None or LIVE_EVAL_SPEC.loader is None:
    raise RuntimeError("could not load the live evaluation entry point")
live_eval = module_from_spec(LIVE_EVAL_SPEC)
LIVE_EVAL_SPEC.loader.exec_module(live_eval)


class InspectingAnalyzer:
    """Observe the ledger state seen immediately before a provider call."""

    model_id = "public.test-model-v1"
    region = "us-test-1"

    def __init__(self, ledger_path: Path, *, fail: bool = False) -> None:
        self.ledger_path = ledger_path
        self.fail = fail
        self.calls = 0
        self.status_seen: str | None = None

    def analyze(self, image_bytes: bytes) -> ProviderObservation:
        assert image_bytes == b"synthetic-only"
        self.calls += 1
        ledger = json.loads(self.ledger_path.read_text(encoding="utf-8"))
        self.status_seen = ledger["attempts"][-1]["status"]
        if self.fail:
            raise RuntimeError("private-provider-sentinel")
        return ProviderObservation(latency_ms=12, cycle_count=1)


def _fixed_clock() -> datetime:
    return datetime(2026, 8, 12, 10, 0, tzinfo=UTC)


def test_ledger_is_pending_before_provider_and_completed_afterward(tmp_path: Path) -> None:
    """A crash cannot hide that an inference may already have been consumed."""

    ledger_path = tmp_path / "attempt-ledger.json"
    delegate = InspectingAnalyzer(ledger_path)
    analyzer = live_eval.LedgerAnalyzer(
        delegate,
        cap=8,
        ledger_path=ledger_path,
        clock=_fixed_clock,
    )

    analyzer.analyze(b"synthetic-only")

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    assert delegate.status_seen == "pending"
    assert ledger["attempts"][0]["status"] == "completed"
    assert ledger["attempts"][0]["completed_at"] is not None


def test_ledger_records_boundary_error_without_raw_exception(tmp_path: Path) -> None:
    """Provider details never enter the content-free attempt ledger."""

    ledger_path = tmp_path / "attempt-ledger.json"
    analyzer = live_eval.LedgerAnalyzer(
        InspectingAnalyzer(ledger_path, fail=True),
        cap=8,
        ledger_path=ledger_path,
        clock=_fixed_clock,
    )

    with pytest.raises(RuntimeError):
        analyzer.analyze(b"synthetic-only")

    serialized = ledger_path.read_text(encoding="utf-8")
    ledger = json.loads(serialized)
    assert ledger["attempts"][0]["status"] == "boundary_error"
    assert ledger["attempts"][0]["failure_code"] == "provider_boundary_error"
    assert "private-provider-sentinel" not in serialized


def test_ledger_reservation_is_exclusive_and_cap_is_enforced(tmp_path: Path) -> None:
    """A second process or call cannot reuse one authorization reservation."""

    ledger_path = tmp_path / "attempt-ledger.json"
    delegate = InspectingAnalyzer(ledger_path)
    analyzer = live_eval.LedgerAnalyzer(
        delegate,
        cap=1,
        ledger_path=ledger_path,
        clock=_fixed_clock,
    )

    with pytest.raises(live_eval.AttemptLedgerExistsError):
        live_eval.LedgerAnalyzer(
            delegate,
            cap=1,
            ledger_path=ledger_path,
            clock=_fixed_clock,
        )

    analyzer.analyze(b"synthetic-only")
    with pytest.raises(RuntimeError, match="cap exhausted"):
        analyzer.analyze(b"synthetic-only")
    assert delegate.calls == 1


def test_json_persistence_recovers_from_a_transient_windows_lock(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """A brief scanner lock cannot make the content-free ledger intermittent."""

    path = tmp_path / "ledger.json"
    path.write_text("{}\n", encoding="utf-8")
    real_replace = live_eval.os.replace
    attempts = 0

    def transiently_locked(source: Path, destination: Path) -> None:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise PermissionError("synthetic transient lock")
        real_replace(source, destination)

    monkeypatch.setattr(live_eval.os, "replace", transiently_locked)

    live_eval._write_json(path, {"attempts": []})

    assert attempts == 2
    assert json.loads(path.read_text(encoding="utf-8")) == {"attempts": []}


def _configure_live_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_FIXTURE_LIVE_ENABLED", "true")
    monkeypatch.setenv("AWS_REGION", "us-test-1")
    monkeypatch.setenv("BEDROCK_MODEL_ID", "public.test-model-v1")


def test_live_command_returns_zero_only_for_eight_matching_results(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Automated success still states that Kevin's Pause 1 is pending."""

    _configure_live_environment(monkeypatch)
    monkeypatch.setattr(live_eval, "LEDGER_PATH", tmp_path / "private" / "ledger.json")
    monkeypatch.setattr(live_eval, "REPORT_PATH", tmp_path / "report.json")
    monkeypatch.setattr(live_eval, "verify_live_preflight", lambda region, model_id: object())

    class SuccessfulAnalyzer:
        model_id = "public.test-model-v1"
        region = "us-test-1"

        def __init__(self) -> None:
            self.candidates = candidates_in_manifest_order()
            self.calls = 0

        def analyze(self, image_bytes: bytes) -> ProviderObservation:
            assert image_bytes.startswith(b"\x89PNG")
            candidate = self.candidates[self.calls]
            self.calls += 1
            return ProviderObservation(candidate=candidate, latency_ms=1, cycle_count=1)

    successful = SuccessfulAnalyzer()
    monkeypatch.setattr(live_eval, "StrandsBedrockAnalyzer", lambda **kwargs: successful)

    exit_code = live_eval.main(["--live", "--acknowledge-metered-bedrock"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "8/8 attempted" in output
    assert "8/8 expected safety behaviors" in output
    assert "Pause 1 manual review is still required" in output


def test_live_command_returns_one_for_a_partial_terminal_failure(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A first-call terminal failure reports one of eight, never one of one."""

    _configure_live_environment(monkeypatch)
    monkeypatch.setattr(live_eval, "LEDGER_PATH", tmp_path / "private" / "ledger.json")
    monkeypatch.setattr(live_eval, "REPORT_PATH", tmp_path / "report.json")
    monkeypatch.setattr(live_eval, "verify_live_preflight", lambda region, model_id: object())

    class TerminalAnalyzer:
        model_id = "public.test-model-v1"
        region = "us-test-1"

        def analyze(self, image_bytes: bytes) -> ProviderObservation:
            assert image_bytes.startswith(b"\x89PNG")
            return ProviderObservation(
                latency_ms=1,
                failure_code="bedrock_access_denied",
            )

    monkeypatch.setattr(live_eval, "StrandsBedrockAnalyzer", lambda **kwargs: TerminalAnalyzer())

    exit_code = live_eval.main(["--live", "--acknowledge-metered-bedrock"])

    output = capsys.readouterr().out
    assert exit_code == 1
    assert "1/8 attempted" in output
    assert "0/8 expected safety behaviors" in output
    assert "7 not attempted" in output


def test_live_command_redacts_invalid_configuration_before_aws(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """An account-bearing model value is neither printed nor sent to AWS discovery."""

    account_id = "123456789012"
    _configure_live_environment(monkeypatch)
    monkeypatch.setenv(
        "BEDROCK_MODEL_ID",
        f"arn:aws:bedrock:us-test-1:{account_id}:inference-profile/private",
    )

    def unexpected_preflight(region: str, model_id: str) -> object:
        raise AssertionError(f"unexpected AWS preflight for {region}/{model_id}")

    monkeypatch.setattr(live_eval, "verify_live_preflight", unexpected_preflight)

    exit_code = live_eval.main(["--live", "--acknowledge-metered-bedrock"])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert "invalid configuration" in captured.err
    assert account_id not in captured.err
