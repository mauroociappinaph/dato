# ADR-005: Use MCP Servers for Infrastructure

**Status:** Accepted

**Date:** 2024-02-10

## Context

DATO necesita múltiples capacidades de infraestructura:
- Web scraping (INDEC, BCRA, fuentes oficiales)
- Búsqueda web (noticias políticas)
- Base de datos vectorial (RAG para fact-checking)
- Base de datos SQL (datos usuarios, claims)
- AI tracing (debugging agentes)
- CI/CD (GitHub operations)

Opciones:
1. Implementar todo custom
2. Usar SaaS individuales con SDKs
3. Usar MCP Servers (Model Context Protocol)

## Decision

Usar **MCP Servers** via Kilo CLI para toda la infraestructura:

| Capacidad | MCP Server | Propósito |
|-----------|------------|-----------|
| Web Scraping | firecrawl | Scrapear INDEC, BCRA |
| Web Search | exa | Buscar noticias |
| Vector DB | pinecone | RAG fact-checking |
| Database | supabase | DB principal |
| AI Tracing | langsmith | Debug agentes |
| CI/CD | github | PRs, Issues |
| Reasoning | sequential-thinking | Razonamiento IA |
| Cache | redis | Cache datos |

## Consequences

### Positivas

- Zero código de infraestructura
- Pre-configurado y listo
- Actualizaciones automáticas via npx
- Interfaz unificada via Kilo CLI
- Comunidad activa de MCP
- Documentación extensa

### Negativas

- Dependencias externas
- Customización limitada
- Potential latency por capa adicional
- Vendor dependencies

## MCP Servers Configuration

```json
{
  "mcp": {
    "firecrawl": {
      "type": "local",
      "command": ["npx", "-y", "firecrawl-mcp"],
      "environment": { "FIRECRAWL_API_KEY": "xxx" }
    },
    "pinecone": {
      "type": "local",
      "command": ["npx", "-y", "@pinecone-database/mcp"],
      "environment": { "PINECONE_API_KEY": "xxx" }
    }
  }
}
```

## Related

- ADR-001: Use Supabase for Backend
- ADR-006: Use Kilo CLI as Primary Interface
