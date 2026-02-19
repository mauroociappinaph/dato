---
name: task-prompt-engineer
description: Genera prompts de ejecución estructurados para cada subtask de TASK.md. 2026 Edition.
---

# Task Prompt Engineer

## Purpose
Transformar subtasks de TASK.md en prompts ejecutables listos para ser procesados por agentes de IA.

## Capabilities
1. **Parser de TASK.md**: Extrae subtasks con su estructura completa
2. **Context Builder**: Identifica archivos, dependencias y skills relacionadas
3. **Prompt Generator**: Crea prompts estructurados con:
   - Contexto del proyecto
   - Objetivo específico
   - Comandos a ejecutar
   - Criterios de aceptación
   - Skills a invocar
   - Dependencias

## Workflow
```
Input: Subtask ID (ej: "0.2.1")
  ↓
1. Leer TASK.md y extraer subtask
  ↓
2. Identificar:
   - Skills referenciadas
   - Dependencias (secciones previas)
   - Archivos a crear/modificar
   - Comandos documentados
  ↓
3. Construir prompt estructurado
  ↓
4. Output: Prompt ejecutable
```

## Prompt Template
El prompt generado sigue esta estructura:

```markdown
## Contexto
- Proyecto: DATO (fact-checking político argentino)
- Fase: [FASE X]
- Subtask: [ID] - [Nombre]

## Objetivo
[Descripción extraída de TASK.md]

## Skills a usar
- `@global_skills/skill-1/`
- `@global_skills/skill-2/`

## Archivos involucrados
- Crear: [lista de archivos]
- Modificar: [lista de archivos]
- Leer: [lista de archivos]

## Comandos
```bash
[comandos extraídos de TASK.md]
```

## Criterios de Aceptación
- [ ] Criterio 1
- [ ] Criterio 2

## Dependencias
- Requiere: [subtasks previas]
- Bloquea: [subtasks siguientes]

## Notas
[Cualquier contexto adicional]
```

## Triggers
- Ejecución manual antes de iniciar una subtask
- Puede usarse para generar todos los prompts de una fase

## Rules
- Siempre leer el TASK.md completo para entender contexto
- Verificar que las skills referenciadas existen
- Incluir SOLO las dependencias relevantes
- Los comandos deben ser ejecutables tal cual