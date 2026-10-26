# Test Strategies by Change Type

## New Feature

### Required Tests
- [ ] Unit tests for business logic
- [ ] Integration tests for API endpoints
- [ ] Component tests for UI (if applicable)
- [ ] Edge case tests (empty input, max values, invalid input)
- [ ] Error handling tests

### Verification Steps
1. Test the happy path end-to-end
2. Test with various input combinations
3. Test error scenarios
4. Test on different browsers/devices (if UI)
5. Test with real data (not just mocks)

---

## Bug Fix

### Required Tests
- [ ] Regression test that fails without the fix
- [ ] Test that the original bug scenario is resolved
- [ ] Test that the fix doesn't break related functionality

### Verification Steps
1. Reproduce the original bug (confirm it exists)
2. Apply the fix
3. Confirm the bug is resolved
4. Confirm no regressions
5. Test edge cases around the fix

---

## Refactoring

### Required Tests
- [ ] All existing tests still pass (no new tests needed if behavior unchanged)
- [ ] If behavior changed intentionally, update/add tests

### Verification Steps
1. Confirm all existing tests pass before refactoring
2. Refactor in small steps
3. Run tests after each step
4. Confirm all tests pass after refactoring
5. Verify no performance regression
6. Verify code is actually simpler (not just moved)

---

## API Change

### Required Tests
- [ ] Request validation tests
- [ ] Response schema tests
- [ ] Authentication tests
- [ ] Authorization tests
- [ ] Error response tests (400, 401, 403, 404, 500)
- [ ] Rate limiting tests (if applicable)
- [ ] Pagination tests (if applicable)

### Verification Steps
1. Test with valid requests
2. Test with invalid/malformed requests
3. Test without authentication
4. Test with insufficient permissions
5. Test rate limiting
6. Test with large payloads
7. Verify response schema matches documentation

---

## Database Change

### Required Tests
- [ ] Migration runs successfully (up and down)
- [ ] Data integrity maintained after migration
- [ ] Application works with new schema
- [ ] Performance of queries is acceptable

### Verification Steps
1. Run migration on copy of production data
2. Verify data integrity
3. Test rollback (down migration)
4. Check query performance (EXPLAIN)
5. Verify indexes are correct
6. Test with large dataset

---

## Security Fix

### Required Tests
- [ ] Test that the vulnerability is fixed
- [ ] Test that normal functionality still works
- [ ] Test edge cases that might bypass the fix

### Verification Steps
1. Attempt the exploit (confirm it's blocked)
2. Test legitimate use cases still work
3. Run security scanner
4. Review the fix with a second person
5. Check for similar issues elsewhere

---

## Performance Fix

### Required Tests
- [ ] Benchmark before and after
- [ ] Test under load
- [ ] Test with large datasets

### Verification Steps
1. Measure baseline performance
2. Apply the fix
3. Measure improved performance
4. Test under concurrent load
5. Test with maximum expected data size
6. Verify no accuracy/precision loss

---

## Configuration Change

### Required Tests
- [ ] Application starts with new config
- [ ] Features enabled/disabled correctly
- [ ] Default values work when config is missing

### Verification Steps
1. Test with new config values
2. Test with missing config (defaults)
3. Test with invalid config (error handling)
4. Test in each environment (dev, staging, prod)
5. Verify secrets are not exposed
