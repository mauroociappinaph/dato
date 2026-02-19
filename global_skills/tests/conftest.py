"""
Pytest configuration and shared fixtures for Global Skills tests.
"""

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, Generator, List
from unittest.mock import MagicMock, Mock

import pytest

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# Path Fixtures
# =============================================================================


@pytest.fixture
def project_root() -> Path:
    """Return the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def test_data_dir() -> Path:
    """Return the test data directory, creating it if needed."""
    data_dir = PROJECT_ROOT / "tests" / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmp:
        yield Path(tmp)


# =============================================================================
# Skill Registry Fixtures
# =============================================================================


@pytest.fixture
def skill_registry_path() -> Path:
    """Return the path to skill_registry.json."""
    return PROJECT_ROOT / "skill_registry.json"


@pytest.fixture
def skill_registry(skill_registry_path: Path) -> List[Dict[str, Any]]:
    """Load and return the skill registry."""
    if not skill_registry_path.exists():
        return []

    with open(skill_registry_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def active_skills(skill_registry: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return only active skills from registry."""
    return [s for s in skill_registry if s.get("status") == "active"]


@pytest.fixture
def sample_skill() -> Dict[str, Any]:
    """Return a sample skill definition for testing."""
    return {
        "name": "test-skill",
        "description": "A test skill for testing purposes",
        "path": "/tmp/test-skill/SKILL.md",
        "id": "test-skill",
        "version": "1.0.0",
        "status": "active",
        "cluster": "TEST",
        "inputs": {"test_input": "string"},
        "outputs": {"test_output": "string"},
        "cost_estimate": {"per_execution": 0.01, "currency": "USD"},
        "preferred_agent": "AGENT_TEST",
    }


# =============================================================================
# Mock Fixtures
# =============================================================================


@pytest.fixture
def mock_skill_engine() -> MagicMock:
    """Create a mock Skill Engine for testing."""
    engine = MagicMock()
    engine.validate_skills.return_value = asyncio.Future()
    engine.validate_skills.return_value.set_result({"test_skill": True})

    engine.execute_skill.return_value = asyncio.Future()
    engine.execute_skill.return_value.set_result({
        "status": "completed",
        "outputs": {"result": "test"},
        "cost": 1.0,
    })

    engine.estimate_cost.return_value = asyncio.Future()
    engine.estimate_cost.return_value.set_result({
        "estimated_cost": 5.0,
        "breakdown": {"test_skill": 5.0},
    })

    engine.get_skill_info.return_value = asyncio.Future()
    engine.get_skill_info.return_value.set_result({
        "name": "test_skill",
        "status": "active",
        "estimated_cost": 5.0,
    })

    return engine


@pytest.fixture
def mock_playbook_engine() -> MagicMock:
    """Create a mock Playbook Engine for testing."""
    engine = MagicMock()
    engine.validate_playbook.return_value = asyncio.Future()
    engine.validate_playbook.return_value.set_result({"valid": True})

    engine.execute_playbook.return_value = asyncio.Future()
    engine.execute_playbook.return_value.set_result({
        "status": "completed",
        "execution_id": "test-123",
    })

    engine.get_execution_status.return_value = asyncio.Future()
    engine.get_execution_status.return_value.set_result({
        "status": "running",
        "progress": 50,
    })

    engine.list_playbooks.return_value = ["test_playbook.yaml"]

    return engine


# =============================================================================
# Helper Fixtures
# =============================================================================


@pytest.fixture
def sample_playbook_data() -> Dict[str, Any]:
    """Return sample playbook data for testing."""
    return {
        "name": "test_playbook",
        "version": "1.0.0",
        "stages": [
            {
                "name": "test_stage",
                "skills": ["test_skill_1", "test_skill_2"],
                "parallel": True,
            }
        ],
    }


@pytest.fixture
def sample_skill_request() -> Dict[str, Any]:
    """Return a sample skill request."""
    return {
        "skill_name": "test_skill",
        "agent_name": "default",
        "timeout": 30,
        "inputs": {"test": "value"},
    }


# =============================================================================
# Environment Fixtures
# =============================================================================


@pytest.fixture(autouse=True)
def clean_env() -> Generator[None, None, None]:
    """Clean environment variables before each test."""
    # Store original env
    original_env = dict(os.environ)

    yield

    # Restore original env
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def test_env_vars() -> Generator[Dict[str, str], None, None]:
    """Set test environment variables."""
    test_vars = {
        "TEST_MODE": "true",
        "LOG_LEVEL": "DEBUG",
    }

    for key, value in test_vars.items():
        os.environ[key] = value

    yield test_vars

    for key in test_vars:
        os.environ.pop(key, None)


# =============================================================================
# Event Loop Fixture
# =============================================================================


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# =============================================================================
# Pytest Configuration
# =============================================================================


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "skill: Skill-specific tests")
    config.addinivalue_line("markers", "slow: Slow tests (>1s)")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on path."""
    for item in items:
        # Add marker based on test location
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)
        elif "skills" in str(item.fspath):
            item.add_marker(pytest.mark.skill)


# =============================================================================
# Custom Assertions
# =============================================================================


class SkillAssertions:
    """Custom assertions for skill testing."""

    @staticmethod
    def assert_valid_skill(skill: Dict[str, Any]) -> None:
        """Assert that a skill definition is valid."""
        required_fields = ["name", "id", "version", "status", "path"]
        for field in required_fields:
            assert field in skill, f"Skill missing required field: {field}"

        assert skill["status"] in ["active", "deprecated", "draft"]

    @staticmethod
    def assert_skill_files_exist(skill: Dict[str, Any], base_path: Path) -> None:
        """Assert that skill files exist on disk."""
        skill_path = Path(skill["path"])
        if not skill_path.is_absolute():
            skill_path = base_path / skill_path

        assert skill_path.exists(), f"Skill file not found: {skill_path}"


@pytest.fixture
def skill_assertions() -> SkillAssertions:
    """Provide custom skill assertions."""
    return SkillAssertions()
