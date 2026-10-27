# Open Writer OS

A free, open-source writing assistant for fiction and memoir writers.
Everything is plain Markdown in a folder you own. The AI is a tool you point
at your project; you stay the author.

**Free for non-profit use by writers, educators and communities — including
writers in India and Africa.** No account, no subscription, no per-word
credits, no data leaving your machine when you run it locally.

## Why this exists

Commercial AI writing tools charge per word or per credit, which makes a
full novel expensive, and their story bibles live inside their platforms.
Open Writer OS keeps your story bible, canon ledger and manuscript as files
on your disk, and works with any model you can reach — including a small
model running offline on your own laptop via [Ollama](https://ollama.com).

## Two ways to run it

### 1. Fully offline with Ollama (recommended to start)

```bash
# install Ollama, then pull a model once
ollama pull llama3.2

# create a project and a book
python -m open_writer_os init ~/my-novel --name "My Novel"
python -m open_writer_os new-book ~/my-novel --title "The Salt Road"

# run a writing mode (nothing leaves your machine)
python -m open_writer_os run ~/my-novel draft --book "The Salt Road" \
    --prompt "Draft the opening scene: Mira finds the letter."
```

List locally available models with:

```bash
python -m open_writer_os models ~/my-novel
python -m open_writer_os set-model ~/my-novel --model mistral
```

### 2. Via an API (OpenAI-compatible)

Works with OpenRouter, Together, Groq, Mistral, or any self-hosted
OpenAI-compatible endpoint:

```bash
python -m open_writer_os init ~/my-novel --backend openai \
    --base-url https://openrouter.ai/api/v1 --model "anthropic/claude-3.5-sonnet"

export OPEN_WRITER_OS_API_KEY="your-key-here"   # never stored on disk
python -m open_writer_os run ~/my-novel draft --book "The Salt Road" \
    --prompt "Draft the opening scene."
```

The API key is read from the environment only. `provider.json` stores just
the backend, base URL and model name — no secrets.

## The twelve writing modes

Adapted from the MISHU Writer OS. The writer owns the story; the modes
draft, propose and audit.

| Mode | What it does |
|---|---|
| `discover` | Extracts the story from messy notes; asks only questions that change the story |
| `architect` | Works on structure and causality; never writes polished prose |
| `scene-plan` | Produces a scene contract: who wants what, what changes, canon dependencies |
| `draft` | Writes prose from an approved scene plan; ends with a CANON CHECK |
| `dialogue` | Dialogue, subtext and voice work |
| `describe` | Sensory and environmental depth without advancing the plot |
| `deepen` | Psychological depth, tension and interiority |
| `compress` | Cuts redundancy; shows every cut and why |
| `continuity` | Audits names, dates, timeline, knowledge states, world rules; rewrites nothing |
| `revise` | Revises a passage toward a stated goal, preserving voice |
| `canon-update` | Promotes accepted facts to CANON in the ledger, with evidence |
| `profile-update` | Records writer preferences in the profile |

## Skill packs

Specialized instruction packs layered on top of the modes:

```bash
# short fiction: single-arc discipline, word-count targets, ending rules
python -m open_writer_os run ~/my-novel draft --book "The Salt Road" \
    --skill short-fiction --prompt "..."

# biography/memoir: evidence statuses, interview-to-prose flow, privacy rules
python -m open_writer_os run ~/my-novel draft --book "Grandmother's War" \
    --skill biography --memoir --prompt "..."
```

## Project folder canon

```
my-novel/
    provider.json            backend + model (no secrets)
    README.md
    AUTHOR/                  your profile, style constitution, preferences, AI rules
        00_WRITER_PROFILE.md
        01_STYLE_CONSTITUTION.md
        02_CREATIVE_PREFERENCES.md
        03_AI_WORKING_RULES.md
    PROJECTS/<BOOK>/         one folder per book
        PROJECT_CORE.md      story in plain language, conflict, tone, non-negotiables
        STORY_BIBLE.md       characters, world rules, history — factual only
        CANON_LEDGER.md      important facts with statuses (CANON, PROPOSED, ...)
        CURRENT_STATE.md     what is happening right now
        STYLE_TARGET.md      the sound you want (learned from prose you approve)
        CHARACTERS/ OUTLINE/ SCENES/ MANUSCRIPT/ NOTES/
    ENGINES/                 reserved for custom mode instructions
```

Everything is Markdown. Read it, edit it by hand, back it up, put it in git.

## Source-of-truth order

When information conflicts, the system follows: (1) your current explicit
statement, (2) writer-confirmed canon, (3) approved manuscript, (4) current
story state, (5) story bible, (6) project core, (7) approved outline,
(8) planning notes, (9) AI suggestions, (10) AI guesses. Guesses never
override confirmed information.

## Export

```bash
python -m open_writer_os export ~/my-novel --book "The Salt Road" --out novel.md
```

Exports the book's core files plus all CHARACTERS/, OUTLINE/, SCENES/,
MANUSCRIPT/ and NOTES/ files as one Markdown document. It is a plain-text
snapshot — convert to .docx with Pandoc (`pandoc novel.md -o novel.docx`) or
any word processor.

## Small-model discipline

The system is built for small local models: one task per request, short
retrieval sets (context is capped at 12,000 characters), and no combined
"plan + draft + check + update" operations. If you run a 7B model locally,
keep each `run` to a single mode.

## Development

Standard library only — Python 3.10+, no dependencies to install.

```bash
cd projects/open-writer-os
python3 -m unittest discover -s tests -v
```

## License and use

Free for non-profit use by writers, educators and communities. If you build
on it, keep it open. The MISHU Writer OS method it adapts is credited in
`open_writer_os/engines.py`.
