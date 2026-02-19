# Protocolo de Curación de Contenido

Este protocolo debe ser invocado por cualquier agente antes de realizar una actualización masiva en la memoria central basada en fuentes externas.

## Paso 1: Triaje de Datos
- Clasificar la fuente: ¿Es un foro (Reddit), un paper científico, o un blog de una empresa de bases de datos?
- Asignar nivel de confianza inicial.

## Paso 2: Ejecución de Evals
- **Consistencia:** ¿La información se repite en al menos 3 fuentes independientes?
- **Obsolescencia:** ¿La fecha de la información es actual (2025-2026)?
- **Accionabilidad:** ¿Podemos implementar un cambio en `AGENT_OPS` o `AGENT_INTEL` basándonos en esto?

## Paso 3: Registro de Curación
Al guardar en la memoria, el registro debe incluir:
- `curated_by`: El agente que realizó la curación.
- `verification_method`: Herramientas usadas (ej: Google Search).
- `fit_score`: Del 1 al 10, qué tan bien encaja con DUDE S.A.S.
