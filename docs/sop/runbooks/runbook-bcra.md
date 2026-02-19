# Runbook: BCRA Data Collection

> **Fuente:** Banco Central de la República Argentina
> **URL:** https://www.bcra.gob.ar/
> **Schedule:** Cada 3 horas

---

## 1. Objetivo

Extraer datos de dólar oficial, reservas, tasas y base monetaria del BCRA.

---

## 2. URLs Objetivo

| Página | URL | Datos |
|--------|-----|-------|
| Principal | https://www.bcra.gob.ar/ | Enlaces a datos |
| Dólar | https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables.asp | Todas las variables |
| API (si disponible) | https://api.bcra.gob.ar/ | Datos estructurados |

---

## 3. Procedimiento Paso a Paso

### Paso 1: Intentar API oficial (si disponible)

```bash
curl -X GET "https://api.bcra.gob.ar/estadisticas/v2.0/principalesvariables" -H "Accept: application/json"
```

### Paso 2: Si no hay API, usar Firecrawl

```bash
kilo run "Use firecrawl_scrape on https://www.bcra.gob.ar/PublicacionesEstadisticas/Principales_variables.asp to extract dollar exchange rates and reserves data"
```

**Tiempo máximo:** 30 segundos

### Paso 3: Si falla, usar Exa Search

```bash
kilo run "Use exa_search to find 'BCRA dólar oficial reservas Argentina hoy' and extract current values"
```

### Paso 4: Validar datos

```python
def validate_bcra_data(data):
    # Dólar oficial
    if data['indicator'].startswith('dollar'):
        assert 100 < data['value'] < 5000, "Dólar fuera de rango razonable"
    
    # Reservas
    if data['indicator'] == 'reserves':
        assert data['value'] > 0, "Reservas deben ser positivas"
    
    # Tasas
    if data['indicator'] == 'interest_rate':
        assert 0 < data['value'] < 200, "Tasa fuera de rango"
    
    return True
```

### Paso 5: Guardar en Supabase

```sql
INSERT INTO economic_data (indicator, value, period, period_type, source, source_url)
VALUES 
  ('dollar_official_buy', :buy, CURRENT_DATE, 'daily', 'BCRA', :url),
  ('dollar_official_sell', :sell, CURRENT_DATE, 'daily', 'BCRA', :url),
  ('reserves', :reserves, CURRENT_DATE, 'daily', 'BCRA', :url);
```

---

## 4. Selectores CSS (Firecrawl)

```yaml
selectors:
  main_table: "table.tbl_datos"
  dollar_row: "tr:contains('Dólar')"
  reserves_row: "tr:contains('Reservas')"
  value_cell: "td:nth-child(2)"
```

---

## 5. Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| SSL Error | Certificado BCRA | Verificar cert, usar http como backup |
| Tabla vacía | Página no actualizada | Usar cache, notificar equipo |
| Valor inválido | Cambio de formato | Actualizar parser |

---

## 6. Contacto BCRA

- **Web:** https://www.bcra.gob.ar/
- **Teléfono:** +54 11 4348-3500
- **Estadísticas:** estadisticas@bcra.gob.ar

---

*Última actualización: 2026-02-19*
