#!/usr/bin/env python3
"""
Playbook Engine - Motor de ejecución de playbooks declarativos (Refactorizado)

Responsabilidades claras según la nueva arquitectura:

PLAYBOOK ENGINE (ESTE ARCHIVO):
- Validación de estructura de playbooks
- Orquestación de etapas (secuencial/concurrente)
- Gestión de políticas de aprobación
- Coordinación de rollback
- Métricas de alto nivel
- Interfaz con el Skill Engine a través de la API

SKILL ENGINE (separado):
- Selección y gestión de agents
- Ejecución individual de skills
- Gestión de recursos y concurrencia
- Costos por skill
- Manejo de errores a nivel de skill
"""

import asyncio
import json
import logging
import os
import sys
import yaml
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

# Importaciones locales
from anti_gravity.scripts.skill_engine_master import SkillEngineMaster
from anti_gravity.global_skills.cost_control.mcp_cost_controller import MCPCostController
from anti_gravity.global_skills.skill_registry_manager.scripts.validate_skill_schema import validate_skill_schema
from anti_gravity.global_skills.playbook_engine_api import (
    SkillEngineAdapter, SkillRequest, StageRequest, CostEstimation,
    PlaybookEngineError, ValidationError, CostLimitExceededError, ApprovalRequiredError
)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlaybookStatus(Enum):
    """Estados de ejecución de un playbook"""
    PENDING = "pending"
    RUNNING = "running"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"
    FAILED = "failed"
    ROLLING_BACK = "rolling_back"
    ROLLED_BACK = "rolled_back"


@dataclass
class StageResult:
    """Resultado de ejecución de una etapa"""
    stage_name: str
    status: PlaybookStatus
    cost_incurred: float
    start_time: datetime
    end_time: Optional[datetime]
    error_message: Optional[str]
    outputs: Dict[str, Any]


@dataclass
class PlaybookExecution:
    """Información de ejecución de un playbook"""
    playbook_name: str
    execution_id: str
    status: PlaybookStatus
    total_cost: float
    start_time: datetime
    end_time: Optional[datetime]
    stages: List[StageResult]
    approval_required: bool


