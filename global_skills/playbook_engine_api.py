#!/usr/bin/env python3
"""
Playbook Engine API Contract - Contrato de interfaz entre Playbook Engine y Skill Engine

Define las interfaces estandarizadas para la comunicación entre motores,
asegurando una separación clara de responsabilidades.
"""

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from enum import Enum

# Importar definiciones core para evitar duplicación DRY
from src.core.interfaces import (
    ExecutionStatus,
    SkillRequest,
    SkillResult,
    StageRequest,
    StageResult,
    CostEstimation,
)


class SkillEngineInterface(ABC):
    """Interfaz del Skill Engine para uso por el Playbook Engine"""

    @abstractmethod
    async def execute_skill(self, request: SkillRequest) -> SkillResult:
        """Ejecuta un skill individual"""
        pass

    @abstractmethod
    async def execute_stage(self, request: StageRequest) -> StageResult:
        """Ejecuta una etapa con múltiples skills"""
        pass

    @abstractmethod
    async def estimate_cost(self, skills: List[str]) -> CostEstimation:
        """Estima el costo de ejecutar una lista de skills"""
        pass

    @abstractmethod
    async def validate_skills(self, skills: List[str]) -> Dict[str, bool]:
        """Valida que los skills existan y sean ejecutables"""
        pass

    @abstractmethod
    async def get_skill_info(self, skill_name: str) -> Dict[str, Any]:
        """Obtiene información detallada de un skill"""
        pass


