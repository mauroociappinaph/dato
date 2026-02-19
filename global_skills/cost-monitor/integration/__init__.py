#!/usr/bin/env python3
"""
Cost Monitor Integration - Integración con Skill Engine

Este módulo proporciona integración transparente entre el sistema de
monitoreo de costos y el Skill Engine.

Usage:
    from cost_monitor.integration import MonitoredSkillEngineAdapter

    adapter = MonitoredSkillEngineAdapter(skill_engine)
    result = await adapter.execute_skill(request)  # Tracking automático
"""

from .model_mapper import SkillModelMapper, get_model_for_skill
from .token_tracker import NIMTokenTracker, TokenUsage
from .monitored_adapter import MonitoredSkillEngineAdapter

__all__ = [
    'SkillModelMapper',
    'get_model_for_skill',
    'NIMTokenTracker',
    'TokenUsage',
    'MonitoredSkillEngineAdapter',
]
