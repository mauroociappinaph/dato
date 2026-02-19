from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

class MetricType(Enum):
    """Tipos de métricas"""
    EXECUTION_TIME = "execution_time"
    COST = "cost"
    SUCCESS_RATE = "success_rate"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    QUEUE_DEPTH = "queue_depth"
    RESOURCE_UTILIZATION = "resource_utilization"

class DashboardType(Enum):
    """Tipos de dashboards"""
    REAL_TIME = "real_time"
    HISTORICAL = "historical"
    AGGREGATED = "aggregated"
    ALERTS = "alerts"

@dataclass
class MetricData:
    """Datos de métrica"""
    metric_id: str
    metric_type: MetricType
    value: float
    timestamp: datetime
    tags: Dict[str, str]
    metadata: Dict[str, Any]

@dataclass
class DashboardWidget:
    """Widget de dashboard"""
    widget_id: str
    title: str
    widget_type: str  # chart, gauge, table, metric
    metric_types: List[MetricType]
    time_range: str  # last_hour, last_day, last_week, custom
    refresh_interval: int  # segundos
    filters: Dict[str, Any]

@dataclass
class AlertRule:
    """Regla de alerta"""
    rule_id: str
    name: str
    metric_type: MetricType
    condition: str  # gt, lt, eq, neq
    threshold: float
    time_window: int  # minutos
    enabled: bool
    severity: str  # info, warning, critical
    notification_channels: List[str]

@dataclass
class Alert:
    """Alerta generada"""
    alert_id: str
    rule_id: str
    metric_type: MetricType
    value: float
    threshold: float
    triggered_at: datetime
    status: str  # triggered, resolved
    message: str
