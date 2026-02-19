#!/usr/bin/env python3
"""
Visual Learning Engine - Type Definitions
Standardized data structures for visual patterns and analysis results.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any, Optional

@dataclass
class VisualPattern:
    """Represents a learned visual pattern"""
    pattern_id: str
    category: str  # 'ui_pattern', 'workflow', 'architecture', 'design_principle'
    description: str
    confidence_score: float
    source_url: str
    extracted_features: Dict[str, Any]
    learned_at: datetime
    applied_count: int = 0

@dataclass
class VisualAnalysis:
    """Result of visual content analysis"""
    content_type: str  # 'screenshot', 'video_frame', 'diagram'
    patterns_found: List[VisualPattern]
    insights: List[str]
    recommendations: List[str]
    confidence_score: float
