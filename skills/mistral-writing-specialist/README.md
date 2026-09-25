# Mistral Writing Skills Specialist / Story Studio

A reusable specialist for building and upgrading a Mistral writing system, plus an author-facing writing agent. Version 1.0.0. Documentation checked 25 September 2026.

Start with **STUDIO_SETUP.md**. For the prompt field, use **prompts/studio-agent.txt**. The root **SKILL.md** is the agent-building specialist, not the author-facing system prompt.

## What is included

The Story Bible follows the supplied layout: Braindump, Genre, Style, Synopsis, Characters, Worldbuilding and Outline. Timeline, Canon, Sources and Session records support continuity and resumption. Six methods handle story architecture, scene drafting, editing, continuity, factual research and audiobook performance coaching. Commands `/bible`, `/outline`, `/draft`, `/edit`, `/continuity`, `/research` and `/audiobook` are prompt conventions; the local runner uses the corresponding `--mode` value.

Approved material, proposals and working drafts are separate. The optional runner provides actual transactional local storage, version checks, duplicate-call receipts, host-only approval and bounded cloud calls. The full Studio prompt works without this runner, using manual project context and explicit proposed changes. Neither mode automatically publishes writing or sends messages.

## Two supported setup paths

**Studio-only:** create an agent using the compiled Studio prompt, start with built-in tools only, and supply relevant project context. No local install is needed. Native Skills can be created separately where the chosen Mistral surface supports them; merely saving a Skill does not prove it is attached to an API agent.

**Optional local runner:** Python 3.10+ and its standard library; no pip packages, Docker, vector database, local model or GPU inference. `compose` and local project operations work offline. `run`, `models` and `deploy` use Mistral only after `--allow-cloud`. Read the privacy and service limitations in STUDIO_SETUP.md.

```powershell
python -m unittest discover -s tests -v
python writer.py init
python writer.py compose --mode outline --input examples/brief.txt --output private/outline-packet.txt
```

The packet can be pasted into a capable text model when API access is absent. It is not generated prose: it contains the instructions and source task.

```powershell
# Set MISTRAL_API_KEY privately in this terminal; never put it in a manuscript or Git.
python writer.py models --allow-cloud
python writer.py run --mode outline --input examples/brief.txt --allow-cloud --output private/outline-result.json
python writer.py proposals
# Inspect the complete proposal before this host-only approval command.
python writer.py approve --proposal PROPOSAL_ID_FROM_OUTPUT
python writer.py export --output private/story-bible-v1.json
```

Each `run` is a bounded task, not a persistent cloud conversation. Local project state is reusable. Supply a checkpoint for conversational continuity and the desired scene context. Outputs are JSON so usage, status and text/chunks are not silently discarded. Read `content` for the prose.

## Optional hosted agent creation

```powershell
python writer.py deploy --dry-run
python writer.py deploy --allow-cloud --output private/agent-receipt.json
```

The second command creates a hosted Mistral agent using the compiled instructions. It does not upload native Skills, upload your manuscript, create Libraries or connect SQLite. Add `--web-search` or repeated `--library-id ID` only for services you have configured. The generated hosted agent contains no local function schemas. To use the local function loop, use `run` instead. Check Studio and the saved receipt before repeating deployment after an uncertain network outcome.

## Status and boundaries

See **TEST_REPORT.md** for the executed offline checks. Live Mistral calls, native Skill activation and model-quality trials were not performed in this build. **EVALUATION.md** contains the acceptance cases to run on the chosen models. This is not model weight fine-tuning, an independently measured performance guarantee, or a clone of the unidentified mobile writing application.

The reusable pack contains only instructions, blank templates and fictional examples. Keep manuscripts, project databases, receipts and credentials in `private/`, outside public Git. `.gitignore` is a convenience, not a security boundary. The local SQLite database is not encrypted; use operating-system protections and backups. Cloud execution sends the input plus any model-requested project sections to Mistral.

## File map

`SKILL.md` — build/upgrade specialist. `prompts/` — full Studio, selective-load, compact and app personalization prompts. `writing-skills/` — six focused methods. `knowledge/` — blank project template. `writer.py` + `tools.json` — executable reference runner and its function contracts. `config.json` — adjustable resource defaults. `tests/`, `EVALUATION.md`, `TEST_REPORT.md` — validation and trial boundaries. `SOURCES.md` — documentation and adaptation provenance.
