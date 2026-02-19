# README: master-rag-2026

## Descripción
Motor de Búsqueda Semántica sobre bases de conocimiento locales. Indexa documentos en Redis Vectors y permite consultas en lenguaje natural usando Ollama.

## Requisitos
- **Python 3.10+**
- **Ollama** (con modelo `nomic-embed-text`)
- **Redis 8.0+**

## Instalación
```bash
pip install -r requirements.txt
```

## Uso Rápido
1. **Indexar:** `python scripts/main.py index /ruta/a/docs`
2. **Consultar:** `python scripts/main.py query "¿Propuesta de valor?"`
3. **Estadísticas:** `python scripts/main.py stats`

## Docker
```bash
docker build -t dude-rag .
docker run --net=host dude-rag index /docs
```
