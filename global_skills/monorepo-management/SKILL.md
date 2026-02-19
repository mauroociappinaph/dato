---
name: monorepo-management
description: Turborepo and Nx multi-package optimization. 2026 Edition.
---

# Monorepo Management (Compressed)

## Purpose
Manage efficient, scalable multi-package repositories. "Share code, not complexity".

## Architecture
- **Tools**: Turborepo, Nx, pnpm workspaces.
- **Optimization**: Remote caching, atomic changes across packages.
- **CI/CD**: Selective task execution based on affected files.

## Standards
- Shared TS/Lint/Prettier configs in `packages/`.
- Use Changesets for versioning.
- Prevent circular dependencies.