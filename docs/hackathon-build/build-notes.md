# Ezriva Build Notes

This is the single chronological journal for build decisions, verification,
deepening rounds, and active-shaping moments. The canonical scope, behavior,
architecture, and order remain in the neighboring contract documents.

## 8 September 2026 - Item 2 pre-live hardening

### Active shaping

- Kevin confirmed that **Ezriva** remains locked and identified **Guiding
  Thread** as the preferred direction to refine; final logo assets remain an
  item-7 decision.
- Kevin asked for a more ambitious future agent: bureaucracy support, voice or
  call assistance, richer autonomy, and private family use.
- The hackathon MVP remains unchanged: one synthetic document-to-approved-
  reminder/ICS vertical slice. Calls, forms, medical decisions, and real family
  documents remain outside this checklist unless a written scope swap replaces
  existing work.
- Visual implementation remains item 7. The concept may be refined now, but no
  product shell, logo assets, or simulated feature screens are presented as a
  working app before their checklist item.

### Item-2 changes prepared

- Moved the synthetic hero appointment from a past date to 18 April 2027.
- Added runtime PNG byte and dimension enforcement before provider input.
- Rejected invisible bidi controls in untrusted structured model output while
  retaining the separate source-document defense.
- Limited Pause 1 evidence to expected, confirmed hero facts.
- Replaced the ambiguous `raw_content_retained` report flag with explicit
  complete-source and synthetic-review retention fields in schema version 2.
- Updated Pillow from 12.2.0 to 12.3.0 after the dependency audit identified
  fixed advisories.
- Added `START-HERE.md`, `CODEX-HANDOFF.md`, and `CHANGELOG.md` for
  non-duplicated repository navigation in this uncommitted increment.

### Verification status

- `python scripts/verify.py ai-fixtures`: 8 fixture pairs and 58 item-2 tests
  passed.
- `python scripts/verify.py verify`: Ruff/format, ESLint, mypy, TypeScript,
  61 Python tests, one web test, compileall, production build, dependency tree,
  repository privacy guard, and secret scan passed.
- npm audit reported zero vulnerabilities; pip-audit reported no known
  vulnerabilities after Pillow 12.3.0.
- Full evidence and the Pillow/libraqm fixture-generation limitation with its
  verified Edge fallback are recorded in
  `docs/evaluations/item-2-offline-revalidation-2026-09-08.md`.
- Live Bedrock attempts remain zero. No AWS resource or external action is part
  of this local increment.
