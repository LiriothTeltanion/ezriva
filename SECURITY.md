# Security Policy

Ezriva is an early hackathon build. Do not use it for real medical, legal,
financial, identity, or government decisions.

## Supported data

Only bundled synthetic fixtures are supported in the public demo. Private
uploads remain disabled until authentication, retention, redaction, and abuse
controls have been implemented and verified.

## Reporting

Do not open a public issue containing a secret, personal document, account
identifier, or exploit payload. Use the repository's **Security** tab and
select **Report a vulnerability** so the report remains private. If private
vulnerability reporting is temporarily unavailable, do not publish sensitive
details; open a content-free issue asking the maintainer to enable a private
reporting channel.

## Non-negotiable controls

- no write without server-verified payload-bound approval;
- no owner identity supplied by a model or untrusted client field;
- no raw documents, prompts, secrets, or tool arguments in telemetry;
- no arbitrary shell, browser, filesystem, or HTTP agent tools;
- deterministic policy and conditional idempotent writes.
