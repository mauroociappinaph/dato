#!/usr/bin/env python3
"""
Cost Monitor Dashboard API - API REST para el dashboard de costos

Proporciona endpoints para:
- Métricas de costos en tiempo real
- Resúmenes por período
- Tendencias y análisis
- Exportación de datos
"""

import sys
import json
from datetime import datetime, timedelta
from typing import Optional, List
from pathlib import Path

# Añadir el path del proyecto
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel

from core.cost_tracker import CostTracker
from core.alert_manager import AlertManager, AlertType
from config import DASHBOARD_CONFIG, calculate_cost, get_tier_for_skill


# Modelos Pydantic
class CostRecordRequest(BaseModel):
    skill_name: str
    model_used: str
    tokens_input: int
    tokens_output: int
    cluster: Optional[str] = None
    execution_time_ms: int = 0
    playbook_id: Optional[str] = None
    stage_id: Optional[str] = None
    success: bool = True


class BudgetConfigRequest(BaseModel):
    amount: float
    period: str = "monthly"
    alert_thresholds: Optional[List[int]] = None


class AlertResponse(BaseModel):
    id: str
    timestamp: str
    alert_type: str
    message: str
    threshold_percent: int
    cost_at_alert: float
    budget_limit: float
    sent: bool


# Crear aplicación FastAPI
app = FastAPI(
    title="The Dude - Cost Monitor API",
    description="API para monitoreo de costos de ejecución de skills",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instancias globales
cost_tracker = CostTracker()
alert_manager = AlertManager()


@app.get("/")
async def root():
    """Endpoint raíz con información básica"""
    return {
        "service": "The Dude Cost Monitor API",
        "version": "1.0.0",
        "status": "operational",
        "endpoints": {
            "metrics": "/api/costs/summary",
            "trends": "/api/costs/trends",
            "skills": "/api/costs/skills",
            "clusters": "/api/costs/clusters",
            "budget": "/api/budget/status",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Verificación de salud del servicio"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "cost_tracker": "operational",
            "alert_manager": "operational"
        }
    }


# =============================================================================
# ENDPOINTS DE COSTOS
# =============================================================================

@app.get("/api/costs/summary")
async def get_costs_summary(
    period: str = Query("today", enum=["today", "week", "month", "all"])
):
    """
    Obtiene un resumen de costos para un período.

    - **today**: Costos del día actual
    - **week**: Costos de los últimos 7 días
    - **month**: Costos de los últimos 30 días
    - **all**: Todos los costos registrados
    """
    try:
        if period == "all":
            # Para "all", usamos un rango muy amplio
            start = datetime.now() - timedelta(days=365*10)  # 10 años
            end = datetime.now()
            summary = cost_tracker.get_cost_summary(
                period="custom",
                start_date=start,
                end_date=end
            )
        else:
            summary = cost_tracker.get_cost_summary(period=period)

        return JSONResponse(content=summary.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/costs/trends")
async def get_cost_trends(
    days: int = Query(7, ge=1, le=90)
):
    """Obtiene tendencias de costos diarios"""
    try:
        trends = cost_tracker.get_cost_trends(days=days)
        return {
            "days": days,
            "data": trends,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/costs/skills")
async def get_skills_costs(
    limit: int = Query(10, ge=1, le=100),
    days: int = Query(30, ge=1, le=365)
):
    """Obtiene los skills más costosos"""
    try:
        top_skills = cost_tracker.get_top_skills(limit=limit, days=days)

        skills_data = []
        for skill_name, cost, executions in top_skills:
            skills_data.append({
                "skill_name": skill_name,
                "total_cost": round(cost, 4),
                "executions": executions,
                "avg_cost": round(cost / executions, 6) if executions > 0 else 0
            })

        return {
            "limit": limit,
            "days": days,
            "skills": skills_data,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/costs/clusters")
async def get_clusters_costs(
    days: int = Query(30, ge=1, le=365)
):
    """Obtiene costos agrupados por cluster"""
    try:
        summary = cost_tracker.get_cost_summary(period="custom")

        # Calcular rango de fechas
        end = datetime.now()
        start = end - timedelta(days=days)
        summary = cost_tracker.get_cost_summary(
            period="custom",
            start_date=start,
            end_date=end
        )

        clusters = []
        for cluster, cost in summary.cluster_breakdown.items():
            clusters.append({
                "cluster": cluster,
                "total_cost": round(cost, 4),
                "percentage": round((cost / summary.total_cost) * 100, 2) if summary.total_cost > 0 else 0
            })

        # Ordenar por costo descendente
        clusters.sort(key=lambda x: x["total_cost"], reverse=True)

        return {
            "days": days,
            "clusters": clusters,
            "total_cost": round(summary.total_cost, 4),
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/costs/models")
async def get_models_costs(
    days: int = Query(30, ge=1, le=365)
):
    """Obtiene costos agrupados por modelo"""
    try:
        end = datetime.now()
        start = end - timedelta(days=days)
        summary = cost_tracker.get_cost_summary(
            period="custom",
            start_date=start,
            end_date=end
        )

        models = []
        for model, cost in summary.model_breakdown.items():
            models.append({
                "model": model,
                "total_cost": round(cost, 4),
                "percentage": round((cost / summary.total_cost) * 100, 2) if summary.total_cost > 0 else 0
            })

        # Ordenar por costo descendente
        models.sort(key=lambda x: x["total_cost"], reverse=True)

        return {
            "days": days,
            "models": models,
            "total_cost": round(summary.total_cost, 4),
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/costs/skill/{skill_name}")
async def get_skill_detail(
    skill_name: str,
    days: int = Query(30, ge=1, le=365)
):
    """Obtiene detalles de costos para un skill específico"""
    try:
        summary = cost_tracker.get_skill_cost_summary(skill_name, days=days)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/costs/track")
async def track_cost(record: CostRecordRequest):
    """Registra una nueva ejecución de skill"""
    try:
        cost_record = cost_tracker.track_execution(
            skill_name=record.skill_name,
            model_used=record.model_used,
            tokens_input=record.tokens_input,
            tokens_output=record.tokens_output,
            cluster=record.cluster,
            execution_time_ms=record.execution_time_ms,
            playbook_id=record.playbook_id,
            stage_id=record.stage_id,
            success=record.success
        )

        # Verificar alertas
        current_month_cost = cost_tracker.get_current_month_cost()
        alert = alert_manager.check_and_alert(
            current_cost=current_month_cost,
            period="monthly",
            channels=["log", "dashboard"]
        )

        return {
            "status": "success",
            "record": cost_record.to_dict(),
            "alert_triggered": alert is not None,
            "alert_id": alert.id if alert else None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ENDPOINTS DE PRESUPUESTO
# =============================================================================

@app.get("/api/budget/status")
async def get_budget_status(
    period: str = Query("monthly", enum=["daily", "weekly", "monthly"])
):
    """Obtiene el estado actual del presupuesto"""
    try:
        # Obtener costo actual del período
        if period == "daily":
            summary = cost_tracker.get_cost_summary(period="today")
        elif period == "weekly":
            summary = cost_tracker.get_cost_summary(period="week")
        else:  # monthly
            current_cost = cost_tracker.get_current_month_cost()
            summary = None

        current_cost = summary.total_cost if summary else current_cost

        status = alert_manager.check_budget_status(current_cost, period)

        return {
            "period": period,
            **status,
            "checked_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/budget/configure")
async def configure_budget(config: BudgetConfigRequest):
    """Configura un nuevo presupuesto"""
    try:
        budget_config = alert_manager.set_budget_limit(
            amount=config.amount,
            period=config.period,
            alert_thresholds=config.alert_thresholds or [50, 75, 90, 100]
        )

        return {
            "status": "success",
            "budget": {
                "id": budget_config.id,
                "period": budget_config.period,
                "amount": budget_config.amount_usd,
                "thresholds": budget_config.alert_thresholds,
                "active": budget_config.active
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/budget/history")
async def get_budget_history(
    days: int = Query(30, ge=1, le=365)
):
    """Obtiene el historial de alertas"""
    try:
        alerts = alert_manager.get_alert_history(days=days)

        return {
            "days": days,
            "total_alerts": len(alerts),
            "alerts": [
                {
                    "id": alert.id,
                    "timestamp": alert.timestamp.isoformat(),
                    "type": alert.alert_type,
                    "message": alert.message,
                    "threshold": alert.threshold_percent,
                    "sent": alert.sent
                }
                for alert in alerts
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ENDPOINTS DE EXPORTACIÓN
# =============================================================================

@app.get("/api/export/json")
async def export_to_json(
    days: int = Query(30, ge=1, le=365)
):
    """Exporta datos a JSON"""
    try:
        end = datetime.now()
        start = end - timedelta(days=days)

        output_path = f"/tmp/cost_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        count = cost_tracker.export_to_json(output_path, start, end)

        return {
            "status": "success",
            "records_exported": count,
            "file_path": output_path,
            "period": {
                "start": start.isoformat(),
                "end": end.isoformat()
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/calculator")
async def calculate_execution_cost(
    model: str,
    tokens_input: int = Query(..., ge=0),
    tokens_output: int = Query(..., ge=0)
):
    """Calcula el costo estimado de una ejecución"""
    try:
        cost = calculate_cost(model, tokens_input, tokens_output)
        tier = get_tier_for_skill("")  # No skill, solo modelo

        return {
            "model": model,
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "total_tokens": tokens_input + tokens_output,
            "estimated_cost_usd": round(cost, 6),
            "tier": tier
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# ENDPOINTS DE ESTADÍSTICAS
# =============================================================================

@app.get("/api/stats/executions")
async def get_execution_stats(
    days: int = Query(30, ge=1, le=365)
):
    """Obtiene estadísticas de ejecuciones"""
    try:
        total_count = cost_tracker.get_execution_count(days=days)

        # Obtener tendencias para calcular promedio diario
        trends = cost_tracker.get_cost_trends(days=days)
        avg_daily_executions = sum(day["executions"] for day in trends) / len(trends) if trends else 0

        return {
            "total_executions": total_count,
            "avg_daily_executions": round(avg_daily_executions, 2),
            "days": days,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats/efficiency")
async def get_efficiency_stats(
    days: int = Query(30, ge=1, le=365)
):
    """Obtiene estadísticas de eficiencia"""
    try:
        end = datetime.now()
        start = end - timedelta(days=days)
        summary = cost_tracker.get_cost_summary(
            period="custom",
            start_date=start,
            end_date=end
        )

        return {
            "total_cost": round(summary.total_cost, 4),
            "total_executions": summary.total_executions,
            "total_tokens": summary.total_tokens,
            "avg_cost_per_execution": round(summary.avg_cost_per_execution, 6),
            "avg_tokens_per_execution": round(summary.total_tokens / summary.total_executions, 2) if summary.total_executions > 0 else 0,
            "cost_per_1k_tokens": round((summary.total_cost / summary.total_tokens) * 1000, 4) if summary.total_tokens > 0 else 0,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn

    print(f"🚀 Starting Cost Monitor API on {DASHBOARD_CONFIG['host']}:{DASHBOARD_CONFIG['port']}")

    uvicorn.run(
        app,
        host=DASHBOARD_CONFIG["host"],
        port=DASHBOARD_CONFIG["port"],
        log_level="info"
    )
