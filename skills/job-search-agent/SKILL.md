---
name: job-search-agent
description: >
  Multi-tool AI agent skill for job seekers who need document creation, career research,
  email history analysis, and job opportunity tracking — all in one workflow.
  Trigger this skill whenever a user asks to update their CV, motivation letter, research
  job opportunities, analyze their email history for career context, create a career CSV,
  or export documents to PDF. Also trigger when the user provides uploaded CV/cover letter
  files and asks for improvements, translations, or reformatting. This skill handles
  partial requests — the agent does NOT need to fulfill all tasks at once. Each section
  below contains conditional logic: "IF user asks X → THEN do Y."
---

# Job Search Agent Skill

## Overview

This skill orchestrates multiple tools to help a job seeker:
- Update CV and motivation letter with correct certifications and terminology
- Research and compile 50-100+ career opportunities
- Cross-reference Gmail history for employer contacts already made
- Create structured CSV databases of opportunities
- Export final documents as PDF
- Build a skill from a completed agent workflow

The agent reads context first, then executes only what the user asks.

---

## STEP 0 — Always Execute First (Context Load)

Before any other action, always run these in order:

```
1. recent_chats(n=5)              — understand prior conversation context
2. read uploaded files            — parse CV, cover letter, any docs provided
3. conversation_search(query)     — search for relevant past discussions
```

Do NOT skip Step 0 even if the request seems simple. The user's history shapes all outputs.

---

## CONDITIONAL TASK MAP

Each task below is independent. Execute only what the user requests.
Multiple tasks can be requested at once — execute them in the order listed below.

---

### IF user asks: "Update my CV" / "Fix my CV" / "Improve my CV"

**Tools**: `view` (uploaded files) → `bash_tool` (PDF generation)

**Process**:
1. Read uploaded CV file from `/mnt/user-data/uploads/`
2. Check chat history for any prior CV discussions
3. Identify terminology issues (e.g., certifications, job titles, dates)
4. Verify any certification names against official sources via `web_search`
   - Example: "CELTA" → verify it is "Cambridge CELTA Certified" not "Cambridge certified teachers for CELTA"
5. Rebuild CV in Markdown first (structured, section-by-section)
6. Export to PDF using `reportlab` (see PDF Generation section below)
7. Save to `/mnt/user-data/outputs/CV_[NAME]_[YEAR].pdf`
8. Call `present_files` with final PDF path

**Key rules**:
- Keep original content — only update what user explicitly asks to change
- Verify certifications, company names, dates against official online sources
- Always use A4 format for French/EU market CVs
- Two-column layout preferred for professional CVs (sidebar + main)

---

### IF user asks: "Update my motivation letter" / "Fix my cover letter"

**Tools**: `view` → `bash_tool` (PDF)

**Process**:
1. Read uploaded letter from `/mnt/user-data/uploads/`
2. Identify company/position being targeted (from context or ask user)
3. Align terminology with updated CV (same certifications, same job titles)
4. Update letter content — preserve tone, only fix what user requests
5. Export to PDF with consistent branding (same palette as CV)
6. Save to `/mnt/user-data/outputs/LETTRE_MOTIVATION_[NAME]_[YEAR].pdf`
7. Call `present_files`

**Key rules**:
- Motivation letter and CV must use identical certification wording
- French market: formal tone mandatory ("Madame, Monsieur," / "salutations distinguées")
- If target company/sector is known, tailor the letter to that sector

---

### IF user asks: "Research job opportunities" / "Find jobs for me"

**Tools**: `web_search` (multiple queries) + `Gmail:search_threads` (email context)

**Process**:
1. Search Gmail for prior outreach emails to identify already-contacted employers
   - Query: `subject:(teaching OR job OR emploi OR formateur)`
2. Run targeted web searches by:
   - Local market (La Réunion, Indian Ocean region)
   - National market (France mainland)
   - International (by relevant region)
   - Job boards (TEFL.com, Glassdoor, Indeed, LinkedIn, Serious Teachers)
3. Cross-reference web results with Gmail history — mark "Already contacted" or "New"
4. Compile into structured document with:
   - Organisation name, sector, location, position type, salary estimate, status, source
5. Save as Markdown guide + CSV

**Minimum output**: 50 opportunities. Target: 75-100+.

**Key search queries (adapt per user profile)**:
```
"[certification] teacher jobs [location] [year]"
"[specialisation] trainer [region] CELTA TEFL"
"English teacher jobs [island/city] 2026"
"[sector] English trainer [country]"
"[certification] jobs salary 2026"
```

