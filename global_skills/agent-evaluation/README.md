# README: agent-evaluation

## Descripción
Framework de LLMOps para evaluación estadística y benchmarking de agentes de IA. Permite certificar la fiabilidad de prompts antes de enviarlos a producción.

## Requisitos
- **Python 3.10+**
- **Ollama** (con modelo target, ej: `llama3.1:8b`)

## Instalación
```bash
pip install -r requirements.txt
```

## Uso Rápido
1. **Ejecutar Eval:** `python scripts/main.py run mi_suite.yaml --runs 5`
2. **Generar Reporte:** `python scripts/main.py report results.json -o report.md`

## Formato de Suite (YAML)
```yaml
name: "mi-test"
tests:
  - name: "test-1"
    prompt: "..."
    invariants:
      - contains: "expected"
      - is_json: true
```
