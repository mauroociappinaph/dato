"""
Visual Learning Engine Cluster (v7.0)
Public API for the visual learning and pattern recognition department.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from visual_processor import visual_processor
from demo_analyzer import demo_analyzer
from visual_types import VisualPattern, VisualAnalysis

__all__ = [
    'visual_processor',
    'demo_analyzer',
    'VisualPattern',
    'VisualAnalysis'
]