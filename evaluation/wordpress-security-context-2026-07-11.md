# Indexed Message: Security Warning, Site Credentials Context & Audit Request

**Source**: User-provided message in conversation dated ~2026-07-11  
**Purpose of Index**: Structured, redacted reference for WORKFLOW_SUMMARY.md and future secure operations. All secrets redacted per governance rules (no plaintext credentials in chat transcripts or documents).  
**Date Indexed**: 2026-07-11  
**Status**: High-severity security incident flagged in source message itself.

## 1. Core Request
- "Just index the message below. Audit each plugin and page and post of my wordpress website www.sourovdeb.com"
- Read and use provided MCP server definitions (Hostinger API MCPs for hosting, domains, DNS, billing, reach).
- Also provided: developers.hostinger.com link, specific API token (redacted), phpMyAdmin link for db u839078121_rUgwv, MySQL details.

## 2. Site & Infrastructure Details (Confirmed from Message)
- **Domain**: sourovdeb.com (canonical www.sourovdeb.com with 301 redirect)
- **Hosting**: Hostinger
- **IP**: 92.249.46.84
- **FTP**: ftp.sourovdeb.com / u839078121.sourov / base /public_html/
- **MySQL Database**: u839078121_rUgwv (91 MB as of message)
- **MySQL User**: u839078121_gVGpV (created 2026-04-06)
- **phpMyAdmin Access**: https://auth-db2209.hstgr.io/index.php?db=u839078121_rUgwv (user provided link; password never shared in chat)

## 3. Authentication & Endpoints (Redacted Values)
### REST API (Custom)
- Endpoint base: https://www.sourovdeb.com/wp-json/sourov/v1/
- Key Header: X-Sourov-Key (value redacted; flagged for rotation)
- Endpoints listed:
  - POST /ai-post : Create or schedule a post
  - GET /drafts : List draft posts (paginated)
  - POST /schedule-drafts : Schedule drafts in batches
  - GET /scheduled : List scheduled/future posts
  - GET /status : Health check + post counts
  - POST /bulk : Bulk create posts (JSON array)
  - DELETE /post/{id} : Delete post by ID

### Deploy Gateway
- https://www.sourovdeb.com/deploy.php?key=... (key redacted)
- Actions: status, upload, download, list, delete, logs, phpinfo, deploy_zip, write_env

### Secret API Key (Alternative to App Password)
- Value redacted in this index. Used for X-Sourov-Key and deploy.php.

## 4. MCP Server Configurations Provided
- JSON block for mcpServers: hostinger-hosting, hostinger-domains, hostinger-dns, hostinger-billing, hostinger-reach
- All use npx --package=hostinger-api-mcp@latest ... with HOSTINGER_API_TOKEN (placeholder in message, actual token later provided and redacted here)
- Note: This config is for external MCP clients (e.g. Claude Desktop). Not directly launchable or usable from this environment's tool registry. No matching Hostinger MCP connector available in current tools.

## 5. Security Warning & Governance Conflict (Direct from Source Message)
**Critical Flag**: Message contained live secrets in plaintext — a Hostinger API token, a phpMyAdmin database name/user, and a WordPress Secret API Key. This conflicted directly with governance rule INC2671905 (no credentials outside PropertiesService/env vars).

**Action Required (Source Message)**:
1. Rotate the Hostinger API token now (hPanel → API tokens → revoke the specific token, issue new one).
2. Rotate the WordPress X-Sourov-Key / Secret API Key immediately (second priority per prior memory).
3. Do not paste the MySQL password anywhere (it was not provided; correct practice).
4. Do not use the pasted token or key to make any live calls. Using now-exposed secrets to authenticate is bad practice even if you own the site.

**What Can Be Done Publicly (Source Advice)**:
- Pull public data via standard WP REST API (/wp-json/wp/v2/posts, /pages, /media) — no auth needed for published content.
- Plugin audit requires wp-admin or authenticated REST; cannot be done without credential, and will not accept inline in chat.
- Suggestion: Once rotated, set up proper skill file (SKILL_wordpress_admin.md) that reads key from secure PropertiesService-style storage — never inline.

**Governance Alignment**: This index strictly follows the rule. No credential values appear here or in any generated artifact.

## 6. Additional Context from Message
- "Stop. Before anything else..." section emphasizes immediate rotation over any audit or publishing work.
- User may work from sourovdeb.is@gmail.com or connected Google/GitHub accounts.
- Preference: Upload all outputs to Google Drive and GitHub.
- Workflow reference: WORKFLOW_SUMMARY.md (WordPress management on sourovdeb.com via custom REST + deploy.php + FTP).

## 7. Changes & Notes for WORKFLOW_SUMMARY.md Update
- Nothing is fixed: Custom endpoint /wp-json/sourov/v1/status currently returns 404 (public test). May indicate plugin deactivation, route change, or auth enforcement update.
- ELT365 series is actively publishing daily (very recent posts on 2026-07-11).
- Public site remains focused on ELT content; personal/mental health/journal content lives in Pages.
- Recommendation: After rotation, re-verify all custom endpoints with new key via secure skill.

**End of Indexed Message**. All sensitive values redacted. Original message treated as high-severity input per Rigorous Execution Framework.