---
name: skill-registry-manager
description: Global skill to manage the THE DUDE Skill Registry, clusters, and redirects.
---

# Skill Registry Manager

## Objective
To provide a secure and standard way for agents to update, deprecate, or re-cluster skills within the global `skill_registry.json`.

## Capabilities
1. **Cataloging**: Add new skills to the registry.
2. **Deprecation**: Mark skills as obsolete and define a `redirect_to` target.
3. **Clustering**: Move skills between functional clústeres (ej. `SECURITY`, `DEVELOPMENT`).
4. **Validation**: Ensure the JSON schema remains intact.
5. **Enhanced Fields Management**: Handle new fields (`inputs`, `outputs`, `cost_estimate`, `preferred_agent`).

## New Fields Support
- **inputs**: Define input schema for skill interfaces
- **outputs**: Define output schema for skill contracts
- **cost_estimate**: Specify execution cost and complexity
- **preferred_agent**: Assign optimal agent for skill execution

## Instructions
- Always load the registry from `/Users/mauroociappina/.gemini/anti_gravity/global_skills/skill_registry.json`.
- When adding a skill, ensure the `path` and `id` are correct.
- Set versioning using SemVer (1.0.0 for new skills).
- For new fields, use the following schema:
  ```json
  {
    "inputs": {
      "field_name": "field_type"
    },
    "outputs": {
      "field_name": "field_type"
    },
    "cost_estimate": {
      "per_execution": 0.05,
      "currency": "USD",
      "complexity_factor": "medium"
    },
    "preferred_agent": "AGENT_NAME"
  }
  ```
