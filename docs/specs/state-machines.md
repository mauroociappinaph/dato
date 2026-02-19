# State Machines - DATO

> **Relacionado:** [Database Schemas](database.md) | [Types](types.md)

## 5. State Machines

### 5.1 Claim Lifecycle

```
┌─────────────┐
│   CREATED   │ ← Usuario/Agente crea claim
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   PENDING   │ ← Esperando verificación
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  VERIFYING  │ ← Agent 3 procesando
└──────┬──────┘
       │
       ├─── success ──▶ ┌─────────────┐
       │                │  VERIFIED   │ ← Con veredicto
       │                └──────┬──────┘
       │                       │
       │                       ▼
       │                ┌─────────────┐
       │                │  PUBLISHED  │ ← En canales
       │                └─────────────┘
       │
       └─── failure ──▶ ┌─────────────┐
                        │   FAILED    │ ← Error, reintentar
                        └─────────────┘

Estados: CREATED → PENDING → VERIFYING → VERIFIED → PUBLISHED
                                        ↘ FAILED
```

### 5.2 Subscription Lifecycle

```
┌──────────────┐
│   trialing   │ ← 7 días gratis
└───────┬──────┘
        │
        ├─── payment ──▶ ┌──────────────┐
        │                 │    active    │ ← Suscripción activa
        │                 └───────┬──────┘
        │                         │
        │                         ├─── payment_failed ──▶ ┌──────────────┐
        │                         │                        │   past_due   │
        │                         │                        └───────┬──────┘
        │                         │                                │
        │                         │                                ├─── payment ──▶ active
        │                         │                                │
        │                         │                                └─── 7 days ──▶ canceled
        │                         │
        │                         ├─── incomplete ──▶ ┌──────────────┐
        │                         │                    │  incomplete  │ ← Pago pendiente
        │                         │                    └───────┬──────┘
        │                         │                            │
        │                         │                            └─── payment ──▶ active
        │                         │
        │                         └─── cancel ──▶ ┌──────────────┐
        │                                          │   canceled   │ ← Cancelado
        │                                          └──────────────┘
        │
        └─── no_payment ──▶ ┌──────────────┐
                            │     FREE     │
                            └──────────────┘

Estados: trialing → active → canceled
                  ↘ past_due → active
                            ↘ canceled
                  ↘ incomplete → active
```

### 5.3 Verification State

```
┌───────────────┐
│    QUEUED     │ ← En cola de procesamiento
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   FETCHING    │ ← Obteniendo datos de fuentes
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   ANALYZING   │ ← LLM procesando
└───────┬───────┘
        │
        ├─── confidence >= 0.85 ──▶ ┌───────────────┐
        │                            │    VERDADERO  │
        │                            │     or FALSO  │
        │                            └───────────────┘
        │
        ├─── confidence 0.70-0.84 ──▶ ┌───────────────┐
        │                              │ PARCIALMENTE_ │
        │                              │   VERDADERO   │
        │                              └───────────────┘
        │
        └─── confidence < 0.70 ────▶ ┌───────────────┐
                                     │  SIN_DATOS    │
                                     └───────────────┘
```

### 5.4 User Plan Limits

```typescript
// Finite State Machine para límites de plan

type PlanState = 'FREE' | 'PREMIUM' | 'PROFESSIONAL';
type VerificationEvent = 'VERIFY' | 'RESET' | 'UPGRADE' | 'DOWNGRADE';

interface PlanLimits {
  verificationsPerDay: number;
  alerts: number;
  historyDays: number;
  apiAccess: boolean;
  reports: boolean;
}

const PLAN_LIMITS: Record<PlanState, PlanLimits> = {
  FREE: {
    verificationsPerDay: 3,
    alerts: 0,
    historyDays: 7,
    apiAccess: false,
    reports: false,
  },
  PREMIUM: {
    verificationsPerDay: Infinity,
    alerts: 10,
    historyDays: 365,
    apiAccess: false,
    reports: false,
  },
  PROFESSIONAL: {
    verificationsPerDay: Infinity,
    alerts: Infinity,
    historyDays: Infinity,
    apiAccess: true,
    reports: true,
  },
};

function canVerify(user: User): boolean {
  const limits = PLAN_LIMITS[user.plan.toUpperCase() as PlanState];
  
  // Reset diario
  if (user.lastVerificationReset < new Date().setHours(0, 0, 0, 0)) {
    user.verificationsUsedToday = 0;
    user.lastVerificationReset = new Date();
  }
  
  return user.verificationsUsedToday < limits.verificationsPerDay;
}
```

---

