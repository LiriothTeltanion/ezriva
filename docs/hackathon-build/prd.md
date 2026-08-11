# Ezriva - Product Requirements Document

> **Event:** Agents for Humans Hackathon
> **Track:** Everyday Agents
> **Author:** Kevin Cusnir with Codex
> **Date:** 2026-08-11 (Asia/Jerusalem)
> **Version:** 0.1 - MVP requirements
> **Source:** `scope.md`

## Product Summary

Ezriva is a multilingual, accessibility-first family-navigation agent. It helps immigrants and older adults understand routine Hebrew documents or messages and safely complete the next step without turning the experience into an open-ended chat.

The MVP centers on one complete journey: a user provides a Hebrew appointment notice; Ezriva extracts the important facts, explains them in plain Spanish, proposes a saved reminder and calendar export, requires informed approval, performs the action, and returns an auditable receipt with an undo path.

Ezriva must feel like a calm helper working on a bounded task. It must not pretend to be a lawyer, doctor, government representative, financial adviser, or omniscient translator.

## Product Goals

1. Reduce the cognitive and language burden of routine Hebrew notices.
2. Turn interpretation into one clear, safe, completed next step.
3. Demonstrate meaningful Strands-agent reasoning and tool use, not a prompt wrapper.
4. Preserve human control over external or consequential actions.
5. Create a coherent, polished product experience suitable for older adults.
6. Produce a public, reproducible, privacy-safe hackathon demonstration.

## Non-Goals

- Replace professional medical, legal, financial, or government advice.
- Make payments or submit official forms.
- Guarantee the accuracy or legal effect of a document interpretation.
- Monitor private accounts without explicit setup and consent.
- Support every Israeli institution, document type, or calendar provider in the MVP.
- Provide unrestricted family access to a user's documents or history.
- Behave as a general conversational assistant.

## Target Users

### Persona A - Spanish-speaking older adult in Israel

- Understands Spanish best and may understand limited spoken or written Hebrew.
- Uses a smartphone for messaging, photos, and basic apps.
- Can become overwhelmed by dense text, multiple buttons, unfamiliar icons, or long forms.
- Wants a simple explanation and confidence that the important date will not be missed.
- May prefer to hear the explanation rather than read it.

### Persona B - Independent newcomer

- Uses Spanish or English as a primary language.
- Can operate apps but does not understand the conventions of Israeli services or Hebrew notices.
- Wants to handle routine obligations independently and involve family only when necessary.

### Persona C - Trusted supporter

- Helps a parent, client, or community member with language and digital tasks.
- Wants a concise, permission-based summary of unresolved issues.
- Must never receive unrestricted access by default.

## Experience Principles

- **One task, one screen, one decision:** every stage has one primary action.
- **Plain language before detail:** show the short explanation first; original text and technical details are optional.
- **Large, calm, forgiving:** generous spacing, large touch targets, no countdown pressure, and reversible actions.
- **Show uncertainty:** use “I could not confirm the date” instead of inventing confidence.
- **Preview before execution:** the approval sheet names the durable reminder/file, exact change, and undo method.
- **Never shame:** errors are framed as recoverable system limits, not user mistakes.
- **Language is a preference, not an identity assumption:** the user can switch Spanish, English, or Hebrew at any time.
- **RTL is structural:** Hebrew screens, fields, and mixed-language content remain readable and correctly aligned.

## Core User Journey

### Stage 1 - Welcome

The first screen asks for preferred explanation language and offers a clearly labeled Demo Mode. The user can enlarge text and enable voice playback without opening settings.

### Stage 2 - Add information

The user can take/upload a picture, choose a PDF, paste text, or select a synthetic demo document. The interface explains what types of routine content Ezriva can help with and what it will refuse.

### Stage 3 - Understand

Ezriva shows a short progress sequence using honest task labels such as “Reading the notice,” “Finding dates and requested actions,” and “Preparing a safe next step.” It does not expose raw chain-of-thought.

### Stage 4 - Review meaning

The result opens with three facts: what the notice is, the most important date/time, and what the sender expects. A “What I am unsure about” section appears whenever a field is incomplete or conflicting.

