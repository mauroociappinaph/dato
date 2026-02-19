#!/usr/bin/env python3
"""
Visual Learning Engine - Core Orchestrator (v7.0)
Lightweight facade that coordinates visual analysis, neural optimization, and acquisition.
"""

import json
import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

# Ensure local imports work regardless of execution context
sys.path.append(os.path.dirname(__file__))

from visual_types import VisualPattern, VisualAnalysis
from adaptive_context_gating import AdaptiveContextEngine
from learning_service import LearningService

# MCP Server imports
try:
    from mcp_server_gemini_vision import GeminiVisionClient
    from mcp_server_firecrawl import FirecrawlClient
    from mcp_server_pinecone import PineconeClient
    from mcp_server_redis import RedisClient
except ImportError:
    GeminiVisionClient = FirecrawlClient = PineconeClient = RedisClient = None

class VisualProcessor:
    """Orchestrates visual learning through specialized engines"""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.vision_client = GeminiVisionClient() if GeminiVisionClient else None
        self.vector_client = PineconeClient() if PineconeClient else None
        
        # Sub-engines
        self.neural = AdaptiveContextEngine()
        self.learning = LearningService(
            vision_client=self.vision_client, 
            firecrawl_client=FirecrawlClient() if FirecrawlClient else None
        )

    async def analyze_screenshot(self, image_url: str, context: str) -> VisualAnalysis:
        """Extract UI/UX patterns and insights from a screenshot"""
        if not self.vision_client:
            return VisualAnalysis('screenshot', [], ['Vision client unavailable'], [], 0.0)

        try:
            prompt = f"Analyze this screenshot in context of: {context}. Extract: patterns, principles, improvements."
            result = await self.vision_client.analyze_image(image_url, prompt)
            data = json.loads(result)

            patterns = [VisualPattern(
                pattern_id=f"ui_{hash(image_url)}_{i}",
                category='ui_pattern',
                description=p.get('description', ''),
                confidence_score=p.get('confidence', 0.8),
                source_url=image_url,
                extracted_features=p.get('features', {}),
                learned_at=datetime.now()
            ) for i, p in enumerate(data.get('patterns', []))]

            return VisualAnalysis('screenshot', patterns, data.get('insights', []), data.get('recommendations', []), data.get('confidence', 0.8))
        except Exception as e:
            self.logger.error(f"Analysis failed: {e}")
            return VisualAnalysis('screenshot', [], [str(e)], [], 0.0)

    async def search_visual_content(self, query: str, types: List[str] = None) -> List[str]:
        """Delegate search to learning service"""
        return await self.learning.search_content(query, types)

    async def learn_from_video(self, video_url: str, context: str) -> List[VisualPattern]:
        """Delegate video learning to service"""
        return await self.learning.learn_from_video(video_url, context, self.analyze_screenshot)

    async def store_visual_pattern(self, pattern: VisualPattern) -> bool:
        """Store pattern with neural compression and memory sync"""
        if not self.vector_client: return False
        try:
            compressed = await self.neural.compress_pattern(pattern)
            await self.neural.update_lstm_memory(pattern.category, compressed)
            
            # Simple mock embedding
            embedding = [0.1] * 1024
            metadata = {
                'category': pattern.category,
                'learned_at': pattern.learned_at.isoformat(),
                'compression_ratio': compressed.get('compression_ratio', 1.0)
            }

            await self.vector_client.upsert_records(
                name='dude-central-brain',
                namespace='visual-patterns',
                records=[{'id': pattern.pattern_id, 'values': embedding, 'metadata': metadata}]
            )
            return True
        except Exception as e:
            self.logger.error(f"Storage failed: {e}")
            return False

    async def retrieve_similar_patterns(self, query: str, category: str = None, limit: int = 5) -> List[VisualPattern]:
        """Retrieve patterns from Pinecone"""
        if not self.vector_client: return []
        try:
            filter_dict = {'category': category} if category else {}
            results = await self.vector_client.search_records(
                name='dude-central-brain',
                namespace='visual-patterns',
                query={'topK': limit, 'inputs': {'text': query}, 'filter': filter_dict}
            )
            return [VisualPattern(r['id'], r['metadata'].get('category', 'unknown'), '', 0.8, '', {}, datetime.now()) for r in results.get('matches', [])]
        except Exception as e:
            self.logger.error(f"Retrieval failed: {e}")
            return []

# Singleton instance
visual_processor = VisualProcessor()
