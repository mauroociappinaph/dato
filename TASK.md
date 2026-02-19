# TASK - DATO

> **Última actualización:** 2026-02-15  
> **Estado:** Documentación completa ✅ | Código: 0% ❌

---

## Estado del Proyecto

| Fase | Estado | Progreso |
|------|--------|----------|
| FASE 0: Setup | ❌ Pendiente | 0/6 secciones (~25 subtasks) |
| **CP0: Checkpoint** | 🔒 Bloqueada | Espera FASE 0 |
| FASE 1: MVP | 🔒 Bloqueada | Espera CP0 (Agentes 1-4) |
| **CP1: Validación** | 🔒 Bloqueada | Espera FASE 1 |
| FASE 2: Growth | 🔒 Bloqueada | Espera CP1 (Agentes 5, 9) |
| **CP2: Validación** | 🔒 Bloqueada | Espera FASE 2 |
| FASE 3: Monetización | 🔒 Bloqueada | Espera CP2 (Agentes 6, 7, 8) |
| **CP3: Validación** | 🔒 Bloqueada | Espera FASE 3 |
| FASE 4: Orchestration | 🔒 Bloqueada | Espera CP3 + triggers (Agent 0) |

**Total Agentes:** 9 (+ 1 opcional Orchestrator)

---

## APIs & MCP Servers Status

**APIs YA configuradas en `opencode.json` (listas para usar):**

| MCP Server | Uso | Estado |
|------------|-----|--------|
| supabase | Database + Auth | ✅ Listo |
| pinecone | Vector DB (RAG) | ✅ Listo |
| firecrawl | Web Scraping | ✅ Listo |
| exa | Web Search | ✅ Listo |
| langsmith | AI Tracing | ✅ Listo |
| browserbase | Browser automation | ✅ Listo |
| github | CI/CD, repos | ✅ Listo |
| redis | Cache | ✅ Listo |
| fetch | HTTP requests | ✅ Listo |
| sequential-thinking | Reasoning | ✅ Listo |
| webmcp | Web MCP client | ✅ Listo |
| gitmcp | Evitar alucinaciones de código | ✅ Listo |
| **pipedream** | Multi-API connector (FASE 2) | 🔒 Pendiente FASE 2 |

**Total MCP Servers:** 12 activos + 1 pendiente (Pipedream)

**APIs FALTANTES (agregar cuando se necesiten):**

| API | Uso | Cuándo agregar |
|-----|-----|----------------|
| Groq API | LLM principal | FASE 1 - Agent 3 |
| Mistral API | LLM fallback | FASE 1 - Agent 4 |
| NVIDIA NIM | LLM alternativo | FASE 1 - Agent 3 |
| Vercel | Deploy frontend | FASE 1 - Deploy |
| Railway | Deploy backend | FASE 1 - Deploy |
| Stripe | Billing internacional | FASE 3 - Billing |
| Mercado Pago | Billing Argentina | FASE 3 - Billing |
| Resend | Email/Newsletter | FASE 2 - Publisher |
| OneSignal/Firebase | Push notifications | FASE 2 - Notifications |

---

## Skills Globales Disponibles

| Skill | Uso | Cuándo invocar |
|-------|-----|----------------|
| `sop-workflow-standardizer` | Crear/actualizar SOPs, estandarizar procedimientos | Al agregar nuevos agentes, workflows, o actualizar `docs/sop/` |

---

## 🔄 Git Flow & Branching Strategy

### Flujo de Trabajo Obligatorio

**IMPORTANTE:** Este flujo debe seguirse para TODA subtask ejecutada via vibe coding.

### Convenciones de Ramas

| Prefijo | Uso | Ejemplo |
|---------|-----|---------|
| `feature/` | Nueva funcionalidad | `feature/dato-0.2-config-files` |
| `fix/` | Corregir subtask que falló | `fix/dato-0.2.3-eslint` |
| `hotfix/` | Urgente en producción | `hotfix/auth-crash` |
| `chore/` | Mantenimiento, docs, deps | `chore/dato-0.2.7-docs` |

### Flujo por Sección (NO por subtask)

**Una rama feature por SECCIÓN completa, NO por subtask individual.**

```
feature/dato-0.2-config-files (una rama para todas las subtasks 0.2.x)
   ├── [0.2.1] → commit "feat(config): add package.json with workspaces"
   ├── [0.2.2] → commit "feat(config): add tsconfig files"
   ├── [0.2.3] → ❌ FALLA → crear fix/dato-0.2.3-eslint
   │                                ├── solucionar
   │                                ├── commit "fix: eslint configuration"
   │                                └── merge a feature/dato-0.2-config-files
   ├── [0.2.3] → commit "feat(config): add eslint and prettier"
   ├── [0.2.4] → commit "feat(config): add error handling"
   ├── [0.2.5] → commit "feat(config): add husky hooks"
   ├── [0.2.6] → commit "feat(config): add modularity setup"
   ├── [0.2.7] → commit "docs: add typedoc and mermaid"
   └── Sección completa → PR a develop → squash & merge → borrar rama
```

### Comandos Git Obligatorios

#### Al INICIAR una sección:
```bash
# Verificar que estás en develop
git checkout develop
git pull origin develop

# Crear rama feature para la sección completa
git checkout -b feature/dato-[SECCIÓN]-[descripción]
# Ejemplo: git checkout -b feature/dato-0.2-config-files
```

#### Al FINALIZAR cada subtask (si pasó):
```bash
git add .
git commit -m "feat([sección]): descripción de la subtask"
# Ejemplo: git commit -m "feat(config): add package.json with workspaces"
```

#### Si una subtask FALLA:
```bash
# NO commitear código roto
# Crear rama fix desde la rama feature actual
git checkout -b fix/dato-[SUBTASK]-[descripción]
# ... solucionar el problema ...
git add .
git commit -m "fix: descripción de la solución"

# Volver a la rama feature y mergear
git checkout feature/dato-[SECCIÓN]-[descripción]
git merge fix/dato-[SUBTASK]-[descripción]

# Borrar rama fix
git branch -d fix/dato-[SUBTASK]-[descripción]
```

#### Al COMPLETAR una sección:
```bash
# Último commit con todos los cambios
git add .
git commit -m "feat([sección]): complete [descripción]"

# Push de la rama feature
git push origin feature/dato-[SECCIÓN]-[descripción]

# Crear Pull Request
gh pr create --base develop --title "feat: [sección] - [descripción]" --body "Completes section [SECCIÓN]"

# Después de merge:
git checkout develop
git pull origin develop

# Borrar rama local
git branch -d feature/dato-[SECCIÓN]-[descripción]

# Borrar rama remota (si quedó)
git push origin --delete feature/dato-[SECCIÓN]-[descripción]
```

### Reglas Obligatorias

| # | Regla | Razón |
|---|-------|-------|
| 1 | **NUNCA** commitear directo a `main` o `develop` | Protección de ramas |
| 2 | **UNA** rama feature por sección | Evitar proliferación de ramas |
| 3 | **SIEMPRE** crear rama desde `develop` actualizado | Evitar conflictos |
| 4 | **NUNCA** commitear código que no pase hooks | Validación automática |
| 5 | **SIEMPRE** usar conventional commits | Historial limpio |
| 6 | **SIEMPRE** squash & merge en PR | Historial limpio en develop |

### Conventional Commits

| Tipo | Uso | Ejemplo |
|------|-----|---------|
| `feat` | Nueva funcionalidad | `feat(config): add husky hooks` |
| `fix` | Corrección de bug | `fix(auth): fix token validation` |
| `docs` | Documentación | `docs: update README` |
| `chore` | Mantenimiento | `chore: update dependencies` |
| `refactor` | Refactor sin cambio funcional | `refactor(api): simplify auth flow` |
| `test` | Agregar/modificar tests | `test(collector): add unit tests` |

### Skills a Usar

| Momento | Skill | Función |
|---------|-------|---------|
| Inicio de subtask | `git-flow-sentinel` | Verificar rama, crear feature branch |
| Antes de commit | `git-workflow-hardener` | Pre-commit hooks, secret scanning |
| Si hay conflicto | `git-advanced-workflows` | Rebase, recovery, merge |

---

## FASE 0: Setup Inicial

> **⚠️ Antes de iniciar una SECCIÓN:** Ver "## 🔄 Git Flow & Branching Strategy" arriba
> - Una rama feature por SECCIÓN completa (ej: `feature/dato-0.2-config-files`)
> - NO crear rama por cada subtask individual

> **Duración estimada:** 5-7 días  
> **Prerrequisito para:** Todo el código

- [ ] **[DOCS] Architecture Decision Records** (Skill: `architecture-decision-historian`)
  - [ ] Crear `docs/adr/` directory
  - [ ] Documentar decisiones arquitectónicas mayores (ADR-001, ADR-002, etc.)

### 0.1 Git & Repositorio ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.1`

**Prioridad:** 🔴 Crítica  
**Dependencias:** Ninguna  
**Tiempo estimado:** 30 min  

**Skills:**
- DevOps: `@global_skills/git-advanced-workflows/`, `@global_skills/git-flow-sentinel/`


- [x] **0.1.1** Crear repositorio en GitHub
  ```bash
  gh repo create dato --public --description "Política argentina verificada con datos reales"
  ```

- [x] **0.1.2** Configurar remote y push inicial
  ```bash
  git remote add origin https://github.com/mauroociappina/dato.git
  git branch -M main
  git push -u origin main
  ```

- [x] **0.1.3** Crear rama `develop`
  ```bash
  git checkout -b develop
  git push -u origin develop
  ```

- [x] **0.1.4** Configurar protección de ramas (GitHub Settings)
  - [x] `main`: Require PR review, Require status checks
  - [x] `develop`: Require PR review (opcional)

- [x] **0.1.5** Configurar branch default en GitHub
  - Settings → Branches → Default: `develop`

---

### 0.2 Config Files (7 subtasks) ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2`

**Prioridad:** 🔴 Crítica  
**Dependencias:** 0.1 Git  
**Tiempo estimado:** 3-4 horas

#### 0.2.1 package.json ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2.1`

**Skills:**
- Core: `@global_skills/typescript-pro/`, `@global_skills/code-modularity-architect/`
- Infra: `@global_skills/monorepo-management/`
- AI: `@global_skills/curacion-de-contenido/`
- Naming: `@global_skills/project-naming-enforcer/`

- [x] Crear `package.json` con pnpm workspaces
  ```json
  {
    "name": "dato",
    "private": true,
    "packageManager": "pnpm@8.15.0",
    "scripts": {
      "dev": "pnpm --filter './apps/*' dev",
      "build": "pnpm --filter './apps/*' build",
      "test": "pnpm --filter './apps/*' test",
      "lint": "pnpm --filter './packages/*' lint"
    }
  }
  ```
- [x] Crear `pnpm-workspace.yaml`
  ```yaml
  packages:
    - 'apps/*'
    - 'packages/*'
  ```
- [x] **✅ Done:** `pnpm install` ejecuta sin errores
- [x] Validar nombres de archivos/carpetas: lowercase, kebab-case (project-naming-enforcer)

#### 0.2.2 tsconfig.json ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2.2`

**Skills:**
- Core: `@global_skills/typescript-pro/`, `@global_skills/code-modularity-architect/`
- Docs: `@global_skills/docs-technical-writer/`

- [x] Crear `tsconfig.json` (base)
- [x] Crear `tsconfig.base.json` (shared config)
- [x] Crear `apps/web/tsconfig.json` (Next.js)
- [x] Crear `apps/api/tsconfig.json` (NestJS)
- [x] **✅ Done:** `pnpm typecheck` ejecuta sin errores

#### 0.2.3 Linting & Formatting ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2.3`

**Skills:**
- Calidad: `@global_skills/code-reviewer/`
- Security: `@global_skills/hardening-auditor/`

- [x] Crear `.eslintrc.json`
- [x] Crear `.prettierrc`
- [x] Crear `.editorconfig`
- [x] **✅ Done:** `pnpm lint` ejecuta sin errores

#### 0.2.4 Otros ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2.4`

**Skills:**
- Calidad: `@global_skills/verification-before-completion/`, `@global_skills/error-handling-patterns/`

- [x] Crear estructura de errores personalizados
- [x] Configurar Result Types para validaciones
- [x] **✅ Done:** Errores importan sin errores y tests pasan

#### 0.2.5 Git Hooks (Husky) ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2.5`

**Skills:**
- DevOps: `@global_skills/git-workflow-hardener/`
- Calidad: `@global_skills/code-reviewer/`, `@global_skills/detect-duplicate-files/`, `@global_skills/code-modularity-architect/`
- AI: `@global_skills/curacion-de-contenido/`

- [x] Instalar Husky
  ```bash
  pnpm add -D husky
  npx husky init
  ```

- [x] Configurar pre-commit hook (validaciones rápidas)
  ```bash
  # .husky/pre-commit
  pnpm lint
  pnpm format:check        # Prettier verification
  pnpm typecheck
  pnpm modularity:check --staged
  gitleaks protect --staged   # Secret scanning
  pnpm audit --audit-level=moderate  # Dependency vulnerabilities (quick)
  ```

