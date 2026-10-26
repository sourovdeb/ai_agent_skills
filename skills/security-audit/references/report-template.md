# Security Report Template

Use this template for the final security audit report.

```markdown
## Security Audit Report

**Scope:** [files/directories scanned]
**Languages:** [detected languages/frameworks]
**Date:** [date]
**Scanner:** AI-powered security review

---

### Summary

| Severity | Count |
|----------|-------|
| CRITICAL | 0 |
| HIGH | 0 |
| MEDIUM | 0 |
| LOW | 0 |
| INFO | 0 |

**Overall Risk:** [Low / Medium / High / Critical]

---

### CRITICAL Findings

#### CRIT-001: [Title]
- **Location:** `path/to/file.ts:42`
- **Category:** [Injection / Auth / Data Exposure / Crypto / SSRF]
- **CWE:** [CWE-XXX]
- **OWASP:** [A0X:2021-Category]
- **Confidence:** High / Medium / Low
- **Description:** [What the vulnerability is, in plain English]
- **Risk:** [What an attacker could do with this]
- **Evidence:**
  ```typescript
  // Vulnerable code at path/to/file.ts:42
  const query = `SELECT * FROM users WHERE id = ${userId}`;
  ```
- **Exploitability:** [How easy is it to exploit? What prerequisites?]
- **Fix:**
  ```typescript
  // Fixed code
  const query = 'SELECT * FROM users WHERE id = ?';
  await db.query(query, [userId]);
  ```

---

### HIGH Findings

[Same format as CRITICAL]

---

### MEDIUM Findings

[Same format, less detail]

---

### LOW Findings

[Same format, brief]

---

### INFO Findings

| Location | Observation |
|----------|-------------|
| `file.ts:10` | Outdated dependency (no known CVE) |

---

### Dependency Audit

| Package | Current | Latest | Vulnerability | Severity | Action |
|---------|---------|--------|--------------|----------|--------|
| lodash | 4.17.15 | 4.17.21 | CVE-2019-10744 | High | Update |

**No vulnerable dependencies found** — or list them above.

---

### Secrets Scan

| File | Line | Type | Severity | Action |
|------|------|------|----------|--------|
| `.env.example` | 5 | API Key pattern | LOW | Verify it's a placeholder |

**No hardcoded secrets found** — or list them above.

**Action for found secrets:**
1. Revoke/rotate immediately at the provider
2. Remove from code and git history
3. Use environment variables or secrets manager
4. Add pre-commit hooks to prevent recurrence

---

### Data Flow Analysis

**Entry Points Identified:**
- `POST /api/users` — accepts user registration data
- `GET /api/documents/:id` — accepts document ID

**Sinks Identified:**
- Database queries in `src/db/`
- HTML rendering in `src/views/`
- External API calls in `src/services/`

**Cross-File Vulnerabilities:**
- [Any vulnerability that spans multiple files]

---

### Proposed Patches

#### Patch 1: [Title]
**File:** `path/to/file.ts`

```diff
- const query = `SELECT * FROM users WHERE id = ${userId}`;
+ const query = 'SELECT * FROM users WHERE id = ?';
+ await db.query(query, [userId]);
```

**Explanation:** [Why this fix works]

---

### Verification Checklist

- [ ] All CRITICAL findings addressed
- [ ] All HIGH findings addressed or risk accepted with justification
- [ ] Patches reviewed by human before applying
- [ ] Tests added for security fixes
- [ ] Secrets rotated if any were exposed
- [ ] Dependencies updated

---

### Notes

- [What was NOT scanned — limitations of this audit]
- [Recommendations for further security testing]
- [Security improvements for the future]

---

**Review each patch before applying. Nothing has been changed yet.**
```
