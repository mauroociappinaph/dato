# Guía de Skills - DATO

> **Última actualización:** 2026-02-13  
> **Estado:** Skills activas y disponibles

---

## Skills por Categoría

### 🎨 UX/UI/Design

| Skill | Ubicación | Uso Principal |
|-------|-----------|---------------|
| `brand-identity/` | `@global_skills/brand-identity/` | Design tokens, voice/tone standards |
| `visual-learning-engine/` | `@global_skills/visual-learning-engine/` | Análisis de screenshots, patrones UI/UX |
| `google-slides-visual-creator/` | `@global_skills/google-slides-visual-creator/` | Generación de contenido visual |
| `ux-researcher/` | `@global_skills/ux-researcher/` | **NUEVO** - Research, usability testing |
| `ui-component-library/` | `@global_skills/ui-component-library/` | **NUEVO** - Componentes reutilizables |
| `design-system/` | `@global_skills/design-system/` | **NUEVO** - Sistema de diseño completo |

### 💻 Frontend

| Skill | Ubicación | Uso Principal |
|-------|-----------|---------------|
| `typescript-pro/` | `@global_skills/typescript-pro/` | Type safety, advanced patterns |
| `code-modularity-architect/` | `@global_skills/code-modularity-architect/` | DRY/SRP, code splitting |
| `codebase-navigator/` | `@global_skills/codebase-navigator/` | Contexto mínimo, surgical read, dependency tracing |
| `react-expert/` | `@global_skills/react-expert/` | **NUEVO** - React/Next.js avanzado |
| `telegram-mini-app/` | `@global_skills/telegram-mini-app/` | Mini apps para Telegram |
| `seo-technical-master/` | `@global_skills/seo-technical-master/` | SEO técnico |

### 🔧 Backend

| Skill | Ubicación | Uso Principal |
|-------|-----------|---------------|
| `nodejs-backend/` | `@global_skills/nodejs-backend/` | **NUEVO** - NestJS, API design |
| `infrastructure-core/` | `@global_skills/infrastructure-core/` | Supabase, Redis |
| `api-endpoint-tester/` | `@global_skills/api-endpoint-tester/` | Smoke testing |
| `database-performance-tuner/` | `@global_skills/database-performance-tuner/` | Query optimization |
| `security-auditor/` | `@global_skills/security-auditor/` | OWASP, hardening |
| `error-handling-patterns/` | `@global_skills/error-handling-patterns/` | **NUEVO** - Resilient architecture, Circuit Breakers, Result Types |

### 🤖 AI/Agents

| Skill | Ubicación | Uso Principal |
|-------|-----------|---------------|
| `ai-engineer/` | `@global_skills/ai-engineer/` | LLM integration, RAG |
| `rag-implementation/` | `@global_skills/rag-implementation/` | Vector search, embeddings |
| `langgraph-director/` | `@global_skills/langgraph-director/` | Multi-agent orchestration |
| `prompt-optimizer-dspy/` | `@global_skills/prompt-optimizer-dspy/` | Prompt engineering |
| `token-accountant/` | `@global_skills/token-accountant/` | **NUEVO** - Token usage tracking, cost optimization, budget enforcement |

### 💰 Financial/Ops

| Skill | Ubicación | Uso Principal |
|-------|-----------|---------------|
| `financial-controller/` | `@global_skills/financial-controller/` | **NUEVO** - Token budget audit, cost efficiency |
| `pricing-strategy/` | `@global_skills/pricing-strategy/` | **NUEVO** - SaaS pricing, tier structure |
| `cost-control/` | `@global_skills/cost-control/` | **NUEVO** - Rate limiting, fallback policies, quota tracking |
| `cost-monitor/` | `@global_skills/cost-monitor/` | **NUEVO** - Real-time cost tracking, dashboard API |

### 🛠️ Quality & Debugging

| Skill | Ubicación | Uso Principal |
|-------|-----------|---------------|
| `data-quality-frameworks/` | `@global_skills/data-quality-frameworks/` | **NUEVO** - Data validation, contracts, quality checks |
| `debugging-strategies/` | `@global_skills/debugging-strategies/` | **NUEVO** - RCA, systematic debugging, profiling |
| `devops-troubleshooter/` | `@global_skills/devops-troubleshooter/` | **NUEVO** - Incident response, observability, K8s debugging |
| `detect-duplicate-files/` | `@global_skills/detect-duplicate-files/` | **NUEVO** - Duplicate file detection, code deduplication |
| `docs-technical-writer/` | `@global_skills/docs-technical-writer/` | **NUEVO** - Technical documentation, API docs, README generation |
| `code-review-excellence/` | `@global_skills/code-review-excellence/` | **NUEVO** - Auto-review MCP tools, checklists, feedback constructivo |
| `self-correction-pilot/` | `@global_skills/self-correction-pilot/` | **NUEVO** - RCA automático, aplica fixes, verifica (FASE 2+) |
| `post-mortem-memory/` | `@global_skills/post-mortem-memory/` | **NUEVO** - Extrae lecciones, sube a Vector Memory (FASE 2+) |
| `compliance-legal-sentinel/` | `@global_skills/compliance-legal-sentinel/` | **NUEVO** - GDPR, EU AI Act, PII Guard, Compliance-Gate |

