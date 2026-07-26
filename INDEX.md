# AI Agent Skills Repository

A comprehensive collection of AI skills, agents, guides, and tools created by Claude Code routines.

**Last Organised**: 2026-07-26 | **Total Files**: 205 | **Branch**: `claude/jolly-fermi-gkbw49`

---

## Quick Navigation

| Folder | Files | Purpose |
|--------|-------|---------|
| [skills/](skills/) | 114 | Skill definitions (SKILL.md + evals + instructions + prompts) |
| [agents/](agents/) | 29 | AI agent instruction sets and automation configs |
| [guides/](guides/) | 8 | Tutorials, best practices, configuration guides |
| [tools/](tools/) | 17 | Python scripts, shell scripts, utilities |
| [evaluation/](evaluation/) | 5 | Testing, audit reports, validation frameworks |
| [templates/](templates/) | 3 | Frameworks for creating new skills and artifacts |
| [config/](config/) | 5 | JSON schemas, manifests, reference docs |
| [prompts/](prompts/) | 7 | Structured prompts (instructions + prompt.json pairs) |
| [projects/](projects/) | 4 | Website redesign and project assets |
| [docs/](docs/) | 5 | Reports, archives, trackers, old index |
| [tests/](tests/) | 1 | Unit tests for repo utilities |

---

## Skills (114 files across 41 skill packages)

Structured as `skills/<name>/SKILL.md` with optional `evals/`, `references/`, `.instructions.md`, `.prompt.json`.

| Skill Package | Has Evals | Has Instructions |
|---------------|-----------|------------------|
| alzheimers-adhd-daily-support | ✅ | — |
| api-reference | — | — |
| biography-interview-kit-private-master | ✅ | — |
| biography-interview-kit-public | ✅ | — |
| biography-memoir-system | ✅ | — |
| brainstorming-matrix | — | — |
| cambridge-writer | ✅ | ✅ |
| content-research-writer | — | — |
| data-analysis | — | ✅ |
| deep-brainstorm | — | ✅ |
| defense-in-depth-hardening | — | — |
| dual-biography-interview-skill-v2 | ✅ | — |
| empathetic-listening | ✅ | — |
| empathic-listening-psychology | ✅ | ✅ |
| epub-pdf-analyzer | — | — |
| family-memory-deep-probe-reliability | ✅ | — |
| ffuf-security-fuzzer | — | — |
| finishing-dev-branch | — | — |
| health-information-advisor | ✅ | — |
| investigative-psychology | — | — |
| investigative-research | — | ✅ |
| invoice-file-organizer | — | — |
| job-search-agent | — | ✅ |
| legal-analysis-compliance | ✅ | ✅ |
| legacy/SKILL_celta_lesson_teacher_v1 | — | — |
| legacy/SKILL_elt_elicitor_v1 | — | — |
| legacy/SKILL_elt_essay_teacher_v1 | — | — |
| life-history-elicitation | — | ✅ |
| medical-information-advisor | ✅ | ✅ |
| memory-elicitation-interview-skill | ✅ | — |
| objective-first | — | ✅ |
| pragmatic-productivity | ✅ | ✅ |
| prompt-architect | — | — |
| psychology-agent | — | ✅ |
| pypict-combinatorial-qa | — | — |
| self-debate | — | ✅ |
| self-hosting-infra-advisor | — | — |
| skill-creator | — | — |
| skill-seekers | — | — |
| structured-interviewer | ✅ | ✅ |
| superpowers | — | — |
| superpowers-lab | — | — |
| system-design | — | — |
| systematic-debugging | — | — |
| tapestry-knowledge-graphs | — | — |
| test-driven-development | — | — |
| universal-upgrade | — | ✅ |
| using-git-worktrees | — | — |
| web-asset-generator | — | — |
| webapp-testing-playwright | — | — |
| writer-agent | — | ✅ |
| youtube-article-extractor | — | — |

---

## Agents (29 files)

### Fleet: Holistic Stability & Productivity

| Agent | Purpose |
|-------|---------|
| 01-holistic-life-orchestrator.md | Chief-of-staff orchestrator: all domains |
| 02-health-stability-guardian.md | Health & stability veto agent |
| 03-appointment-deadline-sentinel.md | Deadlines and reminders with lead-time alerts |
| 04-document-intake-analyst.md | PDF/letter ingestion and routing |
| 05-inbox-triage-agent.md | Gmail triage and daily digest |
| 06-admin-correspondence-drafter.md | FR/EN formal letters — never auto-sends |
| 07-income-opportunity-scout.md | Job and tutoring opportunity search |
| 08-content-publishing-agent.md | WordPress draft and publish |
| 09-weekly-planner-prioritizer.md | Health-first weekly plan |
| 10-knowledge-cache-curator.md | Central knowledge registry — load first |
| BRAINSTORM-v2-five-agents-and-workflows.md | 5-agent core design + workflow chains |
| TWO_CORE_AGENTS.md | Consolidated two-core system v1.0 |

### Specialist Agents

| Agent | Purpose |
|-------|---------|
| AI_Agent_Core_Instructions.md | Core Claude Code agent instructions |
| Biography_Memoir_Writer_Agent.md | Biography and memoir writing automation |
| Critical_Analysis_PostHoc_Agent.md | Post-hoc critical analysis |
| Daily_Living_Productivity_Agent.md | Daily productivity support |
| ELT365_Micro_Course_Publisher_Agent.md | ELT micro-course publication |
| ELT_Teaching_Master_Agent.md | Master ELT teaching agent |
| Job_Application_Career_Agent.md | Job application automation |
| Legal_Regulatory_Dossier_Agent.md | Legal and regulatory research |
| Long_Task_Memory_Protocol.md | Memory management for long tasks |
| Post-hoc Analyzer Agent.md | Output evaluation and analysis |
| Self_Challenge_Devils_Advocate_Agent.md | Devil's advocate reasoning |
| Skilled_Biography_Interviewer_Agent.md | Biography interview specialist |
| Wiki_Knowledge_Management_Agent.md | Knowledge base management |
| arch-usb-agent-instructions.md | Arch Linux USB setup automation |
| email-agent.md | Email automation and drafting |
| Compare two outputs...AGENT.md | Blind comparison evaluator |
| holistic_stability_orchestrator_refined_prompt_v1.md | 10-agent health-first productivity orchestrator |

---

## Getting Started

**Beginners**: → [guides/](guides/) → [skills/](skills/)

**Developers**: → [templates/](templates/) → [tools/](tools/) → [evaluation/](evaluation/)

**Integration**: → [agents/](agents/) → [config/](config/) → [prompts/](prompts/)

---

## Tracker

Full file inventory CSV: [`docs/trackers/AI_Agent_Skills_Organization_2026-07-26.csv`](docs/trackers/AI_Agent_Skills_Organization_2026-07-26.csv)

Agents fleet catalog: [`docs/trackers/agents-catalog.csv`](docs/trackers/agents-catalog.csv)

Also saved to: Google Drive & Box (`free_education - AI Skills Trends` folder)

---

## Contributing

1. Place new content in the correct folder
2. For skills: create `skills/<your-skill-name>/SKILL.md`
3. For agents: add to `agents/`
4. For guides: add to `guides/`
5. Update this INDEX on significant additions
6. Commit to branch `claude/jolly-fermi-gkbw49`

---

See [ORGANIZATION.md](ORGANIZATION.md) for full folder structure reference.
