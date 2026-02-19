---
name: superpower-planning
description: Use when you have requirements for a multi-step task, before touching code. Focuses on TDD, DRY, and frequent commits.
---

# Superpower Planning

> [!IMPORTANT]
> Esta habilidad hereda y se alinea con los principios de **Gemini Skill Creator**. Sigue la metodología de granulación de tareas y diseño basado en pruebas.

## Overview
Escribe planes de implementación exhaustivos asumiendo que el ejecutor tiene poco contexto. Documenta todo: archivos a tocar, código específico, pruebas y documentación necesaria. Divide el plan en tareas del tamaño de un bocado (Acciones de 2-5 minutos).

## Reglas de Planificación
1. **Granularidad**: Acciones mínimas.
2. **Pattern Retrieval**: Antes de proponer una implementación, consultar el **Central Vector Memory (dude-central-brain)** para recuperar fragmentos de código o patrones técnicos que ya hayan sido exitosos en el proyecto.
3. **TDD Forzado**: Siempre empezar por el test fallido.
4. **Paths Exactos**: Rutas absolutas.

## Estructura de Tarea
```markdown
### Task N: [Nombre del Componente]
**Files:**
- Create/Modify: `path/to/file`
- Test: `path/to/test`

**Step 1: Write failing test**
[Código del test]

**Step 2: Verify failure**
Run: [Comando]

**Step 3: Minimal implementation**
[Código]

**Step 4: Verify pass**
Run: [Comando]

**Step 5: Commit**
```

## Referencia Maestra
Esta habilidad promueve el uso de **Gemini Skill Creator** para asegurar que cada tarea cumpla con los estándares globales de calidad y modularidad.
