# Development Guide - DATO

> **Ver también:** [SOP de Desarrollo](../sop/development.md) - Procedimientos operativos

## Prerequisites

> **⚠️ IMPORTANTE:** Antes de comenzar, revisar **FASE 0** en [TASK.md](../../TASK.md) para configuración inicial obligatoria.

- pnpm 8+ (recommended) or npm
- Docker & Docker Compose
- Kilo CLI (`brew install kilo`)
- Redis (`brew install redis`)
- Supabase CLI (optional)
- Git

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/mauroociappina/dato.git
cd dato

# Install dependencies
pnpm install

# Copy environment variables
cp .env.example .env

# Start Redis
redis-server --daemonize yes

# Verify MCP servers
kilo mcp list

# Start development with Kilo CLI
kilo
```

---

## Project Structure

```
dato/
├── apps/
│   ├── web/          # Next.js frontend
│   └── api/          # NestJS backend
├── packages/
│   ├── ui/           # Shared UI components
│   ├── agents/       # AI agents
│   └── types/        # Shared TypeScript types
├── docs/
│   └── archive/      # Original documentation
├── opencode.json     # Kilo CLI + MCP config
├── .env.example
├── README.md
├── PRD.md
├── ARCHITECTURE.md
└── ...
```

---

## Kilo CLI Setup

### Installation

```bash
# Install Kilo CLI
brew install kilo

# Verify installation
kilo --version
```

### Configuration

Create `opencode.json` in the project root:

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
      "command": ["/Users/YOUR_USER/.local/bin/uvx", "langsmith-mcp-server"],
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

### Commands

```bash
# Start Kilo (detects opencode.json automatically)
kilo

# List MCP servers
kilo mcp list

# Run with message
kilo run "Analiza el roadmap"

# Continue last session
kilo -c

# Use specific session
kilo --session <session-id>

# Start web interface
kilo web
```

---

## MCP Servers Usage

### Supabase MCP

```bash
# In Kilo CLI:
"Ejecuta en supabase: SELECT * FROM claims WHERE verdict = 'FALSE' LIMIT 10"

"Crea una migración en supabase para la tabla claims"

"Lista las tablas en supabase"
```

### Pinecone MCP

```bash
# In Kilo CLI:
"Busca en pinecone fact-checks similares a: inflación aumentó"

"Guarda en pinecone este vector con metadata"

"Lista los namespaces en pinecone"
```

### Firecrawl MCP

```bash
# In Kilo CLI:
"Usa firecrawl para scrapear https://www.indec.gob.ar/"

"Extrae datos de inflación de la página del INDEC"

"Busca noticias políticas en medios argentinos"
```

### Exa MCP

```bash
# In Kilo CLI:
"Busca con exa noticias sobre dólar en Argentina"

"Encuentra artículos sobre inflación reciente"

"Busca discursos del presidente sobre economía"
```

### GitHub MCP

> **⚠️ OBLIGATORIO:** Todas las operaciones de GitHub en este proyecto deben realizarse mediante GitHub MCP (Kilo CLI). Esto incluye: crear repositorios, issues, pull requests, branches, commits, búsquedas de código, etc.

**Operaciones disponibles:**

| Acción | Comando Kilo CLI |
|--------|------------------|
| Crear repositorio | `"Crear repositorio dato en GitHub"` |
| Crear issue | `"Crea un issue en GitHub: [descripción]"` |
| Crear PR | `"Crear pull request con título: [título]"` |
| Listar PRs | `"Lista los PRs abiertos en GitHub"` |
| Buscar código | `"Busca en el código del repositorio: [query]"` |
| Crear branch | `"Crear branch feature/nueva-funcionalidad"` |
| Ver commits | `"Lista los commits recientes"` |

**Ejemplos:**

```bash
# Crear issue
kilo run "Crea un issue en GitHub titled: 'Bug en fact-checking' con label 'bug'"

# Crear PR
kilo run "Crear pull request desde feature/nueva-funcionalidad a main"

# Buscar código
kilo run "Busca en GitHub código que contenga 'pinecone'"

# Listar branches
kilo run "Lista las branches del repositorio dato"
```

**⚠️ NO usar:**
- `gh` CLI directamente (usar vía GitHub MCP)
- `git push` directo (usar GitHub MCP para PRs)
- Interfaz web de GitHub para creación de issues/PRs

---

## Environment Variables

See `.env.example` for all required variables.

### Required

```env
# Database
SUPABASE_URL=https://kxdltwdiskmsvhscqndd.supabase.co
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-key

# AI/LLM (FASE 1)
GROQ_API_KEY=gsk_xxx
NVIDIA_API_KEY=nvapi-xxx
MISTRAL_API_KEY=xxx

# External APIs
NEWS_DATA_KEY=xxx
YOUTUBE_API_KEY=xxx

# Auth
JWT_SECRET=your-jwt-secret