- [x] Agregar script format:check en package.json
  ```json
  "format:check": "prettier --check \"**/*.{ts,tsx,js,jsx,json,md}\""
  ```

- [x] Agregar script format (para arreglar):
  ```json
  "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md}\""
  ```

- [x] Configurar pre-push hook (validaciones completas)
  ```bash
  # .husky/pre-push
  pnpm build              # Verify compilation
  pnpm duplicates:check
  pnpm test               # Triggers test-automation-strategist skill
  ```

- [x] Configurar commit-msg hook (conventional commits)
  ```bash
  # .husky/commit-msg
  npx --no -- commitlint --edit $1
  ```

- [x] Configurar post-checkout hook (sync deps al cambiar branch)
  ```bash
  # .husky/post-checkout
  # Ejecutar solo si cambió pnpm-lock.yaml
  if [ "$3" = "1" ] && git diff --name-only HEAD@{1} HEAD | grep -q "pnpm-lock.yaml"; then
    echo "📦 pnpm-lock.yaml cambió, instalando deps..."
    pnpm install
  fi
  ```

- [x] Configurar post-merge hook (sync deps después de merge)
   ```bash
   # .husky/post-merge
   # Ejecutar siempre después de merge si cambió lockfile
   if git diff --name-only ORIG_HEAD HEAD | grep -q "pnpm-lock.yaml"; then
     echo "📦 pnpm-lock.yaml cambió, instalando deps..."
     pnpm install
   fi
   ```
- [x] Sync knowledge files to Pinecone if `packages/agents/` changed (rag-auto-indexer)

- [x] Configurar pre-merge-commit hook (validar antes de merge)
  ```bash
  # .husky/pre-merge-commit
  # Validar antes de merge a main/develop
  pnpm lint
  pnpm test
  ```


- [x] Configurar post-commit hook (cleanup automático)
  ```bash
  # .husky/post-commit
  # Cleanup de cache y archivos temporales
  pnpm store prune
  rm -rf node_modules/.cache 2>/dev/null || true
  echo "🧹 Workspace cleaned after commit"
  ```
  > **Nota:** `docker system prune` NO incluido (requiere Docker corriendo y es lento). Ejecutar manualmente si se necesita.




- [x] Instalar commitlint
  ```bash
  pnpm add -D @commitlint/cli @commitlint/config-conventional
  echo "export default { extends: [@commitlint/config-conventional] }" > commitlint.config.js
  ```

- [x] Instalar Gitleaks: `pnpm add -D gitleaks`
- [x] Configurar secret scanning en pre-commit
- [x] Agregar `.gitignore` para archivos sensibles (.env, .pem, credentials)
- [x] Crear `.nvmrc` (Node 20+)
- [x] Crear `jest.config.js` (base)
- [x] Crear `.env.example` (actualizar con nuevas vars)
- [x] **✅ Done:** Hooks ejecutan sin errores en commit/push de prueba 

> **Skills ejecutadas en hooks:**
> | Hook | Skill/Herramienta | Validación | Frecuencia |
> |------|-------------------|------------|------------|
> | pre-commit | `code-modularity-architect` | Archivos < 300 líneas | Cada commit |
> | pre-commit | `git-workflow-hardener` | Secret scanning (Gitleaks) | Cada commit |
> | pre-commit | `format:check` | Prettier formatting | Cada commit |
> | pre-commit | `pnpm audit` | Dependency vulnerabilities (quick) | Cada commit |
> | pre-push | `detect-duplicate-files` | Código duplicado | Cada push |
> | pre-push | `build` | Compilación correcta | Cada push |
> | pre-push | `test` | Tests pasan | Cada push |
> | pre-commit | `docs-technical-writer` | Implícito via lint (TSDoc) | Cada commit |
> | post-checkout | `pnpm install` | Sync deps si lockfile cambió | Al cambiar branch |
> | post-merge | `pnpm install` | Sync deps post-merge | Después de merge |
> | pre-merge-commit | `lint + test` | Validar antes de merge | Antes de squash merge |
> | post-commit | `environment-cleanup-specialist` | Limpieza automática de cache | Después de commit |

> **🔧 Operaciones avanzadas (manual):** `@global_skills/git-advanced-workflows/`
> | Operación | Comando | Cuándo usar |
> |-----------|---------|-------------|
> | Limpiar historial | `git rebase -i main` | Antes de cada PR |
> | Recuperar trabajo | `git reflog` | Trabajo perdido |
> | Encontrar bug | `git bisect` | Debugging |
> | Forzar push seguro | `git push --force-with-lease` | NUNCA `--force` |
>
> **🤖 Delegación de tareas pesadas (async):** `@global_skills/asynchronous-jules-helper/`
> | Tarea | Comando | Cuándo usar |
> |-------|---------|-------------|
> | Refactor grande | `/jules restructure packages/agents` | Reorganización de módulos |
> | Bulk docs | `/jules generate all API docs` | Documentación masiva |
> | Migración | `/jules migrate tests to vitest` | Cambios跨 módulos |

---

### 0.3 Estructura de Directorios ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.3`

**Prioridad:** 🔴 Crítica  
**Dependencias:** 0.2 package.json  
**Tiempo estimado:** 30 min  

**Skills:**
- Core: `@global_skills/code-modularity-architect/`
- Infra: `@global_skills/monorepo-management/`
- Docs: `@global_skills/codebase-navigator/`

```
dato/
├── apps/
│   ├── web/                 # Next.js frontend
│   │   ├── src/
│   │   ├── public/
│   │   ├── package.json
│   │   └── next.config.js
│   └── api/                 # NestJS backend
│       ├── src/
│       ├── package.json
│       └── nest-cli.json
├── packages/
│   ├── agents/             # 9 AI agents
│   │   ├── src/
│   │   │   ├── agent-0-orchestrator/   # FASE 4 (opcional)
│   │   │   ├── agent-1-collector/
│   │   │   ├── agent-2-extractor/
│   │   │   ├── agent-3-factchecker/
│   │   │   ├── agent-4-simplifier/
│   │   │   ├── agent-5-publisher/
│   │   │   ├── agent-6-billing/
│   │   │   ├── agent-7-learning/
│   │   │   ├── agent-8-qa/             # FASE 3
│   │   │   └── agent-9-growth/         # FASE 2
│   │   └── package.json
│   ├── types/              # Shared TypeScript types
│   │   ├── src/
│   │   └── package.json
│   └── ui/                 # Shared components
│       ├── src/
│       └── package.json
├── tests/
│   ├── e2e/
│   └── integration/
└── docs/                   # ✅ Ya existe
```

- [x] **0.3.1** Crear estructura `apps/`
- [x] **0.3.2** Crear estructura `packages/`
- [x] **0.3.3** Crear estructura `tests/`
- [x] **0.3.4** Inicializar package.json en cada sub-proyecto
- [x] **✅ Done:** Estructura creada y `pnpm install -r` ejecuta sin errores

---

### 0.4 CI/CD ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.4`

**Prioridad:** 🟡 Alta  
**Dependencias:** 0.1 Git, 0.2 Config Files  
**Tiempo estimado:** 3-4 horas

#### 0.4.1 GitHub Actions ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.4.1`

**Skills:**
- DevOps: `@global_skills/github-actions-mechanic/`
- Costos: `@global_skills/financial-controller/`, `@global_skills/token-accountant/`, `@global_skills/cost-control/`
- Calidad: `@global_skills/code-review-excellence/`

- [x] Crear `.github/workflows/ci.yml`
  - Trigger: PR a `main` y `develop`
  - Steps:
    - [x] lint, typecheck, test
    - [x] `pnpm audit --audit-level=high` (dependency vulnerabilities)
    - [ ] Token budget check
    - [ ] Rate limit enforcement
    - [ ] **Code Review Excellence** (Skill: `code-review-excellence`)
      - Análisis automatizado con MCP static tools
      - Checklist: Security (Safe 7), Performance, Architecture (SRP/DRY)
      - Genera comentario estructurado en PR por severidad
      - Aplica técnica "Improved Sandwich" para feedback constructivo
    - [ ] **Blast Radius Analysis** ( Skill: `blast-radius-analyst`)
      - Analiza archivos modificados en el PR
      - Genera comentario en PR con "radio de explosión"
      - Identifica dependencias y zonas de riesgo
      - Sugiere tests adicionales para archivos afectados
- [x] Crear `.github/workflows/deploy.yml`
  - Trigger: Push a `main`
  - Steps: build, deploy Vercel + Railway
  > **Nota:** Smoke tests post-deploy se agregan en **1.11** (FASE 1)
- [x] Crear `.github/workflows/security-audit.yml`
  - Trigger: Push a `main`, cron semanal
  - Steps:
    - [x] OWASP dependency check
    - [x] SAST (Static Application Security Testing)
    - [x] Reportar vulnerabilidades críticas
- [x] Crear `.github/workflows/repo-maintenance.yml`
  - Trigger: Cron diario 00:00 UTC
  - Steps:
    - [x] Auto-label issues (bug, feature, etc.)
    - [x] Triage de issues nuevos
    - [x] Cerrar issues stale (sin actividad 30 días)
- [x] Crear `.github/workflows/health-audit.yml` (basic checks - FASE 0)
   - Trigger: Cron diario 06:00 UTC
   - Skills: `@global_skills/corporate-health-auditor/`
   - Steps (FASE 0):
     - [x] Disk usage alert (>80% warning)
     - [x] Git status (uncommitted changes alert)
     - [x] Telegram notification (requires `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`)
- [x] **[CI] Technical debt analysis** (Skill: `technical-debt-analysis`)
  - [x] Configurar cron mensual (1er día de cada mes)
  - [x] Generar reporte en `docs/reports/debt-[DATE].md`
  - [x] Scope: FASE 2+ code health audits

- [x] **✅ Done:** CI workflow ejecuta en PR de prueba

> **Skills usadas:**
> - `github-actions-mechanic` → Crear workflows
> - `security-auditor` → Auditoría OWASP, SAST
> - `github-actions-guardian` → Auto-label, triage, stale issues
> - `blast-radius-analyst` → Análisis de impacto en PRs, previene fallos en cascada
> - `code-review-excellence` → Auto-review con MCP tools, checklist estructurado, feedback constructivo

> **Troubleshooting FASE 0-1:** Si el CI falla, el flujo es simple:
> 1. `gh run view --log` → Leés el error
> 2. Arreglás el código localmente
> 3. `git push` → CI corre de nuevo
>
> Para troubleshooting avanzado (FASE 2+), ver [docs/sop/ci-troubleshooting.md](../docs/sop/ci-troubleshooting.md).

#### 0.4.2 Secrets en GitHub (Solo para APIs faltantes) ✅
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.4.2`

**Skills:**
- Security: `@global_skills/security-auditor/`
- DevOps: `@global_skills/git-workflow-hardener/`

> **Nota:** La mayoría de APIs ya están configuradas en `opencode.json`. Solo agregar estos secrets para APIs faltantes:

- [x] Configurar secrets en Settings → Secrets
  - `GROQ_API_KEY` (FASE 1 - Agent 3)
  - `MISTRAL_API_KEY` (FASE 1 - Agent 4)
  - `NVIDIA_API_KEY` (FASE 1 - Agent 3)
  - `VERCEL_TOKEN` (FASE 1 - Deploy)
  - `RAILWAY_TOKEN` (FASE 1 - Deploy)
  - `STRIPE_SECRET_KEY` (FASE 3 - Billing)
  - `MERCADOPAGO_ACCESS_TOKEN` (FASE 3 - Billing)
  - `TELEGRAM_BOT_TOKEN` (FASE 0 - Health Audit)
  - `TELEGRAM_CHAT_ID` (FASE 0 - Health Audit)
- [x] **✅ Done:** Secrets configurados y workflow los lee correctamente

---

### 0.5 Supabase Setup ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.5`

> **Nota:** Supabase YA está configurado en `opencode.json`. No es necesario agregar claves allí.

**Prioridad:** 🔴 Crítica  
**Dependencias:** Ninguna (Track B - paralelo a 0.1-0.4)  
**Tiempo estimado:** 1-2 horas  

**Skills:**
- Infra: `@global_skills/supabase-admin-tool/`, `@global_skills/infrastructure-core/`
- Security: `@global_skills/security-auditor/`
- Calidad: `@global_skills/error-handling-patterns/`, `@global_skills/data-quality-frameworks/`

#### 0.5.1 Proyecto Supabase ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.5.1`

- [ ] Crear proyecto "DATO" en supabase.com (si no existe)
- [ ] Configurar región: US East o Sao Paulo (latencia)
- [ ] Guardar credenciales (ya están en opencode.json, solo verificar):
  - `SUPABASE_URL`
  - `SUPABASE_ANON_KEY`
  - `SUPABASE_SERVICE_KEY`
- [ ] **✅ Done:** Proyecto visible en dashboard de Supabase

#### 0.5.2 Base de Datos ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.5.2`

