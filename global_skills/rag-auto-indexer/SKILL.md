---
name: rag-auto-indexer
description: Escaneo y sincronización automática de conocimiento neural (.agent-os, .aitk, .mem0).
version: 1.0.0
---

# Rag Auto-Indexer

## Purpose
Mantener la coherencia entre los archivos físicos de conocimiento y la memoria operativa del AGENT_RAG.

## Workflow
1. Escanear rutas definidas en `resources/index_config.json`.
2. Identificar archivos nuevos o modificados (basado en mtime).
3. Actualizar `knowledge_map.md` en el AGENT_RAG.
4. (Opcional) Sincronizar con Redis o Pinecone.

## Dependencies
- `find`, `grep`, `cat` (Shell tools)
- `AGENT_RAG` (Owner)
