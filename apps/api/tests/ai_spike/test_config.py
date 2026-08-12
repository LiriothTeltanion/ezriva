"""Live-evaluation configuration boundary tests.

Module: test_config
Purpose: Keep the provider optional, bounded, and free of account-bearing IDs.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

import pytest
from pydantic import ValidationError

from ezriva.config import Settings


def test_live_fixture_evaluation_is_off_and_capped_by_default() -> None:
    """Normal tests and CI cannot invoke Bedrock implicitly."""

    settings = Settings(_env_file=None)

    assert settings.ai_fixture_live_enabled is False
    assert settings.ai_fixture_max_inferences == 8
    assert settings.model_max_cycles == 1
    assert settings.aws_region is None
    assert settings.bedrock_model_id is None


def test_account_bearing_model_arn_is_rejected() -> None:
    """Reports use public model/profile IDs rather than AWS account ARNs."""

    account_id = "123456789012"
    with pytest.raises(ValidationError) as captured:
        Settings(
            _env_file=None,
            bedrock_model_id=f"arn:aws:bedrock:region:{account_id}:inference-profile/example",
        )

    assert account_id not in str(captured.value)


def test_more_than_eight_inferences_is_rejected() -> None:
    """Configuration cannot expand Kevin's authorized item-2 cap."""

    with pytest.raises(ValidationError):
        Settings(_env_file=None, ai_fixture_max_inferences=9)