- [ ] Ejecutar migraciones SQL (ver `docs/specs/database.md`)
  - [ ] Tabla `users`
  - [ ] Tabla `claims`
  - [ ] Tabla `verifications`
  - [ ] Tabla `economic_data`
  - [ ] Tabla `news_items`
  - [ ] Tabla `llm_usage` ← Token tracking
  - [ ] Tabla `subscriptions`
  - [ ] Tabla `alerts`
- [ ] Configurar Row Level Security (RLS)
- [ ] Crear índices
- [ ] **[DEV] Configurar data quality constraints** (NOT NULL, UNIQUE, FK)
- [ ] **[AMBOS] Definir data contracts para tablas críticas**
- [ ] **✅ Done:** Tablas creadas y visibles en Supabase Table Editor

#### 0.5.3 Auth ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.5.3`

**Skills:**
- Infra: `@global_skills/supabase-admin-tool/`
- Security: `@global_skills/compliance-legal-sentinel/`

- [ ] Habilitar Email/Password auth
- [ ] Configurar templates de email
- [ ] Configurar URL de redirección
- [ ] **[COMPLIANCE]** Verificar flujo de eliminación de cuenta (GDPR "Right to be Forgotten")
  - [ ] Usuario puede eliminar su cuenta
  - [ ] Todos sus datos se eliminan de DB
  - [ ] Datos en Vector Memory (Pinecone) se eliminan
- [ ] **✅ Done:** Signup/Login funciona y cumple GDPR

---

### 0.6 SOP Standardization ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.6`

**Prioridad:** 🟡 Alta  
**Dependencias:** Ninguna (Track B - paralelo a 0.1-0.5)  
**Tiempo estimado:** 2-3 horas

**Skills:** `@global_skills/sop-workflow-standardizer/`

#### 0.6.1 Fact-Checking SOP Enhancement ⏳

- [ ] Aplicar skill a `docs/sop/fact-checking.md`
  - [ ] Agregar checklist pre-ejecución obligatorio antes de cada verificación
  - [ ] Documentar flujo de rollback si fuente primaria falla
  - [ ] Estandarizar templates de output (formato JSON + explicación simple)
  - [ ] Crear tabla de edge cases con procedimientos específicos
- [ ] **✅ Done:** SOP de fact-checking con formato estandarizado

#### 0.6.2 Data Collection SOP Enhancement ⏳

- [ ] Aplicar skill a `docs/sop/data-collection.md`
  - [ ] Unificar fallback chain en playbook único (Firecrawl → Exa → DuckDuckGo → Cache)
  - [ ] Crear runbooks por fuente:
    - [ ] `runbook-indec.md`: Pasos específicos para INDEC
    - [ ] `runbook-bcra.md`: Pasos específicos para BCRA
    - [ ] `runbook-boletin.md`: Pasos específicos para Boletín Oficial
  - [ ] Documentar procedimiento de retry con delays exactos (5s → 10s → 20s)
  - [ ] Agregar checklist de validación de datos scrapeados
- [ ] **✅ Done:** SOP de data collection con runbooks por fuente

#### 0.6.3 Agent Coordination SOP Enhancement ⏳

- [ ] Aplicar skill a `docs/sop/agents.md`
  - [ ] Definir handoff protocol entre agentes (Agent 1 → 2 → 3 → 4 → 5)
  - [ ] Crear checklists de handoff: "¿Qué debe output Agent X antes de pasar a Agent Y?"
  - [ ] Documentar edge cases:
    - [ ] "¿Qué pasa si Agent 2 extrae 0 claims?"
    - [ ] "¿Qué pasa si Agent 3 no encuentra datos?"
    - [ ] "¿Qué pasa si Agent 4 falla en simplificar?"
  - [ ] Estandarizar formato JSON de output para cada agente
- [ ] **✅ Done:** SOP de agents con handoffs documentados

#### 0.6.4 SOP Wiki Centralizada ⏳

- [ ] Crear `docs/sop/WIKI.md` con índice navegable
  - [ ] Links a todos los SOPs
  - [ ] Quick reference de checklists
  - [ ] Troubleshooting index
- [ ] Configurar versionado de SOPs (fecha de última actualización)
- [ ] **✅ Done:** Wiki centralizada de SOPs

---

## 🧪 CP0: Checkpoint Técnico (Pre-FASE 1)

> **Cuándo:** Inmediatamente después de completar FASE 0
> **Duración:** 30 min
> **Objetivo:** Verificar que el setup está listo antes de codear features

### Checklist CP0

| Item | Comando | Estado |
|------|---------|--------|
| Dependencias | `pnpm install` sin errores | ❌ |
| Linting | `pnpm lint` sin errores | ❌ |
| Typecheck | `pnpm typecheck` sin errores | ❌ |
| Supabase tablas | Ver en Table Editor | ❌ |
| CI en PR de prueba | GitHub Actions verde | ❌ |
| Hooks funcionan | Commit de prueba pasa | ❌ |

### Métricas CP0

| Métrica | Valor | Umbral |
|---------|-------|--------|
| Tiempo real FASE 0 | ___ días | ≤ 7 días |
| Desvío | ___ | ≤ 2x estimado |

### Acción si falla

| Si... | Acción |
|-------|--------|
| Tiempo > 2x estimado | Revisar scope FASE 1, reducir features |
| CI no pasa | Fix antes de continuar |
| Supabase sin tablas | Ejecutar migraciones primero |
| Hooks fallan | Debuggear antes de seguir |

### Checklist CP0 (completo)

- [ ] `pnpm install` ejecuta sin errores
- [ ] `pnpm lint` ejecuta sin errores
- [ ] `pnpm typecheck` ejecuta sin errores
- [ ] Supabase tiene todas las tablas (ver 0.5.2)
- [ ] CI pasa en PR de prueba
- [ ] Pre-commit hook funciona en commit de prueba
- [ ] Documentar tiempo real vs estimado
- [ ] Decidir: Continuar FASE 1 / Ajustar scope

---

## FASE 1: MVP (6 semanas / 42 días)

> **Bloqueada hasta completar FASE 0**

### Sprint 1 (Semana 1-2): Backend + Deploy temprano

**Dependencias:** FASE 0 completa

#### 1.1 NestJS Backend ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1`

**Skills:**
  - Core: `@global_skills/nodejs-backend/`, `@global_skills/typescript-pro/`
  - Infra: `@global_skills/infrastructure-core/`
  - Calidad: `@global_skills/error-handling-patterns/`, `@global_skills/debugging-strategies/`, `@global_skills/code-modularity-architect/`
  - Docs: `@global_skills/codebase-navigator/`

##### 1.1.1 Setup Inicial ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.1`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/typescript-pro/`

- [ ] Inicializar NestJS en `apps/api/`: `nest new apps/api`
- [ ] Configurar Prisma ORM
  - [ ] `pnpm add prisma @prisma/client`
  - [ ] `npx prisma init`
  - [ ] Configurar `schema.prisma` con conexión a Supabase
- [ ] Configurar variables de entorno en `apps/api/.env`
- [ ] Crear estructura de carpetas:
  ```
  apps/api/src/
  ├── modules/
  │   ├── auth/
  │   ├── claims/
  │   ├── verifications/
  │   └── indicators/
  ├── common/
  │   ├── decorators/
  │   ├── filters/
  │   ├── guards/
  │   ├── interceptors/
  │   └── pipes/
  └── config/
  ```
- [ ] **✅ Done:** `pnpm dev` en `apps/api/` ejecuta sin errores

##### 1.1.2 AuthModule ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.2`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/infrastructure-core/`

- [ ] Crear módulo: `nest g module modules/auth`
- [ ] Crear controller: `nest g controller modules/auth`
- [ ] Crear service: `nest g service modules/auth`
- [ ] DTOs:
  - [ ] `auth.dto.ts`: LoginDto, RegisterDto, RefreshTokenDto
  - [ ] Validación con `class-validator`
- [ ] Guards:
  - [ ] `jwt-auth.guard.ts`: Protección de endpoints
  - [ ] `roles.guard.ts`: Autorización por plan
- [ ] Strategies:
  - [ ] `jwt.strategy.ts`: Extracción de token
- [ ] Endpoints:
  - [ ] `POST /auth/register`
  - [ ] `POST /auth/login`
  - [ ] `POST /auth/refresh`
  - [ ] `POST /auth/logout`
- [ ] **✅ Done:** Login/Logout funciona con JWT

##### 1.1.3 ClaimsModule ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.3`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/typescript-pro/`

- [ ] Crear módulo, controller, service
- [ ] DTOs:
  - [ ] `create-claim.dto.ts`
  - [ ] `update-claim.dto.ts`
  - [ ] `query-claims.dto.ts` (filtros, paginación)
- [ ] Repository: `claims.repository.ts` (Prisma)
- [ ] Endpoints:
  - [ ] `GET /claims` (listar, paginar, filtrar)
  - [ ] `GET /claims/:id`
  - [ ] `POST /claims` (protegido)
  - [ ] `PATCH /claims/:id` (protegido)
  - [ ] `DELETE /claims/:id` (protegido)
- [ ] **✅ Done:** CRUD de claims funciona

##### 1.1.4 VerificationsModule ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.4`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/ai-engineer/`

- [ ] Crear módulo, controller, service
- [ ] DTOs:
  - [ ] `create-verification.dto.ts`
  - [ ] `verification-response.dto.ts`
- [ ] Repository: `verifications.repository.ts`
- [ ] Endpoints:
  - [ ] `GET /verifications`
  - [ ] `GET /verifications/:id`
  - [ ] `POST /verifications` (trigger fact-check)
- [ ] **✅ Done:** Verificaciones se crean y listan

##### 1.1.5 IndicatorsModule ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.5`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/infrastructure-core/`

- [ ] Crear módulo, controller, service
- [ ] DTOs:
  - [ ] `indicator-query.dto.ts`
  - [ ] `indicator-response.dto.ts`
- [ ] Repository: `indicators.repository.ts`
- [ ] Endpoints:
  - [ ] `GET /indicators` (listar todos)
  - [ ] `GET /indicators/:type` (inflación, dólar, etc.)
- [ ] **✅ Done:** Indicadores económicos se consultan

##### 1.1.6 Infrastructure - Rate Limiting ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.6`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/cost-control/`

- [ ] Instalar Throttler: `pnpm add @nestjs/throttler`
- [ ] Configurar ThrottlerModule en `app.module.ts`
  - [ ] Limit: 100 req/min por usuario
  - [ ] Limit diferenciado por plan (free/premium/pro)
- [ ] Custom decorator: `@PlanRateLimit()`
- [ ] **✅ Done:** Rate limiting activo y configurable

##### 1.1.7 Infrastructure - Validation & Pipes ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.7`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/typescript-pro/`

- [ ] Instalar: `pnpm add class-validator class-transformer`
- [ ] Configurar `ValidationPipe` global
- [ ] Custom pipes:
  - [ ] `trim.pipe.ts`: Limpiar espacios
  - [ ] `sanitize.pipe.ts`: XSS protection
- [ ] **✅ Done:** Validación automática en todos los endpoints

##### 1.1.8 Infrastructure - Exception Filters ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.8`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/error-handling-patterns/`

- [ ] Crear filtros:
  - [ ] `http-exception.filter.ts`: Errores HTTP estándar
  - [ ] `prisma-exception.filter.ts`: Errores de DB
  - [ ] `all-exceptions.filter.ts`: Catch-all
- [ ] Formato de respuesta estándar:
  ```json
  {
    "statusCode": 400,
    "message": "Error message",
    "error": "Bad Request",
    "timestamp": "2026-02-14T20:00:00Z"
  }
  ```
- [ ] **✅ Done:** Errores retornan formato consistente

##### 1.1.9 Infrastructure - Interceptors ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.9`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/observability-engineer/`

- [ ] Crear interceptores:
  - [ ] `logging.interceptor.ts`: Log de requests/response
  - [ ] `transform.interceptor.ts`: Wrap de respuesta exitosa
  - [ ] `timeout.interceptor.ts`: Timeout de requests
- [ ] **✅ Done:** Logs automáticos en cada request

##### 1.1.10 API Documentation (Swagger) ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.10`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/docs-technical-writer/`

- [ ] Instalar: `pnpm add @nestjs/swagger`
- [ ] Configurar SwaggerModule en `main.ts`
- [ ] Decoradores en DTOs: `@ApiProperty()`, `@ApiResponse()`
- [ ] Documentar autenticación (Bearer JWT)
- [ ] Tags por módulo:
  - [ ] `@ApiTags('auth')`
  - [ ] `@ApiTags('claims')`
  - [ ] `@ApiTags('verifications')`
  - [ ] `@ApiTags('indicators')`
  - [ ] `@ApiTags('health')`
- [ ] Ejemplos de request/response: `@ApiExample()`
- [ ] Endpoint: `GET /api` (Swagger UI)
- [ ] **✅ Done:** Swagger UI accesible en `/api`

##### 1.1.11 Routes Documentation ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.11`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/docs-technical-writer/`

