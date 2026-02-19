# RAG Avanzado (Retrieval-Augmented Generation)

Arquitecturas de producción para sistemas de generación aumentada por recuperación de alto rendimiento.

## El Pipeline RAG de 5 Etapas
1. **Comprensión de la Consulta**: Expansión, re-escritura y descomposición de la duda del usuario.
2. **Pre-Recuperación**: Filtrado de metadatos y enrutamiento hacia el "data store" adecuado.
3. **Recuperación (Retrieval)**: Búsqueda híbrida (Vector + Keyword) y RAG-Fusion.
4. **Post-Recuperación**: Reranking y compresión de contexto para optimizar la ventana del LLM.
5. **Generación**: Síntesis de respuesta con citas y verificación de auto-corrección.

## Técnicas de Optimización
### RAG-Fusion
Genera múltiples variaciones de la consulta original, realiza búsquedas paralelas y combina los resultados usando Reciprocal Rank Fusion (RRF).

### HyDE (Hypothetical Document Embeddings)
El LLM genera una respuesta hipotética a la consulta del usuario. Esa respuesta (que captura mejor el "espacio semántico" de la solución) se usa para buscar en la base de datos vectorial.

### Reranking (Cross-Encoders)
Uso de modelos especializados (Cohere Rerank, BGE Reranker) para re-evaluar la relevancia de los top-K documentos recuperados. Es la técnica con mayor ROI en la precisión de RAG.

### GraphRAG
Integración de grafos de conocimiento para responder preguntas que requieren conectar múltiples entidades o conceptos que no están necesariamente en el mismo fragmento de texto.

## Manejo de Alucinaciones
- **Verificación Basada en Citaciones**: Obligar al modelo a citar fragmentos específicos `[Fuente 1]`.
- **NLI (Natural Language Inference)**: Usar un segundo modelo para verificar si la respuesta está soportada lógicamente por el contexto.
- **Auto-RAG**: El sistema decide recursivamente si necesita recuperar más información antes de dar la respuesta final.

## Evaluación de RAG (RAGAS / TruLens)
Debes medir las "3 Fidelidades":
1. **Fidelidad (Faithfulness)**: ¿La respuesta se deriva solo del contexto?
2. **Relevancia del Contexto**: ¿Los fragmentos recuperados son útiles para responder?
3. **Relevancia de la Respuesta**: ¿La respuesta responde directamente a la duda del usuario?

## Ejemplo de Pipeline Modular
```python
async def advanced_rag_pipeline(query: str):
    # 1. Expandir consulta
    queries = await rewrite_query(query)

    # 2. Recuperación híbrida paralela
    docs = await hybrid_search(queries)

    # 3. Rerank para calidad superior
    ranked_docs = await rerank_documents(query, docs)

    # 4. Generación con citaciones
    response = await generate_with_citations(query, ranked_docs)

    return response
```
