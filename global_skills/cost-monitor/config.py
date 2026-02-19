#!/usr/bin/env python3
"""
Cost Monitor Configuration - Configuración del sistema de monitoreo de costos

Basado en los rates de NVIDIA NIM del proyecto The Dude.
"""

import os
from dataclasses import dataclass
from typing import Dict, List
from ..src.helpers import join_paths


@dataclass
class ModelCostConfig:
    """Configuración de costo para un modelo"""
    name: str
    cost_per_1k_tokens: float
    tier: str  # ultra, high, medium, low
    description: str


# Rates de costos por modelo NVIDIA (USD por 1K tokens)
COST_RATES = {
    # Ultra Tier - $0.004 por 1K tokens
    "nvidia/nemotron-4-340b-instruct": ModelCostConfig(
        name="Nemotron 4 340B",
        cost_per_1k_tokens=0.004,
        tier="ultra",
        description="Razonamiento complejo, seguridad crítica"
    ),
    "meta/llama-3.1-405b-instruct": ModelCostConfig(
        name="Llama 3.1 405B",
        cost_per_1k_tokens=0.004,
        tier="ultra",
        description="AGI, hardening crítico"
    ),

    # High Tier - $0.001 por 1K tokens
    "meta/llama-3.1-70b-instruct": ModelCostConfig(
        name="Llama 3.1 70B",
        cost_per_1k_tokens=0.001,
        tier="high",
        description="Balance calidad/velocidad"
    ),
    "meta/codellama-70b": ModelCostConfig(
        name="CodeLlama 70B",
        cost_per_1k_tokens=0.001,
        tier="high",
        description="Código especializado"
    ),

    # Medium Tier - $0.0002 por 1K tokens
    "meta/llama-3.1-8b-instruct": ModelCostConfig(
        name="Llama 3.1 8B",
        cost_per_1k_tokens=0.0002,
        tier="medium",
        description="Tareas operacionales"
    ),

    # Low Tier - $0.0001 por 1K tokens
    "meta/llama-3.2-3b-instruct": ModelCostConfig(
        name="Llama 3.2 3B",
        cost_per_1k_tokens=0.0001,
        tier="low",
        description="Low-latency routing"
    ),
}

# Modelos fallback si no se encuentra el rate
DEFAULT_COST_PER_TOKEN = 0.000001  # $0.001 por 1K tokens (high tier)

# Configuración de base de datos
DATABASE_CONFIG = {
    "path": os.path.join(os.path.dirname(__file__), "db", "cost_monitor.db"),
    "backup_interval_hours": 24,
}

# Configuración de alertas
ALERT_CONFIG = {
    "default_thresholds": [50, 75, 90, 100],  # % del presupuesto
    "check_interval_minutes": 5,
    "cooldown_minutes": 30,  # Entre alertas del mismo tipo
}

# Configuración de dashboard
DASHBOARD_CONFIG = {
    "host": "0.0.0.0",
    "port": 8080,
    "refresh_interval_seconds": 30,
    "max_history_days": 90,
}

# Canales de notificación disponibles
NOTIFICATION_CHANNELS = ["telegram", "email", "dashboard", "log"]


def get_model_cost_config(model_name: str) -> ModelCostConfig:
    """Obtiene la configuración de costo para un modelo"""
    return COST_RATES.get(model_name, ModelCostConfig(
        name=model_name,
        cost_per_1k_tokens=DEFAULT_COST_PER_TOKEN * 1000,
        tier="unknown",
        description="Modelo no configurado"
    ))


def calculate_cost(model_name: str, tokens_input: int, tokens_output: int) -> float:
    """
    Calcula el costo de una ejecución basado en el modelo y tokens usados.

    Args:
        model_name: Nombre del modelo usado
        tokens_input: Número de tokens de entrada
        tokens_output: Número de tokens de salida

    Returns:
        Costo en USD
    """
    config = get_model_cost_config(model_name)
    total_tokens = tokens_input + tokens_output
    cost_per_token = config.cost_per_1k_tokens / 1000
    return total_tokens * cost_per_token


def get_tier_for_skill(skill_name: str) -> str:
    """
    Obtiene el tier de costo para un skill basado en el registro.
    Esta función se integrará con skill_registry.json
    """
    # TODO: Cargar desde skill_registry.json
    # Por ahora, mapeo básico basado en el análisis previo
    ultra_skills = [
        "security-auditor", "agi-coordinator", "hardening-auditor",
        "secrets-vault-orchestrator", "playbook_engine", "neural-architecture-optimizer"
    ]

    high_skills = [
        "meta-learning-engine", "rag-implementation", "context-manager",
        "prompt-optimizer-dspy", "ai-engineer", "mcp-vetting-guard",
        "code-review-excellence", "database-performance-tuner"
    ]

    low_skills = [
        "detect-duplicate-files", "domain-strategy-router",
        "environment-cleanup-specialist", "run-automation", "project-naming-enforcer"
    ]

    if skill_name in ultra_skills:
        return "ultra"
    elif skill_name in high_skills:
        return "high"
    elif skill_name in low_skills:
        return "low"
    else:
        return "medium"  # Default


def get_recommended_model_for_skill(skill_name: str) -> str:
    """Obtiene el modelo recomendado para un skill"""
    tier = get_tier_for_skill(skill_name)

    tier_models = {
        "ultra": "nvidia/nemotron-4-340b-instruct",
        "high": "meta/llama-3.1-70b-instruct",
        "medium": "meta/llama-3.1-8b-instruct",
        "low": "meta/llama-3.2-3b-instruct"
    }

    return tier_models.get(tier, "meta/llama-3.1-8b-instruct")
