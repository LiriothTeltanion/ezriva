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


def _foundation_model_capabilities(response: object) -> dict[str, bool]:
    """Map visible foundation-model IDs to proven image-input capability."""

    if not isinstance(response, Mapping):
        return {}
    summaries = response.get("modelSummaries")
    if not isinstance(summaries, list):
        return {}
    capabilities: dict[str, bool] = {}
    for summary in summaries:
        if not isinstance(summary, Mapping) or not isinstance(summary.get("modelId"), str):
            continue
        model_identifier = summary["modelId"]
        capabilities[model_identifier] = _active_vision_model(
            {"modelSummaries": [summary]}, model_identifier
        )
    return capabilities


def _foundation_model_id(model_arn: object) -> str | None:
    """Extract a public foundation-model ID without retaining an ARN."""

    if not isinstance(model_arn, str):
        return None
    marker = "foundation-model/"
    if marker not in model_arn:
        return None
    identifier = model_arn.split(marker, maxsplit=1)[1]
    return identifier or None


def _profile_capability(
    response: object,
    model_id: str,
    capabilities: Mapping[str, bool],
) -> tuple[bool, bool]:
    """Return whether a profile was found and proven image capable."""

    if not isinstance(response, Mapping):
        return False, False
    summaries = response.get("inferenceProfileSummaries")
    if not isinstance(summaries, list):
        return False, False
    for summary in summaries:
        if not isinstance(summary, Mapping) or summary.get("inferenceProfileId") != model_id:
            continue
        if summary.get("status") != "ACTIVE":
            return True, False
        models = summary.get("models")
        if not isinstance(models, list) or not models:
            return True, False
        underlying_ids = tuple(
            _foundation_model_id(model.get("modelArn")) if isinstance(model, Mapping) else None
            for model in models
        )
        return True, all(
            identifier is not None and capabilities.get(identifier, False)
            for identifier in underlying_ids
        )
    return False, False


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
        capabilities = _foundation_model_capabilities(foundation_models)
        direct_model_found = model_id in capabilities
        if capabilities.get(model_id, False):
            return session
        profile_found = False
        profile_capable = False
        for page in bedrock.get_paginator("list_inference_profiles").paginate(
            typeEquals="SYSTEM_DEFINED"
        ):
            found, capable = _profile_capability(page, model_id, capabilities)
            profile_found = profile_found or found
            profile_capable = profile_capable or capable
    except (BotoCoreError, ClientError) as error:
        raise PreflightError("bedrock_model_availability_unverified") from error
    if profile_capable:
        return session
    if direct_model_found or profile_found:
        raise PreflightError("bedrock_model_capability_unverified")
    raise PreflightError("bedrock_model_not_available")