- [ ] Crear `apps/api/ROUTES.md`
- [ ] Documentar todos los endpoints:
  ```markdown
  ## Auth
  | Method | Endpoint | Auth | Description |
  |--------|----------|------|-------------|
  | POST | /auth/register | ❌ | Register new user |
  | POST | /auth/login | ❌ | Login user |
  | POST | /auth/refresh | ❌ | Refresh token |
  | POST | /auth/logout | ✅ | Logout user |
  
  ## Claims
  | Method | Endpoint | Auth | Description |
  |--------|----------|------|-------------|
  | GET | /claims | ❌ | List claims (paginated) |
  | GET | /claims/:id | ❌ | Get claim by ID |
  | POST | /claims | ✅ | Create claim |
  | PATCH | /claims/:id | ✅ | Update claim |
  | DELETE | /claims/:id | ✅ | Delete claim |
  
  ## Verifications
  | Method | Endpoint | Auth | Description |
  |--------|----------|------|-------------|
  | GET | /verifications | ❌ | List verifications |
  | GET | /verifications/:id | ❌ | Get verification |
  | POST | /verifications | ✅ | Trigger fact-check |
  
  ## Indicators
  | Method | Endpoint | Auth | Description |
  |--------|----------|------|-------------|
  | GET | /indicators | ❌ | List all indicators |
  | GET | /indicators/:type | ❌ | Get specific indicator |
  
  ## Health
  | Method | Endpoint | Auth | Description |
  |--------|----------|------|-------------|
  | GET | /health | ❌ | Health check |
  | GET | /health/db | ❌ | Database health |
  | GET | /health/redis | ❌ | Redis health |
  ```
- [ ] **✅ Done:** `ROUTES.md` documenta todos los endpoints

##### 1.1.12 Health Checks ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.12`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/infrastructure-core/`

- [ ] Instalar: `pnpm add @nestjs/terminus`
- [ ] Crear HealthController
- [ ] Health indicators:
  - [ ] Database (Prisma/Supabase)
  - [ ] Redis
  - [ ] Memory heap
- [ ] Endpoint: `GET /health`
- [ ] **✅ Done:** Health check responde estado de servicios

##### 1.1.13 Debugging & Tracing ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.13`

**Skills:** `@global_skills/nodejs-backend/`, `@global_skills/debugging-strategies/`

- [ ] Instalar: `pnpm add pino pino-pretty nestjs-pino`
- [ ] Configurar logger estructurado
- [ ] Integrar LangSmith tracing
- [ ] Correlation IDs en requests
- [ ] **[DEV] Debug logging** para cada módulo
- [ ] **✅ Done:** Logs estructurados en consola y LangSmith

##### 1.1.14 Deploy básico ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.1.14`

**Skills:** `@global_skills/deploy-automation-pilot/`, `@global_skills/github-actions-mechanic/`

- [ ] Deploy backend a Railway
- [ ] Verificar environment variables en Railway
- [ ] Configurar health check endpoint
- [ ] Test /health endpoint en producción
- [ ] **✅ Done:** Backend accesible en producción con health check verde


---

### Sprint 2 (Semana 3-4): Agents

**Dependencias:** Sprint 1 completo

#### 1.2 Agent 1: Data Collector ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.2`

**Skills:**
  - Core: `@global_skills/ai-engineer/`
  - Costos: `@global_skills/token-accountant/`, `@global_skills/cost-control/`, `@global_skills/cost-monitor/`
  - Calidad: `@global_skills/code-modularity-architect/`, `@global_skills/data-quality-frameworks/`, `@global_skills/debugging-strategies/`
  - AI: `@global_skills/curacion-de-contenido/`, `@global_skills/mcp-vetting-guard/`, `@global_skills/instruction-compressor/`
  - Infra: `@global_skills/rag-auto-indexer/`

- [ ] Implementar en `packages/agents/src/agent-1-collector/`
- [ ] Integrar MCP `firecrawl_scrape`
- [ ] Integrar MCP `exa_search`
- [ ] Configurar cron jobs
  - [ ] INDEC: diario 9:00 AM
  - [ ] BCRA: cada 3 horas
- [ ] Token budget monitoring
- [ ] Rate limiting para MCP servers
- [ ] Fallback policies (exa → duckduckgo)
- [ ] **[PROD] Validar datos scrapeados (completeness, validity)** ← Cada scrape
- [ ] **[AMBOS] Debug logging para cada fase del collector`
- [ ] Implementar curación de contenido (5-step protocol)
   - [ ] Filtrado de ruido (hype, clickbait, opiniones sin sustento)
   - [ ] Verificación cruzada con Exa/Google para confirmar tendencias
   - [ ] Análisis de Fit vs infraestructura DATO
   - [ ] Business Relevance Filter (alineado con objetivos políticos)
   - [ ] Indexar en Pinecone solo contenido `verified`
- [ ] Tests unitarios
- [ ] **[INFRA] Auto-indexing a Pinecone** (Skill: `rag-auto-indexer`)
  - [ ] Configurar `resources/index_config.json` con paths de contenido
  - [ ] Sincronizar contenido scrapeado a Pinecone post-collection

#### 1.3 Agent 2: Claim Extractor ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.3`

**Skills:**
  - Core: `@global_skills/ai-engineer/`
  - Costos: `@global_skills/token-accountant/`, `@global_skills/cost-control/`, `@global_skills/cost-monitor/`
  - AI: `@global_skills/langgraph-director/`, `@global_skills/curacion-de-contenido/`
  - Calidad: `@global_skills/code-modularity-architect/`

- [ ] Implementar en `packages/agents/src/agent-2-extractor/`
- [ ] Integrar MCP `sequential_thinking`
- [ ] NER para políticos
- [ ] Token budget optimization
- [ ] Rate limiting per extraction
- [ ] Tests unitarios

#### 1.4 Agent 3: Fact Checker ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.4`

**Skills:**
   - Core: `@global_skills/ai-engineer/`
   - Costos: `@global_skills/token-accountant/`, `@global_skills/cost-monitor/`
   - AI/RAG: `@global_skills/rag-implementation/`, `@global_skills/agentic-stress-tester/`, `@global_skills/instruction-compressor/`
   - Infra: `@global_skills/infrastructure-core/`
   - Calidad: `@global_skills/error-handling-patterns/`, `@global_skills/data-quality-frameworks/`, `@global_skills/code-modularity-architect/`
   - AI: `@global_skills/agent-evaluation/`, `@global_skills/memory-systems/`

- [ ] Implementar en `packages/agents/src/agent-3-factchecker/`
- [ ] Integrar MCP `pinecone_query`
- [ ] Integrar MCP `supabase_execute_sql`
- [ ] Sistema de badges (✅⚠️❌⚪)
- [ ] Error handling con retries y backoff
- [ ] Cost tracking en tiempo real
- [ ] **[AMBOS] Data contracts para verificaciones** ← Validar datos de entrada
- [ ] **[PROD] Validar source data quality antes de verificar`
- [ ] **[TEST] Stress testing con agentic-stress-tester** ← Generar queries adversarias para RAG
- [ ] Tests unitarios
- [ ] **[TEST] Agent evaluation suite** (Skill: `agent-evaluation`)
  - [ ] Crear `tests/agent-eval/` con YAML suites
  - [ ] Configurar invariants (contains, not_contains, is_json)
  - [ ] Correr benchmarking estadístico (10+ runs por test)

- [ ] **[INFRA] Memory persistence layer** (Skill: `memory-systems`)
  - [ ] Configurar Redis para short-term session storage
  - [ ] Integrar Pinecone namespace `dude-central-brain` para cross-session memory
  - [ ] Implementar consolidation rules para prevenir index bloat

> **Post-implementación (opcional):** Crear `.github/workflows/stress-test.yml` para stress testing semanal automatizado en producción.

#### 1.5 Agent 4: Simplifier ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.5`

**Skills:**
  - Core: `@global_skills/ai-engineer/`
  - Costos: `@global_skills/token-accountant/`, `@global_skills/cost-control/`
  - AI: `@global_skills/langgraph-director/`, `@global_skills/prompt-optimizer-dspy/`, `@global_skills/curacion-de-contenido/`
  - Calidad: `@global_skills/debugging-strategies/`, `@global_skills/code-modularity-architect/`

- [ ] Implementar en `packages/agents/src/agent-4-simplifier/`
- [ ] Integrar MCP `sequential_thinking`
- [ ] Prompts de simplificación
- [ ] Token cost optimization
- [ ] Model fallback (premium → cost-effective)
- [ ] **[DEV] Debug logging para prompt engineering`
- [ ] Tests unitarios

#### 1.5.1 Agent Handoff Documentation ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.5.1`

**Skills:** `@global_skills/sop-workflow-standardizer/`

- [ ] Documentar handoff protocol entre agentes:
  - [ ] Agent 1 → Agent 2: Formato de datos scrapeados
  - [ ] Agent 2 → Agent 3: Formato de claims extraídos
  - [ ] Agent 3 → Agent 4: Formato de verificaciones
  - [ ] Agent 4 → Agent 5: Formato de contenido simplificado
- [ ] Crear checklists de handoff por agente
- [ ] Definir formato JSON estándar de output para cada agente
- [ ] Documentar procedimiento cuando handoff falla
- [ ] **✅ Done:** Handoffs documentados en `docs/sop/agents.md`

---

### Sprint 3 (Semana 5-6): Frontend + Auth UI

**Dependencias:** Sprint 2 completo


#### 1.6 Next.js Frontend + Zustand ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.6`

**Skills:** `@global_skills/react-expert/`, `@global_skills/typescript-pro/`, `@global_skills/code-modularity-architect/`, `@global_skills/error-handling-patterns/`, `@global_skills/docs-technical-writer/`, `@global_skills/codebase-navigator/`

- [ ] Inicializar proyecto Next.js 14 en `apps/web/`
- [ ] Configurar App Router
- [ ] Configurar Tailwind CSS
- [ ] Configurar Zustand (state)
- [ ] Error boundaries para páginas
- [ ] **✅ Done:** `pnpm dev` ejecuta sin errores en `apps/web/`

##### 1.6.1 State Management (Zustand) ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.6.1`

**Skills:** `@global_skills/react-expert/`, `@global_skills/typescript-pro/`

- [ ] Crear estructura de stores
  ```bash
  mkdir -p apps/web/src/stores
  touch apps/web/src/stores/{auth,feed,search,ui}Store.ts
  ```
- [ ] Implementar `authStore`
- [ ] Implementar `feedStore`
- [ ] Implementar `uiStore`
- [ ] Configurar persist middleware
- [ ] **✅ Done:** Stores importan sin errores y persisten en localStorage

#### 1.7 UI Components ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.7`

**Skills:** `@global_skills/ui-component-library/`, `@global_skills/design-system/`, `@global_skills/brand-identity/`, `@global_skills/error-handling-patterns/`, `@global_skills/code-modularity-architect/`, `@global_skills/docs-technical-writer/`

- [ ] Crear componentes base en `packages/ui/`
  - [ ] FeedCard
  - [ ] VerificationBadge
  - [ ] ClaimCard
  - [ ] IndicatorCard
  - [ ] ErrorBoundary
  - [ ] LoadingStates
- [ ] Configurar Storybook
#### 1.8 Páginas ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.8`

**Skills:** `@global_skills/react-expert/`, `@global_skills/ux-researcher/`, `@global_skills/seo-technical-master/`, `@global_skills/brand-identity/`

- [ ] Landing page (`/`)
- [ ] Feed diario (`/feed`)
- [ ] Detail de claim (`/claim/[id]`)
- [ ] Búsqueda (`/search`)

#### 1.8.1 SEO Técnico ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.8.1`

**Skills:** `@global_skills/seo-technical-master/`, `@global_skills/react-expert/`

**Objetivo:** Optimizar DATO para tráfico orgánico desde el día 1.

- [ ] **Core Web Vitals**
  - [ ] Configurar Lighthouse CI en GitHub Actions
  - [ ] Thresholds: LCP < 2.5s, CLS < 0.1, FID < 100ms
  - [ ] Optimizar imágenes (WebP, AVIF, lazy loading)
  - [ ] Critical CSS inline

- [ ] **Metadatos y OpenGraph**
  - [ ] Configurar Next.js Metadata API
  - [ ] Títulos dinámicos por página
  - [ ] Meta descripciones optimizadas
  - [ ] OpenGraph tags para social sharing
  - [ ] Twitter Cards

- [ ] **Indexabilidad**
  - [ ] Crear `robots.txt` optimizado
  - [ ] Generar sitemap.xml dinámico
  - [ ] Configurar canonical URLs
  - [ ] Estructura de URLs amigables: `/claim/[slug]` en lugar de `/claim/[id]`

- [ ] **Schema.org (Datos Estructurados)**
  - [ ] `NewsArticle` para fact-checks
  - [ ] `ClaimReview` para verificaciones (Google Fact Check)
  - [ ] `Organization` para DATO
  - [ ] `BreadcrumbList` para navegación

- [ ] **SEO para Next.js**
  - [ ] Server Components para contenido indexable
  - [ ] Static generation para páginas públicas
  - [ ] Dynamic rendering para contenido personalizado

- [ ] **Keywords Strategy**
  - [ ] Investigar keywords políticas Argentina
  - [ ] Implementar en títulos y meta descriptions
  - [ ] H1, H2, H3 estructurados

