# AI Agent Skills Repository

A comprehensive collection of AI skills, agents, guides, and tools created by Claude Code routines.

**Last Organised**: 2026-08-01 | **Total Files**: 271 | **Branch**: `claude/jolly-fermi-gkbw49`

---

## Quick Navigation

| Folder | Files | Purpose |
|--------|-------|----------|
| [skills/](skills/) | 119 | Skill definitions (SKILL.md + evals + instructions + prompts) |
| [agents/](agents/) | 34 | AI agent instruction sets and automation configs |
| [guides/](guides/) | 20 | Tutorials, best practices, configuration guides |
| [tools/](tools/) | 34 | Python scripts, shell scripts, JS utilities |
| [evaluation/](evaluation/) | 5 | Testing, audit reports, validation frameworks |
| [templates/](templates/) | 4 | Frameworks for creating new skills and artifacts |
| [config/](config/) | 5 | JSON schemas, manifests, reference docs |
| [prompts/](prompts/) | 7 | Structured prompts (instructions + prompt.json pairs) |
| [projects/](projects/) | 34 | Project assets (website redesign, WP extension, Bengali Radio, free-education, ai-term-lessons, site-monetization) |
| [docs/](docs/) | 8 | Reports, archives, trackers, old index |
| [tests/](tests/) | 1 | Unit tests for repo utilities |

---

## Skills (119 files across 46 skill packages)

Structured as `skills/<name>/SKILL.md` with optional `evals/`, `references/`, `.instructions.md`, `.prompt.json`.

| Skill Package | Has Evals | Has Instructions |
|---------------|-----------|------------------|
| alzheimers-adhd-daily-support | ✅ | — |
| api-reference | — | — |
| biography-interview-kit-private-master | ✅ | — |
| biography-interview-kit-public | ✅ | — |
| biography-memoir-system | ✅ | — |
| brainstorming-matrix | — | — |
| branded-cv-letter-design | — | — |
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
| gmail-bulk-draft-automation | — | — |
| google-apps-script-job-automation | — | — |
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
| neurodiversity-disclosure-documentation | — | — |
| objective-first | — | ✅ |
| pragmatic-productivity | ✅ | ✅ |
| prompt-architect | — | — |
| psychology-agent | — | ✅ |
| pypict-combinatorial-qa | — | — |
| regulatory-case-analysis-education | — | — |
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
| ELT_Teaching_Master_Agent.md | Master ELT teaching agent |
| Job_Application_Career_Agent.md | Job application and career advancement |
| Legal_Regulatory_Dossier_Agent.md | Legal and regulatory research |
| Long_Task_Memory_Protocol.md | Memory management for long multi-session tasks |
| Post-hoc Analyzer Agent.md | Output evaluation against expectations |
| Self_Challenge_Devils_Advocate_Agent.md | Devil's advocate reasoning |
| Skilled_Biography_Interviewer_Agent.md | Biography interview specialist |
| Wiki_Knowledge_Management_Agent.md | Knowledge base and wiki management |
| arch-usb-agent-instructions.md | Arch Linux USB setup automation |
| email-agent.md | Email automation and drafting |
| Compare two outputs...AGENT.md | Blind comparison evaluator |
| holistic_stability_orchestrator_refined_prompt_v1.md | 10-agent health-first orchestrator |

---

## Guides (20 files)

| Guide | Purpose |
|-------|----------|
| 01_MASTER_AUTOMATION_GUIDE.md | WordPress automation system: folder watcher, GitHub Actions, job hunting |
| 02_DEEPSEEK_API_GUIDE.md | DeepSeek API vs OpenAI cost comparison + Python/GAS integration |
| 03_CSV_GOOGLE_SHEETS_TUTORIAL.md | CSV + Google Apps Script tutorial with publishFromSheet() script |
| 04_FREE_AI_TOOLS_GUIDE.md | Comprehensive guide to free AI tools |
| 05_OPEN_SOURCE_TOOLS_COLLECTION.md | WP-CLI, n8n, Huginn, writing tools, job search automation |
| 06_AUDIO_VIDEO_BANNER_TOOLS.md | Canva, GIMP/Pillow banners, ElevenLabs, Whisper, OBS, DaVinci |
| 07_WORDPRESS_CATEGORY_TAG_FIX.md | Python WP REST API category/tag fixes via Application Passwords |
| 08_HEALTH_PRODUCTIVITY_TOOLS.md | eMoods, Daylio, Focusmate, no-zero-days system, neurodivergent writing |
| 09_AUTOMATION_TOOLS.md | Free and open source automation tools: job scraping, email, content, SEO, social, cron, analytics |
| 10_WORDPRESS_SEO_GUIDE.md | WordPress SEO guide with pre/post-publish checklists, keyword strategy, backlinks, timeline |
| 11_AI_LANGUAGE_TEACHING_MODES.md | Three operational modes (Teacher/Linguist/Learner) for consistent AI-assisted ELT |
| GITHUB_SETUP_GUIDE_STEP_BY_STEP.md | Step-by-step git setup for beginners |
| GOOGLE_DRIVE_SETUP_GUIDE_STEP_BY_STEP.md | Google Drive folder structure and sharing setup |
| Always use supporting extensions... | Extensions, local software, cache clearing, efficiency |
| always study and create scripts... | Automation scripts for large tasks |
| always take advantage of copilot... | VS Code Copilot, local LMs, official docs |
| doc-coauthoring.MD.md | Document co-authoring methodology |
| nxtpaper-mode-arch-kde-deep-guide.md | NXTPaper mode on Arch Linux with KDE |
| open automatically browser... | Live browser research guidance |
| wordpress-content-sync.md | WordPress hourly content sync (credential redacted — INC2671905) |

