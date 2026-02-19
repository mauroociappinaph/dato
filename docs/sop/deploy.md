# SOP-005: Deploy - DATO

> **⚠️ NOTA:** Las operaciones de GitHub (crear releases, tags, etc.) deben realizarse mediante **GitHub MCP (Kilo CLI)**.

## SOP-005: Deploy

### 5.1 Pre-Deploy Checklist

```
□ Todos los tests pasan
□ Lint sin errores
□ Typecheck sin errores
□ Variables de entorno configuradas
□ Secrets actualizados en Vercel/Railway
□ Migraciones de DB listas
□ Backup de DB realizado
□ Changelog actualizado
```

### 5.2 Deploy Frontend (Vercel)

```bash
# 1. Build local (verificar)
pnpm build:web

# 2. Deploy preview
vercel --env-file=.env.production

# 3. Si OK, deploy a producción
vercel --prod

# 4. Verificar
curl https://dato.ar/api/health
```

### 5.3 Deploy Backend (Railway)

```bash
# 1. Build local
pnpm build:api

# 2. Deploy
railway up

# 3. Verificar logs
railway logs

# 4. Health check
curl https://api.dato.ar/health
```

### 5.4 Variables de Entorno

```bash
# Frontend (Vercel)
NEXT_PUBLIC_SUPABASE_URL=xxx
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
NEXT_PUBLIC_API_URL=xxx

# Backend (Railway)
SUPABASE_URL=xxx
SUPABASE_SERVICE_KEY=xxx
DATABASE_URL=xxx
REDIS_URL=xxx

# LLM Providers
GROQ_API_KEY=xxx
NVIDIA_API_KEY=xxx
MISTRAL_API_KEY=xxx
OPENROUTER_API_KEY=xxx

# MCP Servers
PINECONE_API_KEY=xxx
FIRECRAWL_API_KEY=xxx
EXA_API_KEY=xxx

# Payments
STRIPE_SECRET_KEY=xxx
STRIPE_WEBHOOK_SECRET=xxx
MERCADO_PAGO_ACCESS_TOKEN=xxx
```

### 5.5 Post-Deploy Verification

```
□ Homepage carga (< 3s)
□ API health responde
□ Login funciona
□ Feed carga datos
□ Fact-check funciona
□ Pagos test mode OK
□ Logs sin errores críticos
□ Monitoring activo (Sentry)
```

### 5.6 Cost Dashboard API

#### Setup

```bash
# El cost dashboard está integrado en apps/api/src/costs/

# Endpoints disponibles:
# GET  /api/v1/costs/daily        - Costos diarios
# GET  /api/v1/costs/by-agent     - Costos por agente
# GET  /api/v1/costs/by-model     - Costos por modelo LLM
# GET  /api/v1/costs/tokens       - Uso de tokens
```

#### Deploy Instructions

```bash
# 1. Verificar migraciones de tablas de costos
cd apps/api
pnpm run migration:check

# 2. Las tablas de costos se crean automáticamente:
#    - cost_logs
#    - token_usage
#    - daily_cost_summary

# 3. Configurar cron para agregación diaria
# Ya incluido en apps/api/src/cron/costs.cron.ts
```

#### Dashboard Access

```
# Admin dashboard
https://dato.ar/admin/costs

# Métricas disponibles:
├── Costo total por día/semana/mes
├── Tokens por agente
├── Costo por modelo LLM
├── ROI por verificación
└── Proyección mensual
```

### 5.7 Token Usage Dashboard

#### Setup

```bash
# El token usage dashboard monitorea uso en tiempo real
# Ubicación: apps/api/src/monitoring/tokens.ts

# Endpoints:
# GET  /api/v1/monitoring/tokens/realtime
# GET  /api/v1/monitoring/tokens/user/:id
# GET  /api/v1/monitoring/tokens/alerts
```

#### Dashboard Features

```
Token Usage Monitoring
│
├── Real-time token counter
│   ├── Por usuario
│   ├── Por agente
│   └── Por endpoint
│
├── Alertas
│   ├── Token budget 80% usado
│   ├── Usuario cerca de límite
│   └── Costo inusual
│
└── Reportes
    ├── Diario: resumen por email
    ├── Semanal: reporte detallado
    └── Mensual: análisis de tendencias
```

### 5.8 Post-Deploy Runbook

#### Health Checks

```bash
# 1. Verificar servicios
curl https://dato.ar/api/health
curl https://api.dato.ar/health

# 2. Verificar DB
curl https://api.dato.ar/health/db

# 3. Verificar Redis
curl https://api.dato.ar/health/redis

# 4. Verificar LLM providers
curl https://api.dato.ar/health/llm
```

#### Troubleshooting Common Issues

| Problema | Síntoma | Solución |
|----------|---------|----------|
| API no responde | 502/503 errors | Revisar logs: `railway logs`, reiniciar servicio |
| DB connection failed | Timeout queries | Verificar `DATABASE_URL`, revisar pool connections |
| Auth falla | 401 errors | Verificar `SUPABASE_URL` y `SUPABASE_ANON_KEY` |
| LLM timeout | Fact-check lento | Verificar API keys, reducir `max_tokens` |
| Token limit excedido | Requests bloqueados | Verificar `token_usage` table, reiniciar contadores |
| Stripe webhook falla | Pagos no procesados | Verificar `STRIPE_WEBHOOK_SECRET`, revisar Stripe Dashboard |

#### Rollback Procedure

```bash
# Vercel
vercel rollback dato-web --yes

# Railway
railway rollback

# Verificar
curl https://dato.ar/api/health
```

### 5.9 Incident Alerts

#### Configuración de Alertas

```yaml
# apps/api/src/config/alerts.yaml

alerts:
  critical:
    - name: api_down
      condition: health_check_failed
      channels: [slack, email, sms]
      
    - name: db_connection_lost
      condition: db_ping_timeout > 30s
      channels: [slack, email]
      
    - name: payment_failure_spike
      condition: payment_failures > 5 in 1h
      channels: [slack, email]

  warning:
    - name: high_latency
      condition: p95_latency > 1000ms
      channels: [slack]
      
    - name: token_budget_alert
      condition: daily_tokens > 80% budget
      channels: [slack]
      
    - name: error_rate_spike
      condition: error_rate > 5%
      channels: [slack]
```

#### Slack Integration

```bash
# Configurar webhook de Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx

# Canales:
#   #dato-alerts-critical - Alertas críticas
#   #dato-alerts-warning  - Alertas de advertencia
#   #dato-deploy         - Notificaciones de deploy
```

#### Email Alerts

```bash
# Configurar Resend para alertas
RESEND_API_KEY=xxx
ALERT_EMAIL_RECIPIENTS=team@dato.ar

# Templates:
#   - alert_critical.html
#   - alert_warning.html
#   - deploy_notification.html
```

---

