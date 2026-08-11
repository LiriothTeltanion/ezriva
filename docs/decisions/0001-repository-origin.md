# ADR-0001: Create a New Isolated Repository

- **Status:** Accepted
- **Date:** 2026-08-11 (Asia/Jerusalem)
- **Owner:** Kevin Cusnir

## Decision

Initialize Ezriva as a new Git repository inside an isolated `ezriva/`
directory. Copy only public-safe planning documents into it. Do not place any
privately supplied source document inside the repository.

## Why

The hackathon requires a newly created project. Isolation also prevents private
attachments from entering Git through an accidental broad add command. No code
or assets from IvritSheli or any earlier project are used.

## Consequences

- the first commit truthfully begins during the official submission period;
- planning history is preserved as documentation, not reused implementation;
- source attachments stay outside the Git working tree;
- every starter, dependency, generated asset, and AI tool remains disclosable.
