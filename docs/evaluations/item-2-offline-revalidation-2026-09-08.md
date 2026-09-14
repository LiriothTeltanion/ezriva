# Item 2 Offline Revalidation - 8 September 2026

**Status:** Offline contracts passed; live Bedrock evaluation and Pause 1 remain pending

## Why this revalidation was required

The first live provider run must evaluate the final synthetic fixtures and the
final safety/report contract. Before spending any Bedrock allowance, this
increment fixed a past hero date, strengthened invisible-text handling,
clarified retained evidence, and moved fixture file bounds into the runtime
preflight.

## Verified changes

- The hero appointment now uses the stable synthetic date 18 April 2027.
- Structured model output containing bidi control characters is rejected by
  Pydantic before gate/report processing.
- Source-document bidi controls remain a separate blocked-untrusted-content
  signal.
- The Pause 1 hero review contains only expected, confirmed evidence.
- Evaluation report schema version 2 states separately that it retains no
  complete source and that it may retain a minimal synthetic hero review.
- Runtime fixture verification enforces the 3,670,016-byte cap and exact
  1600 x 1000 PNG dimensions before provider input.
- Pillow is pinned at 12.3.0 in `pyproject.toml` and `uv.lock`.

## Executed checks

The project-compatible runtime was Python 3.12.13 and the required ignored
portable `uv` was 0.11.33.

`python scripts/verify.py ai-fixtures` completed successfully:

- eight synthetic PNG/source pairs passed generator, allowlist, and hash checks;
- item-2 tests: 58 passed.

`python scripts/verify.py verify` completed successfully:

- `uv lock --check` passed;
- Ruff lint passed, and the Ruff formatting check passed for 53 files;
- ESLint passed with zero warnings;
- strict mypy passed across 28 source files;
- TypeScript typecheck passed;
- Python tests: 61 passed;
- web tests: one file and one test passed;
- Python compileall passed;
- Vite 8.2.1 production build passed;
- dependency-tree, repository privacy, and secret guardrails passed.

Additional dependency audits:

- `npm audit --audit-level=high`: zero known vulnerabilities.
- `pip-audit 2.10.1 --path .venv/Lib/site-packages`: no known
  vulnerabilities after the Pillow 12.3.0 update.

These are current local results, not a claim about an unobserved remote runner.
The repository privacy check is intentionally described as a heuristic
guardrail, not proof that arbitrary PII can never exist.

## Fixture visual review

The revised hero PNG was inspected at its committed 1600 x 1000 dimensions.
The synthetic label, clinic title, hearing-test purpose, 18 April 2027 date,
10:30 time, fictional Beersheba location, and arrival instruction are legible;
Hebrew and mixed numeric content follow the expected RTL reading order.

The Windows Pillow 12.3.0 wheel reported libraqm unavailable. The generator
stopped rather than emitting degraded Hebrew. The hero was therefore rendered
with the local Microsoft Edge Beta 153 Chromium text engine as documented in
`fixtures/provenance.md`; its tracked hash is enforced by the manifest.

## Live acceptance still required

No Bedrock model was invoked during this revalidation. Live attempts remain
zero of eight. There is still no observed model ID, region, latency, token
usage, provider behavior, or hero explanation to approve.

Before the live command, Ezriva still requires:

1. an AWS session configured outside chat and outside the repository;
2. read-only discovery of the actual image-capable model/profile and region;
3. verification that Bedrock model-invocation content logging is disabled;
4. a current cost estimate and Kevin's narrow approval for the named model,
   region, maximum eight attempts, and stated USD/ILS ceiling.

Only `scripts/run_ai_fixture_eval.py` may perform the live run. Item 3 remains
blocked until the live item-2 acceptance succeeds and Kevin approves Pause 1.