class PlaybookEngine:
    """Motor de ejecución de playbooks declarativos - Versión Refactorizada"""

    def __init__(self, skill_engine: SkillEngineMaster):
        self.skill_engine = skill_engine
        self.skill_adapter = SkillEngineAdapter(skill_engine)
        self.cost_controller = MCPCostController()
        self.playbooks_dir = Path("playbooks")
        self.playbooks_dir.mkdir(exist_ok=True)

        # Estado de ejecuciones activas
        self.active_executions: Dict[str, PlaybookExecution] = {}

    async def parse_playbook(self, playbook_path: Union[str, Path]) -> Dict[str, Any]:
        """Parsea y valida un archivo de playbook - SOLO VALIDACIÓN DE ESTRUCTURA"""
        path = Path(playbook_path)

        if not path.exists():
            raise FileNotFoundError(f"Playbook no encontrado: {path}")

        # Determinar formato por extensión
        if path.suffix.lower() in ['.yaml', '.yml']:
            with open(path, 'r') as f:
                playbook_data = yaml.safe_load(f)
        elif path.suffix.lower() == '.json':
            with open(path, 'r') as f:
                playbook_data = json.load(f)
        else:
            raise ValueError(f"Formato no soportado: {path.suffix}")

        # Validar estructura básica (SOLO ESTRUCTURA, no skills)
        self._validate_playbook_structure(playbook_data)

        return playbook_data

    def _validate_playbook_structure(self, playbook_data: Dict[str, Any]):
        """Valida SOLO la estructura básica del playbook"""
        required_fields = ['name', 'version', 'stages']
        for field in required_fields:
            if field not in playbook_data:
                raise ValidationError(f"Campo requerido faltante: {field}")

        # Validar etapas
        for i, stage in enumerate(playbook_data['stages']):
            if 'name' not in stage:
                raise ValidationError(f"Etapas {i+1} no tiene nombre")
            if 'skills' not in stage:
                raise ValidationError(f"Etapas {i+1} no tiene skills definidos")

    async def validate_playbook_comprehensive(self, playbook_path: Union[str, Path]) -> Dict[str, Any]:
        """Validación completa del playbook incluyendo skills"""
        playbook_data = await self.parse_playbook(playbook_path)

        # Validar skills a través del Skill Engine
        all_skills = []
        for stage in playbook_data['stages']:
            all_skills.extend(stage.get('skills', []))

        validation_results = await self.skill_adapter.validate_skills(list(set(all_skills)))

        invalid_skills = [name for name, valid in validation_results.items() if not valid]
        if invalid_skills:
            raise ValidationError(f"Skills inválidos: {invalid_skills}")

        return playbook_data

    async def estimate_playbook_cost(self, playbook_data: Dict[str, Any]) -> CostEstimation:
        """Estima el costo total del playbook"""
        all_skills = []
        for stage in playbook_data['stages']:
            all_skills.extend(stage.get('skills', []))

        return await self.skill_adapter.estimate_cost(list(set(all_skills)))

    async def check_approval_policies(self, playbook_data: Dict[str, Any], cost_estimation: CostEstimation) -> bool:
        """Verifica si el playbook requiere aprobación según políticas"""
        policies = playbook_data.get('policies', [])

        for policy in policies:
            policy_type = policy.get('type')

            if policy_type == 'cost_threshold':
                threshold = policy.get('threshold', 0.0)
                if cost_estimation.estimated_cost >= threshold:
                    return True

            elif policy_type == 'skill_diversity':
                min_agents = policy.get('min_agents', 1)
                unique_agents = set()
                for stage in playbook_data['stages']:
                    agent = stage.get('agent', 'default')
                    unique_agents.add(agent)

                if len(unique_agents) < min_agents:
                    return True

        # Verificar si alguna etapa requiere aprobación
        for stage in playbook_data['stages']:
            if stage.get('approval_required', False):
                return True

        return False

    async def execute_playbook(self, playbook_path: Union[str, Path]) -> PlaybookExecution:
        """Ejecuta un playbook completo - ORQUESTACIÓN DE ALTO NIVEL"""
        playbook_data = await self.validate_playbook_comprehensive(playbook_path)
        playbook_name = playbook_data['name']

        # Estimar costo total
        cost_estimation = await self.estimate_playbook_cost(playbook_data)
        cost_limit = playbook_data.get('cost_limit', float('inf'))

        # Verificar límite de costo
        if cost_estimation.estimated_cost > cost_limit:
            raise CostLimitExceededError(f"Costo estimado ({cost_estimation.estimated_cost}) excede el límite ({cost_limit})")

        # Verificar políticas de aprobación
        approval_required = await self.check_approval_policies(playbook_data, cost_estimation)

        # Crear registro de ejecución
        execution_id = f"{playbook_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        execution = PlaybookExecution(
            playbook_name=playbook_name,
            execution_id=execution_id,
            status=PlaybookStatus.PENDING,
            total_cost=0.0,
            start_time=datetime.now(),
            end_time=None,
            stages=[],
            approval_required=approval_required
        )

        self.active_executions[execution_id] = execution

        try:
            # Si requiere aprobación, esperar aprobación
            if approval_required:
                # En producción, aquí iría el sistema de aprobación real
                execution.status = PlaybookStatus.APPROVED
                logger.info(f"Playbook {playbook_name} requiere aprobación (simulada)")

            execution.status = PlaybookStatus.RUNNING
            logger.info(f"Iniciando ejecución de playbook: {playbook_name}")

            # Ejecutar etapas - ORQUESTACIÓN DE ALTO NIVEL
            await self._execute_stages(playbook_data, execution)

            execution.status = PlaybookStatus.COMPLETED
            execution.end_time = datetime.now()

            logger.info(f"Playbook {playbook_name} completado exitosamente")

        except Exception as e:
            execution.status = PlaybookStatus.FAILED
            execution.end_time = datetime.now()
            logger.error(f"Error ejecutando playbook {playbook_name}: {e}")

            # Intentar rollback si está habilitado
            if playbook_data.get('rollback_on_failure', False):
                await self._execute_rollback(playbook_data, execution)

        finally:
            # Registrar costo final
            final_cost = await self.cost_controller.get_tenant_cost("playbook_execution")
            execution.total_cost = final_cost

        return execution

    async def _execute_stages(self, playbook_data: Dict[str, Any], execution: PlaybookExecution):
        """Ejecuta las etapas del playbook - ORQUESTACIÓN DE ETAPAS"""
        stages = playbook_data['stages']

        for i, stage_data in enumerate(stages):
            stage_name = stage_data['name']
            skills = stage_data['skills']
            agent_name = stage_data.get('agent', 'default')
            parallel = stage_data.get('parallel', False)

            logger.info(f"Ejecutando etapa {i+1}/{len(stages)}: {stage_name}")

            # Crear solicitud de etapa para el Skill Engine
            skill_requests = [
                SkillRequest(
                    skill_name=skill_name,
                    agent_name=agent_name,
                    timeout=stage_data.get('timeout', 300),
                    retry_attempts=stage_data.get('retry_attempts', 3)
                )
                for skill_name in skills
            ]

            stage_request = StageRequest(
                stage_name=stage_name,
                skills=skill_requests,
                parallel=parallel,
                timeout=stage_data.get('timeout', 300)
            )

            # Ejecutar etapa a través del Skill Engine
            stage_result = await self.skill_adapter.execute_stage(stage_request)

            # Convertir resultado del Skill Engine a formato del Playbook Engine
            playbook_stage_result = StageResult(
                stage_name=stage_name,
                status=self._convert_status(stage_result.status),
                cost_incurred=stage_result.total_cost,
                start_time=datetime.now(),  # Simplificado para el ejemplo
                end_time=datetime.now(),
                error_message=stage_result.error_message,
                outputs={"skills_results": [asdict(sr) for sr in stage_result.skills_results]}
            )

            execution.stages.append(playbook_stage_result)

            # Verificar si la etapa requiere aprobación
            if stage_data.get('approval_required', False):
                logger.info(f"Etapas {stage_name} requiere aprobación (simulada)")

            # Verificar costo acumulado
            await self._check_cost_limits(playbook_data, execution)

    def _convert_status(self, skill_status):
        """Convierte status del Skill Engine al del Playbook Engine"""
        status_mapping = {
            'pending': PlaybookStatus.PENDING,
            'running': PlaybookStatus.RUNNING,
            'completed': PlaybookStatus.COMPLETED,
            'failed': PlaybookStatus.FAILED,
            'timeout': PlaybookStatus.FAILED,
            'cancelled': PlaybookStatus.FAILED
        }
        return status_mapping.get(skill_status.value, PlaybookStatus.FAILED)

    async def _check_cost_limits(self, playbook_data: Dict[str, Any], execution: PlaybookExecution):
        """Verifica límites de costo durante la ejecución"""
        current_cost = execution.total_cost
        cost_limit = playbook_data.get('cost_limit', float('inf'))

        if current_cost >= cost_limit:
            raise CostLimitExceededError(f"Límite de costo alcanzado: {current_cost}/{cost_limit}")

        # Alerta de costo cercano al límite
        if current_cost >= cost_limit * 0.8:
            logger.warning(f"Costo cercano al límite: {current_cost}/{cost_limit}")

    async def _execute_rollback(self, playbook_data: Dict[str, Any], execution: PlaybookExecution):
        """Ejecuta rollback en caso de fallo - COORDINACIÓN DE ROLLBACK"""
        logger.info(f"Iniciando rollback para playbook: {execution.playbook_name}")

        execution.status = PlaybookStatus.ROLLING_BACK

        # Ejecutar rollback en orden inverso
        for stage in reversed(execution.stages):
            if stage.status == PlaybookStatus.COMPLETED:
                logger.info(f"Rolling back stage: {stage.stage_name}")
                # Aquí iría la lógica de rollback específica por skill
                # En una implementación completa, esto llamaría al Skill Engine
                # para ejecutar operaciones de rollback

        execution.status = PlaybookStatus.ROLLED_BACK
        logger.info(f"Rollback completado para playbook: {execution.playbook_name}")

    def list_playbooks(self) -> List[Dict[str, Any]]:
        """Lista todos los playbooks disponibles"""
        playbooks = []

        for file_path in self.playbooks_dir.glob("*.{yaml,yml,json}"):
            try:
                with open(file_path, 'r') as f:
                    if file_path.suffix.lower() in ['.yaml', '.yml']:
                        data = yaml.safe_load(f)
                    else:
                        data = json.load(f)

                playbooks.append({
                    'name': data.get('name', file_path.stem),
                    'description': data.get('description', ''),
                    'version': data.get('version', '1.0.0'),
                    'path': str(file_path)
                })

            except Exception as e:
                logger.error(f"Error leyendo playbook {file_path}: {e}")

        return playbooks

    def get_execution_status(self, execution_id: str) -> Optional[PlaybookExecution]:
        """Obtiene el estado de una ejecución específica"""
        return self.active_executions.get(execution_id)