---

## Tools (34 files)

### WordPress Publishing

| Tool | Purpose |
|------|----------|
| auto_publisher.py | Cron-based markdown→WP draft auto-publisher (env vars) |
| folder_watcher.js | Node.js chokidar watcher: drop .md → WP draft (env vars) |
| sheet_publisher.gs | Google Apps Script batch publisher from Sheets (PropertiesService) |
| wp_publisher_gui.py | Tkinter desktop GUI for WP publishing (env vars) |
| WP_PUBLISH_HELPER.py | Validates metadata, generates excerpts, publishing checklist |
| wp_publisher.py | WordPress publisher with SEO via deploy.php gateway (WP_DEPLOY_KEY env var — INC2671905) |
| multiplatform_publisher.py | Multi-platform publisher: WordPress, Dev.to, Box, IndexNow — all credentials via env vars (INC2671905) |
| sync_prep.py | Content manifest scanner: categorizes markdown for multi-platform sync, no credentials |
| sync_verification.py | Content sync verification and deduplication hourly runner (WP_PLUGIN_KEY env var — INC2671905) |

### Dev.to & Email

| Tool | Purpose |
|------|----------|
| devto_publisher.py | Dev.to publisher: scans repos for AI content, posts as drafts (DEVTO_API_KEY env var) |
| SMART_EMAIL_COMPOSER_v1.gs | Google Apps Script personalised outreach: 5 sector templates, placeholder file IDs |

### Job Search

| Tool | Purpose |
|------|----------|
| job_search.py | ELT/TEFL job search via Indeed RSS + daily email digest |
| indeed_scraper.py | Indeed scraper via BeautifulSoup → job_leads/indeed_leads.json |
| contact_finder.py | GitHub API search for writers/collaborators + outreach templates |
| INDEED_SEARCH_AUTOMATION.sh | Bash job search report generator with Indeed URLs |
| run_daily.sh | Daily runner: scrapers, essay count, git status |
| unzip_and_push_my_professional_documents.sh | Bash archive extractor + git push: ZIP/TAR/GZ/7Z/RAR |

### AI Skill Utilities (from skill packages)

| Tool | Purpose |
|------|----------|
| aggregate_benchmark.py | Benchmark aggregation |
| bundle-artifact.sh | Artifact bundling |
| frame_cmposer.py | Frame composition |
| generate_report.py | Report generation |
| generate_review.py | Review generation |
| gif-builder.py | GIF building and animation |
| gif_easing.py | GIF easing effects |
| improve_description.py | Description optimization |
| init-artifact.sh | Artifact initialization |
| package_skill.py | Skill packaging |
| quick_validate.py | Quick validation |
| requirements.txt | Python dependencies |
| run_eval.py | Evaluation runner |
| run_loop.py | Agent loop runner |
| utils.py | Shared utilities |
| validators.py | Input/output validation |

---

## Templates (4 files)

| Template | Purpose |
|----------|----------|
| Skill Creator.md | Comprehensive framework for creating new skills (33KB) |
| Web Artifacts Builder.MD.md | Template for building web artifacts and HTML pages |
| research-template.md | Investigative research template: claim identification, source hierarchy, COI checklist, balance check |

---

## Projects (34 files)

### website-redesign & wordpress-control

| File | Purpose |
|------|----------|
| projects/website-redesign/ | Website redesign assets |
| projects/wordpress-control/README.md | WP AI Studio VS Code extension documentation |
| projects/wordpress-control/package.json | Extension manifest (no credentials) |
| projects/wordpress-control/CONTENT_SYNC_README.md | Content sync README (WP REST key redacted — INC2671905) |
| projects/wordpress-control/extension.js | Extension backend: WP REST + AI providers (credentials via VS Code config) |
| projects/wordpress-control/webview.js | Webview panel: 5 tabs Chat/Generate/Posts/Logs/Settings |
| projects/wordpress-control/audits/INDEXED_MESSAGE_AND_SECURITY_CONTEXT.md | Redacted security context index |
| projects/wordpress-control/audits/PUBLIC_AUDIT_REPORT_sourovdeb_com_2026-07-11.md | Public audit (Hostinger token redacted) |