---

### IF user asks: "Create a CSV from my chat history / email history"

**Tools**: `recent_chats` + `Gmail:search_threads` + `create_file`

**Process**:
1. Pull recent chats (up to 20 per batch via `recent_chats`)
2. Pull Gmail threads (up to 50 at once via `Gmail:search_threads`)
3. Identify career-relevant items: job contacts, applications sent, responses received
4. Structure data into CSV columns:
   ```
   Organisation, Type, Location, Contact_Sector, Position_Title,
   Language_Requirements, Certification_Required, Status, Date_Found, Source
   ```
5. Mark email delivery failures separately (bounced emails = dead contacts)
6. Save CSV to `/mnt/user-data/outputs/[NAME]_CAREER_CSV_[YEAR].csv`
7. Call `present_files`

---

### IF user asks: "Make the CV/letter in PDF" / "Export to PDF"

**Tools**: `bash_tool` with `reportlab`

**Process**:
1. Read existing `.md` files from `/mnt/user-data/outputs/`
2. Run PDF generation script (see template below)
3. Save to `/mnt/user-data/outputs/[document_name].pdf`
4. Call `present_files`

**PDF Generation Template** (ReportLab — A4 professional):
```python
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable
)

# Color palette — adjust per user brand
NAVY  = colors.HexColor("#1a2e4a")
GOLD  = colors.HexColor("#b8892e")
WHITE = colors.white
BLACK = colors.HexColor("#1a1a1a")

# Two-column layout: COL_L = 58mm (sidebar), COL_R = remainder
# Header banner: full width, NAVY background
# Body: Table([[left_content, right_content]], colWidths=[COL_L, COL_R])
# Font: Helvetica (built-in, no install needed)
# Page: A4, margins 0 left/right (let table handle padding)
```

**Critical rules**:
- Never use Unicode subscript/superscript characters in ReportLab
- Use `Paragraph` with HTML-like tags for bold, italic: `<b>text</b>`
- Escape ampersands as `&amp;`, arrows as `&#8594;`, bullets as `&#8226;`
- Test with `python script.py` before presenting to user

---

### IF user asks: "Create a skill from this workflow"

**Tools**: `create_file` → `bash_tool` (package if needed)

**Process**:
1. Review the full conversation to extract:
   - Tools used (list in order)
   - Decision logic applied
   - Conditional branches taken
   - Outputs produced
2. Write SKILL.md with:
   - YAML frontmatter (name, description)
   - Conditional task map (IF user asks X → THEN do Y)
   - Tool usage per task
   - Key rules and constraints
   - Output specifications
3. Save to `/mnt/user-data/outputs/[skill-name]/SKILL.md`
4. Package if `bash_tool` available: `python -m scripts.package_skill path/`
5. Call `present_files`

**Key principle**: Skills must handle partial execution. Each task section is independent. The agent does NOT run everything at once — it reads the user's specific request and executes only the relevant sections.

---

## TOOL USAGE MAP (Reference)

| Task | Primary Tools | Secondary Tools |
|------|--------------|-----------------|
| Read uploaded files | `view`, `bash_tool` | `create_file` |
| Check chat history | `recent_chats`, `conversation_search` | — |
| Check email history | `Gmail:search_threads`, `Gmail:get_thread` | — |
| Verify certifications/terminology | `web_search` | `web_fetch` |
| Research job opportunities | `web_search` (multiple) | `Gmail:search_threads` |
| Create CV (Markdown) | `create_file` | `str_replace` |
| Create Motivation Letter (Markdown) | `create_file` | — |
| Export to PDF | `bash_tool` + `reportlab` | `present_files` |
| Create CSV | `create_file` | — |
| Present outputs | `present_files` | — |
| Save to Google Drive | `Google Drive:create_file` | — |

---

## EXECUTION PRINCIPLES

### Principle 1 — Context First
Always load chat history and uploaded files before acting.
Never assume you know the user's situation without checking.

### Principle 2 — Partial Execution Is Valid
The agent does NOT need to complete all tasks in a single turn.
If the user asks for one thing, do one thing well.
Confirm before starting a large multi-step sequence.

### Principle 3 — Cross-Reference
When updating a document, cross-reference:
- Uploaded source files (ground truth)
- Chat history (user preferences stated earlier)
- Official web sources (certifications, company names, job titles)
- Gmail history (what has already been done/sent)

Conflicts between sources → ask the user to clarify.

### Principle 4 — Verify Claims
For any certification, qualification, or official body name:
- Run `web_search` to confirm correct terminology
- Example: CELTA is issued by Cambridge University → "Cambridge CELTA Certified" is correct

