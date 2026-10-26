---
name: security-audit
description: Security vulnerability scanner and auditor for codebases. Use when asked to scan code for security vulnerabilities, find bugs, check for SQL injection, XSS, command injection, exposed API keys, hardcoded secrets, insecure dependencies, access control issues, weak cryptography, or any request like "is my code secure?", "review for security issues", "audit this codebase", "check for vulnerabilities", or "scan this for secrets". Covers OWASP Top 10, CWE Top 25, secrets detection, dependency auditing, and cross-file data flow analysis across JavaScript, TypeScript, Python, Java, PHP, Go, Ruby, and Rust.
license: MIT
compatibility: Requires git; optional scanners (gitleaks, semgrep, npm audit, pip-audit) enhance detection
metadata:
  author: debug-audit-skills
  version: "1.0.0"
---

# Security Audit

An AI-powered security scanner that reasons about your codebase the way a human security researcher would — tracing data flows, understanding component interactions, and catching vulnerabilities that pattern-matching tools miss.

## When to Use This Skill

Use this skill when the request involves:
- Scanning a codebase or file for security vulnerabilities
- Running a security review or vulnerability check
- Checking for SQL injection, XSS, command injection, or other injection flaws
- Finding exposed API keys, hardcoded secrets, or credentials in code
- Auditing dependencies for known CVEs
- Reviewing authentication, authorization, or access control logic
- Detecting insecure cryptography or weak randomness
- Performing a data flow analysis to trace user input to dangerous sinks
- Any request phrasing like "is my code secure?", "scan this file", "check my repo for vulnerabilities"
- Running `/security-audit` or `/security-audit <path>`

## How This Skill Works

Unlike traditional static analysis tools that match patterns, this skill:
1. **Reads code like a security researcher** — understanding context, intent, and data flow
2. **Traces across files** — following how user input moves through your application
3. **Self-verifies findings** — re-examines each result to filter false positives
4. **Assigns severity ratings** — CRITICAL / HIGH / MEDIUM / LOW / INFO
5. **Proposes targeted patches** — every finding includes a concrete fix
6. **Requires human approval** — nothing is auto-applied; you always review first

## Execution Workflow

Follow these steps **in order** every time:

### Step 1 — Scope Resolution

Determine what to scan:
- If a path was provided (`/security-audit src/auth/`), scan only that scope
- If no path given, scan the **entire project** starting from the root
- Identify the language(s) and framework(s) in use (check package.json, requirements.txt, go.mod, Cargo.toml, pom.xml, Gemfile, composer.json, etc.)

### Step 2 — Dependency Audit

Before scanning source code, audit dependencies first (fast wins):
- **Node.js**: Check `package.json` + `package-lock.json` for known vulnerable packages
- **Python**: Check `requirements.txt` / `pyproject.toml` / `Pipfile`
- **Java**: Check `pom.xml` / `build.gradle`
- **Ruby**: Check `Gemfile.lock`
- **Rust**: Check `Cargo.toml`
- **Go**: Check `go.sum`

Run available audit tools:
```bash
# Node.js
npm audit --json 2>/dev/null || true

# Python
pip-audit 2>/dev/null || safety check 2>/dev/null || true

# Rust
cargo audit 2>/dev/null || true

# Go
govulncheck ./... 2>/dev/null || true
```

Flag packages with known CVEs, deprecated crypto libs, or suspiciously old pinned versions.

### Step 3 — Secrets & Exposure Scan

Scan ALL files (including config, env, CI/CD, Dockerfiles, IaC) for:
- Hardcoded API keys, tokens, passwords, private keys
- `.env` files accidentally committed
- Secrets in comments or debug logs
- Cloud credentials (AWS, GCP, Azure, Stripe, Twilio, etc.)
- Database connection strings with credentials embedded
- Private keys (BEGIN RSA/PRIVATE KEY, etc.)

