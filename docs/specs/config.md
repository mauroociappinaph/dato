## 8. Configuration

### 8.1 Environment Variables

```bash
# ============================================================================
# APPLICATION
# ============================================================================
NODE_ENV=development
PORT=3000
API_URL=http://localhost:3000
WEB_URL=http://localhost:3001

# ============================================================================
# DATABASE (Supabase)
# ============================================================================
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxx
SUPABASE_SERVICE_KEY=xxx
DATABASE_URL=postgresql://xxx

# ============================================================================
# CACHE (Redis)
# ============================================================================
REDIS_URL=redis://localhost:6379
REDIS_PASSWORD=

# ============================================================================
# LLM PROVIDERS
# ============================================================================
# Default provider
LLM_PROVIDER=groq

# Groq (default, fast)
GROQ_API_KEY=gsk_xxx
GROQ_BASE_URL=https://api.groq.com/openai/v1

# NVIDIA NIM (complex tasks)
NVIDIA_API_KEY=nvapi-xxx
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1

# Mistral (reasoning)
MISTRAL_API_KEY=xxx
MISTRAL_BASE_URL=https://api.mistral.ai/v1

# OpenRouter (fallback)
OPENROUTER_API_KEY=sk-or-xxx
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1

# ============================================================================
# VECTOR DB (Pinecone)
# ============================================================================
PINECONE_API_KEY=xxx
PINECONE_ENVIRONMENT=xxx
PINECONE_INDEX=dato-central-brain

# ============================================================================
# MCP SERVERS
# ============================================================================
# Firecrawl (scraping)
FIRECRAWL_API_KEY=xxx

# Exa (search)
EXA_API_KEY=xxx

# LangSmith (tracing)
LANGSMITH_API_KEY=xxx
LANGSMITH_PROJECT=dato

# ============================================================================
# PAYMENTS
# ============================================================================
# Stripe
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Mercado Pago (LATAM)
MERCADO_PAGO_ACCESS_TOKEN=xxx
MERCADO_PAGO_WEBHOOK_SECRET=xxx

# ============================================================================
# NOTIFICATIONS
# ============================================================================
# Push (OneSignal/Firebase)
ONESIGNAL_APP_ID=xxx
ONESIGNAL_API_KEY=xxx

# Email (Resend)
RESEND_API_KEY=xxx
EMAIL_FROM=noreply@dato.ar

# Telegram
TELEGRAM_BOT_TOKEN=xxx

# ============================================================================
# ANALYTICS & MONITORING
# ============================================================================
# Sentry
SENTRY_DSN=xxx

# PostHog
POSTHOG_KEY=xxx
POSTHOG_HOST=https://app.posthog.com

# ============================================================================
# SECURITY
# ============================================================================
JWT_SECRET=xxx
ENCRYPTION_KEY=xxx

# ============================================================================
# RATE LIMITS
# ============================================================================
RATE_LIMIT_FREE=60
RATE_LIMIT_PREMIUM=300
RATE_LIMIT_PROFESSIONAL=1000
```

### 8.2 LLM Model Configuration

```yaml
# config/llm.yaml

providers:
  groq:
    models:
      - id: llama-3.1-8b-instant
        use: [collector, publisher, billing]
        max_tokens: 500
        temperature: 0.1
        cost_per_1m_input: 0.10
        cost_per_1m_output: 0.10
        
      - id: llama-3.3-70b-versatile
        use: [simplifier]
        max_tokens: 500
        temperature: 0.3
        cost_per_1m_input: 0.10
        cost_per_1m_output: 0.10

  nvidia:
    models:
      - id: meta/llama-3.1-70b-instruct
        use: [extractor]
        max_tokens: 2000
        temperature: 0.2
        cost_per_1m_input: 0.20
        cost_per_1m_output: 0.60

  mistral:
    models:
      - id: mistral-large-latest
        use: [factchecker]
        max_tokens: 1500
        temperature: 0.1
        cost_per_1m_input: 0.30
        cost_per_1m_output: 0.90
        
      - id: mistral-medium-latest
        use: [learning]
        max_tokens: 2000
        temperature: 0.4
        cost_per_1m_input: 0.15
        cost_per_1m_output: 0.45

  openrouter:
    models:
      - id: any
        use: [fallback]
        cost_per_1m_input: varies
        cost_per_1m_output: varies

fallback_chain:
  - groq
  - mistral
  - nvidia
  - openrouter

retry_config:
  max_retries: 3
  backoff_multiplier: 2
  initial_delay_ms: 1000
```

### 8.3 Feature Flags

```yaml
# config/features.yaml

features:
  # Core features
  feed:
    enabled: true
    cache_ttl_seconds: 300
    
  fact_checking:
    enabled: true
    auto_publish: false
    min_confidence: 0.85
    
  search:
    enabled: true
    vector_search: true
    
  # Premium features
  alerts:
    enabled: true
    max_free: 0
    max_premium: 10
    max_professional: -1 # unlimited
    
  api_access:
    enabled: true
    plans: [professional]
    
  reports:
    enabled: true
    plans: [professional]
    formats: [csv, pdf]
    
  dashboard:
    enabled: true
    plans: [professional]
    
  # Experimental
  youtube_transcription:
    enabled: false
    
  whatsapp_bot:
    enabled: false
    
  browser_extension:
    enabled: false
```

