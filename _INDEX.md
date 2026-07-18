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
| `agents/Cognitive_Support_Companion_Agent` | Listens-first routing persona for dementia-caregiver and ADHD executive-function conversations (new 2026-07-18) | `skills/empathetic-listening`, `skills/alzheimers-adhd-daily-support`, `skills/health-information-advisor` |

## Developer, Design & Meta Skills (registered in manifest 2026-07-18)

| Skill | Description |
|-------|-------------|
| `skills/decision-battery-antifragile` | 42-step antifragile decision OS with SCAMPER, black-swan module, ND energy gates (+ standalone AGENT.md) |
| `skills/theme-factory` | 10 professional color/font themes for decks, documents, reports, HTML |
| `skills/prompt-architect` | Rebuilds raw questions into precise, testable prompts |
| `skills/brainstorming-matrix` | Rough ideas → structured system-architecture designs |
| `skills/superpowers` / `skills/superpowers-lab` | Coordinator skill for brainstorm/debug/TDD/planning; lab = experimental features |
| `skills/skill-seekers` | Generates a skill from docs, APIs, codebases, or PDFs |
| `skills/tapestry-knowledge-graphs` | Document dumps → navigable knowledge graphs/wiki |
| `skills/defense-in-depth-hardening` | Multi-layered security assessment and hardening |
| `skills/ffuf-security-fuzzer` | Web-app fuzzing for authorized security testing |
| `skills/epub-pdf-analyzer` | Structural parsing and semantic querying of ebooks/whitepapers |
| `skills/youtube-article-extractor` | Transcript and article extraction/summarization |
| `skills/finishing-dev-branch` | Branch-merge staging workflow automation |
| `skills/systematic-debugging` | Root-cause-first debugging discipline |
| `skills/test-driven-development` | Strict TDD enforcement |
| `skills/using-git-worktrees` | Multi-branch work via Git worktrees |
| `skills/pypict-combinatorial-qa` | Pairwise/combinatorial test-matrix generation |
| `skills/webapp-testing-playwright` | End-to-end browser UI test automation |
| `skills/web-asset-generator` | App icons, Open Graph tags, PWA manifests |

Full machine-readable registry: `config/skills_manifest.json` (v1.1, 2026-07-18).

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
