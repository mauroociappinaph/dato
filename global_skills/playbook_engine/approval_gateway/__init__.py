#!/usr/bin/env python3
"""
Approval Gateway Package - Sistema de aprobaciones para playbooks.

Este paquete proporciona gestión de políticas de veto y aprobación
para workflows declarativos. Integra con sistemas de notificación
y registro de decisiones.

Usage:
    from approval_gateway import ApprovalGateway, ApprovalRequest
    from approval_gateway.models import ApprovalStatus, ApprovalType

    gateway = ApprovalGateway(skill_engine)
    request = await gateway.create_approval_request(
        playbook_name="deploy-prod",
        stage_name="production",
        request_type=ApprovalType.MANUAL,
        reason="Deployment to production",
        metadata={"cost": 100.0},
        approvers=["admin", "manager"]
    )
"""

__version__ = "1.0.0"

# Importar modelos
from .models import (
    ApprovalStatus,
    ApprovalType,
    NotificationChannel,
    ApprovalRequest,
    ApprovalPolicy,
    Notification,
    ApprovalDecision,
)

# Importar clase principal
from .gateway import ApprovalGateway

# Importar componentes especializados
from .notifications import NotificationManager
from .policies import PolicyEngine

__all__ = [
    # Version
    "__version__",
    # Enums
    "ApprovalStatus",
    "ApprovalType",
    "NotificationChannel",
    # Dataclasses
    "ApprovalRequest",
    "ApprovalPolicy",
    "Notification",
    "ApprovalDecision",
    # Classes
    "ApprovalGateway",
    "NotificationManager",
    "PolicyEngine",
]
