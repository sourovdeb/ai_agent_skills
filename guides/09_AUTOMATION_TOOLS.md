# Free & Open Source Automation Tools

**Principle:** Automate everything. Write once. Collect proven tools. Recycle scripts.

---

## JOB SCRAPING & TRACKING

### Indeed Scraper (Custom)
- **What:** Scrapes Indeed.com for jobs
- **Tool:** `automation_scripts/indeed_scraper.py`
- **Free:** Yes (no API key needed)
- **Use:** Find teaching/writing/tech jobs daily
- **Command:** 
  ```bash
  python3 automation_scripts/indeed_scraper.py --keywords "English teacher" --location "France"
  ```

### LinkedIn Job Alerts (Browser Extension)
- **What:** Email alerts for LinkedIn jobs
- **Tool:** LinkedIn Built-in
- **Free:** Yes (premium adds filters)
- **Use:** Set up job alerts, export to CSV
- **Setup:** linkedin.com/jobs → Alerts → Email me

### FlexJobs (Paid Alternative)
- **What:** Hand-curated remote jobs
- **Cost:** $15/month
- **Worth it?** If you want verified remote-only positions

### ScraperAPI (Free tier)
- **What:** Headless browser scraping
- **Free:** 1000 requests/month
- **Use:** Advanced job scraping with JavaScript rendering

---

## EMAIL AUTOMATION

### n8n (Self-Hosted)
- **What:** Visual workflow automation (IFTTT-like)
- **Free:** Self-hosted open source
- **Use:** Email sequences, job alerts → Gmail drafts, outreach campaigns
- **Install:** `docker run -it -p 5678:5678 n8nio/n8n`

### Zapier (Paid)
- **What:** Connect 5000+ apps without code
- **Cost:** $19-49/month (free tier: 100 tasks/month)
- **Use:** Job alerts → Email → Spreadsheet, LinkedIn → CRM

### Make.com (Integromat)
- **What:** Like Zapier, European-based
- **Cost:** Similar to Zapier
- **Free:** 1000 operations/month free tier

### Email Hunter / Hunter.io
- **What:** Find email addresses of professionals
- **Cost:** Free: 50 searches/month; Paid: $50+/month
- **Use:** Find contact emails for cold outreach
- **Accuracy:** 95%+

---

## CONTENT MANAGEMENT & PUBLISHING

### WordPress (Your Site)
- **What:** `tools/wp_publisher.py` (direct publish)
- **Cost:** Hosting (~€5-10/month), Domain
- **Custom Plugins:** Create your own
- **SEO:** Yoast, RankMath (free + paid)

### Markdown to WordPress Converter
- **Tool:** `tools/wp_publisher.py`
- **Features:** Auto SEO metadata, categories, tags, scheduling
- **Use:** `python3 tools/wp_publisher.py --file daily_essays/essay.md --publish`

### Hugo + Netlify (Static Site)
- **What:** Fast static site generator + free hosting
- **Free:** Yes (Netlify tier)
- **Use:** Backup blog, faster load times
- **Deploy:** Push to GitHub → Auto-deploy

### Ghost (Hosted)
- **What:** Modern publishing platform
- **Cost:** $9/month hosted (open source free)
- **Features:** Newsletters, membership, clean interface

---

## CONTACT & RELATIONSHIP MANAGEMENT

### Airtable (Free + Paid)
- **What:** Spreadsheet-database hybrid
- **Free:** Unlimited records, basic automation
- **Use:** Track contacts, writing projects, job applications

### HubSpot CRM (Free)
- **What:** Contact relationship management
- **Free:** Full CRM + 1000 contacts
- **Use:** Email tracking, deal pipeline (job applications)

### Dex (Personal CRM)
- **What:** Lightweight contact management for writers
- **Cost:** Free/$5/month

---

## WRITING & PRODUCTIVITY

### Obsidian (Free + Paid)
- **What:** Local markdown vault, PKM system
- **Free:** Personal use
- **Use:** Organize essays, ideas, health notes