### Stage 5 - Review proposed action

Ezriva presents one recommended action card. The card explains why it helps and which durable reminder/file will be created. The user may edit extracted details before approving.

### Stage 6 - Approve and act

The user sees a dedicated approval sheet with the exact reminder title, time, location, notification time, `.ics` contents, and duplicate warning. Only a deliberate approval executes the tools.

### Stage 7 - Confirm and follow up

Ezriva displays the completed action, a direct link or proof, an undo path, retention information, and any unresolved decision. The user can optionally create a consent-based summary for a trusted supporter.

## Epics And User Stories

### Epic 1 - Accessible first-run experience

#### EZR-US-101 - Choose an explanation language

As a user, I want to choose Spanish, English, or Hebrew before adding a document so that the instructions begin in a language I understand.

Acceptance criteria:

- The first-run screen presents all three choices using their native labels: Español, English, עברית.
- Selecting a language immediately changes interface copy without reloading the page.
- Returning to the app restores the previous choice on the same device.
- Switching to Hebrew changes the page direction and component alignment to RTL.
- Mixed Hebrew source text remains visually distinct from the explanation language.

#### EZR-US-102 - Start safely in Demo Mode

As a visitor or judge, I want to use a synthetic example without creating an account so that I can evaluate the complete workflow without sharing private data.

Acceptance criteria:

- A “Try a safe example” action is visible on the first screen.
- Demo Mode is explicitly labeled as synthetic and contains no real person's data.
- At least one synthetic Hebrew appointment fixture is available.
- Demo Mode reaches the same interpretation, approval, execution, and receipt screens as a normal upload.
- Demo Mode creates only an Ezriva demo reminder and a clearly labeled `.ics` file.

#### EZR-US-103 - Adjust readability quickly

As an older adult, I want a large-text option and voice playback near the content so that I do not need to navigate a complex settings page.

Acceptance criteria:

- A large-text control is available from first run and the result screen.
- Large text does not hide, overlap, or truncate primary actions at 200% browser zoom.
- The explanation can be read aloud in the selected language when the browser/device supports it.
- Voice playback has visible play, pause, restart, and stop states.
- If voice is unavailable, the user sees a plain explanation and no nonfunctional control.

#### EZR-US-104 - Understand the product boundary

As a user, I want to know what Ezriva can and cannot do so that I do not mistake it for official or professional advice.

Acceptance criteria:

- The intake screen states that Ezriva helps explain routine information and prepare actions.
- It states that the MVP does not pay bills, submit official forms, diagnose conditions, or make legal decisions.
- The boundary is available in all three interface languages.
- The warning is concise and does not block the user with a long legal wall of text.

### Epic 2 - Safe document intake

#### EZR-US-201 - Add a supported input

As a user, I want to upload an image/PDF, paste text, or select an example so that I can use whichever input is easiest.

Acceptance criteria:

- The input screen supports JPEG, PNG, PDF, and pasted text.
- Accepted file types and maximum size are displayed before selection.
- The selected filename or a small preview is shown before processing.
- The user can remove or replace an input before starting.
- The primary action remains disabled until a valid input exists.

#### EZR-US-202 - Reject unsupported or unsafe input clearly

As a user, I want a clear explanation when a file cannot be processed so that I know how to fix it.

Acceptance criteria:

- Unsupported types, oversized files, empty text, encrypted PDFs, and corrupted files produce distinct messages.
- Error copy gives one useful next action, such as retaking the photo or pasting the text.
- No processing request begins after client or server validation fails.
- The user can retry without refreshing the page.

#### EZR-US-203 - Confirm image readability

As a user, I want Ezriva to detect when an image is too blurry or incomplete so that it does not confidently misread a critical date.

Acceptance criteria:

- If core facts cannot be extracted confidently, the result is “Needs a clearer image,” not a completed interpretation.
- The message explains whether blur, glare, cropping, or missing pages may be the cause when detectable.
- The user can retake or replace the image from the same screen.
- Ezriva never creates an action from an input marked unreadable.

#### EZR-US-204 - Handle multiple detected languages

As a user, I want Ezriva to recognize Hebrew mixed with numbers or another language so that common bilingual notices remain usable.