- [ ] **Google Search Console**
  - [ ] Crear propiedad en GSC
  - [ ] Verificar dominio
  - [ ] Subir sitemap
  - [ ] Configurar alertas

- [ ] **✅ Done:** Lighthouse score > 90, sitemap enviado a GSC, Schema.org implementado

#### 1.9 Auth UI ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.9`

**Skills:** `@global_skills/react-expert/`, `@global_skills/supabase-admin-tool/`, `@global_skills/security-auditor/`

> **Nota:** La integración backend de Supabase Auth ya está en 1.1.2. Esta sección es solo UI.

- [ ] Login/Signup UI components
- [ ] Protected routes
- [ ] Session management UI
- [ ] Error handling para auth flows
- [ ] **[COMPLIANCE]** Compliance-Gate: auditar manejo de PII
  - [ ] Política de privacidad accesible
  - [ ] Consentimiento explícito en signup
- [ ] **✅ Done:** Auth UI funcional con login/signup/logout

#### 1.10 Deploy completo ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.9`

**Skills:**
   - DevOps: `@global_skills/deploy-automation-pilot/`, `@global_skills/github-actions-mechanic/`, `@global_skills/devops-troubleshooter/`, `@global_skills/observability-engineer/`, `@global_skills/reliability-sre-pilot/`
   - Costos: `@global_skills/token-accountant/`, `@global_skills/cost-monitor/`
   - Infra: `@global_skills/database-performance-tuner/`

- [ ] Deploy frontend a Vercel
- [ ] Deploy backend a Railway
- [ ] Configurar dominios
- [ ] Verificar health checks
- [ ] Configurar cost dashboard API
- [ ] Token usage dashboard
- [ ] **[AMBOS] Crear runbook para troubleshooting post-deploy**
- [ ] **[PROD] Configurar alertas de incidentes**
- [ ] **[RUNBOOK] Self-healing troubleshooting** (Skill: `reliability-sre-pilot`)
  - [ ] Documentar runbook para port conflicts, missing deps
  - [ ] Configurar startup failure recovery steps
- [ ] Extender `.github/workflows/health-audit.yml` para FASE 1 (post-deploy)
  - Steps adicionales (habilitar cuando Railway + Redis estén up):
    - [ ] Redis connectivity check
    - [ ] Agent directories verification
    - [ ] Query latency check (database-performance-tuner)
      - [ ] Medir avg query_time de Supabase/Railway DB
      - [ ] Alertar si > 100ms via Telegram
      - [ ] Log en `CORPORATE_LOG.md` para análisis posterior
#### 1.11 Smoke Tests Post-Deploy ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.11`

**Skills:** `@global_skills/api-endpoint-tester/`, `@global_skills/test-automation-strategist/`

- [ ] Agregar step en `.github/workflows/deploy.yml` (después de deploy)
  ```yaml
  - name: Smoke Tests (api-endpoint-tester)
    run: pnpm test:smoke
  ```
- [ ] Crear `tests/smoke/` con tests de endpoints críticos
  - [ ] `health.spec.ts`: GET /health → 200
  - [ ] `claims.spec.ts`: GET /api/claims → 200
  - [ ] `claims.spec.ts`: POST /api/claims → 201 (con auth)
  - [ ] `auth.spec.ts`: Endpoints protegidos → 401 sin token
- [ ] Agregar script en `package.json`
  ```json
  "test:smoke": "vitest run tests/smoke"
  ```
- [ ] Configurar notificación si smoke tests fallan (Slack/Telegram)

> **Ejecución:**
> - **Automática:** GitHub Actions post-deploy (cada merge a main)
> - **Skill usada:** `api-endpoint-tester` (contract validation, auth flows)

---

## 🧪 CP1: Checkpoint de Validación (Post Sprint 3)

> **Cuándo:** Día 42 (post-deploy, 6 semanas)
> **Duración:** 1-2 horas
> **Con quién:** 3-5 usuarios (amigos, colegas)

### Objetivo
Validar que el MVP básico funciona y es entendible antes de seguir invirtiendo.

### Tests a realizar

| Test | Qué validar | Método |
|------|-------------|--------|
| **Badges** | ¿✅⚠️❌⚪ se interpretan correctamente? | Mostrar 5 verificaciones, preguntar significado |
| **Simplificación** | ¿El texto explicado es entendible? | Leer 3 verificaciones, preguntar "¿entendiste?" |
| **Flujo básico** | ¿Navegación intuitiva? | Pedir que busquen un claim y lo verifiquen |
| **UI/UX** | ¿Colores, tipografía, espaciado? | Observar sin intervenir, tomar notas |
| **Auth** | ¿Signup/Login fluido? | Observar proceso, medir abandono |

### Métricas de éxito CP1

| Métrica | Umbral | Estado |
|---------|--------|--------|
| Badges interpretados correctamente | ≥ 80% | ❌ |
| Simplificación entendible | ≥ 70% "sí" | ❌ |
| Flujo completado sin ayuda | ≥ 60% | ❌ |
| Auth completado sin ayuda | ≥ 80% | ❌ |
| Sin bugs críticos | 0 bugs | ❌ |

### Acción si falla

| Si falla... | Acción |
|-------------|--------|
| Badges | Rediseñar con texto + ícono, volver a testear |
| Simplificación | Ajustar prompts del Agent 4, testear con otros ejemplos |
| Flujo | Simplificar navegación, agregar onboarding |
| Auth | Simplificar flujo, mejorar mensajes de error |
| Bugs críticos | Pausar FASE 2, fix primero |

### Checklist CP1

- [ ] Reclutar 3-5 testers (amigos/colelgas)
- [ ] Preparar 5 verificaciones de ejemplo
- [ ] Preparar 3 simplificaciones de ejemplo
- [ ] Ejecutar tests (remoto o presencial)
- [ ] Documentar feedback en `docs/validation/cp1-feedback.md`
- [ ] Decidir: Continuar / Iterar / Pausar

---

## FASE 2: Growth (60 días)

> **Bloqueada hasta completar FASE 1**

### Sprint 4 (Semana 7-8): Auth + Búsqueda

#### 2.1 Sistema de Roles ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 2.1`

**Skills:** `@global_skills/typescript-pro/`, `@global_skills/supabase-admin-tool/`, `@global_skills/security-auditor/`

> **Nota:** Auth UI está en FASE 1 Sprint 3 (1.9). Esta sección es solo el sistema de roles backend.

- [ ] Definir tipos de rol en `packages/types/src/roles.ts`
  ```typescript
  type UserRole = 'user' | 'admin';
  ```
- [ ] Agregar campo `role` a tabla `users` en Supabase
  ```sql
  ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin'));
  ```
- [ ] Implementar `RolesGuard` en backend
  ```typescript
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  ```
- [ ] Crear decorator `@Roles()` para endpoints protegidos
- [ ] Endpoints admin:
  - [ ] `GET /admin/users` - Listar usuarios
  - [ ] `PATCH /admin/users/:id/role` - Cambiar rol
  - [ ] `GET /admin/metrics` - Métricas del sistema
- [ ] Página `/admin` protegida por rol
- [ ] **✅ Done:** Sistema de roles operativo, admin puede acceder a panel


#### 2.2 Búsqueda ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 2.2`

**Skills:** `@global_skills/rag-implementation/`, `@global_skills/vector-index-tuning/`, `@global_skills/cost-monitor/`, `@global_skills/infrastructure-core/`, `@global_skills/error-handling-patterns/`

- [ ] Integrar Pinecone vector search
- [ ] Autocomplete
- [ ] Filtros por categoría
- [ ] Fallback para errores de búsqueda
- [ ] Query cost tracking

---

#### 2.3 Performance Setup ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.10`

**Skills:** `@global_skills/performance-optimization-pilot/`, `@global_skills/financial-controller/`

- [ ] Configurar Lighthouse CI en `.github/workflows/performance.yml`
  - Trigger: PR a `main` y `develop`
  - Thresholds: LCP < 2.5s, CLS < 0.1, FID < 100ms
- [ ] Agregar métricas de performance a cost dashboard
- [ ] Configurar Vercel Analytics
- [ ] Documentar optimizaciones y ROI de tokens

> **Ejecución:**
> - **Continua:** Lighthouse CI en cada PR (automático)
> - **Manual:** Revisar métricas semanales, optimizar si degradan


#### 2.4 WebMCP Integration ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 1.12`

**Skills:** `@global_skills/typescript-pro/`, `@global_skills/react-expert/`

> **Feature diferencial:** Permite usuarios conectarse desde Claude Desktop u otros clientes MCP para usar DATO directamente.

- [ ] Descargar `webmcp.js` a `apps/web/public/`
- [ ] Agregar script en `apps/web/src/app/layout.tsx`:
  ```tsx
  <script src="/webmcp.js" async></script>
  ```
- [ ] Registrar herramientas MCP en `apps/web/src/lib/webmcp-tools.ts`:
  - [ ] `fact-check`: Verificar una frase política
  - [ ] `explain-concept`: Explicar término económico/político
  - [ ] `search-news`: Buscar noticias políticas
  - [ ] `get-indicators`: Obtener indicadores económicos (dólar, inflación)
- [ ] Configurar widget (color brand, posición)
- [ ] Documentar uso en README

> **Beneficio:** Usuarios pueden interactuar con DATO desde su cliente LLM sin visitar el sitio.



#### 2.5 CI Troubleshooting Avanzado ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 2.5`

**Skills:**
  - Ops: `@global_skills/self-correction-pilot/`, `@global_skills/post-mortem-memory/`, `@global_skills/telegram-hq-commander/`
  - AI: `@global_skills/context-manager/`

- [ ] Configurar `context-manager/` para orchestración de contexto
  - [ ] Crear wrapper en `packages/agents/src/shared/context-manager.ts`
  - [ ] Integrar con Pinecone namespace `incident-patterns`
  - [ ] Configurar hybrid search (vector + keyword)
  - [ ] Implementar pruning de logs/boilerplate
- [ ] Configurar `telegram-hq-commander/` para alertas de CI
  - [ ] Agregar `TELEGRAM_BOT_TOKEN` a secrets
  - [ ] Agregar `TELEGRAM_USER_ID` para filtro de seguridad
  - [ ] Configurar notificación automática en CI failure
- [ ] Implementar flujo de diagnóstico con `self-correction-pilot`
  - [ ] RCA automático con sequential-thinking
  - [ ] Aplicación de patches
  - [ ] Verificación post-fix
- [ ] Implementar post-mortem con `post-mortem-memory`
  - [ ] Extracción de lecciones aprendidas
  - [ ] Subida a Vector Memory (Pinecone)
  - [ ] Prevención de recurrencia
- [ ] **[CONTEXT]** Retrieve past incident patterns from Vector Memory for RCA using context-manager hybrid search
- [ ] **✅ Done:** Sistema de troubleshooting operativo

---

### Sprint 5 (Semana 9-10): Notifications + Publishing

#### 2.6 Push Notifications ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 2.3`

**Skills:** `@global_skills/deploy-automation-pilot/`, `@global_skills/observability-engineer/`, `@global_skills/error-handling-patterns/`, `@global_skills/devops-troubleshooter/`, `@global_skills/database-performance-tuner/`

- [ ] Configurar OneSignal o Firebase
- [ ] Suscripción a alerts
- [ ] Notificaciones diarias
- [ ] Retry logic para notificaciones fallidas
- [ ] **[PROD] Incident response plan para notificaciones**
- [ ] **[AMBOS] Debug logging para notification pipeline**

#### 2.7 Agent 5: Publisher ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 2.4`

**Skills:**
  - Core: `@global_skills/ai-engineer/`
  - Costos: `@global_skills/token-accountant/`, `@global_skills/cost-control/`
  - Ops: `@global_skills/telegram-bot-builder/`
  - Infra: `@global_skills/infrastructure-core/`

- [ ] Implementar en `packages/agents/src/agent-5-publisher/`
- [ ] Newsletter (Resend)
- [ ] Twitter auto-posting
- [ ] Telegram bot
- [ ] Token cost tracking por publicación
- [ ] Fallback channels si uno falla

#### 2.8 Agent 9: Growth Engineer ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 2.8`

**Skills:**
  - Growth: `@global_skills/marketing-psychology/`, `@global_skills/pricing-strategy/`
  - Analytics: `@global_skills/observability-engineer/`
  - Costos: `@global_skills/financial-controller/`

**Responsabilidades:**
- Analiza funnel de conversión (visitante → signup → premium)
- Aplica psychology triggers (anchoring, loss aversion, social proof)
- Optimiza pricing display y CTAs
- Detecta churn risk antes de que cancelen
- A/B testing automatizado de mensajes

- [ ] Implementar en `packages/agents/src/agent-9-growth/`
- [ ] Integrar con Supabase analytics
- [ ] Configurar tracking de eventos:
  - [ ] `page_view`, `signup_started`, `signup_completed`
  - [ ] `verification_requested`, `verification_completed`
  - [ ] `upgrade_viewed`, `upgrade_completed`, `churn_risk_detected`
