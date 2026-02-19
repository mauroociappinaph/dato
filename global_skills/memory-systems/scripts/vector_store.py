#!/usr/bin/env python3
"""
Memory Systems - Vector Store
Handles semantic search and vector embeddings indexing.
Now with NVIDIA NIM support for high-quality embeddings.
"""

import os
import sys
import numpy as np
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add path for NVIDIA NIM client
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", "ai-engineer", "scripts"))

try:
    from nvidia_nim_client import NVIDIANIMClient
    NIM_AVAILABLE = True
except ImportError:
    NIM_AVAILABLE = False

class VectorStore:
    """Surgical vector storage with metadata indexing"""

    def __init__(self, dimension: int = 768):
        self.dimension = dimension
        self.vectors: List[np.ndarray] = []
        self.metadata: List[Dict] = []
        self.entity_index: Dict[str, List[int]] = {}
        self.time_index: Dict[str, List[int]] = {}

    def add(self, text: str, metadata: Dict[str, Any] = None) -> int:
        """Add document to store with multi-index support"""
        embedding = self._embed(text)
        index = len(self.vectors)
        self.vectors.append(embedding)
        self.metadata.append(metadata or {})

        if metadata:
            if "entity" in metadata:
                entity = metadata["entity"]
                if entity not in self.entity_index: self.entity_index[entity] = []
                self.entity_index[entity].append(index)

            if "valid_from" in metadata:
                t_key = self._time_key(metadata["valid_from"])
                if t_key not in self.time_index: self.time_index[t_key] = []
                self.time_index[t_key].append(index)
        return index

    def search(self, query: str, limit: int = 5, filters: Dict = None) -> List[Dict]:
        """Hybrid search with metadata filtering"""
        q_emb = self._embed(query)
        scores = []
        for i, vec in enumerate(self.vectors):
            score = np.dot(q_emb, vec) / (np.linalg.norm(q_emb) * np.linalg.norm(vec) + 1e-8)
            if filters and not self._matches_filters(self.metadata[i], filters): score = -1
            scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        return [{"score": s, "text": self.metadata[idx].get("text", ""), "metadata": self.metadata[idx]}
                for idx, s in scores[:limit] if s > 0]

    def _embed(self, text: str) -> np.ndarray:
        """Generate embeddings using NVIDIA NIM (preferred) or Ollama (fallback)"""

        # Try NVIDIA NIM first for high-quality embeddings
        if NIM_AVAILABLE:
            try:
                nim_client = NVIDIANIMClient()
                if nim_client.is_available():
                    vector = nim_client.generate_embedding(text)
                    vec_array = np.array(vector)
                    if len(vec_array) != self.dimension:
                        return np.resize(vec_array, self.dimension)
                    return vec_array
            except Exception as e:
                print(f"⚠️  NVIDIA NIM embedding failed: {e}. Falling back to Ollama...")

        # Fallback to Ollama
        try:
            import requests
            response = requests.post('http://127.0.0.1:11434/api/embeddings', json={
                "model": "nomic-embed-text",
                "prompt": text
            }, timeout=30)
            if response.status_code == 200:
                vector = response.json().get('embedding')
                vec_array = np.array(vector)
                if len(vec_array) != self.dimension:
                    return np.resize(vec_array, self.dimension)
                return vec_array
            else:
                print(f"⚠️  Ollama Error: {response.text}")
                return np.random.randn(self.dimension)
        except Exception as e:
            print(f"⚠️  Embedding failed, using random: {e}")
            return np.random.randn(self.dimension)

    def _time_key(self, timestamp: Any) -> str:
        return timestamp.strftime("%Y-%m") if isinstance(timestamp, datetime) else str(timestamp)

    def _matches_filters(self, metadata: Dict, filters: Dict) -> bool:
        for k, v in filters.items():
            if k not in metadata or (isinstance(v, list) and metadata[k] not in v) or (not isinstance(v, list) and metadata[k] != v):
                return False
        return True
