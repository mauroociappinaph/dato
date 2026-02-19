#!/usr/bin/env python3
"""
Monitored Skill Engine Adapter - Adaptador con Tracking Automático

Este módulo extiende SkillEngineAdapter para añadir tracking automático
de costos sin modificar el código existente del Skill Engine.
"""

import sys
import os
from typing import Optional, Dict, Any
from datetime import datetime

# Añadir paths necesarios
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'playbook_engine_api'))

# Imports del sistema de costos
from core.cost_tracker import CostTracker
from core.alert_manager import AlertManager
from .model_mapper import SkillModelMapper, get_model_for_skill
from .token_tracker import NIMTokenTracker, get_token_tracker

# Imports del Playbook Engine
from playbook_engine_api import (
from ...src.helpers import get_script_dir, join_paths
    SkillEngineAdapter,
    SkillRequest,
    SkillResult,
    StageRequest,
    StageResult,
    ExecutionStatus
)


class MonitoredSkillEngineAdapter(SkillEngineAdapter):
    """
    Adaptador de Skill Engine con monitoreo automático de costos.

    Extiende SkillEngineAdapter para interceptar todas las ejecuciones
    y registrar automáticamente los costos en el CostTracker.

    Usage:
        # Crear adaptador monitoreado
        adapter = MonitoredSkillEngineAdapter(skill_engine)

        # Ejecutar skill - tracking automático
        request = SkillRequest(skill_name="security-auditor", inputs={...})
        result = await adapter.execute_skill(request)

        # El costo se registró automáticamente en la base de datos

        # Desactivar tracking si es necesario
        adapter.enable_tracking = False
    """

    def __init__(
        self,
        skill_engine,
        cost_tracker: Optional[CostTracker] = None,
        alert_manager: Optional[AlertManager] = None,
        enable_tracking: bool = True,
        track_stages: bool = True
    ):
        """
        Inicializa el adaptador monitoreado.

        Args:
            skill_engine: Instancia del Skill Engine
            cost_tracker: Instancia de CostTracker (opcional)
            alert_manager: Instancia de AlertManager (opcional)
            enable_tracking: Si debe hacer tracking automático
            track_stages: Si debe trackear ejecución de stages
        """
        super().__init__(skill_engine)

        # Componentes de tracking
        self.cost_tracker = cost_tracker or CostTracker()
        self.alert_manager = alert_manager
        self.model_mapper = SkillModelMapper()
        self.token_tracker = get_token_tracker()

        # Configuración
        self.enable_tracking = enable_tracking
        self.track_stages = track_stages

        # Estadísticas
        self.total_tracked = 0
        self.total_cost_tracked = 0.0
        self._playbook_id: Optional[str] = None
        self._stage_id: Optional[str] = None

    def set_playbook_context(self, playbook_id: str, stage_id: Optional[str] = None):
        """
        Establece el contexto de playbook para tracking.

        Args:
            playbook_id: ID del playbook en ejecución
            stage_id: ID de la etapa actual (opcional)
        """
        self._playbook_id = playbook_id
        self._stage_id = stage_id

    def clear_playbook_context(self):
        """Limpia el contexto de playbook"""
        self._playbook_id = None
        self._stage_id = None

    async def execute_skill(self, request: SkillRequest) -> SkillResult:
        """
        Ejecuta un skill con tracking automático de costos.

        Args:
            request: Solicitud de ejecución del skill

        Returns:
            SkillResult con resultado de la ejecución
        """
        if not self.enable_tracking:
            # Si el tracking está desactivado, comportamiento normal
            return await super().execute_skill(request)

        # Ejecutar skill con tracking
        start_time = datetime.now()

        try:
            # Obtener modelo para el skill
            model_config = self.model_mapper.get_model_for_skill(request.skill_name)

            # Ejecutar skill (usando el método del padre)
            result = await super().execute_skill(request)

            # Calcular tiempo de ejecución
            execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            # Capturar uso de tokens (estimado o real)
            tokens_input, tokens_output = self._capture_token_usage(request, result)

            # Determinar cluster
            cluster = self._get_cluster_for_skill(request.skill_name)

            # Registrar en CostTracker
            self.cost_tracker.track_execution(
                skill_name=request.skill_name,
                model_used=model_config.model_name,
                tokens_input=tokens_input,
                tokens_output=tokens_output,
                cluster=cluster,
                execution_time_ms=execution_time_ms,
                playbook_id=self._playbook_id,
                stage_id=self._stage_id,
                success=(result.status == ExecutionStatus.COMPLETED),
                metadata={
                    "agent_used": request.agent_name,
                    "tier": model_config.tier,
                    "estimated": True  # Indica que son tokens estimados
                }
            )

            # Actualizar estadísticas
            self.total_tracked += 1
            cost = self.model_mapper.estimate_cost(
                request.skill_name, tokens_input, tokens_output
            )
            self.total_cost_tracked += cost

            # Verificar alertas si hay alert manager
            if self.alert_manager:
                await self._check_budget_alerts()

            return result

        except Exception as e:
            # En caso de error, registrar como fallido
            execution_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)

            self.cost_tracker.track_execution(
                skill_name=request.skill_name,
                model_used="unknown",
                tokens_input=0,
                tokens_output=0,
                cluster="UNKNOWN",
                execution_time_ms=execution_time_ms,
                playbook_id=self._playbook_id,
                stage_id=self._stage_id,
                success=False,
                metadata={"error": str(e)}
            )

            # Re-lanzar la excepción para mantener comportamiento original
            raise

    async def execute_stage(self, request: StageRequest) -> StageResult:
        """
        Ejecuta una etapa con tracking opcional.

        Args:
            request: Solicitud de ejecución de la etapa

        Returns:
            StageResult con resultados de todos los skills
        """
        if not self.enable_tracking or not self.track_stages:
            return await super().execute_stage(request)

        # Establecer contexto de stage
        previous_stage_id = self._stage_id
        self._stage_id = request.stage_name

        try:
            # Ejecutar stage normalmente
            result = await super().execute_stage(request)

            # El tracking de skills individuales ya se hizo en execute_skill
            # Aquí podríamos añadir tracking agregado por stage si se necesita

            return result

        finally:
            # Restaurar contexto anterior
            self._stage_id = previous_stage_id

    def _capture_token_usage(
        self,
        request: SkillRequest,
        result: SkillResult
    ) -> tuple:
        """
        Captura o estima el uso de tokens.

        Args:
            request: Solicitud de ejecución
            result: Resultado de la ejecución

        Returns:
            Tupla (tokens_input, tokens_output)
        """
        # Intentar obtener del token tracker
        last_usage = self.token_tracker.get_last_usage()

        if last_usage and last_usage.timestamp > (datetime.now().timestamp() - 60):
            # Usar datos reales si están disponibles y son recientes
            return (last_usage.tokens_input, last_usage.tokens_output)

        # Estimar basado en el tamaño de los inputs/outputs
        tokens_input = self._estimate_tokens(str(request.inputs))
        tokens_output = self._estimate_tokens(str(result.outputs))

        return (tokens_input, tokens_output)

    def _estimate_tokens(self, text: str) -> int:
        """
        Estima el número de tokens en un texto.

        Args:
            text: Texto a estimar

        Returns:
            Número estimado de tokens
        """
        if not text:
            return 0
        # Estimación conservadora: ~4 caracteres por token
        return max(1, len(text) // 4)

    def _get_cluster_for_skill(self, skill_name: str) -> str:
        """
        Obtiene el cluster para un skill.

        Args:
            skill_name: Nombre del skill

        Returns:
            Nombre del cluster
        """
        tier = self.model_mapper.get_tier_for_skill(skill_name)
        return tier.upper()

    async def _check_budget_alerts(self):
        """Verifica y dispara alertas de presupuesto"""
        if not self.alert_manager:
            return

        # Obtener costo actual del mes
        current_cost = self.cost_tracker.get_current_month_cost()

        # Verificar alertas
        await self.alert_manager.check_budget_alerts(current_cost)

    def get_tracking_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de tracking.

        Returns:
            Diccionario con estadísticas
        """
        return {
            "total_tracked": self.total_tracked,
            "total_cost_tracked": self.total_cost_tracked,
            "tracking_enabled": self.enable_tracking,
            "current_playbook_id": self._playbook_id,
            "current_stage_id": self._stage_id,
            "token_tracker_summary": self.token_tracker.get_usage_summary()
        }

    def enable(self):
        """Activa el tracking"""
        self.enable_tracking = True

    def disable(self):
        """Desactiva el tracking"""
        self.enable_tracking = False


class AutoMonitoredAdapter(MonitoredSkillEngineAdapter):
    """
    Versión que auto-configura el cliente NIM para captura real de tokens.

    Esta versión intenta usar el cliente NVIDIA NIM real para obtener
    tokens exactos en lugar de estimaciones.
    """

    def __init__(self, skill_engine, **kwargs):
        super().__init__(skill_engine, **kwargs)
        self._setup_nim_client()

    def _setup_nim_client(self):
        """Configura el cliente NIM para captura de tokens"""
        try:
            # Intentar importar el cliente NIM
            sys.path.insert(0, os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                'ai-engineer', 'scripts'
            ))
            from nvidia_nim_client import NVIDIANIMClient

            nim_client = NVIDIANIMClient()
            if nim_client.is_available():
                self.token_tracker.set_client(nim_client)
                print("✅ NVIDIA NIM client configured for token tracking")
            else:
                print("⚠️  NVIDIA NIM not available, using token estimation")

        except Exception as e:
            print(f"⚠️  Could not setup NIM client: {e}")
            print("   Using token estimation instead")

    async def execute_skill(self, request: SkillRequest) -> SkillResult:
        """
        Ejecuta skill con intento de captura real de tokens.

        Si el cliente NIM está disponible, intenta ejecutar el skill
        a través del modelo real para obtener tokens exactos.
        """
        # Por ahora, delegar al método base
        # En una implementación completa, aquí se ejecutaría el skill
        # real a través del cliente NIM
        return await super().execute_skill(request)
