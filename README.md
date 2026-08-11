# Ezriva

**Clear help. Safe next steps.**

Ezriva is a multilingual, accessibility-first family navigation agent for the
Agents for Humans Hackathon. It is being built to turn a routine Hebrew notice
into an evidence-backed Spanish or English explanation and one bounded action
that remains under human control.

> Build status: checklist item 1 is complete. The document-to-action hero flow
> and live Bedrock evaluation are not complete, and this repository does not
> claim otherwise.

## Current implementation status

| Area | Status |
|---|---|
| Repository, quality baseline, and CI contract | Implemented and locally verified |
| FastAPI health endpoint | Implemented and tested |
| React foundation screen | Implemented and tested |
| Strands/Bedrock Hebrew fixture evaluation | Planned; awaiting a configured AWS session |
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
apps/api/                 FastAPI foundation; Strands integration is next
fixtures/                 Synthetic-only evaluation material
docs/hackathon-build/     Approved scope, PRD, specification, and checklist
docs/decisions/           Architecture and provenance decisions
docs/submission/          Disclosure and later submission evidence
infra/                    Deferred, least-privilege deployment definitions
scripts/                  Portable setup and verification entry points
```

## Prerequisites

- Python 3.12
- Node.js 24
- npm 11
- `uv`
- Git

Python 3.12 is the tested project version for this build.

## Local setup

```bash
python scripts/verify.py setup
```

On Windows PowerShell:

```powershell
./scripts/verify.ps1 setup
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

`make test-ai-fixtures` is intentionally separate from normal CI. Once item 2
is implemented, its live mode will require explicit opt-in, AWS credentials,
an allowed Bedrock model, and metered inference.

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
