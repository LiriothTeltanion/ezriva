"""Run the explicitly metered, eight-call Strands/Bedrock fixture evaluation.

Module: run_ai_fixture_eval
Purpose: Execute checklist item 2 only after strict local and AWS preflight gates.
Author: Kevin Cusnir with Codex
Date: 2026-08-12 (Asia/Jerusalem)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))

from ezriva.ai_spike.catalog import load_manifest  # noqa: E402
from ezriva.ai_spike.preflight import PreflightError, verify_live_preflight  # noqa: E402
from ezriva.ai_spike.runner import (  # noqa: E402
    FixtureAnalyzer,
    ProviderObservation,
    run_evaluation,
)
from ezriva.ai_spike.strands_bedrock import StrandsBedrockAnalyzer  # noqa: E402
from ezriva.config import Settings  # noqa: E402

LEDGER_PATH = ROOT / "artifacts" / "private" / "item-2-attempt-ledger.json"
REPORT_PATH = ROOT / "artifacts" / "item-2-bedrock-evaluation.json"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporary, path)


class LedgerAnalyzer:
    """Persist a content-free counter after every provider attempt."""

    def __init__(self, delegate: FixtureAnalyzer, cap: int) -> None:
        self._delegate = delegate
        self._cap = cap
        self.model_id = delegate.model_id
        self.region = delegate.region
        self._attempts: list[dict[str, Any]] = []
        self._persist()

    def _persist(self) -> None:
        _write_json(
            LEDGER_PATH,
            {
                "authorized_cap": self._cap,
                "model_id": self.model_id,
                "region": self.region,
                "attempts": self._attempts,
            },
        )

    def analyze(self, image_bytes: bytes) -> ProviderObservation:
        if len(self._attempts) >= self._cap:
            raise RuntimeError("authorized inference cap exhausted")
        observation = self._delegate.analyze(image_bytes)
        self._attempts.append(
            {
                "sequence": len(self._attempts) + 1,
                "recorded_at": datetime.now(UTC).isoformat(),
                "failure_code": observation.failure_code,
            }
        )
        self._persist()
        return observation


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="enable the live provider path")
    parser.add_argument(
        "--acknowledge-metered-bedrock",
        action="store_true",
        help="acknowledge that up to eight configured Bedrock calls may be billed",
    )
    return parser.parse_args()


def main() -> int:
    """Apply all gates, run at most eight calls, and write only a safe report."""

    arguments = _arguments()
    settings = Settings()
    if not arguments.live or not arguments.acknowledge_metered_bedrock:
        print("Live evaluation refused: both explicit CLI gates are required.", file=sys.stderr)
        return 2
    if not settings.ai_fixture_live_enabled:
        print("Live evaluation refused: AI_FIXTURE_LIVE_ENABLED is false.", file=sys.stderr)
        return 2
    if settings.aws_region is None or settings.bedrock_model_id is None:
        print(
            "Live evaluation refused: AWS_REGION and BEDROCK_MODEL_ID are required.",
            file=sys.stderr,
        )
        return 2
    if LEDGER_PATH.exists():
        print(
            "Live evaluation refused: an attempt ledger already exists; "
            "renewed authorization is required.",
            file=sys.stderr,
        )
        return 2

    try:
        session = verify_live_preflight(settings.aws_region, settings.bedrock_model_id)
    except PreflightError as error:
        print(f"Live evaluation preflight failed safely: {error.code}.", file=sys.stderr)
        return 1

    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")
    if len(manifest.fixtures) > settings.ai_fixture_max_inferences:
        print(
            "Live evaluation refused: configured inference cap is below the fixture count.",
            file=sys.stderr,
        )
        return 2
    analyzer = LedgerAnalyzer(
        StrandsBedrockAnalyzer(
            boto_session=session,
            region=settings.aws_region,
            model_id=settings.bedrock_model_id,
            max_tokens=settings.model_max_tokens,
        ),
        cap=settings.ai_fixture_max_inferences,
    )
    report = run_evaluation(
        root=ROOT,
        manifest=manifest,
        analyzer=analyzer,
        inference_cap=settings.ai_fixture_max_inferences,
    )
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(report.model_dump_json(indent=2) + "\n", encoding="utf-8")
    matched = sum(record.expected_behavior_met for record in report.fixtures)
    print(
        f"Evaluation finished: {report.attempted_inferences} bounded attempts; "
        f"{matched}/{len(report.fixtures)} expected safety behaviors observed."
    )
    print(f"Sanitized local report: {REPORT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
