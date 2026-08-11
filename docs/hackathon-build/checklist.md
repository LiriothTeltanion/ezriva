# Ezriva - Build Checklist

> **Event:** Agents for Humans Hackathon
> **Track:** Everyday Agents
> **Author:** Kevin Cusnir with Codex
> **Date:** 2026-08-11 (Asia/Jerusalem)
> **Version:** 0.2 - execution contract

## Build Preferences

- **Plan design:** Handed off to Codex from the approved planning documents; Kevin may revise before code begins.
- **Build mode:** Autonomous. This choice locks when `$build-project` starts.
- **Comprehension checks:** N/A during autonomous execution; concise explanations in checkpoint summaries.
- **Git:** Initialize a new repository created during the official submission period. Commit after each completed checklist item or tightly coupled pair, using conventional commit messages. Never rewrite the submission-period history to conceal timing or reused work.
- **Verification:** Yes - automated checks after every item plus human look-at-it pauses after items 2, 7, and 10.
- **Check-in cadence:** Balanced; stop only at the three visual/risk checkpoints or a genuine blocker.
- **Scope authority:** `scope.md` defines cuts; `prd.md` defines behavior; `spec.md` defines implementation. New features do not enter the build unless they replace, rather than add to, existing scope.
- **Safety authority:** No external/write tool executes without a payload-bound approval. No raw private family data is used in development, screenshots, video, repository, or public demo.
- **Naming decision:** `Ezriva` is locked for the hackathon. Reopen only for a material legal, domain, or official-rule conflict.

## Definition Of Done For Every Item

- The described behavior exists in the working tree.
- Relevant tests/checks run and their actual results are recorded; no invented green status.
- No new secrets, PII, fake buttons, or unhandled primary states are introduced.
- Documentation/configuration changes needed to reproduce the item are included.
- A commit is created only after verification succeeds or the exact known limitation is documented.

## Checklist

- [x] **1. Create the new repository and quality baseline**
  Spec ref: `spec.md > File Structure`, `spec.md > Testing Strategy`, `scope.md > What We Are Building`
  What to build: Create a brand-new repository during the eligible period; scaffold `apps/web`, `apps/api`, `fixtures`, `docs`, `infra`, `scripts`, and workflows; add MIT license, `.gitignore`, `.env.example`, project metadata, Windows-friendly commands, and initial CI for lint/type/test/build. Record creation date and any starter/template disclosure.
  Acceptance: Public-facing metadata can later satisfy the license/repository requirement; no pre-existing project code is copied; a clean checkout has documented setup commands; placeholder commands fail honestly until implemented rather than printing fake success.
  Verify: Inspect `git log --reverse`, run the documented setup, secret scan the tree, run initial frontend/backend lint and smoke tests, and confirm the license is detected locally.

- [ ] **2. Prove Hebrew multimodal understanding with synthetic fixtures**
  Spec ref: `spec.md > AI Usage`, `spec.md > Testing Strategy > AI/evaluation fixtures`, `spec.md > Risks And Verification`
  What to build: Create provenance-documented synthetic appointment, blurry, ambiguous-date, two-deadline, high-risk, bill, no-action, and prompt-injection fixtures; implement a bounded model spike that sends the fixture directly through Strands/Bedrock and validates a minimal Pydantic `DocumentBriefCandidate`; record model ID/region, latency, token usage, and observed failures without storing private content.
  Acceptance: The hero appointment produces a schema-valid brief with Hebrew evidence and Spanish explanation; ambiguous/high-risk/injection fixtures do not produce an executable write proposal; failures are documented and model availability is configuration-driven.
  Verify: Run `make test-ai-fixtures` (or the documented equivalent), inspect the result report, and manually compare the hero fixture evidence with the synthetic source. **Pause 1:** Kevin reviews one result and confirms the explanation feels clear and respectful.

- [ ] **3. Implement domain schemas, deterministic policy, and state transitions**
  Spec ref: `spec.md > Core Domain Model`, `spec.md > Deterministic Policy`, `spec.md > Action state machine`
  What to build: Implement Pydantic domain types for briefs, evidence, uncertainty, action drafts, approvals, receipts, and activity; add pure deterministic policy rules, immutable payload hashing, valid state transitions, owner checks, and stable error codes.
  Acceptance: Missing/conflicting critical fields cannot reach execution; high-risk actions are blocked; every write becomes `AwaitingApproval`; stale or materially edited payloads invalidate approval; illegal state transitions raise typed errors.
  Verify: Run focused unit tests for all policy categories, state transitions, time-zone normalization, ownership, and payload canonicalization; mutation/branch coverage is preferred for the small policy core.

