import statistics
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from collections import defaultdict
from .types import MetricData, MetricType

class MetricsAnalyzer:
    """Procesa y agrega datos de métricas"""

    @staticmethod
    def parse_time_range(time_range: str) -> datetime:
        """Convierte un rango de tiempo a datetime"""
        now = datetime.now()
        if time_range == "last_hour": return now - timedelta(hours=1)
        if time_range == "last_day": return now - timedelta(days=1)
        if time_range == "last_week": return now - timedelta(weeks=1)
        if time_range == "last_month": return now - timedelta(days=30)
        return now - timedelta(hours=1)

    @staticmethod
    def apply_filters(metric: MetricData, filters: Dict[str, Any]) -> bool:
        """Aplica filtros de tags y metadatos"""
        for key, value in filters.items():
            source = metric.tags if key in metric.tags else metric.metadata
            if key not in source: return False
            if isinstance(value, list):
                if source[key] not in value: return False
            elif source[key] != value: return False
        return True

    @staticmethod
    def percentile(data: List[float], p: float) -> float:
        """Calcula el percentil p"""
        if not data: return 0
        sorted_data = sorted(data)
        index = int((p / 100) * len(sorted_data))
        return sorted_data[min(index, len(sorted_data) - 1)]

    def group_by_time_window(self, metrics: List[MetricData], time_window: str) -> Dict[str, List[MetricData]]:
        """Agrupa métricas por ventana temporal (1m, 5m, 15m, 1h)"""
        groups = defaultdict(list)
        for m in metrics:
            ts = m.timestamp
            if time_window == "1m":
                key = ts.replace(second=0, microsecond=0)
            elif time_window == "5m":
                key = ts.replace(minute=(ts.minute // 5) * 5, second=0, microsecond=0)
            elif time_window == "15m":
                key = ts.replace(minute=(ts.minute // 15) * 15, second=0, microsecond=0)
            else:
                key = ts.replace(minute=0, second=0, microsecond=0)
            groups[key.isoformat()].append(m)
        return groups

    def get_summary(self, metrics_map: Dict[str, List[MetricData]], time_range: str) -> Dict[str, Any]:
        """Genera un resumen ejecutivo de performance"""
        start_time = self.parse_time_range(time_range)
        
        exec_times = [m.value for m in metrics_map.get(MetricType.EXECUTION_TIME.value, []) if m.timestamp >= start_time]
        costs = [m.value for m in metrics_map.get(MetricType.COST.value, []) if m.timestamp >= start_time]
        success_metrics = [m for m in metrics_map.get(MetricType.SUCCESS_RATE.value, []) if m.timestamp >= start_time]
        
        success_count = sum(1 for m in success_metrics if m.value > 0.5)
        total_execs = len(success_metrics)

        return {
            "time_range": time_range,
            "execution_stats": {
                "count": len(exec_times),
                "avg_time": statistics.mean(exec_times) if exec_times else 0,
                "min_time": min(exec_times) if exec_times else 0,
                "max_time": max(exec_times) if exec_times else 0,
                "p95_time": self.percentile(exec_times, 95),
                "p99_time": self.percentile(exec_times, 99)
            },
            "cost_stats": {
                "total_cost": sum(costs),
                "avg_cost": statistics.mean(costs) if costs else 0
            },
            "success_rate": (success_count / total_execs * 100) if total_execs > 0 else 0,
            "total_executions": total_execs
        }
