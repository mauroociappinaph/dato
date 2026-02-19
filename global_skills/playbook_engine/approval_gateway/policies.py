#!/usr/bin/env python3
"""
Approval Gateway Policies - Sistema de políticas de aprobación.

Este archivo contiene la lógica para evaluar y aplicar
políticas de aprobación basadas en condiciones.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List

from .models import ApprovalPolicy

logger = logging.getLogger(__name__)


class PolicyEngine:
    """Motor de evaluación de políticas de aprobación"""

    def __init__(self):
        self.policies: List[ApprovalPolicy] = []
        self._load_default_policies()

    def _load_default_policies(self):
        """Carga políticas de aprobación por defecto"""
        default_policies = [
            ApprovalPolicy(
                policy_id="cost_threshold_policy",
                name="Cost Threshold Policy",
                description="Require approval for high-cost operations",
                conditions={
                    "type": "cost_threshold",
                    "threshold": 30.00
                },
                actions={
                    "action": "require_approval",
                    "approvers": ["admin", "manager"]
                },
                priority=1,
                enabled=True
            ),
            ApprovalPolicy(
                policy_id="time_window_policy",
                name="Time Window Policy",
                description="Restrict deployments to business hours",
                conditions={
                    "type": "time_window",
                    "allowed_hours": [9, 10, 11, 12, 13, 14, 15, 16, 17],
                    "allowed_days": ["monday", "tuesday", "wednesday", "thursday", "friday"]
                },
                actions={
                    "action": "require_approval",
                    "approvers": ["oncall"]
                },
                priority=2,
                enabled=True
            ),
            ApprovalPolicy(
                policy_id="production_deployment_policy",
                name="Production Deployment Policy",
                description="Require multiple approvals for production deployments",
                conditions={
                    "type": "environment",
                    "environments": ["production"]
                },
                actions={
                    "action": "require_approval",
                    "approvers": ["admin", "manager", "tech_lead"],
                    "quorum": 2
                },
                priority=3,
                enabled=True
            )
        ]

        self.policies.extend(default_policies)
        logger.info(f"Cargadas {len(default_policies)} políticas de aprobación por defecto")

    async def evaluate_policies(
        self,
        playbook_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> List[ApprovalPolicy]:
        """Evalúa políticas contra un playbook y contexto"""
        matching_policies = []

        for policy in self.policies:
            if not policy.enabled:
                continue

            if await self._policy_matches(policy, playbook_data, context):
                matching_policies.append(policy)

        # Ordenar por prioridad
        matching_policies.sort(key=lambda p: p.priority, reverse=True)
        return matching_policies

    async def _policy_matches(
        self,
        policy: ApprovalPolicy,
        playbook_data: Dict[str, Any],
        context: Dict[str, Any]
    ) -> bool:
        """Verifica si una política coincide con el playbook y contexto"""
        conditions = policy.conditions

        # Evaluar condiciones de costo
        if conditions.get('type') == 'cost_threshold':
            threshold = conditions.get('threshold', 0.0)
            total_cost = await self._calculate_playbook_cost(playbook_data)
            if total_cost >= threshold:
                return True

        # Evaluar condiciones de tiempo
        elif conditions.get('type') == 'time_window':
            if not self._check_time_window(playbook_data):
                return True

        # Evaluar condiciones de entorno
        elif conditions.get('type') == 'environment':
            environments = conditions.get('environments', [])
            environment = playbook_data.get('metadata', {}).get('environment', 'development')
            if environment in environments:
                return True

        # Evaluar condiciones de skills
        elif conditions.get('type') == 'skills':
            required_skills = conditions.get('skills', [])
            all_skills = []
            for stage in playbook_data.get('stages', []):
                all_skills.extend(stage.get('skills', []))

            if any(skill in all_skills for skill in required_skills):
                return True

        return False

    async def _calculate_playbook_cost(self, playbook_data: Dict[str, Any]) -> float:
        """Calcula el costo total del playbook"""
        total_cost = 0.0
        for stage in playbook_data.get('stages', []):
            total_cost += stage.get('cost_estimate', 0.0)
        return total_cost

    def _check_time_window(self, playbook_data: Dict[str, Any]) -> bool:
        """Verifica si está dentro de la ventana de tiempo permitida"""
        metadata = playbook_data.get('metadata', {})
        environment = metadata.get('environment', 'development')

        if environment != 'production':
            return True  # No restringir entornos no productivos

        policies = playbook_data.get('policies', [])
        for policy in policies:
            if policy.get('type') == 'time_window':
                allowed_hours = policy.get('allowed_hours', [])
                allowed_days = policy.get('allowed_days', [])

                now = datetime.now()
                current_hour = now.hour
                current_day = now.strftime('%A').lower()

                if current_hour in allowed_hours and current_day in allowed_days:
                    return True
                else:
                    return False

        return True  # Si no hay política de tiempo, permitir

    async def create_policy(
        self,
        name: str,
        description: str,
        conditions: Dict[str, Any],
        actions: Dict[str, Any],
        priority: int = 1
    ) -> ApprovalPolicy:
        """Crea una nueva política de aprobación"""
        policy = ApprovalPolicy(
            policy_id=f"policy_{len(self.policies) + 1}",
            name=name,
            description=description,
            conditions=conditions,
            actions=actions,
            priority=priority,
            enabled=True
        )

        self.policies.append(policy)
        logger.info(f"Política de aprobación creada: {name}")
        return policy

    def list_policies(self) -> List[ApprovalPolicy]:
        """Lista todas las políticas de aprobación"""
        return self.policies

    def check_approval_required(
        self,
        playbook_data: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> bool:
        """Verifica si se requiere aprobación según políticas"""
        if context is None:
            context = {}

        # Verificar políticas de costos
        import asyncio
        total_cost = asyncio.run(self._calculate_playbook_cost(playbook_data))
        if total_cost >= 30.00:
            return True

        # Verificar políticas de tiempo
        if not self._check_time_window(playbook_data):
            return True

        # Verificar políticas de entorno
        environment = playbook_data.get('metadata', {}).get('environment', 'development')
        if environment == 'production':
            return True

        # Verificar políticas específicas de etapas
        for stage in playbook_data.get('stages', []):
            if stage.get('approval_required', False):
                return True

        return False
