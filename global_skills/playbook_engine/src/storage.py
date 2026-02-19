import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, deque
from dataclasses import asdict
from typing import Dict, List, Any, Optional
from .types import MetricData, MetricType

logger = logging.getLogger(__name__)

class MetricsStorage:
    """Maneja el almacenamiento y persistencia de métricas"""

    def __init__(self, metrics_dir: Path, retention_days: int = 30):
        self.metrics_dir = metrics_dir
        self.metrics_dir.mkdir(exist_ok=True)
        self.retention_days = retention_days
        self.metrics_store: Dict[str, deque] = defaultdict(lambda: deque(maxlen=10000))

    def add_to_store(self, metric_data: MetricData):
        """Agrega métrica al store en memoria y la persiste"""
        self.metrics_store[metric_data.metric_type.value].append(metric_data)
        self._persist_metric(metric_data)

    def _persist_metric(self, metric_data: MetricData):
        """Persiste una métrica en archivo .jsonl"""
        try:
            date_str = metric_data.timestamp.strftime("%Y-%m-%d")
            file_path = self.metrics_dir / f"metrics_{date_str}.jsonl"

            metric_dict = asdict(metric_data)
            metric_dict['timestamp'] = metric_data.timestamp.isoformat()
            metric_dict['metric_type'] = metric_data.metric_type.value

            with open(file_path, 'a') as f:
                f.write(json.dumps(metric_dict) + '
')
        except Exception as e:
            logger.error(f"Error persistiendo métrica: {e}")

    def get_all_from_store(self, metric_type_value: str) -> List[MetricData]:
        """Retorna todas las métricas de un tipo del store"""
        return list(self.metrics_store[metric_type_value])

    def cleanup_old_metrics(self):
        """Limpia métricas antiguas del store y del disco"""
        cutoff_date = datetime.now() - timedelta(days=self.retention_days)

        # 1. Limpiar store en memoria
        for mt_val in list(self.metrics_store.keys()):
            self.metrics_store[mt_val] = deque(
                [m for m in self.metrics_store[mt_val] if m.timestamp >= cutoff_date],
                maxlen=10000
            )

        # 2. Limpiar archivos en disco
        for file_path in self.metrics_dir.glob("metrics_*.jsonl"):
            try:
                date_str = file_path.stem.replace("metrics_", "")
                file_date = datetime.strptime(date_str, "%Y-%m-%d")

                if file_date < cutoff_date:
                    file_path.unlink()
                    logger.info(f"Archivo de métricas eliminado: {file_path}")
            except Exception as e:
                logger.warning(f"Error eliminando archivo de métricas {file_path}: {e}")
