---
name: dev-cycle
description: Complete development cycle workflow — plan, implement, review, QA, and ship. Use when starting a new feature, bug fix, or refactoring task. Use when you want a disciplined, gated development process that catches bugs before they ship. Guides the agent through alignment on a plan, implementation, up to 3 review rounds, QA verification, and final sign-off. Use when asked to "build X", "implement Y", "fix Z properly", or when starting any non-trivial code change.
license: MIT
compatibility: Requires git; uses code-review, security-audit, qa-verify, and debug-cycle skills
metadata:
  author: debug-audit-skills
  version: "1.0.0"
---

# Dev Cycle: Plan → Implement → Review → QA → Ship

## Overview

A disciplined development cycle that forces alignment before coding, adversarial review before merge, and QA verification before ship. Based on the proven gdev_cycle pattern: forcing the agent through a review cycle and a clear QA activity gets much closer to the end result.

**Core principle:** No code ships without review + QA. A clean review is not permission to ship — review + QA together find all bugs.

## When to Use

- Starting any new feature
- Implementing a bug fix (non-trivial)
- Refactoring existing code
- Any change that will be merged to a shared branch
- When asked to "build X properly", "implement Y with tests", "do this right"

## The Development Cycle

```
Phase 1: PLAN       → Align on what to build and how
Phase 2: IMPLEMENT  → Build it with tests
Phase 3: REVIEW     → Adversarial code review (up to 3 rounds)
Phase 4: QA         → End-to-end verification
Phase 5: SHIP       → Commit, push, create PR
```

---

## Phase 1: Plan

**Goal:** Align on the approach before writing any code.

### 1.1 Understand the Task
- What is the user asking for?
- What problem does this solve?
- What are the acceptance criteria?
- What are the constraints (time, compatibility, performance)?

### 1.2 Explore the Codebase
- Find relevant existing code (similar features, patterns, utilities)
- Identify where the change should go
- Understand the existing architecture and conventions
- Check for related tests, configs, and documentation

### 1.3 Design the Solution
- Propose the approach (data flow, components, APIs)
- Identify files that will be created or modified
- Identify potential risks and edge cases
- Consider security implications

### 1.4 Write the Plan
Present a structured plan:

```markdown
## Implementation Plan

### Goal
[One sentence: what we're building]

### Approach
[High-level approach — 2-3 sentences]

### Files to Change
| File | Change | Type |
|------|--------|------|
| src/foo.ts | Add bar() function | New |
| src/foo.test.ts | Add tests for bar() | New |
| src/index.ts | Export bar | Modify |

### Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Edge Cases
- [Edge case 1] → [How to handle]
- [Edge case 2] → [How to handle]

### Risks
- [Risk 1] → [Mitigation]

### Tests
- [Test 1: what it verifies]
- [Test 2: what it verifies]
```

### 1.5 Gate: Plan Approval
**STOP.** Present the plan to the user. Do not proceed to implementation until the plan is approved.

Ask: "Does this plan look right? Any changes before I start implementing?"

---

## Phase 2: Implement

**Goal:** Build the solution with tests.

### 2.1 Write Tests First (TDD when practical)
- Write failing tests that describe the expected behavior
- Tests should cover: happy path, edge cases, error cases

### 2.2 Implement the Change
- Make the smallest change that satisfies the tests
- Follow existing code patterns and conventions
- No unrelated refactoring ("while I'm here" changes)
- No premature optimization

### 2.3 Self-Review Before Submitting
Before moving to formal review, do a quick self-check:
- [ ] Code does what the plan says
- [ ] Tests pass
- [ ] No debug code, console.logs, or commented-out code
- [ ] No hardcoded values that should be configurable
- [ ] Error paths are handled
- [ ] Types are correct (no `any` without justification)

### 2.4 Run the Build
```bash
# Verify everything compiles/builds
npm run build 2>/dev/null || true
npm test 2>/dev/null || true
npm run lint 2>/dev/null || true
```

- [ ] Build succeeds
- [ ] All tests pass
- [ ] Lint passes

---

## Phase 3: Review

**Goal:** Catch bugs through adversarial review. Up to 3 rounds.

### Round 1: Full Adversarial Review

Use the `code-review` skill to perform a full adversarial review:
- Run all five personas (Saboteur, Security Auditor, Performance Reviewer, New Hire, Architect)
- Classify findings by severity (CRITICAL / HIGH / MEDIUM / LOW)
- Determine verdict: BLOCK / CONCERNS / APPROVE

### If Verdict is BLOCK or CONCERNS:

1. Address all CRITICAL and HIGH findings
2. Address MEDIUM findings or justify deferral
3. Re-run tests and build
4. Proceed to Round 2

### Round 2: Focused Re-Review

Re-review only the changes made in response to Round 1:
- Did the fixes introduce new issues?
- Are the original findings resolved?
- Run `code-review` again on the new diff

