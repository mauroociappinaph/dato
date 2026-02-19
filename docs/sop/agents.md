# SOP-002: Ejecución de Agentes - DATO

> **Última actualización:** 2026-02-19
> **Versión:** 2.0
>
> Ver también: [Especificaciones Técnicas de Agentes](../specs/agents.md)

---

## 2.0 Handoff Protocol

### Flujo de Agentes

```
Agent 1          Agent 2           Agent 3           Agent 4          Agent 5
Collector   →    Extractor    →    Fact Checker →   Simplifier  →   Publisher
    │               │                 │                 │               │
    ▼               ▼                 ▼                 ▼               ▼
 datos brutos   claims extraídos  verificaciones   explicación     publicado
```

---

## 2.1 Checklist de Handoff

### Agent 1 → Agent 2 (Collector → Extractor)

```
□ Datos recolectados guardados en DB
□ source_url documentado para cada dato
□ Timestamp de recolección registrado
□ Formato de output válido:
  {
    "data": [...],
    "source": "INDEC|BCRA|BOLETIN_OFICIAL",
    "collected_at": "ISO8601"
  }
```

### Agent 2 → Agent 3 (Extractor → Fact Checker)

```
□ Claims extraídos con confidence ≥ 0.7
□ Speaker identificado
□ Categoría asignada
□ Texto original preservado
□ Formato de output válido:
  {
    "claims": [
      {
        "text": "...",
        "speaker": "...",
        "category": "economy|politics|social|international",
        "confidence": 0.0-1.0
      }
    ]
  }
```

### Agent 3 → Agent 4 (Fact Checker → Simplifier)

```
□ Veredicto asignado (uno de 4)
□ Confidence calculado
□ Fuentes citadas con links
□ Explicación técnica generada
□ Formato de output válido:
  {
    "verdict": "VERDADERO|FALSO|PARCIALMENTE_VERDADERO|SIN_DATOS",
    "confidence": 0.0-1.0,
    "explanation": "texto técnico",
    "sources": [...]
  }
```

### Agent 4 → Agent 5 (Simplifier → Publisher)

```
□ Explicación simple generada (≤100 palabras)
□ Lenguaje accesible verificado
□ Badge asignado
□ Formato de output válido:
  {
    "simple_explanation": "...",
    "badge": "✅|⚠️|❌|⚪"
  }
```

---

## 2.2 Edge Cases

### ¿Qué pasa si Agent 2 extrae 0 claims?

```
ACCION:
1. Registrar el texto como "sin claims verificables"
2. Marcar como OPINIÓN si el texto es subjetivo
3. No continuar a Agent 3
4. Loggear para análisis posterior

OUTPUT:
{
  "claims": [],
  "reason": "no_verifiable_claims",
  "suggested_action": "skip_factcheck"
}
```

### ¿Qué pasa si Agent 3 no encuentra datos?

```
ACCION:
1. Asignar veredicto: SIN_DATOS
2. Confidence: 0.0
3. Listar fuentes consultadas (aunque vacías)
4. Sugerir fuentes alternativas si las hay

OUTPUT:
{
  "verdict": "SIN_DATOS",
  "confidence": 0.0,
  "explanation": "No se encontraron datos oficiales para verificar esta afirmación.",
  "sources_consulted": ["INDEC", "BCRA", "Boletín Oficial"],
  "suggested_sources": ["MIN_ECONOMIA", "WORLD_BANK"]
}
```

### ¿Qué pasa si Agent 4 falla en simplificar?

```
ACCION:
1. Usar template genérico como fallback
2. Mantener explicación técnica original
3. Marcar como "requiere revisión manual"

FALLBACK TEMPLATE:
"No pudimos simplificar este dato automáticamente. 
Consulta la explicación técnica o revisa las fuentes originales."

OUTPUT:
{
  "simple_explanation": "[template genérico]",
  "fallback_used": true,
  "requires_manual_review": true
}
```

---

## 2.3 Formato JSON de Output por Agente

### Agent 1: Data Collector

```json
{
  "agent": "agent-1-collector",
  "version": "1.0.0",
  "timestamp": "2026-02-19T09:00:00Z",
  "status": "success|partial|failure",
  "data": [
    {
      "id": "uuid",
      "type": "economic_indicator|news|official_document",
      "source": "INDEC|BCRA|BOLETIN_OFICIAL",
      "source_url": "https://...",
      "collected_at": "ISO8601",
      "content": { ... }
    }
  ],
  "metrics": {
    "items_collected": 5,
    "duration_ms": 1234,
    "retries": 0
  }
}
```

### Agent 2: Claim Extractor

