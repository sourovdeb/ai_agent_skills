# Content Sync to WordPress — Automated Routine

Source: `sourovdeb/wordpress-control CONTENT_SYNC_README.md`

## Overview

Scheduled routine that syncs content from `my_professional_documents` and `free_education`
repositories to sourovdeb.com as draft posts, **without pushing duplicates**.

## How It Works

- **Schedule**: Runs every hour at `:07` past the hour
- **Verification**: Fetches existing draft/scheduled posts from WordPress, compares titles to avoid duplicates
- **Categorization**: Assigns content to one of 8 categories:
  - Mental Health
  - ELT Masterclass
  - English Teaching
  - Philosophy
  - Photography
  - Software
  - DXO
  - Learn AI in Mistral Studio
- **Exclusions**: Skips sensitive directories:
  - Biography_and_Medical
  - Legal_Documents
  - therapy_and_wellbeing
  - Story_of_Sourov
  - All `*_extracted`, `*_archive` directories

## Baseline (2026-07-19)

- **Existing posts on WordPress**: 50 (draft/scheduled)
- **New items found in repos**: 117 (after dedup)
- **Distribution**:
  - Learn AI in Mistral Studio: 32
  - Software: 44
  - Mental Health: 15
  - ELT Masterclass: 9
  - English Teaching: 7
  - Philosophy: 5
  - Photography: 5

## Scripts

**`../my_professional_documents/wordpress_integration/sync_verification.py`**

Main verification and push script. Reads all `.md` files from repos, deduplicates against
WordPress, categorizes, and pushes up to 5 new items per run.

```bash
python3 wordpress_integration/sync_verification.py
```

## Important Notes

- Routine is **session-only** (in-memory) — survives only while Claude session is active
- Auto-expires after 7 days
- Pushes only drafts (never auto-publishes)
- Checks for exact title matches to prevent duplicates
- API credentials: **[REDACTED — rotate immediately, store in VS Code settings or password manager, never in source files. See INC2671905.]**

---

*Set up 2026-07-19 by Claude Code*
