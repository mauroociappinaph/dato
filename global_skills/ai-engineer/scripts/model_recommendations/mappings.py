#!/usr/bin/env python3
"""
Model Recommendations Mappings - Aggregator.
Refactored to meet the 300-line modularity rule.
"""

from typing import Dict, List
from scripts.nvidia.models import ModelType

# Mapeos por clúster (importados de módulos separados)
from .cluster_mappings.data_ai import DATA_AI_MAPPINGS
from .cluster_mappings.security import SECURITY_MAPPINGS
from .cluster_mappings.dev_ops_infra import DEV_OPS_INFRA_MAPPINGS
from .cluster_mappings.others import OTHER_CLUSTER_MAPPINGS

# Costo por tier
COST_MAP = {
    "ultra": 0.004,
    "high": 0.001,
    "medium": 0.0002,
    "low": 0.0001
}

# Categorías de clusters
CLUSTERS = {
    "DATA_AI", "SECURITY", "DEVELOPMENT", "INFRASTRUCTURE",
    "OPERATIONS", "BUSINESS", "KNOWLEDGE", "GOVERNANCE",
    "INTERFACE", "QUALITY_ASSURANCE", "DATABASE", "PLAYBOOK_ENGINE"
}

# Consolidación de Mapeos
SKILL_MODEL_MAPPING: Dict[str, Dict] = {}
SKILL_MODEL_MAPPING.update(DATA_AI_MAPPINGS)
SKILL_MODEL_MAPPING.update(SECURITY_MAPPINGS)
SKILL_MODEL_MAPPING.update(DEV_OPS_INFRA_MAPPINGS)
SKILL_MODEL_MAPPING.update(OTHER_CLUSTER_MAPPINGS)

# Helper para obtener recomendación
def get_recommendation(skill_id: str) -> Dict:
    return SKILL_MODEL_MAPPING.get(skill_id, {
        "model": ModelType.LLAMA_8B,
        "reasoning": "Modelo default por falta de mapeo específico",
        "cost_tier": "medium",
        "cluster": "UNKNOWN"
    })
