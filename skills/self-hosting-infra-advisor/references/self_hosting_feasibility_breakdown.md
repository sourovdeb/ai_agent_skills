# Self-Hosted Media + Research Automation — Feasibility Breakdown

**Scope:** website / podcast / video (live + pre-recorded), constant info search/collection, own-SSD storage (Dropbox/Drive replacement), automated email trigger to publishers/news agencies.
**Constraint set by user:** no Raspberry Pi purchase assumed as default — Redmi Note 12 (idle phone) evaluated first. Email automation = Google Apps Script (JS), no Google Sheets. n8n + local/cloud LLM in the loop.
**Sourcing note:** no live web search run for this document — pricing, ISP terms, license terms, and free-tier limits below are RECOLLECTION-ONLY and may be outdated. Verify before financial or legal commitment. List of items to verify is in Section 10.

---

## 1. Hardware Comparison

| Device | Upfront cost | Setup difficulty | 24/7 reliability | Docker / n8n | SSD attach | Network | Verdict |
|---|---|---|---|---|---|---|---|
| Redmi Note 12 (Termux) | €0 (owned) | Medium — no-root Linux userspace, no Docker | Low–Medium — Android kills background processes, heat, battery wear if always-on | n8n via `npm`, not Docker | USB-C OTG, power/throughput depends on exact model/cable — unverified | Wi-Fi only unless USB-Ethernet dongle | Orchestration / light scripts only — not a media server |
| Raspberry Pi Zero 2 W | ~€15–20 (approx.) | Medium | Medium | npm yes; Docker possible, tight on RAM | USB2 only | Wi-Fi, no native Ethernet | Weakest dedicated option |
| Raspberry Pi 4/5 (4–8GB) | ~€50–90 board only (approx.) | Low–Medium — large community, official OS | High | Full Docker support | USB3, real throughput | Gigabit Ethernet | Best dedicated hardware fit |
| Used mini-PC / NUC | ~€60–150 used (approx.) | Low — x86, runs anything | High | Full | SATA/NVMe internal | Gigabit Ethernet | Best price/performance if one is available secondhand |
| Oracle Cloud "Always Free" ARM VPS | €0 (free tier — verify current terms) | Low–Medium | Highest — no home power/ISP dependency | Full | Cloud block storage, not physically yours | Datacenter uplink, no home-upload bottleneck | Best for anything public-facing or live |

**Read:** the phone is free and good enough for the automation/orchestration layer. It is not good enough for video encoding, live streaming, or local LLM inference at usable quality. Treat it as a starting point, not the end state.

---

## 2. Redmi Note 12 as Server — Specifics

- Install path (no root): Termux → `pkg install nodejs python git` → `npm install -g n8n` → `n8n start`.
- Docker will not run without root on a stock Android kernel — plan around npm-only.
- Required to survive 24/7: `Termux:Boot` (restart on reboot) + `termux-wake-lock` (prevent Android from suspending the process). Without both, the server dies when the screen sleeps.
- Thermal throttling under sustained load (LLM inference, video transcoding) is a mobile-SoC limitation, not a config issue — expect slowdowns under continuous use.
- Storage wear: phone internal storage (UFS) handles continuous writes better than an SD card, but still not designed for server-grade write cycles. An attached SSD over USB-C OTG is preferable for any data that matters — confirm this exact phone model supports USB OTG host mode with sufficient power delivery before buying a drive/enclosure.

---

## 3. Storage Layer (Dropbox / Drive replacement)

| Tool | Model | Resource need | Fit |
|---|---|---|---|
| Syncthing | Peer-to-peer, no central server | Very low | Best fit — simplest, runs on Termux and Pi alike |
| Nextcloud | Client-server, full office/calendar/share-link suite | Medium–High (PHP + DB) | Overkill unless Drive-style shareable links are needed |
| MinIO | S3-compatible object store | Low–Medium | Best if scripts/APIs expect S3-style access |
| Samba/SMB | LAN file share | Low | Local network only, no remote access |

**Remote access without a public IP:** most French residential ISPs (Orange, Zeop, SFR, etc. in 974) run CGNAT or restrict inbound ports on default plans — unverified for your specific contract. Tailscale or Cloudflare Tunnel solves this without router port-forwarding or a static IP. Recommended over trying to expose the SSD directly to the internet.

---

## 4. Website / Podcast / Video

| Output | Self-host? | Recommended path | Difficulty |
|---|---|---|---|
| Website | Already hosted (Hostinger) | Keep as-is. Home server becomes a backend job-runner that pushes to the existing WP REST endpoint — not a replacement host. | N/A — already solved |
| Podcast (audio) | Yes, trivially | WordPress + podcast plugin (e.g. Seriously Simple Podcasting, PowerPress) — generates the RSS feed Apple/Spotify need, reuses existing WP install | Low |
| Pre-recorded video | Optional | Two paths: (a) upload directly to YouTube — zero self-host cost, but platform-dependent; (b) PeerTube (self-hosted, federated, YouTube-alternative) for platform independence | (a) Low / (b) Medium-High — storage + upload bandwidth become the real cost |
| Live stream | Partial self-host recommended | Run MediaMTX or nginx-rtmp on the Pi as ingest, simulcast (restream) to YouTube Live / Twitch for actual delivery to viewers | Medium |
| Fully self-hosted live (own ingest **and** delivery, no platform) | Not recommended | Residential upload bandwidth in 974 — unverified for your plan — is almost always the bottleneck at viewer-count > a handful | High difficulty, low payoff vs. simulcasting |

