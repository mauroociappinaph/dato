"""
master-rag-2026 scripts package.
Solution-RAG: Index documents and query semantically via Redis Vectors + Ollama.
"""
from .indexer import index_directory
from .query import semantic_query

__all__ = ["index_directory", "semantic_query"]