# Payments (Phase 3)
MERCADO_PAGO_ACCESS_TOKEN=xxx
# or
STRIPE_SECRET_KEY=xxx
```

---

## Development Workflow

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

Follow the coding standards:
- TypeScript strict mode
- ESLint + Prettier
- Conventional commits

### 3. Run Tests

```bash
# Unit tests
pnpm test

# E2E tests
pnpm test:e2e

# Lint
pnpm lint
```

### 4. Submit PR

```bash
git push origin feature/your-feature-name
```

---

## Agent Development

### Agent Structure

```
packages/agents/
├── src/
│   ├── collector/
│   │   ├── index.ts
│   │   ├── sources/
│   │   │   ├── indec.ts
│   │   │   ├── bcra.ts
│   │   │   └── ...
│   │   └── types.ts
│   ├── extractor/
│   ├── fact-checker/
│   ├── simplifier/
│   ├── publisher/
│   ├── billing/
│   └── learning/
└── package.json
```

### Creating a New Agent

```typescript
// packages/agents/src/collector/index.ts
import { Agent } from '../base';

export class DataCollectorAgent extends Agent {
  async execute(input: CollectorInput): Promise<CollectorOutput> {
    // Use MCP tools via Kilo CLI
    const data = await this.fetchSources();
    return this.processData(data);
  }

  private async fetchSources(): Promise<RawData[]> {
    // Implementation
  }
}
```

### Using MCP Tools in Agents

```typescript
// Example: Agent using firecrawl MCP
async scrapeINDEC(): Promise<EconomicData> {
  // This would be called through Kilo CLI
  // "Usa firecrawl para scrapear INDEC"
}
```

---

## Database Setup

### Local Supabase

```bash
# Start local Supabase
supabase start

# Run migrations
supabase db push

# Seed data
pnpm db:seed
```

### Migrations

```bash
# Create new migration
supabase migration new your_migration_name

# Apply migrations
supabase db push
```

---

## API Development

### NestJS Backend

```bash
# Start API in development
cd apps/api
pnpm dev

# Generate module
nest g module claims
nest g controller claims
nest g service claims
```

### API Structure

```
apps/api/
├── src/
│   ├── modules/
│   │   ├── claims/
│   │   ├── verifications/
│   │   ├── indicators/
│   │   └── users/
│   ├── agents/
│   ├── database/
│   └── main.ts
└── test/
```

---

## Frontend Development

### Next.js App

```bash
# Start frontend
cd apps/web
pnpm dev

# Build for production
pnpm build
```

### Component Structure

```
apps/web/
├── src/
│   ├── app/
│   │   ├── (public)/
│   │   │   ├── page.tsx
│   │   │   └── claims/
│   │   └── (protected)/
│   │       └── dashboard/
│   ├── components/
│   │   ├── ui/
│   │   ├── claims/
│   │   └── layout/
│   ├── lib/
│   │   ├── api.ts
│   │   └── utils.ts
│   └── stores/
│       └── useAuth.ts
└── public/
```

---

## Testing

### Unit Tests

```bash
# All tests
pnpm test

# Specific package
pnpm --filter @dato/agents test

# Watch mode
pnpm test:watch
```

### E2E Tests

```bash
# Setup E2E environment
pnpm test:e2e:setup

# Run E2E tests
pnpm test:e2e
```

---

## Deployment

### Production

```bash
# Build all
pnpm build

# Deploy to Vercel (frontend)
vercel --prod

# Deploy to Railway (backend)
railway up
```

### Staging

```bash
# Deploy to staging
vercel
railway up --environment staging
```

---

## Monitoring

### Logs

```bash
# View backend logs
railway logs

# View Vercel logs
vercel logs
```

### Metrics

- Sentry for error tracking
- PostHog for analytics
- Vercel Analytics for web vitals
- LangSmith for AI tracing (via MCP)

---

## Troubleshooting

### Common Issues

**MCP servers not connecting:**
```bash
# Check Kilo config
kilo mcp list

# Restart Kilo
# Kill any hanging processes
```

**Database connection error:**
```bash
# Check Supabase is running
supabase status

# Reset local database
supabase db reset
```

**API not starting:**
```bash
# Check port availability
lsof -i :3001

# Kill process if needed
kill -9 <PID>
```

**Redis not connecting:**
```bash
# Start Redis
redis-server --daemonize yes

# Verify connection
redis-cli ping
```

---

## Useful Commands

```bash
# Development
pnpm dev              # Start all services
pnpm dev:api          # Start API only
pnpm dev:web          # Start web only

# Database
pnpm db:migrate       # Run migrations
pnpm db:seed          # Seed database
pnpm db:reset         # Reset database

# Code Quality
pnpm lint             # Run ESLint
pnpm format           # Run Prettier
pnpm typecheck        # Run TypeScript check

# Testing
pnpm test             # Unit tests
pnpm test:e2e         # E2E tests
pnpm test:coverage    # Coverage report

# Kilo CLI
kilo                  # Start Kilo
kilo mcp list         # List MCP servers
kilo run "message"    # Run with message
kilo -c               # Continue session
```
