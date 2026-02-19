# ADR-002: Multi-LLM Strategy with Groq, NVIDIA, Mistral, OpenRouter

**Status:** Accepted

**Date:** 2024-02-01

## Context

DATO opera 7 agentes de IA con diferentes necesidades:
- Agent 1 (Collector): Velocidad crítica, alto volumen
- Agent 2 (Extractor): Precisión en NER, tareas complejas
- Agent 3 (Fact Checker): Razonamiento profundo
- Agent 4 (Simplifier): Balance velocidad/calidad
- Agent 5 (Publisher): Generación rápida de contenido
- Agent 6 (Billing): Tareas simples
- Agent 7 (Learning): Análisis de patrones

Necesitamos optimizar costo, velocidad y calidad por tarea.

## Decision

Usar múltiples proveedores de LLM con roles específicos:

| Agente | Proveedor | Modelo |
|--------|-----------|--------|
| Agent 1, 5, 6 | Groq | llama-3.1-8b-instant |
| Agent 2 | NVIDIA NIM | meta/llama-3.1-70b-instruct |
| Agent 3, 7 | Mistral | mistral-large-latest |
| Agent 4 | Groq | llama-3.3-70b-versatile |
| Fallback | OpenRouter | Varios |

### Estrategia de Fallback

```
Groq (primary) → Mistral (fallback) → NVIDIA (fallback) → OpenRouter (last resort)
```

## Consequences

### Positivas

- Optimización de costos (usar más barato/rápido por tarea)
- Optimización de velocidad (Groq para tiempo real)
- Optimización de calidad (Mistral para razonamiento complejo)
- Redundancia (fallback chain)
- No vendor lock-in total

### Negativas

- Complejidad en gestión de prompts
- Múltiples API keys para manejar
- Formatos de respuesta variables
- Diferentes rate limits por proveedor
- Latencia variable

## Cost Comparison (per 1M tokens)

| Provider | Input | Output | Best For |
|----------|-------|--------|----------|
| Groq | $0.10 | $0.10 | High volume, simple |
| NVIDIA NIM | $0.20 | $0.60 | Complex GPU tasks |
| Mistral | $0.30 | $0.90 | Deep reasoning |
| OpenRouter | Varies | Varies | Fallback |

## Related

- ADR-004: Groq as Default LLM Provider
- ADR-005: Use MCP Servers for Infrastructure
