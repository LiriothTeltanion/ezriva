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
import tempfile
import time
from collections.abc import Callable, Sequence
from contextlib import suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "apps" / "api" / "src"))

from ezriva.ai_spike.catalog import load_manifest, verify_manifest  # noqa: E402
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
ATOMIC_REPLACE_ATTEMPTS = 8


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent,
        prefix=f".{path.name}.",
        suffix=".tmp",
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(payload, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        for attempt in range(ATOMIC_REPLACE_ATTEMPTS):
            try:
                os.replace(temporary, path)
                return
            except PermissionError:
                if attempt == ATOMIC_REPLACE_ATTEMPTS - 1:
                    raise
                time.sleep(0.01 * (attempt + 1))
    finally:
        with suppress(FileNotFoundError):
            temporary.unlink()


class AttemptLedgerExistsError(RuntimeError):
    """Raised when a live-run ledger has already reserved the authorization."""


class LedgerAnalyzer:
    """Reserve and persist a content-free record around every provider attempt."""

    def __init__(
        self,
        delegate: FixtureAnalyzer,
        cap: int,
        *,
        ledger_path: Path | None = None,
        clock: Callable[[], datetime] | None = None,
    ) -> None:
        self._delegate = delegate
        self._cap = cap
        self._ledger_path = LEDGER_PATH if ledger_path is None else ledger_path
        self._clock = clock or (lambda: datetime.now(UTC))
        self.model_id = delegate.model_id
        self.region = delegate.region
        self._attempts: list[dict[str, Any]] = []

        self._reserve()

    def _payload(self) -> dict[str, Any]:
        return {
            "authorized_cap": self._cap,
            "model_id": self.model_id,
            "region": self.region,
            "attempts": self._attempts,
        }

    def _reserve(self) -> None:
        """Create the run ledger exclusively before any provider can be called."""

        self._ledger_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with self._ledger_path.open("x", encoding="utf-8") as stream:
                json.dump(self._payload(), stream, indent=2, ensure_ascii=False)
                stream.write("\n")
        except FileExistsError as error:
            raise AttemptLedgerExistsError("attempt ledger already exists") from error

    def _persist(self) -> None:
        _write_json(self._ledger_path, self._payload())

    def _timestamp(self) -> str:
        timestamp = self._clock()
        if timestamp.tzinfo is None or timestamp.utcoffset() is None:
            raise ValueError("ledger clock must return an aware datetime")
        return timestamp.isoformat()

    def analyze(self, image_bytes: bytes) -> ProviderObservation:
        if len(self._attempts) >= self._cap:
            raise RuntimeError("authorized inference cap exhausted")
        sequence = len(self._attempts) + 1
        self._attempts.append(
            {
                "sequence": sequence,
                "started_at": self._timestamp(),
                "status": "pending",
                "completed_at": None,
                "failure_code": None,
            }
        )
        self._persist()
        try:
            observation = self._delegate.analyze(image_bytes)
        except Exception:
            self._attempts[-1] = {
                **self._attempts[-1],
                "status": "boundary_error",
                "completed_at": self._timestamp(),
                "failure_code": "provider_boundary_error",
            }
            with suppress(OSError):
                self._persist()
            raise
        self._attempts[-1] = {
            **self._attempts[-1],
            "status": "completed",
            "completed_at": self._timestamp(),
            "failure_code": observation.failure_code,
        }
        self._persist()
        return observation


def _arguments(arguments: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="enable the live provider path")
    parser.add_argument(
        "--acknowledge-metered-bedrock",
        action="store_true",
        help="acknowledge that up to eight configured Bedrock calls may be billed",
    )
    return parser.parse_args(arguments)


def main(arguments: Sequence[str] | None = None) -> int:
    """Apply all gates, run at most eight calls, and write only a safe report."""

    parsed = _arguments(arguments)
    if not parsed.live or not parsed.acknowledge_metered_bedrock:
        print("Live evaluation refused: both explicit CLI gates are required.", file=sys.stderr)
        return 2
    try:
        settings = Settings()
    except ValidationError:
        print("Live evaluation refused: invalid configuration.", file=sys.stderr)
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
    manifest = load_manifest(ROOT / "fixtures" / "manifest.toml")
    verify_manifest(ROOT, manifest)
    if len(manifest.fixtures) > settings.ai_fixture_max_inferences:
        print(
            "Live evaluation refused: configured inference cap is below the fixture count.",
            file=sys.stderr,
        )
        return 2

    try:
        session = verify_live_preflight(settings.aws_region, settings.bedrock_model_id)
    except PreflightError as error:
        print(f"Live evaluation preflight failed safely: {error.code}.", file=sys.stderr)
        return 2

    try:
        analyzer = LedgerAnalyzer(
            StrandsBedrockAnalyzer(
                boto_session=session,
                region=settings.aws_region,
                model_id=settings.bedrock_model_id,
                max_tokens=settings.model_max_tokens,
            ),
            cap=settings.ai_fixture_max_inferences,
        )
    except AttemptLedgerExistsError:
        print(
            "Live evaluation refused: an attempt ledger already exists; "
            "renewed authorization is required.",
            file=sys.stderr,
        )
        return 2

    try:
        report = run_evaluation(
            root=ROOT,
            manifest=manifest,
            analyzer=analyzer,
            inference_cap=settings.ai_fixture_max_inferences,
        )
        _write_json(REPORT_PATH, report.model_dump(mode="json"))
    except Exception:
        print("Live evaluation stopped safely before a complete report.", file=sys.stderr)
        return 1

    fixture_count = len(manifest.fixtures)
    matched = sum(record.expected_behavior_met for record in report.fixtures)
    not_attempted = fixture_count - report.attempted_inferences
    print(
        f"Evaluation finished: {report.attempted_inferences}/{fixture_count} attempted; "
        f"{matched}/{fixture_count} expected safety behaviors observed; "
        f"{not_attempted} not attempted."
    )
    report_display_path = (
        REPORT_PATH.relative_to(ROOT) if REPORT_PATH.is_relative_to(ROOT) else REPORT_PATH.name
    )
    print(f"Sanitized local report: {report_display_path}")
    if report.attempted_inferences == fixture_count and matched == fixture_count:
        print("Automated gates met; Pause 1 manual review is still required.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
