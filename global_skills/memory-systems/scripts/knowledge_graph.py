#!/usr/bin/env python3
"""
Memory Systems - Knowledge Graph
Manages entity relationships and temporal fact consistency.
"""

import hashlib
import time
from datetime import datetime
from typing import Dict, List, Any, Optional

class PropertyGraph:
    """Core property graph storage engine"""
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}
        self.edges: Dict[str, Dict] = {}
        self.node_index: Dict[str, List[str]] = {}
        self.edge_index: Dict[str, List[str]] = {}

    def create_node(self, label: str, properties: Dict = None) -> str:
        node_id = hashlib.md5(f"{label}{time.time()}".encode()).hexdigest()[:16]
        self.nodes[node_id] = {"id": node_id, "label": label, "properties": properties or {}, "created_at": time.time()}
        if label not in self.node_index: self.node_index[label] = []
        self.node_index[label].append(node_id)
        return node_id

    def create_relationship(self, source_id: str, rel_type: str, target_id: str, properties: Dict = None) -> str:
        edge_id = hashlib.md5(f"{source_id}{rel_type}{target_id}{time.time()}".encode()).hexdigest()[:16]
        self.edges[edge_id] = {"id": edge_id, "source": source_id, "target": target_id, "type": rel_type, "properties": properties or {}}
        if rel_type not in self.edge_index: self.edge_index[rel_type] = []
        self.edge_index[rel_type].append(edge_id)
        return edge_id

class TemporalKnowledgeGraph(PropertyGraph):
    """Advanced graph with fact validity tracking"""
    def create_temporal_relationship(self, source_id: str, rel_type: str, target_id: str, valid_from: datetime, valid_until: datetime = None) -> str:
        edge_id = super().create_relationship(source_id, rel_type, target_id)
        self.edges[edge_id].update({"valid_from": valid_from.isoformat(), "valid_until": valid_until.isoformat() if valid_until else None})
        return edge_id

    def get_relationships(self, node_id: str) -> List[Dict]:
        return [{"edge": e, "target": self.nodes.get(e["target"])} for e in self.edges.values() if e["source"] == node_id]
