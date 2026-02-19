"""
Global Skills Package - Root barrel file.

This package contains all Global Skills for THE DUDE.
Auto-generated barrel file.
"""

# Import core components
from src.core import (
    SkillBase,
    SkillResult,
    SkillStatus,
    SkillEngineInterface,
    PlaybookEngineInterface,
)

# Package metadata
__version__ = "2.0.0"
__author__ = "THE DUDE Team"

# Expose core classes
__all__ = [
    "SkillBase",
    "SkillResult",
    "SkillStatus",
    "SkillEngineInterface",
    "PlaybookEngineInterface",
]