```json
{
  "agent": "agent-2-extractor",
  "version": "1.0.0",
  "timestamp": "2026-02-19T09:05:00Z",
  "status": "success",
  "claims": [
    {
      "id": "uuid",
      "text": "La inflación bajó 50%",
      "speaker": "Presidente",
      "speaker_party": "Partido X",
      "speaker_role": "Presidente",
      "category": "economy",
      "date_said": "2026-02-18",
      "source_type": "speech|interview|social_media|news|official",
      "source_url": "https://...",
      "context": "Discurso en rally",
      "confidence": 0.92,
      "verifiable": true
    }
  ],
  "metrics": {
    "claims_extracted": 3,
    "avg_confidence": 0.89,
    "duration_ms": 2345,
    "llm_tokens": 1500
  }
}
```

### Agent 3: Fact Checker

```json
{
  "agent": "agent-3-factchecker",
  "version": "1.0.0",
  "timestamp": "2026-02-19T09:10:00Z",
  "claim_id": "uuid",
  "status": "verified",
  "verdict": "FALSO",
  "confidence": 0.89,
  "explanation": "Según datos del INDEC, la inflación interanual bajó del 211% al 117%...",
  "simple_explanation": null,
  "sources": [
    {
      "name": "INDEC",
      "url": "https://indec.gob.ar/...",
      "data": {
        "value": 117.0,
        "unit": "%",
        "period": "2024-12"
      }
    }
  ],
  "metrics": {
    "sources_consulted": 3,
    "duration_ms": 4567,
    "llm_tokens": 2500,
    "cost_usd": 0.0023
  }
}
```

### Agent 4: Simplifier

```json
{
  "agent": "agent-4-simplifier",
  "version": "1.0.0",
  "timestamp": "2026-02-19T09:15:00Z",
  "verification_id": "uuid",
  "simple_explanation": "El presidente dijo que la inflación bajó 50%, pero los datos oficiales muestran que bajó 44%.",
  "badge": "❌",
  "reading_level": "easy",
  "word_count": 18,
  "metrics": {
    "duration_ms": 890,
    "llm_tokens": 400
  }
}
```

### Agent 5: Publisher

```json
{
  "agent": "agent-5-publisher",
  "version": "1.0.0",
  "timestamp": "2026-02-19T09:20:00Z",
  "verification_id": "uuid",
  "channels": ["web", "twitter", "telegram"],
  "published": {
    "web": { "url": "https://dato.app/claim/abc", "success": true },
    "twitter": { "tweet_id": "123456", "success": true },
    "telegram": { "message_id": 789, "success": true }
  },
  "metrics": {
    "channels_count": 3,
    "duration_ms": 3456
  }
}
```

---

## 2.4 Configuración de LLM Providers

| Agente | LLM Provider | Modelo | Uso |
|--------|--------------|--------|-----|
| Agent 1: Data Collector | Groq | llama-3.1-8b-instant | Velocidad |
| Agent 2: Claim Extractor | NVIDIA | meta/llama-3.1-70b-instruct | Precisión NER |
| Agent 3: Fact Checker | Mistral | mistral-large-latest | Razonamiento |
| Agent 4: Simplifier | Groq | llama-3.3-70b-versatile | Balance |
| Agent 5: Publisher | Groq | llama-3.1-8b-instant | Generación rápida |
| Agent 6: Billing | Groq | llama-3.1-8b-instant | Tareas simples |
| Agent 7: Learning | Mistral | mistral-medium-latest | Análisis |

---

## 2.5 Ejecución Manual

### Agent 1: Data Collector

```bash
kilo run "Collect economic data from INDEC"
pnpm run agents:collector --source=INDEC
```

### Agent 2: Claim Extractor

```bash
kilo run "Extract claims from this text: [texto]"
curl -X POST http://localhost:3000/api/v1/agents/extract -d '{"text": "..."}'
```

### Agent 3: Fact Checker

```bash
kilo run "Verify this claim: [claim]"
curl -X POST http://localhost:3000/api/v1/agents/verify -d '{"claim_id": "abc"}'
```

### Agent 4: Simplifier

```bash
kilo run "Explain this for a regular person: [dato]"
```

### Agent 5: Publisher

```bash
kilo run "Publish verification abc to all channels"
```

---

## 2.6 Cron Jobs

```yaml
# apps/api/src/cron/agents.cron.ts

jobs:
  - name: collector-indec
    schedule: "0 9 * * *"
    agent: agent-1-collector
    args: { source: INDEC }
    
  - name: collector-bcra
    schedule: "0 */3 * * *"
    agent: agent-1-collector
    args: { source: BCRA }
    
  - name: collector-boletin
    schedule: "0 10 * * *"
    agent: agent-1-collector
    args: { source: BOLETIN_OFICIAL }
```

---

*Fin del documento*
