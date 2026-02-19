# Bases de Datos Vectoriales y Embeddings

Guía para la implementación de búsqueda semántica y almacenamiento de conocimiento para sistemas de IA.

## Selección de Modelos de Embedding
| Proveedor | Modelo | Dimensiones | Casos de Uso |
|-----------|--------|-------------|--------------|
| **OpenAI** | `text-embedding-3-large` | 3072 | Máxima precisión, soporte Matryoshka. |
| **Voyage AI** | `voyage-3-large` | 1024 | Optimizado para Claude, excelente en código/legal. |
| **Cohere** | `embed-v3` | 1024 | Líder en búsqueda multilingüe y RAG. |
| **HuggingFace** | `bge-large-en-v1.5` | 1024 | SOTA en modelos Open Source. |

## Estrategias de Fragmentación (Chunking)
- **Fragmentación Recursiva**: Divide por párrafos, luego oraciones, luego palabras.
- **Fragmentación Semántica**: Detecta cambios de tema para mantener la cohesión.
- **Ventana Deslizante (Overlap)**: Mantiene contexto compartido entre fragmentos adyacentes (típicamente 10-20%).
- **Estructura del Documento**: Respeta headers, tablas y listas.

## Gestión de Bases de Datos Vectoriales
- **Pinecone**: Serverless, alta escala, ideal para producción rápida.
- **Qdrant / Milvus**: Potentes para búsqueda híbrida y filtrado complejo.
- **pgvector (PostgreSQL)**: La mejor opción si ya usas Postgres y necesitas transaccionalidad.
- **Weaviate**: Enfocado en grafos de conocimiento y búsqueda semántica enriquecida.

## Optimización de Índices
- **HNSW (Hierarchical Navigable Small World)**: El estándar para búsqueda rápida con alta precisión.
- **IVF (Inverted File Index)**: Más eficiente en memoria, útil para escalas masivas.
- **Cuantización (PQ/SQ)**: Reduce drásticamente el uso de memoria a costa de una pequeña pérdida en precisión.

## Búsqueda Híbrida
Combinación de:
1. **Similitud Vectorial**: Captura el significado semántico.
2. **Búsqueda por Palabra Clave (BM25)**: Asegura coincidencias exactas (nombres, códigos, términos técnicos).
- **Fusión (RRF)**: Algoritmo para combinar y re-rankear los resultados de ambos métodos.

## Mejores Prácticas
- **Normalización**: Siempre normaliza tus vectores para usar similitud de coseno.
- **Metadatos**: Indexa metadatos para realizar pre-filtrado rápido (ej: por `user_id`, `category`).
- **Embeddings Drift**: Monitoriza si la distribución de tus inputs cambia drásticamente respecto a tus embeddings indexados.
