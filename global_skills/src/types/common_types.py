"""
Common type definitions for Global Skills.

Data classes and type definitions shared across the system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum


class ModelTier(Enum):
    """Model tier for cost/quality optimization."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"


@dataclass
class SkillMetadata:
    """Metadata for a Global Skill."""
    name: str
    description: str
    version: str = "1.0.0"
    author: Optional[str] = None
    cluster: str = "DEVELOPMENT"
    status: str = "active"
    tags: List[str] = field(default_factory=list)
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    preferred_agent: str = "AGENT_ORCHESTRATOR"
    estimated_cost: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "author": self.author,
            "cluster": self.cluster,
            "status": self.status,
            "tags": self.tags,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "preferred_agent": self.preferred_agent,
            "estimated_cost": self.estimated_cost,
        }


@dataclass
class ExecutionContext:
    """Context for skill execution."""
    execution_id: str
    playbook_id: Optional[str] = None
    stage_id: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "execution_id": self.execution_id,
            "playbook_id": self.playbook_id,
            "stage_id": self.stage_id,
            "user_id": self.user_id,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


@dataclass
class CostBreakdown:
    """Detailed cost breakdown for execution."""
    skill_name: str
    model_name: str
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    total_cost: float = 0.0

    def calculate(self) -> float:
        """Calculate total cost from tokens and rates."""
        input_cost = (self.input_tokens / 1000) * self.cost_per_1k_input
        output_cost = (self.output_tokens / 1000) * self.cost_per_1k_output
        self.total_cost = input_cost + output_cost
        self.total_tokens = self.input_tokens + self.output_tokens
        return self.total_cost

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "skill_name": self.skill_name,
            "model_name": self.model_name,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "cost_per_1k_input": self.cost_per_1k_input,
            "cost_per_1k_output": self.cost_per_1k_output,
            "total_cost": self.total_cost,
        }


@dataclass
class ModelConfig:
    """Configuration for AI model usage."""
    name: str
    tier: ModelTier = ModelTier.MEDIUM
    provider: str = "nvidia"
    cost_per_1k_input: float = 0.0
    cost_per_1k_output: float = 0.0
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: int = 30

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for given token usage."""
        input_cost = (input_tokens / 1000) * self.cost_per_1k_input
        output_cost = (output_tokens / 1000) * self.cost_per_1k_output
        return input_cost + output_cost

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "tier": self.tier.value,
            "provider": self.provider,
            "cost_per_1k_input": self.cost_per_1k_input,
            "cost_per_1k_output": self.cost_per_1k_output,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "timeout": self.timeout,
        }


@dataclass
class AgentConfig:
    """Configuration for agent assignment."""
    agent_id: str
    agent_type: str
    capabilities: List[str] = field(default_factory=list)
    max_concurrent_tasks: int = 5
    priority: int = 1
    enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type,
            "capabilities": self.capabilities,
            "max_concurrent_tasks": self.max_concurrent_tasks,
            "priority": self.priority,
            "enabled": self.enabled,
        }


@dataclass
class PlaybookConfig:
    """Configuration for playbook execution."""
    name: str
    version: str = "1.0.0"
    cost_limit: Optional[float] = None
    approval_threshold: Optional[float] = None
    timeout_per_stage: int = 300
    max_retries: int = 3
    parallel_execution: bool = False
    notification_channels: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "cost_limit": self.cost_limit,
            "approval_threshold": self.approval_threshold,
            "timeout_per_stage": self.timeout_per_stage,
            "max_retries": self.max_retries,
            "parallel_execution": self.parallel_execution,
            "notification_channels": self.notification_channels,
        }