### Principle 5 — Consistent Terminology
CV and motivation letter must use identical wording for:
- Certification names
- Job titles
- Company names
- Date ranges

If they differ, flag to user and standardise.

### Principle 6 — Output Quality Gates
Before calling `present_files`:
- PDF: run `python script.py` and confirm exit code 0
- CSV: check for missing columns, encoding issues (UTF-8)
- Markdown: confirm headers, tables, bullets render correctly
- Never present a file that errored during generation

---

## OUTPUT SPECIFICATIONS

| Output Type | Format | Path Pattern | Naming Convention |
|-------------|--------|-------------|-------------------|
| Updated CV | PDF | `/mnt/user-data/outputs/` | `CV_[LASTNAME]_[YEAR].pdf` |
| Motivation Letter | PDF | `/mnt/user-data/outputs/` | `LETTRE_MOTIVATION_[LASTNAME]_[YEAR].pdf` |
| Career Guide | Markdown | `/mnt/user-data/outputs/` | `CAREER_OPPORTUNITIES_GUIDE.md` |
| Career CSV | CSV | `/mnt/user-data/outputs/` | `CAREER_OPPORTUNITIES_CSV.csv` |
| Skill File | Markdown | `/mnt/user-data/outputs/[skill-name]/` | `SKILL.md` |

---

## KNOWN CONSTRAINTS

- `Gmail:search_threads` returns max 50 per call — paginate with `pageToken` if needed
- `recent_chats` returns max 20 per call — paginate with `before` parameter
- ReportLab: built-in fonts (Helvetica, Times, Courier) only — no TTF unless installed
- PDF generation: always test in `bash_tool` before presenting to user
- Skill files: `/mnt/skills/` is read-only — write to `/mnt/user-data/outputs/` or `/home/claude/`
- CSV: use UTF-8 encoding, comma delimiter, quoted strings for fields with commas

---

## EXAMPLE FLOW (This Conversation)

The following is a record of the actual tool execution from the session that created this skill:

```
Step 0:  recent_chats(n=5)                    → loaded 5 prior chats (career/legal context)
Step 1:  view("/mnt/user-data/uploads")        → found 3 files (CV PDF, letter PDF, CV docx)
Step 2:  web_search("CELTA terminology")       → verified "Cambridge CELTA Certified"
Step 3:  tool_search("Gmail")                  → loaded Gmail tools
Step 4:  Gmail:search_threads(50 threads)      → found 19 employer outreach emails + career emails
Step 5:  web_search × 3                        → researched 30+ job sources
Step 6:  create_file(CV.md)                    → updated CV with correct terminology
Step 7:  create_file(lettre.md)                → updated motivation letter
Step 8:  create_file(guide.md)                 → 75+ opportunities with salary analysis
Step 9:  create_file(opportunities.csv)        → 55 organisations in structured CSV
Step 10: bash_tool + reportlab × 2             → CV.pdf + lettre.pdf generated
Step 11: create_file(SKILL.md)                 → this file
Step 12: present_files([all outputs])          → delivered to user
```

**Total outputs**: 6 files (2 PDFs, 2 MDs, 1 CSV, 1 SKILL.md)
**Total tools used**: view, recent_chats, web_search × 3, Gmail:search_threads,
                      create_file × 4, bash_tool × 2, present_files, tool_search × 2

---

## CONDITIONAL QUICK REFERENCE

```
IF user asks "update CV"               → read files → verify terms → rebuild → PDF
IF user asks "update letter"           → read files → align with CV → rebuild → PDF
IF user asks "research jobs"           → Gmail history + web_search × N → compile
IF user asks "create CSV"              → recent_chats + Gmail → structure → export
IF user asks "make PDF"                → read md files → reportlab → present
IF user asks "create skill"            → extract workflow → write SKILL.md → package
IF user asks "check chat history"      → recent_chats + conversation_search
IF user asks "check my emails"         → Gmail:search_threads with relevant query
IF user asks for all tasks at once     → execute in order: context → docs → research → PDF → skill
IF user asks for only one task         → execute that task only, confirm before expanding
IF tool call fails                     → check error, retry with corrected params, report to user
IF certification name uncertain        → web_search official source before writing
IF email delivery failed (in history)  → flag in CSV as "Dead contact", suggest alternative
```

---

*Skill created: 18 May 2026*
*Based on: live agent session for Sourov DEB career documents*
*Compatible with: Claude.ai projects with Gmail + Google Drive connectors*