### 📦 Git & GitHub

| Skill | Ubicación | Uso Principal |
|-------|-----------|---------------|
| `git-advanced-workflows/` | `@global_skills/git-advanced-workflows/` | Rebase, cherry-pick, bisect, worktrees |
| `git-flow-sentinel/` | `@global_skills/git-flow-sentinel/` | Branch protection, PR policies |
| `git-workflow-hardener/` | `@global_skills/git-workflow-hardener/` | Husky, hooks, commitlint |

---

### 📋 Task Execution

| Skill | Ubicación | Uso Principal |
|-------|-----------|---------------|
| `task-prompt-engineer/` | `@global_skills/task-prompt-engineer/` | Task decomposition, prompt engineering for execution |
| `asynchronous-jules-helper/` | `@global_skills/asynchronous-jules-helper/` | Delegar tareas pesadas a Jules (background) |

---

## Cómo Usar las Skills

### En TASK.md

Cada tarea tiene una línea `**Skills:**` que indica qué skills usar:

```markdown
#### 1.6 UI Components ⏳
**Skills:** `@global_skills/ui-component-library/`, `@global_skills/design-system/`, `@global_skills/brand-identity/`
```

### Invocación Directa

Para invocar una skill durante el desarrollo:

```
Usa @global_skills/react-expert/ para optimizar el componente FeedCard
```

### Crear Nuevas Skills

Usa `@global_skills/gemini-skill-creator/`:

```
Dude CREATE [nombre-skill] (descripción opcional)
```

---

## Skills Creadas para DATO

Las siguientes skills fueron creadas específicamente para cubrir las necesidades del proyecto:

### 1. ux-researcher/
**Propósito:** User research y usability testing  
**Cuándo usar:** Antes de diseñar nuevas features, validar hipótesis de usuario  
**Tareas relacionadas:** 1.6 UI Components, 1.7 Páginas

### 2. ui-component-library/
**Propósito:** Arquitectura de componentes reutilizables  
**Cuándo usar:** Crear FeedCard, VerificationBadge, ClaimCard, IndicatorCard  
**Tareas relacionadas:** 1.6 UI Components, 3.4 Dashboard B2B

### 3. react-expert/
**Propósito:** Patrones avanzados de React/Next.js  
**Cuándo usar:** Server Components, state management, performance  
**Tareas relacionadas:** 1.5 Next.js Frontend, 1.7 Páginas

### 4. nodejs-backend/
**Propósito:** Arquitectura backend con NestJS  
**Cuándo usar:** AuthModule, ClaimsModule, VerificationsModule  
**Tareas relacionadas:** 1.1 NestJS Backend, 2.2 Agent 2

### 5. design-system/
**Propósito:** Sistema de diseño completo  
**Cuándo usar:** Definir tokens, documentar componentes, theming  
**Tareas relacionadas:** 1.6 UI Components, docs/brand/BRAND.md

### 6. error-handling-patterns/
**Propósito:** Arquitectura resiliente y manejo de errores  
**Cuándo usar:** Circuit Breakers, Result Types, retries, fallbacks  
**Tareas relacionadas:** 0.2.4 Otros, 1.1 NestJS Backend, todas las APIs

### 7. token-accountant/
**Propósito:** Tracking de uso de tokens LLM  
**Cuándo usar:** Cost optimization, budget enforcement, ROI analysis  
**Tareas relacionadas:** Todos los agentes, 0.4.1 GitHub Actions, 3.1 Billing

### 8. financial-controller/
**Propósito:** Auditoría de budget de tokens  
**Cuándo usar:** Cost efficiency analysis, budget audits  
**Tareas relacionadas:** 0.4.1 GitHub Actions, 3.2 Planes

### 9. pricing-strategy/
**Propósito:** Estrategia de pricing SaaS  
**Cuándo usar:** Definir tier structure, pricing models  
**Tareas relacionadas:** 3.1 Billing, 3.2 Planes

### 10. cost-control/
**Propósito:** Control de costos y rate limiting  
**Cuándo usar:** Rate limiting, fallback policies, quota tracking  
**Tareas relacionadas:** 0.4.1 GitHub Actions, todos los agentes

### 11. cost-monitor/
**Propósito:** Monitoreo de costos en tiempo real  
**Cuándo usar:** Dashboard API, SQLite histórico, alerts  
**Tareas relacionadas:** 1.8 Deploy, 3.4 Dashboard B2B

### 12. data-quality-frameworks/
**Propósito:** Validación y calidad de datos  
**Cuándo usar:** Data contracts, quality checks, validation  
**Tareas relacionadas:** 0.5.2 Base de Datos, 1.2 Agent 1, 1.3 Agent 3