- [ ] **4. Build the Strands coordinator and safe activity model**
  Spec ref: `spec.md > Agent Design`, `spec.md > Structured-output strategy`, `spec.md > Prompt-injection defense`
  What to build: Construct one Strands coordinator with a configurable Bedrock model, untrusted-document prompt boundary, validated structured output, bounded cycles/tokens, safe repair/fallback behavior, and activity events that expose stages/tool status but no chain-of-thought or content.
  Acceptance: The coordinator returns only validated public view models; document instructions cannot alter policy or tool access; unavailable/invalid model output produces a safe recoverable state; raw prompts, source bytes, and tool arguments are absent from logs.
  Verify: Run coordinator tests with mocked Bedrock results, adversarial injection fixtures, malformed structured output, timeout/throttle simulation, and a log-capture assertion for forbidden content.

- [ ] **5. Implement HumanInTheLoop, tools, and idempotent persistence**
  Spec ref: `spec.md > Custom tools`, `spec.md > Approval/execution path`, `spec.md > Data Persistence`
  What to build: Add read-only preferences plus approval-gated `save_reminder`, `save_checklist`, `generate_ics`, and supported reversal tools; implement in-memory repository first and DynamoDB adapter behind a protocol; bind every intervention to owner/action/payload hash/expiry; use conditional idempotency writes.
  Acceptance: Denial creates no reminder/file; approval creates exactly one normalized action; double approval/resume returns the original receipt; wrong-user access is denied; `.ics` output matches the approved time zone/data; reversal requires a second approval.
  Verify: Run unit/integration tests for approve, deny, expiry, edited proposal, duplicate retry, provider failure, ownership, DynamoDB conditional conflict, `.ics` parsing, and reversal.

- [ ] **6. Expose the stable FastAPI web contract**
  Spec ref: `spec.md > API Contracts`, `spec.md > Error Strategy`, `spec.md > Data Flow`
  What to build: Implement versioned health, fixtures, analyses, action approval/denial/status/reversal, activity, and history-deletion endpoints; isolate AgentCore interruption/resume details behind a runtime adapter; enforce public fixture-only mode, validation, request IDs, safe problem details, and rate-limit hooks.
  Acceptance: API responses validate against shared/open schemas; public mode rejects arbitrary uploads; no endpoint accepts owner ID from the client/model; errors never echo raw input; retry/status semantics are stable across local and hosted adapters.
  Verify: Run API contract/integration tests, OpenAPI schema validation, auth/ownership negatives, file-validation tests, and a full fixture-to-receipt API flow.

- [ ] **7. Build the accessible multilingual product shell**
  Spec ref: `spec.md > Components And Responsibilities > Web onboarding and accessibility shell`, `brand-ux.md > Visual Direction`, `prd.md > Epic 1`
  What to build: Implement design tokens, responsive shell, Spanish/English/Hebrew resources, RTL direction, welcome/language, large text, Demo Mode entry, focused navigation, reduced-motion behavior, and reusable loading/error/empty patterns.
  Acceptance: Language switches without reload; Hebrew changes direction correctly; the shell works at 360 px and 200% zoom; keyboard focus is visible; no primary meaning depends on color/motion; no dead navigation or fake settings exist.
  Verify: Run component tests, automated accessibility checks, translation-key completeness, RTL snapshots/smoke tests, keyboard walkthrough, mobile/desktop screenshots, and production build. **Pause 2:** Kevin reviews the visual identity and mobile first-run flow before feature screens multiply.

- [ ] **8. Implement intake, analysis, evidence, and voice flow**
  Spec ref: `spec.md > Components And Responsibilities > Intake feature`, `prd.md > Epic 2`, `prd.md > Epic 3`
  What to build: Add synthetic fixture picker, local/private file and text intake boundaries, validation/preview/retry, honest processing stages, three-fact result, source evidence, uncertainty/correction state, and optional browser voice playback of the visible summary.
  Acceptance: Hero fixture reaches What/When/Next step; blurry/invalid/ambiguous inputs show their specific recovery states; corrected critical fields are user-confirmed; voice controls disappear or degrade cleanly when unsupported; no chain-of-thought appears.
  Verify: Run component and API-backed integration tests for every state, voice feature detection tests, mixed Hebrew/Latin rendering, and manual screen-reader/large-text checks.

- [ ] **9. Implement proposal, approval, receipt, undo, and activity UI**
  Spec ref: `spec.md > Components And Responsibilities > Proposal and approval feature`, `prd.md > Epic 4`, `prd.md > Epic 5`, `prd.md > EZR-US-703`
  What to build: Render one primary action, exact immutable approval sheet, approve/deny/execution reconciliation, duplicate-safe retry, completed/failed/refused receipts, `.ics` download, reversal guidance, and the content-safe technical activity timeline.
  Acceptance: No UI path can imply execution before server proof; edits invalidate approval; double-tap creates one action; receipt distinguishes an Ezriva reminder from an externally imported event; activity proves model/policy/HITL/tool stages without private reasoning.
  Verify: Run Playwright hero, denial, stale-approval, double-approve, provider-failure, page-reload/reconciliation, undo, keyboard, and RTL paths; inspect downloaded `.ics` with a parser.

