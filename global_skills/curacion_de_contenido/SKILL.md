---
name: curacion-de-contenido
description: Proceso de filtrado, verificación y encaje estratégico de información externa para la evolución de la memoria maestra.
---

# 🛠️ Skill: Curación de Contenido (Fase 5.22)

## Objetivo
Asegurar que solo información veraz, relevante y tácticamente útil sea integrada en el "Cerebro Corporativo" (Success Vault), evitando el ruido y las alucinaciones de datos externos.

## Protocolo de Ejecución (Mandatorio)

1.  **Filtrado de Ruido:** Eliminar hype publicitario, clickbait y opiniones sin sustento técnico. Identificar patrones técnicos reales y accionables.
2.  **Verificación Cruzada:** Utilizar herramientas de búsqueda (Google Search / Exa) para confirmar si la información es una tendencia global consolidada o un caso aislado.
3.  **Análisis de Fit (Encaje):** Comparar la nueva información con la infraestructura y estándares actuales de **DUDE S.A.S.**. ¿Es compatible? ¿Es una mejora sobre lo que ya tenemos?
4.  **Filtro de Relevancia Empresarial (Business Relevance Filter):** Evaluar contenido contra perfil corporativo de DUDE S.A.S. Solo contenido alineado con objetivos estratégicos y proyectos actuales pasa el filtro.
5.  **Cierre de Aprendizaje:** Solo si la información supera los cuatro filtros anteriores, se procede a indexar en el **Success Vault** (Pinecone + Redis) con el estado `verified`.

## Herramientas Relacionadas
- `google_web_search`
- `sequentialthinking`
- `upsert-records` (Pinecone)
- `redis-cli`
