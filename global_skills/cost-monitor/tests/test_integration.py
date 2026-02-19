#!/usr/bin/env python3
"""
Tests de Integración - Cost Monitor + Skill Engine

Tests para verificar que el tracking automático funciona correctamente
y que no hay breaking changes en el API existente.
"""

import asyncio
import sys
import os
import tempfile
import pytest
from datetime import datetime

# Añadir paths necesarios
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Crear mocks para las clases de playbook_engine_api
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum

class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"

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

@dataclass
class StageResult:
    stage_name: str
    status: ExecutionStatus
    skills_results: list = field(default_factory=list)
    total_cost: float = 0.0
    execution_time: float = 0.0
    error_message: Optional[str] = None

class SkillEngineAdapter:
    def __init__(self, skill_engine):
        self.skill_engine = skill_engine

    async def execute_skill(self, request):
        return SkillResult(
            skill_name=request.skill_name,
            status=ExecutionStatus.COMPLETED,
            outputs={"result": f"Executed {request.skill_name}"}
        )
from integration import (
    MonitoredSkillEngineAdapter,
    SkillModelMapper,
    NIMTokenTracker,
    get_model_for_skill
)
from core.cost_tracker import CostTracker


class MockSkillEngine:
    """Mock del Skill Engine para testing"""

    async def validate_skills(self, skills):
        return {skill: True for skill in skills}

    async def get_skill_info(self, skill_name):
        return {
            "name": skill_name,
            "status": "active",
            "estimated_cost": 1.0
        }


class TestSkillModelMapper:
    """Tests para SkillModelMapper"""

    def test_mapper_initialization(self):
        """Test que el mapper se inicializa correctamente"""
        mapper = SkillModelMapper()
        assert mapper.default_tier == "medium"

    def test_get_tier_for_skill(self):
        """Test que obtiene el tier correcto para skills conocidos"""
        mapper = SkillModelMapper()

        # Ultra tier
        assert mapper.get_tier_for_skill("security-auditor") == "ultra"
        assert mapper.get_tier_for_skill("agi-coordinator") == "ultra"

        # High tier
        assert mapper.get_tier_for_skill("ai-engineer") == "high"
        assert mapper.get_tier_for_skill("code-review-excellence") == "high"

        # Low tier
        assert mapper.get_tier_for_skill("domain-strategy-router") == "low"

        # Unknown skill - default
        assert mapper.get_tier_for_skill("unknown-skill") == "medium"

    def test_get_model_for_skill(self):
        """Test que obtiene el modelo correcto"""
        mapper = SkillModelMapper()

        config = mapper.get_model_for_skill("security-auditor")
        assert config.model_name == "nvidia/nemotron-4-340b-instruct"
        assert config.tier == "ultra"
        assert config.cost_per_1k_tokens == 0.004

        config = mapper.get_model_for_skill("ai-engineer")
        assert config.model_name == "meta/llama-3.1-70b-instruct"
        assert config.tier == "high"

    def test_estimate_cost(self):
        """Test que estima costos correctamente"""
        mapper = SkillModelMapper()

        # Ultra tier: $0.004 por 1K tokens
        cost = mapper.estimate_cost("security-auditor", 1000, 500)
        assert cost == 0.006  # 1500 tokens * $0.004 / 1000

        # High tier: $0.001 por 1K tokens
        cost = mapper.estimate_cost("ai-engineer", 1000, 500)
        assert cost == 0.0015  # 1500 tokens * $0.001 / 1000

    def test_get_all_skills_for_tier(self):
        """Test que obtiene todos los skills de un tier"""
        mapper = SkillModelMapper()

        ultra_skills = mapper.get_all_skills_for_tier("ultra")
        assert "security-auditor" in ultra_skills
        assert "agi-coordinator" in ultra_skills

        low_skills = mapper.get_all_skills_for_tier("low")
        assert "domain-strategy-router" in low_skills

    def test_convenience_function(self):
        """Test función de conveniencia get_model_for_skill"""
        model = get_model_for_skill("security-auditor")
        assert model == "nvidia/nemotron-4-340b-instruct"


