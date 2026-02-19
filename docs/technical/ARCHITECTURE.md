# Architecture - DATO

## System Overview

DATO is a political intelligence platform powered by 7 autonomous AI agents that collect, verify, simplify, and distribute political and economic information for Argentina.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DATO SYSTEM                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐              │
│  │ Agent 1  │───▶│ Agent 2  │───▶│ Agent 3  │───▶│ Agent 4  │              │
│  │Collector │    │ Extractor│    │FactCheck │    │Simplifier│              │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘              │
│       │                                                   │                │
│       │              ┌──────────┐                         │                │
│       └─────────────▶│ Agent 5  │◀────────────────────────┘                │
│                      │Publisher │                                          │
│                      └──────────┘                                          │
│                           │                                                │
│       ┌───────────────────┼───────────────────┐                            │
│       ▼                   ▼                   ▼                            │
│  ┌──────────┐       ┌──────────┐        ┌──────────┐                       │
│  │   Web    │       │  Mobile  │        │  API     │                       │
│  │  (Next)  │       │  (React) │        │ (Nest)   │                       │
│  └──────────┘       └──────────┘        └──────────┘                       │
│                                              │                              │
│                      ┌──────────┐            │                              │
│                      │ Agent 6  │◀───────────┘                              │
│                      │ Billing  │                                          │
│                      └──────────┘                                          │
│                           │                                                │
│                      ┌──────────┐                                          │
│                      │ Agent 7  │                                          │
│                      │ Learning │                                          │
│                      └──────────┘                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## LLM Providers

DATO utiliza múltiples proveedores de IA para optimizar costos, velocidad y calidad:

### Proveedores Configurados

| Proveedor | API Endpoint | Uso Principal |
|-----------|--------------|---------------|
| **Groq** | api.groq.com | Inferencia ultra-rápida |
| **NVIDIA NIM** | integrate.api.nvidia.com | Tareas complejas en GPU |
| **Mistral AI** | api.mistral.ai | Razonamiento profundo |
| **OpenRouter** | openrouter.ai | Acceso multi-modelo |

### Configuración

```env
# Default provider
LLM_PROVIDER=groq

# NVIDIA NIM
NVIDIA_API_KEY=nvapi-xxx
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1

# Mistral AI
MISTRAL_API_KEY=xxx
MISTRAL_BASE_URL=https://api.mistral.ai/v1

# Groq
GROQ_API_KEY=gsk_xxx
GROQ_BASE_URL=https://api.groq.com/openai/v1

# OpenRouter
OPENROUTER_API_KEY=sk-or-xxx
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
```

### Modelos por Agente

| Agente | Proveedor | Modelo | Razón |
|--------|-----------|--------|-------|
| Agent 1: Data Collector | Groq | llama-3.1-8b-instant | Velocidad, bajo costo |
| Agent 2: Claim Extractor | NVIDIA | meta/llama-3.1-70b-instruct | Precisión en extracción |
| Agent 3: Fact Checker | Mistral | mistral-large-latest | Razonamiento profundo |
| Agent 4: Simplifier | Groq | llama-3.3-70b-versatile | Balance velocidad/calidad |
| Agent 5: Publisher | Groq | llama-3.1-8b-instant | Velocidad de generación |
| Agent 6: Billing | Groq | llama-3.1-8b-instant | Tareas simples |
| Agent 7: Learning | Mistral | mistral-medium-latest | Análisis de patrones |

### Estrategia de Fallback

```
Groq (primary) → Mistral (fallback) → NVIDIA (fallback) → OpenRouter (last resort)
```

### Ventajas por Proveedor

**Groq:**
- ✅ Inferencia más rápida del mercado
- ✅ Bajo costo
- ✅ Excelente para tareas simples
- ❌ Menor contexto disponible

**NVIDIA NIM:**
- ✅ Modelos optimizados para GPU
- ✅ Excelente rendimiento
- ✅ Acceso a modelos state-of-the-art
- ❌ Requiere API key específica

**Mistral AI:**
- ✅ Modelos open source
- ✅ Excelente razonamiento
- ✅ Transparente
- ❌ Menos rápido que Groq

**OpenRouter:**
- ✅ Acceso a múltiples modelos
- ✅ Fallback universal
- ✅ Una API para todo
- ❌ Costo variable por modelo

---

## Agent Architecture

### Agent 1: Data Collector

**Purpose:** Fetch raw data from official sources every 1-3 hours.