### bengali-radio (2026-07-27)

| File | Purpose |
|------|----------|
| projects/bengali-radio/execution-plan.md | 4-phase plan: validation → pilot → scale → sustainability |
| projects/bengali-radio/ideas.md | 5 ideas ranked by impact/feasibility |
| projects/bengali-radio/research-methodology.md | MIB licensing research framework |
| projects/bengali-radio/upgrades.md | AI transcription + solar + emergency alerts gap analysis |

### free-education (2026-07-27)

| File | Purpose |
|------|----------|
| projects/free-education/2026-07-18-durable-skills-vs-ai/README.md | AI durable skills article: PwC 62% wage premium, AI×Judgment Stack |
| projects/free-education/2026-07-18-durable-skills-vs-ai/mindmap.mm | FreeMind/Freeplane mind map of AI & durable skills |
| projects/free-education/2026-07-18-durable-skills-vs-ai/build_deck.py | python-pptx 6-slide deck builder |

### weekly-briefings (2026-07-31)

| File | Purpose |
|------|----------|
| projects/weekly-briefings/2026-07-19-human-skills-vs-ai/README.md | The Human-Skills Premium 2026 mid-year trend brief: PwC 62% wage premium, skilliday boom |
| projects/weekly-briefings/2026-07-19-human-skills-vs-ai/build_deck.py | python-pptx 9-slide doodle deck builder (PAPER/INK/ACCENT palette) |
| projects/weekly-briefings/2026-07-19-human-skills-vs-ai/mindmap.mm | FreeMind mind map: DURABLE HUMAN SKILLS, AI shifts, NICHE LEARNING, meta-skill, formula |
| projects/weekly-briefings/2026-06-29-human-nature-evolution-psychology.md | Weekly briefing: human nature, evolution, psychology, major life transitions (June 2026) |

### ai-term-lessons (2026-07-24)

| File | Purpose |
|------|----------|
| projects/ai-term-lessons/README.md | AI Explained Simply series overview: plain-language AI term lessons, 9-episode roadmap |
| projects/ai-term-lessons/mindmaps/AI_Explained_Simply.mm | FreeMind mindmap with speaker notes for Episodes 1–2 and full 9-episode roadmap |
| projects/ai-term-lessons/01_AI_Agent/01_AI_Agent_Lesson_Script.md | Episode 1 script: What's an AI Agent? — slide map, doodle list, Mistral Studio anchor |
| projects/ai-term-lessons/01_AI_Agent/build_deck.js | Episode 1 pptxgenjs Node.js deck builder: Ocean Gradient palette, 5 slides |
| projects/ai-term-lessons/02_Model/02_Model_Lesson_Script.md | Episode 2 script: What's an AI Model? — data+muscle+language formula, next-word predictor |
| projects/ai-term-lessons/02_Model/build_deck.py | Episode 2 python-pptx 5-slide deck builder: Ocean Gradient palette |

### site-monetization (2026-07-24)

| File | Purpose |
|------|----------|
| projects/site-monetization/00-README.md | sourovdeb.com monetization package index — 4 AdSense blockers, 8-file package overview |
| projects/site-monetization/advertiser-attraction-plan.md | Phase-by-phase plan: compliance → AdSense → traffic → direct sponsors; income table |
| projects/site-monetization/category-descriptions.md | SEO descriptions for 11 WP categories + fill-in formula |
| projects/site-monetization/global-improvement-manual.md | Long-term SEO and monetization roadmap, quarterly review guide, Core Web Vitals |
| projects/site-monetization/homepage-meta-tags.md | Homepage title/description options, OG social preview tags, per-post meta formula |
| projects/site-monetization/implementation-manual.md | Step-by-step WP implementation: AdSense blockers through application and ad placement (10 sections) |
| projects/site-monetization/privacy-policy.md | GDPR + AdSense compliant Privacy Policy template — placeholder fields, no live credentials |
| projects/site-monetization/weekly-audit-agent.md | Weekly site audit agent spec: 14-check checklist, Monday 06:00 UTC schedule |

---

## Getting Started

**Beginners**: → [guides/](guides/) → [skills/](skills/)

**Developers**: → [templates/](templates/) → [tools/](tools/) → [evaluation/](evaluation/)

**Integration**: → [agents/](agents/) → [config/](config/) → [prompts/](prompts/)

---

## Tracker

Full file inventory CSV: [`docs/trackers/AI_Agent_Skills_Organization_2026-08-01.csv`](docs/trackers/AI_Agent_Skills_Organization_2026-08-01.csv)

Prior trackers: [`2026-07-31`](docs/trackers/AI_Agent_Skills_Organization_2026-07-31.csv) | [`2026-07-27`](docs/trackers/AI_Agent_Skills_Organization_2026-07-27.csv) | [`2026-07-26`](docs/trackers/AI_Agent_Skills_Organization_2026-07-26.csv)

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
