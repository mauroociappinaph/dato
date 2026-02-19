---
name: memory-systems
description: Persistence layer design for agent continuity. 2026 Edition.
---

# Memory Systems (Compressed)

## Purpose
Enable agents to maintain continuity and reason over historical knowledge. Prevents "state loss" across sessions and ensures entity consistency.

## Layered Architecture (2026)
1.  **Layer 1: Working Memory**: Context window (volatile, zero latency).
2.  **Layer 2: Short-Term**: Redis-based session storage (volatile, fast).
3.  **Layer 3: Central Brain**: **Central Vector Memory (dude-central-brain)** in Pinecone (cross-session persistent, semantic).
4.  **Layer 4: Entity Memory**: Temporal knowledge graphs for tracking state changes over time.

## Schmidhuber Neural Compression (Phase 2)
- **Compression Algorithm**: Implementar algoritmos de compresión neuronal inspirados en Schmidhuber
- **Meta-Memory**: Sistema de memoria que organiza y optimiza el almacenamiento inteligente
- **Adaptive Storage**: Almacenamiento que se adapta basado en importancia y frecuencia de uso
- **Recursive Optimization**: La memoria se optimiza a sí misma para máxima eficiencia

## Central Memory Engine (Mandatory)
- **Engine**: Pinecone (Namespace: `skills-knowledge`).
- **Workflow**:
    1. **Extract**: Identify new learning or successful patterns.
    2. **Embed**: Use **llama-text-embed-v2**.
    3. **Index**: Upsert to `dude-central-brain`.
    4. **Query**: Perform semantic search during planning.

## Retrieval Patterns
- **Semantic**: Search by meaning/intention.
- **Temporal**: Filter by "valid from/until" timestamps.
- **Relational**: Traverse entity links (A works with B).

## Rules
- **Consolidation**: Periodically merge related memories to prevent index bloat.
- **Privacy**: Redact PII before indexing in the Central Brain.
- **Grounding**: Always return source citations for retrieved memories.
