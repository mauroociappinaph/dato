#!/usr/bin/env python3
"""
Approval Gateway - Sistema de aprobaciones para playbooks.

⚠️  DEPRECATED: Este archivo se mantiene por compatibilidad.
Usa el nuevo paquete `approval_gateway` en su lugar:

    from playbook_engine.approval_gateway import ApprovalGateway
    from playbook_engine.approval_gateway.models import ApprovalStatus

Migration Guide:
    ❌ Viejo: from approval_gateway import ApprovalGateway
    ✅ Nuevo: from playbook_engine.approval_gateway import ApprovalGateway
"""

import warnings
from datetime import datetime
from typing import Any, Dict, List, Optional

# Emitir warning de deprecación
warnings.warn(
    "approval_gateway.py está deprecado. "
    "Usa 'from playbook_engine.approval_gateway import ApprovalGateway' en su lugar.",
    DeprecationWarning,
    stacklevel=2
)

# Re-exportar desde el nuevo paquete
from approval_gateway import (
    ApprovalGateway as _ApprovalGateway,
    ApprovalStatus,
    ApprovalType,
    NotificationChannel,
    ApprovalRequest,
    ApprovalPolicy,
    Notification,
    ApprovalDecision,
    NotificationManager,
    PolicyEngine,
)


class ApprovalGateway(_ApprovalGateway):
    """
    Wrapper de compatibilidad para ApprovalGateway.

    Esta clase extiende el nuevo ApprovalGateway del paquete
    approval_gateway para mantener compatibilidad con código existente.

    Todo nuevo código debe usar directamente:
        from playbook_engine.approval_gateway import ApprovalGateway
    """

    def __init__(self, skill_engine=None):
        # Emitir warning en tiempo de ejecución también
        warnings.warn(
            "ApprovalGateway desde 'approval_gateway.py' está deprecado. "
            "Usa 'from playbook_engine.approval_gateway import ApprovalGateway'.",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(skill_engine)


# Re-exportar todos los símbolos públicos para compatibilidad
__all__ = [
    "ApprovalGateway",
    "ApprovalStatus",
    "ApprovalType",
    "NotificationChannel",
    "ApprovalRequest",
    "ApprovalPolicy",
    "Notification",
    "ApprovalDecision",
    "NotificationManager",
    "PolicyEngine",
]

__version__ = "1.0.0-deprecated"