---


---

## 9. Git Hooks Configuration (Husky)

### 9.1 Husky Setup

```bash
# Instalación
pnpm add -D husky
npx husky init

# Estructura
.husky/
├── pre-commit      # Lint + Typecheck
├── commit-msg      # Conventional commits
└── pre-push        # Tests (opcional)
```

### 9.2 Pre-commit Hook

```bash
#!/usr/bin/env sh
# .husky/pre-commit

echo "🔍 Running pre-commit checks..."

# Lint
pnpm lint
if [ $? -ne 0 ]; then
  echo "❌ Lint failed"
  exit 1
fi

# Typecheck
pnpm typecheck
if [ $? -ne 0 ]; then
  echo "❌ Typecheck failed"
  exit 1
fi

# Check for large files (>300 lines)
LARGE_FILES=$(find . -name "*.ts" -o -name "*.tsx" | xargs wc -l | awk '$1 > 300 {print $2}')
if [ -n "$LARGE_FILES" ]; then
  echo "⚠️  Warning: Files exceeding 300 lines:"
  echo "$LARGE_FILES"
  # Uncomment to enforce:
  # exit 1
fi

echo "✅ Pre-commit checks passed"
```

### 9.3 Commit-msg Hook (Commitlint)

```bash
#!/usr/bin/env sh
# .husky/commit-msg

npx --no -- commitlint --edit $1
```

### 9.4 Commitlint Config

```javascript
// commitlint.config.js
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'test', 'chore'],
    ],
    'scope-enum': [
      2,
      'always',
      [
        'web',      // Frontend
        'api',      // Backend
        'agents',   // AI Agents
        'types',    // Shared types
        'ui',       // Shared components
        'docs',     // Documentation
        'ci',       // CI/CD
      ],
    ],
    'subject-max-length': [2, 'always', 72],
  },
};
```

---

## 10. Code Standards Configuration

### 10.1 The 300 Rule

**Implementación via script:**

```bash
# scripts/check-line-count.sh
#!/bin/bash

MAX_LINES=300
VIOLATIONS=0

for file in $(find . -name "*.ts" -o -name "*.tsx" | grep -v node_modules); do
  LINES=$(wc -l < "$file")
  if [ $LINES -gt $MAX_LINES ]; then
    echo "⚠️  $file: $LINES lines (max: $MAX_LINES)"
    VIOLATIONS=$((VIOLATIONS + 1))
  fi
done

if [ $VIOLATIONS -gt 0 ]; then
  echo "❌ $VIOLATIONS files exceed 300 lines"
  exit 1
fi

echo "✅ All files under 300 lines"
```

**Agregar a CI:**

```yaml
# .github/workflows/ci.yml
- name: Check file sizes
  run: ./scripts/check-line-count.sh
```

### 10.2 Barrel File Enforcement

**Estructura obligatoria:**

```
packages/*/src/
├── index.ts              # REQUIRED - exporta todo
├── moduleA/
│   ├── index.ts          # REQUIRED - barrel local
│   └── ModuleA.ts
└── moduleB/
    ├── index.ts          # REQUIRED - barrel local
    └── ModuleB.ts
```

### 10.3 SRP Checklist

**Antes de cada PR, verificar:**

| Componente | Pregunta | Acción si NO |
|------------|----------|--------------|
| Componente React | ¿Hace una sola cosa visual? | Extraer sub-componentes |
| Custom Hook | ¿Maneja una sola lógica? | Dividir en hooks más pequeños |
| Service (Backend) | ¿Un dominio? | Separar en servicios |
| Archivo | ¿< 300 líneas? | Dividir según seams |

---

## 11. State Management (Zustand) Configuration

### 11.1 Stores Structure

```
apps/web/src/stores/
├── authStore.ts       # User, login, logout
├── feedStore.ts       # Feed items, loading
├── searchStore.ts     # Query, results, filters
├── uiStore.ts         # Modals, theme, notifications
└── index.ts           # Barrel file
```

### 11.2 Store Template

```typescript
// Template para nuevos stores
import { create } from 'zustand';
import { persist, devtools } from 'zustand/middleware';

interface StoreState {
  // State
  data: Type | null;
  isLoading: boolean;
  error: string | null;
  
  // Actions
  setData: (data: Type) => void;
  reset: () => void;
}

const initialState = {
  data: null,
  isLoading: false,
  error: null,
};

export const useStore = create<StoreState>()(
  devtools(
    persist(
      (set) => ({
        ...initialState,
        
        setData: (data) => set({ data }),
        reset: () => set(initialState),
      }),
      { name: 'store-name' }
    )
  )
);
```

### 11.3 Usage Rules

| Regla | Ejemplo |
|-------|---------|
| Selectores específicos | `useStore((s) => s.data)` |
| No suscribirse a todo el store | ❌ `const store = useStore()` |
| Persist solo para datos serializables | ✅ User, preferences |
| No persist para UI state | ❌ modals, loading |
