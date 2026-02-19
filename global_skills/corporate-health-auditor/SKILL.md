---
name: corporate-health-auditor
description: Specialized skill for auditing the health of THE DUDE's corporate infrastructure, including Redis, agents, disk usage, and Telegram reporting.
---

# Corporate Health Auditor

## Objective
Provide a robust, deterministic way to verify that the entire synthetic workforce and its infrastructure are operational.

## Workflow
1. **Infrastructure Check**: Verify Redis connectivity.
2. **Resource Check**: Monitor disk usage and project footprint.
3. **Agent Check**: Ensure all critical agent directories (Worker Identity) exist.
4. **VCS Check**: Monitor Git status for uncommitted changes.
5. **Report**: Log results to `CORPORATE_LOG.md` and send a summary to the CEO via Telegram.

## Tools
- `scripts/audit.py`: Python script that executes all checks and sends notifications.

## Instructions
- Run the auditor whenever a "status check" or "system health" report is requested.
- Ensure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are present in `.env`.