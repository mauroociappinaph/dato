# Agent Specifications - DATO

> **Total Agentes:** 9 (+ 1 Orchestrator opcional en FASE 4)
>
> Ver también: [SOP de Ejecución de Agentes](../sop/agents.md)

## Resumen de Agentes

| # | Agente | Fase | Responsabilidad Principal |
|---|--------|------|---------------------------|
| 0 | Orchestrator | 4 (opcional) | Coordina agentes con branching y paralelismo |
| 1 | Data Collector | 1 | Recolecta datos económicos de fuentes oficiales |
| 2 | Claim Extractor | 1 | Extrae afirmaciones verificables de texto |
| 3 | Fact Checker | 1 | Verifica afirmaciones contra datos oficiales |
| 4 | Simplifier | 1 | Traduce términos técnicos a lenguaje simple |
| 5 | Publisher | 2 | Publica contenido verificado en múltiples canales |
| 6 | Billing | 3 | Gestiona suscripciones y pagos |
| 7 | Learning Loop | 3 | Analiza métricas y sugiere mejoras |
| 8 | Quality Assurance | 3 | Evalúa precisión y detecta drift en accuracy |
| 9 | Growth Engineer | 2 | Optimiza conversión y retención |

---

## 4. Agent Specifications

### 4.1 Agent 1: Data Collector

```yaml
agent:
  id: agent-1
  name: Data Collector
  description: Recolecta datos económicos de fuentes oficiales

input:
  type: object
  required: [sources]
  properties:
    sources:
      type: array
      items:
        type: string
        enum: [INDEC, BCRA, BOLETIN_OFICIAL, MIN_ECONOMIA, WORLD_BANK]
      default: [INDEC, BCRA]
    indicators:
      type: array
      items:
        $ref: '#/types/EconomicIndicator'
      default: all

output:
  type: object
  properties:
    collected:
      type: array
      items:
        $ref: '#/types/EconomicData'
    errors:
      type: array
      items:
        type: object
        properties:
          source:
            type: string
          error:
            type: string

llm_config:
  provider: groq
  model: llama-3.1-8b-instant
  max_tokens: 500
  temperature: 0.1

mcp_tools:
  - firecrawl_scrape
  - exa_search

retry_policy:
  max_retries: 3
  backoff: exponential
  initial_delay_ms: 5000

schedule:
  type: cron
  jobs:
    - name: indec_daily
      expression: "0 9 * * *"
      timezone: America/Argentina/Buenos_Aires
    - name: bcra_hourly
      expression: "0 */3 * * *"
      timezone: America/Argentina/Buenos_Aires

confidence_threshold: null # N/A para este agente
```

### 4.2 Agent 2: Claim Extractor

```yaml
agent:
  id: agent-2
  name: Claim Extractor
  description: Extrae afirmaciones verificables de texto

input:
  type: object
  required: [text]
  properties:
    text:
      type: string
      minLength: 50
      maxLength: 50000
    source_type:
      type: string
      enum: [speech, interview, social_media, news, official]
    speaker:
      type: string
    date:
      type: string
      format: date
    context:
      type: string

output:
  type: object
  required: [claims]
  properties:
    claims:
      type: array
      items:
        type: object
        required: [text, speaker, category, verifiable, confidence]
        properties:
          text:
            type: string
            minLength: 10
            maxLength: 1000
          speaker:
            type: string
          category:
            type: string
            enum: [economy, politics, social, international, other]
          verifiable:
            type: boolean
          confidence:
            type: number
            minimum: 0
            maximum: 1

llm_config:
  provider: nvidia
  model: meta/llama-3.1-70b-instruct
  max_tokens: 2000
  temperature: 0.2

mcp_tools:
  - sequential_thinking

validation_rules:
  - max_claims_per_text: 10
  - min_confidence: 0.5
  - only_verifiable: true

confidence_threshold: 0.7
```

### 4.3 Agent 3: Fact Checker

```yaml
agent:
  id: agent-3
  name: Fact Checker
  description: Verifica afirmaciones contra datos oficiales

input:
  type: object
  required: [claim_id, claim_text, category]
  properties:
    claim_id:
      type: string
      format: uuid
    claim_text:
      type: string
    category:
      type: string
      enum: [economy, politics, social, international, other]

output:
  type: object
  required: [verdict, confidence, explanation, sources]
  properties:
    verdict:
      type: string
      enum: [VERDADERO, FALSO, PARCIALMENTE_VERDADERO, SIN_DATOS]
    confidence:
      type: number
      minimum: 0
      maximum: 1
    explanation:
      type: string
      maxLength: 500
    simple_explanation:
      type: string
      maxLength: 150
    sources:
      type: array
      items:
        type: object
        required: [name, url]
        properties:
          name:
            type: string
          url:
            type: string
            format: uri
          data:
            type: object

llm_config:
  provider: mistral
  model: mistral-large-latest
  max_tokens: 1500
  temperature: 0.1

mcp_tools:
  - pinecone_query
  - supabase_execute_sql
  - redis_get

source_priority:
  - INDEC
  - BCRA
  - Boletin Oficial
  - Senado
  - Diputados
  - Ministerios

confidence_rules:
  VERDADERO:
    min: 0.85
    description: "Datos coinciden exactamente con fuente oficial"
  FALSO:
    min: 0.85
    description: "Datos contradicen fuente oficial"
  PARCIALMENTE_VERDADERO:
    min: 0.70
    max: 0.84
    description: "Coincidencia parcial o falta contexto"
  SIN_DATOS:
    max: 0.69
    description: "No hay datos oficiales disponibles"

confidence_threshold: 0.70
```

