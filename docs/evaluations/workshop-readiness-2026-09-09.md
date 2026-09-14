# Workshop Readiness - 9 September 2026

**Status:** Local preparation is complete; authenticated AWS preparation still
requires Kevin to be present.

This dated runbook is operational evidence, not part of the five-file product
contract. Event details were checked on 8 September 2026 and should be rechecked
on the official Resources page before joining.

## Objective

Leave the workshop with a safe AWS session, a confirmed image-capable Bedrock
model or inference profile and region, and clear answers about logging and
AgentCore. Do not widen the MVP or send a real family document.

## Local baseline to bring

- Ezriva `main` is based on `80f135434a9a942b696dd41d792735a316f003fe`.
- Item 1 is complete; item 2 is active.
- Eight synthetic fixture pairs and the complete offline verification contract
  pass locally.
- Live Bedrock attempts remain `0/8`; Pause 1 remains pending.
- The public demo remains synthetic-only.

Open `START-HERE.md`, this runbook, the item-2 evaluation report, and the hero
fixture before the session.

## Kevin-only account preparation

1. Confirm Devpost registration and access to the official Resources page.
2. Create or sign in to AWS Builder ID in Kevin's own browser session.
3. Confirm whether an AWS account with billing and MFA already exists. Builder
   ID alone does not provide Bedrock access.
4. Configure an AWS CLI v2 temporary or SSO session outside chat and outside the
   repository. Never paste credentials, account IDs, tokens, or MFA codes into
   Codex or project files.
5. Tell Codex only `AWS ready`; Codex can then perform the documented read-only
   preflight without displaying identifiers.

## Questions for the AWS mentors

1. Which image-capable Amazon Nova model or inference profile is actually
   available from `il-central-1` for this account, and in which geography can
   inference data be processed?
2. What is the safest read-only way to prove model-invocation content logging is
   disabled before sending the eight synthetic fixtures?
3. Which temporary-login flow is preferred for a Windows 11 development laptop:
   `aws login`, IAM Identity Center, or another non-root option?
4. Would AgentCore in Frankfurt materially improve the judging proof after the
   local vertical slice, or would it add avoidable regional, privacy, and cost
   complexity?
5. Is the promotional-credit request associated with Devpost registration or
   the AWS account, and what confirmation should be retained without exposing
   identifiers?

## Cost and safety gate

No Bedrock invocation is authorized by this runbook. After authenticated
read-only discovery, state the model, region/profile, data geography, published
price, and a USD/ILS ceiling. Obtain Kevin's narrow approval before running only
`scripts/run_ai_fixture_eval.py`: at most eight calls, one per fixture, no retry,
no repair, no action tools, and early stop on a terminal provider error.

If no safe session is available, use the workshop for account and region
clarification and keep the verified offline result. Do not bypass the gate.

## Current official links

- [Agents for Humans resources](https://agentsforhumans.devpost.com/resources)
- [Agents for Humans rules](https://agentsforhumans.devpost.com/rules)
- [AWS Builder ID and AWS account differences](https://docs.aws.amazon.com/signin/latest/userguide/differences-builder-id.html)
- [Create an AWS Builder ID](https://docs.aws.amazon.com/signin/latest/userguide/create-builder-id.html)
- [Create an AWS account](https://docs.aws.amazon.com/accounts/latest/reference/getting-started.html)
- [Bedrock model-invocation logging](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html)
