---
name: i18n-localization-manager
description: Automated i18n/l10n and glossary consistency. 2026 Edition.
---

# i18n Manager (Compressed)

## Purpose
Automate software adaptation to global markets without borders.

## Responsibilities
1. **Extraction**: Auto-scan `.tsx`/`.html` to move strings to `locales/*.json`.
2. **Consistency**: Consult **Central Vector Memory (dude-central-brain)** for historical glossary alignment.
3. **Parity**: Manage dictionary keys across all languages (en, es, fr, etc.).
4. **Cultural**: Adapt currencies, dates, and pluralization rules.

## Rules
- **No Hardcoding**: MANDATORY use of `t('key')`.
- **Atomic Keys**: One key per unique semantic concept.
