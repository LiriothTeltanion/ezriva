# Item 2 Offline Verification

**Date:** 12 August 2026 (Asia/Jerusalem)  
**Status:** Offline lab verified; live Bedrock acceptance and Pause 1 pending

## What this proves

- The public catalog contains exactly eight synthetic Hebrew PNG/source pairs.
- Every pair matches its committed SHA-256 values and generator definition.
- `DocumentBriefCandidate` is extraction-only, strict, and cannot carry action,
  tool, destination, owner, approval, or idempotency fields.
- Confirmed facts require short Hebrew evidence, and evidence must match the
  logical synthetic source after Unicode/spacing normalization.
- Ambiguous dates, multiple dates, unreadable input, medical risk, prompt
  injection, and no-action notices cannot become executable writes.
- A bill may reach reminder review only when its due date is clear; payment is
  always unsupported.
- The Strands adapter exposes no action tools, uses one model turn, disables
  Strands and Botocore retries, and does not request a separate token-count call.
- A terminal provider failure stops the run instead of consuming the remaining
  authorized attempts.
- Missing usage remains `null`; reports do not invent zero usage or retain raw
  source, prompts, messages, traces, request IDs, account IDs, or provider errors.

The offline runner uses hand-authored schema-valid candidates to test these
contracts. Those candidates are test data, not mocked proof of model quality.

## Executed checks

`python scripts/verify.py ai-fixtures` completed successfully:

- deterministic fixture regeneration check: 8/8 pairs;
- focused AI-spike tests: 38 passed.

`python scripts/verify.py verify` completed successfully:

- lock, Ruff, formatting, ESLint, strict mypy, and TypeScript checks;
- Python tests: 41 passed;
- web tests: 1 passed;
- Python compilation and production web build;
- dependency-tree check, repository privacy guardrail, and secret scan.

All eight PNGs were inspected at their committed 1600 × 1000 dimensions. The
right-to-left Hebrew is shaped and legible in the clear fixtures; the blurry
scenario is deliberately unreadable while its synthetic-demo labeling remains
present. The hero image visibly matches its logical source date, time, place,
and arrival instruction.

## Live acceptance still required

No Bedrock model was invoked during this verification. Therefore there is no
honest model ID, region, latency, token usage, structured hero response, or
observed provider failure to report yet. AWS resources created: zero. Model
inferences attempted: zero.

The live runner is ready but requires a configured AWS session, a public model
or inference-profile ID discovered in the selected region, disabled Bedrock
model-invocation content logging, and explicit live opt-in. It permits at most
eight sequential attempts and writes only an ignored, sanitized local report.

Checklist item 2 remains unchecked. Pause 1 begins only after the real eight-
fixture run succeeds sufficiently for Kevin to compare the hero evidence and
confirm that the Spanish explanation feels clear and respectful.
