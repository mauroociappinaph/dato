# Análisis de Rendimiento y Recursos

## 1. El Trinomio: CPU, Memoria e E/S
- **CPU**:
  - **Context Switching**: Demasiados hilos compitiendo.
  - **CPU Throttling**: El sistema limita el proceso por exceder cuotas (común en K8s).
- **Memoria**:
  - **RSS vs Heap**: Diferencia entre memoria física usada y memoria gestionada por el lenguaje (JVM, V8).
  - **Leaks**: Crecimiento constante sin liberación.
- **I/O (Disk & Network)**:
  - **IOPS**: Latencia en escritura/lectura de disco (SSD vs HDD).
  - **Throughput**: Saturación de la interfaz de red.

## 2. Profiling de Aplicaciones
No adivines dónde está el cuello de botella, mídelo.
- **Node.js**: `clinic.js`, Chrome DevTools, Flamegraphs.
- **Python**: `py-spy`, `cProfile`.
- **Go**: `pprof`.
- **Java**: `JVisualVM`, `YourKit`.

## 3. Optimización de Bases de Datos
- **Consultas Lentas**: `EXPLAIN ANALYZE` para ver planes de ejecución e índices faltantes.
- **Connection Pooling**: Agotamiento de conexiones (usar PgBouncer para Postgres o similares).
- **Locks & Deadlocks**: Procesos bloqueando a otros procesos.

## 4. Estrategias de Caché (Redis/Memcached)
- **Cache Misses**: Tasa alta indica que la caché no es efectiva.
- **Cache stampede**: Muchos procesos pidiendo el mismo dato expirado a la vez.
- **Hot Keys**: Un solo par clave-valor recibiendo todo el tráfico.

> [!CAUTION]
> **Premature Optimization**: No optimices por intuición. Usa datos de profiling primero.
