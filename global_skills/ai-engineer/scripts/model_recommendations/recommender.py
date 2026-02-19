#!/usr/bin/env python3
"""
Model Recommendations Engine - Funciones de recomendación de modelos.

Este archivo contiene la lógica para recomendar modelos NVIDIA
según el skill, complejidad y tipo de tarea.
"""

from typing import Dict, List, Optional
from scripts.nvidia.models import ModelType
from .mappings import SKILL_MODEL_MAPPING, COST_MAP


def get_recommended_model(skill_name: str) -> ModelType:
    """
    Obtiene el modelo recomendado para un skill específico.

    Args:
        skill_name: Nombre del skill

    Returns:
        ModelType: Modelo NVIDIA recomendado
    """
    skill_config = SKILL_MODEL_MAPPING.get(skill_name)
    if skill_config:
        return skill_config["model"]

    # Fallback al modelo por defecto
    return ModelType.LLAMA_8B


def get_model_for_task(
    complexity: str,
    task_type: str = "general"
) -> ModelType:
    """
    Obtiene el modelo adecuado según complejidad y tipo de tarea.

    Args:
        complexity: "low", "medium", "high", "ultra"
        task_type: "general", "code", "reasoning", "creative", "fast"

    Returns:
        ModelType: Modelo recomendado
    """
    model_map = {
        ("ultra", "reasoning"): ModelType.NEMOTRON_340B,
        ("ultra", "general"): ModelType.LLAMA_405B,
        ("high", "code"): ModelType.CODELLAMA_70B,
        ("high", "reasoning"): ModelType.NEMOTRON_340B,
        ("high", "general"): ModelType.LLAMA_70B,
        ("medium", "code"): ModelType.DEEPSEEK_CODER,
        ("medium", "general"): ModelType.LLAMA_8B,
        ("low", "fast"): ModelType.LLAMA_3B,
        ("low", "general"): ModelType.LLAMA_3B,
    }

    return model_map.get((complexity, task_type), ModelType.LLAMA_8B)


def get_cost_estimate(skill_name: str) -> Dict:
    """
    Obtiene estimación de costo para un skill.

    Returns:
        Dict con costo estimado por request y tier
    """
    skill_config = SKILL_MODEL_MAPPING.get(skill_name)
    if not skill_config:
        return {
            "cost_per_1k_tokens": COST_MAP["medium"],
            "tier": "medium"
        }

    tier = skill_config.get("cost_tier", "medium")
    return {
        "cost_per_1k_tokens": COST_MAP.get(tier, COST_MAP["medium"]),
        "tier": tier,
        "model": skill_config["model"].value,
        "cluster": skill_config.get("cluster", "UNKNOWN")
    }


def get_skills_by_model(model: ModelType) -> List[str]:
    """
    Obtiene todos los skills que usan un modelo específico.

    Args:
        model: Modelo NVIDIA

    Returns:
        Lista de nombres de skills
    """
    return [
        skill_name
        for skill_name, config in SKILL_MODEL_MAPPING.items()
        if config["model"] == model
    ]


def get_skills_by_tier(tier: str) -> List[str]:
    """
    Obtiene todos los skills de un tier de costo específico.

    Args:
        tier: "ultra", "high", "medium", "low"

    Returns:
        Lista de nombres de skills
    """
    return [
        skill_name
        for skill_name, config in SKILL_MODEL_MAPPING.items()
        if config.get("cost_tier") == tier
    ]


def get_skills_by_cluster(cluster: str) -> List[str]:
    """
    Obtiene todos los skills de un cluster específico.

    Args:
        cluster: Nombre del cluster (e.g., "DATA_AI", "SECURITY")

    Returns:
        Lista de nombres de skills
    """
    return [
        skill_name
        for skill_name, config in SKILL_MODEL_MAPPING.items()
        if config.get("cluster") == cluster
    ]


def get_cluster_for_skill(skill_name: str) -> str:
    """
    Obtiene el cluster al que pertenece un skill.

    Args:
        skill_name: Nombre del skill

    Returns:
        Nombre del cluster o "UNKNOWN"
    """
    skill_config = SKILL_MODEL_MAPPING.get(skill_name)
    return skill_config.get("cluster", "UNKNOWN") if skill_config else "UNKNOWN"


def print_model_recommendations():
    """Imprime un resumen de recomendaciones por categoría."""
    print("=" * 80)
    print("🤖 NVIDIA MODEL RECOMMENDATIONS FOR GLOBAL SKILLS")
    print("=" * 80)

    # Agrupar por tier de costo
    tiers = {"ultra": [], "high": [], "medium": [], "low": []}
    for skill, config in SKILL_MODEL_MAPPING.items():
        tier = config.get("cost_tier", "medium")
        cluster = config.get("cluster", "UNKNOWN")
        tiers[tier].append((skill, config, cluster))

    for tier_name, skills in tiers.items():
        if skills:
            print(f"\n📊 {tier_name.upper()} COST TIER")
            print("-" * 80)
            # Agrupar por cluster dentro del tier
            by_cluster = {}
            for skill, config, cluster in skills:
                by_cluster.setdefault(cluster, []).append((skill, config))

            for cluster, cluster_skills in sorted(by_cluster.items()):
                print(f"\n  📁 {cluster}:")
                for skill, config in cluster_skills:
                    print(f"    • {skill}")
                    print(f"      Model: {config['model'].value}")
                    print(f"      Reason: {config['reasoning']}")


def get_total_skills_count() -> int:
    """Retorna el número total de skills mapeados."""
    return len(SKILL_MODEL_MAPPING)


def get_skills_count_by_cluster() -> Dict[str, int]:
    """Retorna conteo de skills por cluster."""
    counts = {}
    for config in SKILL_MODEL_MAPPING.values():
        cluster = config.get("cluster", "UNKNOWN")
        counts[cluster] = counts.get(cluster, 0) + 1
    return counts


def estimate_cost_for_execution(
    skill_name: str,
    estimated_tokens: int = 1000
) -> float:
    """
    Estima el costo de una ejecución.

    Args:
        skill_name: Nombre del skill
        estimated_tokens: Tokens estimados (default: 1000)

    Returns:
        Costo estimado en USD
    """
    cost_info = get_cost_estimate(skill_name)
    cost_per_1k = cost_info["cost_per_1k_tokens"]
    return (estimated_tokens / 1000) * cost_per_1k
