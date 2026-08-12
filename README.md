# Ezriva

**Clear help. Safe next steps.**

Ezriva is a multilingual, accessibility-first family navigation agent for the
Agents for Humans Hackathon. It is being built to turn a routine Hebrew notice
into an evidence-backed Spanish or English explanation and one bounded action
that remains under human control.

> Build status: checklist item 1 is complete. The item-2 synthetic Hebrew
> evaluation lab is implemented and verified offline; its real Bedrock run and
> Kevin's Pause 1 review are still pending. The document-to-action hero flow is
> not complete, and this repository does not claim otherwise.

## Current implementation status

| Area | Status |
|---|---|
| Repository, quality baseline, and CI contract | Implemented and locally verified |
| FastAPI health endpoint | Implemented and tested |
| React foundation screen | Implemented and tested |
| Eight synthetic Hebrew fixtures and deterministic safety gate | Implemented and verified offline |
| Live Strands/Bedrock Hebrew evaluation | Ready but not run; awaiting a configured AWS session |
| Human approval, reminder persistence, and ICS | Planned in later checklist items |
| Public deployment | Not deployed |

## MVP contract

The submitted vertical slice will:

1. read a synthetic Hebrew appointment notice through Strands and Bedrock;
2. show source-linked facts, uncertainty, and a plain Spanish explanation;
3. prepare one reminder/checklist and `.ics` proposal;
4. require a payload-bound human approval before any write;
5. create an idempotent receipt with recovery or reversal guidance.

It will not pay bills, submit forms, make medical/legal decisions, send
messages, browse arbitrary sites, or retain raw private documents.

## Repository layout

```text
apps/web/                 React + TypeScript product shell
apps/api/                 FastAPI foundation and bounded item-2 AI spike
fixtures/                 Eight synthetic-only Hebrew fixture pairs
docs/hackathon-build/     Approved scope, PRD, specification, and checklist
docs/decisions/           Architecture and provenance decisions
docs/submission/          Disclosure and later submission evidence
infra/                    Deferred, least-privilege deployment definitions
scripts/                  Portable setup and verification entry points
```

## Prerequisites

- Python 3.12 (3.12.13 verified)
- Node.js 24.14.0
- npm 11.9.0
- `uv` 0.11.33
- Git

These are Ezriva's reproducible project versions. Newer global Python or Node
installations may coexist on the workstation, but they are not the evidence
environment for this build.

## Local setup

```bash
python scripts/verify.py setup
```

On Windows PowerShell:

```powershell
./scripts/verify.ps1 setup
```

If Windows marks the PowerShell wrapper as downloaded, use the same portable
Python entry point instead of changing the machine-wide execution policy:

```powershell
python scripts/verify.py setup
```

The setup command installs locked local dependencies and may contact their
package registries. It does not invoke a model, create AWS resources, publish a
repository, or send project documents to an AI provider.

## Verification

```bash
python scripts/verify.py verify
```

Individual checks:

```bash
make lint
make typecheck
make test
make build
make secret-scan
```

The deterministic item-2 fixture contract is also offline and separately
available on Linux/macOS or Windows:

```bash
make test-ai-fixtures
python scripts/verify.py ai-fixtures
```

It verifies the exact eight-fixture allowlist and hashes, extraction-only schema,
Hebrew evidence gate, unsafe/uncertain outcomes, sanitized report shape, and
the one-turn/no-retry Strands adapter contract. It never invokes a model.
See the current [offline verification evidence](docs/evaluations/item-2-offline-verification.md).

The live path is deliberately excluded from normal verification and CI. After
specific authorization, configure `AWS_REGION`, `BEDROCK_MODEL_ID`, and
`AI_FIXTURE_LIVE_ENABLED=true`, then run:

```bash
make test-ai-fixtures-live
```

Before sending a fixture, that command requires AWS credentials, confirms that
Bedrock model-invocation content logging is disabled, and discovers the exact
configured model or inference profile in the selected region. It processes the
fixtures sequentially with one model attempt each, no provider or agent retry,
an eight-inference hard cap, early stop after a terminal provider failure, no
action tools, and a persistent local attempt ledger. Its local report excludes
source images, full prompts/messages, request IDs, account IDs, traces, and raw
provider errors.

## Run the baseline

API:

```bash
uv run uvicorn ezriva.main:app --app-dir apps/api/src --reload
```

Web:

```bash
npm --workspace @ezriva/web run dev
```

The API health endpoint is `GET /healthz`. The current web screen is an honest
foundation marker, not a simulated product demo.

## Planning and safety authority

- [`scope.md`](docs/hackathon-build/scope.md) controls feature cuts.
- [`prd.md`](docs/hackathon-build/prd.md) controls observable behavior.
- [`spec.md`](docs/hackathon-build/spec.md) controls architecture and safety.
- [`checklist.md`](docs/hackathon-build/checklist.md) controls build order.

Public/demo data is synthetic. Model output is untrusted until schema and
domain validation pass. Deterministic code owns policy, approval, ownership,
idempotency, state, and retention.

## Originality and disclosure

This repository was initialized from a blank implementation workspace on
11 August 2026 (Asia/Jerusalem), during the official submission period. No code
was copied from IvritSheli or any prior Kevin Cusnir project. See
[`disclosures.md`](docs/submission/disclosures.md) for starters, libraries, AI
assistance, and non-code inspiration.

## License

[MIT](LICENSE) © 2026 Kevin Cusnir.
