# Architecture Health Indicators

## Healthy Architecture Signs

- Clear module boundaries (each module has one reason to change)
- Dependencies flow inward (outer layers depend on inner layers)
- No circular dependencies
- Business logic is independent of frameworks
- Data access is abstracted behind repositories/interfaces
- Configuration is externalized (not hardcoded)
- Errors are handled at appropriate layers
- Logging is consistent across modules

## Architecture Smells

### Circular Dependencies
**Signal:** Module A imports B, B imports A (directly or transitively)
**Impact:** Hard to test, hard to change, build issues
**Fix:**
- Extract shared code into a third module
- Use dependency inversion (interfaces)
- Restructure module boundaries

### Layer Violations
**Signal:** UI imports database, controller contains business logic
**Impact:** Tight coupling, hard to test, hard to reuse
**Fix:**
- Enforce layer boundaries (linting rules)
- Move business logic to service layer
- Use dependency injection

### God Module
**Signal:** One module imports/exports too much, used everywhere
**Impact:** Change in one place affects everything
**Fix:**
- Split into focused modules
- Identify what each consumer actually needs
- Create specific interfaces instead of exposing everything

### Feature Logic in Shared Modules
**Signal:** Shared utility module has feature-specific code
**Impact:** Shared module changes for every feature
**Fix:**
- Move feature logic to feature module
- Keep shared modules truly generic

### Tight Coupling
**Signal:** Changes in one module require changes in many others
**Impact:** Shotgun surgery, fragile codebase
**Fix:**
- Use interfaces/abstractions
- Apply dependency inversion
- Use events/messaging for cross-cutting concerns

### Missing Abstractions
**Signal:** Repeated patterns that should be extracted
**Impact:** Code duplication, inconsistent implementations
**Fix:**
- Extract common pattern into abstraction
- Create shared utilities for repeated logic

### Anemic Domain Model
**Signal:** Data classes with no behavior, all logic in services
**Impact:** Procedural code in OO disguise, hard to maintain
**Fix:**
- Move behavior into domain objects
- Make data classes responsible for their own validation

### Configuration Scattered
**Signal:** Config values hardcoded in multiple places
**Impact:** Hard to change, environment-specific bugs
**Fix:**
- Centralize configuration
- Use environment variables
- Validate config at startup

## Architecture Patterns Quick Reference

| Pattern | When to Use | Key Benefit |
|---------|------------|-------------|
| Layered | Most applications | Clear separation of concerns |
| Hexagonal (Ports & Adapters) | Need to swap implementations | Framework/database independence |
| Clean Architecture | Complex business logic | Testable business rules |
| Microservices | Large teams, independent scaling | Independent deployment |
| Modular Monolith | Starting point for microservices | Simplicity with clear boundaries |
| CQRS | Read/write have different needs | Optimized read and write models |
| Event-Driven | Async workflows, audit trails | Loose coupling, scalability |

## Dependency Direction Rules

```
Good:  UI → Services → Repository → Database
       (outer depends on inner)

Bad:   Database → Repository → Services → UI
       (inner depends on outer — circular!)

Good:  All layers depend on Domain/Entities (center)
       UI → Domain ← Services
       Repository → Domain ← Services
```

## Module Boundary Checklist

- [ ] Each module has a clear, single responsibility
- [ ] Module's public API is minimal (only what consumers need)
- [ ] No module imports another module's internal implementation
- [ ] Dependencies between modules are explicit (imports, not globals)
- [ ] No circular dependencies
- [ ] Shared code is in a separate shared module
- [ ] Configuration is injected, not imported
