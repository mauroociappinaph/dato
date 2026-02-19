#!/usr/bin/env python3
"""
Demo de Integración - Cost Monitor + Skill Engine

Este demo muestra cómo el MonitoredSkillEngineAdapter intercepta automáticamente
todas las ejecuciones y registra los costos sin modificar el código existente.
"""

import asyncio
import sys
import os
import tempfile
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum

# Añadir paths necesarios
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai-engineer', 'scripts'))

# Clases mock para el demo (simulando playbook_engine_api)
class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class SkillRequest:
    skill_name: str
    agent_name: Optional[str] = None
    inputs: Dict[str, Any] = field(default_factory=dict)
    timeout: Optional[int] = None
    retry_attempts: int = 3
    retry_delay: float = 1.0

@dataclass
class SkillResult:
    skill_name: str
    status: ExecutionStatus
    outputs: Dict[str, Any] = field(default_factory=dict)
    cost_incurred: float = 0.0
    execution_time: float = 0.0
    error_message: Optional[str] = None
    agent_used: Optional[str] = None

@dataclass
class StageRequest:
    stage_name: str
    skills: list = field(default_factory=list)
    parallel: bool = False
    timeout: Optional[int] = None

class SkillEngineAdapter:
    """Adaptador base (mock)"""
    def __init__(self, skill_engine):
        self.skill_engine = skill_engine

    async def execute_skill(self, request):
        return SkillResult(
            skill_name=request.skill_name,
            status=ExecutionStatus.COMPLETED,
            outputs={"result": f"Executed {request.skill_name}"}
        )

# Importar componentes de integración
from integration import (
    MonitoredSkillEngineAdapter,
    SkillModelMapper,
    get_model_for_skill
)
from core.cost_tracker import CostTracker
from ..src.helpers import get_script_dir, join_paths, path_exists


class MockSkillEngine:
    """Mock del Skill Engine para el demo"""

    async def validate_skills(self, skills):
        await asyncio.sleep(0.01)
        return {skill: True for skill in skills}

    async def get_skill_info(self, skill_name):
        await asyncio.sleep(0.01)
        return {
            "name": skill_name,
            "status": "active",
            "estimated_cost": 1.0
        }


async def demo_model_mapping():
    """Demo del mapeo de skills a modelos"""
    print("\n" + "=" * 60)
    print("🎯 DEMO 1: MAPEO DE SKILLS A MODELOS NVIDIA")
    print("=" * 60)

    mapper = SkillModelMapper()

    test_skills = [
        ("security-auditor", "Ultra - Seguridad crítica"),
        ("agi-coordinator", "Ultra - Coordinación AGI"),
        ("ai-engineer", "High - Ingeniería de IA"),
        ("code-review-excellence", "High - Revisión de código"),
        ("telegram-bot-builder", "Medium - Desarrollo de bots"),
        ("domain-strategy-router", "Low - Routing rápido"),
    ]

    print("\n📊 Mapeo de Skills a Modelos:")
    print("-" * 60)

    for skill_name, description in test_skills:
        config = mapper.get_model_for_skill(skill_name)
        cost_1k = config.cost_per_1k_tokens
        print(f"\n🔹 {skill_name}")
        print(f"   Tier: {config.tier.upper()}")
        print(f"   Modelo: {config.model_name}")
        print(f"   Costo: ${cost_1k:.4f} por 1K tokens")
        print(f"   Desc: {description}")

    print("\n💰 Estimación de Costos (ejemplo: 1500 tokens):")
    print("-" * 60)

    for skill_name, _ in test_skills[:4]:
        cost = mapper.estimate_cost(skill_name, 1000, 500)
        print(f"   {skill_name}: ${cost:.6f}")


async def demo_tracking_automatico():
    """Demo del tracking automático"""
    print("\n" + "=" * 60)
    print("🎯 DEMO 2: TRACKING AUTOMÁTICO DE EJECUCIONES")
    print("=" * 60)

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        skill_engine = MockSkillEngine()
        cost_tracker = CostTracker(db_path=db_path)

        adapter = MonitoredSkillEngineAdapter(
            skill_engine=skill_engine,
            cost_tracker=cost_tracker,
            enable_tracking=True
        )

        print("\n🚀 Ejecutando skills con tracking automático...")
        print("-" * 60)

        skills_to_execute = [
            ("security-auditor", {"code": "def vulnerable(): pass"}),
            ("ai-engineer", {"task": "design_architecture"}),
            ("code-review-excellence", {"pr": "#123"}),
            ("domain-strategy-router", {"domain": "api.example.com"}),
        ]

        for skill_name, inputs in skills_to_execute:
            request = SkillRequest(
                skill_name=skill_name,
                inputs=inputs,
                agent_name="demo-agent"
            )

            result = await adapter.execute_skill(request)

            status_icon = "✅" if result.status == ExecutionStatus.COMPLETED else "❌"
            print(f"{status_icon} {skill_name}: {result.status.value}")

        print("\n📊 Estadísticas de Tracking:")
        print("-" * 60)

        stats = adapter.get_tracking_stats()
        print(f"   Total trackeado: {stats['total_tracked']}")
        print(f"   Costo total: ${stats['total_cost_tracked']:.6f}")
        print(f"   Tracking activo: {stats['tracking_enabled']}")

        print("\n💰 Resumen de Costos (DB):")
        print("-" * 60)

        summary = cost_tracker.get_cost_summary(period="today")
        print(f"   Ejecuciones: {summary.total_executions}")
        print(f"   Costo total: ${summary.total_cost:.6f}")
        print(f"   Tokens totales: {summary.total_tokens}")
        print(f"   Costo promedio: ${summary.avg_cost_per_execution:.6f}")

        print("\n🏆 Top Skills por Costo:")
        print("-" * 60)

        for skill, cost in sorted(
            summary.skill_breakdown.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]:
            print(f"   {skill}: ${cost:.6f}")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


