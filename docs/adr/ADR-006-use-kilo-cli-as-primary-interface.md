# ADR-006: Use Kilo CLI as Primary Interface

**Status:** Accepted

**Date:** 2024-02-12

## Context

DATO necesita una interfaz unificada para:
- Gestión de MCP servers
- Orquestación de agentes
- Session management
- Soporte multi-modelo LLM

Opciones consideradas:
1. Custom CLI con Node.js
2. Scripts shell individuales
3. Kilo CLI (opencode)
4. LangChain/LangGraph

## Decision

Usar **Kilo CLI** como interfaz primaria para:
- MCP server management
- Session management
- Agent orchestration
- Multi-provider LLM support

### Configuración Centralizada

Archivo único: `opencode.json` con toda la configuración de:
- MCP servers
- LLM providers
- Environment variables
- Session settings

## Consequences

### Positivas

- Archivo de configuración único
- Built-in MCP support
- Session persistence
- Multi-model support
- CLI intuitivo
- Active development

### Negativas

- Learning curve para nuevo tool
- Dependencia de herramienta externa
- Potential breaking changes
- Limited documentation

## Kilo Commands

```bash
# Iniciar Kilo
kilo

# Listar MCP servers
kilo mcp list

# Ejecutar con mensaje
kilo run "Analiza inflación del INDEC"

# Continuar sesión
kilo -c
```

## Session Management

Kilo maneja sessions automáticamente:
- Persistencia de contexto
- History de conversaciones
- Multi-turn interactions

## Related

- ADR-005: Use MCP Servers for Infrastructure
