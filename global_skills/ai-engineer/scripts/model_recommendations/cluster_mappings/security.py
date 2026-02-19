from scripts.nvidia.models import ModelType

SECURITY_MAPPINGS = {
    "security-auditor": {
        "model": ModelType.NEMOTRON_340B,
        "reasoning": "Análisis de seguridad crítico - no puede fallar",
        "cost_tier": "ultra",
        "cluster": "SECURITY"
    },
    "hardening-auditor": {
        "model": ModelType.LLAMA_405B,
        "reasoning": "Hardening de producción - máxima calidad",
        "cost_tier": "ultra",
        "cluster": "SECURITY"
    },
    "mcp-vetting-guard": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Validación de seguridad de salidas",
        "cost_tier": "high",
        "cluster": "SECURITY"
    },
    "secrets-vault-orchestrator": {
        "model": ModelType.NEMOTRON_340B,
        "reasoning": "Manejo de secretos - crítico",
        "cost_tier": "ultra",
        "cluster": "SECURITY"
    },
    "compliance-legal-sentinel": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Análisis legal y compliance",
        "cost_tier": "high",
        "cluster": "SECURITY"
    },
    "git-workflow-hardener": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Reglas de seguridad predecibles",
        "cost_tier": "medium",
        "cluster": "SECURITY"
    },
}
