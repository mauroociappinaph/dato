# Architecture Decision Records (ADRs)

Este directorio contiene los registros de decisiones arquitectónicas de DATO.

## Índice

| ADR | Título | Estado |
|-----|--------|--------|
| [ADR-001](ADR-001-use-supabase-for-backend.md) | Use Supabase for Backend | Accepted |
| [ADR-002](ADR-002-multi-llm-strategy.md) | Multi-LLM Strategy with Groq, NVIDIA, Mistral, OpenRouter | Accepted |
| [ADR-003](ADR-003-event-driven-agent-communication.md) | Event-Driven Agent Communication | Accepted |
| [ADR-004](ADR-004-groq-as-default-llm-provider.md) | Groq as Default LLM Provider | Accepted |
| [ADR-005](ADR-005-use-mcp-servers-for-infrastructure.md) | Use MCP Servers for Infrastructure | Accepted |
| [ADR-006](ADR-006-use-kilo-cli-as-primary-interface.md) | Use Kilo CLI as Primary Interface | Accepted |

## Formato ADR

Cada ADR sigue el formato estándar:

- **Título**: Nombre descriptivo de la decisión
- **Status**: Accepted, Proposed, Deprecated, Superseded
- **Context**: Situación que motivó la decisión
- **Decision**: La decisión tomada
- **Consequences**: Trade-offs y riesgos asumidos

## Crear Nuevo ADR

```bash
# Copiar template
cp docs/adr/ADR-000-template.md docs/adr/ADR-XXX-titulo.md

# Editar y actualizar índice
```
