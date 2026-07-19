---
title: AI Agent Rules Index
date: 2026-05-15
tags: [index, ai-rules, skills, navigation]
---

# _AI_AGENT_RULES Index

Navigation hub for all skill definitions and eval infrastructure.

## Skills (Agent Capabilities)

| Skill | Description | Links |
|-------|-------------|-------|
| [[Post-hoc Analyzer Agent]] | Evaluates skill outputs against expectations | [[Skill Creator]], [[Compare two outputs WITHOUT knowing which skill produced them_AGENT]] |
| [[Skill Creator]] | Creates and packages new agent skills | [[Post-hoc Analyzer Agent]], [[Grader]], [[Comparator]] |
| [[email-agent]] | Email automation and drafting agent | [[nxtpaper-mode-arch-kde-deep-guide]] |
| [[nxtpaper-mode-arch-kde-deep-guide]] | NXTPaper display mode configuration | [[email-agent]] |
| [[doc-coauthoring]] | Collaborative document writing | — |
| [[JSON Schemas]] | Validation schemas for agent outputs | — |

## Domain Skills — Productivity / Legal / Medical / Psychology / Interviewer / Writer

| Skill | Description | Links |
|-------|-------------|-------|
| `agents/Daily_Living_Productivity_Agent` | State-based daily productivity routing (GTD-grounded capture/clarify/organize, anchors, closing ritual) | `skills/alzheimers-adhd-daily-support` |
| `agents/Legal_Regulatory_Dossier_Agent` | Harvard-associate-rigor legal/regulatory dossiers (CREAC, jurisdiction matrices, Bluebook signal discipline) | — |
| `skills/health-information-advisor` | Careful health information and patient-education advisor with red-flag triage | `skills/health-information-advisor/references/red-flag-triage.md` |
| `skills/empathetic-listening` | Rogerian/motivational-interviewing-grounded reflective listening, with crisis escalation | `skills/alzheimers-adhd-daily-support` |
| `skills/alzheimers-adhd-daily-support` | Alzheimer's/dementia caregiver technique and ADHD executive-function support | `agents/Daily_Living_Productivity_Agent`, `skills/family-memory-deep-probe-reliability` |
| `skills/biography-memoir-system` | Orchestrator for the biography/memoir skill family | See variants below |
| `skills/biography-interview-kit-private-master` | Complete unfiltered private archive interview | `skills/biography-memoir-system` |
| `skills/biography-interview-kit-public` | Publication-ready interview from the start | `skills/biography-memoir-system` |
| `skills/dual-biography-interview-skill-v2` | One session, private archive + publishable draft | `skills/biography-memoir-system` |
| `skills/memory-elicitation-interview-skill` | Single-memory/tight-topic interview | `skills/biography-memoir-system` |
| `skills/family-memory-deep-probe-reliability` | Elderly/memory-impaired narrators, reliability-coded conflicting accounts | `skills/alzheimers-adhd-daily-support` |
| `agents/Skilled_Biography_Interviewer_Agent` | Interviewer persona + non-compromisable rules, routes to the family above | See above |
| `agents/Biography_Memoir_Writer_Agent` | Cambridge-level memoir prose writer, works from tagged interview material | `skills/content-research-writer` |
| `skills/pragmatic-productivity` | Practical non-generic productivity workflows (capture-triage, weekly review, calendar defense) | `agents/Daily_Living_Productivity_Agent` |
| `skills/legal-analysis-compliance` | IRAC-plus analysis, jurisdiction-first rule, UPL boundary | `agents/Legal_Regulatory_Dossier_Agent`, `prompts/legal-agent` |
| `skills/medical-information-advisor` | Trio-format health advisor: red-flag triage, evidence grading, appointment prep | `skills/health-information-advisor` |
| `skills/empathic-listening-psychology` | Enforced listening-first protocol (no advice in first response, OARS, crisis escalation) | `skills/empathetic-listening`, `skills/psychology-agent` |
| `skills/structured-interviewer` | Structured-interview design, BARS scorecards, bias-controlled evaluation | `agents/Job_Application_Career_Agent` |
| `skills/cambridge-writer` | Argument-first prose at a demanding academic standard | `skills/writer-agent` |
| `agents/Care_Support_Companion_Agent` | Orchestrator routing mixed health/emotional/cognitive-support conversations, safety-first order | `skills/alzheimers-adhd-daily-support`, `skills/medical-information-advisor` |
| `agents/Job_Application_Career_Agent` | Router card to the job-search-agent skill + interview/writing/productivity chain | `skills/job-search-agent` |

## Meta & Decision Skills (added July 2026)

| Skill | Description | Links |
|-------|-------------|-------|
| `skills/decision-battery-antifragile` | 42-step antifragile decision OS with SCAMPER core, black-swan module, energy gates | `skills/decision-battery-antifragile/AGENT.md` |
| `skills/theme-factory` | Ten professional visual themes (palettes + typography) for artifacts and documents | `skills/theme-factory/references/theme-details.md` |
| `config/skills_manifest.json` | Machine-readable registry of all skills and agents (v1.1, 2026-07-19) | — |

## Eval Infrastructure

| Tool | Purpose |
|------|---------|
| [[aggregate_benchmark]] | Benchmark aggregation script |
| [[Compare two outputs WITHOUT knowing which skill produced them_AGENT]] | Blind comparator |
| [[Evaluate expectations against an execution transcript and outputs]] | Transcript evaluator |
| [[generate_report]] | Report generation |
| [[generate_review]] | Review generation |
| [[improve_description]] | Description improvement utility |
| [[package_skill]] | Skill packaging tool |
| [[quick_validate]] | Quick validation runner |
| [[run_eval]] | Evaluation runner |
| [[run_loop]] | Loop-based eval runner |
| [[update]] | Update utility |
| [[utils]] | Shared utilities |

## All Rule Files

- [[aggregate_benchmark.py]] — aggregate_benchmark.py.md
- [[Compare two outputs WITHOUT knowing which skill produced them_AGENT]] — Blind Comparator Agent
- [[doc-coauthoring.MD]] — Doc Co-Authoring Workflow
- [[email-agent]] — email-agent.md
- [[Eval Review - Review each output and leave feedback below. Navigate with arrow keys or buttons. When done, copy feedback and paste into AGENT]] — Eval Review - Review each output and leave feedback below. Navigate with arrow keys or buttons. When done, copy feedback and paste into AGENT.md
- [[Evaluate expectations against an execution transcript and outputs.MD]] — Evaluate expectations against an execution transcript and outputs.MD.md
- [[generate_report.py]] — generate_report.py.md
- [[generate_review.py]] — Files to exclude from output listings
- [[improve_description.py]] — Supported AI agent binaries in preference order
- [[JSON Schemas.MD]] — JSON Schemas
- [[nxtpaper-mode-arch-kde-deep-guide]] — NXTPaper Mode on Arch Linux + KDE Plasma
- [[package_skill.py]] — Patterns to exclude when packaging skills.
- [[Post-hoc Analyzer Agent]] — Post-hoc Analyzer Agent
- [[quick_validate.py]] — quick_validate.py.md
- [[run_eval.py]] — run_eval.py.md
- [[run_loop.py]] — run_loop.py.md
- [[Skill Creator]] — Skill Creator
- [[update.MD]] — update.MD.md
- [[utils.py]] — utils.py.md

---
*Back to [[INDEX]] · [[_small_ai_agent/_INDEX]]*
