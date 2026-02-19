# Runbook: Boletín Oficial Data Collection

> **Fuente:** Boletín Oficial de la República Argentina
> **URL:** https://www.boletinoficial.gob.ar/
> **Schedule:** Diario 10:00 AM Argentina

---

## 1. Objetivo

Extraer decretos, resoluciones, disposiciones y avisos oficiales publicados en el Boletín Oficial.

---

## 2. URLs Objetivo

| Página | URL | Datos |
|--------|-----|-------|
| Principal | https://www.boletinoficial.gob.ar/ | Últimas publicaciones |
| Búsqueda | https://www.boletinoficial.gob.ar/busqueda | Búsqueda avanzada |
| Sección 1 | https://www.boletinoficial.gob.ar/seccion/primera | Normativas |

---

## 3. Procedimiento Paso a Paso

### Paso 1: Intentar Firecrawl

```bash
kilo run "Use firecrawl_scrape on https://www.boletinoficial.gob.ar/ to extract today's decrees and resolutions from the main page"
```

**Tiempo máximo:** 30 segundos

### Paso 2: Si falla, usar Exa Search

```bash
kilo run "Use exa_search to find 'Boletín Oficial Argentina decretos [fecha actual]' and extract the official publications"
```

### Paso 3: Validar datos

```python
def validate_boletin_data(data):
    # Verificar fecha de publicación
    assert data['published_at'].date() <= today, "Fecha futura no válida"
    
    # Verificar tipo de documento
    valid_types = ['decreto', 'resolución', 'disposición', 'aviso']
    assert data['doc_type'].lower() in valid_types
    
    # Verificar número de documento
    if data['doc_type'] == 'decreto':
        assert data['number'].startswith('DEC-') or data['number'].isdigit()
    
    return True
```

### Paso 4: Guardar en Supabase

```sql
INSERT INTO news_items (title, summary, source, category, published_at, source_url)
VALUES (:title, :summary, 'BOLETIN_OFICIAL', :category, :published_at, :url);
```

---

## 4. Selectores CSS (Firecrawl)

```yaml
selectors:
  articles_list: "div.contenido-articulo, div.item-boletin"
  title: "h2.titulo, h3.titulo"
  summary: "p.resumen, div.extracto"
  date: "span.fecha, time"
  doc_type: "span.tipo-norma"
```

---

## 5. Categorización Automática

| Palabras Clave | Categoría |
|----------------|-----------|
| decreto, presidente | Decreto |
| resolución, ministerio | Resolución |
| disposición | Disposición |
| aviso, licitación | Aviso Oficial |

---

## 6. Errores Comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Captcha | Detección de bot | Usar Exa como alternativa |
| PDF no accesible | Link roto | Registrar como pendiente |
| Sin publicaciones | Día feriado | Verificar, puede ser correcto |

---

## 7. Contacto Boletín Oficial

- **Web:** https://www.boletinoficial.gob.ar/
- **Teléfono:** +54 11 4349-2100
- **Email:** boletinoficial@boletinoficial.gob.ar

---

*Última actualización: 2026-02-19*
