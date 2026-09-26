# TEST REPORT

Candidate: 1.1.0.

Date: 26 September 2026.

## Candidate execution

Command:

`python -m py_compile writer.py tests/test_writer.py tests/test_candidate_contract.py`

Outcome:

PASS.

Command:

`python -m unittest discover -s tests -v`

Outcome:

37 source regression tests passed.

Runtime:

Python in build container.

No network calls occurred.

The suite covered:

- local project initialization;
- canon staging and approval;
- history retention;
- idempotent receipts;
- stale revision rejection;
- malformed tool rejection;
- draft isolation;
- mocked tool round-trips;
- truncation reporting;
- request budgets;
- sequential tools;
- JSON parsing;
- method loading;
- compiled prompt assembly;
- offline composition;
- deployment dry-run;
- cloud authorization boundary;
- endpoint allowlist;
- output no-overwrite;
- template validation;
- credential exclusion.

Candidate contract script ran.

Seven deterministic checks passed.

Those checks covered:

- source contracts;
- compiled prompt assembly;
- all 74 audit IDs;
- SVG parsing;
- SVG accessibility;
- FAITHFUL source ordering;
- provider fallback boundaries.

## Visual execution

The SVG was rendered.

ImageMagick produced PNG.

The PNG was inspected.

Labels remained readable.

No source prose disappeared.

## Not executed

Live Mistral calls.

Hosted Agent creation.

Native Skill activation.

Library retrieval.

Prompt Registry calls.

TypeSafe execution.

Agnes execution.

Target-model writing trials.

Image-provider generation.

Author A/B review.

Narrator rehearsal.

## Validation

`BEHAVIOR_TESTED`

This applies locally.

Target behavior remains untested.

Release gate G5 stays partial.

Do not call this deployed.
