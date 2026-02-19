# Proceso de Revisión Sistemática

## Fase 1: Contexto (2-3 min)
1. Lee la descripción del PR y el issue vinculado.
2. Si el PR es >400 líneas, sugiere dividirlo.
3. Verifica el estado de CI/CD (pruebas pasando).

## Fase 2: Alto Nivel (5-10 min)
1. **Arquitectura**: ¿La solución encaja? ¿Es escalable?
2. **Evaluación de Trade-offs (`sequentialthinking`)**: Sopesar factores como rendimiento vs. legibilidad, o rapidez vs. mantenibilidad, priorizando la visión de Mauro.
3. **Organización**: ¿Archivos en el lugar correcto? ¿Lógica agrupada?
4. **Estrategia de Tests**: ¿Hay tests? ¿Son legibles?

## Fase 3: Línea por Línea (10-20 min)
1. **Lógica**: Casos borde, errores de "off-by-one", null/undefined.
2. **Seguridad**: Validación de input, SQL injection, XSS, secretos.
3. **Rendimiento**: Consultas N+1, leaks de memoria, operaciones bloqueantes.
4. **Mantenibilidad**: Nombres claros, funciones SRP, comentarios útiles.

## Fase 4: Resumen y Decisión
1. Resume las preocupaciones principales.
2. Destaca lo positivo.
3. Toma una decisión clara:
   - ✅ **Aprobar**
   - 💬 **Comentar** (sugerencias menores)
   - 🔄 **Solicitar Cambios** (debe abordarse)
