#!/usr/bin/env python3
"""
Cost Record Models - Modelos de datos para el monitoreo de costos
"""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any
import uuid
import json


@dataclass
class CostRecord:
    """
    Registro de costo para una ejecución de skill.

    Attributes:
        id: UUID único del registro
        timestamp: Fecha y hora de la ejecución
        skill_name: Nombre del skill ejecutado
        cluster: Cluster al que pertenece el skill
        model_used: Modelo NVIDIA usado
        tokens_input: Tokens de entrada
        tokens_output: Tokens de salida
        total_tokens: Suma de tokens input + output
        cost_usd: Costo calculado en USD
        execution_time_ms: Tiempo de ejecución en milisegundos
        playbook_id: ID del playbook (opcional)
        stage_id: ID de la etapa (opcional)
        success: Si la ejecución fue exitosa
        metadata: Metadata adicional en JSON
    """
    skill_name: str
    model_used: str
    tokens_input: int
    tokens_output: int
    cost_usd: float
    cluster: str = "unknown"
    execution_time_ms: int = 0
    playbook_id: Optional[str] = None
    stage_id: Optional[str] = None
    success: bool = True
    metadata: Optional[Dict[str, Any]] = None
    id: str = None
    timestamp: datetime = None
    total_tokens: int = None

    def __post_init__(self):
        """Inicializa campos calculados automáticamente"""
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.total_tokens is None:
            self.total_tokens = self.tokens_input + self.tokens_output

    def to_dict(self) -> Dict[str, Any]:
        """Convierte el registro a diccionario"""
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "skill_name": self.skill_name,
            "cluster": self.cluster,
            "model_used": self.model_used,
            "tokens_input": self.tokens_input,
            "tokens_output": self.tokens_output,
            "total_tokens": self.total_tokens,
            "cost_usd": round(self.cost_usd, 6),
            "execution_time_ms": self.execution_time_ms,
            "playbook_id": self.playbook_id,
            "stage_id": self.stage_id,
            "success": self.success,
            "metadata": json.dumps(self.metadata) if self.metadata else None
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CostRecord":
        """Crea un CostRecord desde un diccionario"""
        return cls(
            id=data.get("id"),
            timestamp=datetime.fromisoformat(data["timestamp"]) if data.get("timestamp") else None,
            skill_name=data["skill_name"],
            cluster=data.get("cluster", "unknown"),
            model_used=data["model_used"],
            tokens_input=data["tokens_input"],
            tokens_output=data["tokens_output"],
            cost_usd=data["cost_usd"],
            execution_time_ms=data.get("execution_time_ms", 0),
            playbook_id=data.get("playbook_id"),
            stage_id=data.get("stage_id"),
            success=data.get("success", True),
            metadata=json.loads(data["metadata"]) if data.get("metadata") else None,
            total_tokens=data.get("total_tokens")
        )

    def to_json(self) -> str:
        """Serializa a JSON"""
        return json.dumps(self.to_dict(), indent=2, default=str)


@dataclass
class CostSummary:
    """Resumen agregado de costos"""
    period: str  # "today", "week", "month", "custom"
    total_cost: float
    total_executions: int
    total_tokens: int
    avg_cost_per_execution: float
    skill_breakdown: Dict[str, float]
    cluster_breakdown: Dict[str, float]
    model_breakdown: Dict[str, float]
    start_date: datetime
    end_date: datetime

    def to_dict(self) -> Dict[str, Any]:
        return {
            "period": self.period,
            "total_cost": round(self.total_cost, 4),
            "total_executions": self.total_executions,
            "total_tokens": self.total_tokens,
            "avg_cost_per_execution": round(self.avg_cost_per_execution, 6),
            "skill_breakdown": {k: round(v, 4) for k, v in self.skill_breakdown.items()},
            "cluster_breakdown": {k: round(v, 4) for k, v in self.cluster_breakdown.items()},
            "model_breakdown": {k: round(v, 4) for k, v in self.model_breakdown.items()},
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat()
        }


@dataclass
class BudgetConfig:
    """Configuración de presupuesto"""
    id: str
    period: str  # "daily", "weekly", "monthly"
    amount_usd: float
    alert_thresholds: list  # [50, 75, 90, 100]
    active: bool = True
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


@dataclass
class AlertRecord:
    """Registro de alerta enviada"""
    id: str
    timestamp: datetime
    alert_type: str  # "warning", "caution", "critical", "summary"
    message: str
    threshold_percent: int
    cost_at_alert: float
    budget_limit: float
    channels: list
    sent: bool = False

    def __post_init__(self):
        if self.id is None:
            self.id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": self.timestamp.isoformat(),
            "alert_type": self.alert_type,
            "message": self.message,
            "threshold_percent": self.threshold_percent,
            "cost_at_alert": round(self.cost_at_alert, 4),
            "budget_limit": round(self.budget_limit, 4),
            "channels": self.channels,
            "sent": self.sent
        }
