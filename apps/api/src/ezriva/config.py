"""Typed application configuration without secret side effects.

Module: config
Purpose: Validate safe defaults and environment-provided settings.
Author: Kevin Cusnir with Codex
Date: 2026-08-11 (Asia/Jerusalem)
"""

from typing import Literal
from zoneinfo import ZoneInfo

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validate Ezriva runtime configuration at the process boundary."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    app_env: Literal["development", "test", "production"] = "development"
    app_version: str = "0.1.0"
    public_demo_mode: bool = True
    allow_private_uploads: bool = False
    app_timezone: str = "Asia/Jerusalem"
    max_image_bytes: int = Field(default=3_670_016, ge=1, le=3_670_016)
    max_pdf_bytes: int = Field(default=4_194_304, ge=1, le=4_194_304)
    max_pdf_pages: int = Field(default=3, ge=1, le=3)
    aws_region: str | None = None
    bedrock_model_id: str | None = None
    model_max_tokens: int = Field(default=1_800, ge=256, le=4_096)
    model_max_cycles: int = Field(default=1, ge=1, le=1)
    ai_fixture_live_enabled: bool = False
    ai_fixture_max_inferences: int = Field(default=8, ge=1, le=8)

    @field_validator("app_timezone")
    @classmethod
    def timezone_must_exist(cls, value: str) -> str:
        """Reject an unknown IANA time-zone identifier.

        Args:
            value: Candidate IANA time-zone name.

        Returns:
            The validated time-zone name.

        Raises:
            ValueError: If the time zone cannot be resolved.
        """

        try:
            ZoneInfo(value)
        except (KeyError, ValueError) as error:
            raise ValueError("app_timezone must be a valid IANA time zone") from error
        return value

    @field_validator("aws_region")
    @classmethod
    def aws_region_must_be_public_name(cls, value: str | None) -> str | None:
        """Reject empty or account-bearing AWS region values."""

        if value is None:
            return None
        normalized = value.strip()
        if not normalized or not normalized.replace("-", "").isalnum():
            raise ValueError("aws_region must be a standard public AWS region name")
        return normalized

    @field_validator("bedrock_model_id")
    @classmethod
    def model_id_must_not_expose_an_account(cls, value: str | None) -> str | None:
        """Allow public model/profile identifiers but reject account-bearing ARNs."""

        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("bedrock_model_id cannot be blank")
        if normalized.startswith("arn:"):
            raise ValueError(
                "bedrock_model_id must be a public model or inference-profile ID, not an ARN"
            )
        return normalized
