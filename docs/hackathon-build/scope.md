# Ezriva - Project Scope

> **Event:** Agents for Humans Hackathon
> **Track:** Everyday Agents
> **Author:** Kevin Cusnir with Codex
> **Date:** 2026-08-11 (Asia/Jerusalem)
> **Version:** 0.2 - confirmed name and time-boxed build budget

## Confirmed Project Name

**Ezriva** is the locked hackathon name. It is a coined, human-sounding brand associated with help, life, and forward motion.

The project does not claim that “Ezriva” is an existing Hebrew word. Similar-name and linguistic caveats remain disclosed in `brand-ux.md`; they no longer form a pre-build decision gate.

## One-Line Summary

**Ezriva turns everyday Hebrew documents and messages into clear guidance and safely completed next steps for immigrants and older adults, with the person approving every consequential action.**

## Why This Project Exists

People who do not read Hebrew confidently - especially older immigrants with limited digital literacy - can receive an appointment letter, municipal notice, bill, or service message and still not know:

- what it actually means;
- what matters now;
- whether a deadline is real;
- which action is safe;
- how to complete that action in an unfamiliar interface;
- when to ask a trusted family member for help.

Translation tools convert words. Ezriva converts an obligation into a bounded, understandable, reviewable workflow.

## Target User

### Primary persona - The family member navigating an unfamiliar system

- Adult or older adult living in Israel.
- Speaks Spanish more comfortably than Hebrew.
- Uses a phone but is not confident with complex apps, forms, or settings.
- Wants independence without losing the option to ask family for support.
- Needs large readable text, voice playback, few decisions per screen, and clear confirmation before any external action.

### Secondary persona - The trusted supporter

- Adult child, relative, social worker, or volunteer.
- Helps interpret documents and follow up on routine tasks.
- Needs a concise, consent-based handoff, not unrestricted surveillance or account access.

### Hackathon evaluator persona

- Needs to understand the problem in seconds.
- Must see a working Strands agent complete a real workflow end to end.
- Must be able to run or test the project using synthetic data without exposing a real family's information.

## Problem

The user is not primarily missing a translation. They are missing **situational clarity and safe execution**. A translated letter can still leave them with five unanswered questions and a deadline they might miss.

Existing generic assistants often fail this audience because they:

- behave like open-ended chatbots;
- present too much text;
- hide uncertainty;
- do not distinguish advice from an executable action;
- do not reliably turn an interpreted date into a saved reminder and calendar-ready artifact;
- treat family support as account sharing rather than explicit consent;
- are not designed around Hebrew RTL plus Spanish/English output.

## Core Workflow

1. **Receive:** The user uploads or pastes a synthetic Hebrew appointment letter, notice, bill, or message.
2. **Understand:** Ezriva extracts the sender, topic, dates, amounts, location, requested action, and uncertainty.
3. **Explain:** It returns a short Spanish explanation with an optional English/Hebrew view and voice playback.
4. **Plan:** The Strands agent proposes a typed action card, such as “Save this appointment as a reminder and prepare a calendar file.”
5. **Protect:** A deterministic policy layer assigns a risk level and blocks unsupported or high-consequence actions.
6. **Approve:** The user sees exactly what will happen and explicitly approves or rejects it.
7. **Act:** Ezriva uses real tools to persist the reminder/checklist and generate an importable `.ics` calendar file.
8. **Confirm:** The user gets a simple receipt: what was understood, what action occurred, when it will happen, and how to undo it.
9. **Follow up:** A scheduled check surfaces only when an unresolved deadline or meaningful decision remains.

## The Hackathon “Wow Moment”

On one screen, a dense Hebrew appointment letter becomes:

- a spoken Spanish summary;
- three visually highlighted facts: **what, when, where**;
- one safe next action;
- a transparent approval sheet;
- a real reminder appearing in Ezriva plus a generated calendar file after approval;
- an auditable confirmation with an undo path.

The transformation should take less than one minute in the recorded demo and should not rely on pre-rendered fake output.

## What We Are Building

### Must ship - competition MVP

- A new public repository created during the official submission period.
- Responsive React/TypeScript interface with Spanish, English, and Hebrew/RTL foundations.
- Accessible first-run experience and **Demo Mode** using synthetic Hebrew documents.
- Image/PDF/text intake with validation, size limits, and clear error states.
- Strands Agents SDK orchestration that genuinely chooses and invokes typed tools.
- Structured document understanding with explicit confidence/uncertainty fields.
- A plain-language “What it says / What matters / What Ezriva can do” result.
- Deterministic risk policy outside the language model.
- Human approval gate for any write/file-generation action.
- One fully real end-to-end action: persist a reminder/checklist and generate its `.ics` calendar file.
- Idempotency protection so a retry cannot create duplicate reminders/files.
- Audit receipt, undo instructions, and short retention/deletion controls.
- Synthetic fixtures covering appointment, bill/due date, and unreadable/ambiguous input; the recorded hero demo uses the appointment fixture.
- Automated tests for parsing schemas, policy decisions, approval enforcement, tool idempotency, API behavior, and the hero path.
- Public live demo if stable; reproducible local setup regardless.
- MIT license, architecture diagram, English README, and five-minute-or-shorter demo video plan.

### Should ship - high-value stretch

- Voice playback of the explanation using browser speech synthesis or a clearly documented provider.
- AgentCore Runtime deployment after the local/standard deployment is stable.
- Background deadline check with a visible in-app notification or email to a test address.
- One builder.aws post documenting the human-in-control design and technical journey.

### Could ship - only after the submission path is green

