# DATO SOP Wiki

> **Última actualización:** 2026-02-19
> **Versión:** 1.0

---

## 📚 Índice de SOPs

| SOP | Título | Descripción | Última actualización |
|-----|--------|-------------|---------------------|
| [SOP-001](./development.md) | Desarrollo | Workflow de desarrollo, convenciones de código | 2026-02-13 |
| [SOP-002](./agents.md) | Ejecución de Agentes | Handoffs, edge cases, formatos JSON | 2026-02-19 |
| [SOP-003](./fact-checking.md) | Fact-Checking | Procedimiento de verificación manual | 2026-02-19 |
| [SOP-004](./data-collection.md) | Data Collection | Fallback chain, validaciones | 2026-02-19 |
| [SOP-005](./billing.md) | Billing | Stripe, planes, webhooks | 2026-02-13 |
| [SOP-006](./publishing.md) | Publishing | Canales de distribución | 2026-02-13 |
| [SOP-007](./incidents.md) | Incidentes | Procedimiento de respuesta | 2026-02-13 |
| [SOP-008](./deploy.md) | Deploy | Procedimiento de deployment | 2026-02-13 |
| [SOP-009](./ci-troubleshooting.md) | CI Troubleshooting | Problemas comunes en CI | 2026-02-13 |

---

## ✅ Quick Reference de Checklists

### Pre-Verificación (Fact-Checking)

```
□ Claim identificado y extraído
□ Speaker identificado
□ Fecha del claim registrada
□ Contexto documentado
□ Categoría asignada
□ No es opinión subjetiva
□ Fuente primaria identificada
```

### Pre-Publicación

```
□ Veredicto asignado correctamente
□ Confidence calculado
□ Fuente citada con link
□ Explicación en lenguaje simple
□ Sin opiniones personales
□ Badge asignado
```

### Pre-Handoff (Agentes)

```
□ Output en formato JSON válido
□ Timestamp registrado
□ Status documentado
□ Métricas incluidas
□ Sin errores en logs
```

---

## 🔧 Runbooks

| Fuente | Runbook | Schedule |
|--------|---------|----------|
| INDEC | [runbook-indec.md](./runbooks/runbook-indec.md) | Diario 9:00 AM |
| BCRA | [runbook-bcra.md](./runbooks/runbook-bcra.md) | Cada 3 horas |
| Boletín Oficial | [runbook-boletin.md](./runbooks/runbook-boletin.md) | Diario 10:00 AM |

---

## 🚨 Troubleshooting Index

### Agentes

| Problema | Solución | SOP |
|----------|----------|-----|
| Agent 2 extrae 0 claims | Verificar si es opinión, marcar como skip | [SOP-002](./agents.md#edge-cases) |
| Agent 3 no encuentra datos | Asignar SIN_DATOS, sugerir fuentes | [SOP-002](./agents.md#edge-cases) |
| Agent 4 falla en simplificar | Usar template fallback | [SOP-002](./agents.md#edge-cases) |

### Data Collection

| Problema | Solución | SOP |
|----------|----------|-----|
| Firecrawl timeout | Usar Exa como backup | [SOP-004](./data-collection.md#fallback-chain) |
| Dato inválido | Validar formato, rechazar si no pasa | [SOP-004](./data-collection.md#validacion) |
| Fuente caída | Usar cache local < 24h | [SOP-004](./data-collection.md#fallback-chain) |

### CI/CD

| Problema | Solución | SOP |
|----------|----------|-----|
| Tests fallan | `gh run view --log` → arreglar → push | [SOP-009](./ci-troubleshooting.md) |
| Build falla | Verificar dependencias, typecheck | [SOP-009](./ci-troubleshooting.md) |
| Deploy falla | Verificar secrets, health checks | [SOP-008](./deploy.md) |

---

## 📊 Badges de Verificación

| Badge | Significado | Condición |
|-------|-------------|-----------|
| ✅ | Verdadero | Confidence ≥ 85%, datos coinciden |
| ⚠️ | Parcialmente verdadero | 70-84% coincidencia |
| ❌ | Falso | Confidence ≥ 85%, datos contradicen |
| ⚪ | Sin datos | Confidence < 70% |

---

## 🔄 Flujo de Handoffs

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Agent 1   │───▶│   Agent 2   │───▶│   Agent 3   │───▶│   Agent 4   │───▶│   Agent 5   │
│  Collector  │    │  Extractor  │    │ Fact Checker│    │  Simplifier │    │  Publisher  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
      │                  │                  │                  │                  │
      ▼                  ▼                  ▼                  ▼                  ▼
 datos brutos      claims extraídos    verificaciones    explicación        publicado
                                       + badges           simple
```

---

## 📞 Contactos

| Rol | Responsable | Contacto |
|-----|-------------|----------|
| Tech Lead | TBD | - |
| DevOps | TBD | - |
| Data | TBD | - |

---

## 📝 Versionado

Todos los SOPs incluyen:
- Fecha de última actualización
- Número de versión
- Historial de cambios (en el documento)

Formato de versionado: `MAJOR.MINOR`
- MAJOR: Cambios estructurales
- MINOR: Actualizaciones menores, correcciones

---

*Wiki generada automáticamente. Mantener actualizado.*
