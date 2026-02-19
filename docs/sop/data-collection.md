# SOP-004: Data Collection - DATO

## SOP-004: Data Collection

### 4.1 INDEC Scraping

#### Schedule

```
Diario: 9:00 AM Argentina
URL: https://www.indec.gob.ar/
Método: Firecrawl MCP
```

#### Procedimiento

```bash
# Via Kilo CLI con Firecrawl
kilo run "Use firecrawl to scrape INDEC homepage for latest inflation data"

# Via script
cd apps/api
pnpm run scrape:indec
```

#### Datos a Extraer

| Dato | Selector/Pattern | Frecuencia |
|------|------------------|------------|
| IPC (inflación) | Tabla mensual | Mensual |
| Pobreza | Informe semestral | Semestral |
| Empleo | Encuesta permanente | Trimestral |
| PBI | Informe trimestral | Trimestral |

### 4.2 BCRA Data Sync

#### Schedule

```
Cada 3 horas
URL: https://www.bcra.gob.ar/
Método: API oficial + Firecrawl/Exa backup
```

#### Datos a Extraer

| Dato | Endpoint | Frecuencia |
|------|----------|------------|
| Dólar oficial | /api/dolar | Tiempo real |
| Reservas | /api/reservas | Diario |
| Tasas | /api/tasas | Diario |
| Base monetaria | /api/base | Semanal |

### 4.3 BOLETIN_OFICIAL Scraping

#### Schedule

```
Diario: 10:00 AM Argentina
URL: https://www.boletinoficial.gob.ar/
Método: Firecrawl MCP + Exa Search
```

#### Procedimiento

```bash
# Via Kilo CLI con Firecrawl
kilo run "Use firecrawl to scrape BOLETIN_OFICIAL for latest decrees and resolutions"

# Via Kilo CLI con Exa (backup)
kilo run "Use exa_search to find official bulletins from Argentina government"

# Via script
cd apps/api
pnpm run scrape:boletin
```

#### Datos a Extraer

| Dato | Selector/Pattern | Frecuencia |
|------|------------------|------------|
| Decretos | Sección decretos | Diario |
| Resoluciones | Sección resoluciones | Diario |
| Disposiciones | Sección disposiciones | Diario |
| Avisos oficiales | Sección avisos | Diario |

#### Cron Job

```yaml
# apps/api/src/cron/collector.cron.ts

- name: boletin-daily
  schedule: "0 10 * * *"   # 10:00 AM diario
  source: BOLETIN_OFICIAL
  timezone: America/Argentina/Buenos_Aires
```

### 4.4 MCP Tools: Firecrawl vs Exa

#### Firecrawl MCP (Primary)

```bash
# Best for: Scraping contenido específico de URLs conocidas
kilo run "Use firecrawl_scrape to extract data from https://indec.gob.ar/..."

# Use when:
# - URL específica conocida
# - Necesitas contenido completo de la página
# - Estructura HTML predecible
```

#### Exa Search MCP (Backup/Discovery)

```bash
# Best for: Descubrir URLs y buscar contenido
kilo run "Use exa_search to find inflation data from Argentina government sources"

# Use when:
# - URL específica no conocida
# - Necesitas buscar en múltiples fuentes
# - Firecrawl falla (fallback)
```

#### Procedimiento Combinado

```bash
# 1. Intentar Firecrawl primero
kilo run "Use firecrawl_scrape on [URL]"

# 2. Si falla, usar Exa como backup
kilo run "Use exa_search to find [data] and then scrape results"

# 3. Guardar datos en Supabase
kilo run "Save collected data to economic_data table"
```

### 4.5 YouTube Transcript Extraction

#### Procedimiento

```bash
# 1. Buscar videos
kilo run "Search YouTube for 'discurso político Argentina' last 24 hours"

# 2. Extraer transcript
kilo run "Get transcript from video ID: abc123"

# 3. Enviar a Agent 2
kilo run "Extract claims from this transcript: [transcript]"
```

#### Canales Monitoreados

| Canal | Tipo | Frecuencia |
|-------|------|------------|
| Casa Rosada | Oficial | Todos los discursos |
| C5N | Noticias | Segmentos políticos |
| TN | Noticias | Segmentos económicos |
| LN+ | Noticias | Entrevistas políticas |

### 4.6 Error Handling

#### Retry Policy (Exponential Backoff)

```python
def collect_data(source):
    # Exponential backoff: 5s → 10s → 20s
    # Initial delay: 5000ms (5 seconds)
    # Per specs/agents.md retry_policy
    delays = [5, 10, 20]  # seconds
    
    for attempt in range(3):
        try:
            data = scrape(source)
            save_to_db(data)
            return success
        except TimeoutError:
            if attempt < 2:
                wait(delays[attempt])  # Exponential: 5s → 10s → 20s
        except ValidationError:
            log_error("Invalid data format")
            return failure
        except SourceDownError:
            use_cache(source)
            notify_team(f"{source} unavailable")
            return cached
    
    return failure
```

#### Retry Configuration

| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `max_retries` | 3 | Máximo intentos |
| `backoff` | exponential | Tipo de backoff |
| `initial_delay_ms` | 5000 | Delay inicial (5s) |
| Delays | 5s → 10s → 20s | Secuencia exponencial |

#### Fallback Chain

```
Firecrawl falla → Exa Search → DuckDuckGo → Cache local
```

---

