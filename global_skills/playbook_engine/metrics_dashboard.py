#!/usr/bin/env python3
"""
Metrics Dashboard v2.0 - Orchestrator
Modularized according to SRP and Rule of 300.
"""

import asyncio
import logging
import uuid
import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
from dataclasses import asdict

from .src.types import MetricType, DashboardType, MetricData, DashboardWidget, AlertRule, Alert
from .src.storage import MetricsStorage
from .src.analyzer import MetricsAnalyzer
from .src.alerts import AlertManager

# Importaciones locales
from anti_gravity.scripts.skill_engine_master import SkillEngineMaster

logger = logging.getLogger(__name__)

class MetricsDashboard:
    """Facade for the Metrics and Monitoring System"""

    def __init__(self, skill_engine: SkillEngineMaster):
        self.skill_engine = skill_engine
        self.storage = MetricsStorage(Path("metrics"))
        self.analyzer = MetricsAnalyzer()
        self.alerts = AlertManager()
        
        self.dashboards: Dict[str, List[DashboardWidget]] = {}
        self.real_time_metrics: Dict[str, float] = {}
        
        # Tasks
        asyncio.create_task(self._background_cleanup())
        asyncio.create_task(self._background_alerts())
        
        self._load_default_dashboards()

    def _load_default_dashboards(self):
        self.dashboards["playbook_overview"] = [
            DashboardWidget("exec_time", "Tiempo de Ejecución", "chart", [MetricType.EXECUTION_TIME], "last_hour", 30, {}),
            DashboardWidget("cost_sum", "Costo Total", "gauge", [MetricType.COST], "last_day", 60, {}),
            DashboardWidget("success_rate", "Tasa de Éxito", "metric", [MetricType.SUCCESS_RATE], "last_hour", 30, {})
        ]

    async def record_metric(self, metric_type: MetricType, value: float, tags: Dict=None, metadata: Dict=None):
        data = MetricData(str(uuid.uuid4()), metric_type, value, datetime.now(), tags or {}, metadata or {})
        self.storage.add_to_store(data)
        self.real_time_metrics[f"{metric_type.value}_current"] = value
        self.real_time_metrics[f"{metric_type.value}_last_update"] = datetime.now().isoformat()

    async def get_metrics(self, metric_types: List[MetricType], time_range: str="last_hour", filters: Dict=None):
        start_time = self.analyzer.parse_time_range(time_range)
        result = {}
        for mt in metric_types:
            all_m = self.storage.get_all_from_store(mt.value)
            filtered = [m for m in all_m if m.timestamp >= start_time]
            if filters:
                filtered = [m for m in filtered if self.analyzer.apply_filters(m, filters)]
            result[mt.value] = filtered
        return result

    async def get_performance_summary(self, time_range: str="last_hour"):
        metrics_map = {mt.value: self.storage.get_all_from_store(mt.value) for mt in MetricType}
        return self.analyzer.get_summary(metrics_map, time_range)

    async def create_alert_rule(self, **kwargs):
        rule = AlertRule(str(uuid.uuid4()), **kwargs)
        self.alerts.add_rule(rule)
        return rule

    async def _background_cleanup(self):
        while True:
            self.storage.cleanup_old_metrics()
            await asyncio.sleep(3600)

    async def _background_alerts(self):
        while True:
            await self.alerts.check_rules(self.get_metrics)
            await asyncio.sleep(60)

    async def get_dashboard_data(self, dashboard_name: str):
        widgets = self.dashboards.get(dashboard_name, [])
        data = {"dashboard": dashboard_name, "widgets": [], "ts": datetime.now().isoformat()}
        for w in widgets:
            metrics = await self.get_metrics(w.metric_types, w.time_range, w.filters)
            data["widgets"].append({"id": w.widget_id, "title": w.title, "data": metrics})
        return data

    def export_metrics(self, path: str, time_range: str="last_day"):
        start = self.analyzer.parse_time_range(time_range)
        export = {"ts": datetime.now().isoformat(), "metrics": {}}
        for mt in MetricType:
            export["metrics"][mt.value] = [asdict(m) for m in self.storage.get_all_from_store(mt.value) if m.timestamp >= start]
        with open(path, 'w') as f: json.dump(export, f, indent=2, default=str)