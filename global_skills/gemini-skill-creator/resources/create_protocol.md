---
name: Global Skill Factory Protocol
description: Workflow for creating new skills using 'Dude CREATE'. Includes research, sequential planning, and automated generation.
---

# Dude CREATE: Global Skill Factory

Este protocolo se activa automáticamente cuando Mauro ordena la creación de una nueva habilidad.

## Flujo de Trabajo (Orquestación):

1.  **Paso 1: Inteligencia (Benchmarking)**
    - 🏢 **Depto. Inteligencia** investiga en Google/Reddit las mejores prácticas y herramientas para la habilidad solicitada.
2.  **Paso 2: Razonamiento (Sequential Thinking)**
    - 🏢 **Depto. Estrategia** diseña la estructura de la habilidad, definiendo qué scripts, recursos y ejemplos necesita para ser de "Nivel Élite".
3.  **Paso 3: Nomenclatura (Naming Enforcer)**
    - Se asegura que el nombre sea `kebab-case` y cumpla con el estándar Antigravity.
4.  **Paso 4: Generación (Gemini Skill Creator)**
    - 🏢 **Depto. Arquitectura** crea la carpeta en `~/.gemini/anti_gravity/global_skills/` con su `SKILL.md`, `scripts/`, `resources/` y `examples/`.

## Comando:
`Dude CREATE [nombre de la skill] (descripción opcional)`
