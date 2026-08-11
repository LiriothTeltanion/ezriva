"""Configuration boundary tests.

Module: test_config
Purpose: Prove safe defaults and Israel time-zone availability.
Author: Kevin Cusnir with Codex
Date: 2026-08-11 (Asia/Jerusalem)
"""

from zoneinfo import ZoneInfo

from ezriva.config import Settings


def test_defaults_are_demo_only_and_privacy_safe() -> None:
    """Private uploads stay disabled unless deliberately configured later."""

    settings = Settings(_env_file=None)

    assert settings.public_demo_mode is True
    assert settings.allow_private_uploads is False
    assert settings.max_image_bytes <= 3_670_016
    assert settings.max_pdf_bytes <= 4_194_304


def test_asia_jerusalem_timezone_resolves() -> None:
    """The configured local time zone must resolve on every supported OS."""

    settings = Settings(_env_file=None)

    assert ZoneInfo(settings.app_timezone).key == "Asia/Jerusalem"
