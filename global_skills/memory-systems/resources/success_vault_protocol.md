---
name: success-vault-protocol
description: Rules for archiving strategic insights and architectural wins in the hybrid memory system.
---

# Success Vault: The Corporate Brain

## Objective
To ensure that "Lessons Learned" and "Benchmarking Wins" are not lost between projects. This knowledge is stored in Pinecone (Vector) for semantic retrieval and Redis (Graph) for structural relationships.

## What to Archive
1.  **Benchmarking Wins:** Successful UX patterns, trendy features, and competitive advantages discovered in Step 1.
2.  **Architectural Decisions:** Stack combinations that proved efficient (e.g., Next.js + Tailwind + Redis).
3.  **Technical Fixes:** Solutions to complex bugs (e.g., Google Slides API payload corrections).
4.  **Token Economies:** Effective prompt compression strategies that saved costs.

## Retrieval Trigger
At the start of **every new project (Paso 0)**, the Orchestrator MUST query the Success Vault:
- "Find top 3 successful patterns for [Project Type]"
- "Retrieve previous fixes for [API/Tool Name]"

## Storage Commands (via Dude-Memory-Engine)
- `store_strategic_insight(text, category, project_source)`
- `link_success_to_entity(entity, success_description)`
