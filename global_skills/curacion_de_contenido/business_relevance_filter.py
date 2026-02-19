#!/usr/bin/env python3
"""
Business Relevance Filter (v7.0)
Decoupled logic for evaluating content against the dynamic corporate profile.
"""

import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class RelevanceScore:
    """Business relevance scoring metrics"""
    overall_score: float  # 0-40 points
    strategic_alignment: int
    technical_applicability: int
    business_value: int
    urgency_importance: int
    reasoning: List[str]
    recommended_action: str  # 'learn', 'monitor', 'ignore'

class BusinessRelevanceFilter:
    """Scoring engine based on the external business profile"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.profile_path = Path(__file__).parent / "resources" / "business_profile.json"
        self.profile = self._load_profile()
        self.approval_threshold = 25
        self.monitor_threshold = 15

    def _load_profile(self) -> Dict:
        """Load strategy from JSON resource"""
        try:
            with open(self.profile_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load business profile: {e}")
            return {"strategic_goals": [], "primary_focus": [], "current_projects": []}

    def evaluate_content(self, content: Dict[str, Any], content_type: str = "visual") -> RelevanceScore:
        """Score content based on semantic matching with corporate goals"""
        text = self._extract_text(content, content_type)
        
        strategic = self._score_list(text, self.profile.get('strategic_goals', []), weight=2)
        technical = self._score_list(text, self.profile.get('primary_focus', []), weight=2)
        business = 10 if 'tutorial' in text or 'guide' in text else 5
        urgency = 10 if '2026' in text or 'latest' in text else 5

        total = min(strategic + technical + business + urgency, 40)
        action = "learn" if total >= self.approval_threshold else "monitor" if total >= self.monitor_threshold else "ignore"

        return RelevanceScore(
            overall_score=total,
            strategic_alignment=strategic,
            technical_applicability=technical,
            business_value=business,
            urgency_importance=urgency,
            reasoning=[f"Acción determinada: {action}"],
            recommended_action=action
        )

    def _extract_text(self, content: Dict, ctype: str) -> str:
        """Normalize content text for analysis"""
        fields = ['description', 'insights', 'title', 'content', 'summary']
        return ' '.join(str(content.get(f, '')) for f in fields if content.get(f)).lower()

    def _score_list(self, text: str, target_list: List[str], weight: int) -> int:
        """Simple keyword matching score"""
        score = 0
        for item in target_list:
            if any(word in text for word in item.lower().split()):
                score += weight
        return min(score, 10)

# Singleton instance
business_filter = BusinessRelevanceFilter()