- AgentCore Memory for user preferences/session continuity.
- Optional consent-based supporter handoff link with expiring access.
- Two additional builder.aws posts for the maximum documented bonus.
- Broader document categories and more calendar providers.

## What We Are Not Building

- **No general-purpose chatbot.** It weakens the end-to-end story and creates an unsafe open action surface.
- **No automatic payments, form submission, medical decisions, legal advice, or benefit claims.** These are consequential and exceed the time/safety budget.
- **No autonomous phone calls.** That belongs to a later CALL-E-style product and would distract from the current Strands workflow.
- **No production identity verification or family account system.** Demo accounts or passwordless local demo access are sufficient for judging.
- **No long-term storage of raw private documents.** The MVP processes in memory and retains only the minimum redacted structured result required for the action receipt.
- **No WhatsApp scraping or unofficial messaging automation.** It creates platform, privacy, and reliability risk.
- **No dependency on IvritSheli or any frozen/pre-existing repository.** Product insights may inspire the work, but implementation must be new and disclosed.
- **No attempt to support every Israeli authority or document type.** Three synthetic fixture types prove the general pattern.
- **No decorative 3D world, complex gamification, or large dashboard.** The interface must feel calm, trustworthy, and fast.

## Inspiration And References

- **Camera-first translation products:** demonstrate the value of pointing at unfamiliar text, but Ezriva differentiates by turning interpretation into a safe completed action.
- **Accessibility assistance services:** inspire a calm, confidence-building interaction and honest escalation when automation is uncertain.
- **Family calendar/reminder tools:** prove that routine coordination matters, while Ezriva adds multilingual interpretation and consent-based execution.

The design takes inspiration from these interaction patterns, not their proprietary code, data, or branding.

## Design Philosophy

1. **Agency over automation:** success means the user can do more independently, not that the system controls more.
2. **Explain before acting:** every proposal includes what Ezriva understood, why the action is suggested, and what will change.
3. **Confidence is not authority:** low-confidence or high-risk outputs stop and ask for help.
4. **One meaningful decision at a time:** reduce cognitive load and avoid multi-step forms whenever possible.
5. **Family-supported, never family-surveilled:** sharing is explicit, scoped, expiring, and optional.
6. **Privacy by architecture:** minimize collection, separate raw input from durable records, redact logs, and provide deletion.
7. **Cultural and linguistic humility:** Hebrew layout, Spanish clarity, and English compatibility are product behavior, not decoration.
8. **Calm technology:** no shame, streak loss, alarming colors, or manipulative urgency.

## Originality Thesis

Ezriva's originality is not “AI translates Hebrew.” Its non-obvious combination is:

- translation plus action planning;
- agentic tool execution plus deterministic risk policy;
- older-adult accessibility plus correct multilingual/RTL interaction;
- family support plus explicit consent boundaries;
- proactive follow-up without constant notifications;
- a real lived use case validated privately with consenting family members and demonstrated publicly only with synthetic data.

## Demo Path

1. Open Demo Mode in Spanish.
2. Select the included synthetic Hebrew clinic appointment letter.
3. Show the agent's live processing steps at a user-safe level: read, identify obligations, verify missing facts, plan.
4. Reveal the three-fact summary and confidence labels.
5. Play the Spanish explanation aloud.
6. Open the proposed reminder/calendar-export action and show the risk/approval sheet.
7. Approve once.
8. Show the saved reminder and generated `.ics` proof.
9. Return to Ezriva and show the audit receipt and undo instructions.
10. Briefly open the architecture/trace view to prove Strands tool use and safety enforcement.

## Submission Story

“For many immigrant families in Israel, a short Hebrew notice can become a
shared task: translate it, find the deadline, decide what to do, create a
reminder, and verify nothing was missed. Ezriva keeps the person receiving the
message in control while an agent turns confusion into one clear, safe next
step.”

## Success Criteria

- A judge understands the audience and pain point within 20 seconds.
- The hero workflow completes live without manual database edits or mocked action buttons.
- Strands selects and invokes at least one meaningful custom tool.
- No reminder/file write occurs without a valid approval token.
- Repeating the same approved request does not create a duplicate reminder/file.
- Ambiguous dates and high-risk categories stop safely.
- The UI works at 360 px width, keyboard-only, with 200% zoom and RTL Hebrew.
- A new evaluator can run the project from the README.
- Every claim in the video matches observable project behavior.

## Scope Risks

| Risk | Likelihood | Impact | Scope response |
|---|---:|---:|---|
| Hebrew document extraction is unreliable | Medium | High | Use synthetic fixtures, structured validation, confidence thresholds, and a manual correction step. |
| Direct calendar OAuth tempts scope expansion | Medium | High | Keep it outside the MVP; use the same tool interface for a post-submission provider adapter. |
| AgentCore deployment blocks the MVP | Medium | Medium | Make the agent portable; deploy to AgentCore only after local hero flow and tests pass. |
| Too many document categories dilute the demo | High | Medium | Optimize one appointment flow; use bill/unreadable fixtures only as proof of boundaries. |
| “Agent” looks like a chatbot | Medium | High | Lead with action inbox, typed tools, approval, scheduled follow-up, and audit receipt. |
| Public demo exposes personal data | Low | Critical | Demo Mode only, synthetic assets, redacted telemetry, short retention, no family data in repo/video. |

## Scope Deepening Record

- Mandatory beats covered using Kevin's existing detailed project description, goals, audience, design preferences, and technical background.
- Deepening rounds: 1 synthesized architecture/safety round to expose ambiguity, duplication, privacy, and deployment risks.
- Confirmed build mode: autonomous execution with verification pauses after
  checklist items 2, 7, and 10.
