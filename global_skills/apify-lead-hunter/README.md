# README: lead-hunter (Sovereign Edition)

## Descripción
Pipeline soberano de generación de leads. Busca prospectos en DuckDuckGo, los califica con IA y los guarda en Supabase. Todo con coste operativo cero.

## Requisitos
- **Python 3.10+**
- **Ollama** (con `llama3.1:8b`)
- **Supabase** (credenciales en env)

## Instalación
```bash
pip install -r requirements.txt
```

## Uso Rápido
- **Pipeline Completo:** `python scripts/main.py pipeline "Nicho Ciudad" --max 10`
- **Solo Hunt:** `python scripts/main.py hunt "B2B Bilbao"`
- **Solo Score:** `python scripts/main.py score leads.json`

## Variables de Entorno
```bash
SUPABASE_URL=...
SUPABASE_ANON_KEY=...
```