- [ ] Implementar detección de churn:
  - [ ] Usuario sin actividad >7 días
  - [ ] Usuario que reduce uso
  - [ ] Usuario que ve pricing pero no convierte
- [ ] Aplicar psychology triggers:
  - [ ] **Anchoring:** Mostrar Professional primero
  - [ ] **Loss Aversion:** "Perdés X verificaciones por no ser Premium"
  - [ ] **Social Proof:** "X usuarios verificaron esto hoy"
  - [ ] **Scarcity:** "Solo quedan 3 verificaciones gratis hoy"
- [ ] Dashboard de métricas de growth
- [ ] Tests unitarios
- [ ] **✅ Done:** Growth engine optimiza conversa automáticamente

#### 2.9 Pipedream MCP Integration ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 2.9`

**Skills:**
  - Infra: `@global_skills/infrastructure-core/`
  - Ops: `@global_skills/deploy-automation-pilot/`

**Propósito:** Agregar Pipedream MCP para conectar múltiples APIs con una sola configuración.

**APIs a conectar via Pipedream (FASE 2):**
| API | Uso en DATO | Agente |
|-----|-------------|--------|
| Resend | Newsletter | Agent 5 |
| Twitter/X | Auto-posting | Agent 5 |
| Telegram Bot | Notificaciones | Agent 5 |
| OneSignal | Push notifications | Agent 5 |

**Ventajas:**
- Una sola cuenta para múltiples APIs
- OAuth manejado automáticamente
- Sin código de integración para cada API

