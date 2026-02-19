---
name: git-workflow-hardener
description: Local security guards and secret prevention. 2026 Edition.
---

# Git Workflow Hardener (Compressed)

## Purpose
Local defense for code integrity and secret protection.

## Responsibilities
- **Hardening**: Protect branches from direct pushes.
- **Auditing**: Real-time **Gitleaks** and **Trufflehog** scanning.
- **Hooks**: Setup **Husky** for pre-commit lint/test.
- **Zero-Secret**: Enforce `.gitignore` for `.env`/`.pem` files.

## Protocol
1. Detect sensitive files -> 2. Inject hooks -> 3. Validate history before merge.