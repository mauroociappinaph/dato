#!/usr/bin/env python3
"""
Model Recommendations - Backward Compatibility Layer

⚠️ DEPRECATED: Este archivo se mantiene solo para compatibilidad.
Por favor usa el nuevo módulo modular:

    from model_recommendations import (
        get_recommended_model,
        get_cost_estimate,
        ModelType
    )

El nuevo paquete modular proporciona:
- Mejor organización del código
- Testabilidad mejorada
- Separación de responsabilidades
- Funciones adicionales (get_skills_by_cluster, etc.)

Este archivo será removido en la versión 2.0.
"""

import warnings

# Emitir advertencia de deprecación
warnings.warn(
    "model_recommendations.py is deprecated. "
    "Use 'from model_recommendations import ...' instead. "
    "This module will be removed in version 2.0.",
    DeprecationWarning,
    stacklevel=2
)

# Re-exportar todo desde el nuevo módulo modular
from .model_recommendations import (
    # Types
    ModelType,
    # Mappings
    SKILL_MODEL_MAPPING,
    COST_MAP,
    # Functions
    get_recommended_model,
    get_model_for_task,
    get_cost_estimate,
    get_skills_by_model,
    print_model_recommendations,
    # New functions not in original but useful
    get_skills_by_tier,
    get_skills_by_cluster,
)

# Mantener compatibilidad con imports antiguos
__all__ = [
    "ModelType",
    "SKILL_MODEL_MAPPING",
    "get_recommended_model",
    "get_model_for_task",
    "get_cost_estimate",
    "get_skills_by_model",
    "print_model_recommendations",
]
