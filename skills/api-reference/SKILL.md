---
name: api-reference
description: >
  Categorized reference for every external API in this project — France Travail (job search),
  WordPress and Ghost (publishing), Legifrance/PISTE (legal research), CORE (academic research),
  ESCO (EU occupation/skills, no auth). Trigger when building or editing automation scripts
  (Google Apps Script, WordPress deploy, research workflows) that call any of these services, or
  when asked "what API do I use for X." Contains NO credential values — those live only in
  PropertiesService / the service's own admin panel / a local-only file outside this skill,
  per the project's never-commit-secrets rule (origin: incident INC2671905).
---

# API Reference — Job Search, Publishing, Legal & Academic Research

Source basis: user-provided dashboard text (this conversation, 27 Jun 2026), classified DOCUMENTED.
No live verification performed — this sandbox's network is restricted to code/package registries
(no route to francetravail.io, sourovdeb.com, ghost.io, piste.gouv.fr, core.ac.uk, ec.europa.eu).
Confirm against each provider's dashboard before relying on rate limits/scopes below.

---

## PART 1 — PRIVATE / AUTHENTICATED (credentials required, never hardcode)

### A. France Travail — Emploi Store (job search & labor data)
Org: France Travail (French public employment service). App: `Automation_de_recherche_demploi`.
Use for: `france_travail_job_collector.gs` job-lead search, labor stats, ROME occupation context, La Bonne Boite.

| API | Version | Rate limit | Use |
|---|---|---|---|
| Offres d'emploi | v2 | 10/s | Job listings |
| Open Formation | v1 | 10/s | Training offers |
| Informations sur un territoire | v1 | 10/s | Territorial labor data |
| Marché du travail | v1 | 10/s | Labor indicators |
| Accès à l'emploi des demandeurs d'emploi | v1 | 10/s | Jobseeker pathway metrics |
| ROME 4.0 – Contextes de travail | v1 | 1/s | Occupation/skills context |
| La Bonne Boite | v2 | 2/s | Company hiring-potential match |

Setup: OAuth2 client_credentials → `https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=%2Fpartenaire`.
`client_id` is non-secret (lives in `CONFIG.FT_CLIENT_ID`). `client_secret` and `scope` → `PropertiesService` keys
`FT_CLIENT_SECRET` / `FT_SCOPE` via `setup_OnceOnly_()`, literal deleted after first save.
Current client_id expires **24/07/2026** — renew before then.

### B. WordPress — sourovdeb.com (primary publishing)
Org: self-hosted (Hostinger), custom theme `sourov`. Use for: blog posts, research-paper summaries,
ELT365 content, draft-first publishing, deploy/file ops, search-engine indexing.

| Component | Endpoint / detail |
|---|---|
| REST publish | `POST https://www.sourovdeb.com/wp-json/sourov/v1/ai-post` (+ `/scheduled`, `/bulk`, `DELETE /post/{id}`) |
| Status (public) | `GET https://www.sourovdeb.com/wp-json/sourov/v1/status` |
| Deploy gateway | `https://www.sourovdeb.com/deploy.php` — status/upload/download/list/delete/logs/phpinfo/deploy_zip/write_env |
| FTP | host `ftp.sourovdeb.com`, base `/public_html/` |
| IndexNow | key file served at `/{key}.txt` (Bing/Yandex) |
| Doc root | `/home/u839078121/domains/sourovdeb.com/public_html` |

Auth: header `X-Sourov-Key` (REST + deploy.php). Always call via `www.sourovdeb.com` (canonical redirect).
Default publish status: draft; probe `GET /status` before any write. WP-Cron disabled — hPanel cron handles schedule.
**Flag**: this key is already on record as previously exposed in project files — see local credentials file, rotate.

### C. Ghost — sourovdeb.ghost.io (secondary publishing / newsletter)
Org: Ghost (open-source CMS), instance `objective-publishing-ghost`. Use for: content stream parallel to
WordPress, member/newsletter management. Components: Content API (read-only published content), Admin API
(full read/write — highest-sensitivity credential in this set). Docs: https://ghost.org/docs/
Credential location: Ghost Admin → Integrations → `objective-publishing-ghost`.

### D. Legifrance via PISTE (French legal/regulatory research)
Org: French government (DILA), via piste.gouv.fr. Use for: citing exact statute/article text in
Ofqual / Défenseur des droits / CNIL / Equality Act correspondence — your evidence standard requires
legal claims cite the specific statute.
Setup: OAuth2 Client Credentials, app type Public (no client secret used). API Key + OAuth Client ID
created 25/06/2026; JS origin `*`, redirect `https://piste.gouv.fr/cb`. Docs: Swagger inside portal post-login.
Note: the API-Key *secret string* (behind "View secret") was never pasted — keep it that way; only the
key ID and client ID (not secrets by PISTE's own design for Public apps) are on record.

### E. CORE API (academic research)
Org: CORE (Open University / Jisc, UK) — open-access research aggregator.
Use for: literature sourcing for "Disclosure Without Demand" (target: Studies in Continuing Education)
and JEFL paper corrections. Docs: https://api.core.ac.uk/docs/v3
Credential location: personal key, store via `PropertiesService` (GAS) or local env var if used outside GAS.

---

## PART 2 — PUBLIC / NO AUTH REQUIRED

### F. ESCO API (EU)
Org: European Commission. Use for: standardized occupation/skill matching (CV ↔ "formateur anglais" /
"English teacher" taxonomy alignment). No key.
Base: `https://ec.europa.eu/esco/api` · Example: `?text=English+teacher&type=occupation`
(French: `text=formateur+anglais`). Docs: https://ec.europa.eu/esco/api/doc/esco_api_doc.html

### G. Candidate future additions — NOT BUILT, flag before adding
Relevant to the project's research-paper / blog / YouTube expansion, all free or free-tier, no key
or self-serve key (verify current terms before integrating — not yet checked this session):
- **OpenAlex / Crossref / Semantic Scholar** — academic citation lookup for both pending papers
- **YouTube Data API v3** — once channel identity is confirmed (Google Cloud Console, OAuth)
- **DeepL API** — FR/EN translation QA for formal correspondence and bilingual content
`free-apis.github.io` was checked this session and is blocked by current network allowlist (403);
the GitHub repo backing a similarly-named directory (`zhaotoday/free-apis`) is a Chinese-language
consumer-API catalogue (Baidu/Taobao/WeChat-class services) — not relevant to this project's subjects,
nothing imported from it.

---

## Carry-over conventions for any script touching these APIs
- No Google Sheets read-back for logic (Sheets, if present at all, is write-only display)
- All secrets via `PropertiesService`; `setup_OnceOnly_()` pattern, delete literal after first save
- `DRY_RUN` defaults `true`; no auto-send, no auto-publish
- Never commit a literal secret to GitHub (origin: INC2671905)

## Where the actual key values are
Not in this skill. See the local-only credentials file generated alongside this skill — that file is
explicitly excluded from GitHub and from anything meant to be shared or re-pasted elsewhere.
