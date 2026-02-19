# Seguridad y Gobernanza de la IA

Principios y herramientas para construir sistemas de inteligencia artificial seguros, éticos y conformes.

## Mitigación de Riesgos en LLMs
- **Prompt Injection**: Uso de delimitadores, detección de instrucciones maliciosas y validación de outputs.
- **Jailbreaking**: Protección contra intentos de saltarse los filtros de seguridad del modelo.
- **Alucinaciones**: Implementación de pasos de verificación y fundamentación en datos reales (Grounding).

## Privacidad de Datos (PII)
- **Detección y Redacción**: Escaneo automático de entradas y salidas para detectar Información de Identificación Personal (Nombres, DNI, Emails) antes de enviarlos a proveedores externos.
- **Anonimización**: Reemplazo de datos sensibles por placeholders genéricos para mantener el contexto sin comprometer la privacidad.

## Gobernanza y Ética
- **Detección de Sesgos (Bias)**: Pruebas sistemáticas para asegurar que el modelo no discrimine por género, raza o religión.
- **Transparencia**: El sistema debe poder explicar (o dejar traza de) por qué tomó una decisión (Explainable AI).
- **IA Responsable**: Definición de límites claros; el sistema debe saber cuándo decir "no sé" o cuándo escalar a un humano.

## Moderación de Contenido
- **Filtros de Entrada/Salida**: Uso de APIs de moderación (como OpenAI Moderation API) o modelos locales especializados.
- **Guardrails**: Implementación de NeMo Guardrails o herramientas similares para forzar el cumplimiento de políticas de diálogo.

## Seguridad en el Desarrollo
- **Gestión de Secretos**: Nunca hardcodear API Keys; usar Vaults o variables de entorno seguras.
- **Sandboxing**: Todo código generado por IA debe ejecutarse en entornos totalmente aislados (gVisor, Firecracker).
- **Auditoría**: Mantener un rastro inmutable de todas las interacciones con el LLM para auditorías de cumplimiento.

## Checklist de Seguridad
- [ ] ¿Están las API Keys protegidas?
- [ ] ¿Hay detección de PII activa?
- [ ] ¿El sistema previene la inyección de prompts?
- [ ] ¿Se auditan las salidas del modelo para detectar alucinaciones peligrosas?
- [ ] ¿Existe un plan de respuesta ante comportamientos inesperados de la IA?