Run available scanners:
```bash
# gitleaks (if installed)
gitleaks detect --source . --no-git --report-format json 2>/dev/null || true

# trufflehog (if installed)
trufflehog filesystem . --no-verification --json 2>/dev/null || true

# Basic grep for common patterns
grep -rEn '(api[_-]?key|secret|password|token|private[_-]?key)\s*[=:]\s*["'"'"'][^"'"'"']{8,}' --include='*.js' --include='*.ts' --include='*.py' --include='*.java' --include='*.go' --include='*.rb' --include='*.php' --include='*.env' --include='*.yml' --include='*.yaml' --include='*.json' . 2>/dev/null | grep -v node_modules | grep -v '.git/' || true
```

Check `.gitignore` covers: `.env`, `.env.*`, `*.pem`, `*.key`, `credentials*`, `secrets*`

### Step 4 — Vulnerability Deep Scan

This is the core scan. Reason about the code — don't just pattern-match.

**Injection Flaws**
- SQL Injection: raw queries with string interpolation, ORM misuse, second-order SQLi
- XSS: unescaped output, dangerouslySetInnerHTML, innerHTML, template injection
- Command Injection: exec/spawn/system with user input
- LDAP, XPath, Header, Log injection
- NoSQL injection (MongoDB $where, $ne, etc.)

**Authentication & Access Control**
- Missing authentication on sensitive endpoints
- Broken object-level authorization (BOLA/IDOR)
- JWT weaknesses (alg:none, weak secrets, no expiry validation)
- Session fixation, missing CSRF protection
- Privilege escalation paths
- Mass assignment / parameter pollution
- Missing rate limiting on auth endpoints

**Data Handling**
- Sensitive data in logs, error messages, or API responses
- Missing encryption at rest or in transit
- Insecure deserialization
- Path traversal / directory traversal
- XXE (XML External Entity) processing
- SSRF (Server-Side Request Forgery)

**Cryptography**
- Use of MD5, SHA1, DES for security purposes
- Hardcoded IVs or salts
- Weak random number generation (Math.random() for tokens)
- Missing TLS certificate validation
- ECB mode encryption

**Business Logic**
- Race conditions (TOCTOU)
- Integer overflow in financial calculations
- Missing rate limiting on sensitive endpoints
- Predictable resource identifiers
- Negative amount handling in financial transactions

**Infrastructure & Config**
- Debug mode left on in production
- Permissive CORS (Access-Control-Allow-Origin: *)
- Missing security headers (CSP, HSTS, X-Frame-Options)
- Insecure cookie settings (no HttpOnly, no Secure, no SameSite)
- Exposed admin interfaces
- Verbose error messages in production

### Step 5 — Cross-File Data Flow Analysis

After the per-file scan, perform a **holistic review**:
- Trace user-controlled input from entry points (HTTP params, headers, body, file uploads) all the way to sinks (DB queries, exec calls, HTML output, file writes)
- Identify vulnerabilities that only appear when looking at multiple files together
- Check for insecure trust boundaries between services or modules

### Step 6 — Self-Verification Pass

For EACH finding:
1. Re-read the relevant code with fresh eyes
2. Ask: "Is this actually exploitable, or is there sanitization I missed?"
3. Check if a framework or middleware already handles this upstream
4. Downgrade or discard findings that aren't genuine vulnerabilities
5. Assign final severity: CRITICAL / HIGH / MEDIUM / LOW / INFO

### Step 7 — Generate Security Report

Output the full report in the format below.

### Step 8 — Propose Patches

For every CRITICAL and HIGH finding, generate a concrete patch:
- Show the vulnerable code (before)
- Show the fixed code (after)
- Explain what changed and why
- Preserve the original code style, variable names, and structure

Explicitly state: **"Review each patch before applying. Nothing has been changed yet."**

## Severity Guide

| Severity | Meaning | Example |
|----------|---------|---------|
| CRITICAL | Immediate exploitation risk, data breach likely | SQLi, RCE, auth bypass, exposed secrets |
| HIGH | Serious vulnerability, exploit path exists | XSS, IDOR, hardcoded credentials, SSRF |
| MEDIUM | Exploitable with conditions or chaining | CSRF, open redirect, weak crypto, info disclosure |
| LOW | Best practice violation, low direct risk | Verbose errors, missing headers, outdated non-vulnerable deps |
| INFO | Observation worth noting, not a vulnerability | Outdated dependency (no CVE), code smell with security implications |

