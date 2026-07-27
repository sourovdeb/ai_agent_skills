# Your Complete WordPress Automation System

> **For someone with bipolar and depression:** Start with ONE thing from this guide. Section 2 (Google Sheets) is the easiest start. Do not try to implement everything at once.

---

## Table of Contents

1. [The "Just Write" Workflow](#1-the-just-write-workflow)
2. [Google Sheets Publishing Queue](#2-google-sheets-publishing-queue) 
3. [Folder Watcher (Logseq Integration)](#3-folder-watcher)
4. [Python Desktop App (GUI)](#4-python-desktop-app)
5. [GitHub + Actions (Auto-publish on push)](#5-github-actions)
6. [WordPress Health Check](#6-wordpress-health)
7. [Job Hunting Automation](#7-job-hunting)
8. [Repository Structure](#8-repository-structure)

---

## 1. The "Just Write" Workflow

You write. Everything else is automatic.

```
You write 500 words in Google Docs / Logseq
         |
         v
Save to ~/Dropbox/wordpress_queue/   (or Google Drive folder)
         |
         v
Folder watcher detects new file (every 15 minutes)
         |
         v
Script auto-generates: tags, category, SEO title, meta description
         |
         v
Sends to WordPress as DRAFT (safe - you review before publishing)
         |
         v
You get a notification. File is moved to /archive.
```

**What you never have to do again:**
- Manually assign categories
- Write SEO descriptions
- Remember to check the queue
- Copy-paste from writing app to WordPress

---

## 2. Google Sheets Publishing Queue

**This is your control centre.** See `guides/03_CSV_GOOGLE_SHEETS_TUTORIAL.md` for the full beginner-friendly tutorial.

**Quick start:**
1. Create a sheet with headers: `Title | Content | Category | Tags | Status | Date | SEO_Title | Meta_Desc`
2. Open Extensions → Apps Script
3. Paste the script from `scripts/sheet_publisher.gs`
4. Set a time trigger (every hour)
5. Fill in rows, set Status to `queued`
6. Done — it publishes automatically

**AI-powered version:** See `guides/02_DEEPSEEK_API_GUIDE.md` — add one function to auto-fill tags and categories using DeepSeek API (~$0.003/month for daily posts).

---

## 3. Folder Watcher

**For Logseq users.** See `scripts/folder_watcher.js`.

Setup (one time):
```bash
npm install -g chokidar-cli  # or use the Node.js script directly
node scripts/folder_watcher.js
```

Write in Logseq → export as Markdown → save to `~/Dropbox/wordpress_queue/` → auto-published as draft.

---

## 4. Python Desktop App

See `scripts/wp_publisher_gui.py`. Run with: `python3 scripts/wp_publisher_gui.py`

Features: publish form, draft/schedule toggle, auto-tag suggestions, no terminal needed.

---

## 5. GitHub Actions

Push a Markdown file to the `drafts/` folder → GitHub Action publishes it to WordPress automatically.

See `.github/workflows/publish_on_push.yml`. Requires `WP_API_KEY` stored as a repository secret.

---

## 6. WordPress Health

Run the health audit to fix existing posts:
```bash
python3 scripts/wordpress_category_fixer.py
```

This will:
- List posts missing tags or categories
- Auto-fix uncategorized posts (guesses category from title)
- Add tags to posts that have none

See `guides/07_WORDPRESS_CATEGORY_TAG_FIX.md` for the full guide.

---

## 7. Job Hunting

See `scripts/job_search.py`. Run daily via cron or GitHub Actions:

```bash
# Cron: run at 8am every day
0 8 * * * /usr/bin/python3 /path/to/scripts/job_search.py
```

Searches Indeed RSS feeds for ELT/TEFL/CELTA positions and emails you a digest.

---

## 8. Repository Structure

```
my_professional_documents/
├── guides/                          ← All tutorial guides (you are here)
│   ├── 01_MASTER_AUTOMATION_GUIDE.md
│   ├── 02_DEEPSEEK_API_GUIDE.md
│   ├── 03_CSV_GOOGLE_SHEETS_TUTORIAL.md
│   ├── 04_FREE_AI_TOOLS_GUIDE.md
│   ├── 05_OPEN_SOURCE_TOOLS_COLLECTION.md
│   ├── 06_AUDIO_VIDEO_BANNER_TOOLS.md
│   ├── 07_WORDPRESS_CATEGORY_TAG_FIX.md
│   └── 08_HEALTH_PRODUCTIVITY_TOOLS.md
├── scripts/                         ← All runnable scripts
│   ├── auto_publisher.py             ← Folder watcher + auto-publish
│   ├── wp_publisher_gui.py          ← Tkinter desktop GUI
│   ├── sheet_publisher.gs           ← Google Apps Script (Sheets)
│   ├── folder_watcher.js            ← Node.js folder watcher
│   ├── job_search.py                ← Indeed/job scraper
│   └── wordpress_category_fixer.py  ← Fix categories/tags in bulk
├── drafts/                          ← Your daily writing
│   └── TEMPLATE_ELT_POST.md
├── .github/workflows/
│   └── publish_on_push.yml          ← Auto-publish when you push a draft
├── Biography_and_Medical/
├── CELTA_Teaching_Materials/
├── tools_and_scripts/               ← Existing tools (kept as-is)
└── therapy_and_wellbeing/
```
