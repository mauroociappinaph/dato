import asyncio
import logging
import uuid
import statistics
from datetime import datetime
from typing import Dict, List, Any, Optional
from .types import Alert, AlertRule, MetricType, MetricData

logger = logging.getLogger(__name__)

class AlertManager:
    """Gestiona la lógica de monitoreo y activación de alertas"""

    def __init__(self):
        self.alert_rules: Dict[str, AlertRule] = {}
        self.active_alerts: Dict[str, Alert] = {}

    def add_rule(self, rule: AlertRule):
        self.alert_rules[rule.rule_id] = rule

    async def check_rules(self, metrics_getter_fn):
        """Evalúa todas las reglas activas"""
        for rule in self.alert_rules.values():
            if not rule.enabled: continue

            # Obtener métricas para la ventana de tiempo de la regla
            time_range = f"last_{rule.time_window}m"
            metrics_data = await metrics_getter_fn([rule.metric_type], time_range)
            metrics = metrics_data.get(rule.metric_type.value, [])

            if not metrics: continue

            current_value = self._calculate_rule_value(metrics, rule.condition)
            triggered = self._evaluate_condition(current_value, rule.condition, rule.threshold)

            alert_key = f"{rule.rule_id}_{rule.metric_type.value}"

            if triggered:
                if alert_key not in self.active_alerts:
                    alert = Alert(
                        alert_id=str(uuid.uuid4()),
                        rule_id=rule.rule_id,
                        metric_type=rule.metric_type,
                        value=current_value,
                        threshold=rule.threshold,
                        triggered_at=datetime.now(),
                        status="triggered",
                        message=f"Alerta: {rule.name} - {rule.metric_type.value} = {current_value} {rule.condition} {rule.threshold}"
                    )
                    self.active_alerts[alert_key] = alert
                    await self._notify(alert, rule)
            elif alert_key in self.active_alerts:
                self.active_alerts[alert_key].status = "resolved"
                logger.info(f"Alerta resuelta: {self.active_alerts[alert_key].message}")
                del self.active_alerts[alert_key]

    def _calculate_rule_value(self, metrics: List[MetricData], condition: str) -> float:
        values = [m.value for m in metrics]
        if condition in ["gt", "gte"]: return max(values)
        if condition in ["lt", "lte"]: return min(values)
        return statistics.mean(values)

    def _evaluate_condition(self, value: float, cond: str, thresh: float) -> bool:
        ops = {
            "gt": value > thresh, "gte": value >= thresh,
            "lt": value < thresh, "lte": value <= thresh,
            "eq": value == thresh, "neq": value != thresh
        }
        return ops.get(cond, False)

    async def _notify(self, alert: Alert, rule: AlertRule):
        for channel in rule.notification_channels:
            if channel == "console":
                print(f"
🚨 ALERTA: {alert.message} | Severidad: {rule.severity}")
            # Otros canales (Telegram, Slack) se inyectarían aquí