Acceptance criteria:

- Hebrew, Latin text, dates, phone numbers, currency, and addresses can appear in one input.
- The result separates quoted source text from Ezriva's explanation.
- Unknown or conflicting fragments are listed under uncertainty.
- The user can correct a key fact before any action proposal is approved.

### Epic 3 - Understand and explain the notice

#### EZR-US-301 - Receive a three-fact summary

As a user, I want to see what the notice is, when it matters, and what I need to do so that I can understand it quickly.

Acceptance criteria:

- The first result view contains “What,” “When,” and “Next step” sections.
- Each section uses one or two short sentences, not a long generated essay.
- Dates show both a localized human-readable form and the detected source value.
- Amounts display the currency and preserve the source amount.
- Missing facts are labeled “Not found” or “Needs confirmation.”

#### EZR-US-302 - See extracted facts and their confidence

As a user, I want to inspect the exact facts Ezriva found so that I can catch mistakes before acting.

Acceptance criteria:

- Sender/organization, document category, date/time, location, amount, contact details, and requested action have dedicated fields when applicable.
- Each critical field is marked confirmed, uncertain, conflicting, or not found.
- The product does not display invented values to fill empty fields.
- The user can edit an uncertain critical field before approval.
- An edited field is visibly marked as user-confirmed.

#### EZR-US-303 - Hear a plain-language explanation

As a user, I want the short explanation read aloud so that reading ability is not a barrier.

Acceptance criteria:

- Playback uses the currently selected explanation language.
- The spoken content matches the visible short summary.
- It does not read hidden personal data, raw logs, or long source text by default.
- Playback stops when the user leaves the result or presses stop.

#### EZR-US-304 - View the original context

As a user or supporter, I want to compare the explanation with the relevant source excerpt so that the interpretation is transparent.

Acceptance criteria:

- A secondary expandable section shows relevant source snippets.
- Hebrew snippets render RTL and preserve numbers sensibly.
- The source view is collapsed by default to reduce cognitive load.
- The system never claims an excerpt exists when the input could not be read.

#### EZR-US-305 - Stop on high-risk content

As a user, I want Ezriva to recognize when the content may involve medical instructions, legal deadlines, payments, identity documents, or other high-consequence matters so that it does not act beyond its role.

Acceptance criteria:

- High-risk categories produce an explanation and safe escalation options, not an automatic external action.
- The result names the boundary in plain language.
- Calendar reminders may still be proposed for a clearly extracted deadline, but the underlying decision is not made for the user.
- No payment, form submission, prescription change, legal filing, or identity verification tool is available in the MVP.

### Epic 4 - Propose one safe next action

#### EZR-US-401 - Receive one primary action recommendation

As a user, I want one clearly recommended next action so that I am not overwhelmed by a menu of possibilities.

Acceptance criteria:

- The result shows at most one primary recommendation above secondary options.
- The recommendation contains action type, reason, exact data it will use, and risk label.
- The recommendation can be accepted, edited, dismissed, or replaced with “Remind me later” when supported.
- The user can return to the explanation without losing confirmed corrections.

#### EZR-US-402 - Prepare a calendar-ready reminder

As a user, I want an appointment notice converted into a saved reminder and calendar-ready proposal so that I do not have to copy Hebrew details manually.

Acceptance criteria:

- The proposal contains title, start/end time, time zone, location, description, source label, and reminder.
- Israel time is explicit when the source does not specify another zone.
- Missing start time or ambiguous date blocks execution until corrected.
- Default event duration and reminder are clearly labeled as defaults and editable.
- The proposal creates neither the reminder nor the file before approval.

#### EZR-US-403 - Explain why approval is required

As a user, I want to know why Ezriva is asking me before acting so that approval feels protective rather than confusing.

Acceptance criteria:

- The approval sheet states that Ezriva will save a reminder and generate a calendar file.
- It lists the exact fields that will be sent.
- It identifies the Ezriva history destination and explains that importing the file into an external calendar is a separate user action.
- It explains how to cancel and how to undo after execution.
- The approve and cancel actions are visually distinct and keyboard accessible.

