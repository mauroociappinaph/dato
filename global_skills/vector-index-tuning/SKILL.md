---
name: vector-index-tuning
description: Optimization of HNSW, Quantization, and search performance. 2026 Edition.
inherited_from: [ai-engineer, gemini-skill-creator]
---

# Vector Index Tuning (Compressed)

## Purpose
Ensure sub-millisecond latency and high recall for the Sovereign Agent Cloud. Act as the technical guardian of the `dude-central-brain` in Pinecone.

## Central Brain Monitoring (2026)
- **Target**: `dude-central-brain` (Pinecone).
- **Metric**: Monitor Latency (p95 < 100ms) and Recall (> 95%).
- **Action**: Suggest re-indexing or quantization if performance drifts.

## Index Selection Matrix
- **< 100K vectors**: HNSW (M=16, efC=100).
- **100K - 1M**: HNSW (M=32, efC=200).
- **> 1M**: HNSW + Scalar Quantization (INT8).
- **> 10M**: Product Quantization (PQ).

## HNSW Parameters
| Param | Default | Effect |
| :--- | :--- | :--- |
| **M** | 16 | Connections per node. ↑ = Better recall, ↑ RAM. |
| **efConstruction** | 100 | Build quality. ↑ = Better index, ↓ Build speed. |
| **efSearch** | 128 | Search quality. ↑ = Better recall, ↓ Speed. |

## Quantization (Memory Savings)
- **FP16**: 50% saving vs FP32.
- **INT8 Scalar**: 75% saving.
- **PQ**: > 90% saving (Approximate search).

## Rules (Mandatory)
1. **Benchmark First**: Never tune without a baseline measurement.
2. **Quantize Large Only**: Apply quantization only if index exceeds 1GB.
3. **Rescore Strategy**: If using quantization, use `rescore=true` for final top-k.