### If Round 2 finds new CRITICAL/HIGH issues:

1. Address them
2. Proceed to Round 3

### Round 3: Final Review

Final focused review of remaining changes. After this round:
- All CRITICAL and HIGH findings must be resolved
- MEDIUM findings should be resolved or explicitly deferred with justification
- Verdict must be APPROVE or APPROVE WITH CONCERNS

### Security Review

If the change touches security-sensitive code (auth, payments, data access, API endpoints, user input handling):
- Run the `security-audit` skill on the changed files
- Address all CRITICAL and HIGH security findings

### Review Gate

**STOP.** Present the review findings and fixes to the user.

```markdown
## Review Summary

### Round 1 Findings
- CRITICAL: X found, Y fixed
- HIGH: X found, Y fixed
- MEDIUM: X found, Y fixed, Z deferred
- LOW: X found, Y fixed

### Round 2 Findings
[...]

### Security Review
- CRITICAL: X found, Y fixed
- HIGH: X found, Y fixed

### Deferred Items
- [Item] — [Reason for deferral] — [Tracking issue]

### Verdict: APPROVE / APPROVE WITH CONCERNS
```

---

## Phase 4: QA

**Goal:** Verify the change works end-to-end.

Use the `qa-verify` skill to perform comprehensive QA:

### Automated Verification
- [ ] Lint passes
- [ ] Type check passes
- [ ] All tests pass (unit + integration)
- [ ] Build succeeds
- [ ] No new security vulnerabilities
- [ ] Test coverage meets threshold

### Functional Verification
- [ ] Happy path works correctly
- [ ] Edge cases handled
- [ ] Error paths produce appropriate errors
- [ ] No regressions in existing functionality

### Manual Verification
- [ ] UI changes verified visually (if applicable)
- [ ] API changes verified with real requests (if applicable)
- [ ] Documentation is accurate

### QA Gate

**STOP.** Present the QA report.

Verdict must be APPROVED or APPROVED WITH CONCERNS to proceed.

---

## Phase 5: Ship

**Goal:** Commit, push, and create PR.

### 5.1 Prepare the Commit

```bash
# Check what will be committed
git status
git diff --cached
```

Write a clear commit message:
```
<type>: <short description>

<body: what and why, not how>

- Bullet points for key changes
- Reference issue numbers if applicable
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`, `style`

### 5.2 Commit

```bash
git add -A
git commit -m "<message>"
```

### 5.3 Push and Create PR

```bash
git push -u origin <branch>
```

Create PR with description:

```markdown
## Summary
[What this PR does — 2-3 sentences]

## Changes
- [Change 1]
- [Change 2]

## Testing
- [How it was tested]
- [Test results]

## Review & QA
- [x] Code review completed (X rounds)
- [x] Security review completed (if applicable)
- [x] QA verification passed
- [x] All tests pass
- [x] Build succeeds

## Checklist
- [ ] Self-reviewed the code
- [ ] Added/updated tests
- [ ] Updated documentation
- [ ] No breaking changes (or migration guide included)
```

### 5.4 Final Report

```markdown
## Dev Cycle Complete

### What Was Built
[Summary]

### Cycle Summary
| Phase | Status | Details |
|-------|--------|---------|
| Plan | ✅ | Approved with [X] changes |
| Implement | ✅ | [N] files changed, [M] tests added |
| Review | ✅ | [R] rounds, [F] findings, all resolved |
| QA | ✅ | All checks passed |
| Ship | ✅ | PR created: [URL] |

### Metrics
- Lines changed: +X / -Y
- Tests added: N
- Review rounds: R
- Findings resolved: F

### PR Link
[URL]
```

---

## Debugging During the Cycle

If any phase encounters a bug, test failure, or unexpected behavior:
- Use the `debug-cycle` skill for systematic root-cause debugging
- Do NOT skip the debugging process — find the root cause first
- After fixing, return to the phase where the issue was found

## Cycle Rules

1. **Never skip the plan phase** — alignment prevents rework
2. **Never skip review** — self-review bias is real
3. **Never skip QA** — review catches code issues, QA catches behavioral issues
4. **Maximum 3 review rounds** — if still finding critical issues after 3 rounds, the architecture needs discussion
5. **No "quick fixes" during review** — every fix gets reviewed
6. **Document deferrals** — "I'll fix it later" must become a tracked issue

## Quick Reference

| Phase | Gate | Skill to Use |
|-------|------|-------------|
| Plan | User approves plan | — |
| Implement | Tests + build pass | — |
| Review | Verdict: APPROVE | `code-review` |
| Security | No CRITICAL/HIGH findings | `security-audit` |
| QA | Verdict: APPROVED | `qa-verify` |
| Ship | PR created | — |
| Debug (any phase) | Root cause found and fixed | `debug-cycle` |
