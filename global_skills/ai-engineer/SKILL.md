---
name: ai-engineer
description: Production LLM apps, RAG, and Agentic workflows. 2026 Edition.
inherited_from: [Gemini Skill Creator, Error Handling, Debugging]
---

# AI Engineer (Compressed)

## Purpose
Build scalable, secure, and cost-effective AI systems. Transition from simple prompts to resilient intelligence architectures.

## Core Objectives
- **LLM Ops**: Integration with NVIDIA NIM, GPT-4o, Claude 4.5, Llama 3.2.
- **MCP-First**: Prioritize **Model Context Protocol** for tool and data access.
- **Advanced RAG**: Hybrid search, reranking, and GraphRAG.
- **Orchestration**: LangGraph, CrewAI, AutoGen workflows.
- **Observability**: Tracing (LangSmith/Phoenix), evaluation metrics.
- **Schmidhuber Optimization**: Natural gradients, meta-learning, and AGI architectures.

## NVIDIA NIM Integration

### Available Models
- `meta/llama-3.1-8b-instruct` - Fast reasoning (default)
- `meta/llama-3.1-70b-instruct` - High quality
- `nvidia/nemotron-4-340b-instruct` - Best reasoning
- `mistralai/mistral-7b-instruct-v0.3` - Efficient

### Usage
```python
from scripts.nvidia_nim_client import NVIDIANIMClient, ModelType

client = NVIDIANIMClient()
response = client.generate("Explain quantum computing", model=ModelType.LLAMA_3_1_8B)
print(response.text)
print(f"Tokens used: {response.tokens_used}")
```

### Fallback Strategy
NVIDIA NIM → Ollama (local) → Error

## Protocols
1. **Financial**: Optimize token usage; select model size based on task complexity.
2. **Security**: Prevent prompt injection and ensure PII governance.
3. **Evaluation**: Use quantitative metrics over qualitative hypotheses.
