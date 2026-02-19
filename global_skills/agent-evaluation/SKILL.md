# Skill: agent-evaluation
**Description:** Statistical and behavioral benchmarking for LLM agents. Certification for Paso 22.

## Stack Soberano
- **LLM Runtime:** Ollama local (`llama3.1:8b`), $0
- **Eval Format:** YAML suites with invariant checkers
- **Output:** JSON results + Markdown reports

## Requisitos
- Ollama corriendo con modelo target (`ollama pull llama3.1:8b`)
- `pip install requests pyyaml`

## Uso CLI

```bash
cd global_skills/agent-evaluation/scripts

# Ejecutar eval suite
python main.py run sample_eval.yaml
python main.py run sample_eval.yaml --runs 10 -o results.json

# Generar reporte legible
python main.py report results.json
python main.py report results.json -o report.md
```

## Formato YAML de Eval Suite
```yaml
name: "my-eval"
model: "llama3.1:8b"
runs: 5
tests:
  - name: "test_name"
    prompt: "Your prompt here"
    invariants:
      - contains: "expected text"
      - not_contains: "unwanted text"
      - max_length: 500
      - min_length: 10
      - matches_regex: "\\d+"
      - is_json: true
```

## Invariantes Soportadas
| Invariante | Descripción |
|---|---|
| `contains` | Response must contain text (case-insensitive) |
| `not_contains` | Response must NOT contain text |
| `max_length` | Max character length |
| `min_length` | Min character length |
| `matches_regex` | Must match regex pattern |
| `is_json` | Must be valid JSON |

## Core Patterns
- **Statistical Evaluation:** Run tests multiple times to analyze distribution.
- **Behavioral Contract:** Define invariants that the agent must never violate.
- **Adversarial Testing:** Attempt to break the agent's logic.

## Anti-Patterns
- ❌ Single-run testing.
- ❌ Only happy path tests.
- ❌ Output string matching (prefer semantic or logic checks).
