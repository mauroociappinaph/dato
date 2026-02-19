# SOP-002: Ejecución de Agentes - DATO

> Ver también: [Especificaciones Técnicas de Agentes](../specs/agents.md)

## Configuración de LLM Providers

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

### 2.1 Agent 1: Data Collector

#### Propósito
Recolectar datos de fuentes oficiales (INDEC, BCRA, Boletín Oficial) cada 1-3 horas.

#### Ejecución Manual

```bash
# Via Kilo CLI
kilo run "Collect economic data from INDEC"

# Via script directo
cd apps/api
pnpm run agents:collector --source=INDEC
pnpm run agents:collector --source=BCRA
pnpm run agents:collector --source=all
```

#### Ejecución Automática (Cron)

```yaml
# Configuración en apps/api/src/cron/collector.cron.ts

jobs:
  - name: indec-daily
    schedule: "0 9 * * *"    # 9:00 AM diario
    source: INDEC
    
  - name: bcra-hourly
    schedule: "0 */3 * * *"  # Cada 3 horas
    source: BCRA
    
  - name: boletin-daily
    schedule: "0 10 * * *"   # 10:00 AM diario
    source: BOLETIN_OFICIAL
```

#### Output Esperado

```json
{
  "agent": "collector",
  "timestamp": "2026-02-13T09:00:00Z",
  "source": "INDEC",
  "data": [
    {
      "indicator": "inflacion",
      "value": 4.2,
      "period": "2026-01",
      "url": "https://indec.gob.ar/..."
    }
  ],
  "status": "success"
}
```

#### Manejo de Errores

```
Si INDEC no responde:
1. Reintentar 3 veces con backoff (5s, 15s, 45s)
2. Si persiste, usar cache del día anterior
3. Registrar error en logs
4. Notificar via Slack/email si crítico
```

### 2.2 Agent 2: Claim Extractor

#### Propósito
Extraer afirmaciones verificables de discursos y noticias.

#### Input Format

```json
{
  "text": "El presidente anunció: 'La inflación bajó 50% desde que asumimos'",
  "source": "YouTube",
  "speaker": "Presidente",
  "date": "2026-02-13",
  "context": "Discurso en rally político"
}
```

#### Ejecución

```bash
# Via Kilo CLI
kilo run "Extract claims from this text: [texto]"

# Via API
curl -X POST http://localhost:3000/api/v1/agents/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "source": "YouTube"}'
```

#### Output Esperado

```json
{
  "agent": "extractor",
  "claims": [
    {
      "text": "La inflación bajó 50% desde que asumimos",
      "speaker": "Presidente",
      "category": "economy",
      "verifiable": true,
      "confidence": 0.92
    }
  ]
}
```

#### Criterios de Aceptación

- Solo extraer afirmaciones con datos cuantificables
- Ignorar opiniones vagas ("El país va a mejorar")
- Máximo 5 claims por texto
- Confidence mínimo: 0.7

### 2.3 Agent 3: Fact Checker

#### Propósito
Verificar claims contra datos oficiales.

#### Ejecución

```bash
# Via Kilo CLI
kilo run "Verify this claim: [claim]"

# Via API
curl -X POST http://localhost:3000/api/v1/agents/verify \
  -H "Content-Type: application/json" \
  -d '{"claim_id": "abc123"}'
```

#### Confidence Thresholds

| Confidence | Badge | Acción |
|------------|-------|--------|
| ≥ 85% | ✅ Verdadero / ❌ Falso | Publicar directamente |
| 70-84% | ⚠️ Parcialmente verdadero | Publicar con advertencia |
| < 70% | ⚪ Sin datos suficientes | No publicar, esperar más datos |

#### Output Esperado

```json
{
  "agent": "factchecker",
  "claim_id": "abc123",
  "verdict": "FALSO",
  "confidence": 0.89,
  "explanation": "La inflación bajó 12%, no 50%...",
  "sources": [
    {
      "name": "INDEC",
      "url": "https://indec.gob.ar/...",
      "data": {"value": 4.2, "previous": 4.8}
    }
  ]
}
```

### 2.4 Agent 4: Simplifier

#### Propósito
Traducir economía compleja a lenguaje simple.

#### Ejecución

```bash
kilo run "Explain this for a regular person: [dato técnico]"
```

#### Reglas de Output

1. Máximo 3 oraciones
2. Sin tecnicismos sin definir
3. Usar ejemplos numéricos concretos
4. Máximo 150 caracteres por explicación

#### Ejemplo

```
Input:  "Déficit fiscal primario del 2.1% del PBI"
Output: "El Estado gastó más de lo que le entró. 
         Por cada $100 que recibió, gastó $102.10."
```

### 2.5 Agent 5: Publisher

#### Propósito
Distribuir contenido verificado a múltiples canales.

#### Canales Configurados

| Canal | Formato | Frecuencia |
|-------|---------|------------|
| Web App | Card completo | Tiempo real |
| Twitter/X | Tuit 280 chars | 3-5/día |
| Newsletter | Email resumen | Diario 9 AM |
| Telegram | Mensaje corto | Tiempo real |

#### Ejecución

```bash
kilo run "Publish verification abc123 to all channels"

# Canal específico
kilo run "Publish verification abc123 to Twitter"
```

### 2.6 Agent 6: Billing

#### Propósito
Gestionar suscripciones y pagos.

#### Eventos Manejados

| Evento | Acción |
|--------|--------|
| `subscription.created` | Activar Premium, enviar email |
| `subscription.deleted` | Marcar fin de período, enviar email |
| `payment.failed` | Iniciar dunning (3 intentos) |
| `payment.succeeded` | Renovar acceso, actualizar DB |

#### Webhook Stripe

```bash
# Test local
stripe listen --forward-to localhost:3000/webhooks/stripe

# Producción
# Configurar en Stripe Dashboard → Webhooks
```

### 2.7 Agent 7: Learning Loop

#### Propósito
Analizar métricas y mejorar el sistema.

#### Métricas Diarias

| Métrica | Fuente | Umbral |
|---------|--------|--------|
| Usuarios activos | Supabase | Trend up |
| Engagement rate | Analytics | > 30% |
| Fact-check accuracy | Auditoría | > 95% |
| Latencia p95 | APM | < 100ms |

#### Ejecución

```bash
# Reporte diario
kilo run "Generate daily learning report"

# Análisis semanal
kilo run "Analyze weekly trends and suggest improvements"
```

---

