## 7. Error Codes

### 7.1 Error Code Registry

```typescript
// packages/types/src/errors.ts

export enum ErrorCode {
  // ============================================================================
  // AUTH ERRORS (AUTH-xxx)
  // ============================================================================
  AUTH_INVALID_CREDENTIALS = 'AUTH-001',
  AUTH_TOKEN_EXPIRED = 'AUTH-002',
  AUTH_TOKEN_INVALID = 'AUTH-003',
  AUTH_EMAIL_EXISTS = 'AUTH-004',
  AUTH_PASSWORD_WEAK = 'AUTH-005',
  AUTH_UNAUTHORIZED = 'AUTH-006',

  // ============================================================================
  // VALIDATION ERRORS (VAL-xxx)
  // ============================================================================
  VAL_INVALID_INPUT = 'VAL-001',
  VAL_MISSING_FIELD = 'VAL-002',
  VAL_INVALID_EMAIL = 'VAL-003',
  VAL_INVALID_DATE = 'VAL-004',
  VAL_STRING_TOO_LONG = 'VAL-005',
  VAL_STRING_TOO_SHORT = 'VAL-006',

  // ============================================================================
  // RATE LIMIT ERRORS (RATE-xxx)
  // ============================================================================
  RATE_LIMIT_EXCEEDED = 'RATE-001',
  RATE_DAILY_LIMIT = 'RATE-002',

  // ============================================================================
  // RESOURCE ERRORS (RES-xxx)
  // ============================================================================
  RES_NOT_FOUND = 'RES-001',
  RES_ALREADY_EXISTS = 'RES-002',
  RES_DELETED = 'RES-003',

  // ============================================================================
  // PERMISSION ERRORS (PERM-xxx)
  // ============================================================================
  PERM_DENIED = 'PERM-001',
  PERM_UPGRADE_REQUIRED = 'PERM-002',
  PERM_FEATURE_LOCKED = 'PERM-003',

  // ============================================================================
  // BILLING ERRORS (BIL-xxx)
  // ============================================================================
  BIL_PAYMENT_FAILED = 'BIL-001',
  BIL_SUBSCRIPTION_INACTIVE = 'BIL-002',
  BIL_ALREADY_SUBSCRIBED = 'BIL-003',
  BIL_NO_SUBSCRIPTION = 'BIL-004',

  // ============================================================================
  // AGENT ERRORS (AGT-xxx)
  // ============================================================================
  AGT_PROCESSING_FAILED = 'AGT-001',
  AGT_TIMEOUT = 'AGT-002',
  AGT_LOW_CONFIDENCE = 'AGT-003',
  AGT_NO_DATA = 'AGT-004',

  // ============================================================================
  // EXTERNAL SERVICE ERRORS (EXT-xxx)
  // ============================================================================
  EXT_LLM_ERROR = 'EXT-001',
  EXT_DATABASE_ERROR = 'EXT-002',
  EXT_CACHE_ERROR = 'EXT-003',
  EXT_VECTOR_DB_ERROR = 'EXT-004',

  // ============================================================================
  // INTERNAL ERRORS (INT-xxx)
  // ============================================================================
  INT_INTERNAL_ERROR = 'INT-001',
  INT_CONFIGURATION_ERROR = 'INT-002',
  INT_UNAVAILABLE = 'INT-003',
}

export interface AppError {
  code: ErrorCode;
  message: string;
  details?: Record<string, unknown>;
  retryable: boolean;
  httpStatus: number;
}

export const ERROR_REGISTRY: Record<ErrorCode, AppError> = {
  // Auth
  [ErrorCode.AUTH_INVALID_CREDENTIALS]: {
    code: ErrorCode.AUTH_INVALID_CREDENTIALS,
    message: 'Credenciales inválidas',
    httpStatus: 401,
    retryable: false,
  },
  [ErrorCode.AUTH_TOKEN_EXPIRED]: {
    code: ErrorCode.AUTH_TOKEN_EXPIRED,
    message: 'Sesión expirada',
    httpStatus: 401,
    retryable: true,
  },
  [ErrorCode.AUTH_TOKEN_INVALID]: {
    code: ErrorCode.AUTH_TOKEN_INVALID,
    message: 'Token inválido',
    httpStatus: 401,
    retryable: false,
  },
  [ErrorCode.AUTH_EMAIL_EXISTS]: {
    code: ErrorCode.AUTH_EMAIL_EXISTS,
    message: 'El email ya está registrado',
    httpStatus: 409,
    retryable: false,
  },
  [ErrorCode.AUTH_PASSWORD_WEAK]: {
    code: ErrorCode.AUTH_PASSWORD_WEAK,
    message: 'La contraseña no cumple los requisitos',
    httpStatus: 400,
    retryable: false,
  },
  [ErrorCode.AUTH_UNAUTHORIZED]: {
    code: ErrorCode.AUTH_UNAUTHORIZED,
    message: 'No autorizado',
    httpStatus: 401,
    retryable: false,
  },

  // Validation
  [ErrorCode.VAL_INVALID_INPUT]: {
    code: ErrorCode.VAL_INVALID_INPUT,
    message: 'Datos inválidos',
    httpStatus: 400,
    retryable: false,
  },
  [ErrorCode.VAL_MISSING_FIELD]: {
    code: ErrorCode.VAL_MISSING_FIELD,
    message: 'Campo requerido faltante',
    httpStatus: 400,
    retryable: false,
  },
  [ErrorCode.VAL_INVALID_EMAIL]: {
    code: ErrorCode.VAL_INVALID_EMAIL,
    message: 'Email inválido',
    httpStatus: 400,
    retryable: false,
  },
  [ErrorCode.VAL_INVALID_DATE]: {
    code: ErrorCode.VAL_INVALID_DATE,
    message: 'Fecha inválida',
    httpStatus: 400,
    retryable: false,
  },
  [ErrorCode.VAL_STRING_TOO_LONG]: {
    code: ErrorCode.VAL_STRING_TOO_LONG,
    message: 'Texto demasiado largo',
    httpStatus: 400,
    retryable: false,
  },
  [ErrorCode.VAL_STRING_TOO_SHORT]: {
    code: ErrorCode.VAL_STRING_TOO_SHORT,
    message: 'Texto demasiado corto',
    httpStatus: 400,
    retryable: false,
  },

  // Rate Limit
  [ErrorCode.RATE_LIMIT_EXCEEDED]: {
    code: ErrorCode.RATE_LIMIT_EXCEEDED,
    message: 'Límite de requests excedido',
    httpStatus: 429,
    retryable: true,
  },
  [ErrorCode.RATE_DAILY_LIMIT]: {
    code: ErrorCode.RATE_DAILY_LIMIT,
    message: 'Límite diario de verificaciones excedido',
    httpStatus: 429,
    retryable: true,
    details: { resetAt: 'next_day' },
  },

  // Resource
  [ErrorCode.RES_NOT_FOUND]: {
    code: ErrorCode.RES_NOT_FOUND,
    message: 'Recurso no encontrado',
    httpStatus: 404,
    retryable: false,
  },
  [ErrorCode.RES_ALREADY_EXISTS]: {
    code: ErrorCode.RES_ALREADY_EXISTS,
    message: 'El recurso ya existe',
    httpStatus: 409,
    retryable: false,
  },
  [ErrorCode.RES_DELETED]: {
    code: ErrorCode.RES_DELETED,
    message: 'El recurso fue eliminado',
    httpStatus: 410,
    retryable: false,
  },

  // Permission
  [ErrorCode.PERM_DENIED]: {
    code: ErrorCode.PERM_DENIED,
    message: 'Acceso denegado',
    httpStatus: 403,
    retryable: false,
  },
  [ErrorCode.PERM_UPGRADE_REQUIRED]: {
    code: ErrorCode.PERM_UPGRADE_REQUIRED,
    message: 'Esta funcionalidad requiere un plan superior',
    httpStatus: 402,
    retryable: false,
  },
  [ErrorCode.PERM_FEATURE_LOCKED]: {
    code: ErrorCode.PERM_FEATURE_LOCKED,
    message: 'Funcionalidad no disponible en tu plan',
    httpStatus: 403,
    retryable: false,
  },

  // Billing
  [ErrorCode.BIL_PAYMENT_FAILED]: {
    code: ErrorCode.BIL_PAYMENT_FAILED,
    message: 'Pago rechazado',
    httpStatus: 402,
    retryable: true,
  },
  [ErrorCode.BIL_SUBSCRIPTION_INACTIVE]: {
    code: ErrorCode.BIL_SUBSCRIPTION_INACTIVE,
    message: 'Suscripción inactiva',
    httpStatus: 402,
    retryable: true,
  },
  [ErrorCode.BIL_ALREADY_SUBSCRIBED]: {
    code: ErrorCode.BIL_ALREADY_SUBSCRIBED,
    message: 'Ya tienes una suscripción activa',
    httpStatus: 409,
    retryable: false,
  },
  [ErrorCode.BIL_NO_SUBSCRIPTION]: {
    code: ErrorCode.BIL_NO_SUBSCRIPTION,
    message: 'No tienes una suscripción activa',
    httpStatus: 404,
    retryable: false,
  },

  // Agent
  [ErrorCode.AGT_PROCESSING_FAILED]: {
    code: ErrorCode.AGT_PROCESSING_FAILED,
    message: 'Error procesando solicitud',
    httpStatus: 500,
    retryable: true,
  },
  [ErrorCode.AGT_TIMEOUT]: {
    code: ErrorCode.AGT_TIMEOUT,
    message: 'Tiempo de espera agotado',
    httpStatus: 504,
    retryable: true,
  },
  [ErrorCode.AGT_LOW_CONFIDENCE]: {
    code: ErrorCode.AGT_LOW_CONFIDENCE,
    message: 'Resultado con baja confianza',
    httpStatus: 200,
    retryable: true,
  },
  [ErrorCode.AGT_NO_DATA]: {
    code: ErrorCode.AGT_NO_DATA,
    message: 'No hay datos disponibles',
    httpStatus: 200,
    retryable: true,
  },

  // External
  [ErrorCode.EXT_LLM_ERROR]: {
    code: ErrorCode.EXT_LLM_ERROR,
    message: 'Error en servicio de IA',
    httpStatus: 502,
    retryable: true,
  },
  [ErrorCode.EXT_DATABASE_ERROR]: {
    code: ErrorCode.EXT_DATABASE_ERROR,
    message: 'Error en base de datos',
    httpStatus: 503,
    retryable: true,
  },
  [ErrorCode.EXT_CACHE_ERROR]: {
    code: ErrorCode.EXT_CACHE_ERROR,
    message: 'Error en cache',
    httpStatus: 503,
    retryable: true,
  },
  [ErrorCode.EXT_VECTOR_DB_ERROR]: {
    code: ErrorCode.EXT_VECTOR_DB_ERROR,
    message: 'Error en base vectorial',
    httpStatus: 503,
    retryable: true,
  },

  // Internal
  [ErrorCode.INT_INTERNAL_ERROR]: {
    code: ErrorCode.INT_INTERNAL_ERROR,
    message: 'Error interno del servidor',
    httpStatus: 500,
    retryable: true,
  },
  [ErrorCode.INT_CONFIGURATION_ERROR]: {
    code: ErrorCode.INT_CONFIGURATION_ERROR,
    message: 'Error de configuración',
    httpStatus: 500,
    retryable: false,
  },
  [ErrorCode.INT_UNAVAILABLE]: {
    code: ErrorCode.INT_UNAVAILABLE,
    message: 'Servicio no disponible',
    httpStatus: 503,
    retryable: true,
  },
};

export function getError(code: ErrorCode, details?: Record<string, unknown>): AppError {
  const error = ERROR_REGISTRY[code];
  return {
    ...error,
    details: { ...error.details, ...details },
  };
}
```

### 7.2 HTTP Status Code Mapping

```
2xx Success
├── 200 OK                 → Request exitoso
├── 201 Created            → Recurso creado
└── 204 No Content         → Eliminado sin respuesta

4xx Client Errors
├── 400 Bad Request        → VAL-xxx
├── 401 Unauthorized       → AUTH-xxx
├── 402 Payment Required   → PERM-002, BIL-xxx
├── 403 Forbidden          → PERM-xxx
├── 404 Not Found          → RES-001
├── 409 Conflict           → RES-002, AUTH-004, BIL-003
├── 410 Gone               → RES-003
├── 422 Unprocessable      → VAL-xxx
└── 429 Too Many Requests  → RATE-xxx

5xx Server Errors
├── 500 Internal Error     → INT-001
├── 502 Bad Gateway        → EXT-001
├── 503 Unavailable        → EXT-002, EXT-003, EXT-004, INT-003
├── 504 Gateway Timeout    → AGT-002
```

---

