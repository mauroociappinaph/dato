"""
Core interfaces for Global Skills.

Defines the contracts between different components of the system,
ensuring loose coupling and testability.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ExecutionStatus(Enum):
    """Status for playbook/stage execution."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class SkillRequest:
    """Request to execute a skill."""
    skill_name: str
    inputs: Dict[str, Any]
    agent_name: Optional[str] = None
    timeout: Optional[int] = None
    retry_attempts: int = 3
    retry_delay: float = 1.0
    context: Dict[str, Any] = None

    def __post_init__(self):
        if self.context is None:
            self.context = {}


@dataclass
class StageRequest:
    """Request to execute a stage (collection of skills)."""
    stage_name: str
    skills: List[SkillRequest]
    parallel: bool = False
    timeout: Optional[int] = None
    cost_limit: Optional[float] = None


@dataclass
class CostEstimation:
    """Cost estimation for execution."""
    estimated_cost: float
    breakdown: Dict[str, float]
    currency: str = "USD"
    confidence: float = 0.9


class SkillEngineInterface(ABC):
    """
    Interface for the Skill Engine.

    The Skill Engine is responsible for:
    - Skill validation
    - Skill execution
    - Agent management
    - Cost estimation
    - Resource monitoring
    """

    @abstractmethod
    async def execute_skill(self, request: SkillRequest) -> SkillResult:
        """Execute a single skill."""
        pass

    @abstractmethod
    async def execute_stage(self, request: StageRequest) -> StageResult:
        """Execute a stage with multiple skills."""
        pass

    @abstractmethod
    async def validate_skill(self, skill_name: str) -> bool:
        """Validate that a skill exists and is executable."""
        pass

    @abstractmethod
    async def estimate_cost(self, skill_names: List[str]) -> CostEstimation:
        """Estimate the cost of executing multiple skills."""
        pass

    @abstractmethod
    async def get_skill_info(self, skill_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a skill."""
        pass

    @abstractmethod
    def list_skills(self) -> List[str]:
        """List all available skills."""
        pass

    @abstractmethod
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of available agents."""
        pass


class PlaybookEngineInterface(ABC):
    """
    Interface for the Playbook Engine.

    The Playbook Engine is responsible for:
    - Playbook orchestration
    - Stage coordination
    - Dependency management
    - Cost policies
    - Error handling strategies
    """

    @abstractmethod
    async def execute_playbook(self, playbook_path: str) -> PlaybookResult:
        """Execute a playbook from file path."""
        pass

    @abstractmethod
    async def validate_playbook(self, playbook_path: str) -> ValidationResult:
        """Validate a playbook without executing."""
        pass

    @abstractmethod
    async def get_execution_status(self, execution_id: str) -> Optional[ExecutionState]:
        """Get status of a running or completed execution."""
        pass

    @abstractmethod
    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel a running execution."""
        pass

    @abstractmethod
    def list_playbooks(self) -> List[str]:
        """List all available playbooks."""
        pass

    @abstractmethod
    async def check_approval_required(
        self, playbook_path: str, estimated_cost: float
    ) -> bool:
        """Check if playbook execution requires approval based on cost."""
        pass


# Forward references for type hints
@dataclass
class SkillResult:
    skill_name: str
    status: ExecutionStatus
    outputs: Dict[str, Any]
    cost_incurred: float
    execution_time_ms: float
    errors: List[str]
    execution_id: str


@dataclass
class StageResult:
    stage_name: str
    status: ExecutionStatus
    skills_results: List[SkillResult]
    total_cost: float
    execution_time_ms: float
    error_message: Optional[str]


@dataclass
class PlaybookResult:
    playbook_name: str
    status: ExecutionStatus
    stages_results: List[StageResult]
    total_cost: float
    total_execution_time_ms: float
    execution_id: str
    timestamp: datetime


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    estimated_cost: Optional[float]


@dataclass
class ExecutionState:
    execution_id: str
    status: ExecutionStatus
    current_stage: Optional[str]
    completed_stages: List[str]
    failed_stages: List[str]
    progress_percentage: float
    estimated_remaining_time_ms: Optional[float]
