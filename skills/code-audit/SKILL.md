---
name: code-audit
description: Comprehensive code quality audit for entire codebases or specific modules. Use when asked to audit code quality, assess technical debt, evaluate maintainability, check code complexity, find anti-patterns, review architecture health, assess test coverage, identify code smells, measure duplication, or perform a pre-refactoring assessment. Use when you need a holistic view of code health before a major change, migration, or release.
license: MIT
compatibility: Requires git; optional tools (cloc, eslint, pylint, etc.) enhance analysis
metadata:
  author: debug-audit-skills
  version: "1.0.0"
---

# Code Audit: Comprehensive Quality Assessment

## Overview

A holistic code quality audit that assesses the health of a codebase across multiple dimensions: complexity, maintainability, test coverage, duplication, architecture, and adherence to best practices. Produces a prioritized action plan for improvement.

## When to Use

- Before a major refactoring or migration
- When assessing technical debt
- During codebase health checkups
- Before onboarding new team members
- When evaluating whether to adopt or reject a dependency
- After a major release (post-mortem code health check)
- When asked to "audit this codebase", "how healthy is this code?", "find code smells", "assess technical debt"

## Audit Dimensions

### 1. Code Complexity

Measure and flag overly complex code:

**Metrics to assess:**
- Cyclomatic complexity (flag functions with complexity > 10)
- Cognitive complexity (flag functions that are hard to understand)
- Nesting depth (flag > 4 levels of nesting)
- Function/method length (flag > 50 lines)
- File length (flag > 500 lines)
- Parameter count (flag > 4 parameters)

**Run available tools:**
```bash
# JavaScript/TypeScript
npx eslint --format json . 2>/dev/null | jq '[.[] | .messages[] | select(.ruleId == "complexity" or .ruleId == "max-lines" or .ruleId == "max-depth" or .ruleId == "max-params")]' 2>/dev/null || true

# Python
pylint --disable=all --enable=C0301,C0302,R0912,R0915,R0913 --output-format=json . 2>/dev/null || true

# General line counts
find . -type f \( -name '*.js' -o -name '*.ts' -o -name '*.py' -o -name '*.java' -o -name '*.go' -o -name '*.rb' -o -name '*.php' -o -name '*.rs' \) -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/build/*' | xargs wc -l 2>/dev/null | sort -rn | head -30
```

**Complexity red flags:**
- God classes/modules (doing too many things)
- Deep inheritance hierarchies (> 3 levels)
- Long parameter lists (> 4 params — use object parameters)
- Deeply nested conditionals (> 3 levels)
- Large switch/if-else chains (missing polymorphism)

### 2. Code Duplication

Identify duplicated code that should be extracted:

```bash
# Basic duplicate detection (requires jscpd or similar)
npx jscpd . --min-lines 5 --min-tokens 50 2>/dev/null || true

# Manual: search for repeated patterns
grep -rn "function\|const.*=.*=>" --include='*.ts' --include='*.js' src/ | head -50
```

**Duplication red flags:**
- Copy-pasted functions with minor variations
- Repeated business logic across modules
- Duplicate API client code
- Repeated validation logic
- Copy-pasted test setup

### 3. Test Coverage

Assess test health:

```bash
# Run coverage if available
npm test -- --coverage 2>/dev/null || true
npm run test:coverage 2>/dev/null || true
pytest --cov=. --cov-report=term-missing 2>/dev/null || true
```

**Test health checklist:**
- [ ] Tests exist for critical business logic
- [ ] Tests cover edge cases and error paths
- [ ] Tests are not flaky (no timing dependencies)
- [ ] Tests test behavior, not implementation
- [ ] Test names describe what they verify
- [ ] No tests are skipped without a tracking issue
- [ ] Integration tests exist for external dependencies
- [ ] Coverage is above project threshold (typically 80%+)

