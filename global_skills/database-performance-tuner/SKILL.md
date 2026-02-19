---
name: database-performance-tuner
description: Especialista en optimización de bases de datos, diseño de esquemas y eficiencia de consultas. Domina SQL (Postgres) y NoSQL (Mongo/Redis) para garantizar latencia sub-milisegundo.
---

# Database Performance Tuner: El Mecánico de F1

> [!IMPORTANT]
> **Trigger**: Activar ante reportes de lentitud, antes de lanzar una feature con alta carga de datos, o durante el diseño de esquemas.

## Protocolos de Optimización

### 0. Consulta de Memoria Técnica
- **Acción**: Consultar el **Central Vector Memory (dude-central-brain)** para recuperar estrategias de indexación y particionamiento que hayan sido exitosas en stacks tecnológicos similares dentro del ecosistema de Mauro.

### 1. La Ley del Índice (Indexing Strategy)
- **Análisis**: Uso de `EXPLAIN ANALYZE` para verificar que las consultas usan índices.
- **Regla**: Toda columna usada en `WHERE`, `JOIN` o `ORDER BY` es candidata a índice.
- **Cuidado**: No sobre-indexar (ralentiza los `INSERT`/`UPDATE`).

### 2. Prevención de N+1
- **Síntoma**: El ORM hace 1 query para obtener la lista y N queries para obtener los detalles de cada ítem.
- **Solución**: Uso estricto de `.include()` (Prisma/Sequelize) o `$lookup` (Mongo) para traer todo en una sola vuelta (Eager Loading).

### 3. Diseño de Esquemas Escalables
- **Normalización vs Desnormalización**: Saber cuándo duplicar datos para evitar JOINs costosos en lecturas masivas (CQRS pattern).
- **Tipos de Datos**: Usar el tipo más pequeño posible (`VARCHAR(50)` vs `TEXT`, `INT` vs `BIGINT`) para optimizar almacenamiento y memoria RAM.

### 4. Caché Estratégico (Redis)
- Identificar datos de lectura frecuente y baja mutabilidad para cachear en Redis y aliviar la base de datos principal.

## Recursos
- [Query Optimization](resources/query-optimization.md)
- [Indexing Guide](resources/indexing.md)