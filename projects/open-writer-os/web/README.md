# Open Writer OS 2.0 (web)

The browser version of Open Writer OS. Plain HTML + JavaScript, no
framework, no build step for the app itself; the Python server is standard
library only. **Runs on your own computer** — a hosted page cannot reach
Ollama or your API key, so this is a local app, exactly like v1.0.

## Run with Ollama (offline, private)

```bash
ollama pull llama3.2          # or any small instruct model
python3 serve.py              # then open http://localhost:8099
```

In Settings press **Test and list models** and pick one. Browse current
models at ollama.com/library. Small models vary a lot by language — try
two or three before judging quality in Hindi, Tamil, Swahili, Yoruba, etc.

## Run through an API

```bash
UPSTREAM=https://api.example.com API_KEY=your-key python3 serve.py
```

In Settings choose **OpenAI-compatible API** and set the base URL to
`http://localhost:8099/v1`. The key stays in the server process and never
reaches the browser: the proxy adds `Authorization: Bearer $API_KEY`
server-side and a server key always overrides any client header.

Opening `app/index.html` directly from disk also works (the skills are
embedded into `app/skills.js` by `build.py`), but then the page talks to
the model directly: start Ollama with `OLLAMA_ORIGINS=*` and enter any API
key in the browser (it is stored only in your browser's localStorage).

## What's in the UI

- **General** — all twelve writing modes (Discover, Structure, Scene plan,
  Draft, Dialogue, Describe, Deepen, Tighten, Continuity, Revise, Canon
  update, Profile update) as buttons.
- **Short fiction skill pack** — the same 12 modes tuned for short stories:
  premise ideas, outline, scene contract, draft/continue, dialogue pass,
  describe, deepen, tighten, show-don't-tell, beta reader, canon update,
  profile update.
- **Biography skill pack** — interview questions, timeline, draft from
  notes, fact-check list, consent & risk check; memoir evidence rules are
  always on for this pack.
- **Writer's material** — voice-sample box (matched, never copied), notes
  box (authoritative story bible / source file), manuscript area with text
  selection for the rewrite tools, optional instruction line.
- **Streaming output** with Stop, then Append / Replace selection / Copy.
- **Autosave** in the browser (localStorage); export `.txt`, `.md`, or a
  project `.owos.json`; open a project file again later.
- Dark mode follows the OS. Works on a phone browser and a low-end laptop.

## Grounding rules (biography)

The biography pack writes only from your notes, tags anything unsupported
as `[VERIFY]`, tags invented material `[IMAGINED]`, never invents quotes or
dates, labels evidence with the eight memoir statuses, and runs a consent /
defamation / cultural-sensitivity check on request.

## Short fiction rules

Writer's language and dialect preserved (never "corrected"), local
settings by default, one central pressure, concrete over abstract, word
-count targets respected, ending must be surprising and inevitable.

## Files

```
web/
    serve.py                  local server: static app + model proxy (127.0.0.1 only)
    build.py                  embeds skills/*/SKILL.md into app/skills.js
    app/index.html            single-page UI
    app/core.js               modes, prompt building, streaming parser (Node-testable)
    app/skills.js             generated - do not edit by hand
    skills/short-fiction/SKILL.md
    skills/biography/SKILL.md
    tests/tests.js            Node tests for core.js (offline)
    tests/mock_upstream.py    mock Ollama + mock API for manual testing
    tests/run.sh              runs everything
```

## Tests

```bash
sh web/tests/run.sh        # python3 build.py + node tests + python unittest
```

All offline: the Node suite uses an in-process mock server and the Python
suite (`tests/test_web_serve.py`) starts `serve.py` and a mock upstream on
loopback. Covers prompt building, streaming for both API shapes (streams
split at every byte), unicode text, selection-required tools, budget
clipping, error surfacing, model listing, the proxy, and key handling —
including a direct-to-API test that fails if the client `Authorization`
header is dropped.

## Add a skill

Create `skills/<name>/SKILL.md`, add its buttons to `ACTIONS` in
`app/core.js`, add an `<option>` in `app/index.html`, run
`python3 build.py`.

## Known limits

- Never tested against a real model yet — only mocks. Try 2-3 small models
  with real writers before promising quality in any language.
- The UI logic is tested in Node, not yet by a human in a real browser.
- No translated interface, no PWA install, no EPUB export yet.