- [ ] **10. Deploy the public demo and AgentCore runtime safely**
  Spec ref: `spec.md > AWS deployment target`, `spec.md > Deployment Plan`, `spec.md > Observability`
  What to build: Provision the smallest reproducible hosted path; deploy frontend, DynamoDB, and Strands agent to AgentCore Runtime; add a thin BFF only if required; enable fixture-only public mode, throttling, least-privilege IAM, health checks, AWS Budget, metrics, and PII-safe trace settings.
  Acceptance: Public URL completes the synthetic hero flow free of charge; arbitrary public uploads are rejected; runtime and state survive five sequential demos; no secrets/PII appear in deployed logs; teardown/cost controls are documented; fallback deployment is honest if AgentCore cannot carry the final demo.
  Verify: Run deploy smoke tests, IAM review, five clean end-to-end runs, log redaction scan, cost/alarm check, cold-start observation, and external-device mobile test. **Pause 3:** Kevin opens the public demo, completes the hero flow, and approves moving to submission hardening.

- [ ] **11. Harden quality, security, accessibility, documentation, and scoring proof**
  Spec ref: `spec.md > Testing Strategy`, `spec.md > Security And Privacy`, `prd.md > Submission Proof Points`
  What to build: Close critical test gaps; run lint/type/unit/integration/e2e/accessibility/security/build checks; create English README, SECURITY, PRIVACY, architecture diagram source+PNG, fixture provenance, setup/testing instructions, known limitations, screenshots, and a judging-criteria evidence matrix. Add repository About/license metadata instructions.
  Acceptance: Clean checkout setup is reproducible; all claimed checks have real captured results; zero known critical safety/accessibility defects remain; every incomplete feature is labeled; architecture image is submission-ready; README explains exactly where Strands and AgentCore are used.
  Verify: Run `make verify`/portable equivalent from a clean environment, inspect CI, render README diagrams/images, scan for secrets/PII/license issues, and compare every public claim with observable behavior.

- [ ] **12. Prepare the Devpost handoff and presentation package**
  Spec ref: `prd.md > Submission Proof Points`, `spec.md > Demo And Submission Flow`, `scope.md > Submission Story`
  What to build: Gather the project story, public repo link, live demo, architecture PNG, AWS Builder ID placeholder, testing instructions, feature screenshots, five-minute-max video script/shot list, disclosure of tools/pre-existing work, and draft English submission answers; outline up to three builder.aws posts using the official `#AgentsforHumans` hashtag without publishing or submitting anything automatically.
  Acceptance: Kevin has enough accurate material to run `$prepare-submission`; the pitch covers problem, audience, why it matters, and a real end-to-end demonstration; no private family material appears; every URL/file requirement is accounted for; optional blog/form inconsistencies are flagged for final official-page verification.
  Verify: Perform a timed dry run under five minutes, link/file/access check in a signed-out browser, rules-to-artifact compliance audit, and Kevin's final content review. Confirm the next command is `$prepare-submission`.

## Verification Pauses

| Pause | After | Kevin verifies | If rejected |
|---|---|---|---|
| 1 | Item 2 | Hebrew explanation is clear, respectful, and evidence-backed. | Change fixture/model/prompt before building UI. |
| 2 | Item 7 | Visual identity, mobile hierarchy, text size, and language behavior feel like Ezriva. | Adjust tokens/components before feature duplication. |
| 3 | Item 10 | Public hero flow works reliably on Kevin's device. | Fix deployment/runtime before submission work. |

## Critical Path

`1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 11 → 12`

The visual shell is intentionally after the model/safety/API vertical slice. A beautiful interface cannot rescue an unreliable Hebrew interpretation or an unsafe approval path.

## Features That Do Not Enter This Checklist

- Direct Google Calendar OAuth.
- Payments/forms/phone calls/messages.
- AgentCore Memory or multi-agent orchestration.
- Real family documents in hosted/public mode.
- Production supporter accounts.
- Native mobile application.
- Broad portal integrations.
- Decorative 3D/gamification.

Adding any of these requires a written scope swap: identify which existing checklist requirement will be removed, why scoring improves, and how the hero flow stays reliable.

## Checklist Gut Check

This is the smallest plan that still proves all five judging dimensions: non-trivial Strands implementation, a coherent accessible product, credible impact, an original human-control pattern, and a clear end-to-end presentation. It is intentionally ambitious in quality and restrained in feature count.
