#!/usr/bin/env python3
"""
Alert Manager - Proxy Wrapper (v2.0)
Refactored to meet the 300-line modularity rule.
"""

import sys
import os
from typing import List, Dict, Optional, Any

# Ensure we can import from the sub-package
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alerts import AlertType, AlertManager as ModularAlertManager
from config import ALERT_CONFIG, DATABASE_CONFIG

class AlertManager:
    """
    Wrapper for backward compatibility.
    New logic resides in the 'alerts/' sub-package.
    """

    def __init__(self, db_path: Optional[str] = None):
        self.db_path = db_path or self._get_db_path()
        self._manager = ModularAlertManager(self.db_path, ALERT_CONFIG)

    def _get_db_path(self) -> str:
        from pathlib import Path
        return str(Path(DATABASE_CONFIG["path"]).parent / "cost_monitor.db")

    def set_budget_limit(self, amount: float, period: str = "monthly",
                         alert_thresholds: Optional[List[int]] = None,
                         active: bool = True):
        thresholds = alert_thresholds or ALERT_CONFIG["default_thresholds"]
        return self._manager.set_budget_limit(amount, period, thresholds, active)

    def get_active_budget(self, period: str = "monthly"):
        return self._manager.get_active_budget(period)

    def check_budget_status(self, current_cost: float, period: str = "monthly"):
        return self._manager.check_budget_status(current_cost, period)

    def should_send_alert(self, alert_type: AlertType, threshold: int):
        return self._manager.should_send_alert(alert_type, threshold)

    def send_alert(self, alert_type: AlertType, message: str, threshold_percent: int,
                   cost_at_alert: float, budget_limit: float,
                   channels: List[str] = None):
        return self._manager.send_alert(alert_type, message, threshold_percent,
                                        cost_at_alert, budget_limit, channels)

    def get_alert_history(self, days: int = 30, alert_type: Optional[str] = None):
        return self._manager.get_alert_history(days, alert_type)

    def check_and_alert(self, current_cost: float, period: str = "monthly",
                       channels: List[str] = None):
        return self._manager.check_and_alert(current_cost, period, channels)

    def get_budget_summary(self):
        return self._manager.get_budget_summary()
