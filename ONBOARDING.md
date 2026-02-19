# 🚀 Onboarding - DATO

> Bienvenido al proyecto DATO. Esta guía te ayudará a configurar tu entorno y empezar a contribuir.

---

## 📋 Prerrequisitos

| Herramienta | Versión | Cómo instalar |
|-------------|---------|---------------|
| Node.js | 20+ | `nvm install 20` |
| pnpm | 8.15+ | `npm install -g pnpm` |
| Git | 2.40+ | `brew install git` |
| Redis | 7+ | `brew install redis` |
| Kilo CLI | Latest | [kilo.ai](https://kilo.ai) |

---

## ⚡ Quick Start (5 min)

```bash
# 1. Clonar repositorio
git clone https://github.com/mauroociappina/dato.git
cd dato

# 2. Instalar dependencias
pnpm install

# 3. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales (ver sección Variables de Entorno)

# 4. Iniciar Redis
redis-server --daemonize yes

# 5. Iniciar desarrollo
pnpm dev
```

---

## 🔑 Variables de Entorno

Crear archivo `.env` en la raíz con:

```bash
# Supabase (ya configurado en opencode.json)
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# Redis
REDIS_URL=redis://localhost:6379

# LLM Providers (agregar cuando se necesiten)
GROQ_API_KEY=your_groq_key        # FASE 1
MISTRAL_API_KEY=your_mistral_key  # FASE 1

# Optional
TELEGRAM_BOT_TOKEN=your_token     # Para alertas
TELEGRAM_CHAT_ID=your_chat_id
```

> **Nota:** Las APIs principales ya están configuradas en `opencode.json`. Solo necesitas agregar las que faltan cuando inicies FASE 1+.

---

## 📁 Estructura del Proyecto

```
dato/
├── apps/
│   ├── web/          # Next.js frontend (puerto 3000)
│   └── api/          # NestJS backend (puerto 3001)
├── packages/
│   ├── agents/       # 9 AI agents
│   ├── types/        # TypeScript types compartidos
│   └── ui/           # Componentes UI compartidos
├── docs/
│   ├── product/      # PRD, Roadmap, User Stories
│   ├── technical/    # Architecture, API docs
│   ├── sop/          # Procedimientos estándar
│   └── specs/        # Database, types, validation
├── tests/
│   ├── e2e/          # Tests end-to-end
│   └── integration/  # Tests de integración
├── global_skills/    # Skills para Kilo CLI
├── TASK.md           # 📍 Tu fuente de verdad para tareas
└── ONBOARDING.md     # Este archivo
```

---

## 🔧 Comandos Principales

| Comando | Descripción |
|---------|-------------|
| `pnpm dev` | Iniciar todos los servicios en desarrollo |
| `pnpm build` | Build de producción |
| `pnpm test` | Ejecutar tests |
| `pnpm lint` | Linting con ESLint |
| `pnpm typecheck` | Verificar tipos TypeScript |
| `pnpm format` | Formatear código con Prettier |

### Por app (desde subdirectorios)

```bash
# Frontend (apps/web)
pnpm dev          # Next.js en localhost:3000

# Backend (apps/api)
pnpm dev          # NestJS en localhost:3001
pnpm test         # Tests del backend
```

---

## 🌿 Git Workflow

### Convenciones de Ramas

| Prefijo | Uso | Ejemplo |
|---------|-----|---------|
| `feature/` | Nueva funcionalidad | `feature/dato-0.2-config-files` |
| `fix/` | Corregir subtask que falló | `fix/dato-0.2.3-eslint` |
| `hotfix/` | Urgente en producción | `hotfix/auth-crash` |
| `chore/` | Mantenimiento, docs | `chore/update-deps` |

### Flujo Básico

```bash
# 1. Asegurarte de estar en develop actualizado
git checkout develop
git pull origin develop

# 2. Crear rama feature (una por SECCIÓN, no por subtask)
git checkout -b feature/dato-0.2-config-files

# 3. Trabajar y commitear
git add .
git commit -m "feat(config): add package.json with workspaces"

# 4. Al completar la sección, crear PR
git push origin feature/dato-0.2-config-files
gh pr create --base develop --title "feat: 0.2 config files"

# 5. Después del merge, actualizar develop
git checkout develop
git pull origin develop
```

### Conventional Commits

| Tipo | Uso | Ejemplo |
|------|-----|---------|
| `feat` | Nueva funcionalidad | `feat(auth): add JWT validation` |
| `fix` | Bug fix | `fix(api): handle null response` |
| `docs` | Documentación | `docs: update README` |
| `chore` | Mantenimiento | `chore: update dependencies` |
| `test` | Tests | `test(collector): add unit tests` |

---

## 📖 Documentación Clave

| Archivo | Descripción | Cuándo leerlo |
|---------|-------------|---------------|
| `TASK.md` | **📍 Fuente de verdad para tareas** | Primero |
| `docs/product/PRD.md` | Requisitos del producto | Para entender el "por qué" |
| `docs/technical/ARCHITECTURE.md` | Arquitectura técnica | Para entender el "cómo" |
| `docs/sop/agents.md` | Ejecución de los 9 agentes | Antes de codear agents |
| `docs/sop/fact-checking.md` | Procedimiento de verificación | Para Agent 3 |
| `docs/sop/data-collection.md` | Scraping INDEC/BCRA | Para Agent 1 |

---

## 🤖 Usar task-prompt-engineer

El script `task-prompt-engineer` genera prompts detallados para cada subtask:

```bash
# Generar prompt para una sección
python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2

# Generar prompt para una subtask específica
python3 global_skills/task-prompt-engineer/scripts/prompt_generator.py 0.2.1
```

El prompt generado incluye:
- Contexto específico de la subtask
- Skills recomendadas
- Criterios de aceptación
- Comandos a ejecutar

---

## 🎯 Empezar a Trabajar

1. **Leer `TASK.md`** para entender el estado actual
2. **Elegir una subtask** de FASE 0 (setup inicial)
3. **Generar prompt** con `task-prompt-engineer`
4. **Crear rama feature** siguiendo el Git Workflow
5. **Ejecutar con Kilo CLI** o manualmente
6. **Commitear y crear PR** cuando la sección esté completa

---

## 🆘 Troubleshooting

| Problema | Solución |
|----------|----------|
| `pnpm install` falla | Verificar Node 20+: `node -v` |
| Redis no conecta | `redis-server --daemonize yes` |
| Tests fallan | Verificar `.env` configurado |
| Linting errors | `pnpm format` luego `pnpm lint --fix` |
| Type errors | `pnpm typecheck` para ver detalles |

---

## 📞 Contacto

- **Autor:** Mauro Ciappina
- **Repositorio:** [github.com/mauroociappina/dato](https://github.com/mauroociappina/dato)
- **Kilo CLI:** [kilo.ai](https://kilo.ai)

---

¡Bienvenido al equipo! 🎉
