# Complexity Metrics Guide

## Cyclomatic Complexity

Measures the number of independent paths through code.

**Formula:** M = E - N + 2P
- E = edges, N = nodes, P = connected components

**Thresholds:**
| Complexity | Risk Level | Action |
|-----------|-----------|--------|
| 1-5 | Low | Simple, easy to test |
| 6-10 | Moderate | Acceptable |
| 11-20 | High | Consider refactoring |
| 21-50 | Very High | Refactor recommended |
| 50+ | Extreme | Must refactor |

**How to reduce:**
- Extract functions (one responsibility per function)
- Replace conditionals with polymorphism or lookup tables
- Use early returns to reduce nesting
- Extract complex conditions into named functions

## Cognitive Complexity

Measures how hard code is to understand (not just count paths).

**Thresholds:**
| Score | Risk Level |
|-------|-----------|
| 0-5 | Good |
| 6-10 | Acceptable |
| 11-20 | Should improve |
| 20+ | Refactor needed |

**What increases cognitive complexity:**
- Nesting (each level adds to the score)
- Breaks in linear flow (continue, break, goto)
- Long boolean expressions
- Catch/switch with many cases

## Nesting Depth

| Depth | Risk |
|-------|------|
| 1-2 | Good |
| 3 | Acceptable |
| 4 | Warning |
| 5+ | Refactor — use early returns, extract functions |

## Function Length

| Lines | Assessment |
|-------|-----------|
| 1-20 | Ideal |
| 21-50 | Acceptable |
| 51-100 | Consider splitting |
| 100+ | Should split |

## File Length

| Lines | Assessment |
|-------|-----------|
| 1-200 | Good |
| 201-500 | Acceptable |
| 501-1000 | Consider splitting |
| 1000+ | Should split |

## Parameter Count

| Parameters | Assessment |
|-----------|-----------|
| 0-3 | Ideal |
| 4 | Acceptable |
| 5-6 | Consider options object |
| 7+ | Use options object or builder pattern |

## Class/Module Size

| Metric | Threshold |
|--------|-----------|
| Methods per class | < 20 |
| Lines per class | < 300 |
| Imports per file | < 15 |
| Exports per module | < 10 |

## Measuring Tools

```bash
# JavaScript/TypeScript
npx eslint --rule '{"complexity": ["error", 10], "max-lines": ["warn", 500], "max-depth": ["warn", 4], "max-params": ["warn", 4]}' src/

# Python
pylint --disable=all --enable=C0301(line-too-long),C0302(too-many-lines),R0912(too-many-branches),R0915(too-many-statements),R0913(too-many-arguments)
radon cc src/ -a  # Average complexity
radon cc src/ -nc  # Show functions with complexity > C

# General
cloc src/  # Lines of code by language
tokei src/ # Fast code counting
```
