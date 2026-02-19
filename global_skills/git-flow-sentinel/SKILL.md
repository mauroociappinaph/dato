---
name: git-flow-sentinel
description: Repository integrity and branch strategy guard. 2026 Edition.
---

# Git Flow Sentinel (Compressed)

## Purpose
Protect `main`/`develop` branches. Enforce isolated feature development.

## Responsibilities
1. **Branch Verification**: MANDATORY `git status` check at task start.
2. **Auto-Branching**: Create `feature/dude-[task]` branches from `develop`.
3. **Cleanliness**: Ensure no uncommitted changes before switching.
4. **Sync**: Rebase feature branches with the latest `develop` regularly.

## Protocol
Step #0 of the Dude Pipeline.
