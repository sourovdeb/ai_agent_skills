# Open Source & Free Tools Collection

All tools listed here are verified, actively maintained, and free.

---

## WordPress Automation

| Tool | GitHub | What it does | Install |
|------|--------|-------------|--------|
| **WP-CLI** | wp-cli/wp-cli | Full WordPress control from terminal | `curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar` |
| **n8n** | n8n-io/n8n | No-code automation (connect any service) | `docker run -p 5678:5678 n8nio/n8n` |
| **Huginn** | huginn/huginn | Agent-based automation, monitors and posts | Docker install |
| **Automattic Newspack** | Automattic/newspack-plugin | Publisher-grade WordPress tools | WordPress plugin |

### WP-CLI Quick Commands
```bash
# Create a draft post from command line
wp post create --post_title="Day 33 Grammar" --post_content="<p>Content here</p>" --post_status=draft

# List all posts missing categories
wp post list --fields=ID,post_title,post_status --post_status=publish

# Bulk assign category
wp post term add 101 102 103 category --by=id elt-masterclass

# Export all posts
wp export --post_type=post --filename_format=posts-export.xml
```

---

## Writing & Note-Taking

| Tool | Website | Best for |
|------|---------|----------|
| **Logseq** | logseq.com | Daily notes, linked knowledge, Markdown export |
| **Obsidian** | obsidian.md | More polished, plugin ecosystem |
| **Joplin** | joplinapp.org | Open source Evernote alternative, syncs to cloud |
| **Standard Notes** | standardnotes.com | Encrypted, minimal, focuses on writing |
| **Zettlr** | zettlr.com | Academic/long-form writing, Pandoc integration |

---

## Automation & Scheduling

| Tool | Type | Free tier | Best for |
|------|------|-----------|----------|
| **n8n** | Self-hosted | Unlimited (self-host) | Replacing Zapier |
| **Zapier** | Cloud | 100 tasks/month | Simple triggers |
| **Make.com** | Cloud | 1,000 ops/month | Visual flows |
| **Activepieces** | Self-host/cloud | Open source | n8n alternative |
| **Windmill** | Self-host | Open source | Python/TS scripts as workflows |
| **Prefect** | Cloud/self-host | Free tier | Python data pipelines |

---

## Email Automation

| Tool | GitHub/Website | What it does |
|------|---------------|-------------|
| **Mautic** | mautic/mautic | Open source email marketing platform |
| **Listmonk** | knadh/listmonk | Self-hosted newsletter and mailing list manager |
| **Postal** | postalserver/postal | Self-hosted email server |
| **EmailEngine** | postalsys/emailengine | IMAP/SMTP to REST API bridge |

---

## Job Hunting Automation

| Tool | GitHub | What it does |
|------|--------|-------------|
| **JobFunnel** | JordanMcDonough/JobFunnel | Scrapes job boards to spreadsheet |
| **job-board-api** | Various | Aggregates Indeed/LinkedIn |
| **python-linkedin** | ozgur/python-linkedin | LinkedIn API wrapper |
| **praw** | praw-dev/praw | Reddit API (find job posts in r/TEFL etc.) |

### Indeed RSS Feed (No Key Needed)
```
https://rss.indeed.com/rss?q=ELT+teacher&l=Reunion
https://rss.indeed.com/rss?q=English+language+teacher&l=
https://rss.indeed.com/rss?q=CELTA
```
Add these URLs to an RSS reader (Feedly, Inoreader) for free job alerts.

---

## Health & Productivity (Neurodivergent-Friendly)

### Mood & Medication Tracking
| App | Platform | Cost | Why it helps |
|-----|---------|------|-------------|
| **eMoods** | Android/iOS | Free | Tracks mood, sleep, medication, energy — specifically designed for bipolar |
| **Bearable** | iOS/Android | Free/Premium | Comprehensive health journal, links mood to activities |
| **Daylio** | iOS/Android | Free | Micro-journal (icons, not words) — very low effort on bad days |
| **Finch** | iOS/Android | Free | Self-care companion — gentle goals, no punishment |
| **Moodfit** | iOS/Android | Free | CBT tools, mood graphs |

### Focus & Productivity
| App | Platform | Cost | Why it helps |
|-----|---------|------|-------------|
| **Forest** | iOS/Android | Paid (worth it) | Grow a tree while you focus — visual motivation |
| **Focusmate** | focusmate.com | Free (3/week) | Virtual body doubling — work with a stranger on video |
| **Brain in Hand** | braininhands.com | NHS-covered | Crisis management for neurodivergent people |
| **Toggl Track** | toggl.com | Free | Time tracking — shows you when you're most productive |
| **Cold Turkey** | getcoldturkey.com | Free basic | Blocks distracting websites on a schedule |

### Sleep
| App | Notes |
|-----|------|
| **Sleep Diary (free)** | Track sleep patterns — important for bipolar management |
| **f.lux** | Reduces blue light in evenings — helps sleep onset |

---

## Content Creation (Free)

### Banner & Image Creation
| Tool | Website | Best for |
|------|---------|----------|
| **Canva** (free) | canva.com | Blog banners, Pinterest, social cards |
| **GIMP** | gimp.org | Full Photoshop replacement |
| **Inkscape** | inkscape.org | Vector graphics (logos, SVG) |
| **Photopea** | photopea.com | Browser-based Photoshop, no install |
| **Pixlr** | pixlr.com | Quick edits in browser |
| **Stable Diffusion** | via Automatic1111 | AI image generation, completely free locally |
| **DALL-E 3** | ChatGPT free | 2 free images/day |

### Audio Tools
| Tool | Website | Best for |
|------|---------|----------|
| **Audacity** | audacityteam.org | Record, edit podcasts |
| **Tenacity** | tenacityaudio.org | Audacity fork (cleaner UI) |
| **Descript** | descript.com | Edit audio like a document (free tier) |
| **ElevenLabs** | elevenlabs.io | AI voice generation (free 10K chars/month) |
| **Whisper** | github.com/openai/whisper | Free transcription (runs locally) |

### Video Tools
| Tool | Website | Best for |
|------|---------|----------|
| **DaVinci Resolve** | blackmagicdesign.com | Professional editing, free forever |
| **Kdenlive** | kdenlive.org | Open source, simpler than Resolve |
| **OpenShot** | openshot.org | Very simple, good for beginners |
| **OBS Studio** | obsproject.com | Screen recording + streaming |
| **Handbrake** | handbrake.fr | Compress/convert video files |

---

## GitHub Repositories Worth Starring

```
wp-cli/wp-cli              — WordPress CLI control
n8n-io/n8n                  — Automation platform
huginn/huginn               — Agent automation
openai/whisper              — Free transcription
knadh/listmonk              — Newsletter management
JordanMcDonough/JobFunnel   — Job search automation
automattic/newspack-plugin  — Publisher WordPress tools
praw-dev/praw               — Reddit API (Python)
audacity/audacity           — Audio editor
Kdenlive/kdenlive           — Video editor
```

Star these on GitHub. They will notify you of updates.
