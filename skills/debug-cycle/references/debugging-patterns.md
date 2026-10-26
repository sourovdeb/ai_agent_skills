# Debugging Patterns by Symptom

## Common Bug Patterns

### Null/Undefined Errors

**Symptom:** `Cannot read property 'x' of undefined`, `TypeError: null`

**Common causes:**
- Async data not yet loaded when accessed
- API returning null where code expects an object
- Optional chaining missing on possibly-undefined values
- Race condition: state updated after component unmounted

**Debug approach:**
1. Find where the value originates (network? props? state?)
2. Check if it can be undefined at that point
3. Add null check or default value at the source

### Off-by-One Errors

**Symptom:** Array index out of bounds, loop missing last element, extra iteration

**Common causes:**
- `<` vs `<=` in loop conditions
- `slice(0, n)` vs `slice(0, n+1)`
- 0-indexed vs 1-indexed confusion

**Debug approach:**
1. Write out the expected indices/values
2. Compare with actual
3. Check boundary conditions explicitly

### Race Conditions

**Symptom:** Intermittent failures, works sometimes, state corruption

**Common causes:**
- Multiple async operations modifying shared state
- Missing await on promises
- State updates after component unmount
- Concurrent requests with stale data

**Debug approach:**
1. Add logging with timestamps at each step
n2. Check if operations complete in expected order
3. Look for missing `await` or unhandled promises
4. Check for state updates after cleanup

### Memory Leaks

**Symptom:** Performance degrades over time, increasing memory usage

**Common causes:**
- Event listeners not removed
- Subscriptions not unsubscribed
- Closures holding references
- Growing arrays/caches without eviction
- Timers not cleared

**Debug approach:**
1. Use memory profiler (Chrome DevTools, heap snapshots)
2. Compare heap before/after repeated operations
3. Look for objects that should be garbage collected but aren't

### Infinite Loops

**Symptom:** Page freezes, timeout, stack overflow

**Common causes:**
- Loop condition never becomes false
- Recursive function without base case
- State update in loop triggers re-render which triggers loop

**Debug approach:**
1. Add iteration counter with limit
2. Log loop variables at each iteration
3. Check what changes (or doesn't change) each iteration

### State Inconsistency

**Symptom:** UI shows stale data, actions have no effect, double submissions

**Common causes:**
- Multiple sources of truth for same data
- State updates not batched (React < 18)
- Optimistic updates not rolled back on failure
- Cache not invalidated after mutation

**Debug approach:**
1. Trace the data flow: where does it come from? where does it go?
2. Check if all update paths are covered
3. Verify cache invalidation

## Error Message Interpretation

| Error Message | Likely Cause | First Check |
|--------------|-------------|-------------|
| `Cannot read property 'x' of undefined` | Accessing property on undefined | Where does the object come from? |
| `X is not a function` | Calling non-function | Check imports, check if X is defined |
| `Module not found` | Missing dependency or wrong path | Check import path, run install |
| `CORS error` | Browser blocking cross-origin request | Check server CORS headers |
| `401 Unauthorized` | Missing/invalid auth | Check token, check auth header |
| `403 Forbidden` | Insufficient permissions | Check user roles, check endpoint auth |
| `404 Not Found` | Wrong URL or resource doesn't exist | Check URL, check route definition |
| `500 Internal Server Error` | Server-side error | Check server logs |
| `Network Error` | Connection failed | Check server is running, check URL |
| `TypeError: X is not a constructor` | Calling class without `new` or wrong import | Check import, check `new` keyword |
| `ReferenceError: X is not defined` | Using undefined variable | Check variable name, check scope |
| `SyntaxError: Unexpected token` | Parse error | Check syntax at reported location |

## Debugging by Layer

### Frontend
1. Check browser console for errors
2. Check Network tab for failed requests
3. Check React/Vue DevTools for component state
4. Check Application tab for localStorage/cookies
5. Add `debugger` statement or console.log at key points

### Backend
1. Check server logs for stack traces
2. Add request/response logging
3. Check database query logs
4. Verify environment variables are set
5. Check for unhandled promise rejections

### Database
1. Check query execution plan (EXPLAIN)
2. Verify indexes exist for queried columns
3. Check for locks or long-running transactions
4. Verify data integrity (foreign keys, constraints)

### Infrastructure
1. Check service health/status
2. Verify DNS resolution
3. Check firewall/security group rules
4. Verify SSL/TLS certificates
5. Check resource limits (CPU, memory, disk)
