"""Read-only AWS preflight tests.

Module: test_preflight
Purpose: Prove live evaluation refuses unsafe logging or unavailable model configuration.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from __future__ import annotations

from typing import Protocol, cast

import pytest

from ezriva.ai_spike import preflight


class RetryConfig(Protocol):
    """Structural view of the botocore setting inspected by this test."""

    retries: dict[str, object]


class FakePaginator:
    """Return fixed, typed inference-profile discovery pages."""

    def __init__(self, pages: tuple[dict[str, object], ...]) -> None:
        self._pages = pages

    def paginate(self, **kwargs: str) -> tuple[dict[str, object], ...]:
        assert kwargs == {"typeEquals": "SYSTEM_DEFINED"}
        return self._pages


class FakeBedrock:
    """Minimal Bedrock control-plane fake with no model invocation method."""

    def __init__(
        self,
        *,
        logging_config: dict[str, object] | None = None,
        foundation_models: list[dict[str, object]] | None = None,
        profile_pages: tuple[dict[str, object], ...] = (),
    ) -> None:
        self.logging_config = logging_config or {}
        self.foundation_models = foundation_models or []
        self.profile_pages = profile_pages
        self.list_calls = 0

    def get_model_invocation_logging_configuration(self) -> dict[str, object]:
        return self.logging_config

    def list_foundation_models(self, **kwargs: str) -> dict[str, object]:
        assert kwargs == {"byOutputModality": "TEXT"}
        self.list_calls += 1
        return {"modelSummaries": self.foundation_models}

    def get_paginator(self, operation: str) -> FakePaginator:
        assert operation == "list_inference_profiles"
        return FakePaginator(self.profile_pages)


class FakeSession:
    """Minimal credentialed boto3 session fake."""

    def __init__(self, bedrock: FakeBedrock, credentials: object | None = object()) -> None:
        self._bedrock = bedrock
        self._credentials = credentials
        self.client_config: object | None = None

    def get_credentials(self) -> object | None:
        return self._credentials

    def client(
        self,
        service_name: str,
        *,
        region_name: str,
        config: object,
    ) -> FakeBedrock:
        assert service_name == "bedrock"
        assert region_name == "us-test-1"
        self.client_config = config
        return self._bedrock


def _install_session(monkeypatch: pytest.MonkeyPatch, session: FakeSession) -> None:
    def session_factory(region: str) -> FakeSession:
        assert region == "us-test-1"
        return session

    monkeypatch.setattr(preflight, "_aws_session", session_factory)


def test_preflight_accepts_configured_active_vision_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A visible active image-input model passes read-only discovery."""

    model_id = "anthropic.synthetic-vision-v1"
    bedrock = FakeBedrock(
        foundation_models=[
            {
                "modelId": model_id,
                "inputModalities": ["TEXT", "IMAGE"],
                "modelLifecycle": {"status": "ACTIVE"},
            }
        ]
    )
    session = FakeSession(bedrock)
    _install_session(monkeypatch, session)

    result = preflight.verify_live_preflight("us-test-1", model_id)

    assert result is session
    assert cast(RetryConfig, session.client_config).retries == {
        "total_max_attempts": 1,
        "mode": "standard",
    }


def test_preflight_accepts_configured_active_inference_profile(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """An active system profile is discovered by configured public ID."""

    profile_id = "global.anthropic.synthetic-vision-v1"
    bedrock = FakeBedrock(
        profile_pages=(
            {"inferenceProfileSummaries": [{"inferenceProfileId": profile_id, "status": "ACTIVE"}]},
        )
    )
    session = FakeSession(bedrock)
    _install_session(monkeypatch, session)

    result = preflight.verify_live_preflight("us-test-1", profile_id)

    assert result is session


def test_preflight_refuses_bedrock_content_logging(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Fixture bytes never leave the process when provider logging is enabled."""

    bedrock = FakeBedrock(logging_config={"loggingConfig": {"textDataDeliveryEnabled": True}})
    _install_session(monkeypatch, FakeSession(bedrock))

    with pytest.raises(preflight.PreflightError) as captured:
        preflight.verify_live_preflight("us-test-1", "model-id")

    assert captured.value.code == "bedrock_model_invocation_logging_enabled"
    assert bedrock.list_calls == 0


def test_preflight_refuses_missing_credentials(monkeypatch: pytest.MonkeyPatch) -> None:
    """A live run cannot fall through to provider discovery without credentials."""

    bedrock = FakeBedrock()
    _install_session(monkeypatch, FakeSession(bedrock, credentials=None))

    with pytest.raises(preflight.PreflightError) as captured:
        preflight.verify_live_preflight("us-test-1", "model-id")

    assert captured.value.code == "aws_credentials_missing"
    assert bedrock.list_calls == 0


def test_preflight_refuses_model_id_not_visible_in_configured_region(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The live runner cannot silently substitute a remembered model ID."""

    bedrock = FakeBedrock()
    _install_session(monkeypatch, FakeSession(bedrock))

    with pytest.raises(preflight.PreflightError) as captured:
        preflight.verify_live_preflight("us-test-1", "missing-model")

    assert captured.value.code == "bedrock_model_not_available"
