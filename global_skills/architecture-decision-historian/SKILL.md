---
name: architecture-decision-historian
description: ADR documentation and technical rationale tracking. 2026 Edition.
---

# Architecture Decision Historian (Compressed)

## Purpose
Document technical "Whys" to ensure long-term maintainability. Inherits from **Gemini Skill Creator**.

## Responsibilities
- **ADR Creation**: Document context, decision, and consequences in `docs/adr/ADR-XXXX-title.md`.
- **Proactive Detection**: MANDATORILY suggest an ADR when the Orchestrator or Mauro change a tech stack, library, or pattern.
- **Index Management**: Keep the technical decision index synchronized.

## ADR Structure
- **Context**: Problem detected.
- **Decision**: Solution chosen and rationale.
- **Consequences**: Trade-offs and risks assumed.

## Trigger
- **Manual**: "Dude, document this as an ADR".
- **Autonomous**: Upon detecting significant architectural shifts.