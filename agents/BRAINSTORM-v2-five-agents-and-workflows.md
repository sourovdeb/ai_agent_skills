# Brainstorm v2 — Five Core Productivity Agents, Email Debrief Routine, Agent-to-Agent Workflow, and Gmail Backup Plan

**Date:** 2026-07-11 · **Status: BRAINSTORM ONLY — no scripts, no IDs yet.**
This document deliberately stops at *design*. Scripts, spreadsheet IDs, folder IDs, and code
come in a later step, once these designs are approved.

Source: `sourovdeb/my_professional_documents agents/BRAINSTORM-v2-five-agents-and-workflows.md`

> ⚠️ **Security note:** A prior workflow document contained plain-text credentials (FTP password,
> deploy key, REST API key). **Rotate them** and store future secrets only in a password manager
> / Apps Script Properties — never in Markdown, Drive docs, or repos. All designs below assume
> secrets-by-reference.

---

## Part 1 — The 5 Core Productivity Agents (generic, intelligent, long-term)

Design constraints:
- **Generic**: zero personal facts in the agent body; everything personal fetched at run time from Cache.
- **Intelligent**: each agent has a *reasoning contract* (what it must think about before acting).
- **Efficient**: consult cache before searching, batch, summarize, dedupe tool calls.
- **Long-term**: platform-agnostic wording so instructions run on Claude Code, Grok, or any future runtime.
- **Health gate inherited**: every agent respects red/yellow/green energy gate.

### Agent A — Chief Synthesizer
Turns everything that happened (mail, documents, deadlines, events) into ONE short debrief with decisions attached. Ranking: Health impact · Irreversibility · Time · Who-is-waiting. Max 3 priorities surfaced.

### Agent B — Signal Scanner
Scans Inbox, Sent, Drafts for signals: deadlines, requests, confirmations, risks, opportunities. Classifies every item into {Action / Wait / Info / Risk / Noise}. Extracts dates, amounts, reference numbers **verbatim**.

### Agent C — Solution Builder
For each admin/legal/medical problem, builds a concrete solution path **using official sources only** (service-public.fr, ameli.fr, urssaf.fr, impots.gouv.fr, francetravail.fr, legifrance). Never guesses a rule.

### Agent D — Executor & Artifact Maker
Turns decisions into artifacts — drafts, letters, CSV rows, calendar entries — ready for one-click human approval. Applies compliance gate (blocked-phrases / required-disclosures pre-flight). **Never sends anything itself.**

### Agent E — Memory & Continuity Keeper
Keeps the brain file current, versioned, and **multi-homed** (Drive + GitHub mirrors). Verifies backups actually restored. Quarterly "restore drill" report.

**Mapping to 10-agent fleet:** A≈01+09, B≈04+05, C≈06+official-source discipline, D≈06/07/08 execution layer, E≈10 extended with continuity.

---

## Part 2 — The Email Debrief Routine

**Cadence:** daily (evening) + lightweight midday delta.

**Steps:**
1. Read last-run timestamp. Scan only newer items.
2. Scan three views: Inbox (new/unread), **Sent** (questions with no reply >N days), **Drafts** (stale >N days).
3. Classify each thread: Action / Wait / Info / Risk / Noise; tag domain.
4. Extract verbatim: dates, deadlines, amounts, reference numbers, who is waiting.
5. Solve: for each Action/Risk item, attach a mini solution card (official sources only).
6. Write debrief (≤ 1 screen): Top 3 actions → things waiting → risks → FYI. One line each.
7. Update tracker (CSV/spreadsheet): one row per open item; update status; never duplicate.
8. Create artifacts where obvious (reply drafts, calendar entries) — draft-only, never send.
9. Save checkpoint + append a one-line run log.

**Tracker schema:**
`ID · Date_Detected · Domain · Source · What_It_Is · Advice · Steps · Deadline · Owner · Status · Result · Next_Check_Date · Health_Impact · Irreversible · Notes`

---

## Part 3 — Agent-to-Agent + Drive Workflow

```
[Schedule / new-mail event]
   → B Signal Scanner  (Gmail: Inbox+Sent+Drafts; incremental)
   → (attachments/docs found) → Drive intake
   → C Solution Builder (official sources; solution cards)
   → D Executor (drafts, CSV rows, calendar entries — approval-gated)
   → A Chief Synthesizer (debrief to human; Top-3)
   → E Memory Keeper (cache update, backups, checkpoint)
```

**Design rules:**
- Hand-offs are files, not chat. Each agent writes output to a known Drive/repo path.
- One shared state file (tracker + checkpoint) prevents double-processing.
- Pre-made Gmail scripts join the chain as *data producers only* — they keep their compliance gates.
- Health gate wraps the chain: red flag → only steps 1–2 + a one-line debrief.

---

## Part 4 — Gmail Backup Plan (continuity kit)

**Layer 0 — Prevention:** 2FA with two methods; recovery email + phone kept current.

**Layer 1 — Continuous data escape:** Google Takeout on recurring schedule. Cache index, tracker CSV, agent instructions: Drive + GitHub + one offline copy.

**Layer 2 — Standby identity:** Second mailbox at independent provider (Proton Mail recommended). Optional custom-domain address that survives provider changes.

**Layer 3 — Failover runbook:**
1. Switch to standby mailbox (already has forwarded history).
2. From tracker (multi-homed), notify agencies via their official in-portal contact settings.
3. Agents repoint: only the email system connector changes.
4. Attempt Google recovery in parallel.

**Layer 4 — Drill:** Quarterly 15-minute restore test by Agent E.

---

## Part 5 — Decision list

1. Approve the 5-agent core as the operating layer over the existing 10.
2. Approve the tracker schema — then create the actual spreadsheet.
3. Approve the chain + file-hand-off rule.
4. Choose standby provider and custom-domain strategy.
5. Rotate the exposed credentials.
6. In order: create tracker → write `email-debrief` instruction → wire Drive folders → dry-run → enable artifact creation.
