# SOP-006: Incidentes - DATO

## SOP-006: Incidentes

### 6.1 Clasificación de Severidad

| Nivel | Nombre | Impacto | SLA |
|-------|--------|---------|-----|
| P0 | Crítico | Servicio caído | 15 min |
| P1 | Alto | Feature principal roto | 1 hora |
| P2 | Medio | Feature secundario roto | 4 horas |
| P3 | Bajo | Bug menor | 24 horas |

### 6.2 Response Procedure

```
Detección del incidente
│
├── P0/P1: Inmediatamente
│   ├── Notificar equipo (Slack #incidents)
│   ├── Crear incident channel
│   ├── Asignar on-call engineer
│   └── Iniciar bridge call
│
├── P2: Dentro de 30 min
│   ├── Crear ticket
│   ├── Asignar developer
│   └── Investigar causa
│
└── P3: Dentro de 4 horas
    ├── Crear ticket
    ├── Priorizar en backlog
    └── Investigar cuando sea posible
```

### 6.3 Escalation Matrix

| Nivel | Escalar a | Después de |
|-------|-----------|------------|
| P0 | CTO + CEO | 30 min sin resolución |
| P1 | Tech Lead | 1 hora sin resolución |
| P2 | Senior Dev | 4 horas sin resolución |
| P3 | Equipo | No escalar |

### 6.4 Comunicación

#### Template: Incident Start

```
🚨 INCIDENT [P0/P1/P2/P3]

**Servicio:** [Servicio afectado]
**Impacto:** [Descripción del impacto]
**Inicio:** [Timestamp]
**Status:** Investigando

**Canal:** #incident-[id]
**Lead:** [Persona a cargo]

Próxima actualización: [time]
```

#### Template: Incident Update

```
📊 UPDATE [Timestamp]

**Status:** [Investigando/Identificado/Mitigando/Resuelto]
**Progreso:** [Qué se ha hecho]
**ETA:** [Tiempo estimado]

Próxima actualización: [time]
```

#### Template: Incident Resolved

```
✅ RESUELTO [Timestamp]

**Duración total:** [Tiempo]
**Causa raíz:** [Descripción]
**Acción tomada:** [Qué se hizo]
**Post-mortem:** [Link o fecha]

Gracias al equipo: [Nombres]
```

### 6.5 Post-Mortem Template

```markdown
# Post-Mortem: [Título del incidente]

**Fecha:** [Fecha]
**Duración:** [Tiempo]
**Severidad:** [P0/P1/P2/P3]
**Servicios afectados:** [Lista]

## Resumen
[Descripción breve del incidente]

## Timeline
| Hora | Evento |
|------|--------|
| XX:XX | Detección |
| XX:XX | Acción 1 |
| XX:XX | Resolución |

## Causa Raíz
[Análisis de por qué ocurrió]

## Acciones Correctivas
| Acción | Owner | Deadline |
|--------|-------|----------|
| [Acción 1] | [Persona] | [Fecha] |
| [Acción 2] | [Persona] | [Fecha] |

## Lecciones Aprendidas
[Qué aprendimos]

## Links
- [Link a logs]
- [Link a ticket]
- [Link a PR de fix]
```

---