class PlaybookEngineInterface(ABC):
    """Interfaz del Playbook Engine para uso externo"""

    @abstractmethod
    async def execute_playbook(self, playbook_path: str) -> Dict[str, Any]:
        """Ejecuta un playbook completo"""
        pass

    @abstractmethod
    async def validate_playbook(self, playbook_path: str) -> Dict[str, Any]:
        """Valida un playbook sin ejecutarlo"""
        pass

    @abstractmethod
    async def get_execution_status(self, execution_id: str) -> Dict[str, Any]:
        """Obtiene el estado de una ejecución"""
        pass

    @abstractmethod
    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancela una ejecución en curso"""
        pass

    @abstractmethod
    async def list_playbooks(self) -> List[Dict[str, Any]]:
        """Lista todos los playbooks disponibles"""
        pass


class SkillEngineAdapter:
    """
    Adaptador que implementa SkillEngineInterface usando el Skill Engine existente

    Este adaptador encapsula la lógica del Skill Engine y proporciona una interfaz
    limpia para el Playbook Engine.
    """

    def __init__(self, skill_engine):
        self.skill_engine = skill_engine

    async def execute_skill(self, request: SkillRequest) -> SkillResult:
        """Ejecuta un skill individual a través del Skill Engine"""
        start_time = datetime.now()

        try:
            # Validar skill
            validation_result = await self.skill_engine.validate_skills([request.skill_name])
            if not validation_result.get(request.skill_name, False):
                return SkillResult(
                    skill_name=request.skill_name,
                    status=ExecutionStatus.FAILED,
                    outputs={},
                    cost_incurred=0.0,
                    execution_time=0.0,
                    error_message=f"Skill no válido: {request.skill_name}"
                )

            # Ejecutar skill
            result = await self._execute_with_retry(request)

            execution_time = (datetime.now() - start_time).total_seconds()

            return SkillResult(
                skill_name=request.skill_name,
                status=ExecutionStatus.COMPLETED,
                outputs=result.get('outputs', {}),
                cost_incurred=result.get('cost', 0.0),
                execution_time=execution_time,
                agent_used=request.agent_name
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return SkillResult(
                skill_name=request.skill_name,
                status=ExecutionStatus.FAILED,
                outputs={},
                cost_incurred=0.0,
                execution_time=execution_time,
                error_message=str(e)
            )

    async def execute_stage(self, request: StageRequest) -> StageResult:
        """Ejecuta una etapa con múltiples skills"""
        start_time = datetime.now()

        try:
            # Validar todos los skills de la etapa
            skill_names = [skill.skill_name for skill in request.skills]
            validation_results = await self.skill_engine.validate_skills(skill_names)

            invalid_skills = [name for name, valid in validation_results.items() if not valid]
            if invalid_skills:
                return StageResult(
                    stage_name=request.stage_name,
                    status=ExecutionStatus.FAILED,
                    skills_results=[],
                    total_cost=0.0,
                    execution_time=0.0,
                    error_message=f"Skills inválidos: {invalid_skills}"
                )

            # Ejecutar skills
            if request.parallel:
                # Ejecución paralela
                tasks = [self.execute_skill(skill) for skill in request.skills]
                skills_results = await asyncio.gather(*tasks, return_exceptions=True)

                # Manejar excepciones
                valid_results = []
                for i, result in enumerate(skills_results):
                    if isinstance(result, Exception):
                        valid_results.append(SkillResult(
                            skill_name=request.skills[i].skill_name,
                            status=ExecutionStatus.FAILED,
                            outputs={},
                            cost_incurred=0.0,
                            execution_time=0.0,
                            error_message=str(result)
                        ))
                    else:
                        valid_results.append(result)
            else:
                # Ejecución secuencial
                valid_results = []
                for skill in request.skills:
                    result = await self.execute_skill(skill)
                    valid_results.append(result)

                    # Detener en caso de fallo
                    if result.status == ExecutionStatus.FAILED:
                        break

            # Calcular métricas
            total_cost = sum(result.cost_incurred for result in valid_results)
            execution_time = (datetime.now() - start_time).total_seconds()

            # Determinar estado de la etapa
            if any(result.status == ExecutionStatus.FAILED for result in valid_results):
                status = ExecutionStatus.FAILED
            elif all(result.status == ExecutionStatus.COMPLETED for result in valid_results):
                status = ExecutionStatus.COMPLETED
            else:
                status = ExecutionStatus.RUNNING

            return StageResult(
                stage_name=request.stage_name,
                status=status,
                skills_results=valid_results,
                total_cost=total_cost,
                execution_time=execution_time
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return StageResult(
                stage_name=request.stage_name,
                status=ExecutionStatus.FAILED,
                skills_results=[],
                total_cost=0.0,
                execution_time=execution_time,
                error_message=str(e)
            )

    async def estimate_cost(self, skills: List[str]) -> CostEstimation:
        """Estima el costo de ejecutar una lista de skills"""
        try:
            # Obtener información de costos de cada skill
            cost_breakdown = {}
            total_cost = 0.0

            for skill_name in skills:
                skill_info = await self.skill_engine.get_skill_info(skill_name)
                estimated_cost = skill_info.get('estimated_cost', 0.0)
                cost_breakdown[skill_name] = estimated_cost
                total_cost += estimated_cost

            return CostEstimation(
                estimated_cost=total_cost,
                breakdown=cost_breakdown
            )

        except Exception as e:
            return CostEstimation(
                estimated_cost=0.0,
                breakdown={},
                error_message=str(e)
            )

    async def validate_skills(self, skills: List[str]) -> Dict[str, bool]:
        """Valida que los skills existan y sean ejecutables"""
        results = {}

        for skill_name in skills:
            try:
                # Intentar obtener información del skill
                skill_info = await self.skill_engine.get_skill_info(skill_name)
                results[skill_name] = skill_info is not None and skill_info.get('status') == 'active'
            except Exception:
                results[skill_name] = False

        return results

    async def get_skill_info(self, skill_name: str) -> Dict[str, Any]:
        """Obtiene información detallada de un skill"""
        try:
            return await self.skill_engine.get_skill_info(skill_name)
        except Exception:
            return None

    async def _execute_with_retry(self, request: SkillRequest) -> Dict[str, Any]:
        """Ejecuta un skill con lógica de reintentos"""
        last_exception = None

        for attempt in range(request.retry_attempts):
            try:
                # Aquí iría la llamada real al Skill Engine
                # Por ahora simulamos la ejecución
                result = await self._simulate_skill_execution(request)
                return result

            except Exception as e:
                last_exception = e
                if attempt < request.retry_attempts - 1:
                    await asyncio.sleep(request.retry_delay * (2 ** attempt))  # Exponential backoff
                else:
                    raise last_exception

        raise last_exception

    async def _simulate_skill_execution(self, request: SkillRequest) -> Dict[str, Any]:
        """Simulación de ejecución de skill (para pruebas)"""
        # En producción, esto llamaría al Skill Engine real
        import random
        import time

        # Simular tiempo de ejecución
        await asyncio.sleep(random.uniform(0.1, 0.5))

        # Simular costo
        cost = random.uniform(1.0, 5.0)

        return {
            'skill_name': request.skill_name,
            'status': 'completed',
            'outputs': {'result': f'Executed {request.skill_name} successfully'},
            'cost': cost,
            'agent_used': request.agent_name
        }


# Excepciones personalizadas
class PlaybookEngineError(Exception):
    """Excepción base para errores del Playbook Engine"""
    pass


class SkillExecutionError(PlaybookEngineError):
    """Error durante la ejecución de un skill"""
    pass


class ValidationError(PlaybookEngineError):
    """Error durante la validación de un playbook o skill"""
    pass


class CostLimitExceededError(PlaybookEngineError):
    """Error cuando se excede el límite de costo"""
    pass


class ApprovalRequiredError(PlaybookEngineError):
    """Error cuando se requiere aprobación para continuar"""
    pass
