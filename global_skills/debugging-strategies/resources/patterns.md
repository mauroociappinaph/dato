# Patrones de Depuración por Tipo de Problema

## Patrón 1: Errores Intermitentes (Flaky)
1. **Logs extensos**: Registra todos los tiempos y transiciones de estado.
2. **Carreras (Race Conditions)**: Busca accesos concurrentes a estados compartidos o promesas que terminan fuera de orden.
3. **Dependencias de tiempo**: Revisa `setTimeout`, intervalos y resoluciones de promesas.
4. **Stress Test**: Ejecuta el proceso muchas veces seguidas bajo carga.

## Patrón 2: Problemas de Rendimiento
1. **Perfilado (Profiling)**: No optimices a ciegas. Mide primero.
2. **Culpables comunes**: Consultas N+1, re-renders innecesarios, I/O síncrono en rutas calientes.
3. **Herramientas**: Lighthouse, Chrome DevTools Performance, `py-spy` o `0x`.

## Patrón 3: Errores de Producción
1. **Evidencia**: Sentry, Bugsnag, logs de la aplicación y métricas.
2. **Reproducción Local**: Usa datos anonimizados de producción para igualar el entorno.
3. **Inhibición de cambios**: No cambies nada en producción directamente; usa feature flags o despliega en staging primero para validar el fix.
