"""
Core module for Global Skills - Base classes and interfaces.

This module provides the foundational abstractions for all Global Skills,
including base classes, interfaces, and core exceptions.
"""

from .base_skill import SkillBase, SkillResult, SkillStatus
from .interfaces import SkillEngineInterface, PlaybookEngineInterface
from .exceptions import (
    SkillError,
    ValidationError,
    ExecutionError,
    CostExceededError,
    SkillNotFoundError,
)
from .barrel_generator import BarrelGenerator

__all__ = [
    # Base classes
    "SkillBase",
    "SkillResult",
    "SkillStatus",
    # Interfaces
    "SkillEngineInterface",
    "PlaybookEngineInterface",
    # Exceptions
    "SkillError",
    "ValidationError",
    "ExecutionError",
    "CostExceededError",
    "SkillNotFoundError",
    # Utilities
    "BarrelGenerator",
]
