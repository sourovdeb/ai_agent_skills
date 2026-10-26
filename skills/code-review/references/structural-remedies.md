# Structural Remedies: Common Problems and Fixes

When you flag a structural problem, propose the move — not just the problem.

## Replace a Chain of Conditionals

**Problem:** Long if/else or switch chains that are hard to extend.

**Remedy:** Use a typed model or explicit dispatcher (lookup table, strategy pattern, or polymorphism).

```typescript
// Before: chain of conditionals
if (type === 'a') { return doA(); }
else if (type === 'b') { return doB(); }
else if (type === 'c') { return doC(); }

// After: dispatcher
const handlers = { a: doA, b: doB, c: doC };
return handlers[type]?.() ?? defaultHandler();
```

## Collapse Duplicate Branches

**Problem:** Multiple branches with nearly identical logic.

**Remedy:** Merge into a single flow with parameterized differences.

## Separate Orchestration from Business Logic

**Problem:** A function that coordinates AND implements.

**Remedy:** Split into an orchestrator (coordinates) and services (implement).

## Move Feature-Specific Logic Out of Shared Modules

**Problem:** Shared utility module has feature-specific code.

**Remedy:** Move the logic to the package/module that owns the concept.

## Reuse the Canonical Helper

**Problem:** A bespoke near-duplicate of an existing helper.

**Remedy:** Delete the duplicate, use the canonical helper, extend the helper if needed.

## Make Type Boundaries Explicit

**Problem:** Silent fallbacks and `any` types hide unclear invariants.

**Remedy:** Make the boundary explicit — use proper types, discriminated unions, or validation at the boundary.

```typescript
// Before: silent fallback
hfunction process(data: any) {
  return data?.value ?? 0;
}

// After: explicit boundary
type ProcessInput = { value: number };
function process(data: ProcessInput): number {
  return data.value;
}
// Validate at the boundary: ProcessInput = ProcessInputSchema.parse(rawData)
```

## Delete Pass-Through Wrappers

**Problem:** A function that just calls another function without adding value.

**Remedy:** Delete the wrapper, call the inner function directly.

## Extract Helper or Split Large File

**Problem:** A file or function that's too large.

**Remedy:** Extract focused helpers or split into smaller modules with clear responsibilities.

## Replace Inheritance with Composition

**Problem:** Deep inheritance hierarchy that's hard to follow.

**Remedy:** Use composition — smaller, focused objects that delegate.

## Introduce Missing Abstraction

**Problem:** Repeated conditionals on the same shape signal a missing model.

**Remedy:** Introduce a type, enum, or class that captures the concept.

## Remove Dead Code

**Problem:** Unreachable code, unused exports, commented-out code.

**Remedy:** Delete it. Version control preserves history.

---

## Remedy Selection Guide

Prefer the remedy that **removes moving pieces** over one that **spreads complexity around**.

| Situation | Preferred Remedy |
|-----------|-----------------|
| Conditional chain | Dispatcher / lookup table |
| Duplicate logic | Extract shared helper |
| Mixed responsibilities | Split orchestration from logic |
| Feature logic in shared module | Move to owning module |
| Near-duplicate helper | Use canonical helper |
| Unclear type boundary | Make boundary explicit |
| Pass-through wrapper | Delete wrapper |
| Large file/function | Extract or split |
| Deep inheritance | Composition |
| Repeated conditionals | Introduce abstraction |
| Dead code | Delete |