### 4.4 Agent 4: Simplifier

```yaml
agent:
  id: agent-4
  name: Simplifier
  description: Traduce términos técnicos a lenguaje simple

input:
  type: object
  required: [text, type]
  properties:
    text:
      type: string
      maxLength: 1000
    type:
      type: string
      enum: [explanation, indicator, claim]

output:
  type: object
  required: [simple_text]
  properties:
    simple_text:
      type: string
      maxLength: 200
    examples:
      type: array
      items:
        type: string
      maxItems: 2
    terms:
      type: array
      items:
        type: object
        properties:
          term:
            type: string
          definition:
            type: string
            maxLength: 50

llm_config:
  provider: groq
  model: llama-3.3-70b-versatile
  max_tokens: 500
  temperature: 0.3

mcp_tools:
  - sequential_thinking

rules:
  max_sentences: 3
  max_characters: 150
  no_technical_terms: true
  use_concrete_examples: true
  use_round_numbers: true

forbidden_terms:
  - PBI
  - IPC
  - déficit fiscal
  - tipo de cambio
  - base monetaria
  - reservas netas

# Si se usan, deben definirse inline
confidence_threshold: null
```

### 4.5 Agent 5: Publisher

```yaml
agent:
  id: agent-5
  name: Publisher
  description: Publica contenido verificado en múltiples canales

input:
  type: object
  required: [verification_id, channels]
  properties:
    verification_id:
      type: string
      format: uuid
    channels:
      type: array
      items:
        type: string
        enum: [web, twitter, telegram, newsletter, api, github_issue]
      default: [web]

output:
  type: object
  properties:
    published:
      type: array
      items:
        type: object
        properties:
          channel:
            type: string
          success:
            type: boolean
          url:
            type: string
          error:
            type: string

llm_config:
  provider: groq
  model: llama-3.1-8b-instant
  max_tokens: 300
  temperature: 0.2

mcp_tools:
  - github_create_issue    # Para crear issues de reportes

channel_formats:
  twitter:
    max_length: 280
    include_hashtags: true
    hashtags: ["#DatoVerificado", "#Argentina"]
  telegram:
    max_length: 500
    include_link: true
  newsletter:
    format: html
    include_image: true
  github_issue:
    # Crear issues de reportes vía GitHub MCP
    labels: ["report", "verified"]
    template: "fact-check-report.md"

rate_limits:
  twitter: 5/day
  telegram: unlimited
  newsletter: 1/day
  github_issue: unlimited

confidence_threshold: null
```

### 4.6 Agent 6: Billing

```yaml
agent:
  id: agent-6
  name: Billing
  description: Gestiona suscripciones y pagos

input:
  type: object
  required: [event, data]
  properties:
    event:
      type: string
      enum:
        - subscription.created
        - subscription.updated
        - subscription.deleted
        - payment.succeeded
        - payment.failed
    data:
      type: object
      properties:
        user_id:
          type: string
          format: uuid
        stripe_customer_id:
          type: string
        stripe_subscription_id:
          type: string
        plan:
          type: string
          enum: [premium, professional]
        amount:
          type: number
        currency:
          type: string
          default: USD

output:
  type: object
  properties:
    success:
      type: boolean
    user:
      $ref: '#/types/User'
    action:
      type: string

llm_config:
  provider: groq
  model: llama-3.1-8b-instant
  max_tokens: 200
  temperature: 0

mcp_tools:
  - supabase_execute_sql
environment_variables:
  - STRIPE_SECRET_KEY

integrations:
  - stripe
  - mercado_pago (future)

dunning:
  max_attempts: 3
  delays_days: [3, 5, 7]
  final_action: downgrade

confidence_threshold: null
```

### 4.7 Agent 7: Learning Loop

```yaml
agent:
  id: agent-7
  name: Learning Loop
  description: Analiza métricas y sugiere mejoras

input:
  type: object
  required: [type]
  properties:
    type:
      type: string
      enum: [daily_report, weekly_analysis, trend_detection]
    date_range:
      type: object
      properties:
        start:
          type: string
          format: date
        end:
          type: string
          format: date

output:
  type: object
  properties:
    insights:
      type: array
      items:
        type: object
        properties:
          type:
            type: string
            enum: [trend, anomaly, opportunity]
          description:
            type: string
          data:
            type: object
    recommendations:
      type: array
      items:
        type: object
        properties:
          priority:
            type: string
            enum: [high, medium, low]
          action:
            type: string
          expected_impact:
            type: string

llm_config:
  provider: mistral
  model: mistral-medium-latest
  max_tokens: 2000
  temperature: 0.4

mcp_tools:
  - langsmith_traces
  - supabase_execute_sql

metrics_tracked:
  - daily_active_users
  - verifications_per_day
  - engagement_rate
  - fact_check_accuracy
  - llm_cost_per_request
  - latency_p95

alerts:
  - metric: fact_check_accuracy
    threshold: 0.95
    operator: less_than
  - metric: latency_p95
    threshold: 5000
    operator: greater_than

confidence_threshold: null
```

