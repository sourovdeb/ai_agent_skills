# Validation report — v1.0.0

Checked 25 September 2026. Environment: Python 3.13.5 in the build container. No credentials or live Mistral API calls were used.

## Executed

`python -m unittest discover -s tests -v`: **37 tests passed**, zero failures and zero errors. The final run took 0.115 seconds in this container; this is not a benchmark for the user's computer or an AI model.

The tests cover project initialization and readback; all eleven sections; proposal versus approved canon; version conflicts; retained history; idempotent approval and duplicate tool receipts; malformed JSON, unknown functions, invalid sections, unexpected arguments and type checks; draft isolation; mocked tool-call round trips; truncation reporting; sequential execution and request limits; compiled prompt completeness; offline composition; explicit cloud authorization; endpoint restrictions; no-overwrite output behavior; and absence of the test credential from composed instructions.

`python -m py_compile writer.py tests/test_writer.py`: passed.

CLI smoke checks: `compose --mode outline` created a 7,279-byte offline instruction packet from the fictional example; `deploy --dry-run` produced a 16,363-byte hosted-agent request payload. No agent was created by the dry run. Both outputs remained outside the published package.

All package JSON files parsed. Function declarations matched the three implemented handlers. The compiled Studio prompt contained the director instructions and all six focused methods.

## Not executed

Live Mistral authentication, account model availability, hosted-agent creation, native Skill activation, Library retrieval, Prompt Registry integration, model-quality trials, narration rehearsal and target-machine performance measurements were not executed. The 37 checks are code and artifact tests, not evidence that every model follows the writing instructions or produces strong prose.

The package's declared Python 3.10+ compatibility is based on the language/library features used; this build ran on Python 3.13.5 only. Run the included tests on the actual target interpreter. Run EVALUATION.md on each selected model and host before production use.

## Release scope

New reusable instructions, blank project data, fictional examples, a standard-library reference runner, documentation and tests. No earlier repository skill is replaced. No private manuscript, screenshot, API key, local project database or personal email address belongs in this release.