### 13. debugging-strategies/
**Propósito:** Debugging sistemático  
**Cuándo usar:** RCA, profiling, debug logging  
**Tareas relacionadas:** 1.1 Backend, 1.4 Agent 4, 3.3 Agent 7

### 14. devops-troubleshooter/
**Propósito:** Troubleshooting de DevOps  
**Cuándo usar:** Incident response, observability, K8s debugging  
**Tareas relacionadas:** 1.8 Deploy, 2.4 Push Notifications, 3.4 Dashboard

### 15. git-advanced-workflows/
**Propósito:** Workflows avanzados de Git  
**Cuándo usar:** Rebase, cherry-pick, bisect, worktrees  
**Tareas relacionadas:** 0.1 Git & Repositorio

### 16. git-flow-sentinel/
**Propósito:** Protección de branches y PRs  
**Cuándo usar:** Branch protection, PR policies  
**Tareas relacionadas:** 0.1 Git & Repositorio

### 17. git-workflow-hardener/
**Propósito:** Hardening de Git workflow  
**Cuándo usar:** Husky, hooks, commitlint  
**Tareas relacionadas:** 0.2.5 Git Hooks (Husky)

### 18. asynchronous-jules-helper/
**Propósito:** Delegar tareas pesadas a Jules  
**Cuándo usar:** Refactors grandes, bulk docs, migraciones  
**Tareas relacionadas:** Tareas diferidas

### 19. code-review-excellence/
**Propósito:** Revisión automatizada de código  
**Cuándo usar:** Auto-review con MCP tools, checklists estructurados, feedback constructivo  
**Tareas relacionadas:** 0.4.1 GitHub Actions (CI)

### 20. codebase-navigator/
**Propósito:** Navegación quirúrgica del código  
**Cuándo usar:** Contexto mínimo, surgical read (offset/limit), dependency tracing  
**Tareas relacionadas:** 0.3 Estructura, 1.1 Backend, 1.6 Frontend

### 21. self-correction-pilot/
**Propósito:** Diagnóstico y fix automático  
**Cuándo usar:** FASE 2+ - RCA automático, aplica patches, verifica, registra en Vector Memory  
**Tareas relacionadas:** 2.5 CI Troubleshooting Avanzado

### 22. post-mortem-memory/
**Propósito:** Capitalización del conocimiento  
**Cuándo usar:** FASE 2+ - Extraer lecciones, subir a Pinecone, prevenir recurrencia  
**Tareas relacionadas:** 2.5 CI Troubleshooting Avanzado

### 23. compliance-legal-sentinel/
**Propósito:** Auditor de cumplimiento legal y privacidad  
**Cuándo usar:** GDPR, EU AI Act, PII Guard, Compliance-Gate antes de features con pagos/PII  
**Tareas relacionadas:** 0.5.3 Auth, 2.1 Autenticación, 3.1 Billing

---

## Jerarquía de Skills

```
gemini-skill-creator/ (Master)
├── ux-researcher/
│   └── inherited_from: [visual-learning-engine]
├── ui-component-library/
│   └── inherited_from: [code-modularity-architect, brand-identity]
├── react-expert/
│   └── inherited_from: [typescript-pro]
├── nodejs-backend/
│   └── inherited_from: [typescript-pro, infrastructure-core]
├── design-system/
│   └── inherited_from: [brand-identity, ui-component-library]
├── error-handling-patterns/
│   └── inherited_from: [typescript-pro, infrastructure-core]
├── token-accountant/
│   └── inherited_from: [ai-engineer]
├── financial-controller/
│   └── inherited_from: [token-accountant]
├── pricing-strategy/
│   └── inherited_from: [financial-controller]
├── cost-control/
│   └── inherited_from: [token-accountant, infrastructure-core]
├── cost-monitor/
│   └── inherited_from: [cost-control, infrastructure-core]
├── data-quality-frameworks/
│   └── inherited_from: [typescript-pro, infrastructure-core]
├── codebase-navigator/
│   └── inherited_from: [typescript-pro]
├── debugging-strategies/
│   └── inherited_from: [typescript-pro]
├── devops-troubleshooter/
│   └── inherited_from: [debugging-strategies, infrastructure-core]
├── github-master/
│   └── inherited_from: [typescript-pro]
├── git-advanced-workflows/
│   └── inherited_from: [github-master]
├── git-flow-sentinel/
│   └── inherited_from: [git-advanced-workflows]
├── git-workflow-hardener/
│   └── inherited_from: [git-flow-sentinel]
├── code-review-excellence/
│   └── inherited_from: [code-reviewer, code-modularity-architect]
├── self-correction-pilot/
│   └── inherited_from: [debugging-strategies, sequential-thinking]
├── post-mortem-memory/
│   └── inherited_from: [self-correction-pilot]
└── compliance-legal-sentinel/
    └── inherited_from: [security-auditor, infrastructure-core]
```

---

*Documento generado usando @global_skills/gemini-skill-creator/*
