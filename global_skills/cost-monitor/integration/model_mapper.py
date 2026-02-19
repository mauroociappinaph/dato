#!/usr/bin/env python3
"""
Skill Model Mapper - Mapeo de Skills a Modelos NVIDIA

Este módulo mapea cada skill al modelo NVIDIA recomendado basado en su
tier de costo y complejidad.
"""

from typing import Dict, Optional
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuración de modelo para un skill"""
    model_name: str
    tier: str
    cost_per_1k_tokens: float
    description: str


class SkillModelMapper:
    """
    Mapea skills a modelos NVIDIA según su tier de costo.

    Basado en el análisis de complejidad y requisitos de cada skill,
    determina el modelo óptimo balanceando calidad y costo.
    """

    # Mapeo de tiers a modelos
    TIER_MODELS = {
        "ultra": {
            "model": "nvidia/nemotron-4-340b-instruct",
            "cost_per_1k": 0.004,
            "description": "Razonamiento complejo, seguridad crítica"
        },
        "high": {
            "model": "meta/llama-3.1-70b-instruct",
            "cost_per_1k": 0.001,
            "description": "Balance calidad/velocidad"
        },
        "medium": {
            "model": "meta/llama-3.1-8b-instruct",
            "cost_per_1k": 0.0002,
            "description": "Tareas operacionales"
        },
        "low": {
            "model": "meta/llama-3.2-3b-instruct",
            "cost_per_1k": 0.0001,
            "description": "Low-latency routing"
        }
    }

    # Mapeo específico de skills (del análisis previo)
    SKILL_TIER_MAP = {
        # Ultra Tier
        "security-auditor": "ultra",
        "agi-coordinator": "ultra",
        "hardening-auditor": "ultra",
        "secrets-vault-orchestrator": "ultra",
        "playbook_engine": "ultra",
        "neural-architecture-optimizer": "ultra",

        # High Tier
        "meta-learning-engine": "high",
        "rag-implementation": "high",
        "context-manager": "high",
        "prompt-optimizer-dspy": "high",
        "ai-engineer": "high",
        "mcp-vetting-guard": "high",
        "code-review-excellence": "high",
        "code-modularity-architect": "high",
        "typescript-pro": "high",
        "debugging-strategies": "high",
        "legacy-modernizer": "high",
        "subagent-driven-development": "high",
        "infrastructure-as-code-expert": "high",
        "reliability-sre-pilot": "high",
        "devops-troubleshooter": "high",
        "self-correction-pilot": "high",
        "agent-optimizer": "high",
        "marketing-psychology": "high",
        "pricing-strategy": "high",
        "brand-identity": "high",
        "reddit-strategic-insights": "high",
        "stripe-integration": "high",
        "payment-integration": "high",
        "smart-contract-developer": "high",
        "memory-systems": "high",
        "post-mortem-memory": "high",
        "architecture-decision-historian": "high",
        "docs-technical-writer": "high",
        "project-orchestrator-pm": "high",
        "google-slides-visual-creator": "high",
        "visual-learning-engine": "high",
        "agent-evaluation": "high",
        "technical-debt-analysis": "high",
        "database-performance-tuner": "high",
        "compliance-legal-sentinel": "high",

        # Medium Tier (default para la mayoría)
        "vector-index-tuning": "medium",
        "git-workflow-hardener": "medium",
        "semantic-code-navigator": "medium",
        "monorepo-management": "medium",
        "error-handling-patterns": "medium",
        "python-patterns": "medium",
        "deploy-automation-pilot": "medium",
        "github-actions-mechanic": "medium",
        "docker-hub-autonomous": "medium",
        "git-flow-sentinel": "medium",
        "github-master": "medium",
        "infrastructure-core": "medium",
        "observability-engineer": "medium",
        "performance-optimization-pilot": "medium",
        "cost-control": "medium",
        "ephemeral-env-manager": "medium",
        "latency-optimizer": "medium",
        "apify-lead-hunter": "medium",
        "telegram-bot-builder": "medium",
        "telegram-mini-app": "medium",
        "twilio-communications": "medium",
        "seo-technical-master": "medium",
        "sop-workflow-standardizer": "medium",
        "financial-controller": "medium",
        "token-accountant": "medium",
        "corporate-health-auditor": "medium",
        "skill-registry-manager": "medium",
        "web-command-center": "medium",
        "telegram-hq-commander": "medium",
        "api-endpoint-tester": "medium",
        "agentic-stress-tester": "medium",
        "verification-before-completion": "medium",
        "acceptance-criteria-guardian": "medium",
        "data-quality-frameworks": "medium",
        "supabase-admin-tool": "medium",

        # Low Tier
        "detect-duplicate-files": "low",
        "domain-strategy-router": "low",
        "environment-cleanup-specialist": "low",
        "run-automation": "low",
        "project-naming-enforcer": "low",
    }

    def __init__(self):
        """Inicializa el mapper con configuración por defecto"""
        self.default_tier = "medium"

    def get_tier_for_skill(self, skill_name: str) -> str:
        """
        Obtiene el tier de costo para un skill.

        Args:
            skill_name: Nombre del skill

        Returns:
            Tier del skill (ultra, high, medium, low)
        """
        return self.SKILL_TIER_MAP.get(skill_name, self.default_tier)

    def get_model_for_skill(self, skill_name: str) -> ModelConfig:
        """
        Obtiene la configuración de modelo para un skill.

        Args:
            skill_name: Nombre del skill

        Returns:
            ModelConfig con el modelo recomendado
        """
        tier = self.get_tier_for_skill(skill_name)
        tier_config = self.TIER_MODELS.get(tier, self.TIER_MODELS["medium"])

        return ModelConfig(
            model_name=tier_config["model"],
            tier=tier,
            cost_per_1k_tokens=tier_config["cost_per_1k"],
            description=tier_config["description"]
        )

    def get_model_name(self, skill_name: str) -> str:
        """
        Obtiene solo el nombre del modelo para un skill.

        Args:
            skill_name: Nombre del skill

        Returns:
            Nombre del modelo NVIDIA
        """
        return self.get_model_for_skill(skill_name).model_name

    def estimate_cost(self, skill_name: str, tokens_input: int, tokens_output: int) -> float:
        """
        Estima el costo de una ejecución.

        Args:
            skill_name: Nombre del skill
            tokens_input: Tokens de entrada
            tokens_output: Tokens de salida

        Returns:
            Costo estimado en USD
        """
        config = self.get_model_for_skill(skill_name)
        total_tokens = tokens_input + tokens_output
        cost_per_token = config.cost_per_1k_tokens / 1000
        return total_tokens * cost_per_token

    def get_all_skills_for_tier(self, tier: str) -> list:
        """
        Obtiene todos los skills de un tier específico.

        Args:
            tier: Tier a filtrar (ultra, high, medium, low)

        Returns:
            Lista de nombres de skills
        """
        return [
            skill for skill, skill_tier in self.SKILL_TIER_MAP.items()
            if skill_tier == tier
        ]


# Instancia global para uso conveniente
_default_mapper = None


def get_model_for_skill(skill_name: str) -> str:
    """
    Función de conveniencia para obtener el modelo de un skill.

    Args:
        skill_name: Nombre del skill

    Returns:
        Nombre del modelo NVIDIA
    """
    global _default_mapper
    if _default_mapper is None:
        _default_mapper = SkillModelMapper()
    return _default_mapper.get_model_name(skill_name)


def estimate_skill_cost(skill_name: str, tokens_input: int, tokens_output: int) -> float:
    """
    Función de conveniencia para estimar costo de un skill.

    Args:
        skill_name: Nombre del skill
        tokens_input: Tokens de entrada
        tokens_output: Tokens de salida

    Returns:
        Costo estimado en USD
    """
    global _default_mapper
    if _default_mapper is None:
        _default_mapper = SkillModelMapper()
    return _default_mapper.estimate_cost(skill_name, tokens_input, tokens_output)
