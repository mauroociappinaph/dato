---
name: mcp-vetting-guard
description: Sanitización y validación de outputs provenientes de servidores MCP externos.
---

# MCP Vetting Guard

## Propósito
Actuar como un firewall lógico entre los servidores MCP externos y la lógica de ejecución de la empresa.

## Reglas de Validación
1. **Detección de Scripting:** Bloquear cualquier respuesta que contenga tags `<script>`, `eval()` o comandos de sistema.
2. **Validación de Esquema:** Asegurar que el JSON recibido coincida con el contrato esperado (Zod/Pydantic style).
3. **Redacción de PII:** Forzar el filtrado de datos sensibles si el MCP devuelve información no autorizada.

## Workflow
1. Recibir output de MCP -> 2. Escanear patrones maliciosos -> 3. Validar contra esquema -> 4. Emitir Certificado de Limpieza.
