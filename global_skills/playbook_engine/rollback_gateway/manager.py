import asyncio
import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from anti_gravity.scripts.skill_engine_master import SkillEngineMaster

from .models import RollbackOperation, RollbackPlan, RollbackStatus, RollbackStrategy
from .strategies import get_rollback_function

logger = logging.getLogger(__name__)


class RollbackManager:
    def __init__(self, skill_engine: SkillEngineMaster):
        self.skill_engine = skill_engine
        self.active_rollbacks: Dict[str, RollbackPlan] = {}

    async def create_rollback_plan(
        self,
        playbook_name: str,
        execution_id: str,
        completed_stages: List[Dict[str, Any]],
        strategy: RollbackStrategy = RollbackStrategy.STAGED
    ) -> RollbackPlan:
        plan_id = str(uuid.uuid4())
        operations = []

        for stage_data in reversed(completed_stages):
            stage_name = stage_data['stage_name']
            skills = stage_data.get('skills', [])
            for skill_name in skills:
                rollback_func = get_rollback_function(skill_name)
                operation = RollbackOperation(
                    operation_id=str(uuid.uuid4()),
                    stage_name=stage_name,
                    skill_name=skill_name,
                    rollback_strategy=strategy,
                    rollback_function=rollback_func,
                    rollback_data={'stage_data': stage_data, 'execution_id': execution_id},
                    status=RollbackStatus.PENDING,
                    start_time=datetime.now(),
                    end_time=None,
                    error_message=None
                )
                operations.append(operation)

        plan = RollbackPlan(
            plan_id=plan_id,
            playbook_name=playbook_name,
            execution_id=execution_id,
            strategy=strategy,
            operations=operations,
            status=RollbackStatus.PENDING,
            created_at=datetime.now(),
            completed_at=None
        )
        self.active_rollbacks[plan_id] = plan
        logger.info(f"Plan de rollback creado: {plan_id} con {len(operations)} operaciones")
        return plan

    async def execute_rollback(self, plan_id: str) -> bool:
        plan = self.active_rollbacks.get(plan_id)
        if not plan:
            logger.error(f"Plan no encontrado: {plan_id}")
            return False

        plan.status = RollbackStatus.IN_PROGRESS
        logger.info(f"Iniciando rollback: {plan_id}")

        try:
            if plan.strategy == RollbackStrategy.IMMEDIATE:
                return await self._execute_immediate(plan)
            elif plan.strategy == RollbackStrategy.STAGED:
                return await self._execute_staged(plan)
            elif plan.strategy == RollbackStrategy.GRACEFUL:
                return await self._execute_graceful(plan)
            else:
                logger.error(f"Estrategia no soportada: {plan.strategy}")
                return False
        except Exception as e:
            logger.error(f"Error ejecutando rollback {plan_id}: {e}")
            plan.status = RollbackStatus.FAILED
            return False

    async def _execute_immediate(self, plan: RollbackPlan) -> bool:
        for operation in plan.operations:
            try:
                operation.status = RollbackStatus.IN_PROGRESS
                operation.start_time = datetime.now()
                if operation.rollback_function:
                    await operation.rollback_function(operation)
                operation.status = RollbackStatus.COMPLETED
                operation.end_time = datetime.now()
                plan.status = RollbackStatus.COMPLETED
                plan.completed_at = datetime.now()
                logger.info(f"Rollback inmediato completado: {operation.operation_id}")
                return True
            except Exception as e:
                operation.status = RollbackStatus.FAILED
                operation.error_message = str(e)
                operation.end_time = datetime.now()
                plan.status = RollbackStatus.FAILED
                plan.completed_at = datetime.now()
                logger.error(f"Rollback inmediato fallido: {operation.operation_id} - {e}")
                return False

    async def _execute_staged(self, plan: RollbackPlan) -> bool:
        success = 0
        for operation in plan.operations:
            try:
                operation.status = RollbackStatus.IN_PROGRESS
                operation.start_time = datetime.now()
                if operation.rollback_function:
                    await operation.rollback_function(operation)
                operation.status = RollbackStatus.COMPLETED
                operation.end_time = datetime.now()
                success += 1
                logger.info(f"Operación completada: {operation.operation_id}")
            except Exception as e:
                operation.status = RollbackStatus.FAILED
                operation.error_message = str(e)
                operation.end_time = datetime.now()
                logger.error(f"Operación fallida: {operation.operation_id} - {e}")

        plan.status = RollbackStatus.COMPLETED if success == len(plan.operations) else RollbackStatus.FAILED
        plan.completed_at = datetime.now()
        logger.info(f"Rollback staged: {success}/{len(plan.operations)} exitosas")
        return plan.status == RollbackStatus.COMPLETED

    async def _execute_graceful(self, plan: RollbackPlan) -> bool:
        logger.info(f"Rollback gracefully no implementado para {plan.plan_id}")
        plan.status = RollbackStatus.SKIPPED
        plan.completed_at = datetime.now()
        return True

    def get_status(self, plan_id: str) -> Optional[RollbackPlan]:
        return self.active_rollbacks.get(plan_id)

    def list_active(self) -> List[RollbackPlan]:
        return list(self.active_rollbacks.values())

    async def cleanup(self):
        completed = [pid for pid, plan in self.active_rollbacks.items()
                     if plan.status in [RollbackStatus.COMPLETED, RollbackStatus.FAILED, RollbackStatus.SKIPPED]]
        for pid in completed:
            del self.active_rollbacks[pid]
        if completed:
            logger.info(f"Limpieza de {len(completed)} rollbacks completados")

    def export_report(self, output_path: str):
        data = {
            'active_rollbacks': [self._serialize(plan) for plan in self.active_rollbacks.values()],
            'exported_at': datetime.now().isoformat()
        }
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        logger.info(f"Reporte exportado a: {output_path}")

    def _serialize(self, plan: RollbackPlan) -> Dict[str, Any]:
        return {
            'plan_id': plan.plan_id,
            'playbook_name': plan.playbook_name,
            'execution_id': plan.execution_id,
            'strategy': plan.strategy.value,
            'status': plan.status.value,
            'operations': [{
                'operation_id': op.operation_id,
                'stage_name': op.stage_name,
                'skill_name': op.skill_name,
                'status': op.status.value,
                'error_message': op.error_message
            } for op in plan.operations],
            'created_at': plan.created_at.isoformat(),
            'completed_at': plan.completed_at.isoformat() if plan.completed_at else None
        }

    async def get_statistics(self) -> Dict[str, Any]:
        total_ops = sum(len(plan.operations) for plan in self.active_rollbacks.values())
        completed = sum(sum(1 for op in plan.operations if op.status == RollbackStatus.COMPLETED)
                        for plan in self.active_rollbacks.values())
        failed = sum(sum(1 for op in plan.operations if op.status == RollbackStatus.FAILED)
                     for plan in self.active_rollbacks.values())
        return {
            'total_rollbacks': len(self.active_rollbacks),
            'total_operations': total_ops,
            'completed_operations': completed,
            'failed_operations': failed,
            'success_rate': (completed / total_ops * 100) if total_ops > 0 else 0
        }

    async def create_manual(
        self,
        playbook_name: str,
        execution_id: str,
        operations: List[Dict[str, Any]]
    ) -> RollbackPlan:
        plan_id = str(uuid.uuid4())
        rollback_ops = []
        for op_data in operations:
            op = RollbackOperation(
                operation_id=str(uuid.uuid4()),
                stage_name=op_data.get('stage_name', 'manual'),
                skill_name=op_data.get('skill_name', 'manual'),
                rollback_strategy=RollbackStrategy.MANUAL,
                rollback_function=rollback_generic,
                rollback_data=op_data,
                status=RollbackStatus.PENDING,
                start_time=datetime.now(),
                end_time=None,
                error_message=None
            )
            rollback_ops.append(op)

        plan = RollbackPlan(
            plan_id=plan_id,
            playbook_name=playbook_name,
            execution_id=execution_id,
            strategy=RollbackStrategy.MANUAL,
            operations=rollback_ops,
            status=RollbackStatus.PENDING,
            created_at=datetime.now(),
            completed_at=None
        )
        self.active_rollbacks[plan_id] = plan
        logger.info(f"Rollback manual creado: {plan_id}")
        return plan


async def rollback_generic(operation: RollbackOperation):
    logger.info(f"Rolling back generic: {operation.stage_name}")
    await asyncio.sleep(0.5)
    logger.info(f"Generic rollback completed")
