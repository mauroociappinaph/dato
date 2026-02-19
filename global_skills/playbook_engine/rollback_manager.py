#!/usr/bin/env python3
"""
Rollback Manager - Sistema de reversión para playbooks

Gestiona estrategias de rollback en caso de fallo durante la ejecución de playbooks.
Proporciona diferentes estrategias de reversión según el tipo de skill y operación.
"""

import asyncio
import json
import logging
import os
import uuid
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path

# Importaciones locales
from anti_gravity.scripts.skill_engine_master import SkillEngineMaster

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RollbackStrategy(Enum):
    """Estrategias de rollback"""
    IMMEDIATE = "immediate"           # Rollback inmediato al primer fallo
    STAGED = "staged"                 # Rollback por etapas completadas
    GRACEFUL = "graceful"             # Intentar completar antes de rollback
    MANUAL = "manual"                 # Requiere intervención manual


class RollbackStatus(Enum):
    """Estados de rollback"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class RollbackOperation:
    """Operación de rollback"""
    operation_id: str
    stage_name: str
    skill_name: str
    rollback_strategy: RollbackStrategy
    rollback_function: Optional[Callable]
    rollback_data: Dict[str, Any]
    status: RollbackStatus
    start_time: datetime
    end_time: Optional[datetime]
    error_message: Optional[str]


@dataclass
class RollbackPlan:
    """Plan de rollback para un playbook"""
    plan_id: str
    playbook_name: str
    execution_id: str
    strategy: RollbackStrategy
    operations: List[RollbackOperation]
    status: RollbackStatus
    created_at: datetime
    completed_at: Optional[datetime]


class RollbackManager:
    """Sistema de gestión de rollback para playbooks"""

    def __init__(self, skill_engine: SkillEngineMaster):
        self.skill_engine = skill_engine
        self.rolls_dir = Path("rollbacks")
        self.rolls_dir.mkdir(exist_ok=True)

        # Estado de rollbacks activos
        self.active_rollbacks: Dict[str, RollbackPlan] = {}

        # Estrategias de rollback por tipo de skill
        self.rollback_strategies = {
            "deploy-automation": self._rollback_deployment,
            "infrastructure-checker": self._rollback_infrastructure,
            "database-migration": self._rollback_database,
            "file-system": self._rollback_file_system,
            "api-integration": self._rollback_api,
            "security-auditor": self._rollback_security,
            "code-reviewer": self._rollback_code_review,
            "test-runner": self._rollback_testing,
            "build-optimizer": self._rollback_build,
            "typescript-pro": self._rollback_typescript
        }

    async def create_rollback_plan(
        self,
        playbook_name: str,
        execution_id: str,
        completed_stages: List[Dict[str, Any]],
        strategy: RollbackStrategy = RollbackStrategy.STAGED
    ) -> RollbackPlan:
        """Crea un plan de rollback basado en etapas completadas"""

        plan_id = str(uuid.uuid4())
        operations = []

        # Crear operaciones de rollback en orden inverso
        for stage_data in reversed(completed_stages):
            stage_name = stage_data['stage_name']
            skills = stage_data.get('skills', [])

            for skill_name in skills:
                rollback_func = self.rollback_strategies.get(skill_name, self._rollback_generic)

                operation = RollbackOperation(
                    operation_id=str(uuid.uuid4()),
                    stage_name=stage_name,
                    skill_name=skill_name,
                    rollback_strategy=strategy,
                    rollback_function=rollback_func,
                    rollback_data={
                        'stage_data': stage_data,
                        'execution_id': execution_id
                    },
                    status=RollbackStatus.PENDING,
                    start_time=datetime.now(),
                    end_time=None,
                    error_message=None
                )

                operations.append(operation)

        rollback_plan = RollbackPlan(
            plan_id=plan_id,
            playbook_name=playbook_name,
            execution_id=execution_id,
            strategy=strategy,
            operations=operations,
            status=RollbackStatus.PENDING,
            created_at=datetime.now(),
            completed_at=None
        )

        self.active_rollbacks[plan_id] = rollback_plan

        logger.info(f"Plan de rollback creado: {plan_id} para {playbook_name} con {len(operations)} operaciones")

        return rollback_plan

    async def execute_rollback(self, plan_id: str) -> bool:
        """Ejecuta un plan de rollback"""
        plan = self.active_rollbacks.get(plan_id)
        if not plan:
            logger.error(f"Plan de rollback no encontrado: {plan_id}")
            return False

        plan.status = RollbackStatus.IN_PROGRESS
        logger.info(f"Iniciando rollback para plan: {plan_id}")

        try:
            if plan.strategy == RollbackStrategy.IMMEDIATE:
                return await self._execute_immediate_rollback(plan)
            elif plan.strategy == RollbackStrategy.STAGED:
                return await self._execute_staged_rollback(plan)
            elif plan.strategy == RollbackStrategy.GRACEFUL:
                return await self._execute_graceful_rollback(plan)
            else:
                logger.error(f"Estrategia de rollback no soportada: {plan.strategy}")
                return False

        except Exception as e:
            logger.error(f"Error ejecutando rollback {plan_id}: {e}")
            plan.status = RollbackStatus.FAILED
            return False

    async def _execute_immediate_rollback(self, plan: RollbackPlan) -> bool:
        """Ejecuta rollback inmediato (primera operación que falle)"""
        for operation in plan.operations:
            try:
                operation.status = RollbackStatus.IN_PROGRESS
                operation.start_time = datetime.now()

                if operation.rollback_function:
                    await operation.rollback_function(operation)

                operation.status = RollbackStatus.COMPLETED
                operation.end_time = datetime.now()

                logger.info(f"Rollback inmediato completado en operación: {operation.operation_id}")
                plan.status = RollbackStatus.COMPLETED
                plan.completed_at = datetime.now()
                return True

            except Exception as e:
                operation.status = RollbackStatus.FAILED
                operation.error_message = str(e)
                operation.end_time = datetime.now()

                logger.error(f"Rollback inmediato fallido en operación: {operation.operation_id} - {e}")
                plan.status = RollbackStatus.FAILED
                plan.completed_at = datetime.now()
                return False

    async def _execute_staged_rollback(self, plan: RollbackPlan) -> bool:
        """Ejecuta rollback por etapas"""
        success_count = 0
        total_operations = len(plan.operations)

        for operation in plan.operations:
            try:
                operation.status = RollbackStatus.IN_PROGRESS
                operation.start_time = datetime.now()

                if operation.rollback_function:
                    await operation.rollback_function(operation)

                operation.status = RollbackStatus.COMPLETED
                operation.end_time = datetime.now()
                success_count += 1

                logger.info(f"Operación de rollback completada: {operation.operation_id}")

            except Exception as e:
                operation.status = RollbackStatus.FAILED
                operation.error_message = str(e)
                operation.end_time = datetime.now()

                logger.error(f"Operación de rollback fallida: {operation.operation_id} - {e}")

        plan.status = RollbackStatus.COMPLETED if success_count == total_operations else RollbackStatus.FAILED
        plan.completed_at = datetime.now()

        logger.info(f"Rollback por etapas completado: {success_count}/{total_operations} operaciones exitosas")
        return plan.status == RollbackStatus.COMPLETED

    async def _execute_graceful_rollback(self, plan: RollbackPlan) -> bool:
        """Ejecuta rollback intentando completar antes de revertir"""
        # En esta estrategia, primero intentamos completar la ejecución
        # y solo hacemos rollback si es absolutamente necesario

        logger.info(f"Rollback gracefully no implementado completamente para {plan.plan_id}")
        plan.status = RollbackStatus.SKIPPED
        plan.completed_at = datetime.now()
        return True

    async def _rollback_deployment(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones de despliegue"""
        logger.info(f"Rolling back deployment: {operation.stage_name}")

        # Simular rollback de despliegue
        # En producción, aquí iría la lógica específica de rollback de despliegue
        await asyncio.sleep(1)  # Simular tiempo de rollback

        # Restaurar versión anterior
        logger.info(f"Deployment rollback completed for {operation.stage_name}")

    async def _rollback_infrastructure(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones de infraestructura"""
        logger.info(f"Rolling back infrastructure changes: {operation.stage_name}")

        # Simular rollback de infraestructura
        await asyncio.sleep(2)  # Simular tiempo de rollback

        # Destruir recursos creados
        logger.info(f"Infrastructure rollback completed for {operation.stage_name}")

    async def _rollback_database(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones de base de datos"""
        logger.info(f"Rolling back database migration: {operation.stage_name}")

        # Simular rollback de base de datos
        await asyncio.sleep(1.5)  # Simular tiempo de rollback

        # Ejecutar migraciones inversas
        logger.info(f"Database rollback completed for {operation.stage_name}")

    async def _rollback_file_system(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones del sistema de archivos"""
        logger.info(f"Rolling back file system changes: {operation.stage_name}")

        # Simular rollback de archivos
        await asyncio.sleep(0.5)  # Simular tiempo de rollback

        # Restaurar archivos desde backup
        logger.info(f"File system rollback completed for {operation.stage_name}")

    async def _rollback_api(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones de API"""
        logger.info(f"Rolling back API integration: {operation.stage_name}")

        # Simular rollback de API
        await asyncio.sleep(0.8)  # Simular tiempo de rollback

        # Deshacer cambios en endpoints
        logger.info(f"API rollback completed for {operation.stage_name}")

    async def _rollback_security(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones de seguridad"""
        logger.info(f"Rolling back security changes: {operation.stage_name}")

        # Simular rollback de seguridad
        await asyncio.sleep(1)  # Simular tiempo de rollback

        # Restaurar configuraciones de seguridad
        logger.info(f"Security rollback completed for {operation.stage_name}")

    async def _rollback_code_review(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones de revisión de código"""
        logger.info(f"Rolling back code review: {operation.stage_name}")

        # Simular rollback de revisión de código
        await asyncio.sleep(0.3)  # Simular tiempo de rollback

        # Eliminar comentarios y marcas de revisión
        logger.info(f"Code review rollback completed for {operation.stage_name}")

    async def _rollback_testing(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones de testing"""
        logger.info(f"Rolling back test execution: {operation.stage_name}")

        # Simular rollback de testing
        await asyncio.sleep(0.5)  # Simular tiempo de rollback

        # Limpiar resultados de tests
        logger.info(f"Testing rollback completed for {operation.stage_name}")

    async def _rollback_build(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones de build"""
        logger.info(f"Rolling back build process: {operation.stage_name}")

        # Simular rollback de build
        await asyncio.sleep(1)  # Simular tiempo de rollback

        # Eliminar artefactos de build
        logger.info(f"Build rollback completed for {operation.stage_name}")

    async def _rollback_typescript(self, operation: RollbackOperation) -> None:
        """Rollback para operaciones de TypeScript"""
        logger.info(f"Rolling back TypeScript compilation: {operation.stage_name}")

        # Simular rollback de TypeScript
        await asyncio.sleep(0.5)  # Simular tiempo de rollback

        # Eliminar archivos compilados
        logger.info(f"TypeScript rollback completed for {operation.stage_name}")

    async def _rollback_generic(self, operation: RollbackOperation) -> None:
        """Rollback genérico para skills no especificados"""
        logger.info(f"Rolling back generic operation: {operation.stage_name} - {operation.skill_name}")

        # Simular rollback genérico
        await asyncio.sleep(0.5)  # Simular tiempo de rollback

        logger.info(f"Generic rollback completed for {operation.stage_name}")

    def get_rollback_status(self, plan_id: str) -> Optional[RollbackPlan]:
        """Obtiene el estado de un plan de rollback"""
        return self.active_rollbacks.get(plan_id)

    def list_active_rollbacks(self) -> List[RollbackPlan]:
        """Lista rollbacks activos"""
        return list(self.active_rollbacks.values())

    async def cleanup_completed_rollbacks(self):
        """Limpia rollbacks completados"""
        completed_rollbacks = []

        for plan_id, plan in self.active_rollbacks.items():
            if plan.status in [RollbackStatus.COMPLETED, RollbackStatus.FAILED, RollbackStatus.SKIPPED]:
                completed_rollbacks.append(plan_id)

        for plan_id in completed_rollbacks:
            del self.active_rollbacks[plan_id]

        if completed_rollbacks:
            logger.info(f"Limpieza de {len(completed_rollbacks)} rollbacks completados")

    def export_rollback_report(self, output_path: str):
        """Exporta reporte de rollbacks a JSON"""
        data = {
            'active_rollbacks': [asdict(plan) for plan in self.active_rollbacks.values()],
            'exported_at': datetime.now().isoformat()
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        logger.info(f"Reporte de rollbacks exportado a: {output_path}")

    async def get_rollback_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas de rollback"""
        total_operations = sum(len(plan.operations) for plan in self.active_rollbacks.values())

        completed_operations = sum(
            sum(1 for op in plan.operations if op.status == RollbackStatus.COMPLETED)
            for plan in self.active_rollbacks.values()
        )

        failed_operations = sum(
            sum(1 for op in plan.operations if op.status == RollbackStatus.FAILED)
            for plan in self.active_rollbacks.values()
        )

        return {
            'total_rollbacks': len(self.active_rollbacks),
            'total_operations': total_operations,
            'completed_operations': completed_operations,
            'failed_operations': failed_operations,
            'success_rate': (completed_operations / total_operations * 100) if total_operations > 0 else 0,
            'strategies_used': list(set(plan.strategy.value for plan in self.active_rollbacks.values()))
        }

    async def create_manual_rollback(
        self,
        playbook_name: str,
        execution_id: str,
        operations: List[Dict[str, Any]]
    ) -> RollbackPlan:
        """Crea un rollback manual con operaciones específicas"""

        plan_id = str(uuid.uuid4())
        rollback_operations = []

        for op_data in operations:
            operation = RollbackOperation(
                operation_id=str(uuid.uuid4()),
                stage_name=op_data.get('stage_name', 'manual'),
                skill_name=op_data.get('skill_name', 'manual'),
                rollback_strategy=RollbackStrategy.MANUAL,
                rollback_function=self._rollback_generic,
                rollback_data=op_data,
                status=RollbackStatus.PENDING,
                start_time=datetime.now(),
                end_time=None,
                error_message=None
            )
            rollback_operations.append(operation)

        rollback_plan = RollbackPlan(
            plan_id=plan_id,
            playbook_name=playbook_name,
            execution_id=execution_id,
            strategy=RollbackStrategy.MANUAL,
            operations=rollback_operations,
            status=RollbackStatus.PENDING,
            created_at=datetime.now(),
            completed_at=None
        )

        self.active_rollbacks[plan_id] = rollback_plan

        logger.info(f"Rollback manual creado: {plan_id} con {len(operations)} operaciones")

        return rollback_plan
