#!/usr/bin/env python3
"""
Cost Tracker - Servicio central para tracking de costos

Este módulo proporciona funcionalidades para:
- Registrar ejecuciones de skills con sus costos
- Calcular costos basados en modelos NVIDIA
- Generar reportes y análisis
- Exportar datos
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any, Tuple
from pathlib import Path

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import calculate_cost, get_tier_for_skill, DATABASE_CONFIG
from models.cost_record import CostRecord, CostSummary
from ...src.helpers import get_script_dir


class CostTracker:
    """
    Servicio central para tracking de costos de ejecución de skills.

    Usage:
        tracker = CostTracker()

        # Registrar una ejecución
        tracker.track_execution(
            skill_name="security-auditor",
            model_used="nvidia/nemotron-4-340b-instruct",
            tokens_input=1500,
            tokens_output=800,
            execution_time_ms=2500
        )

        # Obtener resumen de costos
        summary = tracker.get_cost_summary(period="today")
        print(f"Costo hoy: ${summary.total_cost:.4f}")
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Inicializa el CostTracker.

        Args:
            db_path: Ruta a la base de datos SQLite. Si no se especifica,
                    usa la configuración por defecto.
        """
        self.db_path = db_path or DATABASE_CONFIG["path"]
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Crea la base de datos y tablas si no existen"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Tabla de registros de costos
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS cost_records (
                    id TEXT PRIMARY KEY,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    skill_name TEXT NOT NULL,
                    cluster TEXT NOT NULL,
                    model_used TEXT NOT NULL,
                    tokens_input INTEGER NOT NULL,
                    tokens_output INTEGER NOT NULL,
                    total_tokens INTEGER NOT NULL,
                    cost_usd REAL NOT NULL,
                    execution_time_ms INTEGER,
                    playbook_id TEXT,
                    stage_id TEXT,
                    success BOOLEAN DEFAULT 1,
                    metadata TEXT
                )
            """)

            # Índices para queries rápidos
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_costs_timestamp
                ON cost_records(timestamp)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_costs_skill
                ON cost_records(skill_name)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_costs_cluster
                ON cost_records(cluster)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_costs_model
                ON cost_records(model_used)
            """)

            conn.commit()

    def track_execution(
        self,
        skill_name: str,
        model_used: str,
        tokens_input: int,
        tokens_output: int,
        cluster: Optional[str] = None,
        execution_time_ms: int = 0,
        playbook_id: Optional[str] = None,
        stage_id: Optional[str] = None,
        success: bool = True,
        metadata: Optional[Dict[str, Any]] = None
    ) -> CostRecord:
        """
        Registra una ejecución de skill con su costo.

        Args:
            skill_name: Nombre del skill ejecutado
            model_used: Modelo NVIDIA usado
            tokens_input: Tokens de entrada
            tokens_output: Tokens de salida
            cluster: Cluster del skill (auto-detectado si no se especifica)
            execution_time_ms: Tiempo de ejecución
            playbook_id: ID del playbook (opcional)
            stage_id: ID de la etapa (opcional)
            success: Si la ejecución fue exitosa
            metadata: Metadata adicional

        Returns:
            CostRecord creado
        """
        # Calcular costo
        cost_usd = calculate_cost(model_used, tokens_input, tokens_output)

        # Detectar cluster si no se especifica
        if cluster is None:
            # TODO: Cargar desde skill_registry.json
            cluster = self._get_cluster_for_skill(skill_name)

        # Crear registro
        record = CostRecord(
            skill_name=skill_name,
            cluster=cluster,
            model_used=model_used,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            cost_usd=cost_usd,
            execution_time_ms=execution_time_ms,
            playbook_id=playbook_id,
            stage_id=stage_id,
            success=success,
            metadata=metadata
        )

        # Guardar en base de datos
        self._save_record(record)

        return record

    def _save_record(self, record: CostRecord):
        """Guarda un registro en la base de datos"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            data = record.to_dict()

            cursor.execute("""
                INSERT INTO cost_records
                (id, timestamp, skill_name, cluster, model_used, tokens_input,
                 tokens_output, total_tokens, cost_usd, execution_time_ms,
                 playbook_id, stage_id, success, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["id"], data["timestamp"], data["skill_name"],
                data["cluster"], data["model_used"], data["tokens_input"],
                data["tokens_output"], data["total_tokens"], data["cost_usd"],
                data["execution_time_ms"], data["playbook_id"], data["stage_id"],
                data["success"], data["metadata"]
            ))

            conn.commit()

    def _get_cluster_for_skill(self, skill_name: str) -> str:
        """Obtiene el cluster para un skill (simplificado)"""
        # Mapeo básico - en producción cargar desde skill_registry.json
        cluster_map = {
            "security-auditor": "SECURITY",
            "hardening-auditor": "SECURITY",
            "mcp-vetting-guard": "SECURITY",
            "secrets-vault-orchestrator": "SECURITY",
            "git-workflow-hardener": "SECURITY",
            "ai-engineer": "DATA_AI",
            "meta-learning-engine": "DATA_AI",
            "rag-implementation": "DATA_AI",
            "context-manager": "DATA_AI",
            "prompt-optimizer-dspy": "DATA_AI",
            "code-review-excellence": "QUALITY_ASSURANCE",
            "agent-evaluation": "QUALITY_ASSURANCE",
            "stripe-integration": "BUSINESS",
            "telegram-bot-builder": "BUSINESS",
            "deploy-automation-pilot": "INFRASTRUCTURE",
            "github-actions-guardian": "INFRASTRUCTURE",
        }
        return cluster_map.get(skill_name, "UNKNOWN")

    def get_cost_summary(
        self,
        period: str = "today",
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> CostSummary:
        """
        Obtiene un resumen de costos para un período.

        Args:
            period: "today", "week", "month", "custom"
            start_date: Fecha de inicio (solo para period="custom")
            end_date: Fecha de fin (solo para period="custom")

        Returns:
            CostSummary con el resumen
        """
        # Calcular rango de fechas
        now = datetime.now()

        if period == "today":
            start = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end = now
        elif period == "week":
            start = now - timedelta(days=7)
            end = now
        elif period == "month":
            start = now - timedelta(days=30)
            end = now
        elif period == "custom":
            start = start_date or now - timedelta(days=1)
            end = end_date or now
        else:
            start = now - timedelta(days=1)
            end = now

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Query principal
            cursor.execute("""
                SELECT
                    COUNT(*) as total_executions,
                    SUM(cost_usd) as total_cost,
                    SUM(total_tokens) as total_tokens
                FROM cost_records
                WHERE timestamp >= ? AND timestamp <= ?
            """, (start.isoformat(), end.isoformat()))

            row = cursor.fetchone()
            total_executions = row[0] or 0
            total_cost = row[1] or 0.0
            total_tokens = row[2] or 0

            # Breakdown por skill
            cursor.execute("""
                SELECT skill_name, SUM(cost_usd) as cost
                FROM cost_records
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY skill_name
                ORDER BY cost DESC
            """, (start.isoformat(), end.isoformat()))

            skill_breakdown = {row[0]: row[1] for row in cursor.fetchall()}

            # Breakdown por cluster
            cursor.execute("""
                SELECT cluster, SUM(cost_usd) as cost
                FROM cost_records
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY cluster
                ORDER BY cost DESC
            """, (start.isoformat(), end.isoformat()))

            cluster_breakdown = {row[0]: row[1] for row in cursor.fetchall()}

            # Breakdown por modelo
            cursor.execute("""
                SELECT model_used, SUM(cost_usd) as cost
                FROM cost_records
                WHERE timestamp >= ? AND timestamp <= ?
                GROUP BY model_used
                ORDER BY cost DESC
            """, (start.isoformat(), end.isoformat()))

            model_breakdown = {row[0]: row[1] for row in cursor.fetchall()}

            avg_cost = total_cost / total_executions if total_executions > 0 else 0.0

            return CostSummary(
                period=period,
                total_cost=total_cost,
                total_executions=total_executions,
                total_tokens=total_tokens,
                avg_cost_per_execution=avg_cost,
                skill_breakdown=skill_breakdown,
                cluster_breakdown=cluster_breakdown,
                model_breakdown=model_breakdown,
                start_date=start,
                end_date=end
            )

    def get_skill_cost_summary(
        self,
        skill_name: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Obtiene un resumen de costos para un skill específico.

        Args:
            skill_name: Nombre del skill
            days: Número de días hacia atrás

        Returns:
            Diccionario con estadísticas del skill
        """
        start = datetime.now() - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*) as executions,
                    SUM(cost_usd) as total_cost,
                    SUM(total_tokens) as total_tokens,
                    AVG(cost_usd) as avg_cost,
                    AVG(execution_time_ms) as avg_time
                FROM cost_records
                WHERE skill_name = ? AND timestamp >= ?
            """, (skill_name, start.isoformat()))

            row = cursor.fetchone()

            return {
                "skill_name": skill_name,
                "period_days": days,
                "total_executions": row[0] or 0,
                "total_cost": round(row[1] or 0, 4),
                "total_tokens": row[2] or 0,
                "avg_cost_per_execution": round(row[3] or 0, 6),
                "avg_execution_time_ms": round(row[4] or 0, 2)
            }

    def get_top_skills(
        self,
        limit: int = 10,
        days: int = 30
    ) -> List[Tuple[str, float, int]]:
        """
        Obtiene los skills más costosos.

        Args:
            limit: Número de skills a retornar
            days: Período en días

        Returns:
            Lista de tuplas (skill_name, cost, executions)
        """
        start = datetime.now() - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    skill_name,
                    SUM(cost_usd) as total_cost,
                    COUNT(*) as executions
                FROM cost_records
                WHERE timestamp >= ?
                GROUP BY skill_name
                ORDER BY total_cost DESC
                LIMIT ?
            """, (start.isoformat(), limit))

            return [(row[0], row[1], row[2]) for row in cursor.fetchall()]

    def get_cost_trends(
        self,
        days: int = 7
    ) -> List[Dict[str, Any]]:
        """
        Obtiene tendencias de costos diarios.

        Args:
            days: Número de días hacia atrás

        Returns:
            Lista de registros diarios
        """
        start = datetime.now() - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    DATE(timestamp) as date,
                    SUM(cost_usd) as daily_cost,
                    COUNT(*) as executions,
                    SUM(total_tokens) as tokens
                FROM cost_records
                WHERE timestamp >= ?
                GROUP BY DATE(timestamp)
                ORDER BY date
            """, (start.isoformat(),))

            return [
                {
                    "date": row[0],
                    "cost": round(row[1], 4),
                    "executions": row[2],
                    "tokens": row[3]
                }
                for row in cursor.fetchall()
            ]

    def export_to_json(
        self,
        output_path: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> int:
        """
        Exporta registros a JSON.

        Args:
            output_path: Ruta del archivo de salida
            start_date: Fecha de inicio (opcional)
            end_date: Fecha de fin (opcional)

        Returns:
            Número de registros exportados
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM cost_records"
            params = []

            if start_date and end_date:
                query += " WHERE timestamp >= ? AND timestamp <= ?"
                params = [start_date.isoformat(), end_date.isoformat()]

            query += " ORDER BY timestamp DESC"

            cursor.execute(query, params)

            records = []
            for row in cursor.fetchall():
                record = CostRecord.from_dict({
                    "id": row[0],
                    "timestamp": row[1],
                    "skill_name": row[2],
                    "cluster": row[3],
                    "model_used": row[4],
                    "tokens_input": row[5],
                    "tokens_output": row[6],
                    "total_tokens": row[7],
                    "cost_usd": row[8],
                    "execution_time_ms": row[9],
                    "playbook_id": row[10],
                    "stage_id": row[11],
                    "success": row[12],
                    "metadata": row[13]
                })
                records.append(record.to_dict())

            with open(output_path, "w") as f:
                json.dump(records, f, indent=2, default=str)

            return len(records)

    def get_execution_count(
        self,
        skill_name: Optional[str] = None,
        days: int = 30
    ) -> int:
        """Obtiene el número de ejecuciones"""
        start = datetime.now() - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            if skill_name:
                cursor.execute("""
                    SELECT COUNT(*) FROM cost_records
                    WHERE skill_name = ? AND timestamp >= ?
                """, (skill_name, start.isoformat()))
            else:
                cursor.execute("""
                    SELECT COUNT(*) FROM cost_records
                    WHERE timestamp >= ?
                """, (start.isoformat(),))

            return cursor.fetchone()[0] or 0

    def get_current_month_cost(self) -> float:
        """Obtiene el costo acumulado del mes actual"""
        now = datetime.now()
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT SUM(cost_usd) FROM cost_records
                WHERE timestamp >= ?
            """, (start.isoformat(),))

            return cursor.fetchone()[0] or 0.0
