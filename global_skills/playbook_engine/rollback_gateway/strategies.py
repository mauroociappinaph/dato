import asyncio
import logging
from .models import RollbackOperation

logger = logging.getLogger(__name__)


async def rollback_deployment(operation: RollbackOperation):
    logger.info(f"Rolling back deployment: {operation.stage_name}")
    await asyncio.sleep(1)
    logger.info(f"Deployment rollback completed for {operation.stage_name}")


async def rollback_infrastructure(operation: RollbackOperation):
    logger.info(f"Rolling back infrastructure changes: {operation.stage_name}")
    await asyncio.sleep(2)
    logger.info(f"Infrastructure rollback completed for {operation.stage_name}")


async def rollback_database(operation: RollbackOperation):
    logger.info(f"Rolling back database migration: {operation.stage_name}")
    await asyncio.sleep(1.5)
    logger.info(f"Database rollback completed for {operation.stage_name}")


async def rollback_file_system(operation: RollbackOperation):
    logger.info(f"Rolling back file system changes: {operation.stage_name}")
    await asyncio.sleep(0.5)
    logger.info(f"File system rollback completed for {operation.stage_name}")


async def rollback_api(operation: RollbackOperation):
    logger.info(f"Rolling back API integration: {operation.stage_name}")
    await asyncio.sleep(0.8)
    logger.info(f"API rollback completed for {operation.stage_name}")


async def rollback_security(operation: RollbackOperation):
    logger.info(f"Rolling back security changes: {operation.stage_name}")
    await asyncio.sleep(1)
    logger.info(f"Security rollback completed for {operation.stage_name}")


async def rollback_code_review(operation: RollbackOperation):
    logger.info(f"Rolling back code review: {operation.stage_name}")
    await asyncio.sleep(0.3)
    logger.info(f"Code review rollback completed for {operation.stage_name}")


async def rollback_testing(operation: RollbackOperation):
    logger.info(f"Rolling back test execution: {operation.stage_name}")
    await asyncio.sleep(0.5)
    logger.info(f"Testing rollback completed for {operation.stage_name}")


async def rollback_build(operation: RollbackOperation):
    logger.info(f"Rolling back build process: {operation.stage_name}")
    await asyncio.sleep(1)
    logger.info(f"Build rollback completed for {operation.stage_name}")


async def rollback_typescript(operation: RollbackOperation):
    logger.info(f"Rolling back TypeScript compilation: {operation.stage_name}")
    await asyncio.sleep(0.5)
    logger.info(f"TypeScript rollback completed for {operation.stage_name}")


async def rollback_generic(operation: RollbackOperation):
    logger.info(f"Rolling back generic operation: {operation.stage_name} - {operation.skill_name}")
    await asyncio.sleep(0.5)
    logger.info(f"Generic rollback completed for {operation.stage_name}")


STRATEGY_MAP = {
    "deploy-automation": rollback_deployment,
    "infrastructure-checker": rollback_infrastructure,
    "database-migration": rollback_database,
    "file-system": rollback_file_system,
    "api-integration": rollback_api,
    "security-auditor": rollback_security,
    "code-reviewer": rollback_code_review,
    "test-runner": rollback_testing,
    "build-optimizer": rollback_build,
    "typescript-pro": rollback_typescript
}


def get_rollback_function(skill_name: str) -> Callable:
    return STRATEGY_MAP.get(skill_name, rollback_generic)
