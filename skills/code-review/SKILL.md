---
name: code-review
description: Multi-axis adversarial code review that catches real bugs before they ship. Use when reviewing code changes, pull requests, staged/unstaged changes, commits, or any code before merging. Use when you need to assess code quality across correctness, security, performance, architecture, and readability. Forces perspective shifts through adversarial personas to break self-review bias. Use when asked to "review this code", "check my PR", "is this code good?", or before merging any change.
license: MIT
compatibility: Requires git for diff operations
metadata:
  author: debug-audit-skills
  version: "1.0.0"
---

# Code Review: Multi-Axis Adversarial Review

## Overview

Every change gets reviewed before merge — no exceptions. Review covers five axes: correctness, security, performance, architecture, and readability. Uses adversarial personas to break the self-review monoculture.

**The approval standard:** Approve a change when it definitely improves overall code health, even if it isn't perfect. Perfect code doesn't exist — the goal is continuous improvement. Don't block a change because it isn't exactly how you would have written it.

## When to Use

- Before merging any PR or change
- After completing a feature implementation
- When another agent or model produced code you need to evaluate
- When refactoring existing code
- After any bug fix (review both the fix and the regression test)
- When asked to "review this code", "check my PR", "look at my changes"

## Usage

```
/code-review                    # Review staged + unstaged changes
/code-review --diff HEAD~3      # Review last 3 commits
/code-review --diff main...HEAD # Review PR against main
/code-review --file src/auth.ts # Review a specific file
/code-review focus on security  # Review with specific focus
```

## Review Workflow

### Step 1: Gather the Changes

Determine what to review based on invocation:
- **No arguments:** Run `git diff` (unstaged) + `git diff --cached` (staged). If both empty, run `git diff HEAD~1` (last commit).
- **`--diff <ref>`:** Run `git diff <ref>`
- **`--file <path>`:** Read the entire file. Focus review on the full file rather than just changes.

If no changes are found, stop and report: "Nothing to review."

### Step 2: Read the Full Context

For every file in the diff:
1. Read the **full file** (not just the changed lines) — bugs hide in how new code interacts with existing code.
2. Identify the **purpose** of the change: bug fix, new feature, refactor, config change, test.
3. Note any **project conventions** from AGENTS.md, .editorconfig, linting configs, or existing patterns.

### Step 3: Understand the Context

Before looking at code, understand the intent:
- What is this change trying to accomplish?
- What spec or task does it implement?
- What is the expected behavior change?

### Step 4: Review the Tests First

Tests reveal intent and coverage:
- Do tests exist for the change?
- Do they test behavior (not implementation details)?
- Are edge cases covered?
- Do tests have descriptive names?
- Would the tests catch a regression if the code changed?

### Step 5: Run the Adversarial Personas

Execute each persona sequentially. Each persona MUST produce at least one finding. If a persona finds nothing wrong, it has not looked hard enough — go back and look again.

**IMPORTANT:** Do not soften findings. Do not hedge. Do not say "this might be fine but..." — either it's a problem or it isn't. Be direct.

---

#### Persona 1: The Saboteur

**Mindset:** "I am trying to break this code in production."

**Priorities:**
- Input that was never validated
- State that can become inconsistent
- Concurrent access without synchronization
- Error paths that swallow exceptions or return misleading results
- Assumptions about data format, size, or availability that could be violated
- Off-by-one errors, integer overflow, null/undefined dereferences
- Resource leaks (file handles, connections, subscriptions, listeners)

**Review Process:**
1. For each function/method changed, ask: "What is the worst input I could send this?"
2. For each external call, ask: "What if this fails, times out, or returns garbage?"
3. For each state mutation, ask: "What if this runs twice? Concurrently? Never?"
4. For each conditional, ask: "What if neither branch is correct?"

**You MUST find at least one issue. If the code is genuinely bulletproof, note the most fragile assumption it relies on.**

---

#### Persona 2: The Security Auditor

**Mindset:** "This code will be attacked. My job is to find the vulnerability before an attacker does."

**OWASP-Informed Checklist:**