**LLM:** Groq (llama-3.1-8b-instant) - Velocidad crítica

**Sources:**
- INDEC (inflation, poverty, employment)
- BCRA (dollar rates, reserves, interest rates)
- Senado/Diputados (legislative activity)
- Boletín Oficial (decrees, resolutions)
- NewsData.io (political news)
- YouTube Data API (speeches, interviews)

**MCP Tools:** `firecrawl_scrape`, `exa_search`

**Output:**
```json
{
  "source": "INDEC",
  "type": "inflation",
  "data": { "value": 4.2, "period": "2026-01" },
  "timestamp": "2026-01-15T10:00:00Z"
}
```

---

### Agent 2: Claim Extractor

**Purpose:** Extract verifiable claims from speeches and news.

**LLM:** NVIDIA (meta/llama-3.1-70b-instruct) - Precisión en NER

**Input:** Raw text from news, transcripts, official statements

**MCP Tools:** `sequential_thinking`

**Output:**
```json
{
  "claim": "La inflación bajó 50%",
  "speaker": "Político X",
  "date": "2026-01-14",
  "context": "Discurso en rally político",
  "category": "economy"
}
```

---

### Agent 3: Fact Checker

**Purpose:** Verify claims against official data.

**LLM:** Mistral (mistral-large-latest) - Máximo razonamiento

**MCP Tools:** `pinecone_query`, `supabase_execute_sql`, `redis_get`

**Verification Matrix:**

| Badge | Description |
|-------|-------------|
| ✅ Verdadero | Matches official data |
| ⚠️ Parcial | Contains nuances |
| ❌ Falso | Contradicts data |
| ⚪ Sin datos | Insufficient information |

**Output:**
```json
{
  "claim_id": "abc123",
  "verdict": "PARCIALMENTE_VERDADERO",
  "confidence": 0.85,
  "sources": ["INDEC", "BCRA"],
  "explanation": "La inflación bajó 12%, no 50%..."
}
```

---

### Agent 4: Simplifier

**Purpose:** Translate complex economics to simple language.

**LLM:** Groq (llama-3.3-70b-versatile) - Balance calidad/velocidad

**MCP Tools:** `sequential_thinking`

**Example Transformations:**

| Technical | Simple |
|-----------|--------|
| "Déficit fiscal del 2.1% del PBI" | "El Estado gastó más de lo que le entró. Por cada $100 que recibió, gastó $102." |
| "Tasa de interés del 60% TNA" | "Si pedís un préstamo de $100, vas a devolver $160 en un año." |
| "Reservas netas en descenso" | "El Banco Central tiene cada vez menos dólares para respaldar la moneda." |

---

### Agent 5: Publisher

**Purpose:** Generate and distribute content automatically.

**LLM:** Groq (llama-3.1-8b-instant) - Generación rápida

**MCP Tools:** `github_create_issue`

**Channels:**
- Web app (Next.js)
- Mobile app (React Native)
- Newsletter (email)
- Twitter/X (auto-post)
- Telegram bot
- PDF reports

---

### Agent 6: Billing & Access

**Purpose:** Manage subscriptions and access control.

**LLM:** Groq (llama-3.1-8b-instant) - Tareas simples

**MCP Tools:** `supabase_execute_sql`

**Plans:**
| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | 3 fact-checks/day |
| Premium | $3/month | Unlimited + alerts + history |
| Professional | $50/month | Dashboard + API + reports |

**Payment Processors:** Mercado Pago, Stripe

---

### Agent 7: Learning Loop

**Purpose:** Continuously improve based on user feedback.

**LLM:** Mistral (mistral-medium-latest) - Análisis de patrones

**MCP Tools:** `supabase_execute_sql`, `langsmith_traces`

**Metrics Tracked:**
- Most read topics
- Verification engagement
- User retention
- Conversion rates

---

## Tech Stack

### Backend

| Component | Technology |
|-----------|------------|
| API Framework | NestJS |
| Database | PostgreSQL (via Supabase) |
| Auth | Supabase Auth |
| Storage | Supabase Storage |
| Queue | Bull/BullMQ |
| Cache | Redis |
| AI/LLM | Groq, NVIDIA NIM, Mistral, OpenRouter |

### Frontend

| Component | Technology |
|-----------|------------|
| Web | Next.js 14 |
| State | Zustand |
| Styling | Tailwind CSS |
| Charts | Recharts |
| Mobile | React Native |