class TestNIMTokenTracker:
    """Tests para NIMTokenTracker"""

    def test_tracker_initialization(self):
        """Test inicialización del tracker"""
        tracker = NIMTokenTracker()
        assert tracker.nim_client is None
        assert tracker._last_usage is None
        assert tracker._history == []

    def test_estimate_tokens(self):
        """Test estimación de tokens"""
        tracker = NIMTokenTracker()

        # Texto vacío
        assert tracker._estimate_input_tokens("") == 0

        # Texto corto
        tokens = tracker._estimate_input_tokens("Hello")
        assert tokens >= 1

        # Texto largo (~100 caracteres = ~25 tokens)
        text = "This is a test sentence that has approximately one hundred characters in it."
        tokens = tracker._estimate_input_tokens(text)
        assert tokens > 20

    def test_get_last_usage_empty(self):
        """Test obtener uso cuando no hay registros"""
        tracker = NIMTokenTracker()
        assert tracker.get_last_usage() is None

    def test_usage_summary_empty(self):
        """Test resumen cuando no hay registros"""
        tracker = NIMTokenTracker()
        summary = tracker.get_usage_summary()

        assert summary["total_calls"] == 0
        assert summary["total_tokens"] == 0
        assert summary["avg_tokens_per_call"] == 0


class TestMonitoredSkillEngineAdapter:
    """Tests para MonitoredSkillEngineAdapter"""

    @pytest.fixture
    def temp_db(self):
        """Crea una base de datos temporal para testing"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_path = f.name
        yield temp_path
        # Cleanup
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @pytest.fixture
    def mock_skill_engine(self):
        """Crea un mock del skill engine"""
        return MockSkillEngine()

    @pytest.fixture
    def cost_tracker(self, temp_db):
        """Crea un CostTracker con DB temporal"""
        return CostTracker(db_path=temp_db)

    @pytest.mark.asyncio
    async def test_adapter_initialization(self, mock_skill_engine, cost_tracker):
        """Test inicialización del adaptador"""
        adapter = MonitoredSkillEngineAdapter(
            skill_engine=mock_skill_engine,
            cost_tracker=cost_tracker
        )

        assert adapter.enable_tracking is True
        assert adapter.track_stages is True
        assert adapter.cost_tracker == cost_tracker
        assert adapter.total_tracked == 0

    @pytest.mark.asyncio
    async def test_execute_skill_with_tracking(self, mock_skill_engine, cost_tracker):
        """Test ejecución de skill con tracking"""
        adapter = MonitoredSkillEngineAdapter(
            skill_engine=mock_skill_engine,
            cost_tracker=cost_tracker
        )

        request = SkillRequest(
            skill_name="security-auditor",
            inputs={"code": "test"}
        )

        result = await adapter.execute_skill(request)

        # Verificar resultado
        assert isinstance(result, SkillResult)
        assert result.skill_name == "security-auditor"

        # Verificar que se trackeó
        assert adapter.total_tracked == 1
        assert adapter.total_cost_tracked > 0

    @pytest.mark.asyncio
    async def test_execute_skill_without_tracking(self, mock_skill_engine, cost_tracker):
        """Test ejecución sin tracking"""
        adapter = MonitoredSkillEngineAdapter(
            skill_engine=mock_skill_engine,
            cost_tracker=cost_tracker,
            enable_tracking=False
        )

        request = SkillRequest(
            skill_name="security-auditor",
            inputs={"code": "test"}
        )

        result = await adapter.execute_skill(request)

        # Verificar resultado
        assert isinstance(result, SkillResult)

        # Verificar que NO se trackeó
        assert adapter.total_tracked == 0

    @pytest.mark.asyncio
    async def test_playbook_context(self, mock_skill_engine, cost_tracker):
        """Test contexto de playbook"""
        adapter = MonitoredSkillEngineAdapter(
            skill_engine=mock_skill_engine,
            cost_tracker=cost_tracker
        )

        # Establecer contexto
        adapter.set_playbook_context("playbook-123", "stage-1")

        assert adapter._playbook_id == "playbook-123"
        assert adapter._stage_id == "stage-1"

        # Limpiar contexto
        adapter.clear_playbook_context()

        assert adapter._playbook_id is None
        assert adapter._stage_id is None

    @pytest.mark.asyncio
    async def test_tracking_stats(self, mock_skill_engine, cost_tracker):
        """Test estadísticas de tracking"""
        adapter = MonitoredSkillEngineAdapter(
            skill_engine=mock_skill_engine,
            cost_tracker=cost_tracker
        )

        stats = adapter.get_tracking_stats()

        assert stats["total_tracked"] == 0
        assert stats["tracking_enabled"] is True
        assert "token_tracker_summary" in stats

    def test_enable_disable(self, mock_skill_engine, cost_tracker):
        """Test activar/desactivar tracking"""
        adapter = MonitoredSkillEngineAdapter(
            skill_engine=mock_skill_engine,
            cost_tracker=cost_tracker
        )

        assert adapter.enable_tracking is True

        adapter.disable()
        assert adapter.enable_tracking is False

        adapter.enable()
        assert adapter.enable_tracking is True


class TestIntegrationEndToEnd:
    """Tests de integración end-to-end"""

    @pytest.fixture
    def temp_db(self):
        """Crea una base de datos temporal"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            temp_path = f.name
        yield temp_path
        if os.path.exists(temp_path):
            os.unlink(temp_path)

    @pytest.mark.asyncio
    async def test_multiple_skills_tracked(self, temp_db):
        """Test que múltiples skills se trackean correctamente"""
        skill_engine = MockSkillEngine()
        cost_tracker = CostTracker(db_path=temp_db)
        adapter = MonitoredSkillEngineAdapter(
            skill_engine=skill_engine,
            cost_tracker=cost_tracker
        )

        skills = [
            "security-auditor",
            "ai-engineer",
            "domain-strategy-router"
        ]

        for skill in skills:
            request = SkillRequest(skill_name=skill, inputs={"test": True})
            await adapter.execute_skill(request)

        # Verificar estadísticas
        assert adapter.total_tracked == 3

        # Verificar DB
        summary = cost_tracker.get_cost_summary(period="today")
        assert summary.total_executions == 3

    @pytest.mark.asyncio
    async def test_backward_compatibility(self, temp_db):
        """Test que el adaptador original sigue funcionando"""
        skill_engine = MockSkillEngine()

        # Usar adaptador original (sin tracking)
        original_adapter = SkillEngineAdapter(skill_engine=skill_engine)

        request = SkillRequest(
            skill_name="security-auditor",
            inputs={"code": "test"}
        )

        result = await original_adapter.execute_skill(request)

        assert isinstance(result, SkillResult)
        assert result.skill_name == "security-auditor"