### Notion (Free)
- **What:** All-in-one workspace
- **Free:** Unlimited personal use
- **Use:** Essay drafts, job tracker, contact database, health journal

### Hemingway Editor
- **What:** Simplify writing (active voice, passive detection)
- **Cost:** Free web version (hemingwayapp.com) or $19 desktop

### Grammarly
- **What:** Grammar + plagiarism checker
- **Free:** Browser extension, basic checks
- **Paid:** $12/month for advanced

### Copyscape
- **What:** Check for plagiarism, duplicate content
- **Cost:** Free (limited searches)

---

## SEO OPTIMIZATION

### Yoast SEO (WordPress Plugin)
- **What:** On-page SEO analysis
- **Free:** Plugin (free version)

### RankMath (WordPress Plugin)
- **What:** Advanced SEO + Schema markup
- **Free:** Core features

### Google Search Console
- **What:** Monitor your site's performance in Google
- **Cost:** Free
- **Use:** Track rankings, fix indexing issues, check CTR

### AnswerThePublic
- **What:** See what people search for
- **Free:** 2 searches/day
- **Use:** Find essay topics, keywords people actually search

---

## SOCIAL MEDIA AUTOMATION

### Buffer (Paid)
- **What:** Schedule posts to Twitter, LinkedIn, etc.
- **Cost:** $5-99/month

### IFTTT (Free)
- **What:** If This Then That - simple automation
- **Free:** 3 applets max
- **Use:** WordPress new post → Tweet, LinkedIn share

---

## SCHEDULING & CRON JOBS

### Cron (Built-in Linux)
- **What:** Schedule scripts to run automatically
- **Free:** Built into Linux/Mac
- **Use:** Run job scraper daily, check emails, publish scheduled posts
- **Setup:**
  ```bash
  crontab -e
  # Run job scraper every morning at 9 AM
  0 9 * * * python3 /path/to/automation_scripts/indeed_scraper.py --keywords "teacher"
  # Check email every hour
  0 * * * * python3 automation_scripts/email_checker.py
  ```

### GitHub Actions (Free)
- **What:** Run workflows on GitHub push/schedule
- **Free:** 2000 minutes/month
- **Use:** Auto-scrape jobs, publish scheduled essays, send weekly digest

---

## ANALYTICS & TRACKING

### Google Analytics (Free)
- **What:** Track blog visitors
- **Free:** Yes
- **Use:** See which essays get traffic

### Plausible (Privacy-Friendly)
- **What:** Simple analytics, no cookies
- **Cost:** $9/month

---

## BACKUP & VERSION CONTROL

### GitHub (Free Public Repo)
- **What:** Version control + backup
- **Free:** Unlimited public repos
- **Use:** Your essays, scripts, everything tracked

### GitHub Actions Backup
```yaml
name: Daily Backup
on:
  schedule:
    - cron: '0 2 * * *'  # 2 AM daily
jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: |
          git add .
          git commit -m "Daily auto-backup"
          git push
```

---

## RECOMMENDED WORKFLOW

**Free Stack (Best for starting):**
1. **Writing:** Obsidian (local) + WordPress (publish) + GitHub (backup)
2. **Jobs:** Custom scraper + Airtable (free tier)
3. **Contacts:** HubSpot CRM (free)
4. **Email:** Gmail + n8n (self-hosted)
5. **Analytics:** Google Analytics
6. **Automation:** Cron jobs + GitHub Actions

**Paid Upgrade (When making money):**
1. Add Zapier for complex workflows
2. Add Hunter.io for email finding
3. Add RankMath for advanced SEO
4. Add Buffer for social sharing

---

## QUICK COMMAND CHEAT SHEET

```bash
# Publish essay to WordPress
python3 tools/wp_publisher.py --file daily_essays/my_essay.md --publish

# Schedule daily jobs scraping
crontab -e
# Add: 0 9 * * * cd /path/repo && python3 automation_scripts/indeed_scraper.py
```

---

**Source:** `my_professional_documents/tools_collection/AUTOMATION_TOOLS.md`  
**Last Updated:** 2026-06-02  
**Next Review:** Monthly