### 4.8 Agent 8: Quality Assurance (QA)

```yaml
agent:
  id: agent-8
  name: Quality Assurance
  description: Evalúa precisión de verificaciones y detecta drift en accuracy

input:
  type: object
  required: [action]
  properties:
    action:
      type: string
      enum: [daily_evaluation, drift_detection, prompt_suggestion, weekly_report]
    sample_size:
      type: number
      default: 0.05
      description: Porcentaje de verificaciones a evaluar (default 5%)
    date_range:
      type: object
      properties:
        start:
          type: string
          format: date
        end:
          type: string
          format: date

output:
  type: object
  properties:
    evaluation:
      type: object
      properties:
        sample_size:
          type: number
        accuracy:
          type: number
        precision:
          type: number
        recall:
          type: number
        f1_score:
          type: number
        errors_by_category:
          type: object
    drift_detected:
      type: boolean
    drift_details:
      type: object
      properties:
        previous_accuracy:
          type: number
        current_accuracy:
          type: number
        delta:
          type: number
    prompt_suggestions:
      type: array
      items:
        type: object
        properties:
          category:
            type: string
          issue:
            type: string
          suggestion:
            type: string
          expected_improvement:
            type: string

llm_config:
  provider: mistral
  model: mistral-medium-latest
  max_tokens: 2000
  temperature: 0.3

mcp_tools:
  - supabase_execute_sql
  - sequential_thinking

evaluation_config:
  sample_method: random
  sample_size: 0.05
  ground_truth_source: manual_review
  
  accuracy_thresholds:
    excellent: 0.95
    good: 0.90
    warning: 0.85
    critical: 0.80
    
  drift_thresholds:
    warning: 0.05
    critical: 0.10

schedule:
  daily_evaluation: "0 6 * * *"
  weekly_report: "0 9 * * 1"

alerts:
  - condition: accuracy < 0.90
    action: alert_team
  - condition: accuracy < 0.85
    action: pause_agent_3
  - condition: drift > 0.10
    action: escalate_investigation

confidence_threshold: null
```

### 4.9 Agent 9: Growth Engineer

```yaml
agent:
  id: agent-9
  name: Growth Engineer
  description: Optimiza conversión y retención usando psychology triggers

input:
  type: object
  required: [action]
  properties:
    action:
      type: string
      enum: [analyze_funnel, detect_churn, optimize_pricing, ab_test, weekly_report]
    user_segment:
      type: string
      enum: [all, free, premium, professional, at_risk]
    date_range:
      type: object
      properties:
        start:
          type: string
          format: date
        end:
          type: string
          format: date

output:
  type: object
  properties:
    funnel_analysis:
      type: object
      properties:
        visitors:
          type: number
        signups:
          type: number
        conversions:
          type: number
        conversion_rate:
          type: number
        drop_off_points:
          type: array
          items:
            type: object
    churn_predictions:
      type: array
      items:
        type: object
        properties:
          user_id:
            type: string
          risk_score:
            type: number
          risk_factors:
            type: array
            items:
              type: string
          recommended_action:
            type: string
    psychology_triggers:
      type: object
      properties:
        anchoring:
          type: object
        loss_aversion:
          type: object
        social_proof:
          type: object
        scarcity:
          type: object
    ab_test_results:
      type: object
      properties:
        test_name:
          type: string
        variant_a:
          type: object
        variant_b:
          type: object
        winner:
          type: string
        confidence:
          type: number

llm_config:
  provider: mistral
  model: mistral-medium-latest
  max_tokens: 2000
  temperature: 0.4

mcp_tools:
  - supabase_execute_sql
  - sequential_thinking

funnel_events:
  - page_view
  - signup_started
  - signup_completed
  - verification_requested
  - verification_completed
  - upgrade_viewed
  - upgrade_completed

churn_signals:
  - no_activity_7_days
  - usage_declining
  - viewed_pricing_no_conversion
  - multiple_failed_verifications
  - negative_feedback

psychology_triggers:
  anchoring:
    description: "Mostrar Professional primero para hacer Premium parecer barato"
    enabled: true
  loss_aversion:
    description: "Perdés X verificaciones por no ser Premium"
    enabled: true
  social_proof:
    description: "X usuarios verificaron esto hoy"
    enabled: true
  scarcity:
    description: "Solo quedan 3 verificaciones gratis hoy"
    enabled: true

schedule:
  funnel_analysis: "0 8 * * *"
  churn_detection: "0 9 * * *"
  weekly_report: "0 10 * * 1"

confidence_threshold: null
```

---