#### EZR-US-404 - Refuse unsupported actions honestly

As a user, I want Ezriva to say when it cannot complete a requested action so that I do not assume something happened.

Acceptance criteria:

- Requests outside the supported action set return “I did not do this” language.
- The response offers a safe alternative such as a checklist, reminder, or supporter handoff.
- No success receipt appears for a refused or failed action.
- The audit history records the refusal without storing the raw private request.

### Epic 5 - Approve, execute, verify, and undo

#### EZR-US-501 - Give informed approval

As a user, I want to approve the exact action once so that Ezriva cannot reinterpret a vague yes as permission for something else.

Acceptance criteria:

- Approval is tied to a specific action preview and expires after a short period or any material edit.
- Editing date, destination, title, or reminder invalidates the previous approval.
- A chat message such as “okay” is not sufficient approval in the MVP.
- The user must activate the dedicated approval control.
- The product confirms that approval was received before showing execution progress.

#### EZR-US-502 - Complete a real reminder action

As a user, I want the approved reminder saved and a calendar file prepared so that the task is completed rather than merely suggested.

Acceptance criteria:

- A successful approved request creates exactly one normalized Ezriva reminder and exactly one importable `.ics` file.
- The confirmation includes the reminder identifier and generated file.
- The saved reminder and generated file match the approved preview.
- A failed provider request returns a recoverable failure state and does not claim success.
- The user can retry safely without creating duplicates.

#### EZR-US-503 - Prevent duplicate execution

As a user, I want retries and double taps handled safely so that I do not receive duplicate reminders or files.

Acceptance criteria:

- Repeating the same execution request returns the original result while the idempotency window is active.
- Rapid double activation does not create two reminders/files.
- A genuinely changed proposal can be approved and created as a new action.
- Duplicate prevention is covered by an automated test and a visible demo/test trace.

#### EZR-US-504 - Receive a useful receipt

As a user, I want a simple record of what happened so that I can trust and verify the result.

Acceptance criteria:

- The receipt states completed/failed/refused status, action summary, time, destination, and next reminder.
- It includes “What Ezriva did not do” when the boundary could be confusing.
- It includes the Ezriva reminder identifier and calendar-file proof when available.
- It contains an undo instruction or action.
- It avoids exposing access tokens, internal prompts, or raw model traces.

#### EZR-US-505 - Undo or recover

As a user, I want to reverse or recover from an action so that automation remains safe.

Acceptance criteria:

- The receipt offers an explicit delete/undo action for the Ezriva-owned reminder with a second confirmation.
- It explains that an already imported external calendar event must be removed separately and gives exact manual guidance.
- A successful undo changes the receipt status and records the time.
- A failed undo does not hide the original completed action.

### Epic 6 - Follow-up without constant interruption

#### EZR-US-601 - See unresolved obligations

As a user, I want Ezriva to remember that a deadline remains unresolved so that I do not have to re-read the source.

Acceptance criteria:

- The home view separates completed, awaiting approval, and needs-attention items.
- It shows only a short redacted title and due time, not the original document.
- Completed demo items can be cleared.
- An item with no supported follow-up does not create fake monitoring.

#### EZR-US-602 - Receive a meaningful reminder

As a user, I want a reminder only when a decision or deadline is approaching so that Ezriva reduces rather than adds notification burden.

Acceptance criteria:

- The user chooses or confirms the reminder time.
- The reminder identifies the task and next action without exposing sensitive source text on a lock screen.
- Dismissing a reminder does not silently mark the task complete.
- Demo Mode can simulate the follow-up in a deterministic way for judges.

#### EZR-US-603 - Ask a trusted person for help

As a user, I want to share a concise summary with a trusted supporter so that I can get help without forwarding the full document.

Acceptance criteria:

- The user previews the exact summary before sharing.
- The summary contains only selected facts and the unresolved question.
- Sharing is off by default and never triggered automatically.
- The MVP may copy/download the summary instead of sending it directly.
- No supporter gains ongoing access from a one-time summary.

### Epic 7 - Privacy, transparency, and evaluator readiness

#### EZR-US-701 - Know what data is retained