| Category | What to Look For |
|----------|-----------------|
| **Injection** | SQL, NoSQL, OS command, LDAP — any place user input reaches a query or command without parameterization |
| **Broken Auth** | Hardcoded credentials, missing auth checks on new endpoints, session tokens in URLs or logs |
| **Data Exposure** | Sensitive data in error messages, logs, or API responses; missing encryption at rest or in transit |
| **Insecure Defaults** | Debug mode left on, permissive CORS, wildcard permissions, default passwords |
| **Missing Access Control** | IDOR (can user A access user B's data?), missing role checks, privilege escalation paths |
| **Dependency Risk** | New dependencies with known CVEs, pinned to vulnerable versions, unnecessary transitive dependencies |
| **Secrets** | API keys, tokens, passwords in code, config, or comments — even "temporary" ones |

**Review Process:**
1. Identify every trust boundary the code crosses (user input, API calls, database, file system, environment variables).
2. For each boundary: is input validated? Is output sanitized? Is the principle of least privilege followed?
3. Check: could an authenticated user escalate privileges through this change?
4. Check: does this change expose any new attack surface?

**You MUST find at least one issue. If the code has no security surface, note the closest thing to a security-relevant assumption.**

---

#### Persona 3: The Performance Reviewer

**Mindset:** "This code will run at scale. I need to find the bottleneck before users do."

**Priorities:**
- N+1 query patterns
- Unbounded loops or unconstrained data fetching
- Synchronous operations that should be async
- Unnecessary re-renders in UI components
- Missing pagination on list endpoints
- Large objects created in hot paths
- Missing caching where appropriate
- Memory leaks (unclosed streams, growing arrays)

**Review Process:**
1. Identify the hot path this change affects.
2. Ask: "What happens when this runs 1000x concurrently?"
3. Check: is there unnecessary work in a loop?
4. Check: are resources properly released?

**You MUST find at least one issue. If performance is genuinely fine, note the most likely scaling bottleneck.**

---

#### Persona 4: The New Hire

**Mindset:** "I just joined this team. I need to understand and modify this code in 6 months with zero context from the original author."

**Priorities:**
- Names that don't communicate intent (what does `data` mean? what does `process()` do?)
- Logic that requires reading 3+ other files to understand
- Magic numbers, magic strings, unexplained constants
- Functions doing more than one thing (the name says X but it also does Y and Z)
- Missing type information that forces the reader to trace through call chains
- Inconsistency with surrounding code style or project conventions
- Tests that test implementation details instead of behavior
- Comments that describe *what* (redundant) instead of *why* (useful)

**Review Process:**
1. Read each changed function as if you've never seen the codebase. Can you understand what it does from the name, parameters, and body alone?
2. Trace one code path end-to-end. How many files do you need to open?
3. Check: would a new contributor know where to add a similar feature?
4. Look for "the author knew something the reader won't" — implicit knowledge baked into the code.

**You MUST find at least one issue. If the code is crystal clear, note the most likely point of confusion for a newcomer.**

---

#### Persona 5: The Architect

**Mindset:** "I own this system's long-term health. I need to catch design problems before they become legacy debt."

**Priorities:**
- Does it follow existing patterns or introduce a new one? If new, is it justified?
- Does it maintain clean module boundaries?
- Is there code duplication that should be shared?
- Are dependencies flowing in the right direction (no circular dependencies)?
- Is the abstraction level appropriate (not over-engineered, not too coupled)?
- Does this refactor reduce complexity or just relocate it?
- Is feature-specific logic leaking into a shared or general-purpose module?
- Are type boundaries explicit? Question gratuitous `any`/`unknown`/optional/casts.
- Is a new conditional bolted onto an unrelated flow? That's a design smell.
- Do repeated conditionals on the same shape appear? They signal a missing model or dispatcher.

**Review Process:**
1. Look at the change in the context of the whole system.
2. Ask: "Will this make the next change harder or easier?"
3. Check: does this change reduce the number of concepts a reader must hold?
4. Check: is there a simpler design that achieves the same goal?

**You MUST find at least one issue. If the architecture is sound, note the most likely future maintenance burden.**

### Step 6: Deduplicate and Synthesize

After all personas have reported:
1. Merge duplicate findings (same issue caught by multiple personas).
2. Promote findings caught by 2+ personas to the next severity level.
3. Produce the final structured output.

## Severity Classification

| Severity | Definition | Action Required |
|----------|-----------|-----------------|
| **CRITICAL** | Will cause data loss, security breach, or production outage. Must fix before merge. | Block merge. |
| **HIGH** | Serious bug, security vulnerability, or significant performance issue. Should fix before merge. | Fix or explicitly accept risk with justification. |
| **MEDIUM** | Likely to cause bugs in edge cases, degrade performance, or confuse future maintainers. | Should fix before merge. |
| **LOW** | Style issue, minor improvement opportunity, or documentation gap. | Nice to fix. Author's discretion. |

**Promotion rule:** A finding flagged by 2+ personas is promoted one level.

## The Five-Axis Review Checklist

### 1. Correctness
- Does it match the spec or task requirements?
- Are edge cases handled (null, empty, boundary values)?
- Are error paths handled (not just the happy path)?
- Does it pass all tests? Are the tests actually testing the right things?
- Are there off-by-one errors, race conditions, or state inconsistencies?

### 2. Readability & Simplicity
- Are names descriptive and consistent with project conventions?
- Is the control flow straightforward (avoid nested ternaries, deep callbacks)?
- Is the code organized logically (related code grouped, clear module boundaries)?
- Are there any "clever" tricks that should be simplified?
- Could this be done in fewer lines?
- Are abstractions earning their complexity?
- Are there dead code artifacts: no-op variables, backwards-compat shims, `// removed` comments?

### 3. Architecture
- Does it follow existing patterns or introduce a new one? If new, is it justified?
- Does it maintain clean module boundaries?
- Is there code duplication that should be shared?
- Are dependencies flowing in the right direction?
- Is the abstraction level appropriate?
- Does this refactor reduce complexity or just relocate it?

### 4. Security
- Is user input validated and sanitized?
- Are secrets kept out of code, logs, and version control?
- Is authentication/authorization checked where needed?
- Are SQL queries parameterized (no string concatenation)?
- Are outputs encoded to prevent XSS?
- Are dependencies from trusted sources with no known vulnerabilities?
- Is data from external sources treated as untrusted?

### 5. Performance
- Any N+1 query patterns?
- Any unbounded loops or unconstrained data fetching?
- Any synchronous operations that should be async?
- Any unnecessary re-renders in UI components?
- Any missing pagination on list endpoints?
- Any large objects created in hot paths?

## Output Format

Structure your review as follows:

```markdown
## Code Review: [brief description of what was reviewed]

**Scope:** [files reviewed, lines changed, type of change]
**Verdict:** BLOCK / CONCERNS / APPROVE

### Critical Findings
[If any — these block the merge]

### High Findings
[Should-fix items]

### Medium Findings
[Should-fix before merge]

### Low Findings
[Nice-to-fix items]

### Summary
[2-3 sentences: what's the overall risk profile? What's the single most important thing to fix?]
```

**Verdict definitions:**
- **BLOCK** — 1+ CRITICAL findings. Do not merge until resolved.
- **CONCERNS** — No criticals but 1+ HIGH or 2+ MEDIUM findings. Merge at your own risk.
- **APPROVE** — Only LOW findings or none. Safe to merge.

## Structural Remedies

When you flag a structural problem, propose the move — not just the problem:

- **Replace a chain of conditionals** with a typed model or an explicit dispatcher.
- **Collapse duplicate branches** into a single clearer flow.
- **Separate orchestration from business logic** so each reads on its own.
- **Move feature-specific logic** out of a shared module into the package that owns the concept.
- **Reuse the canonical helper** instead of a bespoke near-duplicate.
- **Make a type boundary explicit** so downstream branching disappears.
- **Delete a pass-through wrapper** that adds indirection without clarifying the API.
- **Extract a helper, or split a large file** into focused modules.

Prefer the remedy that removes moving pieces over one that spreads the same complexity around.

## Anti-Patterns

### What This Review is NOT

| Anti-Pattern | Why It's Wrong |
|-------------|---------------|
| "LGTM, no issues found" | If you found nothing, you didn't look hard enough. Every change has at least one risk, assumption, or improvement opportunity. |
| Cosmetic-only findings | Reporting only whitespace/formatting while missing a null dereference is worse than no review at all. Substance first, style second. |
| Pulling punches | "This might possibly be a minor concern..." — No. Be direct. "This will throw a NullPointerException when `user` is undefined." |
| Restating the diff | "This function was added to handle authentication" is not a finding. What's WRONG with how it handles authentication? |
| Ignoring test gaps | New code without tests is a finding. Always. Tests are not optional. |
| Reviewing only the changed lines | Bugs live in the interaction between new code and existing code. Read the full file. |

### The Self-Review Trap

You are likely reviewing code you just wrote or just read. Your brain formed the same mental model that produced this code. You will naturally think it looks correct because it matches your expectations.

**To break this pattern:**
1. Read the code **bottom-up** (start from the last function, work backward).
2. For each function, state its contract **before** reading the body. Does the body match?
3. Assume every variable could be null/undefined until proven otherwise.
4. Assume every external call will fail.
5. Ask: "If I deleted this change entirely, what would break?" — if the answer is "nothing," the change might be unnecessary.

## Change Sizing

Small, focused changes are easier to review, faster to merge, and safer to deploy:

```
~100 lines changed   → Good. Reviewable in one sitting.
~300 lines changed   → Acceptable if it's a single logical change.
~1000 lines changed  → Too large. Split it.
```

**Watch file size, not just diff size.** A small diff can still push a file past a healthy boundary — around 1000 total lines in a single file is a common inspection signal.

## Honesty in Review

- **Don't rubber-stamp.** "LGTM" without evidence of review helps no one.
- **Don't soften real issues.** "This might be a minor concern" when it's a bug that will hit production is dishonest.
- **Quantify problems when possible.** "This N+1 query will add ~50ms per item" is better than "this could be slow."
- **Push back on approaches with clear problems.** Sycophancy is a failure mode in reviews.
- **Accept override gracefully.** If the author has full context and disagrees, defer to their judgment.

## Red Flags

- PRs merged without any review
- Review that only checks if tests pass (ignoring other axes)
- "LGTM" without evidence of actual review
- Security-sensitive changes without security-focused review
- Large PRs that are "too big to review properly" (split them)
- No regression tests with bug fix PRs
- Review comments without severity labels
- Accepting "I'll fix it later" — it never happens
- A refactor that moves code around without reducing complexity

## Verification

After review is complete:
- [ ] All Critical issues are resolved
- [ ] All High issues are resolved or explicitly deferred with justification
- [ ] Tests pass
- [ ] Build succeeds
- [ ] The verification story is documented

## Reference Files

- [references/review-checklist.md](references/review-checklist.md) — Quick reference checklist
- [references/severity-guide.md](references/severity-guide.md) — Detailed severity classification
- [references/structural-remedies.md](references/structural-remedies.md) — Common structural problems and fixes
