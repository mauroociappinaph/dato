# Post-Mortem Template - DATO

> **Uso:** Copiar este template para cada incidente P0/P1. Guardar en `docs/post-mortems/YYYY-MM-DD-[incident-name].md`

---

# Post-Mortem: [Título del Incidente]

**Incident ID:** INC-YYYY-XXX
**Fecha:** YYYY-MM-DD
**Hora inicio:** HH:MM (UTC-3)
**Hora resolución:** HH:MM (UTC-3)
**Duración total:** Xh Xm
**Severidad:** P0 / P1 / P2
**Servicios afectados:** [Lista de servicios]
**Detección:** [Monitoring / Usuario / Internal]

---

## Resumen Ejecutivo

> [1-2 oraciones describiendo qué pasó y el impacto en usuarios]

---

## Impacto

| Métrica | Valor |
|---------|-------|
| Usuarios afectados | ~X |
| Requests fallidas | ~X |
| Downtime | Xh Xm |
| Pérdida estimada | $X (si aplica) |

---

## Timeline

| Hora (UTC-3) | Evento | Actor |
|--------------|--------|-------|
| HH:MM | 🚨 Detección inicial | [Sistema/Persona] |
| HH:MM | Notificación equipo | [Persona] |
| HH:MM | Diagnóstico inicial | [Persona] |
| HH:MM | Acción correctiva X | [Persona] |
| HH:MM | Mitigación aplicada | [Persona] |
| HH:MM | Servicio restaurado | [Persona] |
| HH:MM | Confirmación monitoreo | [Persona] |

---

## Causa Raíz (Root Cause Analysis)

### ¿Qué pasó?
[Descripción técnica del fallo]

### ¿Por qué pasó?
[Análisis profundo - no solo el síntoma]

### ¿Por qué no se detectó antes?
[Análisis de gaps en testing/monitoring]

### 5 Whys (opcional)

1. **¿Por qué falló el servicio?** → [Respuesta]
2. **¿Por qué [Respuesta 1]?** → [Respuesta]
3. **¿Por qué [Respuesta 2]?** → [Respuesta]
4. **¿Por qué [Respuesta 3]?** → [Respuesta]
5. **¿Por qué [Respuesta 4]?** → [Root cause]

---

## Acciones Correctivas

| # | Acción | Tipo | Owner | Prioridad | Deadline | Status |
|---|--------|------|-------|-----------|----------|--------|
| 1 | [Acción inmediata] | Fix | @owner | 🔴 Crítica | YYYY-MM-DD | ✅ Done |
| 2 | [Mejora preventiva] | Prevent | @owner | 🟡 Alta | YYYY-MM-DD | ⏳ Pending |
| 3 | [Mejora de monitoring] | Detect | @owner | 🟢 Media | YYYY-MM-DD | ⏳ Pending |
| 4 | [Documentación] | Doc | @owner | 🟢 Media | YYYY-MM-DD | ⏳ Pending |

**Tipos:** Fix (corregir bug), Prevent (prevenir recurrencia), Detect (mejorar detección), Doc (documentar)

---

## Lecciones Aprendidas

### ✅ Qué funcionó bien
- [Aspecto positivo 1]
- [Aspecto positivo 2]

### ❌ Qué no funcionó
- [Aspecto a mejorar 1]
- [Aspecto a mejorar 2]

### 💡 Ideas para mejorar
- [Sugerencia 1]
- [Sugerencia 2]

---

## Recursos

- **Logs:** [Link a LangSmith/CloudWatch/etc]
- **Ticket:** [Link a GitHub Issue]
- **PR Fix:** [Link a PR]
- **Slack thread:** [Link a #incident-XXX]
- **Monitoring dashboard:** [Link a Grafana/etc]

---

## Aprobación

| Rol | Nombre | Fecha |
|-----|--------|-------|
| Incident Lead | | |
| Tech Lead | | |
| CTO (si P0) | | |

---

**Próxima revisión de acciones:** YYYY-MM-DD