## Output Format

```markdown
## Security Audit Report

**Scope:** [files/directories scanned]
**Languages:** [detected languages/frameworks]
**Date:** [date]

### Summary
| Severity | Count |
|----------|-------|
| CRITICAL | X |
| HIGH | Y |
| MEDIUM | Z |
| LOW | W |
| INFO | V |

### CRITICAL Findings
#### 1. [Title]
- **Location:** `path/to/file.ts:42`
- **Category:** [Injection/Auth/Data Exposure/etc.]
- **CWE:** [CWE-XXX]
- **Confidence:** High/Medium/Low
- **Description:** [What the vulnerability is]
- **Risk:** [What an attacker could do]
- **Evidence:** [Code snippet]
- **Fix:** [Recommended fix with code]

### HIGH Findings
[...]

### MEDIUM Findings
[...]

### LOW Findings
[...]

### Dependency Audit
| Package | Version | Vulnerability | Severity | Fixed In |
|---------|---------|--------------|----------|----------|

### Secrets Scan
| File | Line | Type | Action |
|------|------|------|--------|

### Proposed Patches
[Before/after code for CRITICAL and HIGH findings]

**Review each patch before applying. Nothing has been changed yet.**
```

## Output Rules

- **Always** produce a findings summary table first (counts by severity)
- **Never** auto-apply any patch — present patches for human review only
- **Always** include a confidence rating per finding (High / Medium / Low)
- **Group findings** by category, not by file
- **Be specific** — include file path, line number, and the exact vulnerable code snippet
- **Explain the risk** in plain English — what could an attacker do with this?
- If the codebase is clean, say so clearly: "No vulnerabilities found" with what was scanned

## Language-Specific Patterns

### JavaScript/TypeScript
- `eval()`, `new Function()` with user input
- `child_process.exec()` with string concatenation
- `dangerouslySetInnerHTML` in React
- `innerHTML`, `document.write()`
- `JSON.parse()` on untrusted data without validation
- Prototype pollution (`__proto__`, `constructor.prototype`)
- ReDoS (catastrophic regex backtracking)

### Python
- `eval()`, `exec()` with user input
- `pickle.loads()` on untrusted data
- `os.system()`, `subprocess.call(shell=True)`
- SQL string formatting (`%`, `.format()`, f-strings in queries)
- `yaml.load()` without `SafeLoader`
- Jinja2 `autoescape=False`

### Java
- `Runtime.exec()` with string concatenation
- `ObjectInputStream.readObject()` on untrusted data
- SQL string concatenation
- `MessageDigest.getInstance("MD5")` or `"SHA-1"` for security
- XML parsers without XXE protection

### Go
- `os/exec.Command()` with user input in args
- `template.HTML()` without escaping
- SQL string concatenation
- `math/rand` for security purposes

### PHP
- `eval()`, `system()`, `exec()`, `shell_exec()`
- `unserialize()` on untrusted data
- SQL string concatenation
- `include`/`require` with user input (LFI/RFI)

### Ruby
- `eval()`, `system()`, backticks with user input
- `Marshal.load()` on untrusted data
- SQL string interpolation
- `YAML.load()` (use `YAML.safe_load()`)

### Rust
- `std::process::Command` with untrusted input
- `unsafe` blocks without justification
- Integer overflow in release mode (wrapping)

## Reference Files

- [references/owasp-top10.md](references/owasp-top10.md) — OWASP Top 10 detailed checklist
- [references/secret-patterns.md](references/secret-patterns.md) — Regex patterns and entropy heuristics for secret detection
- [references/language-patterns.md](references/language-patterns.md) — Framework-specific vulnerability patterns
- [references/vulnerable-packages.md](references/vulnerable-packages.md) — Curated CVE watchlist
- [references/report-template.md](references/report-template.md) — Structured report template
