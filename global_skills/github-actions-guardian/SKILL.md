---
name: github-actions-guardian
description: 24/7 repo maintenance and security PR audits. 2026 Edition.
---

# GitHub Actions Guardian (Compressed)

## Purpose
Autonomous oversight of GitHub repositories. The "Night Guard".

## Automation Protocol
- **Triage**: Auto-label issues/bugs.
- **Auto-Fix**: Resolve lint/simple bugs via Gemini CLI.
- **Security-Gate (Mandatory)**: Invoke **security-auditor** for vulnerability audits on every PR. Block critical findings.

## Setup
Configured in `.github/workflows/` using Gemini-aware actions.