#!/usr/bin/env python3
"""
Memory Systems - Integrated Orchestrator (v7.0)
Coordinates vector storage and knowledge graphs for agent continuity.
"""

import sys
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

# Ensure local imports work
sys.path.append(os.path.dirname(__file__))

from vector_store import VectorStore
from knowledge_graph import TemporalKnowledgeGraph

class IntegratedMemorySystem:
    """Hybrid memory system: Vector search + Relational graph"""
    
    def __init__(self):
        self.vector_store = VectorStore()
        self.graph = TemporalKnowledgeGraph()
        self.session_id: str = ""
    
    def start_session(self, session_id: str):
        """Initialize context window for current session"""
        self.session_id = session_id
    
    def store_fact(self, fact: str, entity: str, timestamp: datetime = None, relationships: List[Dict] = None):
        """Sync fact across both storage engines"""
        self.vector_store.add(fact, {
            "text": fact, "entity": entity, 
            "valid_from": (timestamp or datetime.now()).isoformat(),
            "session_id": self.session_id
        })
        
        if not self.graph.nodes.get(entity):
            self.graph.create_node("Entity", {"id": entity, "name": entity})
        
        if relationships:
            for rel in relationships:
                self.graph.create_relationship(entity, rel["type"], rel["target"], rel.get("properties", {}))
    
    def retrieve_memories(self, query: str, entity_filter: str = None, limit: int = 5) -> List[Dict]:
        """Retrieve enriched context with vector and graph data"""
        filters = {"session_id": self.session_id}
        if entity_filter: filters["entity"] = entity_filter
        
        results = self.vector_store.search(query, limit=limit, filters=filters)
        for r in results:
            ent = r["metadata"].get("entity")
            if ent: r["relationships"] = self.graph.get_relationships(ent)
        return results

    def consolidate(self):
        """Autonomous memory optimization protocol"""
        pass
