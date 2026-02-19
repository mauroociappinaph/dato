from scripts.nvidia.models import ModelType

DATA_AI_MAPPINGS = {
    "meta-learning-engine": {
        "model": ModelType.NEMOTRON_340B,
        "reasoning": "Razonamiento complejo para meta-learning y auto-optimización",
        "cost_tier": "high",
        "cluster": "DATA_AI"
    },
    "agi-coordinator": {
        "model": ModelType.LLAMA_405B,
        "reasoning": "Máxima capacidad para coordinación AGI",
        "cost_tier": "ultra",
        "cluster": "DATA_AI"
    },
    "rag-implementation": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Balance para RAG híbrido",
        "cost_tier": "high",
        "cluster": "DATA_AI"
    },
    "context-manager": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Ingeniería de contexto dinámico",
        "cost_tier": "high",
        "cluster": "DATA_AI"
    },
    "neural-architecture-optimizer": {
        "model": ModelType.NEMOTRON_340B,
        "reasoning": "Optimización arquitectural compleja",
        "cost_tier": "ultra",
        "cluster": "DATA_AI"
    },
    "prompt-optimizer-dspy": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Optimización matemática de prompts",
        "cost_tier": "high",
        "cluster": "DATA_AI"
    },
    "vector-index-tuning": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Técnico pero no requiere razonamiento profundo",
        "cost_tier": "medium",
        "cluster": "DATA_AI"
    },
    "ai-engineer": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Arquitectura de sistemas de IA",
        "cost_tier": "high",
        "cluster": "DATA_AI"
    },
    "gemini-skill-creator": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Creación de skills especializados",
        "cost_tier": "high",
        "cluster": "DATA_AI"
    },
    "instruction-compressor": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Compresión de instrucciones",
        "cost_tier": "medium",
        "cluster": "DATA_AI"
    },
    "langgraph-director": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Orquestación de flujos LangGraph",
        "cost_tier": "high",
        "cluster": "DATA_AI"
    },
    "master-rag-2026": {
        "model": ModelType.NEMOTRON_340B,
        "reasoning": "RAG avanzado 2026",
        "cost_tier": "ultra",
        "cluster": "DATA_AI"
    },
    "rag-auto-indexer": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Indexación automática RAG",
        "cost_tier": "high",
        "cluster": "DATA_AI"
    },
}