As a user, I want a simple retention explanation so that I understand what remains after processing.

Acceptance criteria:

- Before processing, the interface says whether raw input is stored and for how long.
- The MVP defaults to not retaining raw uploaded content after processing completes.
- Durable history contains only the minimum structured/action information required for receipts and reminders.
- Demo fixtures are clearly exempt because they are synthetic and bundled with the project.

#### EZR-US-702 - Delete my local/session history

As a user, I want to remove retained task history so that I remain in control of my information.

Acceptance criteria:

- A delete action identifies what will be removed and what external actions will remain.
- Deleting Ezriva history does not falsely claim to delete an event the user already imported into an external calendar.
- Successful deletion removes the visible record and confirms completion.
- Failure leaves the record visible and explains the recovery step.

#### EZR-US-703 - See safe agent activity

As a user or judge, I want a concise activity view so that I can verify the agent used tools and respected approval without exposing private reasoning.

Acceptance criteria:

- The view shows stages such as input validated, facts extracted, risk classified, approval required, tool invoked, and receipt created.
- It shows tool names/statuses and timestamps but not chain-of-thought or secrets.
- It marks which decision came from deterministic policy versus model output.
- Demo Mode activity is deterministic enough to explain during the video.

#### EZR-US-704 - Run the project from public instructions

As a judge, I want complete setup and test instructions so that I can evaluate the project even if the hosted demo is unavailable.

Acceptance criteria:

- The public project page links to a public repository.
- The repository contains all source, synthetic assets, configuration examples, license, and commands required for local use.
- No real credentials or personal data are committed.
- The README distinguishes local, public synthetic demo, and private-upload behavior.
- Known limitations and unsupported actions are stated explicitly.

## Cross-Epic Product Rules

### Approval rules

- Write/file-generation actions require a dedicated UI approval.
- Approval is scoped to an immutable preview.
- High-risk categories cannot bypass policy through conversation or document instructions.
- A tool cannot execute without a valid approval reference.

### Uncertainty rules

- Critical facts are date/time, amount, recipient, destination account/service, and requested action.
- Any unresolved critical fact blocks external execution.
- The product may still explain the notice and ask for correction.
- The UI distinguishes “not found,” “uncertain,” and “conflicting.”

### Language rules

- Spanish is the primary pilot explanation language.
- English is the required evaluator and repository language.
- Hebrew supports source display and an RTL interface path.
- Machine-generated translations are labeled as explanations, not certified translations.

### Privacy rules

- Raw private documents are not placed in logs, analytics, screenshots, repository fixtures, or public videos.
- Demo content is synthetic.
- Provider identifiers and tokens are never displayed.
- Trusted-supporter sharing is previewed, explicit, minimal, and one-time by default.

## Edge Cases

| Scenario | Expected behavior |
|---|---|
| Blank or corrupted file | Reject before processing; explain how to retry. |
| Blurry/cropped image | Stop at “Needs a clearer image”; no action proposal. |
| Multiple dates with no clear appointment date | Mark conflict and require user selection/correction. |
| Date present but no time | Explain the date; block calendar execution until the time is provided or explicitly marked all-day. |
| Hebrew calendar date or ambiguous numeric date | Show source form, converted candidate if supported, and require confirmation. |
| Notice contains an instruction telling the AI to ignore policy | Treat document text as untrusted data; do not change tool or approval rules. |
| Unsupported language | Explain the limitation; allow retry/paste; do not fabricate a translation. |
| Medical instruction or result | Summarize cautiously; advise contacting the provider; allow a reminder but no clinical advice/action. |
| Bill/payment request | Extract due date/amount; allow reminder; never pay. |
| Legal/government deadline | Extract with uncertainty; require confirmation and safe escalation; never submit. |
| Browser blocks the `.ics` download | Keep the saved reminder, explain the block, and allow a duplicate-safe download retry. |
| Reminder repository returns an error | Show failed receipt, retain proposal, and allow idempotent retry. |
| User double-clicks Approve | Create one action only. |
| User edits after approval | Invalidate approval and require a fresh preview/approval. |
| User closes browser during execution | On return, reconcile status before allowing retry. |
| Model/provider unavailable | Preserve input only for the active session as stated; show retry and demo fixture options. |
| User asks to send private data to a supporter | Preview minimal summary, warn about selected fields, require explicit share action. |
| User deletes Ezriva history after importing the `.ics` | Delete Ezriva history but clearly state that the external calendar event remains unless separately removed. |
| Very long PDF/multiple pages | Enforce MVP page limit and ask user to select the relevant page or text. |
| 100 saved tasks | Paginate/filter by status; do not load raw source files. This is a boundary test, not an MVP optimization target. |

