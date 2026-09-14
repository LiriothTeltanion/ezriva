# Ezriva Agent Instructions

## Mission

Build the smallest complete, safe, original Ezriva MVP for the Agents for Humans Hackathon. Ezriva turns a routine Hebrew notice into an evidence-backed Spanish/English explanation and one human-approved reminder/checklist/ICS action.

## Required Context

Start with `START-HERE.md`, then read `CODEX-HANDOFF.md` completely and
follow its repository reading order. The canonical public build documents
remain `scope.md`, `prd.md`, `brand-ux.md`, `spec.md`, and `checklist.md`. Do
not restart planning or silently override scope, acceptance criteria,
architecture, or checklist sequencing.

## Authority And Scope

- Planning is complete. Start code only when Kevin explicitly asks to run `$build-project` or clearly requests implementation.
- `docs/hackathon-build/scope.md` controls feature cuts.
- `docs/hackathon-build/prd.md` controls observable behavior.
- `docs/hackathon-build/spec.md` controls architecture and safety boundaries.
- `docs/hackathon-build/checklist.md` controls execution order and verification pauses.
- Ask before any external/public write, paid AWS resource, Devpost project creation/submission, repository publication, email/message, or credit request.

## Originality

- Create a new repository during the official submission period.
- Do not touch or copy code from IvritSheli or any pre-existing project.
- Disclose starters, generated assets, third-party code/data, and AI coding tools.
- Preserve truthful Git history and the submitted release/tag.

## Engineering

- Python: PEP 8, strict type hints, small functions, Google-style docstrings, `pathlib`, structured logging, and Pydantic boundaries.
- TypeScript: strict mode, ES modules, descriptive types, functional React, minimal state, and accessible semantic components.
- Comments/documentation are in English; user-facing copy supports Spanish, English, and Hebrew/RTL.
- Prefer minimal dependencies and boring, reliable infrastructure.
- No general-purpose agent tools, arbitrary shell/browser/HTTP access, or hidden side effects.
- Model output is untrusted until schema/domain validation passes.
- Deterministic code owns policy, approval, ownership, idempotency, state, and retention.
- Every write requires a server-verified payload-bound human approval.

## Privacy And Security

- Public/demo data is synthetic.
- Never commit or log raw documents, unapproved PII, prompts,
  chain-of-thought, secrets, tokens, or full tool arguments/results. Public
  owner attribution in LICENSE/package metadata is intentional.
- Derive ownership from verified auth context, never a model/client-supplied user ID.
- Provide `.env.example`; keep secrets in supported secret stores/environment only.
- Use least privilege, file limits, rate limits, cost limits, TTL, redaction, and idempotent conditional writes.

## Quality

- Implement loading, empty, validation, unreadable, uncertain, blocked, approval, failure, completed, retry, and reversal states.
- Tests cover policy, approval, ownership, idempotency, prompt injection, tools, API, accessibility, RTL, and the hero path.
- Never state that checks pass unless they were executed successfully.
- No fake buttons, hard-coded hero results, or mocks presented as production behavior.
- Keep the public README, architecture diagram, deployment, video, and submitted behavior consistent.

## Build Rhythm

- Work through checklist items in order.
- Commit verified increments using conventional commits.
- Stop for Kevin after items 2, 7, and 10.
- Stop immediately on privacy exposure, material official-rule change, new spending/authority need, or a scope expansion that displaces the critical path.
