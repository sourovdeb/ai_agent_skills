---
name: "finishing-dev-branch"
description: "Load this skill when merging a development branch. Automates and optimizes the terminal staging workflow including validation, formatting, reviews, and cleanup."
---
# Finishing a Development Branch

Automates and optimizes the terminal staging workflow. Streamlines code validation, formatting, final code reviews, and cleanup routines during branch merges.

## Natural Triggers
- "merge this branch"
- "finish the feature"
- "prepare for PR"
- "clean up branch"
- "stage for merge"
- "final review"
- "pre-merge checklist"
- "branch cleanup"
- "get ready to merge"

## Pre-Merge Checklist

### Code Quality
- [ ] All tests pass
- [ ] Linting passes
- [ ] No type errors
- [ ] Code formatted correctly
- [ ] No console.log statements
- [ ] No commented-out code
- [ ] No TODO comments (or converted to issues)

### Documentation
- [ ] Code comments updated
- [ ] README updated (if applicable)
- [ ] CHANGELOG updated
- [ ] API documentation updated
- [ ] Migration guides (if breaking changes)

### Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] E2E tests pass (if applicable)
- [ ] Manual testing completed
- [ ] Edge cases covered

### Code Review Preparation
- [ ] Commit messages are clear
- [ ] Commit history is clean
- [ ] Related issues linked
- [ ] Screenshots attached (for UI changes)
- [ ] Performance metrics included (if applicable)

## Automated Workflow

### Step 1: Run Validation Suite
```bash
# Run all tests
npm test

# Run linting
npm run lint

# Check types
npm run type-check

# Check formatting
npm run format:check
```

### Step 2: Fix Issues
```bash
# Auto-fix linting issues
npm run lint:fix

# Auto-fix formatting
npm run format
```

### Step 3: Final Review
- Review all changes
- Check for sensitive data
- Verify no unintended files
- Confirm build passes
- Check bundle size (if frontend)

### Step 4: Update Documentation
- Update version numbers
- Add release notes
- Update dependencies
- Document breaking changes

### Step 5: Create Pull Request
- Use descriptive title
- Include detailed description
- Link to issues
- Add reviewers
- Add labels

### Step 6: Post-Merge Cleanup
- Delete feature branch (if using GitHub flow)
- Update local branches
- Clean up temporary files
- Archive old branches

## Git Workflow Commands

### Check Status
```bash
git status
git diff
git log --oneline
```

### Stage Changes
```bash
git add .
git add -p  # Interactive staging
git reset HEAD <file>  # Unstage
```

### Commit
```bash
git commit -m "feat: add new feature"
git commit --amend  # Amend last commit
git commit --no-verify  # Skip hooks
```

### Push
```bash
git push origin feature-branch
git push --force-with-lease  # Force push safely
```

### Create PR
```bash
gh pr create
gh pr create --fill  # Auto-fill from branch name
```

### Merge
```bash
git checkout main
git pull origin main
git merge feature-branch
git push origin main
```

## Cleanup Tasks

### Branch Management
```bash
# Delete local branch
git branch -d feature-branch

# Delete remote branch
git push origin --delete feature-branch

# Prune remote tracking branches
git remote prune origin
```

### File Cleanup
```bash
# Remove temporary files
rm -rf node_modules/.cache
rm -rf dist/
rm -rf build/

# Remove IDE files
rm -rf .vscode/
rm -rf .idea/

# Remove log files
rm -f *.log
rm -f npm-debug.log*
```

### Dependency Cleanup
```bash
# Remove unused dependencies
npm prune
npm uninstall <package>

# Update dependencies
npm update
npm outdated
```

## Quality Gates

### Mandatory Checks (Must Pass)
- All tests pass
- No linting errors
- No type errors
- Build succeeds
- No breaking changes (or documented)

### Recommended Checks (Should Pass)
- All tests pass on CI
- Code coverage maintained
- Performance not degraded
- Bundle size not increased significantly
- Accessibility checks pass

### Optional Checks (Nice to Have)
- Documentation complete
- Examples updated
- Tutorials updated
- Screenshots updated
- Video walkthrough

## Review Guidelines

### For Reviewers
- Focus on the "why", not just the "what"
- Check for edge cases
- Verify error handling
- Validate assumptions
- Check for performance issues
- Review security implications

### For Authors
- Respond to all comments
- Update code based on feedback
- Re-run tests after changes
- Update documentation
- Thank reviewers

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills
- GitHub Flow: https://guides.github.com/introduction/flow/
- Git Best Practices: https://git-scm.com/book/en/v2

## Integration with Other Skills
- **Using Git Worktrees**: For multi-branch workflows
- **Systematic Debugging**: For fixing issues found during review
- **Test-Driven Development**: For ensuring test coverage
