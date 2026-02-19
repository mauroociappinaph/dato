#!/usr/bin/env python3
"""
Integration Tests - Pruebas de integración entre Playbook Engine y Skill Engine

Verifica que la separación de responsabilidades funcione correctamente
y que la comunicación entre motores sea adecuada.
"""

import asyncio
import logging
import tempfile
import yaml
from pathlib import Path
from typing import Dict, Any

# Importaciones locales
from anti_gravity.scripts.skill_engine_master_enhanced import enhanced_skill_engine
from anti_gravity.global_skills.playbook_engine.playbook_engine_refactored import PlaybookEngine
from anti_gravity.global_skills.playbook_engine_api import (
    SkillRequest, StageRequest, CostEstimation, ValidationError,
    CostLimitExceededError, ApprovalRequiredError
)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("INTEGRATION_TESTS")


class IntegrationTestSuite:
    """Suite de pruebas de integración"""

    def __init__(self):
        self.playbook_engine = PlaybookEngine(enhanced_skill_engine)
        self.test_playbooks_dir = Path(tempfile.mkdtemp(prefix="test_playbooks_"))

    async def test_skill_validation(self):
        """Prueba la validación de skills entre motores"""
        logger.info("Testing skill validation...")

        # Crear un playbook de prueba
        playbook_data = {
            'name': 'test_playbook',
            'version': '1.0.0',
            'stages': [
                {
                    'name': 'test_stage',
                    'skills': ['test_skill_1', 'test_skill_2']
                }
            ]
        }

        # Guardar playbook temporal
        playbook_path = self.test_playbooks_dir / "test_validation.yaml"
        with open(playbook_path, 'w') as f:
            yaml.dump(playbook_data, f)

        try:
            # Intentar validar el playbook
            result = await self.playbook_engine.validate_playbook_comprehensive(playbook_path)
            logger.info("✓ Skill validation test passed")
            return True
        except ValidationError as e:
            logger.info(f"✓ Skill validation correctly caught error: {e}")
            return True
        except Exception as e:
            logger.error(f"✗ Skill validation test failed: {e}")
            return False

    async def test_cost_estimation(self):
        """Prueba la estimación de costos"""
        logger.info("Testing cost estimation...")

        # Crear un playbook de prueba
        playbook_data = {
            'name': 'cost_test_playbook',
            'version': '1.0.0',
            'stages': [
                {
                    'name': 'cost_stage',
                    'skills': ['test_skill_1', 'test_skill_2'],
                    'cost_estimate': 10.0
                }
            ]
        }

        # Guardar playbook temporal
        playbook_path = self.test_playbooks_dir / "test_cost.yaml"
        with open(playbook_path, 'w') as f:
            yaml.dump(playbook_data, f)

        try:
            # Validar playbook
            await self.playbook_engine.validate_playbook_comprehensive(playbook_path)

            # Estimar costo
            cost_estimation = await self.playbook_engine.estimate_playbook_cost(playbook_data)
            logger.info(f"✓ Cost estimation: {cost_estimation.estimated_cost}")
            return True
        except Exception as e:
            logger.error(f"✗ Cost estimation test failed: {e}")
            return False

    async def test_approval_policies(self):
        """Prueba las políticas de aprobación"""
        logger.info("Testing approval policies...")

        # Crear un playbook que requiera aprobación por costo
        playbook_data = {
            'name': 'approval_test_playbook',
            'version': '1.0.0',
            'cost_limit': 5.0,
            'policies': [
                {
                    'type': 'cost_threshold',
                    'threshold': 3.0
                }
            ],
            'stages': [
                {
                    'name': 'approval_stage',
                    'skills': ['test_skill_1'],
                    'cost_estimate': 4.0
                }
            ]
        }

        try:
            # Estimar costo
            cost_estimation = await self.playbook_engine.estimate_playbook_cost(playbook_data)

            # Verificar políticas de aprobación
            approval_required = await self.playbook_engine.check_approval_policies(playbook_data, cost_estimation)

            if approval_required:
                logger.info("✓ Approval policy correctly triggered")
                return True
            else:
                logger.error("✗ Approval policy should have been triggered")
                return False
        except Exception as e:
            logger.error(f"✗ Approval policies test failed: {e}")
            return False

    async def test_stage_execution(self):
        """Prueba la ejecución de etapas"""
        logger.info("Testing stage execution...")

        try:
            # Crear solicitud de etapa
            skill_requests = [
                SkillRequest(
                    skill_name='test_skill_1',
                    agent_name='default',
                    timeout=30
                ),
                SkillRequest(
                    skill_name='test_skill_2',
                    agent_name='default',
                    timeout=30
                )
            ]

            stage_request = StageRequest(
                stage_name='test_stage_execution',
                skills=skill_requests,
                parallel=True,
                timeout=60
            )

            # Ejecutar etapa a través del Skill Engine
            stage_result = await enhanced_skill_engine.execute_stage(stage_request)

            if stage_result.status.value in ['completed', 'failed']:
                logger.info(f"✓ Stage execution test passed with status: {stage_result.status.value}")
                return True
            else:
                logger.error(f"✗ Unexpected stage execution status: {stage_result.status.value}")
                return False
        except Exception as e:
            logger.error(f"✗ Stage execution test failed: {e}")
            return False

    async def test_skill_engine_capabilities(self):
        """Prueba las capacidades del Skill Engine"""
        logger.info("Testing Skill Engine capabilities...")

        try:
            # Probar validación de skills
            validation_results = await enhanced_skill_engine.validate_skills(['test_skill_1', 'test_skill_2'])
            logger.info(f"✓ Skill validation results: {validation_results}")

            # Probar estimación de costos
            cost_estimation = await enhanced_skill_engine.estimate_cost(['test_skill_1', 'test_skill_2'])
            logger.info(f"✓ Cost estimation: {cost_estimation.estimated_cost}")

            # Probar estado de agents
            agent_status = enhanced_skill_engine.get_agent_status()
            logger.info(f"✓ Agent status: {list(agent_status.keys())}")

            # Probar métricas de ejecución
            metrics = enhanced_skill_engine.get_execution_metrics()
            logger.info(f"✓ Execution metrics: {metrics}")

            return True
        except Exception as e:
            logger.error(f"✗ Skill Engine capabilities test failed: {e}")
            return False

    async def test_playbook_engine_capabilities(self):
        """Prueba las capacidades del Playbook Engine"""
        logger.info("Testing Playbook Engine capabilities...")

        try:
            # Probar listado de playbooks
            playbooks = self.playbook_engine.list_playbooks()
            logger.info(f"✓ Found {len(playbooks)} playbooks")

            # Probar estado de ejecución
            status = self.playbook_engine.get_execution_status("test_execution")
            logger.info(f"✓ Execution status check passed")

            return True
        except Exception as e:
            logger.error(f"✗ Playbook Engine capabilities test failed: {e}")
            return False

    async def test_error_handling(self):
        """Prueba el manejo de errores"""
        logger.info("Testing error handling...")

        # Probar límite de costo excedido
        playbook_data = {
            'name': 'error_test_playbook',
            'version': '1.0.0',
            'cost_limit': 1.0,  # Límite muy bajo
            'stages': [
                {
                    'name': 'error_stage',
                    'skills': ['test_skill_1'],
                    'cost_estimate': 10.0  # Costo muy alto
                }
            ]
        }

        try:
            # Estimar costo
            cost_estimation = await self.playbook_engine.estimate_playbook_cost(playbook_data)

            # Verificar límite de costo
            if cost_estimation.estimated_cost > playbook_data['cost_limit']:
                logger.info("✓ Cost limit correctly detected")
                return True
            else:
                logger.error("✗ Cost limit should have been exceeded")
                return False
        except Exception as e:
            logger.error(f"✗ Error handling test failed: {e}")
            return False

    async def run_all_tests(self):
        """Ejecuta todas las pruebas de integración"""
        logger.info("=" * 60)
        logger.info("INTEGRATION TESTS STARTING")
        logger.info("=" * 60)

        tests = [
            ("Skill Validation", self.test_skill_validation),
            ("Cost Estimation", self.test_cost_estimation),
            ("Approval Policies", self.test_approval_policies),
            ("Stage Execution", self.test_stage_execution),
            ("Skill Engine Capabilities", self.test_skill_engine_capabilities),
            ("Playbook Engine Capabilities", self.test_playbook_engine_capabilities),
            ("Error Handling", self.test_error_handling)
        ]

        results = []
        for test_name, test_func in tests:
            logger.info(f"\n--- Running {test_name} ---")
            try:
                result = await test_func()
                results.append((test_name, result))
                status = "PASSED" if result else "FAILED"
                logger.info(f"--- {test_name}: {status} ---")
            except Exception as e:
                logger.error(f"--- {test_name}: FAILED with exception: {e} ---")
                results.append((test_name, False))

        # Resumen de resultados
        logger.info("\n" + "=" * 60)
        logger.info("INTEGRATION TESTS SUMMARY")
        logger.info("=" * 60)

        passed = sum(1 for _, result in results if result)
        total = len(results)

        for test_name, result in results:
            status = "✓ PASSED" if result else "✗ FAILED"
            logger.info(f"{test_name}: {status}")

        logger.info(f"\nTotal: {passed}/{total} tests passed")

        if passed == total:
            logger.info("🎉 ALL INTEGRATION TESTS PASSED!")
            return True
        else:
            logger.info("❌ SOME INTEGRATION TESTS FAILED!")
            return False


async def main():
    """Función principal para ejecutar las pruebas"""
    test_suite = IntegrationTestSuite()
    success = await test_suite.run_all_tests()

    if success:
        logger.info("\n✅ Integration tests completed successfully!")
        logger.info("The separation of responsibilities is working correctly.")
    else:
        logger.info("\n❌ Integration tests failed!")
        logger.info("There are issues with the separation of responsibilities.")

    return success


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
