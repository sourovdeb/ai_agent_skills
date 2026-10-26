# CHANGELOG

## 1.1.0

Upgrade type:
`REVIEW_VERIFICATION`

Review status:
`review-verified` (2026-10-26)

Preserved:
- seven author-facing Story Bible sections plus Timeline, Canon, Sources and Session records;
- six focused writing methods (story-bible, scene-draft, editor, continuity, research, audiobook);
- CANON / PROPOSAL / DRAFT separation with host-only approval;
- transactional SQLite storage, revision checks, duplicate-call receipts and retained history;
- endpoint allowlist, redirect refusal, explicit `--allow-cloud` gate and no-overwrite output writes;
- honest test boundaries (offline only; live model trials not run);
- source discipline in SOURCES.md (official docs, checked 2026-09-25).

Changed:
- version bumped 1.0.0 to 1.1.0 across SKILL.md metadata, config.json, all six writing-skills and documentation;
- review status recorded as `review-verified` with review date in SKILL.md metadata;
- offline test suite expanded from 37 to 57 tests covering CLI behavior, API boundaries, canon lifecycle, security hygiene and documentation consistency;
- TEST_REPORT.md updated with the expanded executed checks and unchanged not-executed boundaries.

Added:
- this CHANGELOG.md (preserved/changed/added map plus source commit and blob);
- 20 new offline tests: CLI lifecycle (init, compose, run gate, models gate, deploy gate, deploy dry-run, proposals, approve, export), tool batch limit, malformed tool arguments, unknown tool name, call-id idempotency and reuse rejection, path-traversal draft title, oversized/whitespace/negative/boolean argument rejection, endpoint allowlist breadth, redirect refusal, API-key absence from composed instructions, non-finite JSON rejection, NaN-safe dump, and full canon lifecycle (stage, list, approve, history, idempotent re-approval, export, stale-revision rejection, draft isolation, ordered multi-call batch).

Removed:
- nothing.

Source:
`skills/mistral-writing-specialist/SKILL.md`

Source commit:
`02602051fcbbcc38b0ae3e7a18a6a9c83ec0e958`

Validation:
- `python -m unittest discover -s tests -v`: 57 tests, 0 failures, 0 errors;
- `python -m py_compile writer.py tests/test_writer.py`: passed;
- CLI smoke checks: `init`, `compose --output`, `deploy --dry-run`, `proposals`, `export --output` all exercised in a temporary directory;
- 79 additional ad-hoc verification checks (package consistency, CLI behavior, API boundaries, canon lifecycle, documentation consistency) all passed.

Not executed (unchanged):
- live Mistral authentication, hosted-agent creation, native Skill activation, Library retrieval, Prompt Registry integration, model-quality trials, narration rehearsal and target-machine performance measurements.