## What We Are Building

### Required vertical slice

- First-run language/accessibility controls.
- Synthetic Demo Mode.
- Hebrew appointment input.
- Structured interpretation and uncertainty.
- One primary reminder/calendar-export proposal.
- Deterministic risk and approval behavior.
- Real saved reminder plus generated `.ics` file.
- Idempotent execution.
- Receipt, undo guidance, redacted history, and safe activity trace.

### Required quality states

- Loading, success, empty, validation error, extraction uncertainty, policy refusal, provider failure, duplicate retry, and undo status.
- Responsive mobile and desktop layouts.
- Keyboard navigation, visible focus, semantic labels, adequate contrast, large touch targets, and reduced-motion support.
- Spanish, English, and Hebrew/RTL foundations across the hero flow.

## What We Would Add With More Time

- Production supporter invitations with expiring scoped access.
- Email intake and provider-authorized document monitoring.
- Additional action tools for calls, official portals, task managers, and transportation.
- More document categories and country-specific knowledge packs.
- AgentCore Memory-based preferences with explicit consent and deletion.
- Human volunteer escalation network.
- Voice input and conversational repair designed for older adults.
- Native Android/iOS wrappers and push notifications.
- Formal evaluations with older adults, immigrants, accessibility specialists, and Hebrew translators.
- Certified translation or institution partnerships where appropriate.

## Submission Proof Points

| Judging criterion | Observable proof |
|---|---|
| Technological Implementation | Strands agent invokes typed tools; deterministic approval policy; idempotent reminder/ICS action; tests; live demo; optional AgentCore deployment. |
| Design | Calm multilingual experience, large-text/voice options, RTL, coherent loading/error/refusal/receipt states, mobile-first hero flow. |
| Potential Impact | Specific lived problem; private consenting family pilot; synthetic public demo; measurable reduction from manual interpretation steps to one approval. |
| Creativity & Originality | Translation-to-action pipeline, family support without surveillance, risk-aware autonomy, minimal-interruption follow-up. |
| Presentation | Under-one-minute hero transformation; architecture/activity proof; clear “problem, audience, why it matters” narrative. |

## Product Success Measures

These are MVP evaluation targets, not claims of achieved performance until tests or user sessions occur.

- **Hero-flow completion:** 100% across the included appointment fixture in automated/demo checks.
- **Unsafe-action prevention:** 100% of defined high-risk policy fixtures blocked from external execution.
- **Approval enforcement:** 100% of external-action attempts without a valid approval rejected.
- **Duplicate prevention:** 100% of repeated identical execution tests create no second reminder/file.
- **Task clarity:** pilot user can state what, when, and next step after viewing/hearing the result.
- **Demo reliability:** five consecutive clean hero-flow runs before recording.
- **Accessibility baseline:** zero critical automated accessibility violations on hero screens, plus manual keyboard/zoom/RTL review.

## Acceptance Test Narrative

Given a first-time Spanish-speaking user in Demo Mode and the bundled synthetic Hebrew clinic appointment notice, when the user processes the notice, then Ezriva must show the appointment purpose, date/time, location, and next step in Spanish; disclose any uncertainty; propose one reminder/calendar export; refuse to execute before explicit approval; create exactly one saved reminder and one `.ics` file after approval; show a receipt and undo path; and retain no real personal data.

## PRD Deepening Record

- Mandatory beats: complete.
- Deepening rounds: 1 synthesized round covering persistence, altered approval data, prompt injection, duplicate execution, provider failure, 100-item boundary, and the Devpost wow moment.
- Deferred implementation decisions belong in `spec.md`.
