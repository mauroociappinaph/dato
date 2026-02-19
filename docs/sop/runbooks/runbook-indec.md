# Runbook: INDEC Data Collection

> **Fuente:** Instituto Nacional de Estadística y Censos
> **URL:** https://www.indec.gob.ar/
> **Schedule:** Diario 9:00 AM Argentina

---

## 1. Objetivo

Extraer datos oficiales de inflación, pobreza, empleo y PBI del INDEC.

---

## 2. URLs Objetivo

| Página | URL | Datos |
|--------|-----|-------|
| Principal | https://www.indec.gob.ar/ | Enlaces a informes |
| IPC | https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31 | Inflación mensual |
| Pobreza | https://www.indec.gob.ar/indec/web/Nivel4-Tema-4-46-165 | Pobreza e indigencia |
| Empleo | https://www.indec.gob.ar/indec/web/Nivel4-Tema-4-41-120 | Empleo y desempleo |

---

## 3. Procedimiento Paso a Paso

### Paso 1: Intentar Firecrawl

```bash
kilo run "Use firecrawl_scrape on https://www.indec.gob.ar/indec/web/Nivel4-Tema-3-5-31 to extract the latest IPC monthly data table"
```

**Tiempo máximo:** 30 segundos

### Paso 2: Si falla, usar Exa Search

```bash
kilo run "Use exa_search to find 'INDEC inflación Argentina [mes actual]' and extract the IPC value"
```

**Tiempo máximo:** 20 segundos

### Paso 3: Validar datos

```python
# Validación específica INDEC
def validate_indec_ipc(data):
    assert data['value'] >= 0, "IPC no puede ser negativo"
    assert data['value'] < 100, "IPC mensual > 100% es improbable"
    assert data['source'] == 'INDEC'
    assert data['period'].month == current_month or data['period'].month == last_month
    return True
```

### Paso 4: Guardar en Supabase

```sql
INSERT INTO economic_data (indicator, value, period, period_type, source, source_url)
VALUES ('inflation_monthly', :value, :period, 'monthly', 'INDEC', :url)
ON CONFLICT (indicator, period, source) DO UPDATE SET value = EXCLUDED.value;
```

---

## 4. Selectores CSS (Firecrawl)

```yaml
selectors:
  ipc_table: "table.tablas" o "div.contenido table"
  value_cell: "td:nth-child(2)" # Segunda columna = variación mensual
  date_cell: "th" # Encabezado con mes/año
```

---

## 5. Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| 403 Forbidden | Rate limit | Esperar 60s, reintentar |
| Timeout | Página lenta | Usar Exa como backup |
| Selector no encontrado | Cambio de layout | Actualizar selectores, notificar equipo |
| Dato vacío | Informe no publicado | Marcar SIN_DATOS, reintentar en 1h |

---

## 6. Contacto INDEC

- **Web:** https://www.indec.gob.ar/
- **Teléfono:** +54 11 4899-6000
- **Email:** comunicacion@indec.gob.ar

---

*Última actualización: 2026-02-19*
