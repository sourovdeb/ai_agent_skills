# v1.0 vs 2.0 — side-by-side comparison

- **v1.0** = `mishu-writer-os.zip` (Google Drive, MIT) — browser app +
  `serve.py` proxy + 2 skill packs, 6 short-fiction tools + 5 biography
  tools, tested only against fake servers.
- **2.0** = this folder, `projects/open-writer-os/` (MIT, repo license) —
  the same local-app architecture, plus a CLI core (`open_writer_os/`
  package) and a web UI (`web/`) exposing **all 12 MISHU writing modes**.

| Aspect | v1.0 (Drive zip) | 2.0 (this repo) |
|---|---|---|
| Form | browser app only | browser app (`web/`) **+** CLI (`python -m open_writer_os`) sharing one engine core |
| Local server | `serve.py`, stdlib, 127.0.0.1:8099, proxies `/api/*`,`/v1/*` | same pattern, plus `/healthz`, testable `make_server()`, server key overrides client header |
| Model access | Ollama or any OpenAI-compatible API; key server-side via proxy | same two backends in one provider layer; CLI reads key from env var only |
| Writing modes | 6 short-fiction + 5 biography actions | all 12 modes (discover → profile-update) in web UI and CLI |
| Skill packs | short-fiction, biography (SKILL.md, also loadable by other agents) | same two packs, enriched: word-count targets, ending discipline, 8 memoir evidence statuses, interview-to-prose flow, privacy rules |
| Story bible / canon | notes box in the page (localStorage) | notes box in web UI **+** on-disk folder canon (STORY_BIBLE.md, CANON_LEDGER.md, CURRENT_STATE.md) via CLI; web app keeps the lightweight notes box |
| Grounding (biography) | notes-only writing, `[VERIFY]` tags, never invent quotes/dates, consent & defamation check | same rules, plus evidence statuses (REMEMBERED…FICTIONALIZED), `[IMAGINED]` tag, attribution |
| Voice | voice-sample box, matched never copied | same in web UI; CLI keeps STYLE_TARGET.md learned from approved prose |
| Dialect / language | preserved, code-mixing allowed; output language field | same, in both web and CLI engines ("answer in the writer's language") |
| Streaming | SSE/NDJSON parser, stop mid-stream | same parser (byte-split tested), plus abort handling |
| Storage | localStorage autosave; export .txt / project .json | same in web UI (.txt/.md/.owos.json) + plain-Markdown project folders on disk; CLI `export` command |
| Tests | ~50 checks vs fake Ollama/fake API (Node), incl. one survived break later fixed with a direct-to-API key test | Node suite for `core.js` (modes, prompt building, byte-split streams, unicode, key-header regression test) + Python suite incl. live loopback proxy tests with mock upstream |
| Real-model testing | none | none — both need 2-3 real small models tried with real writers |
| Human browser testing | none | none yet — automated HTTP checks only |
| License | MIT | MIT (repo LICENSE) |
| Hosting | local only (a hosted page can't reach Ollama); `app/` also works from `file://` with `OLLAMA_ORIGINS=*` | same stance: real project folder, not a published page |

## How to compare them side by side

```bash
# v1.0
unzip mishu-writer-os.zip && cd mishu-writer-os
python3 serve.py                 # http://localhost:8099

# 2.0, in another terminal
cd projects/open-writer-os
python3 web/serve.py             # http://localhost:8099 (use PORT=8098 to run both at once)
# or the CLI: python3 -m open_writer_os run <project> draft --book "My Book" --prompt "..."
```

Run both against the same Ollama model with the same notes/voice sample
and compare: premise ideas, a draft, a tighten pass, and a biography
fact-check.

## What 2.0 adds

1. The full 12-mode engine (scene contracts, canon ledger with fact
   statuses, continuity audit, profile updates) — not just 11 preset
   buttons.
2. A persistent, human-readable project folder (Markdown) the CLI and
   any editor can use — the web app's localStorage is only a scratchpad.
3. One provider layer shared by web and CLI; keys never stored on disk.
4. Loopback proxy tests that prove the server-side key wins over any
   client header, plus a direct-to-API key regression test.

## What v1.0 still does better / not ported yet

- Nothing feature-wise is lost; v1.0's smaller action set is a subset of
  2.0's modes. Deliberately not ported: PWA install, EPUB export, UI
  translations — listed as contributor ideas in both READMEs.
