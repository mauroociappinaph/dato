---
name: deploy-automation-pilot
description: Automated deployments (Vercel, Railway, MCP). 2026 Edition.
---

# Deploy Automation Pilot (Compressed)

## Purpose
Zero-config code deployment from local to production.

## Capabilities
- **Platform**: Vercel (CLI), Railway (Up), GitHub Actions.
- **Health Check (MCP)**: Automated smoke tests post-deploy using MCP tools.
- **Rollback**: Log analysis and autonomous revert on failure.

## Rules
1. **Build First**: MANDATORY `npm run build` check before push.
2. **Logs**: Provide direct inspection links to the Owner.
3. **Validation**: Confirm `/health` or logs before closing task.
