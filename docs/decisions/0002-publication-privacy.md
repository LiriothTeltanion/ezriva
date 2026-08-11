# ADR-0002: Publish a Privacy-Sanitized History

- **Status:** Accepted
- **Date:** 2026-08-11 (Asia/Jerusalem)
- **Owner:** Kevin Cusnir

## Decision

Create the public Git history from a curated snapshot before the first GitHub
push. Exclude private planning state, source-evidence notes, personal schedules,
authorization records, and privately supplied filenames.

## Why

Early local-only commits recorded labels for private source materials. The
source files themselves were never copied into the implementation repository,
but publishing those labels would disclose unnecessary personal context. A
cleanup commit would leave the earlier blobs visible on GitHub.

## Integrity

This privacy sanitization does not hide reused application code: Ezriva's
implementation is new and no earlier project code is included. The public root
commit remains inside the official submission period and truthfully represents
the verified foundation at first publication. The original local evidence
history remains private and is never pushed.

## Consequences

- only the curated public repository becomes the ongoing development checkout;
- private evidence/history is retained separately and never pushed;
- public commits and releases remain immutable after submission;
- future changes follow the public checklist and normal conventional commits.
