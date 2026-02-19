# Documentación - DATO

> Índice central de documentación del proyecto

---

> **⚠️ IMPORTANTE:** Todas las acciones relacionadas con GitHub (crear repositorios, issues, PRs, commits, etc.) deben realizarse exclusivamente mediante **GitHub MCP (Kilo CLI)**. No usar comandos git directos ni la interfaz web de GitHub para operaciones que puedan automatizarse.
>
> Ejemplo: `"Crear repositorio dato en GitHub..."` → usar GitHub MCP vía Kilo CLI.

---

## Estructura

```
docs/
├── product/        # Documentación de producto
├── technical/      # Documentación técnica
├── specs/          # Especificaciones técnicas
├── sop/            # Procedimientos operativos
├── brand/          # Manual de marca
├── guides/         # Guías de desarrollo
└── archive/        # Documentación histórica
```

---

## Producto

| Archivo | Descripción |
|---------|-------------|
| [PRD.md](product/PRD.md) | Requisitos del producto, objetivos, métricas |
| [USER_STORIES.md](product/USER_STORIES.md) | Historias de usuario con Gherkin (49 escenarios) |
| [ROADMAP.md](product/ROADMAP.md) | Timeline, fases, milestones |

## Técnica

| Archivo | Descripción |
|---------|-------------|
| [ARCHITECTURE.md](technical/ARCHITECTURE.md) | Arquitectura de 7 agentes, MCP, multi-LLM |
| [API.md](technical/API.md) | Fuentes de datos, endpoints internos |
| [TASK.md](../TASK.md) | Tareas pendientes, bloqueadores |

## Especificaciones

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| [database.md](specs/database.md) | 235 | Schemas SQL completos (9 tablas) |
| [types.md](specs/types.md) | 500 | TypeScript types e interfaces |
| [api-contracts.md](specs/api-contracts.md) | 971 | OpenAPI 3.1 specification |
| [agents.md](specs/agents.md) | 520 | Especificaciones de los 7 agentes IA |
| [state-machines.md](specs/state-machines.md) | 155 | Diagramas de estado (claims, subscriptions) |
| [validation.md](specs/validation.md) | 203 | Zod schemas, rate limits, permissions |
| [errors.md](specs/errors.md) | 356 | Códigos de error (30+) y HTTP mapping |
| [config.md](specs/config.md) | 238 | Environment variables, LLM config, features |

## Procedimientos (SOP)

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| [development.md](sop/development.md) | 149 | Git workflow, commits, code review, testing |
| [agents.md](sop/agents.md) | 266 | Ejecución de los 7 agentes IA |
| [fact-checking.md](sop/fact-checking.md) | 71 | Procedimiento de verificación manual |
| [data-collection.md](sop/data-collection.md) | 101 | Scraping INDEC, BCRA, YouTube |
| [deploy.md](sop/deploy.md) | 108 | Deploy a Vercel/Railway, rollback |
| [incidents.md](sop/incidents.md) | 127 | Clasificación, escalación, post-mortem |
| [publishing.md](sop/publishing.md) | 107 | Publicación en canales (Twitter, Telegram) |
| [billing.md](sop/billing.md) | 157 | Gestión de suscripciones, pagos, dunning |

## Marca

| Archivo | Descripción |
|---------|-------------|
| [BRAND.md](brand/BRAND.md) | Manual de marca, colores, tipografía, tono |

## Guías

| Archivo | Descripción |
|---------|-------------|
| [DEVELOPMENT.md](guides/DEVELOPMENT.md) | Setup, estructura, comandos |

---

## Resumen de Tamaño

| Categoría | Archivos | Líneas totales |
|-----------|----------|----------------|
| specs/ | 8 | 3,178 |
| sop/ | 8 | 1,086 |
| product/ | 3 | 1,148 |
| technical/ | 3 | 1,566 |
| brand/ | 1 | 351 |
| guides/ | 1 | 567 |
| **Total** | **24** | **8,896** |

---

## Quick Links

- [Volver al README principal](../README.md)
- [Contributing](../CONTRIBUTING.md)
- [Changelog](../CHANGELOG.md)
