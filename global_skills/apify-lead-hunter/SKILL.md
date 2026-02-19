# Skill: lead-hunter (Sovereign Edition)
**Departamento:** DATA, AI & RESEARCH
**Responsable:** `data-engineer`

## Descripción
Motor soberano de generación de leads. Busca, califica y persiste prospectos de negocio sin dependencias de pago (DuckDuckGo + Ollama + Supabase).

## Stack Soberano
- **Search:** DuckDuckGo LITE (HTTP, sin JS, sin API key)
- **Scoring:** Ollama local `llama3.1:8b` ($0)
- **Persistence:** Supabase (tabla `leads`)
- **Anti-spam:** Deduplicación por URL antes de insertar

## Requisitos
- Internet para búsqueda
- Ollama con `llama3.1:8b` para scoring
- `SUPABASE_URL` y `SUPABASE_ANON_KEY` en env para persistencia
- `pip install requests beautifulsoup4 supabase`

## Uso CLI

```bash
cd global_skills/apify-lead-hunter/scripts

# Solo buscar
python main.py hunt "Agencias inmobiliarias Bilbao" --max 20

# Solo scorear (de archivo o stdin)
python main.py score leads.json
python main.py score leads.json --model llama3.1:8b

# Solo persistir en Supabase
python main.py persist scored_leads.json
python main.py persist scored_leads.json --dry-run

# Pipeline completo: Hunt → Score → Persist
python main.py pipeline "Agencias inmobiliarias Bilbao" --max 10
python main.py pipeline "Software agencies Madrid" --min-score 60 --dry-run
```

## Output Format (JSON)
```json
{
  "status": "completed",
  "query": "Agencias inmobiliarias Bilbao",
  "total_found": 15,
  "qualified": 8,
  "persisted": 6,
  "duplicates_skipped": 2,
  "leads": [{"name": "...", "url": "...", "score": 82, "reasoning": "..."}]
}
```

## Seguridad
- Los leads son deduplicados por URL antes de insertar (anti-spam, mandato de Mauro)
- Scoring local: los datos nunca salen del servidor
- PII scrubbing disponible via `pii_scrubber.py` antes de envío