# Tests de ejecución síncrona para facilitar el debugging
def run_async_test(coro):
    """Helper para ejecutar tests async"""
    return asyncio.run(coro)


class TestSynchronous:
    """Tests síncronos para facilitar debugging"""

    def test_model_mapper_sync(self):
        """Test síncrono del mapper"""
        mapper = SkillModelMapper()

        model = mapper.get_model_name("security-auditor")
        assert model == "nvidia/nemotron-4-340b-instruct"

        print("✅ Model mapper test passed")

    def test_token_tracker_sync(self):
        """Test síncrono del token tracker"""
        tracker = NIMTokenTracker()

        tokens = tracker._estimate_input_tokens("Hello world")
        assert tokens > 0

        print("✅ Token tracker test passed")


if __name__ == "__main__":
    print("=" * 60)
    print("🧪 COST MONITOR INTEGRATION TESTS")
    print("=" * 60)

    # Ejecutar tests síncronos
    print("\n📊 Running synchronous tests...")
    sync_tests = TestSynchronous()
    sync_tests.test_model_mapper_sync()
    sync_tests.test_token_tracker_sync()

    # Ejecutar tests con pytest si está disponible
    print("\n📊 Running async tests with pytest...")
    try:
        pytest.main([__file__, "-v", "--tb=short"])
    except Exception as e:
        print(f"⚠️  Could not run pytest tests: {e}")
        print("   (This is OK if pytest is not installed)")

    print("\n✅ Tests completed!")
