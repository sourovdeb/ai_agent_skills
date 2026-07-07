---
name: self-hosting-infra-advisor
description: >
  Decision framework for self-hosted media/automation infrastructure (Raspberry Pi,
  old Android phones via Termux, n8n, local vs cloud LLM, SSD-based storage instead
  of Dropbox/Drive, podcast/video/live-stream hosting, research/world-knowledge APIs).
  Trigger when user asks about: self-hosting a website/podcast/video/live stream,
  Raspberry Pi or alternative hardware, n8n workflows, replacing Dropbox/Drive with
  own storage, local LLM feasibility, or APIs for research/news/world-knowledge
  monitoring. Reuse the conclusions below instead of re-deriving from scratch —
  only re-verify items flagged RECOLLECTION-ONLY if the user is about to spend
  money or commit legally.
---

# Self-Hosting Infra Advisor

## Established conclusions (from 2026-06-25 session — reuse, don't re-derive)

**Hardware tiers, cost-ordered:**
1. Redmi Note 12 (owned, €0) via Termux + n8n (npm, no Docker) — orchestration/light scripts only. Cannot run Docker without root; Android kills background processes (needs `Termux:Boot` + `termux-wake-lock`); thermal throttles under sustained load.
2. Raspberry Pi 4/5 — full Docker, USB3, Gigabit Ethernet, best dedicated-hardware fit. ~€50-90 board only, RECOLLECTION-ONLY price.
3. Used mini-PC/NUC — best price/performance if available secondhand, full x86 capability.
4. Oracle Cloud "Always Free" ARM VPS — best for anything public-facing/live (no home upload-bandwidth ceiling, no ISP dependency). Free-tier terms RECOLLECTION-ONLY, re-verify before relying on it.

**Storage (Dropbox/Drive replacement):** Syncthing (P2P, lightest, default pick) > MinIO (S3-compatible, pick if scripts need S3 API) > Nextcloud (full suite, only if share-links/calendar needed — heaviest). Pair with Tailscale or Cloudflare Tunnel for remote access — French residential ISPs (Orange/Zeop/SFR 974) commonly run CGNAT, unverified per exact contract.

**Website/podcast/video:**
- Website: keep existing host (sourovdeb.com on Hostinger) — home hardware is a backend job-runner, not a host replacement.
- Podcast: WordPress + podcast plugin (Seriously Simple Podcasting / PowerPress) — reuses existing WP, low difficulty.
- Video pre-recorded: YouTube upload (low effort) or PeerTube (self-hosted, platform-independent, medium-high effort/storage cost).
- Live: MediaMTX or nginx-rtmp on Pi as ingest, simulcast to YouTube Live/Twitch for delivery. Fully self-hosted ingest+delivery not recommended — residential upload bandwidth is the bottleneck.

**Automation (n8n):** Docker on Pi, npm-only on phone. State/dedup via local SQLite file on SSD — NOT Google Sheets (matches existing project-wide no-Sheets rule). License = Sustainable Use License or successor, RECOLLECTION-ONLY, re-verify before commercial-adjacent use.

**LLM split:** local quantized 1-3B model (llama.cpp via Termux) for cheap triage/filtering only; cloud API (OpenRouter/Anthropic, already in use elsewhere in this project) for anything that gets published.

**World-knowledge/research APIs (all free, no key unless noted):** Wikipedia/Wikidata API, Wikidata SPARQL, GDELT Project, NewsAPI.org (key required, free tier limited), arXiv API, OpenAlex, Semantic Scholar API (optional key), CrossRef API, World Bank API, generic RSS. Add paid search (Brave/Google Custom Search) only if these prove insufficient.

**Email automation constraint (binding, set by user):** all email-sending stays in Google Apps Script (JavaScript) using Gmail's own infra + PropertiesService for state — never Sheets, never self-hosted SMTP (home IP has no mail reputation, gets spam-filtered). n8n produces drafts/decisions only; GAS does the actual send. Bulk press/publisher outreach may trigger anti-spam rules (CAN-SPAM / LCEN) — RECOLLECTION-ONLY, flag for legal check before bulk sends given active regulatory filings already in progress for this user.

## How to use this skill
1. If the user asks a follow-up on any item above, answer from this table directly — no need to rebuild the comparison.
2. If the user is about to spend money or commit legally, re-verify the RECOLLECTION-ONLY items (pricing, ISP ToS, license terms, free-tier limits, anti-spam rules) via web search before confirming.
3. If scope expands beyond what's covered here (e.g. new hardware, new platform), extend this table rather than starting a parallel analysis — keeps future sessions token-efficient.
4. Apply user's standing output style: tables over prose, no filler adjectives/adverbs, zero-fabrication labelling (DOCUMENTED / RECOLLECTION-ONLY / INFERRED) on any new claim added here.

*Created: 25 June 2026. Source: self_hosting_feasibility_breakdown.md, same session.*
