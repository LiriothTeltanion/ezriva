"""Strands/Bedrock adapter contract tests.

Module: test_strands_bedrock
Purpose: Prove one-turn multimodal extraction exposes no action tools or retries.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from __future__ import annotations

from typing import Protocol, cast

import pytest

from ezriva.ai_spike import strands_bedrock
from ezriva.ai_spike.schemas import DocumentBriefCandidate
from tests.ai_spike.candidates import hero_candidate


class FakeMetrics:
    """Small metrics shape matching the allowlisted adapter reads."""

    def __init__(self, cycle_count: int = 1) -> None:
        self.cycle_count = cycle_count
        self.accumulated_usage = {
            "inputTokens": 900,
            "outputTokens": 180,
            "totalTokens": 1_080,
        }


class RetryConfig(Protocol):
    """Structural view of the botocore setting inspected by this test."""

    retries: dict[str, object]


class FakeResult:
    """Structured result without messages, prompts, or traces."""

    def __init__(self, candidate: DocumentBriefCandidate | None, cycle_count: int = 1) -> None:
        self.metrics = FakeMetrics(cycle_count)
        self.structured_output = candidate


class FakeAgent:
    """Capture exactly one structured-output invocation."""

    def __init__(
        self,
        candidate: DocumentBriefCandidate | None,
        error: Exception | None = None,
        cycle_count: int = 1,
    ) -> None:
        self._candidate = candidate
        self._error = error
        self._cycle_count = cycle_count
        self.calls = 0
        self.prompt: object | None = None
        self.invocation_kwargs: dict[str, object] = {}

    def __call__(self, prompt: object, **kwargs: object) -> FakeResult:
        self.calls += 1
        self.prompt = prompt
        self.invocation_kwargs = kwargs
        if self._error is not None:
            raise self._error
        return FakeResult(self._candidate, self._cycle_count)


class CapturingFactory:
    """Record constructor arguments and return one fixed object."""

    def __init__(self, result: object) -> None:
        self._result = result
        self.calls = 0
        self.kwargs: dict[str, object] = {}

    def __call__(self, **kwargs: object) -> object:
        self.calls += 1
        self.kwargs = kwargs
        return self._result


def _install_fakes(
    monkeypatch: pytest.MonkeyPatch,
    agent: FakeAgent,
) -> tuple[CapturingFactory, CapturingFactory]:
    model_factory = CapturingFactory(object())
    agent_factory = CapturingFactory(agent)
    monkeypatch.setattr(strands_bedrock, "BedrockModel", model_factory)
    monkeypatch.setattr(strands_bedrock, "Agent", agent_factory)
    return model_factory, agent_factory


def test_adapter_uses_one_turn_no_retry_and_no_action_tools(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The provider contract is bounded before any live fixture can run."""

    agent = FakeAgent(hero_candidate())
    model_factory, agent_factory = _install_fakes(monkeypatch, agent)
    analyzer = strands_bedrock.StrandsBedrockAnalyzer(
        boto_session=object(),
        region="us-test-1",
        model_id="public.test-model-v1",
        max_tokens=1_800,
    )

    observation = analyzer.analyze(b"\x89PNG\r\n\x1a\npublic-synthetic-image")

    assert observation.candidate == hero_candidate()
    assert observation.total_tokens == 1_080
    assert model_factory.calls == 1
    assert model_factory.kwargs["streaming"] is False
    assert model_factory.kwargs["strict_tools"] is False
    assert model_factory.kwargs["use_native_token_count"] is False
    client_config = model_factory.kwargs["boto_client_config"]
    assert cast(RetryConfig, client_config).retries == {
        "total_max_attempts": 1,
        "mode": "standard",
    }
    assert agent_factory.calls == 1
    assert agent_factory.kwargs["tools"] == []
    assert agent_factory.kwargs["callback_handler"] is None
    assert agent_factory.kwargs["retry_strategy"] is None
    assert agent_factory.kwargs["load_tools_from_directory"] is False
    assert agent.calls == 1
    invocation_limits = cast(dict[str, object], agent.invocation_kwargs["limits"])
    assert invocation_limits["turns"] == 1
    assert agent.invocation_kwargs["structured_output_model"] is DocumentBriefCandidate
    prompt = cast(list[dict[str, object]], agent.prompt)
    assert prompt[1] == {
        "image": {
            "format": "png",
            "source": {"bytes": b"\x89PNG\r\n\x1a\npublic-synthetic-image"},
        }
    }


def test_adapter_does_not_retry_or_log_raw_provider_failure(
    monkeypatch: pytest.MonkeyPatch,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """One unsafe provider failure becomes one stable, content-free result."""

    sensitive_detail = "raw fixture and provider request must stay private"
    agent = FakeAgent(None, error=RuntimeError(sensitive_detail))
    _install_fakes(monkeypatch, agent)
    analyzer = strands_bedrock.StrandsBedrockAnalyzer(
        boto_session=object(),
        region="us-test-1",
        model_id="public.test-model-v1",
        max_tokens=1_800,
    )

    observation = analyzer.analyze(b"\x89PNG\r\n\x1a\nprivate-sentinel")

    assert agent.calls == 1
    assert observation.failure_code == "model_invocation_failed"
    assert sensitive_detail not in caplog.text
    assert "private-sentinel" not in caplog.text


def test_adapter_reports_observed_cycle_limit_violation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A cycle violation is reported honestly and remains a terminal failure."""

    agent = FakeAgent(hero_candidate(), cycle_count=2)
    _install_fakes(monkeypatch, agent)
    analyzer = strands_bedrock.StrandsBedrockAnalyzer(
        boto_session=object(),
        region="us-test-1",
        model_id="public.test-model-v1",
        max_tokens=1_800,
    )

    observation = analyzer.analyze(b"\x89PNG\r\n\x1a\npublic-synthetic-image")

    assert observation.cycle_count == 2
    assert observation.failure_code == "inference_cycle_limit_exceeded"
