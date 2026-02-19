#!/usr/bin/env python3
"""
Cost Monitor - Sistema de monitoreo de costos para The Dude

Módulo para tracking de costos de ejecución de skills con:
- Tracking de tokens por skill
- Dashboard de costos acumulados
- Alertas de presupuesto
"""

__version__ = "1.0.0"
__author__ = "The Dude AI"

from .core.cost_tracker import CostTracker
from .core.alert_manager import AlertManager, AlertType
from .config import calculate_cost, get_tier_for_skill

__all__ = [
    "CostTracker",
    "AlertManager",
    "AlertType",
    "calculate_cost",
    "get_tier_for_skill",
]
