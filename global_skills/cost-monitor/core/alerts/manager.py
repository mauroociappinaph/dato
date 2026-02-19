#!/usr/bin/env python3
"""
Alert Manager - Central Orchestrator.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from pathlib import Path

from .models import AlertType, BudgetConfig, AlertRecord
from .notifier import AlertNotifier

class AlertManager:
    """Gestor de alertas de presupuesto."""

    def __init__(self, db_path: str, alert_config: Dict[str, Any]):
        self.db_path = db_path
        self.alert_config = alert_config
        self.notifier = AlertNotifier()
        self._last_alert_times = {}

    def set_budget_limit(self, amount: float, period: str, alert_thresholds: List[int], active: bool = True) -> BudgetConfig:
        config = BudgetConfig(id=None, period=period, amount_usd=amount, alert_thresholds=alert_thresholds, active=active)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE budget_configs SET active = 0 WHERE period = ?", (period,))
            cursor.execute("""
                INSERT INTO budget_configs (id, period, amount_usd, alert_thresholds, active)
                VALUES (?, ?, ?, ?, ?)
            """, (config.id, config.period, config.amount_usd, json.dumps(config.alert_thresholds), config.active))
            conn.commit()
        return config

    def get_active_budget(self, period: str = "monthly") -> Optional[BudgetConfig]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, period, amount_usd, alert_thresholds, active, created_at, updated_at FROM budget_configs WHERE period = ? AND active = 1 ORDER BY updated_at DESC LIMIT 1", (period,))
            row = cursor.fetchone()
            if row:
                return BudgetConfig(id=row[0], period=row[1], amount_usd=row[2], alert_thresholds=json.loads(row[3]), active=bool(row[4]),
                                   created_at=datetime.fromisoformat(row[5]) if row[5] else None,
                                   updated_at=datetime.fromisoformat(row[6]) if row[6] else None)
        return None

    def check_budget_status(self, current_cost: float, period: str = "monthly") -> Dict[str, Any]:
        budget = self.get_active_budget(period)
        if not budget:
            return {"has_budget": False, "alert_needed": False, "message": "No hay presupuesto configurado"}

        percentage = (current_cost / budget.amount_usd) * 100
        alert_type = None
        threshold_triggered = None

        for threshold in sorted(budget.alert_thresholds, reverse=True):
            if percentage >= threshold:
                threshold_triggered = threshold
                if threshold >= 100: alert_type = AlertType.CRITICAL
                elif threshold >= 90: alert_type = AlertType.CAUTION
                elif threshold >= 75: alert_type = AlertType.WARNING
                break

        return {
            "has_budget": True, "budget_limit": budget.amount_usd, "current_cost": current_cost,
            "percentage": round(percentage, 2), "alert_needed": alert_type is not None,
            "alert_type": alert_type.value if alert_type else None,
            "threshold_triggered": threshold_triggered, "remaining": round(budget.amount_usd - current_cost, 2)
        }

    def should_send_alert(self, alert_type: AlertType, threshold: int) -> bool:
        cooldown = self.alert_config.get("cooldown_minutes", 60)
        key = f"{alert_type.value}_{threshold}"
        if key in self._last_alert_times:
            elapsed = (datetime.now() - self._last_alert_times[key]).total_seconds() / 60
            if elapsed < cooldown: return False
        self._last_alert_times[key] = datetime.now()
        return True

    def send_alert(self, alert_type: AlertType, message: str, threshold: int, cost: float, limit: float, channels: List[str] = None) -> AlertRecord:
        if channels is None: channels = ["dashboard", "log"]
        if not self.should_send_alert(alert_type, threshold): return None

        alert = AlertRecord(id=None, timestamp=datetime.now(), alert_type=alert_type.value, message=message,
                           threshold_percent=threshold, cost_at_alert=cost, budget_limit=limit, channels=channels)

        sent_successfully = True
        for channel in channels:
            try:
                self.notifier.send_by_channel(channel, alert)
            except Exception as e:
                sent_successfully = False

        alert.sent = sent_successfully
        self._save_alert_record(alert)
        return alert

    def _save_alert_record(self, alert: AlertRecord):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alert_history (id, timestamp, alert_type, message, threshold_percent, cost_at_alert, budget_limit, channels, sent)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (alert.id, alert.timestamp.isoformat(), alert.alert_type, alert.message, alert.threshold_percent,
                  alert.cost_at_alert, alert.budget_limit, json.dumps(alert.channels), alert.sent))
            conn.commit()
