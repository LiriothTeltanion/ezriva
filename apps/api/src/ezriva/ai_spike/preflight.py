"""Read-only AWS preflight for the metered item-2 evaluation.

Module: preflight
Purpose: Refuse live document inference without credentials and disabled content logging.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from __future__ import annotations

from collections.abc import Mapping

import boto3  # type: ignore[import-untyped]
from botocore.config import Config  # type: ignore[import-untyped]
from botocore.exceptions import BotoCoreError, ClientError  # type: ignore[import-untyped]

NO_RETRY_CONFIG = Config(
    connect_timeout=10,
    read_timeout=30,
    retries={"total_max_attempts": 1, "mode": "standard"},
    user_agent_extra="ezriva-item-2-preflight",
)


class PreflightError(RuntimeError):
    """Safe preflight failure carrying only a stable code."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


def _aws_session(region: str) -> boto3.Session:
    """Create the configured AWS session without reading fixture content."""

    return boto3.Session(region_name=region)


def _active_vision_model(response: object, model_id: str) -> bool:
    """Return whether discovery contains the configured active vision model."""

    if not isinstance(response, Mapping):
        return False
    summaries = response.get("modelSummaries")
    if not isinstance(summaries, list):
        return False
    for summary in summaries:
        if not isinstance(summary, Mapping) or summary.get("modelId") != model_id:
            continue
        modalities = summary.get("inputModalities")
        lifecycle = summary.get("modelLifecycle")
        return (
            isinstance(modalities, list)
            and "IMAGE" in modalities
            and isinstance(lifecycle, Mapping)
            and lifecycle.get("status") == "ACTIVE"
        )
    return False


def _active_inference_profile(response: object, model_id: str) -> bool:
    """Return whether one discovery page contains the configured active profile."""

    if not isinstance(response, Mapping):
        return False
    summaries = response.get("inferenceProfileSummaries")
    if not isinstance(summaries, list):
        return False
    return any(
        isinstance(summary, Mapping)
        and summary.get("inferenceProfileId") == model_id
        and summary.get("status") == "ACTIVE"
        for summary in summaries
    )


def verify_live_preflight(region: str, model_id: str) -> boto3.Session:
    """Verify identity, privacy settings, and configured model visibility.

    This performs credential discovery and read-only Bedrock control-plane queries.
    It does not send fixture content, invoke a model, or create a resource.
    """

    session = _aws_session(region)
    try:
        credentials = session.get_credentials()
    except BotoCoreError as error:
        raise PreflightError("aws_credentials_unavailable") from error
    if credentials is None:
        raise PreflightError("aws_credentials_missing")

    try:
        bedrock = session.client("bedrock", region_name=region, config=NO_RETRY_CONFIG)
        response = bedrock.get_model_invocation_logging_configuration()
    except (BotoCoreError, ClientError) as error:
        raise PreflightError("bedrock_logging_status_unverified") from error
    if response.get("loggingConfig"):
        raise PreflightError("bedrock_model_invocation_logging_enabled")

    try:
        foundation_models = bedrock.list_foundation_models(byOutputModality="TEXT")
        profile_pages = bedrock.get_paginator("list_inference_profiles").paginate(
            typeEquals="SYSTEM_DEFINED"
        )
        model_is_visible = _active_vision_model(foundation_models, model_id) or any(
            _active_inference_profile(page, model_id) for page in profile_pages
        )
    except (BotoCoreError, ClientError) as error:
        raise PreflightError("bedrock_model_availability_unverified") from error
    if not model_is_visible:
        raise PreflightError("bedrock_model_not_available")
    return session
