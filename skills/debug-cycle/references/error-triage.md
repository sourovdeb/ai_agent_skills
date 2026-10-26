# Error Triage Guide

## How to Read Stack Traces

Stack traces are read **bottom to top** — the root cause is usually near the bottom.

```
Error: Something went wrong
    at functionA (file.ts:10:5)      ← called from here
    at functionB (file.ts:20:3)      ← which was called from here
    at functionC (file.ts:30:1)      ← root cause is usually here (bottom)
```

## Triage by Error Type

### TypeError
**Meaning:** Wrong type used (undefined, null, wrong type)

**Triage steps:**
1. Read the exact property/function being accessed
2. Check if the object could be null/undefined
3. Trace where the object comes from
4. Check if async data is being accessed before it loads

### ReferenceError
**Meaning:** Variable/function doesn't exist in scope

**Triage steps:**
1. Check spelling of variable name
2. Check if variable is declared in the right scope
3. Check import statements
4. Check for hoisting issues (TDZ with `let`/`const`)

### SyntaxError
**Meaning:** Code can't be parsed

**Triage steps:**
1. Check the reported line and column
n2. Look for missing brackets, semicolons, quotes
3. Check for invalid characters
4. Run linter/formatter

### RangeError
**Meaning:** Value out of valid range

**Triage steps:**
1. Check array/string index bounds
2. Check number is within min/max
3. Check for infinite recursion (stack overflow)

### Network Errors
**Meaning:** HTTP request failed

**Triage steps:**
1. Check if server is running
2. Check URL is correct (typo? wrong port?)
3. Check CORS configuration
4. Check network connectivity
5. Check for SSL/TLS issues

### Permission Errors
**Meaning:** Access denied

**Triage steps:**
1. Check file/directory permissions
2. Check user has required role
3. Check API keys/tokens are valid
4. Check resource ownership

## Triage by Symptom

### "It works on my machine"
1. Compare environments (OS, Node version, dependencies)
2. Check environment variables
3. Check for hardcoded paths
4. Run in clean environment (Docker, CI)
5. Check for local-only config files

### "It worked yesterday"
1. Check recent commits: `git log --oneline -10`
2. Check recent dependency updates
3. Check for config changes
4. Use `git bisect` to find the breaking commit
5. Check external service changes (API deprecations)

### "It's intermittent"
1. Look for race conditions
2. Check for timing-dependent code
3. Add logging to capture state when it fails
4. Try to reproduce under load
5. Check for shared mutable state

### "It's slow"
1. Profile the code (find the bottleneck)
2. Check for N+1 queries
3. Check for unnecessary re-renders (UI)
4. Check for large data transfers
5. Check for missing indexes (database)
6. Check for memory leaks

## Diagnostic Commands

```bash
# Check recent changes
git log --oneline -20
git diff HEAD~3

# Find when a bug was introduced
git bisect start
git bisect bad HEAD
git bisect good <known-good-commit>

# Check environment
node --version
npm --version
printenv | grep -i relevant_var

# Check dependencies
npm list --depth=0
npm outdated

# Run specific test
npm test -- --grep "test name"

# Check for type errors
npx tsc --noEmit

# Check for lint errors
npx eslint src/

# Profile performance
node --prof app.js
node --inspect app.js  # Then open chrome://inspect
```
