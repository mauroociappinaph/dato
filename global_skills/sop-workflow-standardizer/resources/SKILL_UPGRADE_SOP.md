---
name: skill-upgrade-protocol
description: Standard Operating Procedure for upgrading a skill from score 5/10 (manual) to 10/10 (automated execution).
---

# SOP: JIT Skill Upgrading

Este protocolo asegura que nuestra empresa automatice sus procesos de forma orgánica y eficiente.

## 1. Disparador (Trigger)
Una orden del Dueño o del CEO requiere el uso de una skill que no posee archivos en su directorio `scripts/`.

## 2. Fase de Diseño (Architecture)
- **Responsable:** `senior-architect`.
- **Acción:** Definir qué inputs (argumentos) necesita el script y qué output debe devolver para ser útil al Orquestador.

## 3. Fase de Construcción (Development)
- **Responsable:** `gemini-skill-creator`.
- **Acción:** Escribir el script (Python o TypeScript) siguiendo los estándares de la empresa (Error handling, logs limpios).
- **Ubicación:** `~/.gemini/anti_gravity/global_skills/[skill-name]/scripts/main.py`.

## 4. Fase de Certificación (QA)
- **Responsable:** `agent-evaluation`.
- **Acción:** Ejecutar el script con `--help` o con datos de prueba. Si pasa, el especialista es marcado como **"Ejecutable (10/10)"**.

## 5. Continuidad
Solo tras la certificación, la tarea original se reanuda usando la nueva herramienta automatizada.
