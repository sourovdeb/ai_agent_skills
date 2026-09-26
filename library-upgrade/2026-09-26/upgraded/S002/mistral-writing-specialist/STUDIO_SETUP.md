# Setup routes

Use the smallest route
that meets the task.

## Route A: text chat

This is recommended.

No install is required.

No API key is required.

Paste `prompts/director.md`.

Supply relevant source material.

Choose one source contract.

Choose one writing method.

This route provides
instruction-only writing assistance.

It does not provide
persistent project state.

## Route B: Mistral Studio

Use Studio only
with an active account.

Current official documentation,
checked 26 September 2026,
lists Mistral Small 4.

Its API identifier is
`mistral-small-2603`.

Official documentation lists
Agents and function calling.

Studio also documents Skills.

Account model availability
still needs checking.

Do not assume access.

Paste `prompts/studio-agent.txt`.

Start without custom functions.

Add built-in tools
only when needed.

Web search and code tools
vary by API surface.

Check current documentation.

API use may cost money.

Do not make paid calls
without authorization.

Current published pricing
was checked separately.

Recheck before spending.

## Route C: local runner

Requires Python 3.10+.

No pip package is required.

Run:

`python -m unittest discover -s tests -v`

Then:

`python writer.py init`

Then offline composition:

`python writer.py compose --mode outline --input examples/brief.txt --output private/outline-packet.txt`

Cloud commands require:

`--allow-cloud`

Cloud commands also need
`MISTRAL_API_KEY`.

Keep keys outside prompts.

## What local tools mean

`tools.json` declares:

`get_project_context`.

`stage_canon_update`.

`save_draft`.

`writer.py` implements them.

Declarations alone
do not execute anything.

Hosted Studio agents
cannot access local SQLite
without an actual bridge.

Do not register
nonfunctional local tools.

## Story Bible

The template contains:

Braindump.

Genre.

Style.

Synopsis.

Characters.

Worldbuilding.

Outline.

Support records include:

Timeline.

Canon.

Sources.

Session.

Unknown fields stay unknown.

## Provider fallback

Mistral fails?

Preserve completed work.

Use another authorized
text host.

Native Skills unavailable?

Use compiled instructions.

Library unavailable?

Paste versioned excerpts.

Search unavailable?

Mark evidence gaps.

Image rendering unavailable?

Use editable SVG.

TypeSafe unavailable?

Continue without it.

Agnes unavailable?

Continue without it.

## Privacy

Keep manuscripts private.

Keep credentials private.

Keep receipts private.

Do not upload elsewhere
without authorization.

SQLite is unencrypted.

Use OS protections.

## Verification

A saved prompt
is not deployment.

A Skill listing
is not agent attachment.

A dry-run payload
is not agent creation.

A tool schema
is not a working tool.

Verify each postcondition.
