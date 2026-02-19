---
name: git-advanced-workflows
description: Complex Git operations (Rebase, Bisect, Reflog). 2026 Edition.
---

# Git Advanced Workflows (Compressed)

## Purpose
Maintain clean repository history and enable high-confidence disaster recovery.

## Core Operations
- **Interactive Rebase**: `pick`, `squash`, `fixup`, `drop`. Clean history before PR.
- **Git Bisect**: Binary search for bugs. Use `git bisect run` for automation.
- **Worktrees**: Simultaneous multi-branch development without stashing.
- **Reflog**: Safety net for recovering deleted commits or branches (90-day window).
- **Cherry-Pick**: Apply specific commits across branches with `-n` (no-commit) option.

## Practical Workflows
1. **Cleanup**: `git rebase -i main` -> Squash/Reword -> `push --force-with-lease`.
2. **Recovery**: `git reflog` -> Find Hash -> `git reset --hard [hash]`.
3. **Hotfix**: Apply to multiple releases using `cherry-pick`.

## Rules (Mandatory)
1. **Force Lease**: NEVER use `--force`; always use `--force-with-lease`.
2. **Atomic Commits**: One logical change per commit.
3. **Pre-PR Cleanup**: MANDATORILY squash "fix typo" or "temp" commits before merge.
4. **Reflog Check**: Consult reflog before admitting "lost work".
