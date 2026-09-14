# Codex Handoff

This file is the repository reading and resume index for Ezriva. It does not
duplicate the product requirements or make historical checks current.

## Authority

When information differs, use this order:

1. Kevin's current explicit request.
2. The applicable `AGENTS.md` instructions.
3. `docs/hackathon-build/scope.md` for feature cuts.
4. `docs/hackathon-build/prd.md` for observable behavior.
5. `docs/hackathon-build/brand-ux.md` for identity, trust, and accessibility.
6. `docs/hackathon-build/spec.md` for architecture and safety.
7. `docs/hackathon-build/checklist.md` for execution order.
8. Current Git, code, and freshly executed verification evidence.
9. Dated evaluation documents as historical evidence only.

## Mandatory Reading Order

After opening `START-HERE.md` and reading this handoff completely, read every
tracked file in this order:

1. `AGENTS.md`.
2. `README.md`.
3. `docs/hackathon-build/README.md`.
4. `docs/hackathon-build/scope.md`.
5. `docs/hackathon-build/prd.md`.
6. `docs/hackathon-build/brand-ux.md`.
7. `docs/hackathon-build/spec.md`.
8. `docs/hackathon-build/checklist.md`.
9. `docs/hackathon-build/build-notes.md`.
10. `SECURITY.md`, `PRIVACY.md`, `CONTRIBUTING.md`, `LICENSE`, and
    `CHANGELOG.md` when present.
11. `docs/decisions/`, `docs/evaluations/`, and `docs/submission/`, each in
    lexical path order.
12. Root configuration, manifests, workflow, and lockfiles in lexical order.
13. `apps/api/src/`, then `apps/web/`, excluding generated output.
14. `apps/api/tests/`, then `scripts/`.
15. `fixtures/manifest.toml`, `fixtures/provenance.md`, and every tracked
    synthetic `.txt` fixture in lexical order.
16. Visually inspect every tracked synthetic image in lexical order.
17. Read tracked files under `infra/`, if any.
18. Run `git ls-files` and read any remaining tracked file not covered above.

Do not inspect ignored dependencies, virtual environments, build output,
caches, private artifacts, `.env` values, credential stores, or
`project_sources/`.

## Resume Rule

Determine the active work item from the first unchecked checklist entry and
current Git/code evidence. Do not begin the next checklist item before the
active item's acceptance and required Kevin pause.

Fixtures, hand-authored candidates, mocked providers, previous logs, or a
schema-valid response are not proof of a current live model result. Public and
recorded demos remain synthetic-only.

## Current Checkpoint - 8 September 2026

- Branch/base before the current uncommitted increment: `main` at
  `80f135434a9a942b696dd41d792735a316f003fe`.
- Item 1 is complete.
- Item 2 is the only active checklist item.
- The current uncommitted item-2 increment passed the offline fixture and full
  local verification contracts; see
  `docs/evaluations/item-2-offline-revalidation-2026-09-08.md`.
- Live Bedrock evaluation remains `0/8`; Pause 1 is pending.
- Item 3 must not start until the bounded live evaluation succeeds and Kevin
  approves Pause 1.
- No account creation, AWS resource, credit request, deployment, commit, push,
  or publication is authorized by this handoff. Re-run verification if the
  working tree changes after the dated evidence.

## Current Item-2 Verification Contract

Use the pinned project runtime. On Kevin's Windows machine, put the repository's
ignored portable `uv` 0.11.33 directory first on the task-local `PATH` when the
global `uv` differs from the required version.

```powershell
python scripts/verify.py ai-fixtures
python scripts/verify.py verify
npm audit --audit-level=high
git diff --check
git status --short --branch
```

The live path is only `scripts/run_ai_fixture_eval.py`. Before any call, require
an external AWS session, discover the actual image-capable model/profile,
verify Bedrock model-invocation content logging is disabled, state the current
USD/ILS budget, and obtain narrow approval. Maximum: eight fixtures, one call
each, no retry or repair, no action tools, and early stop on a terminal provider
failure.

## Truth Pointers

- Public project status: `README.md`.
- Feature cuts and product behavior: `docs/hackathon-build/`.
- Execution order: `docs/hackathon-build/checklist.md`.
- Decisions and active-shaping record: `docs/hackathon-build/build-notes.md`.
- Latest dated checks: `docs/evaluations/`.
- Runtime behavior: `apps/`, `scripts/`, and `fixtures/`.
- Repository truth: `git status`, `git log`, current diff, and fresh checks.

If these disagree, stop implementation, label the contradiction, and reconcile
it with evidence before continuing.
