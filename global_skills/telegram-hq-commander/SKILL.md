---
name: telegram-hq-commander
description: Interfaz de comando remoto vía Telegram. Permite al usuario Mauro dar órdenes al Senior Architect desde cualquier lugar, recibir reportes de estado y gestionar despliegues mediante un puente seguro.
---

# Telegram HQ Commander: Tu Centro de Comando en el Bolsillo

> [!IMPORTANT]
> **Seguridad Crítica**: Este agente solo responde a comandos provenientes del **Telegram User ID de Mauro**. Cualquier otro intento de acceso es ignorado y alertado.
> **Privacidad**: Nunca enviar secretos o API Keys en texto plano por el chat de Telegram.

## Funciones Principales
1. **Control de Estado**: Comando `/status` para resumen de procesos.
2. **Gestión de Proyectos**: Consultas directas sobre el estado de GitHub.
3. **Ejecución Remota**: Disparar deploys y tareas desde el chat.
4. **Notificaciones Proactivas & Alertas de Riesgo**: Notificar fallos de deploy y, proactivamente, alertar sobre riesgos detectados semánticamente en el repositorio mediante consultas recurrentes al **Central Vector Memory (dude-central-brain)**.

## Protocolo de Comunicación
- **Entrada**: Mensajes de texto, comandos de barra (`/`), o notas de voz (que el LLM transcribe).
- **Salida**: Texto estructurado, capturas de pantalla de logs (opcional), y botones de acción rápida.

## Configuración de Emergencia
Si la PC local está apagada, el agente en la nube (Vercel/Railway) toma el control para responder dudas teóricas o verificar estados externos (GitHub/Vercel).

---
*Powered by Gemini Skill Creator - "The power of your engineering suite, everywhere"*