### Infrastructure

| Component | Technology |
|-----------|------------|
| Hosting | Vercel (frontend) + Railway (backend) |
| CI/CD | GitHub Actions |
| Monitoring | Sentry |
| Analytics | PostHog |
| AI Tracing | LangSmith |

---

## Database Schema

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  plan TEXT DEFAULT 'free',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Claims
CREATE TABLE claims (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  claim_text TEXT NOT NULL,
  speaker TEXT,
  date DATE,
  context TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Verifications
CREATE TABLE verifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  claim_id UUID REFERENCES claims(id),
  verdict TEXT NOT NULL,
  confidence DECIMAL(3,2),
  sources JSONB,
  explanation TEXT,
  llm_provider TEXT,
  llm_model TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Economic Data
CREATE TABLE economic_data (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  source TEXT NOT NULL,
  indicator TEXT NOT NULL,
  value DECIMAL(10,4),
  period DATE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- LLM Usage Tracking
CREATE TABLE llm_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider TEXT NOT NULL,
  model TEXT NOT NULL,
  agent TEXT NOT NULL,
  tokens_input INT,
  tokens_output INT,
  cost_usd DECIMAL(10,6),
  latency_ms INT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Endpoints

### Public

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/feed` | Daily summary |
| GET | `/api/claims/:id` | Claim + verification |
| GET | `/api/search?q=` | Search claims |
| GET | `/api/indicators` | Current economic indicators |

### Protected (Premium)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/history` | Full verification history |
| POST | `/api/alerts` | Create custom alert |
| GET | `/api/reports/weekly` | Weekly PDF report |
| GET | `/api/dashboard` | B2B dashboard data |

---

## Architecture Decision Records (ADRs)

### ADR-001: Use Supabase for Backend

**Status:** Accepted

**Context:** Need fast development with auth, database, and storage.

**Decision:** Use Supabase instead of custom PostgreSQL + Auth0 + S3.

**Consequences:**
- ✅ Faster development
- ✅ Built-in auth and real-time
- ❌ Vendor lock-in
- ❌ Limited customization

---

### ADR-002: Multi-LLM Strategy with Groq, NVIDIA, Mistral, OpenRouter

**Status:** Accepted

**Context:** Need reliable, fast, and cost-effective AI for multiple agent tasks.

**Decision:** Use multiple LLM providers with specific roles:
- **Groq** for fast, simple tasks (data collection, publishing, billing)
- **NVIDIA NIM** for complex GPU-optimized tasks (claim extraction)
- **Mistral** for deep reasoning (fact-checking, learning)
- **OpenRouter** as universal fallback

**Consequences:**
- ✅ Cost optimization (use cheapest/fastest per task)
- ✅ Speed optimization (Groq for real-time)
- ✅ Quality optimization (Mistral for complex reasoning)
- ✅ Redundancy (fallback chain)
- ❌ Complexity in prompt management
- ❌ Multiple API keys to manage
- ❌ Variable response formats

---

### ADR-003: Event-Driven Agent Communication

**Status:** Accepted

**Context:** Agents need to communicate asynchronously.

**Decision:** Use event queue (BullMQ) for agent communication.

**Consequences:**
- ✅ Scalability
- ✅ Fault tolerance
- ❌ Debugging complexity

---

### ADR-004: Groq as Default LLM Provider

**Status:** Accepted

**Context:** Need fast inference for most agent tasks.

**Decision:** Set Groq as default LLM provider with fallback to Mistral, NVIDIA, OpenRouter.

**Consequences:**
- ✅ Ultra-fast inference (~100 tokens/sec)
- ✅ Low latency for user-facing features
- ✅ Cost-effective for high-volume tasks
- ❌ Rate limits on free tier
- ❌ Limited model selection

---

## Security Considerations

1. **API Keys:** Stored in environment variables, never in code
2. **Rate Limiting:** 100 req/min for free, 1000 for premium
3. **Input Validation:** All user inputs sanitized
4. **CORS:** Restricted to production domains
5. **CSP:** Strict Content Security Policy on frontend
6. **LLM Costs:** Track per-request costs in `llm_usage` table

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        PRODUCTION                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │   Vercel    │     │   Railway   │     │   Supabase  │   │
│  │  (Frontend) │────▶│  (Backend)  │────▶│  (Database) │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│         │                   │                               │
│         │            ┌──────┴──────┐                        │
│         │            │             │                        │
│         ▼            ▼             ▼                        │
│  ┌─────────────┐  ┌───────┐  ┌──────────────────────┐      │
│  │   Sentry    │  │ Redis │  │    LLM Providers     │      │
│  │ (Monitoring)│  │ (Cache)│  │ Groq | NVIDIA |      │      │
│  └─────────────┘  └───────┘  │ Mistral | OpenRouter │      │
│                              └──────────────────────┘      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## MCP Servers Integration

DATO utiliza **Model Context Protocol (MCP) Servers** para extender capacidades sin escribir código adicional.

### MCP Servers Configurados (Kilo CLI)

#### Estado Actual

```
┌  MCP Servers - DATO
│
●  ✓ supabase           connected
●  ✓ pinecone           connected
●  ✓ firecrawl          connected
●  ✓ exa                connected
●  ✓ github             connected
●  ✓ langsmith          connected
●  ✓ sequential-thinking connected
●  ✓ redis              connected
●  ✓ browserbase        connected
●  ✓ fetch              connected
●  ✓ webmcp             connected
●  ✓ gitmcp             connected
│
└  12 servers activos
```

#### Servidores Críticos

| MCP Server | Propósito | Uso en DATO | Estado |
|------------|-----------|-------------|--------|
| **supabase** | Database + Auth + Storage | DB principal, migraciones | ✅ Connected |
| **pinecone** | Vector Database | RAG para fact-checking | ✅ Connected |
| **firecrawl** | Web Scraping | Scraper INDEC, BCRA | ✅ Connected |
| **exa** | Web Search | Búsqueda noticias | ✅ Connected |
| **github** | GitHub Operations | CI/CD, PRs, Issues, Repos | ✅ Connected |
| **langsmith** | AI Tracing | Debugging agentes | ✅ Connected |
| **sequential-thinking** | Reasoning | Razonamiento IA | ✅ Connected |
| **redis** | Cache | Cache de datos económicos, rate limiting | ✅ Connected |
| **browserbase** | Browser Automation | Scraping dinámico | ✅ Connected |
| **fetch** | HTTP Requests | APIs externas | ✅ Connected |
| **webmcp** | Web MCP Client | Integración usuarios externos | ✅ Connected |
| **gitmcp** | Code Documentation | Evita alucinaciones de código | ✅ Connected |

---

### Configuración de Kilo CLI

#### Archivo de Configuración

**Ubicación:** `~/Desktop/Dato/opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "supabase": {
      "type": "local",
      "command": ["npx", "-y", "@supabase/mcp-server-supabase@latest", "--access-token", "YOUR_TOKEN"]
    },
    "pinecone": {
      "type": "local",
      "command": ["npx", "-y", "@pinecone-database/mcp"],
      "environment": { "PINECONE_API_KEY": "YOUR_KEY" }
    },
    "firecrawl": {
      "type": "local",
      "command": ["npx", "-y", "firecrawl-mcp"],
      "environment": { "FIRECRAWL_API_KEY": "YOUR_KEY" }
    },
    "exa": {
      "type": "local",
      "command": ["npx", "-y", "exa-mcp-server"],
      "environment": { "EXA_API_KEY": "YOUR_KEY" }
    },
    "github": {
      "type": "local",
      "command": ["docker", "run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
      "environment": { "GITHUB_PERSONAL_ACCESS_TOKEN": "YOUR_TOKEN" }
    },
    "langsmith": {
      "type": "local",
      "command": ["/Users/mauroociappina/.local/bin/uvx", "langsmith-mcp-server"],
      "environment": {
        "LANGSMITH_API_KEY": "YOUR_KEY",
        "LANGSMITH_ENDPOINT": "//api.smith.langchain.com"
      }
    },
    "sequential-thinking": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-sequential-thinking"]
    }
  }
}
```

---

### Comandos Kilo CLI

```bash
# Iniciar Kilo en el proyecto
cd ~/Desktop/Dato
kilo

# Listar MCP servers
kilo mcp list

# Ejecutar con mensaje
kilo run "Analiza inflación del INDEC"

# Iniciar sesión específica
kilo --session <session-id>

# Continuar última sesión
kilo -c
```

---

### Arquitectura con MCP + Multi-LLM

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      DATO + MCP + MULTI-LLM                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         KILO CLI                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │    │
│  │  │   opencode   │  │    kilo      │  │   Session    │               │    │
│  │  │    .json     │  │     mcp      │  │   Manager    │               │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘               │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                       LLM PROVIDERS                                  │    │
│  │                                                                      │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    │    │
│  │  │    Groq    │  │   NVIDIA   │  │  Mistral   │  │ OpenRouter │    │    │
│  │  │   (fast)   │  │   (GPU)    │  │  (reason)  │  │  (multi)   │    │    │
│  │  │            │  │            │  │            │  │            │    │    │
│  │  │ Agent 1    │  │ Agent 2    │  │ Agent 3    │  │  Fallback  │    │    │
│  │  │ Agent 4    │  │            │  │ Agent 7    │  │            │    │    │
│  │  │ Agent 5    │  │            │  │            │  │            │    │    │
│  │  │ Agent 6    │  │            │  │            │  │            │    │    │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        MCP SERVERS                                   │    │
│  │                                                                      │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐    │    │
│  │  │  firecrawl │  │   exa      │  │  pinecone  │  │  supabase  │    │    │
│  │  │  (scrape)  │  │  (search)  │  │  (vectors) │  │   (db)     │    │    │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘    │    │
│  │                                                                      │    │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐                    │    │
│  │  │  github    │  │ langsmith  │  │ sequential │                    │    │
│  │  │   (ci)     │  │  (trace)   │  │  thinking  │                    │    │
│  │  └────────────┘  └────────────┘  └────────────┘                    │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                          7 AGENTS                                    │    │
│  │                                                                      │    │
│  │  Agent 1 ──▶ Agent 2 ──▶ Agent 3 ──▶ Agent 4 ──▶ Agent 5           │    │
│  │  Collector    Extractor   FactCheck   Simplifier   Publisher        │    │
│  │    (Groq)      (NVIDIA)   (Mistral)    (Groq)       (Groq)          │    │
│  │                                               │                      │    │
│  │                            Agent 6 ◀──────────┘                      │    │
│  │                             Billing                                   │    │
│  │                             (Groq)                                    │    │
│  │                               │                                      │    │
│  │                            Agent 7                                   │    │
│  │                            Learning                                  │    │
│  │                           (Mistral)                                  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

### Herramientas MCP por Agente

| Agente | LLM Provider | MCP Tools | Descripción |
|--------|--------------|-----------|-------------|
| Agent 1: Data Collector | Groq | `firecrawl_scrape`, `exa_search` | Scrapear INDEC, BCRA, buscar noticias |
| Agent 2: Claim Extractor | NVIDIA | `sequential_thinking` | Extraer afirmaciones verificables |
| Agent 3: Fact Checker | Mistral | `pinecone_query`, `supabase_execute_sql` | Verificar contra datos históricos |
| Agent 4: Simplifier | Groq | `sequential_thinking` | Traducir a lenguaje simple |
| Agent 5: Publisher | Groq | `github_create_issue` | Publicar contenido |
| Agent 6: Billing | Groq | `supabase_execute_sql` | Gestionar suscripciones |
| Agent 7: Learning | Mistral | `langsmith_traces`, `supabase_execute_sql` | Analizar métricas |

---

### Ejemplos de Uso MCP

#### Firecrawl - Scraping INDEC

```bash
# En Kilo CLI:
"Usa firecrawl para scrapear https://www.indec.gob.ar/ y extraer datos de inflación"
```

#### Pinecone - Búsqueda Vectorial

```bash
# En Kilo CLI:
"Busca en pinecone fact-checks anteriores sobre inflación"
```

#### Supabase - Query Database

```bash
# En Kilo CLI:
"Ejecuta en supabase: SELECT * FROM claims WHERE verdict = 'FALSE' LIMIT 10"
```

#### Exa - Búsqueda Web

```bash
# En Kilo CLI:
"Busca con exa noticias recientes sobre dólar en Argentina"
```

#### GitHub - Operaciones de Repositorio

> **⚠️ OBLIGATORIO:** Todas las acciones de GitHub en este proyecto se realizan mediante GitHub MCP (Kilo CLI).

```bash
# En Kilo CLI:

# Crear repositorio
"Crear repositorio dato en GitHub con descripción 'Political intelligence platform'"

# Crear issue
"Crea un issue en GitHub titled: 'Bug en fact-checking' con labels ['bug', 'high-priority']"

# Crear pull request
"Crear pull request desde feature/nueva-funcionalidad a main con título 'Add new feature'"

# Listar PRs abiertos
"Lista los pull requests abiertos en el repositorio"

# Buscar código
"Busca en el código del repositorio: 'pinecone'"

# Crear branch
"Crear branch feature/mejora-agentes desde main"

# Ver commits recientes
"Lista los últimos 10 commits del repositorio"
```

---

### Supabase Projects Disponibles

| Proyecto | Ref | Estado | Uso Potencial |
|----------|-----|--------|---------------|
| MathQuest | fmcgnrjkyecppxquijvj | ACTIVE | ✅ Usar para DATO |
| Hecho En Casa | qkhjtrcuddhyhluitgrn | INACTIVE | - |
| padel | ukxkvkznhpspxmdjmqcy | INACTIVE | - |

**Recomendación:** Crear nuevo proyecto "DATO" o usar MathQuest activo.

---

### ADR-005: Use MCP Servers for Infrastructure

**Status:** Accepted

**Context:** Need scraping, vector search, web search, and AI tracing without building custom solutions.

**Decision:** Use MCP servers via Kilo CLI instead of custom implementations:
- Scraping → firecrawl
- Web Search → exa
- Vector DB → pinecone
- Database → supabase
- Tracing → langsmith
- CI/CD → github

**Consequences:**
- ✅ Zero infrastructure code
- ✅ Pre-configured and ready
- ✅ Automatic updates via npx
- ✅ Unified interface via Kilo CLI
- ❌ External dependencies
- ❌ Limited customization

---

### ADR-006: Use Kilo CLI as Primary Interface

**Status:** Accepted

**Context:** Need a unified CLI for running agents and MCP servers.

**Decision:** Use Kilo CLI with opencode.json configuration for:
- MCP server management
- Session management
- Agent orchestration
- Multi-provider LLM support

**Consequences:**
- ✅ Single configuration file
- ✅ Built-in MCP support
- ✅ Session persistence
- ✅ Multi-model support
- ❌ Learning curve for new tool

---

## Redis Setup

### Instalación (macOS)

```bash
# Instalar Redis
brew install redis

# Iniciar Redis en background
redis-server --daemonize yes

# Verificar conexión
redis-cli ping
# Output: PONG
```

### Uso en DATO

Redis se usa para:
- Cache de datos económicos (inflación, dólar)
- Cola de mensajes para agentes
- Rate limiting
- Session storage

### Comandos Útiles

```bash
# Verificar estado
redis-cli ping

# Ver todas las keys
redis-cli KEYS "*"

# Limpiar cache
redis-cli FLUSHDB

# Ver info
redis-cli INFO
```

---

## Development Workflow

### Iniciar Desarrollo

```bash
# 1. Ir al proyecto
cd ~/Desktop/Dato

# 2. Verificar MCP servers
kilo mcp list

# 3. Iniciar Kilo
kilo

# 4. O con mensaje directo
kilo run "Analiza el roadmap y sugiere mejoras"
```

### Flujo de Trabajo

```
1. Escribir código/consulta
        ↓
2. Kilo CLI procesa con MCP servers
        ↓
3. MCP servers ejecutan (scrape, query, search)
        ↓
4. LLM Provider procesa (Groq/NVIDIA/Mistral/OpenRouter)
        ↓
5. Resultados retornan al agente
        ↓
6. Output guardado en Supabase
        ↓
7. Tracing en LangSmith
```

---

## Cost Optimization

### LLM Cost Comparison (per 1M tokens)

| Provider | Input Cost | Output Cost | Best For |
|----------|------------|-------------|----------|
| Groq | $0.10 | $0.10 | High volume, simple tasks |
| NVIDIA NIM | $0.20 | $0.60 | Complex GPU tasks |
| Mistral | $0.30 | $0.90 | Deep reasoning |
| OpenRouter | Varies | Varies | Fallback |

### Cost Tracking

```sql
-- Track LLM costs per request
INSERT INTO llm_usage (provider, model, agent, tokens_input, tokens_output, cost_usd, latency_ms)
VALUES ('groq', 'llama-3.1-8b-instant', 'collector', 500, 200, 0.00007, 150);
```

### Cost Optimization Strategy

1. **Use Groq for 70% of tasks** (fast, cheap)
2. **Use Mistral for 20%** (complex reasoning)
3. **Use NVIDIA for 10%** (specialized tasks)
4. **Use OpenRouter only as fallback**
