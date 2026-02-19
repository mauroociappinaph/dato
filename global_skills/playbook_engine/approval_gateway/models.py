#!/usr/bin/env python3
"""
Approval Gateway Models - Modelos de datos para el sistema de aprobaciones.

Este archivo contiene los enums y dataclasses fundamentales
para el sistema de aprobaciones de playbooks.
"""

from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


class ApprovalStatus(Enum):
    """Estados de aprobación"""
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class ApprovalType(Enum):
    """Tipos de aprobación"""
    MANUAL = "manual"
    AUTOMATIC = "automatic"
    TIME_BASED = "time_based"
    POLICY_BASED = "policy_based"


class NotificationChannel(Enum):
    """Canales de notificación"""
    TELEGRAM = "telegram"
    EMAIL = "email"
    WEBHOOK = "webhook"
    CONSOLE = "console"


@dataclass
class ApprovalRequest:
    """Solicitud de aprobación"""
    request_id: str
    playbook_name: str
    stage_name: Optional[str]
    request_type: ApprovalType
    reason: str
    metadata: Dict[str, Any]
    created_at: datetime
    expires_at: Optional[datetime]
    status: ApprovalStatus
    approvers: List[str]
    decision: Optional[Dict[str, Any]] = None
    notifications_sent: List[str] = field(default_factory=list)


@dataclass
class ApprovalPolicy:
    """Política de aprobación"""
    policy_id: str
    name: str
    description: str
    conditions: Dict[str, Any]
    actions: Dict[str, Any]
    priority: int
    enabled: bool


@dataclass
class Notification:
    """Notificación de aprobación"""
    notification_id: str
    request_id: str
    channel: NotificationChannel
    recipient: str
    message: str
    sent_at: datetime
    status: str


@dataclass
class ApprovalDecision:
    """Decisión de aprobación"""
    approver: str
    decision: str  # "approved" or "rejected"
    comment: str
    timestamp: datetime
