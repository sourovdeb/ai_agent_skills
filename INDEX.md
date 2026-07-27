# AI Agent Skills Repository

A comprehensive collection of AI skills, agents, guides, and tools created by Claude Code routines.

**Last Organised**: 2026-07-27 | **Total Files**: 217 | **Branch**: `claude/jolly-fermi-gkbw49`

---

## Quick Navigation

| Folder | Files | Purpose |
|--------|-------|----------|
| [skills/](skills/) | 114 | Skill definitions (SKILL.md + evals + instructions + prompts) |
| [agents/](agents/) | 34 | AI agent instruction sets and automation configs |
| [guides/](guides/) | 8 | Tutorials, best practices, configuration guides |
| [tools/](tools/) | 18 | Python scripts, shell scripts, utilities |
| [evaluation/](evaluation/) | 5 | Testing, audit reports, validation frameworks |
| [templates/](templates/) | 3 | Frameworks for creating new skills and artifacts |
| [config/](config/) | 5 | JSON schemas, manifests, reference docs |
| [prompts/](prompts/) | 7 | Structured prompts (instructions + prompt.json pairs) |
| [projects/](projects/) | 10 | Project assets (website redesign, WP extension, Bengali Radio) |
| [docs/](docs/) | 6 | Reports, archives, trackers, old index |
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

## Agents (34 files)

### Fleet: Holistic Stability & Productivity

| Agent | Purpose |
|-------|----------|
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

### v2 Architecture (Redesigned System)

Upgraded from v1.0. Wellbeing gatekeeper broadened; France Travail merged into Legal Sentinel; Deep Brainstorm (#6) and Tutoring Designer (#9) added; deadlines moved to tracker CSV.

| File | Purpose |
|------|----------|
| v2/README.md | v2 system overview and v1→v2 change table |
| v2/00_orchestrator_spec.yaml | Agent 0 full YAML spec — intake→extract→verify→health-gate→route→act→report |
| v2/01-09_specialized_agents.md | Agents 1–9 summary specs (YAML blocks) |
| v2/master_tracker_v2.csv | Single source of truth for deadlines and obligations |

### Specialist Agents

| Agent | Purpose |
|-------|----------|
| AI_Agent_Core_Instructions.md | Core Claude Code agent instructions and protocols |
| Biography_Memoir_Writer_Agent.md | Biography and memoir writing automation |
| Critical_Analysis_PostHoc_Agent.md | Post-hoc critical analysis |
| Daily_Living_Productivity_Agent.md | Daily productivity and living support |
| ELT365_Micro_Course_Publisher_Agent.md | ELT micro-course publication |
| ELT_Teaching_Master_Agent.md | Master ELT teaching agent for lesson planning and delivery |
| Job_Application_Career_Agent.md | Job application and career advancement automation |
| Legal_Regulatory_Dossier_Agent.md | Legal and regulatory research and dossier building |
| Long_Task_Memory_Protocol.md | Memory management protocol for long multi-session tasks |
| Post-hoc Analyzer Agent.md | Output evaluation and analysis against expectations |
| Self_Challenge_Devils_Advocate_Agent.md | Devil's advocate reasoning |
| Skilled_Biography_Interviewer_Agent.md | Biography interview specialist with elicitation techniques |
| Wiki_Knowledge_Management_Agent.md | Knowledge base and wiki management automation |
| arch-usb-agent-instructions.md | Arch Linux USB setup automation |
| email-agent.md | Email automation and drafting |
| Compare two outputs...AGENT.md | Blind comparison evaluator |
| holistic_stability_orchestrator_refined_prompt_v1.md | 10-agent health-first productivity orchestrator |

---

## Projects (10 files)

### website-redesign & wordpress-control

| File | Purpose |
|------|----------|
| projects/website-redesign/ | Website redesign assets and documentation |
| projects/wordpress-control/README.md | WP AI Studio VS Code extension documentation |
| projects/wordpress-control/package.json | WP AI Studio VS Code extension manifest (no credentials) |

### bengali-radio (2026-07-27)

Community radio platform research and planning for West Bengal Bengali-language content.

| File | Purpose |
|------|----------|
| projects/bengali-radio/execution-plan.md | 4-phase plan: validation → pilot → scale → sustainability |
| projects/bengali-radio/ideas.md | 5 brainstormed ideas ranked by impact/feasibility |
| projects/bengali-radio/research-methodology.md | Investigative research framework for MIB licensing |
| projects/bengali-radio/upgrades.md | Gap analysis: AI transcription + solar power + emergency alerts |

### wordpress-control/audits (2026-07-27)

| File | Purpose |
|------|----------|
| projects/wordpress-control/audits/INDEXED_MESSAGE_AND_SECURITY_CONTEXT.md | Redacted security context index (INC2671905) |
| projects/wordpress-control/audits/PUBLIC_AUDIT_REPORT_sourovdeb_com_2026-07-11.md | Public audit — plugins/pages/posts (Hostinger token redacted) |

---

## Getting Started

**Beginners**: → [guides/](guides/) → [skills/](skills/)

**Developers**: → [templates/](templates/) → [tools/](tools/) → [evaluation/](evaluation/)

**Integration**: → [agents/](agents/) → [config/](config/) → [prompts/](prompts/)

---

## Tracker

Full file inventory CSV: [`docs/trackers/AI_Agent_Skills_Organization_2026-07-27.csv`](docs/trackers/AI_Agent_Skills_Organization_2026-07-27.csv)

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
