# ADR-004: Groq as Default LLM Provider

**Status:** Accepted

**Date:** 2024-02-05

## Context

La mayoría de tareas de los agentes DATO requieren:
- Alta velocidad de respuesta
- Bajo costo
- Alto volumen de requests

Groq ofrece inferencia ultra-rápida (~100 tokens/sec) con costos muy bajos.

## Decision

Establecer **Groq** como proveedor LLM por defecto con fallback a Mistral → NVIDIA → OpenRouter.

### Modelos por Defecto

| Tipo | Modelo | Uso |
|------|--------|-----|
| Simple/Fast | llama-3.1-8b-instant | Collector, Publisher, Billing |
| Balanced | llama-3.3-70b-versatile | Simplifier |

## Consequences

### Positivas

- Inferencia más rápida del mercado (~100 tokens/sec)
- Latencia baja para features user-facing
- Costo efectivo para tareas de alto volumen
- Simple integration (OpenAI-compatible API)
- Sin rate limits agresivos en tier pago

### Negativas

- Rate limits en free tier
- Selección de modelos limitada
- No soporta modelos propietarios (GPT-4, Claude)
- Potential availability issues (provider nuevo)

## Fallback Strategy

```typescript
async function callLLM(prompt: string) {
  try {
    return await groq.chat(prompt);
  } catch (e) {
    try {
      return await mistral.chat(prompt);
    } catch (e) {
      try {
        return await nvidia.chat(prompt);
      } catch (e) {
        return await openrouter.chat(prompt);
      }
    }
  }
}
```

## Cost Comparison

| Tarea | Groq Cost | Mistral Cost | Savings |
|-------|-----------|--------------|---------|
| 1M tokens simple | $0.10 | $0.30 | 66% |
| 10M tokens/mes | $1 | $3 | 66% |

## Related

- ADR-002: Multi-LLM Strategy
