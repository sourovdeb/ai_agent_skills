# QA Checklist (Printable)

## Pre-Merge QA Checklist

### Automated
- [ ] Lint passes (`npm run lint`)
- [ ] Type check passes (`npm run typecheck` / `tsc --noEmit`)
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Build succeeds (`npm run build`)
- [ ] No new high/critical dependency vulnerabilities (`npm audit`)
- [ ] No secrets in code or recent commits
- [ ] Test coverage meets threshold
- [ ] Code is properly formatted

### Functional
- [ ] Primary use case works correctly
- [ ] Expected outputs match actual outputs
- [ ] Edge cases handled (null, empty, boundary)
- [ ] Error cases produce appropriate errors
- [ ] No regressions in existing functionality
- [ ] Performance is acceptable

### UI (if applicable)
- [ ] Visual appearance is correct
- [ ] Responsive design works (mobile/tablet/desktop)
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Sufficient color contrast
- [ ] Loading states shown
- [ ] Error states displayed clearly
- [ ] Empty states handled

### API (if applicable)
- [ ] Request/response match documented schema
- [ ] HTTP status codes are correct
- [ ] Headers set correctly (CORS, security)
- [ ] Pagination works
- [ ] Rate limiting works
- [ ] Authentication enforced
- [ ] Authorization enforced
- [ ] Input validation comprehensive

### Documentation
- [ ] Code changes documented (if public API)
- [ ] README updated (if user-facing)
- [ ] Changelog updated
- [ ] Inline comments for non-obvious logic
- [ ] Migration guide (if breaking change)

### Pre-Merge
- [ ] Branch up to date with target
- [ ] No merge conflicts
- [ ] Commit messages clear and descriptive
- [ ] No debug code or console.logs
- [ ] No hardcoded values (should be configurable)
- [ ] Feature flags for incomplete features

---

## Verdict

- [ ] **APPROVED** — Ready to merge and deploy
- [ ] **APPROVED WITH CONCERNS** — Merge OK, follow-ups tracked
- [ ] **BLOCKED** — Issues must be resolved first

## Sign-Off

**Reviewer:** ________________
**Date:** ________________
**Notes:** ________________
