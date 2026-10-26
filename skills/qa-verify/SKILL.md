---
name: qa-verify
description: QA verification and sign-off process before shipping code. Use when you need to verify a change is ready for production, before merging a PR, before deploying, or when asked to "verify this works", "QA this change", "is this ready to ship?", "run the QA checklist". Validates tests, build, manual verification, documentation, and produces a sign-off report.
license: MIT
compatibility: Requires git and the project's test/build commands
metadata:
  author: debug-audit-skills
  version: "1.0.0"
---

# QA Verify: Pre-Ship Verification and Sign-Off

## Overview

A comprehensive QA verification process that validates a change is ready for production. Catches issues that code review might miss by focusing on end-to-end verification, not just code inspection. Produces a clear sign-off or block report.

**Key principle:** A clean code review is NOT permission to ship. Review + QA together find all bugs.

## When to Use

- Before merging any PR to main
- Before deploying to production
- After completing a feature
- When asked to "verify this", "QA this", "is this ready?", "check if this works"
- After a bug fix (verify the fix actually works end-to-end)
- Before a release

## The QA Verification Process

### Phase 1: Automated Verification

Run all automated checks in order. Any failure blocks sign-off.

#### 1.1 Code Quality Gates
```bash
# Linting
npm run lint 2>/dev/null || true

# Type checking
npm run typecheck 2>/dev/null || npx tsc --noEmit 2>/dev/null || true

# Formatting check
npm run format:check 2>/dev/null || npx prettier --check . 2>/dev/null || true
```

- [ ] Lint passes with zero errors
- [ ] Type checking passes with zero errors
- [ ] Code is properly formatted

#### 1.2 Test Suite
```bash
# Run the full test suite
npm test 2>/dev/null || npm run test 2>/dev/null || true

# Run with coverage if available
npm run test:coverage 2>/dev/null || true
```

- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] No tests are skipped without justification
- [ ] Test coverage meets project threshold
- [ ] New code has corresponding tests

#### 1.3 Build Verification
```bash
# Production build
npm run build 2>/dev/null || true
```

- [ ] Production build succeeds
- [ ] Build output size is reasonable (no unexpected bloat)
- [ ] No build warnings that indicate problems

#### 1.4 Security Checks
```bash
# Dependency audit
npm audit --audit-level=high 2>/dev/null || true

# Check for secrets in recent changes
git diff HEAD~1 -- . | grep -iE '(api[_-]?key|secret|password|token)\s*[=:]' || true
```

- [ ] No new high/critical dependency vulnerabilities
- [ ] No secrets in code or recent commits
- [ ] `.env` files are not committed

### Phase 2: Functional Verification

Verify the change actually works as intended.

#### 2.1 Understand the Change
- What is this change supposed to do?
- What is the expected behavior?
- What are the edge cases?

#### 2.2 Test the Happy Path
- [ ] The primary use case works correctly
- [ ] Expected outputs match actual outputs
- [ ] UI renders correctly (if applicable)
- [ ] API returns expected responses

#### 2.3 Test Edge Cases
- [ ] Empty/null inputs handled gracefully
- [ ] Boundary values work correctly
- [ ] Error cases produce appropriate errors
- [ ] Large inputs don't cause performance issues
- [ ] Concurrent access is safe (if applicable)

#### 2.4 Test Error Paths
- [ ] Invalid input is rejected with clear error messages
- [ ] Network failures are handled gracefully
- [ ] Timeouts don't leave the system in a bad state
- [ ] Error messages don't leak sensitive information

#### 2.5 Regression Check
- [ ] Existing functionality still works
- [ ] No unrelated features are broken
- [ ] Performance hasn't regressed

### Phase 3: Integration Verification

#### 3.1 API Contract
- [ ] API responses match documented schema
- [ ] HTTP status codes are correct
- [ ] Headers are set correctly (CORS, security headers)
- [ ] Pagination works correctly (if applicable)
- [ ] Rate limiting works (if applicable)

#### 3.2 Database
- [ ] Migrations run successfully
- [ ] Data integrity is maintained
- [ ] Queries are performant (no N+1)
- [ ] Transactions are handled correctly

#### 3.3 External Services
- [ ] Third-party API integrations work
- [ ] Webhook handlers are correct
- [ ] External service failures are handled

### Phase 4: Manual Verification Checklist

