# Severity Classification Guide

## CRITICAL — Block Merge

Will cause data loss, security breach, or production outage.

**Examples:**
- SQL injection vulnerability
- Authentication bypass
- Data corruption or loss
- Remote code execution
- Exposed secrets/credentials in code
- Race condition causing data corruption
- Missing authorization on sensitive endpoint

**Action:** Must fix before merge. No exceptions.

---

## HIGH — Fix or Accept Risk

Serious bug, security vulnerability, or significant performance issue.

**Examples:**
- XSS vulnerability
- IDOR (Insecure Direct Object Reference)
- Null pointer dereference on common path
- Memory leak
- N+1 query on critical path
- Missing input validation on public API
- Weak cryptography (MD5/SHA1 for security)

**Action:** Fix before merge, or explicitly accept risk with written justification.

---

## MEDIUM — Should Fix

Likely to cause bugs in edge cases, degrade performance, or confuse future maintainers.

**Examples:**
- Missing error handling on non-critical path
- Code duplication
- Overly complex function (high cyclomatic complexity)
- Missing pagination on list endpoint
- Inconsistent naming
- Missing type safety (gratuitous `any`)
- Test gaps for edge cases

**Action:** Should fix before merge. Can defer with tracking issue.

---

## LOW — Nice to Fix

Style issue, minor improvement opportunity, or documentation gap.

**Examples:**
- Formatting inconsistency
- Missing JSDoc/docstring
- Variable could have better name
- Comment is redundant
- Import ordering
- Minor refactoring opportunity

**Action:** Author's discretion. Nice to fix but not required.

---

## Promotion Rules

- A finding flagged by **2+ personas** is promoted one level
- A finding that is both a correctness issue AND a security issue is promoted one level
- A finding on a critical path (auth, payment, data integrity) is promoted one level

## Demotion Rules

- If framework/middleware already handles the issue, demote one level
- If the code path is unreachable in practice, demote one level
- If the issue requires multiple unlikely conditions to trigger, demote one level