**Test red flags:**
- Tests that mock everything (testing nothing real)
- Tests with no assertions
- Tests that depend on execution order
- Snapshot tests without review
- Tests that take too long (> 5 minutes for unit tests)

### 4. Architecture Health

Assess structural quality:

**Check for:**
- Circular dependencies between modules
- Violations of project's intended architecture (layered, hexagonal, etc.)
- Feature logic leaking into shared/infrastructure modules
- Tight coupling between unrelated components
- Missing abstractions (repeated patterns that should be extracted)
- God modules (files that import/export too much)

**Dependency analysis:**
```bash
# Check for circular dependencies (Node.js)
npx madge --circular --extensions js,ts src/ 2>/dev/null || true

# General import analysis
grep -rn "^import\|^from\|^require" --include='*.ts' --include='*.js' src/ | wc -l
```

**Architecture red flags:**
- UI components importing directly from database layer
- Business logic in controllers/handlers
- Shared utilities becoming a dumping ground
- Config values hardcoded instead of injected
- No clear module boundaries

### 5. Code Smells

Common code smells to detect:

| Smell | Detection Signal | Severity |
|-------|-----------------|----------|
| Dead code | Unused exports, unreachable branches, commented-out code | Medium |
| Magic numbers | Hardcoded numbers without named constants | Low |
| Long methods | Functions > 50 lines | Medium |
| Large classes | Classes > 300 lines or > 10 methods | Medium |
| Feature envy | Method uses more of another class than its own | Medium |
| Shotgun surgery | One change requires edits in many files | High |
| Divergent change | One class changed for multiple reasons | High |
| Primitive obsession | Using primitives instead of small objects | Low |
| Temporary field | Class field only used in some methods | Low |
| Refused bequest | Subclass doesn't use inherited methods | Medium |

### 6. Error Handling

Assess error handling quality:

**Check for:**
- Swallowed exceptions (empty catch blocks)
- Generic error messages that don't help debugging
- Missing error handling on external calls
- Inconsistent error handling patterns
- Errors that leak sensitive information
- Missing error boundaries (UI)
- No retry logic for transient failures

```bash
# Find empty catch blocks
grep -rn "catch" --include='*.ts' --include='*.js' --include='*.py' --include='*.java' --include='*.go' src/ -A 1 | grep -B 1 "}" | grep "catch" || true

# Find TODO/FIXME/HACK comments
grep -rn "TODO\|FIXME\|HACK\|XXX\|TEMPORARY" --include='*.ts' --include='*.js' --include='*.py' --include='*.java' --include='*.go' --include='*.rb' --include='*.php' src/ || true
```

### 7. Documentation

Assess documentation quality:
- [ ] README exists and is up to date
- [ ] API endpoints are documented
- [ ] Complex algorithms have explanatory comments
- [ ] Public APIs have usage examples
- [ ] Architecture decisions are recorded (ADRs)
- [ ] Setup/development instructions work for new developers
- [ ] Changelog is maintained

### 8. Dependency Health

Assess dependency hygiene:

```bash
# Check for outdated dependencies
npm outdated 2>/dev/null || true
pip list --outdated 2>/dev/null || true

# Check dependency count (too many deps = risk)
cat package.json | jq '.dependencies | length' 2>/dev/null || true
cat requirements.txt | wc -l 2>/dev/null || true
```

**Dependency red flags:**
- Dependencies with no recent updates (> 2 years)
- Multiple dependencies doing the same thing
- Large dependencies for small tasks
- Dependencies with known vulnerabilities
- Unpinned versions in production
- Dev dependencies mixed into production

### 9. Consistency

Check for consistency across the codebase:
- Naming conventions (camelCase vs snake_case, etc.)
- File/folder structure patterns
- Error handling patterns
- Logging patterns
- Import ordering
- Code formatting (run linter/formatter check)

```bash
# Check if formatter would change anything
npx prettier --check . 2>/dev/null || true
npx eslint . 2>/dev/null || true
```

