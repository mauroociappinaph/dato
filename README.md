# DATO

> Política argentina verificada con datos reales

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0+-blue.svg)](https://www.typescriptlang.org/)
[![NestJS](https://img.shields.io/badge/NestJS-10+-red.svg)](https://nestjs.com/)
[![Kilo CLI](https://img.shields.io/badge/Kilo_CLI-1.0+-purple.svg)](https://kilo.ai)

> **⚠️ OPERACIONES GITHUB:** Todas las acciones de GitHub en este proyecto (crear repositorios, issues, PRs, branches, etc.) deben realizarse mediante **GitHub MCP (Kilo CLI)**.
>
> Ejemplo: `kilo run "Crear repositorio dato en GitHub..."`

## Descripción

**DATO** es una plataforma de inteligencia política y económica que traduce la complejidad de Argentina a datos verificables y lenguaje simple.

### Promesa de marca

> "No opiniones. Datos."

---

## Características principales

### 1. Noticias políticas y económicas de Argentina

- Resumen diario automático
- Solo temas relevantes (leyes, inflación, dólar, medidas, elecciones)
- Sin ruido mediático

### 2. Verificación de veracidad (Feature diferencial)

- Detecta frases de políticos
- Busca datos oficiales, estadísticas, antecedentes históricos
- Devuelve: `Verdadero / Engañoso / Falso`
- Explicación en lenguaje simple

### 3. Explicaciones simples

- Traduce economía y política a lenguaje cotidiano
- Ejemplos reales, sin tecnicismos

**Ejemplo:**

| Técnico | Simple |
|---------|--------|
| "Déficit fiscal primario del 2,1% del PBI" | "El Estado gastó más de lo que le entró. Por cada $100 que recibió, gastó $102." |

---

## Tech Stack

| Categoría | Tecnología |
|-----------|------------|
| **Backend** | NestJS, Prisma ORM |
| **Frontend** | Next.js, React, Zustand |
| **Base de datos** | Supabase (PostgreSQL) |
| **Vector DB** | Pinecone |
| **Cache** | Redis |
| **IA** | NVIDIA NIM, Mistral, Groq, OpenRouter |
| **CLI** | Kilo CLI |
| **MCP Servers** | Supabase, Pinecone, Firecrawl, Exa, GitHub, LangSmith |
| **Pagos** | Mercado Pago / Stripe |
| **Datos** | INDEC, BCRA, Senado, Diputados, Boletín Oficial |

---

## Quick Start

```bash
# Clonar el repositorio
git clone https://github.com/mauroociappina/dato.git
cd dato

# Instalar dependencias
pnpm install

# Configurar variables de entorno
cp .env.example .env

# Iniciar Redis
redis-server --daemonize yes

# Ejecutar con Kilo CLI
kilo
```

---

## Documentación

### Producto

| Archivo | Descripción |
|---------|-------------|
| [PRD.md](docs/product/PRD.md) | Requisitos del producto |
| [USER_STORIES.md](docs/product/USER_STORIES.md) | Historias de usuario con Gherkin |
| [ROADMAP.md](docs/product/ROADMAP.md) | Timeline y fases |

### Técnica

| Archivo | Descripción |
|---------|-------------|
| [ARCHITECTURE.md](docs/technical/ARCHITECTURE.md) | Arquitectura técnica + MCP + LLM |
| [API.md](docs/technical/API.md) | Fuentes de datos y endpoints |
| [TASK.md](./TASK.md) | Tareas pendientes |

### Especificaciones

| Archivo | Descripción |
|---------|-------------|
| [database.md](docs/specs/database.md) | Schemas SQL |
| [types.md](docs/specs/types.md) | TypeScript types |
| [api-contracts.md](docs/specs/api-contracts.md) | OpenAPI specification |
| [agents.md](docs/specs/agents.md) | Especificaciones de los 7 agentes |
| [state-machines.md](docs/specs/state-machines.md) | Diagramas de estado |
| [validation.md](docs/specs/validation.md) | Reglas de validación |
| [errors.md](docs/specs/errors.md) | Códigos de error |
| [config.md](docs/specs/config.md) | Configuración |

### Procedimientos (SOP)

| Archivo | Descripción |
|---------|-------------|
| [development.md](docs/sop/development.md) | Git workflow, code review, testing |
| [agents.md](docs/sop/agents.md) | Ejecución de los 7 agentes |
| [fact-checking.md](docs/sop/fact-checking.md) | Procedimiento de verificación |
| [data-collection.md](docs/sop/data-collection.md) | Scraping INDEC/BCRA |
| [deploy.md](docs/sop/deploy.md) | Deploy a Vercel/Railway |
| [incidents.md](docs/sop/incidents.md) | Manejo de incidentes |
| [publishing.md](docs/sop/publishing.md) | Publicación en canales |
| [billing.md](docs/sop/billing.md) | Gestión de pagos |

### Marca y Guías

| Archivo | Descripción |
|---------|-------------|
| [BRAND.md](docs/brand/BRAND.md) | Manual de marca |
| [DEVELOPMENT.md](docs/guides/DEVELOPMENT.md) | Guía de desarrollo |

---

## Arquitectura

DATO funciona como un sistema de 9 agentes de IA que producen información confiable automáticamente:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    ENTRADAS     │────▶│ PROCESAMIENTO IA │────▶│     SALIDA      │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│ Datos oficiales │     │ 9 Agentes:       │     │ Feed diario     │
│ Noticias        │     │ • Recolector     │     │ Fact-checks     │
│ Discursos       │     │ • Extractor      │     │ Reportes PDF    │
│ Videos YouTube  │     │ • Verificador    │     │ Dashboard B2B   │
└─────────────────┘     │ • Simplificador  │     └─────────────────┘
                        │ • Publisher      │
                        │ • Billing        │
                        │ • Learning       │
                        │ • QA             │
                        │ • Growth         │
                        └──────────────────┘
```

Ver [ARCHITECTURE.md](docs/technical/ARCHITECTURE.md) para detalles completos.

---

## Roadmap

| Fase | Tiempo | Entregables |
|------|--------|-------------|
| **Fase 1** | 30 días | Feed resumido, Verificación básica, Explicación simple |
| **Fase 2** | 60 días | Búsqueda, Notificaciones, Mejor IA |
| **Fase 3** | 90+ días | Suscripción, Dashboard profesional B2B |

Ver [ROADMAP.md](docs/product/ROADMAP.md) para detalles.

---

## Contribuir

Las contribuciones son bienvenidas. Ver [CONTRIBUTING.md](./CONTRIBUTING.md) para:

- Fork & Branch workflow
- Convenciones de código
- Proceso de PR

---

## Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](./LICENSE) para más detalles.

---

## Contacto

**Autor:** Mauro Ciappina

**Proyecto:** [https://github.com/mauroociappina/dato](https://github.com/mauroociappina/dato)

**Kilo CLI:** [https://kilo.ai](https://kilo.ai)
