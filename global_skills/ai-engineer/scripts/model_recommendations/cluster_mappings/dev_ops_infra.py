from scripts.nvidia.models import ModelType

DEV_OPS_INFRA_MAPPINGS = {
    # DEVELOPMENT
    "code-review-excellence": {
        "model": ModelType.CODELLAMA_70B,
        "reasoning": "Especializado en código",
        "cost_tier": "high",
        "cluster": "DEVELOPMENT"
    },
    "code-modularity-architect": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Arquitectura de código",
        "cost_tier": "high",
        "cluster": "DEVELOPMENT"
    },
    "typescript-pro": {
        "model": ModelType.CODELLAMA_70B,
        "reasoning": "Tipos complejos de TypeScript",
        "cost_tier": "high",
        "cluster": "DEVELOPMENT"
    },
    "semantic-code-navigator": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Navegación rápida de código",
        "cost_tier": "medium",
        "cluster": "DEVELOPMENT"
    },
    "debugging-strategies": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Análisis de debugging complejo",
        "cost_tier": "high",
        "cluster": "DEVELOPMENT"
    },
    "legacy-modernizer": {
        "model": ModelType.CODELLAMA_70B,
        "reasoning": "Migración y refactorización",
        "cost_tier": "high",
        "cluster": "DEVELOPMENT"
    },
    "monorepo-management": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Gestión de dependencias",
        "cost_tier": "medium",
        "cluster": "DEVELOPMENT"
    },
    "error-handling-patterns": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Patrones de error estándar",
        "cost_tier": "medium",
        "cluster": "DEVELOPMENT"
    },
    "python-patterns": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Patrones Python estándar",
        "cost_tier": "medium",
        "cluster": "DEVELOPMENT"
    },
    "detect-duplicate-files": {
        "model": ModelType.LLAMA_3B,
        "reasoning": "Tarea simple de detección",
        "cost_tier": "low",
        "cluster": "DEVELOPMENT"
    },
    "subagent-driven-development": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Arquitectura de subagentes",
        "cost_tier": "high",
        "cluster": "DEVELOPMENT"
    },
    "codebase-navigator": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Navegación de codebase",
        "cost_tier": "medium",
        "cluster": "DEVELOPMENT"
    },
    "i18n-localization-manager": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Gestión de internacionalización",
        "cost_tier": "medium",
        "cluster": "DEVELOPMENT"
    },

    # INFRASTRUCTURE
    "infrastructure-as-code-expert": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Arquitectura cloud compleja",
        "cost_tier": "high",
        "cluster": "INFRASTRUCTURE"
    },
    "deploy-automation-pilot": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Despliegues automatizados",
        "cost_tier": "medium",
        "cluster": "INFRASTRUCTURE"
    },
    "github-actions-mechanic": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "CI/CD workflows",
        "cost_tier": "medium",
        "cluster": "INFRASTRUCTURE"
    },
    "docker-hub-autonomous": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Análisis de imágenes Docker",
        "cost_tier": "medium",
        "cluster": "INFRASTRUCTURE"
    },
    "git-flow-sentinel": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Reglas de git",
        "cost_tier": "medium",
        "cluster": "INFRASTRUCTURE"
    },
    "github-master": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Operaciones GitHub",
        "cost_tier": "medium",
        "cluster": "INFRASTRUCTURE"
    },
    "infrastructure-core": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Abstracciones de infraestructura",
        "cost_tier": "medium",
        "cluster": "INFRASTRUCTURE"
    },
    "github-actions-guardian": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Validación de workflows GitHub",
        "cost_tier": "medium",
        "cluster": "INFRASTRUCTURE"
    },
    "git-advanced-workflows": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Workflows Git avanzados",
        "cost_tier": "medium",
        "cluster": "INFRASTRUCTURE"
    },

    # OPERATIONS
    "reliability-sre-pilot": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Análisis de confiabilidad",
        "cost_tier": "high",
        "cluster": "OPERATIONS"
    },
    "devops-troubleshooter": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Resolución de incidentes",
        "cost_tier": "high",
        "cluster": "OPERATIONS"
    },
    "observability-engineer": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Monitoreo y logs",
        "cost_tier": "medium",
        "cluster": "OPERATIONS"
    },
    "self-correction-pilot": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Autocorrección inteligente",
        "cost_tier": "high",
        "cluster": "OPERATIONS"
    },
    "performance-optimization-pilot": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Optimización de performance",
        "cost_tier": "medium",
        "cluster": "OPERATIONS"
    },
    "cost-control": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Control de costos",
        "cost_tier": "medium",
        "cluster": "OPERATIONS"
    },
    "domain-strategy-router": {
        "model": ModelType.LLAMA_3B,
        "reasoning": "Ruteo rápido - baja latencia requerida",
        "cost_tier": "low",
        "cluster": "OPERATIONS"
    },
    "ephemeral-env-manager": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Gestión de entornos",
        "cost_tier": "medium",
        "cluster": "OPERATIONS"
    },
    "environment-cleanup-specialist": {
        "model": ModelType.LLAMA_3B,
        "reasoning": "Limpieza de archivos",
        "cost_tier": "low",
        "cluster": "OPERATIONS"
    },
    "latency-optimizer": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Optimización de latencia",
        "cost_tier": "medium",
        "cluster": "OPERATIONS"
    },
    "run-automation": {
        "model": ModelType.LLAMA_3B,
        "reasoning": "Ejecución de scripts",
        "cost_tier": "low",
        "cluster": "OPERATIONS"
    },
    "agent-optimizer": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Optimización de agentes",
        "cost_tier": "high",
        "cluster": "OPERATIONS"
    },
    "blast-radius-analyst": {
        "model": ModelType.LLAMA_70B,
        "reasoning": "Análisis de impacto de cambios",
        "cost_tier": "high",
        "cluster": "OPERATIONS"
    },
    "asynchronous-jules-helper": {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Asistencia asíncrona",
        "cost_tier": "medium",
        "cluster": "OPERATIONS"
    },
}