async def demo_comparacion():
    """Demo comparando adaptadores"""
    print("\n" + "=" * 60)
    print("🎯 DEMO 3: COMPARACIÓN DE ADAPTADORES")
    print("=" * 60)

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        skill_engine = MockSkillEngine()
        normal_adapter = SkillEngineAdapter(skill_engine=skill_engine)

        cost_tracker = CostTracker(db_path=db_path)
        monitored_adapter = MonitoredSkillEngineAdapter(
            skill_engine=skill_engine,
            cost_tracker=cost_tracker
        )

        print("\n🔧 Adaptador Normal:")
        print("-" * 60)

        request = SkillRequest(
            skill_name="security-auditor",
            inputs={"code": "test"}
        )

        result1 = await normal_adapter.execute_skill(request)
        print(f"   Resultado: {result1.status.value}")
        print(f"   Tracking: No disponible")

        print("\n🔍 Adaptador Monitoreado:")
        print("-" * 60)

        result2 = await monitored_adapter.execute_skill(request)
        print(f"   Resultado: {result2.status.value}")
        print(f"   Ejecuciones trackeadas: {monitored_adapter.total_tracked}")
        print(f"   Costo acumulado: ${monitored_adapter.total_cost_tracked:.6f}")

        print("\n✅ Ambos adaptadores retornan el mismo resultado!")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


async def demo_contexto():
    """Demo de contexto playbook/stage"""
    print("\n" + "=" * 60)
    print("🎯 DEMO 4: CONTEXTO DE PLAYBOOK Y STAGES")
    print("=" * 60)

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        skill_engine = MockSkillEngine()
        cost_tracker = CostTracker(db_path=db_path)
        adapter = MonitoredSkillEngineAdapter(
            skill_engine=skill_engine,
            cost_tracker=cost_tracker
        )

        adapter.set_playbook_context(
            playbook_id="playbook-deploy-001",
            stage_id="security-check"
        )

        print("\n📋 Contexto establecido:")
        print("-" * 60)
        print(f"   Playbook: {adapter._playbook_id}")
        print(f"   Stage: {adapter._stage_id}")

        print("\n🚀 Ejecutando skills...")

        for skill in ["security-auditor", "mcp-vetting-guard"]:
            request = SkillRequest(skill_name=skill, inputs={})
            await adapter.execute_skill(request)

        summary = cost_tracker.get_cost_summary(period="today")
        print(f"\n✅ Ejecuciones registradas: {summary.total_executions} skills")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


async def demo_enable_disable():
    """Demo activar/desactivar tracking"""
    print("\n" + "=" * 60)
    print("🎯 DEMO 5: ACTIVAR/DESACTIVAR TRACKING")
    print("=" * 60)

    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name

    try:
        skill_engine = MockSkillEngine()
        cost_tracker = CostTracker(db_path=db_path)
        adapter = MonitoredSkillEngineAdapter(
            skill_engine=skill_engine,
            cost_tracker=cost_tracker
        )

        request = SkillRequest(skill_name="security-auditor", inputs={})

        print("\n✅ Tracking ACTIVADO:")
        adapter.enable()
        await adapter.execute_skill(request)
        print(f"   Ejecuciones: {adapter.total_tracked}")

        print("\n❌ Tracking DESACTIVADO:")
        adapter.disable()
        await adapter.execute_skill(request)
        print(f"   Ejecuciones: {adapter.total_tracked} (no cambió)")

        print("\n✅ Tracking REACTIVADO:")
        adapter.enable()
        await adapter.execute_skill(request)
        print(f"   Ejecuciones: {adapter.total_tracked}")

    finally:
        if os.path.exists(db_path):
            os.unlink(db_path)


async def main():
    """Función principal"""
    print("=" * 60)
    print("🚀 COST MONITOR + SKILL ENGINE INTEGRATION DEMO")
    print("=" * 60)
    print("\nIntegración automática con tracking transparente")

    try:
        await demo_model_mapping()
        await demo_tracking_automatico()
        await demo_comparacion()
        await demo_contexto()
        await demo_enable_disable()

        print("\n" + "=" * 60)
        print("✅ DEMO COMPLETADO EXITOSAMENTE")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
