---
name: latency-optimizer
description: Expert in sub-second inference and token efficiency. 2026 Edition.
---

# Latency Optimizer

## Purpose
Minimize the time between user request and actionable result.

## Core Metrics
- **TTFT**: Time to First Token.
- **TPS**: Tokens Per Second.
- **End-to-End Latency**: Total pipeline time.

## Optimization Protocol
1. **Model Routing**: Use local small models (Llama 3.2 1B/3B) for classification.
2. **Context Pruning**: Use LLMLingua-2 to reduce prompt size.
3. **Semantic Caching**: Implement Redis-based semantic cache for redundant queries.
