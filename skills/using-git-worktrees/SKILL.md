---
name: "using-git-worktrees"
description: "Load this skill when working with multiple branches simultaneously. Provides deep architectural context for Git worktree environments."
---
# Using Git Worktrees

Provides deep architectural context for workspace environments where engineers concurrently handle multi-branch context switching via Git worktrees.

## Natural Triggers
- "work on multiple branches"
- "switch between branches"
- "git worktree"
- "parallel development"
- "multi-branch workflow"
- "context switching"
- "simultaneous branches"
- "worktree setup"

## Core Concepts

### What are Git Worktrees?
Git worktrees allow you to have multiple working directories from the same repository, each checked out to a different branch. This enables:
- Working on multiple features simultaneously
- Testing different versions side-by-side
- Comparing branches easily
- Reducing context switching overhead

### When to Use Worktrees
- Developing multiple features in parallel
- Fixing bugs in different branches
- Testing integration between branches
- Maintaining multiple versions
- Comparing implementations

### When NOT to Use Worktrees
- Simple linear development
- Small projects with few branches
- When branch isolation isn't needed
- For beginners (can be confusing)

## Setup & Configuration

### Create a New Worktree
```bash
# List existing worktrees
git worktree list

# Add a new worktree for a branch
git worktree add ../feature-branch feature-branch

# Add a worktree for a new branch
git worktree add ../new-feature -b new-feature

# Add a worktree at a specific commit
git worktree add ../experiment HEAD~5
```

### Worktree Structure
```
/project/
  .git/              # Main repository (shared)
  /worktree-main/    # Main branch worktree
  /worktree-feat1/   # Feature 1 worktree
  /worktree-feat2/   # Feature 2 worktree
  /worktree-fix/     # Bug fix worktree
```

### Configuration
```bash
# Set worktree-specific config
git -C /path/to/worktree config user.name "Feature Bot"

# Set default branch for new worktrees
git config --global init.defaultBranch main
```

## Workflow Patterns

### Pattern 1: Feature Branches
```bash
# Create worktree for new feature
git worktree add ../feature-login -b feature/login

# Work in the feature worktree
cd ../feature-login
# Make changes, commit, etc.

# Create PR from feature branch
gh pr create
```

### Pattern 2: Parallel Development
```bash
# Have multiple features in progress
git worktree add ../feature-A -b feature/A
git worktree add ../feature-B -b feature/B
git worktree add ../feature-C -b feature/C

# Work on each independently
cd ../feature-A
# ... work on A

cd ../feature-B
# ... work on B
```

### Pattern 3: Bug Fixing
```bash
# Create worktree for hotfix
git worktree add ../hotfix -b hotfix/critical-bug

# Fix the issue
cd ../hotfix
# ... make fixes

# Create PR
gh pr create --base main --head hotfix/critical-bug
```

### Pattern 4: Version Maintenance
```bash
# Maintain multiple versions
git worktree add ../v1.x -b release/v1.x
git worktree add ../v2.x -b release/v2.x
git worktree add ../main -b main

# Apply fixes to all versions
cd ../v1.x && git cherry-pick <commit>
cd ../v2.x && git cherry-pick <commit>
cd ../main && git cherry-pick <commit>
```

## Advanced Operations

### Remove a Worktree
```bash
# Remove worktree (must not be checked out in that worktree)
git worktree remove ../feature-old

# Force remove (if worktree is corrupted)
git worktree remove --force ../feature-old
```

### Prune Stale Worktrees
```bash
# Remove worktrees for deleted branches
git worktree prune
```

### Worktree Status
```bash
# Show status across all worktrees
git worktree list

# Show which worktree you're in
pwd

# Show branch of current worktree
git branch --show-current
```

### Synchronize Changes
```bash
# Pull changes in all worktrees
for worktree in $(git worktree list | cut -d' ' -f1); do
  git -C "$worktree" pull
 done

# Fetch in main repository (shared)
git fetch --all
```

## Context Management

### Understanding Context
Each worktree has:
- Its own working directory
- Its own index (staging area)
- Checked out to a specific branch/commit
- Shared .git directory with main repository

### Switching Context
```bash
# Switch to different worktree
cd /path/to/worktree

# See which branch you're on
git status

# See changes in this worktree
git diff
```

### Sharing Changes Between Worktrees
```bash
# Commit in one worktree
cd ../feature-A
git add .
git commit -m "Add feature"

# Changes are immediately available in other worktrees
git -C ../feature-B log  # Shows the new commit
```

## Troubleshooting

### Common Issues

#### "Already checked out"
```bash
# You're already in a worktree, can't add another
cd /main/repository
git worktree add ../new-feature new-feature
```

#### Worktree is locked
```bash
# Another process is using the worktree
# Close the other process or use --force
 git worktree add --force ../new-feature new-feature
```

#### Missing files
```bash
# Files might be in a different worktree
# Check all worktrees
git worktree list
```

#### Conflicting paths
```bash
# Path already exists
git worktree add --force ../existing-path branch
```

### Recovery

#### Recreate a corrupted worktree
```bash
# Remove the corrupted worktree
git worktree remove --force ../corrupted

# Recreate it
git worktree add ../corrupted branch
```

#### Reset all worktrees
```bash
# Remove all worktrees except main
git worktree list | grep -v main | awk '{print $1}' | xargs -I {} git worktree remove {}
```

## Best Practices

### Organization
- Use descriptive worktree names
- Group related worktrees together
- Document worktree purposes
- Keep worktree directory clean

### Naming Conventions
```bash
# By feature
git worktree add ../feat/login -b feature/login

# By issue number
git worktree add ../issue-123 -b fix/issue-123

# By version
git worktree add ../v2.1 -b release/v2.1
```

### Workflow Integration
- Use worktrees with CI/CD
- Integrate with IDEs
- Use with Git hooks
- Combine with Git LFS

### Performance
- Worktrees share .git directory (space efficient)
- Each worktree has its own index
- Minimal overhead for additional worktrees

## IDE Integration

### VS Code
- Open each worktree in separate window
- Use workspace trust settings
- Configure workspace-specific settings

### IntelliJ/WebStorm
- Open each worktree as separate project
- Configure project-specific SDKs
- Set up separate run configurations

### Vim/Neovim
- Use :cd to switch worktrees
- Configure per-directory settings
- Use plugins for worktree awareness

## References
- Repository: https://github.com/BehiSecc/awesome-claude-skills
- Git Documentation: https://git-scm.com/docs/git-worktree
- Git Worktree Tutorial: https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows

## Integration with Other Skills
- **Finishing a Dev Branch**: For merging worktree branches
- **Systematic Debugging**: For debugging across worktrees
- **Superpowers**: For complex multi-branch workflows
