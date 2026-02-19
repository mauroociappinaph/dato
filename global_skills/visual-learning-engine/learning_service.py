#!/usr/bin/env python3
"""
Visual Learning Engine - Learning Service
Handles content discovery, video analysis, and business relevance evaluation.
"""

import asyncio
import logging
import sys
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

# Ensure local imports work
sys.path.append(os.path.dirname(__file__))
from visual_types import VisualPattern, VisualAnalysis

# Import business relevance filter
try:
    from curacion_de_contenido.business_relevance_filter import business_filter
except ImportError:
    business_filter = None

class LearningService:
    """Service for discovering and learning from external visual content"""

    def __init__(self, vision_client=None, firecrawl_client=None):
        self.logger = logging.getLogger(__name__)
        self.vision_client = vision_client
        self.firecrawl_client = firecrawl_client

    async def search_content(self, query: str, content_types: List[str] = None) -> List[str]:
        """Search for relevant visual content using Exa and Firecrawl"""
        if not content_types:
            content_types = ['screenshot', 'tutorial', 'diagram']
        
        visual_urls = []
        try:
            from mcp_server_exa import ExaClient
            exa_client = ExaClient()
            for content_type in content_types:
                search_query = f"{query} {content_type} example"
                results = await exa_client.web_search_exa(search_query, numResults=5)
                for result in results:
                    if self._is_visual_content(result.get('url', ''), content_type):
                        visual_urls.append(result['url'])
        except ImportError:
            self.logger.warning("Exa client not available for search")

        if self.firecrawl_client:
            for url in visual_urls[:3]:
                try:
                    await self.firecrawl_client.firecrawl_scrape(url=url, formats=['screenshot'])
                except Exception as e:
                    self.logger.warning(f"Firecrawl capture failed for {url}: {e}")

        return visual_urls[:10]

    async def learn_from_video(self, video_url: str, task_context: str, analyzer_fn) -> List[VisualPattern]:
        """Extract patterns from video content by analyzing key frames"""
        patterns = []
        try:
            video_content = {'title': f'Video from {video_url}', 'description': task_context, 'url': video_url, 'type': 'tutorial_video'}
            
            relevance_score = await self.evaluate_relevance(video_content)
            if relevance_score and getattr(relevance_score, 'recommended_action', '') != 'learn':
                self.logger.info(f"Video {video_url} not relevant")
                return []

            key_frames = await self._extract_video_frames(video_url)
            for i, frame_url in enumerate(key_frames):
                analysis = await analyzer_fn(frame_url, task_context)
                if analysis.patterns_found:
                    for p in analysis.patterns_found:
                        patterns.append(p)
        except Exception as e:
            self.logger.error(f"Video learning failed: {e}")
        return patterns

    async def evaluate_relevance(self, content: Dict[str, Any]) -> Any:
        """Evaluate business relevance of content before learning"""
        if not business_filter:
            return None
        try:
            return business_filter.evaluate_content(content, content_type="video")
        except Exception as e:
            self.logger.warning(f"Relevance evaluation failed: {e}")
            return None

    def _is_visual_content(self, url: str, content_type: str) -> bool:
        indicators = {
            'screenshot': ['screenshot', 'demo', 'example', 'ui', 'interface'],
            'tutorial': ['tutorial', 'guide', 'how-to', 'step-by-step'],
            'diagram': ['diagram', 'architecture', 'flow', 'schema']
        }
        return any(ind in url.lower() for ind in indicators.get(content_type, []))

    async def _extract_video_frames(self, video_url: str) -> List[str]:
        """Mock frame extraction logic"""
        return []