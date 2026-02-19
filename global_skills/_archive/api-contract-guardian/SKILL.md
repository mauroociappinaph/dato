---
name: api-contract-guardian
description: OpenAPI governance and breaking change prevention. 2026 Edition.
---

# API Contract Guardian (Compressed)

## Purpose
Authority in API design. Ensure perfect compatibility between client and server via strict OpenAPI specs and SemVer.

## Rules (Mandatory)
1. **Contract-First**: Define `openapi.yaml` or DTOs before any implementation.
2. **No Breaking Changes**: Prohibited to remove fields or change types in existing versions. Use Versioning (`/v1` -> `/v2`).
3. **Standard Envelopes**: All responses must use the `{ data, meta, error }` structure.
4. **Semantic HTTP**: Use correct codes (201 for Created, 403 for Forbidden, etc.).

## Automation
- Use `openapi-generator` for auto-SDK creation.
- Validate DTOs with Swagger decorators.

## Trigger
Activate upon any endpoint design or DTO modification.
