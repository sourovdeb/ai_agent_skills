---
name: "test-driven-development"
description: "Load this skill when you need to enforce strict test-driven development workflows. Restricts code generation until robust test specifications are written."
---
# Test-Driven Development (TDD)

Strictly enforces automated test-first architectural patterns. Prevents shifting to functional script generation until robust test specifications are written.

## Natural Triggers
- "write tests first"
- "TDD approach"
- "test-driven development"
- "test before code"
- "red green refactor"
- "write unit tests"
- "test specifications"
- "test-first"
- "behavior-driven development"
- "acceptance criteria"

## Core Principles

### Red-Green-Refactor Cycle
1. **Red**: Write a failing test for desired functionality
2. **Green**: Write minimal code to make test pass
3. **Refactor**: Improve code while keeping tests passing

### Strict Enforcement
- NO code generation without tests
- Tests must be written first
- Tests must be executable
- Tests must fail initially (Red phase)
- Code must make tests pass (Green phase)

## Workflow

### Step 1: Define Requirements
- Gather user stories
- Extract acceptance criteria
- Identify edge cases
- Define success metrics

### Step 2: Write Tests
- Create test file structure
- Write failing test cases
- Include assertions
- Cover happy path and edge cases
- Ensure tests are executable

### Step 3: Verify Red Phase
- Confirm tests fail
- Validate failure messages
- Check test coverage
- Identify missing test cases

### Step 4: Generate Code
- Write minimal implementation
- Focus on making tests pass
- Avoid over-engineering
- Keep it simple

### Step 5: Verify Green Phase
- Run tests
- Confirm all pass
- Check for regressions
- Validate edge cases

### Step 6: Refactor
- Improve code structure
- Maintain test coverage
- Optimize performance
- Keep tests passing

## Test Quality Standards

### Good Tests
- Clear, descriptive names
- Single responsibility
- Fast execution
- Deterministic results
- Isolated from other tests
- Test behavior, not implementation

### Test Structure
```
Describe: Feature/Component
  Context: Scenario/State
    It: Should do something
    It: Should handle edge case
    It: Should validate input
```

## Supported Testing Frameworks

### JavaScript/TypeScript
- Jest
- Mocha + Chai
- Vitest
- Cypress (E2E)
- Playwright (E2E)

### Python
- pytest
- unittest
- doctest

### Java
- JUnit
- TestNG

### C#
- xUnit
- NUnit
- MSTest

### Go
- testing package
- Testify

### Rust
- rust-test

### PHP
- PHPUnit

## Test Types

### Unit Tests
- Test individual functions/methods
- Fast, isolated
- Mock dependencies

### Integration Tests
- Test component interactions
- Validate system boundaries
- Use real dependencies where possible

### End-to-End Tests
- Test complete user flows
- Validate full system behavior
- Slower, but comprehensive

### Property-Based Tests
- Test invariants
- Generate random inputs
- Validate properties hold

## Anti-Patterns to Avoid

### Don't
- Write code before tests
- Write tests that always pass
- Test implementation details
- Create slow tests
- Write flaky tests
- Skip edge cases
- Test multiple things in one test

### Do
- Write tests first
- Write tests that fail initially
- Test behavior, not implementation
- Keep tests fast
- Make tests deterministic
- Test one thing per test
- Include edge cases

## References
- Repository: https://github.com/obra/superpowers (includes TDD skill)
- Also found in: https://github.com/BehiSecc/awesome-claude-skills
- TDD Manifesto: https://agilemanifesto.org/

## Integration with Other Skills
- Works with: Systematic Debugging (for test failures)
- Complements: Code Quality Collection (for test standards)
- Enhances: Superpowers (TDD enforcement in workflows)