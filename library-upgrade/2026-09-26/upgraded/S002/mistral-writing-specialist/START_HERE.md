# START HERE

## Recommended route

Use a text chat.

No installation is required.

No API key is required.

1. Open a text host.
2. Paste `prompts/director.md`.
3. Supply needed source text.
4. State one deliverable.
5. Choose a source contract.
6. Request one method.

For supplied documents,
choose FAITHFUL first.

## Mistral Studio route

Use Studio only
when your account exposes it.

Choose an available model.

Paste `prompts/studio-agent.txt`.

Start without custom functions.

Test one writing task.

Add tools after validation.

No paid call
is authorized automatically.

## Local runner route

Python 3.10+ is optional.

No pip package is required.

From the package folder:

`python -m unittest discover -s tests -v`

Expected result:

all included tests pass.

Then try offline composition:

`python writer.py compose --mode outline --input examples/brief.txt --output private/outline-packet.txt`

Expected result:

a new text packet appears.

Common errors:

`python` not found:
use the browser route.

output already exists:
choose another filename.

missing API key:
stay offline.

Undo:

delete only task-owned outputs.

Do not delete Python.

## Visual fallback

Use image tools
when available.

Otherwise use editable SVG.

See:

`examples/illumination-key-state.svg`

The SVG is usable.
It is not evidence.