For UI changes:
- [ ] Visual appearance is correct across browsers
- [ ] Responsive design works on mobile/tablet/desktop
- [ ] Accessibility: keyboard navigation works
- [ ] Accessibility: screen reader compatible
- [ ] Accessibility: sufficient color contrast
- [ ] Loading states are shown
- [ ] Error states are displayed clearly
- [ ] Empty states are handled

For API changes:
- [ ] Request/response examples in docs are accurate
- [ ] Authentication works as expected
- [ ] Authorization is enforced correctly
- [ ] Input validation is comprehensive

For infrastructure changes:
- [ ] Configuration is environment-appropriate
- [ ] Secrets are properly managed
- [ ] Resource limits are set
- [ ] Monitoring/alerting is in place

### Phase 5: Documentation Verification

- [ ] Code changes are documented (if public API)
- [ ] README is updated (if user-facing change)
- [ ] Changelog is updated
- [ ] Inline comments explain non-obvious logic
- [ ] Migration guide exists (if breaking change)

### Phase 6: Pre-Merge Checklist

- [ ] Branch is up to date with target branch
- [ ] No merge conflicts
- [ ] Commit messages are clear and descriptive
- [ ] No debug code, console.logs, or commented-out code
- [ ] No hardcoded values that should be configurable
- [ ] Feature flags are used for incomplete features

## Sign-Off Report Format

```markdown
## QA Verification Report

**Change:** [PR/change title]
**Branch:** [branch name]
**Reviewer:** [agent/user]
**Date:** [date]

### Automated Checks
| Check | Status | Details |
|-------|--------|---------|
| Lint | ✅/❌ | |
| Type Check | ✅/❌ | |
| Unit Tests | ✅/❌ | X passed, Y failed |
| Integration Tests | ✅/❌ | X passed, Y failed |
| Build | ✅/❌ | |
| Security Scan | ✅/❌ | |
| Coverage | ✅/❌ | X% (threshold: Y%) |

### Functional Verification
| Scenario | Status | Notes |
|----------|--------|-------|
| Happy path | ✅/❌ | |
| Edge cases | ✅/❌ | |
| Error handling | ✅/❌ | |
| Regression check | ✅/❌ | |

### Manual Verification
| Item | Status | Notes |
|------|--------|-------|
| UI/UX (if applicable) | ✅/❌/N/A | |
| API contract | ✅/❌/N/A | |
| Documentation | ✅/❌ | |

### Issues Found
1. [Issue description] — [Severity] — [Blocking?]

### Verdict
**✅ APPROVED** — Ready to merge and deploy.
**⚠️ APPROVED WITH CONCERNS** — Merge with noted follow-ups: [list]
**❌ BLOCKED** — Issues must be resolved before merge: [list]

### Follow-Up Items
- [ ] [Action item] — [Owner] — [Due]
```

## Verdict Definitions

| Verdict | Meaning |
|---------|---------|
| **APPROVED** | All checks pass. Ready to merge and deploy. |
| **APPROVED WITH CONCERNS** | No blockers, but follow-up items should be tracked. Merge is OK. |
| **BLOCKED** | One or more critical issues found. Must be resolved before merge. |

## Common QA Failures

| Failure | Prevention |
|---------|-----------|
| "Works on my machine" | Verify in CI environment, not just local |
| Tests pass but feature is broken | Manual functional verification is mandatory |
| Edge cases not tested | Explicitly test null, empty, boundary, and error cases |
| Performance regression | Run performance-sensitive tests, check bundle size |
| Security issue introduced | Run security audit as part of QA |
| Documentation out of date | Update docs in the same PR as code changes |
| Flaky tests | Fix flakiness, don't ignore it |

## Quick QA Checklist (One-Liner)

```markdown
## QA Checklist
- [ ] Lint passes
- [ ] Types check
- [ ] All tests pass
- [ ] Build succeeds
- [ ] No new security issues
- [ ] Feature works end-to-end
- [ ] Edge cases handled
- [ ] Error paths tested
- [ ] No regressions
- [ ] Docs updated
- [ ] No debug code left
- [ ] Ready to ship
```

## Reference Files

- [references/qa-checklist.md](references/qa-checklist.md) — Printable QA checklist
- [references/test-strategies.md](references/test-strategies.md) — Testing strategies by change type