- [ ] Crear cuenta en [mcp.pipedream.com](https://mcp.pipedream.com)
- [ ] Obtener Pipedream API key
- [ ] Agregar a `opencode.json`:
  ```json
  "pipedream": {
    "type": "remote",
    "url": "https://mcp.pipedream.net/v2",
    "environment": {
      "PIPEDREAM_API_KEY": "tu-api-key"
    }
  }
  ```
- [ ] Conectar APIs en Pipedream dashboard:
  - [ ] Resend (newsletter)
  - [ ] Twitter/X (auto-posting)
  - [ ] Telegram Bot
  - [ ] OneSignal (push)
- [ ] Testear cada conexión desde Kilo CLI
- [ ] Documentar tools disponibles en `docs/technical/mcp-tools.md`
- [ ] **✅ Done:** Pipedream MCP conecta 4+ APIs sin código adicional

---

## 🧪 CP2: Checkpoint de Validación (Post Sprint 5)

> **Cuándo:** Día 60 (post-FASE 2)
> **Duración:** 2-3 horas
> **Con quién:** 5-10 usuarios reales (no solo amigos)

### Objetivo
Validar features de growth antes de monetizar.

### Tests a realizar

| Test | Qué validar | Método |
|------|-------------|--------|
| **Búsqueda** | ¿Encuentran lo que buscan? | Pedir 3 búsquedas, medir tiempo y éxito |
| **Notificaciones** | ¿Son útiles? ¿Molestan? | Encuesta post-3 días de uso |
| **Publisher** | ¿Contenido es relevante? | Mostrar newsletter/Telegram, preguntar valor |
| **Auth** | ¿Signup es fluido? | Observar proceso, medir abandono |

### Métricas de éxito CP2

| Métrica | Umbral | Estado |
|---------|--------|--------|
| Búsqueda exitosa | ≥ 70% encuentra en < 30s | ❌ |
| Notificaciones útiles | ≥ 60% "útiles" | ❌ |
| Contenido relevante | ≥ 50% "me interesa" | ❌ |
| Signup completado | ≥ 80% sin ayuda | ❌ |
| Retención 7 días | ≥ 30% | ❌ |

### Checklist CP2

- [ ] Reclutar 5-10 usuarios (Twitter, LinkedIn, comunidad)
- [ ] Preparar guía de uso (email de bienvenida)
- [ ] Monitorear uso por 7 días (analytics)
- [ ] Enviar encuesta de satisfacción
- [ ] Documentar feedback en `docs/validation/cp2-feedback.md`
- [ ] Decidir: Continuar a FASE 3 / Iterar features

---

## FASE 3: Monetización (90+ días)

> **Bloqueada hasta completar FASE 2**

### 3.0 Pricing Research ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 3.0`

**Prioridad:** 🟡 Alta  
**Dependencias:** CP2 completado  
**Tiempo estimado:** 2-3 días

**Skills:** `@global_skills/pricing-strategy/`, `@global_skills/marketing-psychology/`

> **Nota:** Esta investigación debe completarse ANTES de implementar billing para definir precios correctos.

- [ ] **3.0.1** Investigación Van Westendorp
  - [ ] Encuesta a 20-30 usuarios potenciales
  - [ ] Identificar "Optimal Price Point" y "Acceptable Range"
  - [ ] Documentar resultados en `docs/business/pricing-research.md`

- [ ] **3.0.2** MaxDiff Feature Ranking
  - [ ] Listar features candidatas por tier
  - [ ] Ranking de utilidad percibida
  - [ ] Decidir qué features van en cada plan

- [ ] **3.0.3** Definir Estructura de Tiers
  - [ ] **Free:** 3 verificaciones/día, sin historial
  - [ ] **Premium:** Verificaciones ilimitadas, alerts, historial 30 días
  - [ ] **Professional:** Dashboard B2B, API access, reports, historial completo
  - [ ] Documentar en `docs/business/pricing-tiers.md`

- [ ] **3.0.4** Calcular Price Points
  - [ ] Analizar willingness to pay por segmento
  - [ ] Comparar con alternativas (Chequeado, etc.)
  - [ ] Definir precios: Premium (~$5/mes), Professional (~$50/mes)

- [ ] **3.0.5** Aplicar modelos de marketing-psychology
  - [ ] **Anchoring:** Mostrar Professional primero para hacer Premium parecer barato
  - [ ] **Decoy Effect:** Free muy limitado para impulsar Premium
  - [ ] **Loss Aversion:** "Perdés X verificaciones por no ser Premium"

- [ ] **✅ Done:** Estructura de precios documentada y validada

### Sprint 6 (Semana 11-14): Billing

#### 3.1 Agent 8: Quality Assurance (QA) ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 3.1`

**Skills:**
  - QA: `@global_skills/agent-evaluation/`
  - AI: `@global_skills/ai-engineer/`
  - Data: `@global_skills/data-quality-frameworks/`

**Responsabilidades:**
- Evalúa precisión de verificaciones (sample aleatorio del 5%)
- Detecta drift en accuracy (si accuracy baja >5%)
- Genera reports de calidad semanales
- Sugiere ajustes de prompts cuando accuracy baja
- Identifica patrones de errores comunes

- [ ] Implementar en `packages/agents/src/agent-8-qa/`
- [ ] Integrar con `@global_skills/agent-evaluation/scripts/`
- [ ] Configurar evaluación diaria:
  - [ ] Sample aleatorio de 5% de verificaciones
  - [ ] Comparar veredicto LLM vs ground truth
  - [ ] Calcular accuracy, precision, recall, F1
- [ ] Configurar alertas de drift:
  - [ ] Si accuracy < 95% → alerta
  - [ ] Si accuracy < 90% → pausar Agent 3, escalar
- [ ] Implementar sugerencias automáticas:
  - [ ] Detectar tipo de claim con más errores
  - [ ] Suggestir prompt improvements
  - [ ] Log en `docs/qa/suggestions-[DATE].md`
- [ ] Dashboard de calidad:
  - [ ] Accuracy por día/semana/mes
  - [ ] Distribución de errores por categoría
  - [ ] Comparación de LLM providers
- [ ] Tests unitarios
- [ ] **✅ Done:** QA evalúa calidad automáticamente y sugiere mejoras

#### 3.2 Agent 6: Billing ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 3.2`

**Skills:**
   - Core: `@global_skills/nodejs-backend/`
   - Billing: `@global_skills/stripe-integration/`, `@global_skills/pricing-strategy/`
   - Payment: `@global_skills/stripe-integration/`, `@global_skills/payment-integration/`
   - Costos: `@global_skills/token-accountant/`, `@global_skills/cost-monitor/`
   - Infra: `@global_skills/infrastructure-core/`
   - Security: `@global_skills/compliance-legal-sentinel/`

- [ ] Integrar Stripe
- [ ] Integrar Mercado Pago
- [ ] **[INFRA] Payment Integration** (Skill: `payment-integration`)
   - [ ] Configurar Stripe webhooks con signature verification
   - [ ] Implementar idempotency keys para prevenir double charges
   - [ ] Manejar state machine de webhooks (payment_intent.succeeded, etc.)
   - [ ] Rate limiting en endpoints de pago
   - [ ] Tokenización de tarjetas (nunca almacenar datos crudos)
   - [ ] Re-fetch payment status desde API (no confiar en client responses)
   - [ ] Retornar 2xx dentro de 200ms para webhooks
   - [ ] Preservar raw body para signature validation
- [ ] Sistema de suscripciones
- [ ] Webhooks
- [ ] Token usage billing (metered billing)
- [ ] Cost reports por usuario
- [ ] **[COMPLIANCE MANDATORIO]** Compliance-Gate antes de lanzar pagos
   - [ ] Términos y Condiciones actualizados
   - [ ] Política de privacidad con sección de pagos
   - [ ] Flujo de reembolso documentado
   - [ ] Datos de pago almacenados de forma segura (PCI DSS)
   - [ ] Usuario puede eliminar datos de pago
   - [ ] Auditoría de EU AI Act (si aplica IA en billing)

#### 3.3 Planes ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 3.3`

**Skills:**
  - Billing: `@global_skills/pricing-strategy/`, `@global_skills/marketing-psychology/`
  - Costos: `@global_skills/financial-controller/`, `@global_skills/token-accountant/`, `@global_skills/cost-control/`

- [ ] Free: 3 verificaciones/día (token limit)
- [ ] Premium: $5/mes (token quota: 1000 tokens/día)
- [ ] Professional: $50/mes (unlimited tokens)
- [ ] Rate limits diferenciados por plan

---

### Sprint 7 (Semana 15-18): Dashboard + Learning

#### 3.3 Agent 7: Learning ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 3.3`

**Skills:**
  - Core: `@global_skills/ai-engineer/`
  - Costos: `@global_skills/token-accountant/`, `@global_skills/cost-monitor/`
  - AI/RAG: `@global_skills/rag-auto-indexer/`, `@global_skills/meta-learning-engine/`, `@global_skills/context-manager/`
  - DevOps: `@global_skills/observability-engineer/`
  - Calidad: `@global_skills/debugging-strategies/`


- [ ] Implementar en `packages/agents/src/agent-7-learning/`
- [ ] Configurar context-manager para Agent 7 (learning sync)
  - [ ] Definir namespace `episodic-learning` en Pinecone
  - [ ] Implementar sync de métricas de engagement a Vector Memory
  - [ ] Configurar retrieval de learning patterns históricos
- [ ] Integrar MCP `langsmith_traces`
- [ ] Métricas de engagement
- [ ] Recomendaciones automáticas
- [ ] Token efficiency learning
- [ ] Cost optimization patterns
- [ ] **[DEV] Debug de métricas ML**
- [ ] **[CONTEXT]** Sync episodic learning nodes to Vector Memory via context-manager for meta-learning continuity

#### 3.4 Dashboard B2B ⏳
> **Ejecutar:** `python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 3.4`

**Skills:** `@global_skills/react-expert/`, `@global_skills/ui-component-library/`, `@global_skills/cost-monitor/`, `@global_skills/design-system/`, `@global_skills/token-accountant/`, `@global_skills/database-performance-tuner/`, `@global_skills/devops-troubleshooter/`

- [ ] Dashboard con gráficos
- [ ] Token usage reports
- [ ] Cost analytics
- [ ] Exportar CSV/PDF
- [ ] API access
- [ ] Cost dashboard API integration
- [ ] **[PROD] Production debugging procedures**

---

## 🧪 CP3: Checkpoint Pre-Orchestration (Post FASE 3)

> **Cuándo:** Post-FASE 3, antes de decidir implementar FASE 4
> **Duración:** 1-2 horas
> **Objetivo:** Validar si realmente se necesita un orquestador

### Checklist de Decisión

| Pregunta | Sí | No |
|----------|----|----|
| ¿Necesitas ejecutar agentes en paralelo? | □ | □ |
| ¿Necesitas branching condicional (IF/ELSE)? | □ | □ |
| ¿Necesitas sincronizar resultados de múltiples fuentes? | □ | □ |
| ¿Necesitas cancelar workflows en progreso? | □ | □ |
| ¿Necesitas visibilidad en tiempo real de cada paso? | □ | □ |
| ¿Necesitas retry logic complejo (backoff + escalar)? | □ | □ |

**Decisión:**
- **0-2 "Sí"** → NO implementar FASE 4, BullMQ es suficiente
- **3-4 "Sí"** → Evaluar caso por caso
- **5-6 "Sí"** → Implementar FASE 4

### Métricas que Justifican Orquestación

| Métrica | Umbral para Justificar |
|---------|----------------------|
| Verificaciones/día | > 1000 |
| Claims multi-fuente | > 20% del total |
| Timeout de verificación | > 10% fallan por timeout |
| Incidents sin recovery | > 10% requieren intervención manual |
| Usuario cancela verificación | > 5% cancelan en progreso |

---

## FASE 4: Orchestration Layer (Post-MVP)

> **Estado:** 🔒 Bloqueada hasta completar FASE 3 + validación de necesidad
>
> **Prerrequisito:** MVP funcional + >1000 verificaciones/día + flujos complejos identificados

### ¿Cuándo implementar?

| Trigger | Descripción |
|---------|-------------|
| Flujo con branching | Si necesitas IF/ELSE en el pipeline de verificación |
| Paralelización | Si necesitas ejecutar Agent 3A, 3B, 3C en paralelo |
| Sincronización | Si necesitas esperar resultados de múltiples agentes |
| Visibilidad | Si necesitas ver en tiempo real el estado de cada paso |
| Cancelación | Si necesitas poder cancelar verificaciones en progreso |
| Retry complejo | Si necesitas lógica de retry con backoff exponencial + escalar a humano |

**Si ninguno de estos triggers ocurre → NO implementar (seguir con BullMQ)**

---

### Agent 0: Orchestrator

```yaml
agent:
  id: agent-0
  name: Orchestrator
  description: Coordina la ejecución de agentes con branching, paralelismo y manejo de errores

input:
  type: object
  required: [workflow_type, payload]
  properties:
    workflow_type:
      type: string
      enum: [verification_complex, publishing_multi, incident_response, learning_sync]
    payload:
      type: object
    priority:
      type: string
      enum: [low, normal, high, critical]
      default: normal
    timeout_ms:
      type: number
      default: 30000

output:
  type: object
  properties:
    workflow_id:
      type: string
      format: uuid
    status:
      type: string
      enum: [pending, running, completed, failed, cancelled]
    steps:
      type: array
      items:
        type: object
        properties:
          agent_id:
            type: string
          status:
            type: string
          result:
            type: object
          error:
            type: string
          duration_ms:
            type: number

llm_config:
  provider: mistral
  model: mistral-medium-latest
  max_tokens: 1000
  temperature: 0.2

mcp_tools:
  - langsmith_traces
  - supabase_execute_sql
```

---

### Casos de Uso Concretos

#### 4.1 Verificación Compleja Multi-Fuente

```
ESCENARIO: "Milei dijo que la inflación bajó 50% en su gobierno"

┌─────────────────────────────────────────────────────────────┐
│                    AGENT 0: ORCHESTRATOR                     │
│                                                              │
│  1. Clasifica: "claim económico" → branching                 │
│                                                              │
│  2. Ejecuta EN PARALELO:                                    │
│     ├── Agent 3A: Verifica INDEC                            │
│     ├── Agent 3B: Verifica BCRA                             │
│     └── Agent 3C: Busca declaraciones oficiales             │
│                                                              │
│  3. SINCRONIZA resultados:                                  │
│     ├── INDEC: inflación bajó 12%                           │
│     ├── BCRA: confirma 12%                                  │
│     └── Oficial: speech encontrado con "50%"                │
│                                                              │
│  4. DECIDE:                                                  │
│     ├── Si 3 fuentes coinciden → ✅ VERDADERO               │
│     ├── Si discrepan → ⚠️ PARCIAL + explicar diferencia     │
│     └── Si no hay datos → ⚪ SIN_DATOS                      │
│                                                              │
│  5. RETRY con lógica:                                       │
│     ├── Si Agent 3A falla → reintentar con backoff          │
│     ├── Si falla 3 veces → escalar a humano                 │
│     └── Si timeout → continuar con fuentes disponibles      │
│                                                              │
│  6. TRACKING en tiempo real:                                │
│     └── Dashboard muestra: "Verificando INDEC... ✓ BCRA..." │
│                                                              │
│  7. CANCELACIÓN:                                            │
│     └── Si usuario cierra app → cancelar todo el flujo      │
└─────────────────────────────────────────────────────────────┘
```

#### 4.2 Publicación Multi-Canal con Fallbacks

```
ESCENARIO: "Verificación viral >1000 views"

┌─────────────────────────────────────────────────────────────┐
│                    AGENT 0: ORCHESTRATOR                     │
│                                                              │
│  1. Detecta: claim tiene >1000 views → prioridad ALTA       │
│                                                              │
│  2. Ejecuta EN PARALELO:                                    │
│     ├── Agent 5A: Publicar en Twitter                       │
│     ├── Agent 5B: Publicar en Telegram                      │
│     ├── Agent 5C: Enviar newsletter                         │
│     └── Agent 5D: Notificar usuarios con alertas            │
│                                                              │
│  3. MANEJA ERRORES:                                         │
│     ├── Twitter API rate limit → esperar 15 min, reintentar │
│     ├── Telegram OK → marcar completado                     │
│     └── Newsletter falla → log, notificar admin             │
│                                                              │
│  4. REPORTA:                                                 │
│     └── "Publicado en 3/4 canales. Twitter pendiente"       │
└─────────────────────────────────────────────────────────────┘
```

#### 4.3 Incident Response Automatizado

```
ESCENARIO: "Agent 3 falló 5 veces en última hora"

┌─────────────────────────────────────────────────────────────┐
│                    AGENT 0: ORCHESTRATOR                     │
│                                                              │
│  1. Detecta patrón de fallas (via LangSmith traces)         │
│                                                              │
│  2. SECUENCIA DE RECUPERACIÓN:                              │
│     ├── Step 1: Ejecutar Agent 7 (Learning) → analizar RCA  │
│     ├── Step 2: Si RCA identifica fix → aplicar patch       │
│     ├── Step 3: Verificar con smoke test                    │
│     └── Step 4: Si falla → escalar a humano                 │
│                                                              │
│  3. NOTIFICACIÓN:                                           │
│     └── Telegram: "Incidente detectado + acción tomada"     │
└─────────────────────────────────────────────────────────────┘
```

---

### Tasks de Implementación

#### 4.1 Setup LangGraph ⏳

**Skills:** `@global_skills/langgraph-director/`, `@global_skills/ai-engineer/`

- [ ] Instalar LangGraph: `pnpm add langgraph @langchain/core`
- [ ] Crear estructura en `packages/agents/src/agent-0-orchestrator/`
  ```
  agent-0-orchestrator/
  ├── index.ts
  ├── workflows/
  │   ├── verification-complex.ts
  │   ├── publishing-multi.ts
  │   ├── incident-response.ts
  │   └── learning-sync.ts
  ├── nodes/
  │   ├── classify.ts
  │   ├── branch.ts
  │   ├── parallel.ts
  │   ├── sync.ts
  │   ├── retry.ts
  │   └── escalate.ts
  └── state.ts
  ```
- [ ] Definir StateGraph para cada workflow
- [ ] Configurar checkpointing en Redis
- [ ] **✅ Done:** LangGraph ejecuta workflow básico

#### 4.2 Workflow: Verificación Compleja ⏳

**Skills:** `@global_skills/langgraph-director/`, `@global_skills/rag-implementation/`

- [ ] Implementar nodo `classify_claim`
- [ ] Implementar nodo `branch_by_category`
- [ ] Implementar nodo `parallel_verify` (INDEC, BCRA, Oficial)
- [ ] Implementar nodo `sync_results`
- [ ] Implementar nodo `decide_verdict`
- [ ] Implementar nodo `handle_timeout`
- [ ] Implementar nodo `escalate_to_human`
- [ ] Tests con escenarios reales
- [ ] **✅ Done:** Verificación compleja funciona con 3 fuentes paralelas

#### 4.3 Workflow: Publicación Multi-Canal ⏳

**Skills:** `@global_skills/langgraph-director/`, `@global_skills/telegram-bot-builder/`

- [ ] Implementar nodo `detect_viral_claim`
- [ ] Implementar nodo `parallel_publish` (Twitter, Telegram, Newsletter)
- [ ] Implementar nodo `handle_rate_limits`
- [ ] Implementar nodo `report_status`
- [ ] Tests con canales mock
- [ ] **✅ Done:** Publicación paralela con manejo de rate limits

#### 4.4 Workflow: Incident Response ⏳

**Skills:** `@global_skills/langgraph-director/`, `@global_skills/self-correction-pilot/`

- [ ] Implementar nodo `detect_failure_pattern`
- [ ] Implementar nodo `run_rca` (Agent 7)
- [ ] Implementar nodo `apply_patch`
- [ ] Implementar nodo `verify_fix`
- [ ] Implementar nodo `escalate_to_human`
- [ ] Integrar con Telegram notifications
- [ ] **✅ Done:** Incident response automatizado

#### 4.5 Dashboard de Orquestación ⏳

**Skills:** `@global_skills/react-expert/`, `@global_skills/observability-engineer/`

- [ ] Crear endpoint `GET /api/orchestration/status/:workflow_id`
- [ ] Crear endpoint `POST /api/orchestration/cancel/:workflow_id`
- [ ] Implementar WebSocket para updates en tiempo real
- [ ] Crear UI de dashboard:
  - [ ] Lista de workflows activos
  - [ ] Estado de cada step
  - [ ] Timeline visual
  - [ ] Botón de cancelación
- [ ] **✅ Done:** Dashboard muestra workflows en tiempo real

#### 4.6 Migración desde BullMQ ⏳

**Skills:** `@global_skills/langgraph-director/`

- [ ] Identificar flujos lineales que se beneficiarían de orquestación
- [ ] Crear workflows LangGraph equivalentes
- [ ] Migrar gradualmente (mantener BullMQ como fallback)
- [ ] Tests A/B para comparar rendimiento
- [ ] Deprecar BullMQ para flujos complejos
- [ ] **✅ Done:** Migración completa a LangGraph

---

### Métricas de Éxito FASE 4

| Métrica | Baseline (BullMQ) | Target (LangGraph) |
|---------|-------------------|-------------------|
| Tiempo verificación compleja | N/A (no soportado) | < 5s (paralelo) |
| Visibilidad del flujo | 0% | 100% |
| Cancelaciones exitosas | 0% | 100% |
| Recovery automático | 0% | > 80% |
| Incidentes escalados | 100% manual | < 20% manual |

---

### Checkpoint FASE 4

- [ ] LangGraph operativo con 3+ workflows
- [ ] Dashboard de orquestación funcional
- [ ] Verificación multi-fuente en paralelo
- [ ] Recovery automático de incidentes
- [ ] Métricas de éxito cumplidas
- [ ] BullMQ deprecado para flujos complejos

---

## Skills Disponibles por Categoría

### 📈 SEO & Marketing

| Skill | Estado | Descripción | Ejecución |
|-------|--------|-------------|-----------|
| `seo-technical-master/` | ✅ **AGREGADO** | Core Web Vitals, Schema.org, metadatos, sitemaps | FASE 1.8.1 (Frontend) |
| `marketing-psychology/` | ✅ Activo | Psychology triggers, growth | FASE 2 (Growth) |
| `pricing-strategy/` | ✅ Activo | SaaS pricing, tiers | FASE 3 (Billing) |

### 🎨 UX/UI/Design

| Skill | Estado | Descripción |
|-------|--------|-------------|
| `brand-identity/` | ✅ Activo | Design tokens, voice/tone standards via Vector Memory |
| `google-slides-visual-creator/` | ✅ Activo | Generación de slides con dark glassmorphism, 2026 trends |
| `visual-learning-engine/` | ✅ Activo | Análisis de screenshots, videos, patrones UI/UX |
| `ux-researcher/` | ✅ **NUEVO** | User research, usability testing, journey mapping |
| `ui-component-library/` | ✅ **NUEVO** | Componentes reutilizables, Storybook, accessibility |
| `design-system/` | ✅ **NUEVO** | Sistema de diseño completo, tokens, Figma integration |

### 💻 Frontend

| Skill | Estado | Descripción |
|-------|--------|-------------|
| `typescript-pro/` | ✅ Activo | Advanced types, generics, strict type safety |
| `code-modularity-architect/` | ✅ Activo | DRY/SRP enforcement, code splitting |
| `react-expert/` | ✅ **NUEVO** | React/Next.js 14+, Server Components, performance |
| `telegram-mini-app/` | ✅ Activo | Mini apps para Telegram |
| `seo-technical-master/` | ✅ Activo | SEO técnico para web apps |

### 🔧 Backend

| Skill | Estado | Descripción |
|-------|--------|-------------|
| `typescript-pro/` | ✅ Activo | NestJS, Node.js, Express integration |
| `nodejs-backend/` | ✅ **NUEVO** | NestJS architecture, API design, security |
| `api-endpoint-tester/` | ✅ Activo | Smoke testing, contract validation |
| `database-performance-tuner/` | ✅ Activo | Query optimization, indexing, latency monitoring (FASE 1+) |
| `infrastructure-core/` | ✅ Activo | Supabase, Redis abstractions |
| `security-auditor/` | ✅ Activo | OWASP Top 10, hardening |
| `error-handling-patterns/` | ✅ Activo | Resilient architecture, Circuit Breakers, Result Types |

### 🔧 DevOps

| Skill | Estado | Descripción | Ejecución |
|-------|--------|-------------|-----------|
| `git-flow-sentinel/` | ✅ Activo | Branch protection, feature branching | Automática (por tarea) |
| `git-workflow-hardener/` | ✅ Activo | Hooks, secret scanning | Continua (cada commit) |
| `git-advanced-workflows/` | ✅ Activo | Rebase, bisect, recovery | Manual |
| `performance-optimization-pilot/` | ✅ Activo | Lighthouse CI, optimización | Continua (cada PR) |
| `corporate-health-auditor/` | ✅ **AGREGADO** | Disk, Git health (FASE 0) → Redis, Agents (FASE 1+) | Cron diario (06:00 UTC) |

### 🤖 AI/Agents

| Skill | Estado | Descripción |
|-------|--------|-------------|
| `ai-engineer/` | ✅ Activo | LLM integration, RAG, NVIDIA NIM |
| `rag-implementation/` | ✅ Activo | Vector search, embeddings, hybrid search |
| `langgraph-director/` | ✅ Activo | Multi-agent orchestration |
| `prompt-optimizer-dspy/` | ✅ Activo | Prompt engineering, DSPy optimization |
| `token-accountant/` | ✅ Activo | Token usage tracking, cost optimization, budget enforcement |
| `context-manager/` | ✅ **AGREGADO** | Dynamic context engineering, pruning, hybrid retrieval, multi-agent sync (FASE 2.5+) |
| `curacion-de-contenido/` | ✅ **AGREGADO** | Content filtering, verification, business relevance (Agent 1) |
| `instruction-compressor/` | ✅ **AGREGADO** | Token reduction via LLMLingua-2 (Agents 1, 3) |

### 💰 Financial/Ops

| Skill | Estado | Descripción |
|-------|--------|-------------|
| `financial-controller/` | ✅ Activo | Token budget audit, cost efficiency |
| `token-accountant/` | ✅ Activo | LLM token usage tracking, ROI analysis |
| `pricing-strategy/` | ✅ Activo | SaaS pricing, tier structure |
| `cost-control/` | ✅ **AGREGADO** | Rate limiting, fallback policies, quota tracking |
| `cost-monitor/` | ✅ **AGREGADO** | Real-time cost tracking, dashboard API, SQLite histórico |

### 🛠️ Quality & Debugging

| Skill | Estado | Descripción | Ejecución |
|-------|--------|-------------|-----------|
| `test-automation-strategist/` | ✅ **NUEVO** | TDD, BDD, Pirámide de pruebas (Unit 70%, Integration 20%, E2E 10%), Coverage Gate 80% | Continua (pre-push) |
| `api-endpoint-tester/` | ✅ Activo | Smoke testing, contract validation, auth testing | Post-deploy |
| `data-quality-frameworks/` | ✅ **AGREGADO** | Data validation, contracts, quality checks | **[AMBOS]** Dev + Prod |
| `debugging-strategies/` | ✅ **AGREGADO** | RCA, systematic debugging, profiling | **[DEV]** Principalmente |
| `blast-radius-analyst/` | ✅ **AGREGADO** | Impact analysis, dependency tracing, previene fallos en cascada | **CI (PRs)** Antes de merge |
| `code-review-excellence/` | ✅ **AGREGADO** | Auto-review con MCP tools, checklists estructurados, feedback constructivo | **CI (PRs)** En cada PR |
| `devops-troubleshooter/` | ✅ **AGREGADO** | Incident response, observability, K8s debugging | **[PROD]** Principalmente |
| `self-correction-pilot/` | ✅ **AGREGADO** | RCA automático, aplica fixes, verifica | **FASE 2+** (tras CI fail) |
| `post-mortem-memory/` | ✅ **AGREGADO** | Extrae lecciones, sube a Pinecone | **FASE 2+** (post-fix) |
| `telegram-hq-commander/` | ✅ **AGREGADO** | CI notifications, control remoto via Telegram | **FASE 2+** (con incidentes) |
| `compliance-legal-sentinel/` | ✅ **AGREGADO** | GDPR, EU AI Act, PII Guard, Compliance-Gate | **Manual** (antes de features PII/pagos) |
| `environment-cleanup-specialist/` | ✅ **AGREGADO** | Workspace cleanup, cache pruning, disk optimization | post-commit (automático) |
| `codebase-navigator/` | ✅ **AGREGADO** | Contexto mínimo, surgical read, dependency tracing | Continua (navegación) |
| `code-modularity-architect/` | ✅ Activo | DRY/SRP, archivos <300 LOC | Continua |
| `detect-duplicate-files/` | ✅ Activo | Hash-based duplicate detection | Semanal |
| `docs-technical-writer/` | ✅ Activo | Docs-as-Code, OpenAPI, Mermaid | Continua |

### 📋 Task Execution

| Skill | Estado | Descripción | Ejecución |
|-------|--------|-------------|-----------|
| `task-prompt-engineer/` | ✅ **NUEVO** | Genera prompts de ejecución para subtasks | Manual (antes de ejecutar) |
| `asynchronous-jules-helper/` | ✅ **AGREGADO** | Delega tareas pesadas a Jules (background), notifica al completar | Manual (large refactors, bulk docs) |

---

## Legenda de Ejecución

| Tag | Significado | Cuándo se Ejecuta |
|-----|-------------|-------------------|
| `[DEV]` | Solo durante desarrollo | Ahora, al ejecutar el plan |
| `[PROD]` | Solo en producción | Cuando el sistema esté funcional |
| `[AMBOS]` | Desarrollo + Producción | Ahora y siempre |

---

## ✅ Skills Creadas (2026-02-13)

Las siguientes skills fueron creadas usando `@global_skills/gemini-skill-creator/`:

| Skill | Propósito | Hereda de |
|-------|-----------|-----------|
| `ux-researcher/` | User research, usability testing | visual-learning-engine |
| `ui-component-library/` | Componentes reutilizables, Storybook | code-modularity-architect, brand-identity |
| `react-expert/` | React/Next.js avanzado, Server Components | typescript-pro |
| `nodejs-backend/` | NestJS, API design, seguridad | typescript-pro, infrastructure-core |
| `design-system/` | Sistema de diseño, tokens, Figma | brand-identity, ui-component-library |
| `task-prompt-engineer/` | Generar prompts de ejecución para subtasks | task-deconstructor-pro (adaptado) |
| `asynchronous-jules-helper/` | Delegar tareas pesadas a Jules (background) | central-vector-memory |

> **Ver documentación completa:** `docs/guides/SKILLS.md`

---

## 🚀 Cómo Ejecutar las Tasks con task-prompt-engineer

### Uso de la Skill

Esta skill genera prompts estructurados para ejecutar cada subtask de TASK.md.

**Ejecución manual:**
```bash
# Generar prompt para una subtask específica
python global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2.1

# El output es un prompt listo para copiar y usar con el agente
```

**Output ejemplo:**
```markdown
## Contexto
- Proyecto: DATO (fact-checking político argentino)
- Fase: FASE 0
- Subtask: 0.2.1 - package.json

## Objetivo
Crear package.json con pnpm workspaces

## Skills a usar
- `@global_skills/monorepo-management/`
- `@global_skills/typescript-pro/`
- `@global_skills/code-modularity-architect/`, `@global_skills/curacion-de-contenido/`

## Comandos
```bash
# Crear package.json
# Crear pnpm-workspace.yaml
```

## Criterios de Aceptación
- [x] Crear `package.json` con pnpm workspaces
- [x] Crear `pnpm-workspace.yaml`

## Dependencias
- 0.1 Git (completado)
```

### Flujo de Trabajo Recomendado

1. **Identificar subtask**: Elegir la próxima subtask pendiente (ej: 0.2.1)
2. **Generar prompt**: `python global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2.1`
3. **Copiar prompt**: El output está listo para usar
4. **Ejecutar**: Pasar el prompt al agente de IA
5. **Verificar**: Marcar checkboxes en TASK.md al completar

---

## Bloqueadores Actuales

| # | Bloqueador | Sección | Solución | Estado |
|---|------------|---------|----------|--------|
| B1 | Sin repositorio GitHub | 0.1 | Crear repo + ramas | ❌ |
| B2 | Sin config files | 0.2 | Crear package.json, tsconfig | ❌ |
| B3 | Sin estructura código | 0.3 | Crear apps/, packages/ | ❌ |
| B4 | Sin proyecto Supabase | 0.5 | Crear proyecto + tablas | ❌ |

---

## Próximas Acciones (Priorizadas)

| Prioridad | Acción | Sección | Tiempo |
|-----------|--------|---------|--------|
| 🔴 1 | Crear repo GitHub + ramas | 0.1 | 30 min |
| 🔴 2 | Crear proyecto Supabase | 0.5 | 30 min |
| 🔴 3 | Crear package.json + workspaces | 0.2.1 | 20 min |
| 🔴 4 | Crear estructura directorios | 0.3 | 30 min |
| 🟡 5 | Config files restantes | 0.2.2-4 | 1-2 horas |
| 🟡 6 | CI/CD GitHub Actions | 0.4 | 3-4 horas |

---

## Métricas de Éxito

### CP1 - Validación MVP (Día 42)
- [ ] 3-5 usuarios testean
- [ ] Badges interpretados ≥ 80%
- [ ] Simplificación entendible ≥ 70%
- [ ] Flujo completado sin ayuda ≥ 60%
- [ ] 0 bugs críticos

### CP2 - Validación Growth (Día 60)
- [ ] 5-10 usuarios reales
- [ ] Búsqueda exitosa ≥ 70%
- [ ] Notificaciones útiles ≥ 60%
- [ ] Retención 7 días ≥ 30%

### MVP (Mes 1)
- [ ] 100 usuarios activos
- [ ] 500 fact-checks/día
- [ ] 30% retención 7 días
- [ ] Token cost < $0.10/verification
- [ ] Cost visibility: 100% de operaciones trackeadas
- [ ] Data quality score > 95%

### Growth (Mes 3)
- [ ] 500 usuarios mensuales
- [ ] 3% conversión premium
- [ ] $500 MRR
- [ ] Token efficiency > 80%
- [ ] Fallback success rate > 95%
- [ ] Incident response time < 5 min

### Scale (Mes 12)
- [ ] 5000 usuarios mensuales
- [ ] 150 usuarios premium
- [ ] 10 clientes B2B
- [ ] $5000 MRR
- [ ] Cost per verification < $0.05
- [ ] Data quality score > 99%

---

## Tareas Diferidas (YAGNI)

> **Principio:** No implementar hasta que se necesite.

| Tarea | Ubicación original | Mover a | Trigger para implementar |
|-------|-------------------|---------|---------------------------|
| **TypeDoc + Mermaid** | FASE 0.2.7 | FASE 1.11 (post-Swagger) | Cuando haya API docs que generar |
| **Weekly Code Hygiene** | FASE 0.4.2 | FASE 1.9 (post-deploy) | Cuando haya código que auditar semanalmente |
| **modularity:check** | FASE 0.2.6 | FASE 1.1 (backend) | Cuando archivos superen 200 líneas |
| **Circuit Breaker** | FASE 1.1.10 | Post-Agent 3 (1.4) | Cuando se integren APIs externas (Groq, Mistral, NVIDIA) |
| **Storybook** | FASE 1.7 | ✅ Ya bien ubicado | Cuando haya 5+ componentes |

### Detalle de Tareas Diferidas

#### TypeDoc + Mermaid (mover a FASE 1.11)
> **Trigger:** Swagger completo + al menos 10 endpoints documentados
- [ ] Instalar TypeDoc: `pnpm add -D typedoc`
- [ ] Crear `typedoc.json` config
- [ ] Agregar script `pnpm docs:generate`
- [ ] Configurar Mermaid CLI
- [ ] **✅ Done:** `pnpm docs:generate` produce HTML en `docs/api/`

#### Weekly Code Hygiene (mover a FASE 1.9)
> **Trigger:** Deploy funcionando + al menos 100 commits
- [ ] Instalar jscpd: `pnpm add -D jscpd`
- [ ] Agregar script `pnpm duplicates:check`
- [ ] Crear `.github/workflows/code-hygiene.yml`
- [ ] **✅ Done:** GitHub Actions corre auditoría semanal

#### Code Modularity Check (mover a FASE 1.1)
> **Trigger:** Cualquier archivo > 200 líneas
- [ ] Configurar ESLint rule `max-lines: 300`
- [ ] Crear template de barrel file (index.ts)
- [ ] Agregar script `pnpm modularity:check`
- [ ] **✅ Done:** `pnpm modularity:check` reporta archivos grandes

#### Circuit Breaker (mover a post-Agent 3)
> **Trigger:** Primera integración con API externa (Groq/Mistral/NVIDIA)
- [ ] Instalar circuit-breaker-js o similar
- [ ] Crear `circuit-breaker.service.ts`
- [ ] Configurar para Groq, Mistral, NVIDIA NIM
- [ ] Definir fallback policies
- [ ] **✅ Done:** APIs externas protegidas con retry + fallback

---

*Documento vivo - Actualizar al completar cada tarea*
