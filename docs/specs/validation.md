## 6. Validation Rules

### 6.1 Input Validation

```typescript
// packages/types/src/validation.ts

import { z } from 'zod';

// ============================================================================
// AUTH VALIDATION
// ============================================================================

export const RegisterSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string()
    .min(8, 'Mínimo 8 caracteres')
    .regex(/[A-Z]/, 'Al menos una mayúscula')
    .regex(/[a-z]/, 'Al menos una minúscula')
    .regex(/[0-9]/, 'Al menos un número'),
  fullName: z.string().min(2).max(100).optional(),
});

export const LoginSchema = z.object({
  email: z.string().email('Email inválido'),
  password: z.string().min(1, 'Contraseña requerida'),
});

// ============================================================================
// CLAIM VALIDATION
// ============================================================================

export const CreateClaimSchema = z.object({
  claimText: z.string()
    .min(10, 'Mínimo 10 caracteres')
    .max(1000, 'Máximo 1000 caracteres'),
  speaker: z.string().min(2, 'Speaker requerido').max(200),
  speakerParty: z.string().max(100).optional(),
  speakerRole: z.string().max(100).optional(),
  sourceType: z.enum(['speech', 'interview', 'social_media', 'news', 'official']),
  sourceUrl: z.string().url().optional(),
  sourceTitle: z.string().max(500).optional(),
  context: z.string().max(1000).optional(),
  category: z.enum(['economy', 'politics', 'social', 'international', 'other']),
  dateSaid: z.string().refine((val) => !isNaN(Date.parse(val)), {
    message: 'Fecha inválida',
  }),
});

export const SearchClaimsSchema = z.object({
  q: z.string().min(3, 'Mínimo 3 caracteres').max(200),
  speaker: z.string().max(200).optional(),
  category: z.enum(['economy', 'politics', 'social', 'international', 'other']).optional(),
  verdict: z.enum(['VERDADERO', 'FALSO', 'PARCIALMENTE_VERDADERO', 'SIN_DATOS']).optional(),
  dateFrom: z.string().datetime().optional(),
  dateTo: z.string().datetime().optional(),
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

// ============================================================================
// VERIFICATION VALIDATION
// ============================================================================

export const VerifyClaimSchema = z.object({
  claimId: z.string().uuid('ID inválido'),
});

// ============================================================================
// ALERT VALIDATION
// ============================================================================

export const CreateAlertSchema = z.object({
  type: z.enum(['speaker', 'topic', 'category', 'indicator']),
  value: z.string().min(1).max(200),
  channels: z.array(z.enum(['push', 'email', 'telegram'])).default(['push']),
});

// ============================================================================
// BILLING VALIDATION
// ============================================================================

export const CheckoutSchema = z.object({
  plan: z.enum(['premium', 'professional']),
  successUrl: z.string().url().optional(),
  cancelUrl: z.string().url().optional(),
});

// ============================================================================
// SANITIZATION
// ============================================================================

export function sanitizeInput(input: string): string {
  return input
    .trim()
    .replace(/<[^>]*>/g, '') // Remove HTML tags
    .replace(/javascript:/gi, '') // Remove javascript:
    .replace(/on\w+=/gi, ''); // Remove event handlers
}

export function sanitizeClaimText(text: string): string {
  return sanitizeInput(text)
    .replace(/[^\w\sáéíóúñüÁÉÍÓÚÑÜ.,;:!?¿¡"'\-()]/g, '');
}
```

### 6.2 Rate Limits

```yaml
# Configuración de rate limiting

rate_limits:
  # Por endpoint
  /api/v1/feed:
    free: 60/minute
    premium: 300/minute
    professional: 1000/minute
    
  /api/v1/claims/verify:
    free: 3/day
    premium: unlimited
    professional: unlimited
    
  /api/v1/search:
    free: 30/minute
    premium: 120/minute
    professional: 500/minute
    
  /api/v1/dashboard:
    professional: 100/minute

  # Por IP (sin auth)
  default:
    100/minute

# Implementación
storage: redis
key_format: "ratelimit:{user_id}:{endpoint}"
headers:
  - X-RateLimit-Limit
  - X-RateLimit-Remaining
  - X-RateLimit-Reset
```

### 6.3 Permission Matrix

```typescript
// packages/types/src/permissions.ts

type Permission = 
  | 'feed:read'
  | 'claims:read'
  | 'claims:verify'
  | 'search:basic'
  | 'search:advanced'
  | 'alerts:create'
  | 'alerts:manage'
  | 'history:read'
  | 'api:access'
  | 'reports:generate'
  | 'dashboard:access'
  // Admin permissions
  | 'admin:users:read'
  | 'admin:users:write'
  | 'admin:metrics:read'
  | 'admin:claims:moderate';

const PERMISSIONS: Record<Plan, Set<Permission>> = {
  free: new Set([
    'feed:read',
    'claims:read',
    'claims:verify', // limited
    'search:basic',
  ]),
  
  premium: new Set([
    'feed:read',
    'claims:read',
    'claims:verify',
    'search:basic',
    'search:advanced',
    'alerts:create',      // max 10 alerts
    'alerts:manage',      // max 10 alerts
    'history:read',
  ]),
  
  professional: new Set([
    'feed:read',
    'claims:read',
    'claims:verify',
    'search:basic',
    'search:advanced',
    'alerts:create',
    'alerts:manage',
    'history:read',
    'api:access',
    'reports:generate',
    'dashboard:access',
  ]),
};

const ROLE_PERMISSIONS: Record<UserRole, Set<Permission>> = {
  user: new Set(), // Uses plan permissions
  admin: new Set([
    // All plan permissions (inherited)
    'feed:read',
    'claims:read',
    'claims:verify',
    'search:basic',
    'search:advanced',
    'alerts:create',
    'alerts:manage',
    'history:read',
    'api:access',
    'reports:generate',
    'dashboard:access',
    // Admin-only permissions
    'admin:users:read',
    'admin:users:write',
    'admin:metrics:read',
    'admin:claims:moderate',
  ]),
};

export function hasPermission(user: User, permission: Permission): boolean {
  // Admin has all permissions
  if (user.role === 'admin') {
    return ROLE_PERMISSIONS.admin.has(permission);
  }
  // Regular users use plan permissions
  return PERMISSIONS[user.plan].has(permission);
}

export function hasRole(user: User, role: UserRole): boolean {
  return user.role === role;
}
```

---

