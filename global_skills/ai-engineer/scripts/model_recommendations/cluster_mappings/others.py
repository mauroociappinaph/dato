from scripts.nvidia.models import ModelType

OTHER_CLUSTER_MAPPINGS = {
    # BUSINESS
    "marketing-psychology": {
        "model": ModelType.LLAMA_70B, "reasoning": "Psicología y creatividad", "cost_tier": "high", "cluster": "BUSINESS"
    },
    "pricing-strategy": {
        "model": ModelType.LLAMA_70B, "reasoning": "Estrategia de precios", "cost_tier": "high", "cluster": "BUSINESS"
    },
    "brand-identity": {
        "model": ModelType.LLAMA_70B, "reasoning": "Identidad de marca", "cost_tier": "high", "cluster": "BUSINESS"
    },
    "curacion_de_contenido": {
        "model": ModelType.LLAMA_8B, "reasoning": "Curación y análisis de contenido", "cost_tier": "medium", "cluster": "BUSINESS"
    },

    # KNOWLEDGE
    "memory-systems": {
        "model": ModelType.LLAMA_70B, "reasoning": "Diseño de sistemas de memoria", "cost_tier": "high", "cluster": "KNOWLEDGE"
    },
    "docs-technical-writer": {
        "model": ModelType.LLAMA_70B, "reasoning": "Escritura técnica", "cost_tier": "high", "cluster": "KNOWLEDGE"
    },

    # GOVERNANCE
    "financial-controller": {
        "model": ModelType.LLAMA_8B, "reasoning": "Control financiero", "cost_tier": "medium", "cluster": "GOVERNANCE"
    },
    "skill-registry-manager": {
        "model": ModelType.LLAMA_8B, "reasoning": "Gestión de registros", "cost_tier": "medium", "cluster": "GOVERNANCE"
    },

    # PLAYBOOK_ENGINE
    "playbook_engine": {
        "model": ModelType.NEMOTRON_340B, "reasoning": "Orquestación crítica del sistema", "cost_tier": "ultra", "cluster": "PLAYBOOK_ENGINE"
    },

    # DATABASE
    "database-performance-tuner": {
        "model": ModelType.LLAMA_70B, "reasoning": "Optimización de queries", "cost_tier": "high", "cluster": "DATABASE"
    },

    # QUALITY_ASSURANCE
    "technical-debt-analysis": {
        "model": ModelType.CODELLAMA_70B, "reasoning": "Análisis de deuda técnica", "cost_tier": "high", "cluster": "QUALITY_ASSURANCE"
    },
}
