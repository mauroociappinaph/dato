# SOP-008: Billing - DATO

## SOP-008: Billing

### 8.1 Flujos de Suscripción

#### Nueva Suscripción

```
Usuario selecciona plan
│
├── Crear checkout session (Stripe)
│   └── Redirigir a Stripe Checkout
│
├── Usuario completa pago
│   └── Stripe envía webhook
│
├── Webhook: checkout.session.completed
│   ├── Verificar firma
│   ├── Crear registro en DB
│   ├── Actualizar plan usuario
│   ├── Enviar email bienvenida
│   └── Activar features Premium
│
└── Usuario redirigido a app
    └── Mostrar confirmación
```

#### Cancelación

```
Usuario cancela desde settings
│
├── Marcar cancelación pendiente
├── Mantener acceso hasta fin de período
├── Enviar email confirmación
├── No ofrecer reembolso automático
│
└── Al fin de período
    ├── Downgrade a Free
    ├── Eliminar datos Premium
    └── Enviar email "Te extrañamos"
```

### 8.2 Manejo de Pagos Fallidos

#### Dunning Sequence

```
Día 0: Pago falla
├── Enviar email "Pago rechazado"
├── Reintento automático en 3 días
│
Día 3: Reintento 1
├── Si falla → Email "Problema con tu tarjeta"
├── Reintento en 5 días
│
Día 8: Reintento 2
├── Si falla → Email "Último aviso"
├── Reintento en 7 días
│
Día 15: Reintento 3 (final)
├── Si falla → Downgrade a Free
├── Email "Suscripción cancelada"
└── Guardar registro para reactivación
```

#### Email Templates

**Pago Rechazado:**
```
Asunto: Hubo un problema con tu pago

Hola [Nombre],

Tu pago de $[monto] fue rechazado por tu banco.

Para mantener tu acceso Premium, actualiza tu método de pago:
[Link a billing portal]

Si necesitas ayuda, respondé este email.

El equipo de DATO
```

**Suscripción Cancelada:**
```
Asunto: Tu suscripción Premium ha finalizado

Hola [Nombre],

Tu suscripción Premium finalizó el [fecha].

Te extrañamos. Si querés volver, reactivá tu cuenta:
[Link a reactivación]

Mientras tanto, seguís teniendo acceso al plan Free (3 verificaciones/día).

El equipo de DATO
```

### 8.3 Reembolsos

#### Política

| Situación | Reembolso |
|-----------|-----------|
| Dentro de 7 días, sin uso | 100% |
| Dentro de 7 días, con uso | Prorrateado |
| Después de 7 días | No reembolsable |
| Error de DATO | 100% |

#### Procedimiento

```
Solicitud de reembolso
│
├── Verificar elegibilidad
│   ├── Tiempo desde compra
│   ├── Uso del servicio
│   └── Motivo
│
├── Si elegible
│   ├── Procesar via Stripe Dashboard
│   ├── Actualizar DB
│   ├── Enviar email confirmación
│   └── Downgrade a Free
│
└── Si no elegible
    ├── Explicar política
    └── Ofrecer alternativas (extensión, etc.)
```

### 8.4 Webhook Events

| Evento | Acción |
|--------|--------|
| `checkout.session.completed` | Activar Premium |
| `customer.subscription.created` | Registrar en DB |
| `customer.subscription.updated` | Actualizar plan |
| `customer.subscription.deleted` | Programar downgrade |
| `invoice.paid` | Renovar acceso |
| `invoice.payment_failed` | Iniciar dunning |
| `charge.refunded` | Actualizar DB, notificar |

### 8.5 Mercado Pago Integration

#### Argentina-Specific Payment Method

```
Usuario selecciona plan (Argentina)
│
├── Crear preferencia (Mercado Pago)
│   └── Redirigir a MP Checkout
│
├── Usuario completa pago
│   └── MP envía webhook
│
├── Webhook: payment
│   ├── Verificar firma (x-signature)
│   ├── Validar payment_id
│   ├── Crear registro en DB
│   ├── Actualizar plan usuario
│   └── Enviar email confirmación
│
└── Usuario redirigido a app
```

#### Webhook Events

| Evento | Acción |
|--------|--------|
| `payment` | Verificar estado del pago |
| `status=approved` | Activar plan |
| `status=rejected` | Notificar usuario |
| `status=cancelled` | Cancelar proceso |

#### Configuración

```bash
# Variables de entorno
MERCADO_PAGO_ACCESS_TOKEN=xxx
MERCADO_PAGO_WEBHOOK_SECRET=xxx

# Webhook URL
https://api.dato.ar/webhooks/mercadopago
```

### 8.6 Token Usage Billing

#### Metered Billing

```
Token tracking por usuario
│
├── Cada request a LLM
│   ├── Registrar tokens usados
│   ├── Actualizar contador diario
│   └── Verificar límite del plan
│
├── Si excede límite
│   ├── Bloquear request
│   ├── Mostrar mensaje de upgrade
│   └── Ofrecer plan superior
│
└── Reset diario a medianoche (UTC-3)
```

#### Token Tracking

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `user_id` | UUID | Usuario |
| `date` | Date | Día del uso |
| `tokens_used` | Integer | Total tokens |
| `requests_count` | Integer | Número de requests |
| `cost_usd` | Decimal | Costo en USD |

#### Tabla de Tracking

```sql
CREATE TABLE token_usage (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  date DATE NOT NULL,
  tokens_used INTEGER DEFAULT 0,
  requests_count INTEGER DEFAULT 0,
  cost_usd DECIMAL(10,6) DEFAULT 0,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, date)
);
```

### 8.7 Plan Tiers

| Plan | Precio | Verificaciones/día | Tokens/día | Features |
|------|--------|-------------------|------------|----------|
| Free | $0 | 3 | 500 | Feed básico, búsquedas limitadas |
| Premium | $5/mes | 50 | 1000 | Feed completo, historial, alertas |
| Professional | $50/mes | Ilimitado | Ilimitado | API access, B2B dashboard, soporte |

#### Límites por Plan

```
Free:
├── 3 verificaciones/día
├── 500 tokens/día
├── Sin historial guardado
└── Sin alertas

Premium:
├── 50 verificaciones/día
├── 1000 tokens/día
├── Historial 30 días
├── Alertas por email
└── Sin API access

Professional:
├── Verificaciones ilimitadas
├── Tokens ilimitados
├── Historial completo
├── Alertas en tiempo real
├── API access (rate limit: 1000 req/hora)
└── Dashboard B2B
```

### 8.8 Métricas de Billing

| Métrica | Target | Frecuencia |
|---------|--------|------------|
| MRR | $500 (mes 3) | Diario |
| Churn | < 10% | Mensual |
| ARPU | $5 | Mensual |
| Payment success rate | > 95% | Semanal |
| Dunning recovery | > 50% | Mensual |
| Token cost/user | < $0.10 | Diario |

---

