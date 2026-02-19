# ADR-003: Event-Driven Agent Communication

**Status:** Accepted

**Date:** 2024-01-20

## Context

Los 7 agentes de DATO necesitan comunicarse de forma asíncrona:
- Agent 1 → Agent 2 (datos crudos → claims)
- Agent 2 → Agent 3 (claims → verificación)
- Agent 3 → Agent 4 (verificación → simplificación)
- Agent 4 → Agent 5 (contenido → publicación)
- Agent 5 → Agent 6 (evento → billing)
- Todos → Agent 7 (métricas → learning)

Opciones consideradas:
1. Sync HTTP calls entre agentes
2. Event queue (BullMQ)
3. Message broker (RabbitMQ/Kafka)
4. Serverless functions con colas nativas

## Decision

Usar **BullMQ** con Redis como event queue para comunicación entre agentes.

## Consequences

### Positivas

- Escalabilidad horizontal
- Fault tolerance (reintentos automáticos)
- Observabilidad (Bull Board)
- Priorización de jobs
- Delayed jobs
- Rate limiting nativo

### Negativas

- Complejidad en debugging
- Necesidad de Redis
- No hay ordering garantizado
- Potential message loss si Redis falla

## Architecture

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
│ Agent 1 │───▶│  Queue  │───▶│ Agent 2 │───▶│  Queue  │
│Collector│    │ (BullMQ)│    │Extractor│    │ (BullMQ)│
└─────────┘    └─────────┘    └─────────┘    └─────────┘
```

## Queue Configuration

```typescript
const queue = new Queue('claims-extraction', {
  defaultJobOptions: {
    attempts: 3,
    backoff: { type: 'exponential', delay: 1000 },
    removeOnComplete: 100,
    removeOnFail: 50
  }
});
```

## Related

- ADR-001: Use Supabase for Backend
