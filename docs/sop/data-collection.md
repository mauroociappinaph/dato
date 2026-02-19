# SOP-004: Data Collection - DATO

> **Última actualización:** 2026-02-19
> **Versión:** 2.0

---

## 4.1 Fallback Chain Unificada

```
┌─────────────────────────────────────────────────────────────┐
│                    FALLBACK CHAIN                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PASO 1: Firecrawl MCP                                      │
│  ├── URL conocida → scrape directo                          │
│  ├── Timeout: 30s                                           │
│  └── Si falla → PASO 2                                      │
│                                                              │
│  PASO 2: Exa Search MCP                                     │
│  ├── Búsqueda de contenido alternativo                      │
│  ├── Timeout: 20s                                           │
│  └── Si falla → PASO 3                                      │
│                                                              │
│  PASO 3: DuckDuckGo Search                                  │
│  ├── Búsqueda web alternativa                               │
│  ├── Timeout: 15s                                           │
│  └── Si falla → PASO 4                                      │
│                                                              │
│  PASO 4: Cache Local                                        │
│  ├── Usar datos cacheados (últimas 24h)                    │
│  ├── Marcar como "cached"                                   │
│  └── Notificar al equipo                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Retry Procedure (Exponential Backoff)

| Intento | Delay | Acción |
|---------|-------|--------|
| 1 | 5s | Reintentar fuente actual |
| 2 | 10s | Reintentar fuente actual |
| 3 | 20s | Pasar a siguiente fuente en chain |

**Timeout total máximo:** 120 segundos

---

## 4.2 Checklist de Validación de Datos Scrapeados

Antes de guardar datos, validar:

```
□ Dato no vacío (value != null/empty)
□ Formato correcto (número, fecha, texto según tipo)
□ Fuente identificada y registrada
│
□ Para números:
│   ├── Rango razonable (no negativo para inflación, etc.)
│   ├── Unidad correcta (%, USD, millones)
│   └── Período válido (fecha en formato correcto)
│
□ Para texto:
│   ├── Encoding correcto (UTF-8)
│   ├── Sin caracteres corruptos
│   └── Longitud razonable (< 10MB)
│
□ Metadatos:
│   ├── Timestamp de recolección
│   ├── Agente que recolectó (agent-1)
│   └── URL fuente
```

---

## 4.3 Runbooks por Fuente

### Runbook: INDEC

> **Ver:** [runbook-indec.md](./runbooks/runbook-indec.md)

**Schedule:** Diario 9:00 AM Argentina

**URL Principal:** https://www.indec.gob.ar/

**Datos a Extraer:**

| Dato | Endpoint/Selector | Frecuencia |
|------|-------------------|------------|
| IPC (inflación) | Tabla mensual principal | Mensual |
| Pobreza | Informe semestral | Semestral |
| Empleo | Encuesta permanente | Trimestral |
| PBI | Informe trimestral | Trimestral |

---

### Runbook: BCRA

> **Ver:** [runbook-bcra.md](./runbooks/runbook-bcra.md)

**Schedule:** Cada 3 horas

**URL Principal:** https://www.bcra.gob.ar/

**Datos a Extraer:**

| Dato | Endpoint | Frecuencia |
|------|----------|------------|
| Dólar oficial | /api/dolar | Tiempo real |
| Reservas | /api/reservas | Diario |
| Tasas | /api/tasas | Diario |
| Base monetaria | /api/base | Semanal |

---

### Runbook: Boletín Oficial

> **Ver:** [runbook-boletin.md](./runbooks/runbook-boletin.md)

**Schedule:** Diario 10:00 AM Argentina

**URL Principal:** https://www.boletinoficial.gob.ar/

**Datos a Extraer:**

| Dato | Sección | Frecuencia |
|------|---------|------------|
| Decretos | Sección decretos | Diario |
| Resoluciones | Sección resoluciones | Diario |
| Disposiciones | Sección disposiciones | Diario |
| Avisos oficiales | Sección avisos | Diario |

---

## 4.4 MCP Tools Comparison

| Herramienta | Uso | Cuando usar |
|-------------|-----|-------------|
| **Firecrawl** | Scrape directo | URL conocida, estructura predecible |
| **Exa Search** | Búsqueda/AI | URL desconocida, descubrimiento |
| **DuckDuckGo** | Web search | Fallback, resultados públicos |

---

## 4.5 Error Handling

```python
def collect_with_fallback(source):
    """
    Collection with unified fallback chain.
    Implements exponential backoff: 5s → 10s → 20s
    """
    tools = ['firecrawl', 'exa', 'duckduckgo', 'cache']
    delays = [5, 10, 20]
    
    for tool in tools:
        for attempt in range(3):
            try:
                data = collect(source, tool)
                if validate(data):
                    save_to_db(data)
                    return success(tool)
            except TimeoutError:
                if attempt < 2:
                    wait(delays[attempt])
                continue
            except ValidationError:
                log_error(f"Invalid data from {tool}")
                break
        
        # Tool failed, try next
        log_warning(f"{tool} failed for {source}")
    
    return failure()
```

---

## 4.6 Cron Jobs Configuration

```yaml
# apps/api/src/cron/collector.cron.ts

sources:
  - name: indec-daily
    schedule: "0 9 * * *"
    timezone: America/Argentina/Buenos_Aires
    source: INDEC
    
  - name: bcra-every-3h
    schedule: "0 */3 * * *"
    timezone: America/Argentina/Buenos_Aires
    source: BCRA
    
  - name: boletin-daily
    schedule: "0 10 * * *"
    timezone: America/Argentina/Buenos_Aires
    source: BOLETIN_OFICIAL
```

---

*Fin del documento*
