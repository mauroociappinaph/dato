#!/usr/bin/env python3
"""
Alert Manager Models - Enums and DataClasses.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

class AlertType(Enum):
    """Tipos de alertas"""
    WARNING = "warning"      # 75% del presupuesto
    CAUTION = "caution"      # 90% del presupuesto
    CRITICAL = "critical"    # 100% del presupuesto
    DAILY_SUMMARY = "daily_summary"  # Resumen diario
    ANOMALY = "anomaly"      # Gasto inusual detectado

@dataclass
class BudgetConfig:
    """Configuración de presupuesto"""
    id: Optional[str]
    period: str
    amount_usd: float
    alert_thresholds: List[int]
    active: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        if self.id is None:
            import uuid
            self.id = str(uuid.uuid4())

@dataclass
class AlertRecord:
    """Registro de alerta enviada"""
    id: Optional[str]
    timestamp: datetime
    alert_type: str
    message: str
    threshold_percent: int
    cost_at_alert: float
    budget_limit: float
    channels: List[str]
    sent: bool = False

    def __post_init__(self):
        if self.id is None:
            import uuid
            self.id = str(uuid.uuid4())
