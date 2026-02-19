#!/usr/bin/env python3
"""
Model Recommendations Package - Recomendaciones de modelos NVIDIA para Global Skills.

Este paquete proporciona mapeo inteligente de skills a modelos NVIDIA,
optimizando costos y calidad según el tipo de tarea.

Usage:
    from model_recommendations import (
        get_recommended_model,
        get_cost_estimate,
        ModelType
    )

    model = get_recommended_model("security-auditor")
    cost = get_cost_estimate("security-auditor")
"""

__version__ = "1.0.0"

# Reutilizar ModelType del módulo nvidia
from scripts.nvidia.models import ModelType

# Importar mapeos
from .mappings import SKILL_MODEL_MAPPING, COST_MAP

# Importar funciones de recomendación
from .recommender import (
    get_recommended_model,
    get_model_for_task,
    get_cost_estimate,
    get_skills_by_model,
    print_model_recommendations,
    get_skills_by_tier,
    get_skills_by_cluster,
)

__all__ = [
    # Types
    "ModelType",
    # Mappings
    "SKILL_MODEL_MAPPING",
    "COST_MAP",
    # Functions
    "get_recommended_model",
    "get_model_for_task",
    "get_cost_estimate",
    "get_skills_by_model",
    "get_skills_by_tier",
    "get_skills_by_cluster",
    "print_model_recommendations",
]
