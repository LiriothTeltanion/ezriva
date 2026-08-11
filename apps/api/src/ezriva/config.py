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