async def main():
    """Función principal para CLI"""
    if len(sys.argv) < 2:
        print("Uso: python3 playbook_engine_refactored.py <comando> [argumentos]")
        print("Comandos:")
        print("  run <playbook_path>  - Ejecutar un playbook")
        print("  validate <playbook_path> - Validar un playbook")
        print("  list - Listar playbooks disponibles")
        sys.exit(1)

    command = sys.argv[1]

    # Inicializar componentes
    skill_engine = SkillEngineMaster()
    engine = PlaybookEngine(skill_engine)

    if command == "run":
        if len(sys.argv) < 3:
            print("Uso: python3 playbook_engine_refactored.py run <playbook_path>")
            sys.exit(1)

        playbook_path = sys.argv[2]
        try:
            execution = await engine.execute_playbook(playbook_path)
            print(f"Playbook completado: {execution.playbook_name}")
            print(f"Costo total: ${execution.total_cost:.2f}")
            print(f"Duración: {execution.end_time - execution.start_time}")
        except Exception as e:
            print(f"Error ejecutando playbook: {e}")
            sys.exit(1)

    elif command == "validate":
        if len(sys.argv) < 3:
            print("Uso: python3 playbook_engine_refactored.py validate <playbook_path>")
            sys.exit(1)

        playbook_path = sys.argv[2]
        try:
            await engine.validate_playbook_comprehensive(playbook_path)
            print(f"Playbook válido: {playbook_path}")
        except Exception as e:
            print(f"Playbook inválido: {e}")
            sys.exit(1)

    elif command == "list":
        playbooks = engine.list_playbooks()
        print("Playbooks disponibles:")
        for pb in playbooks:
            print(f"  - {pb['name']} ({pb['version']})")
            if pb['description']:
                print(f"    {pb['description']}")
    else:
        print(f"Comando desconocido: {command}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