### 10. Performance Indicators

Identify potential performance issues:
- Synchronous I/O in request handlers
- Missing database indexes (check migration files)
- N+1 query patterns
- Unbounded list queries (no pagination)
- Large payloads in API responses
- Missing caching for expensive operations
- Memory-intensive operations in loops

## Audit Workflow

### Step 1: Scope and Overview
1. Identify project type, languages, frameworks
2. Get overall size (lines of code, file count)
3. Identify entry points and critical paths
4. Review project structure and organization

### Step 2: Automated Analysis
Run available static analysis tools and collect metrics.

### Step 3: Manual Review
Sample key files across the codebase:
- Entry points and routing
- Core business logic
- Data access layer
- Authentication/authorization code
- Error handling middleware
- Configuration management

### Step 4: Deep Dive
Focus on areas flagged by automated analysis:
- Most complex files
- Most duplicated code
- Areas with lowest test coverage
- Recently changed files (git log)

### Step 5: Synthesize Findings
Categorize and prioritize findings by impact and effort.

### Step 6: Generate Report
Produce the audit report with actionable recommendations.

## Output Format

```markdown
## Code Audit Report

**Project:** [name]
**Scope:** [files/directories audited]
**Date:** [date]
**Overall Health:** [Excellent / Good / Fair / Poor / Critical]

### Executive Summary
[2-3 sentences on overall code health]

### Metrics
| Metric | Value | Status |
|--------|-------|--------|
| Total Lines of Code | X | |
| Number of Files | Y | |
| Average File Size | Z lines | |
| Largest File | [name] (N lines) | ⚠️ |
| Test Coverage | X% | |
| Number of Dependencies | N | |
| Outdated Dependencies | N | |
| Lint Errors | N | |
| TODO/FIXME Count | N | |

### Findings by Category

#### Complexity
| Severity | Count | Top Offenders |
|----------|-------|---------------|
| Critical (>20 complexity) | X | [file:line] |
| High (10-20 complexity) | Y | [file:line] |
| Medium (5-10 complexity) | Z | |

#### Duplication
- [ ] X% code duplication detected
- Top duplicated blocks: [locations]

#### Test Coverage
- Overall coverage: X%
- Untested critical paths: [list]
- Flaky tests: [list]

#### Architecture
- Circular dependencies: [list or "None"]
- Layer violations: [list or "None"]
- Coupling hotspots: [list]

#### Error Handling
- Swallowed exceptions: [count and locations]
- Missing error handling: [locations]

#### Code Smells
| Smell | Count | Locations |
|-------|-------|-----------|
| Dead code | X | |
| Magic numbers | Y | |
| Long methods | Z | |
| TODO/FIXME | W | |

### Prioritized Action Plan

#### Immediate (This Sprint)
1. [Action] — [Impact] — [Effort]
2. [Action] — [Impact] — [Effort]

#### Short Term (This Quarter)
1. [Action] — [Impact] — [Effort]

#### Long Term (Roadmap)
1. [Action] — [Impact] — [Effort]

### Risk Assessment
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|

### Recommendations
[Strategic recommendations for improving code health]
```

## Health Score Rubric

| Score | Rating | Description |
|-------|--------|-------------|
| 90-100 | Excellent | Clean, well-tested, maintainable. Minimal tech debt. |
| 75-89 | Good | Generally healthy with some areas for improvement. |
| 60-74 | Fair | Noticeable tech debt. Needs focused improvement. |
| 40-59 | Poor | Significant tech debt. Refactoring recommended. |
| 0-39 | Critical | Severe tech debt. Major intervention needed. |

## Reference Files

- [references/complexity-metrics.md](references/complexity-metrics.md) — Detailed complexity measurement guide
- [references/code-smells.md](references/code-smells.md) — Comprehensive code smell catalog
- [references/architecture-patterns.md](references/architecture-patterns.md) — Architecture health indicators
