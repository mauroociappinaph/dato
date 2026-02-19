# ADR-001: Use Supabase for Backend

**Status:** Accepted

**Date:** 2024-01-15

## Context

DATO necesita un backend con autenticación, base de datos PostgreSQL, y almacenamiento de archivos. Las opciones consideradas fueron:

1. Supabase (PostgreSQL + Auth + Storage + Realtime)
2. PostgreSQL + Auth0 + S3 separados
3. Firebase (NoSQL)
4. Custom backend con NestJS + TypeORM

## Decision

Usar **Supabase** como backend unificado para:
- Base de datos PostgreSQL
- Autenticación (Auth)
- Almacenamiento de archivos (Storage)
- Realtime subscriptions

## Consequences

### Positivas

- Desarrollo más rápido (integrated solution)
- Auth built-in con OAuth providers
- Realtime subscriptions incluido
- Dashboard de administración
- Row Level Security (RLS) nativo
- Backups automáticos

### Negativas

- Vendor lock-in
- Limited customization vs custom backend
- Pricing scales con usage
- Dependencia de un proveedor

## Alternatives Considered

| Alternativa | Pros | Cons | Razón de rechazo |
|-------------|------|------|------------------|
| PostgreSQL + Auth0 + S3 | Full control | 3 servicios separados | Complejidad de integración |
| Firebase | Realtime nativo | NoSQL limita queries | Necesitamos SQL para datos económicos |
| Custom NestJS | Total control | Tiempo de desarrollo | No justificado para MVP |

## Related

- ADR-005: Use MCP Servers for Infrastructure
