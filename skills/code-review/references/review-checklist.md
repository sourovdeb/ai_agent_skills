# Code Review Quick Reference Checklist

## Context
- [ ] I understand what this change does and why
- [ ] The change matches the spec/task requirements

## Correctness
- [ ] Edge cases handled (null, empty, boundary values)
- [ ] Error paths handled (not just happy path)
- [ ] No off-by-one errors
- [ ] No race conditions or state inconsistencies
- [ ] Tests cover the change adequately
- [ ] Tests test behavior, not implementation details

## Readability
- [ ] Names are clear and consistent with project conventions
- [ ] Logic is straightforward (no deep nesting)
- [ ] No unnecessary complexity
- [ ] No magic numbers or strings
- [ ] Comments explain why, not what
- [ ] No dead code

## Architecture
- [ ] Follows existing patterns
- [ ] Clean module boundaries maintained
- [ ] No unnecessary coupling
- [ ] Appropriate abstraction level
- [ ] No feature logic in shared modules
- [ ] Dependencies flow in the right direction

## Security
- [ ] No secrets in code, logs, or config
- [ ] Input validated at boundaries
- [ ] No injection vulnerabilities
- [ ] Auth checks in place where needed
- [ ] External data treated as untrusted
- [ ] No new vulnerable dependencies

## Performance
- [ ] No N+1 query patterns
- [ ] No unbounded loops or data fetching
- [ ] No synchronous operations that should be async
- [ ] Pagination on list endpoints
- [ ] No unnecessary re-renders (UI)
- [ ] Resources properly released

## Tests
- [ ] Tests exist for new code
- [ ] Tests cover edge cases
- [ ] Tests have descriptive names
- [ ] Tests would catch a regression
- [ ] No flaky tests introduced

## Verification
- [ ] All tests pass
- [ ] Build succeeds
- [ ] Lint passes
- [ ] Manual verification done (if applicable)
- [ ] No debug code left

## Verdict
- [ ] **APPROVE** — Ready to merge
- [ ] **CONCERNS** — Merge at own risk, follow-ups needed
- [ ] **BLOCK** — Issues must be addressed before merge
