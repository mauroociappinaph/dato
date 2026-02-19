---
name: rag-implementation
description: Knowledge-grounded AI systems using vector databases. 2026 Edition.
inherited_from: [ai-engineer, gemini-skill-creator]
---

# RAG Implementation (Compressed)

## Purpose
Build Retrieval-Augmented Generation systems to provide grounded, factual, and accurate LLM responses.

## Core Engine (Mandatory)
- **Primary Database**: **Central Vector Memory (dude-central-brain)** in Pinecone.
- **Embedding Model**: `llama-text-embed-v2` (1024 dims).
- **Search Type**: Hybrid (Dense + Sparse) with reranking.

## Pipeline Steps
1. **Chunking**: Recursive splitting (500-1000 tokens) with 15% overlap.
2. **Indexing**: Include metadata (source, timestamp, category) for filtering.
3. **Retrieval**: Use MMR (Maximal Marginal Relevance) for diversity.
4. **Reranking**: Apply Cross-Encoders or Cohere Rerank for precision.
5. **Generation**: Use grounded prompts with explicit source citations.

## Retrieval Strategies
- **Multi-Query**: Generate query variations to improve recall.
- **Parent Document**: Retrieve small chunks but feed large parent context.
- **Contextual Compression**: Extract only relevant snippets before feeding LLM.

## Rules
- **Anti-Hallucination**: If context is insufficient, reply "I don't have enough information."
- **Efficiency**: Use `dude-central-brain` namespace isolation to minimize search noise.