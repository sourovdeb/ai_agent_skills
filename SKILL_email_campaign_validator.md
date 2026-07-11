# SKILL_email_campaign_validator

**Trigger phrases:** email campaign validator, bulk email compliance gate, CV wording check CELTA, Gmail bulk sender dry run, batch resumable outreach, GMAIL_BULK_SENDER_v2, compliance blocker email send

## Purpose

Validates and safely executes bulk email campaigns for job applications, regulatory follow-ups, or targeted outreach. Enforces hard compliance gates on attachments and content (specifically prohibiting non-compliant CELTA terminology in CVs per established memory and legal strategy). Supports dry-run mode (drafts only), resumable batch processing via PropertiesService state, detailed logging, and controlled progression from test to live sends.

## When to Activate

- Preparing or running bulk job application emails or authority correspondence
- Before any live send where CV, motivation letter, or attachments must pass compliance review
- Recovering or resuming a partially completed email batch
- Validating recipient list integrity + content + attachment compliance in one pass
- Cross-checking against regulatory tracker or research outputs before outreach

## Core Guardrails (Rigorous Execution Framework)

- **Verification Before Action**: Explicitly confirm Drive file IDs exist, filenames are clean, and content passes compliance BEFORE any send attempt. State: "Verified in Drive" or "Cannot confirm — provide latest file ID."
- **Hard Compliance Gate**: Script MUST block send if CV filename or extracted content contains blacklisted terms ("certified", "titulaire", "certifié", etc.). Only permitted phrasing allowed in filename and visible text: "Formation Cambridge CELTA complétée — 120 heures supervisées, 4 travaux écrits validés au standard requis, qualification en appel"
- **Dry-Run Default TRUE**: All runs start in test mode. Emails draft to sender account (sourovdeb.is@gmail.com or connected) for manual inspection of 2–3 samples before live.
- **Resumable Batches**: PropertiesService tracks completion index. Can resume without re-sending duplicates. Full audit log of every attempted send.
- **Evidence & Logging**: Every batch run logged with timestamp, recipient count, compliance status, and outcome. Persist logs to Drive or GitHub.

## Recommended Script Architecture (GMAIL_BULK_SENDER_v2.gs)

- CONFIG object: DRY_RUN, CV_FILE_ID, MOTIVATION_FILE_ID, EMAIL_LIST array (to, subject, body template), BATCH_SIZE
- Functions:
  - setup_InitialRun() — one-time PropertiesService initialization
  - checkCompliance(fileId) — filename + content gate (hard fail if violated)
  - sendBatch() — main loop with dry-run branching, resume logic, logging
  - getStatus() — report current batch progress
- Always present pre-run checklist table to user

## Pre-Run Validation Table (Mandatory)

| Priority | Action | Blocker? | Current Status / Notes |
|----------|--------|----------|------------------------|
| 1        | Rename CV file in Drive (remove prohibited CELTA wording) | **YES** — hard lock on all sends | Pending user action |
| 2        | Complete EMAIL_LIST (indices 11–40) in script | **YES** — script requires full list | User to paste real addresses |
| 3        | Update CONFIG.CV_FILE_ID and MOTIVATION_FILE_ID if changed | **YES** — attachment load fails otherwise | Verify current IDs |
| 4        | Run setup_InitialRun() once | No | Creates PropertiesService state |
| 5        | Run sendBatch() with DRY_RUN=true | No | Safe test mode; inspect drafts |
| 6        | Manual review of 2–3 drafts in Gmail | No | Confirm compliance + tone |
| 7        | Set DRY_RUN=false and re-run sendBatch() | No | Only after explicit approval |

## Integration Points

- Directly supports job-search-agent and regulatory filing tracker (outreach to employers or authorities)
- Pulls research synthesis outputs for personalized email body content
- Respects CELTA memory and prohibited wording rules from legal-reasoning-agent / authority-letters
- Logs can feed back into Consolidated_Skills_Summary.md or case tracker

## Prevention of Common Failures

- Never bypass compliance gate even for "test" sends
- Always confirm recipient list is clean and consented (where required)
- Use only approved CV filename before first run
- Keep sender address consistent (sourovdeb.is@gmail.com or connected Google account)
- After live batch, archive logs and update regulatory tracker if any authority emails were included

## Activation Command Example

"Run email campaign validator on job applications batch #3 with DRY_RUN=true first"