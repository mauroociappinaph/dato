"""
Base Skill class - Abstract base for all Global Skills.

Provides the foundation for skill implementation with standardized
input/output handling, cost tracking, and execution patterns.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Callable
import uuid


class SkillStatus(Enum):
    """Execution status for skills."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


@dataclass
class SkillResult:
    """Standardized result container for skill execution."""
    skill_name: str
    status: SkillStatus
    outputs: Dict[str, Any] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    cost_incurred: float = 0.0
    execution_time_ms: float = 0.0
    tokens_used: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    execution_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def is_success(self) -> bool:
        """Check if execution was successful."""
        return self.status == SkillStatus.COMPLETED and not self.errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "skill_name": self.skill_name,
            "status": self.status.value,
            "outputs": self.outputs,
            "errors": self.errors,
            "cost_incurred": self.cost_incurred,
            "execution_time_ms": self.execution_time_ms,
            "tokens_used": self.tokens_used,
            "timestamp": self.timestamp.isoformat(),
            "execution_id": self.execution_id,
            "metadata": self.metadata,
        }


@dataclass
class SkillConfig:
    """Configuration for skill execution."""
    timeout_seconds: int = 30
    max_retries: int = 3
    retry_delay_seconds: float = 1.0
    cost_limit: Optional[float] = None
    enable_caching: bool = False
    cache_ttl_seconds: int = 300
    log_level: str = "INFO"


class SkillBase(ABC):
    """
    Abstract base class for all Global Skills.

    All skills must inherit from this class and implement the abstract methods.
    Provides standardized patterns for execution, error handling, and cost tracking.
    """

    def __init__(self, config: Optional[SkillConfig] = None):
        """Initialize the skill with optional configuration."""
        self.config = config or SkillConfig()
        self._execution_history: List[SkillResult] = []
        self._cache: Dict[str, Any] = {}

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the unique name of the skill."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Return a description of what the skill does."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Return the version of the skill (semver format)."""
        pass

    @property
    def input_schema(self) -> Dict[str, Any]:
        """
        Return the JSON schema for expected inputs.
        Override to define input validation schema.
        """
        return {"type": "object", "properties": {}}

    @property
    def output_schema(self) -> Dict[str, Any]:
        """
        Return the JSON schema for expected outputs.
        Override to define output validation schema.
        """
        return {"type": "object", "properties": {}}

    @property
    def estimated_cost_per_execution(self) -> float:
        """Return estimated cost in USD per execution."""
        return 0.0

    @property
    def preferred_model_tier(self) -> str:
        """Return preferred model tier (low, medium, high, ultra)."""
        return "medium"

    @abstractmethod
    async def execute(self, inputs: Dict[str, Any]) -> SkillResult:
        """
        Execute the skill with the given inputs.

        Args:
            inputs: Dictionary containing input parameters

        Returns:
            SkillResult containing execution results
        """
        pass

    async def validate_inputs(self, inputs: Dict[str, Any]) -> List[str]:
        """
        Validate input parameters.

        Args:
            inputs: Dictionary containing input parameters

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        # Basic validation - check required fields
        required = self.input_schema.get("required", [])
        for field in required:
            if field not in inputs:
                errors.append(f"Missing required field: {field}")
        return errors

    async def run(
        self, inputs: Dict[str, Any], context: Optional[Dict[str, Any]] = None
    ) -> SkillResult:
        """
        Run the skill with full lifecycle management.

        This method handles:
        - Input validation
        - Cost checking
        - Execution with retries
        - Result caching
        - History tracking

        Args:
            inputs: Input parameters
            context: Optional execution context

        Returns:
            SkillResult from execution
        """
        import asyncio
        import time

        start_time = time.time()
        execution_id = str(uuid.uuid4())

        # Check cache if enabled
        if self.config.enable_caching:
            cache_key = self._generate_cache_key(inputs)
            if cache_key in self._cache:
                return self._cache[cache_key]

        # Validate inputs
        validation_errors = await self.validate_inputs(inputs)
        if validation_errors:
            result = SkillResult(
                skill_name=self.name,
                status=SkillStatus.FAILED,
                errors=validation_errors,
                execution_id=execution_id,
            )
            self._execution_history.append(result)
            return result

        # Execute with retries
        last_error = None
        for attempt in range(self.config.max_retries):
            try:
                result = await self.execute(inputs)
                result.execution_id = execution_id
                result.execution_time_ms = (time.time() - start_time) * 1000

                # Cache result if successful and caching enabled
                if result.is_success() and self.config.enable_caching:
                    cache_key = self._generate_cache_key(inputs)
                    self._cache[cache_key] = result

                self._execution_history.append(result)
                return result

            except Exception as e:
                last_error = str(e)
                if attempt < self.config.max_retries - 1:
                    await asyncio.sleep(self.config.retry_delay_seconds * (2 ** attempt))

        # All retries failed
        result = SkillResult(
            skill_name=self.name,
            status=SkillStatus.FAILED,
            errors=[f"Execution failed after {self.config.max_retries} attempts: {last_error}"],
            execution_id=execution_id,
            execution_time_ms=(time.time() - start_time) * 1000,
        )
        self._execution_history.append(result)
        return result

    def _generate_cache_key(self, inputs: Dict[str, Any]) -> str:
        """Generate a cache key from inputs."""
        import hashlib
        import json

        # Create deterministic key from sorted inputs
        key_data = json.dumps(inputs, sort_keys=True, default=str)
        return hashlib.sha256(key_data.encode()).hexdigest()

    def get_execution_history(self) -> List[SkillResult]:
        """Get the execution history for this skill."""
        return self._execution_history.copy()

    def get_statistics(self) -> Dict[str, Any]:
        """Get execution statistics for this skill."""
        if not self._execution_history:
            return {"total_executions": 0}

        total = len(self._execution_history)
        successful = sum(1 for r in self._execution_history if r.is_success())
        failed = total - successful
        total_cost = sum(r.cost_incurred for r in self._execution_history)
        avg_time = sum(r.execution_time_ms for r in self._execution_history) / total

        return {
            "total_executions": total,
            "successful": successful,
            "failed": failed,
            "success_rate": successful / total if total > 0 else 0,
            "total_cost": total_cost,
            "average_execution_time_ms": avg_time,
        }

    def clear_cache(self) -> None:
        """Clear the execution cache."""
        self._cache.clear()

    def clear_history(self) -> None:
        """Clear the execution history."""
        self._execution_history.clear()