---

## 5. Automation Layer — n8n

- Pi: install via Docker (standard, documented path).
- Phone: npm only, no Docker (see Section 2).
- License: n8n's self-hosting terms have changed before (Sustainable Use License model — free for internal/personal use, restrictions apply to reselling n8n itself as a hosted service) — RECOLLECTION-ONLY, verify at n8n.io before any commercial-adjacent use.
- Example chain (orchestration only, no Sheets):
  `RSS/API trigger → dedupe against local SQLite file on SSD → cloud LLM summarize/score → draft to WordPress or Gmail draft → human approval → publish/send`
- SQLite (a single file on the SSD) replaces the role Sheets would otherwise play for state/dedup — consistent with the existing "no Sheets dependency" rule, and queryable directly from an n8n Execute Command node or a small script.

---

## 6. LLM Strategy

| Tier | Where | Use |
|---|---|---|
| Local (llama.cpp, 1–3B quantized model) | Pi or phone via Termux | Cheap triage: relevance filtering, dedup-by-meaning, tagging — not final-quality writing |
| Cloud API (existing OpenRouter key, or Anthropic API) | Called from n8n's HTTP Request node | Actual drafting, summarization, research synthesis — where quality matters |

Local model pre-filters before anything reaches a paid cloud call — keeps token/API cost down without sacrificing output quality on the parts that get published.

---

## 7. World-Knowledge / Research APIs

| API | Auth | Cost | Best for |
|---|---|---|---|
| Wikipedia / Wikimedia REST API | None | Free | Facts, entity lookups, summaries |
| Wikidata SPARQL endpoint | None | Free | Structured/relational queries |
| GDELT Project | None | Free | Global news/event monitoring at scale |
| NewsAPI.org | API key | Free tier limited, paid above that | Current headlines by topic/region |
| arXiv API | None | Free | Academic preprints (directly relevant to your JEFL/manuscript work) |
| OpenAlex | None | Free | Scholarly works metadata, citation graphs |
| Semantic Scholar API | Optional key | Free | Paper search, citation context |
| CrossRef API | None | Free | DOI/citation metadata |
| World Bank API | None | Free | Economic/development data |
| Generic RSS (any publisher/journal) | None | Free | Continuous monitoring without any key management |

These cover the "constant search, collection, organisation" requirement without paid search APIs. Add a paid search API (Brave Search API or Google Custom Search) only if RSS + the above prove insufficient for a specific gap.

---

## 8. Email Automation — Constraint

Do not self-host outbound SMTP from the Pi/phone/home IP. A home connection has no mail-server reputation (no SPF/DKIM/DMARC history, no reverse DNS) — Gmail/Outlook will spam-filter or block it almost immediately. This is a deliverability fact independent of script quality.

Per your stated preference, all email-sending stays in Google Apps Script (JavaScript), using Gmail's own sending infrastructure, with state in PropertiesService — no Sheets. n8n's role stops at producing the draft/decision; the actual send is a GAS function, mirroring the existing `france_travail_job_collector.gs` / Gmail Bulk Sender pattern already in place. This avoids running two separate Gmail-credential surfaces (n8n's Gmail node and GAS) for the same job.

For "automatically trigger email to publisher or news agency" specifically: unsolicited bulk outreach to press contacts may fall under anti-spam rules (CAN-SPAM if any US recipients; French/EU rules under LCEN for B2B prospecting) — RECOLLECTION-ONLY, not verified against current text. Given the active regulatory filings already in progress, this is worth a direct check before any bulk send, not an assumption.

---

## 9. Recommended Path (cost-ordered)

1. **Now, €0:** Redmi Note 12 + Termux + n8n (npm) + Syncthing for orchestration and file sync. Cloud LLM via existing OpenRouter/Anthropic API key. WordPress/Hostinger and Gmail/GAS stay exactly as they are.
2. **If outgrown (storage/CPU/uptime limits hit):** Raspberry Pi 4/5 + Docker n8n + MediaMTX + dedicated SSD. Real Ethernet, real Docker, real 24/7 stability.
3. **If home network/ISP becomes the bottleneck for anything public-facing (live stream viewers, public API):** Oracle Cloud free ARM VPS, or equivalent, removes the home-upload-bandwidth ceiling entirely.

Skipping straight to step 2 or 3 is reasonable if step 1's limitations (no Docker, Android process kill, thermal throttling) cost more setup time than they save in money.

---

## 10. Items Needing Live Verification Before Acting

- Current Raspberry Pi 4/5 and SBC pricing (listed above is approximate).
- Redmi Note 12 exact USB-C OTG host-mode and power-delivery spec (affects SSD viability).
- Home ISP (Orange/Zeop/SFR Réunion, etc.) residential ToS on running servers, and whether the connection sits behind CGNAT.
- n8n's current license terms (Sustainable Use License or successor) for your exact use case.
- Oracle Cloud / Google Cloud / other free-tier current limits and regional availability.
- Anti-spam regulation applicable to unsolicited press/publisher outreach (French + EU + any US recipients).

None of the above should be treated as settled until checked — flagged per the zero-fabrication standard already in use across your other documentation.
