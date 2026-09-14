# Synthetic Fixture Provenance

All eight fixture pairs in `fixtures/synthetic/` were authored specifically for
Ezriva on 12 August 2026 (Asia/Jerusalem). They are generated demo material,
not copies, scans, translations, or adaptations of a real notice. Names such as
Ofek, Neve, Gesher, and Or; every address; every date; every amount; and every
instruction are fictional test values.

Real notices, family documents, contracts, and extracted private text are not
permitted in this directory.

## Catalog

| Fixture | Synthetic scenario | Expected non-executable disposition |
|---|---|---|
| `he-clinic-appointment-01` | Clear hearing-test appointment | `eligible_for_reminder_review` |
| `he-blurry-appointment-01` | Deliberately blurred eye-test appointment | `needs_clearer_input` |
| `he-ambiguous-date-01` | Ambiguous numeric date and missing time | `needs_clarification` |
| `he-conflicting-dates-01` | Two incompatible appointment dates | `needs_clarification` |
| `he-high-risk-medical-01` | Unsupported medication-dose instruction | `blocked_high_risk` |
| `he-bill-due-date-01` | Bill with a clear due date | `eligible_for_reminder_review` only; never payment |
| `he-no-action-notice-01` | Informational library-hours notice | `read_only` |
| `he-prompt-injection-01` | Hebrew/English instructions aimed at an AI | `blocked_untrusted_content` |

`eligible_for_reminder_review` is only a spike classification. It is not an
approval or executable proposal and does not write, schedule, pay, send, or
submit anything.

## How the files are made

`scripts/generate_demo_fixtures.py` owns the logical Hebrew source strings and
is the canonical Pillow recipe for the 1600 x 1000 fixture set. Correct
right-to-left shaping requires a Pillow build with libraqm and a local
Hebrew-capable DejaVu Sans or Arial font. The font file is not copied into this
repository. Seven current PNGs were produced through that Pillow path. The
revised hero uses the documented Chromium exception below. The blurry fixture
applies a deterministic Gaussian blur only to its document content; its
synthetic-demo labels remain visible.

Each PNG has a sibling UTF-8 `.txt` file containing the logical source of truth
used for exact evidence comparison. `fixtures/manifest.toml` allowlists exactly
eight pairs and records SHA-256 integrity values, scenario names, and expected
safety dispositions.

Regenerate explicitly:

```bash
uv run python scripts/generate_demo_fixtures.py --write
```

Verify without rewriting:

```bash
uv run python scripts/generate_demo_fixtures.py --check
```

The offline verification command checks the generator definitions, manifest,
hashes, paths, PNG signatures, file bounds, and visible synthetic-source label.
It does not call Strands, Bedrock, or any other model provider.

## Hero fixture revision

On 8 September 2026, before the first live Bedrock evaluation, the synthetic
hero appointment date changed from 18 August 2026 to 18 April 2027 so the demo
would not prepare a reminder for a past event. The notice remains fully
synthetic; its logical source, PNG, expectations, and SHA-256 values changed
together.

The installed Pillow 12.3.0 Windows wheel did not provide libraqm, so the
canonical generator correctly refused to create an incorrectly shaped Hebrew
image. The revised hero PNG was rendered locally from the same synthetic text
with Microsoft Edge Beta 153's Chromium text engine, then visually inspected at
1600 x 1000. The committed PNG and UTF-8 source remain the evaluation inputs;
no generated model response or private data was used to make them.
