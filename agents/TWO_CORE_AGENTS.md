# Two Core Agents — Consolidated System (v1.0, 2026-07-13)

Source: `sourovdeb/my_professional_documents agents/TWO_CORE_AGENTS.md`

Distilled from the earlier 1-orchestrator + 9-specialist design into the **2 most important
agents**, built for long-term use. Health stability is the non-negotiable gate for both.

| # | Agent | Folder | Hard-coding | Role |
|---|-------|--------|-------------|------|
| 1 | **Life & Health Orchestrator** | `01_life_health_orchestrator/` | **None** — all specifics in `registry.yaml` | One agent for many areas: text/docs, health, doctor appointments, any administrative body. Scans email/Drive/Box + documents, analyses, reminds, and creates drafts/letters/reminders/tracker rows. Owns the Health Gate. |
| 2 | **Professional & Administrative** | `02_professional_admin_agent/` | **Permitted** (the only one) | French auto-entrepreneur admin: URSSAF, DGFiP/impôts, CGSS Réunion, France Travail, BNC regime, SIRET, DSN, PAS, facturation électronique. Defers to Agent 1's Health Gate + shared tracker. |

## Design principles

- **Health first, always.** Neither agent proposes work that risks stability.
- **No hard-coding except Agent 2.** Agent 1 references registry keys, never literal names/agencies/dates.
- **Long-lived.** Change the `registry.yaml`, not the prompts.
- **Evidence-based.** Every admin/legal/medical/deadline claim verified against the authority's official URL.

## Files structure

```
agents/
├── TWO_CORE_AGENTS.md                          ← this file
├── 01_life_health_orchestrator/
│   ├── AGENT.md
│   ├── PROMPT.md
│   └── registry.example.yaml
├── 02_professional_admin_agent/
│   ├── AGENT.md
│   └── PROMPT.md
└── trackers/
    └── two_core_agents_tracker.csv
```

## Storage / sync

- **GitHub:** `sourovdeb/my_professional_documents` (origin).
- **Google Drive:** CSV mirrored to obligations folder.
- **Box:** CSV + agent files backed up.

## Migration note

The previous 10-agent specs remain in their sub-folders for reference. Going forward, the
**two core agents above are the system**: Agent 1 handles everything general (owns the Health Gate
+ tracker); Agent 2 handles the professional/French-admin specialism.
