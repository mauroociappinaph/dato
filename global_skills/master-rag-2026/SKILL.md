---
name: master-rag-2026
description: Conecta a los agentes de la empresa con el motor de IA Soberana de grado industrial.
inherited_from: [ai-engineer]
---

# Skill: Master RAG 2026 (El Motor de la Empresa)

## Propósito
Permitir que cualquier agente de la empresa acceda al conocimiento almacenado en documentos locales mediante búsqueda semántica vectorial.

## Stack Soberano
- **Embeddings:** Ollama `nomic-embed-text` (local, $0)
- **Vector Store:** Redis 8 VectorSet (`VADD`/`VSIM`)
- **Cache:** Redis con TTL 24h por query

## Requisitos
- Ollama corriendo con `nomic-embed-text` (`ollama pull nomic-embed-text`)
- Redis 8+ corriendo (`redis-server`)
- `pip install requests redis`

## Uso CLI

```bash
cd global_skills/master-rag-2026/scripts

# Indexar documentos de un directorio
python main.py index /path/to/docs
python main.py index /path/to/docs --extensions md txt
python main.py index /path/to/docs --dry-run

# Buscar semánticamente
python main.py query "propuesta de valor"
python main.py query "lead generation" --top-k 5

# Ver estadísticas del índice
python main.py stats
```

## Output Format (JSON)
```json
{"results": [{"text": "...", "source": "file.md", "score": 0.92}], "from_cache": false}
```

## Protocolo de Uso
- El agente debe verificar si existe cache semántico antes de gastar tokens.
- Toda respuesta debe pasar por el evaluator externo para certificar veracidad.

---
*Esta skill integra el activo de producto con el activo operativo.*
