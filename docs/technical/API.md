# API Documentation - DATO

## Overview

DATO integrates with multiple official and third-party APIs to collect, verify, and distribute political and economic information for Argentina.

---

## External APIs (Data Sources)

### 1. INDEC (Instituto Nacional de Estadística y Censos)

**Purpose:** Official economic statistics

**Data Available:**
- Inflation (IPC)
- Poverty rate
- Employment/unemployment
- GDP
- Trade balance

**Endpoint:** `https://www.indec.gob.ar/`

**Integration Method:** Web scraping or open data portal

**Rate Limit:** N/A (public data)

---

### 2. BCRA (Banco Central de la República Argentina)

**Purpose:** Monetary and exchange data

**Data Available:**
- Official dollar rate
- Exchange reserves
- Interest rates
- Money supply
- External debt

**Endpoint:** `https://www.bcra.gob.ar/`

**Integration Method:** API + Web scraping

**Example Response:**
```json
{
  "dolar_oficial": {
    "compra": 850.25,
    "venta": 890.50,
    "fecha": "2026-01-15"
  },
  "reservas": {
    "valor": 28000000000,
    "variacion": -2.5
  }
}
```

---

### 3. Senado de la Nación

**Purpose:** Legislative activity tracking

**Data Available:**
- Bill proposals
- Voting records
- Session transcripts
- Committee activities

**Endpoint:** `https://www.senado.gob.ar/`

---

### 4. Cámara de Diputados

**Purpose:** Legislative activity tracking

**Data Available:**
- Bill proposals
- Voting records
- Deputy profiles
- Session agendas

**Endpoint:** `https://www.diputados.gob.ar/`

---

### 5. Boletín Oficial

**Purpose:** Official government publications

**Data Available:**
- Decrees
- Resolutions
- New laws
- Administrative decisions

**Endpoint:** `https://www.boletinoficial.gob.ar/`

---

### 6. YouTube Data API v3

**Purpose:** Political speeches and interviews

**Data Available:**
- Video metadata
- Captions/transcripts
- Channel information
- Search by keyword

**Endpoint:** `https://www.googleapis.com/youtube/v3/`

**Required Scope:** `youtube.readonly`

**Quota:** 10,000 units/day (free tier)

**Example Request:**
```bash
GET https://www.googleapis.com/youtube/v3/search
  ?part=snippet
  &q=discurso+politico+argentina
  &type=video
  &maxResults=10
  &key=YOUR_API_KEY
```

**Example Response:**
```json
{
  "items": [
    {
      "id": { "videoId": "abc123" },
      "snippet": {
        "title": "Discurso del Presidente",
        "publishedAt": "2026-01-15T20:00:00Z",
        "channelTitle": "Canal Oficial"
      }
    }
  ]
}
```

---

### 7. NewsData.io

**Purpose:** Political news aggregation

**Data Available:**
- News headlines
- Article content
- Source attribution
- Publication dates

**Endpoint:** `https://newsdata.io/api/1/news`

**Pricing:** Free tier: 200 requests/day

**Example Request:**
```bash
GET https://newsdata.io/api/1/news
  ?apikey=YOUR_KEY
  &country=ar
  &category=politics
  &language=es
```

---

### 8. Datos Argentina (Portal de Datos Abiertos)

**Purpose:** Government open data

**Data Available:**
- Economic indicators
- Government spending
- Public sector data
- Historical series

**Endpoint:** `https://datos.gob.ar/`

---

## Internal API (DATO)

### Base URL

```
Production: https://api.dato.ar
Staging: https://api-staging.dato.ar
```

### Authentication

All protected endpoints require Bearer token:

```bash
Authorization: Bearer <jwt_token>
```

---

### Auth Endpoints

#### POST /v1/auth/register

Register a new user.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "fullName": "Juan Pérez"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "fullName": "Juan Pérez",
    "plan": "free",
    "verificationsUsedToday": 0,
    "createdAt": "2026-01-15T10:00:00Z"
  },
  "token": "jwt_token",
  "refreshToken": "refresh_token"
}
```

---

#### POST /v1/auth/login

Login to existing account.

**Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response:**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "fullName": "Juan Pérez",
    "plan": "premium",
    "verificationsUsedToday": 2,
    "createdAt": "2026-01-15T10:00:00Z"
  },
  "token": "jwt_token",
  "refreshToken": "refresh_token"
}
```

---

#### GET /v1/auth/me

Get current authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "fullName": "Juan Pérez",
  "plan": "premium",
  "verificationsUsedToday": 2,
  "createdAt": "2026-01-15T10:00:00Z"
}
```

---

### Public Endpoints

#### GET /v1/feed

Get daily news summary.

**Query Parameters:**
- `date` (optional): Date filter (YYYY-MM-DD)
- `category` (optional): economy, politics, social, international, other

**Response:**
```json
{
  "date": "2026-01-15",
  "items": [
    {
      "id": "uuid",
      "type": "verification",
      "title": "Inflación de enero",
      "summary": "La inflación fue del 4.2%...",
      "category": "economy",
      "source": "INDEC",
      "timestamp": "2026-01-15T10:00:00Z",
      "badge": {
        "type": "VERDADERO",
        "color": "green"
      }
    }
  ]
}
```

---

#### GET /v1/claims/{id}

Get claim with verification.

**Response:**
```json
{
  "id": "uuid",
  "claimText": "La inflación bajó 50%",
  "speaker": "Político X",
  "speakerParty": "Partido Y",
  "sourceType": "speech",
  "category": "economy",
  "dateSaid": "2026-01-14",
  "verification": {
    "id": "uuid",
    "claimId": "uuid",
    "verdict": "PARCIALMENTE_VERDADERO",
    "confidence": 0.85,
    "explanation": "La inflación bajó 12%, no 50%...",
    "simpleExplanation": "Los precios siguen subiendo, pero más lento que antes.",
    "sources": [
      {
        "name": "INDEC",
        "url": "https://indec.gob.ar/...",
        "data": { "value": 4.2, "previous": 4.8 }
      }
    ],
    "verifiedAt": "2026-01-15T10:00:00Z"
  }
}
```

---

#### GET /v1/claims/search

Search claims and verifications.

**Query Parameters:**
- `q` (required): Search query (min 3 chars)
- `limit` (optional): Max results (default: 10)

**Response:**
```json
{
  "results": [
    {
      "type": "claim",
      "id": "uuid",
      "title": "Afirmación sobre inflación",
      "snippet": "La inflación bajó...",
      "relevance": 0.95
    }
  ]
}
```

---

#### POST /v1/claims/verify

Request verification of a claim.

**Body:**
```json
{
  "claim": "La inflación bajó 50% según datos oficiales",
  "speaker": "Político X",
  "source": "Entrevista en Canal 13",
  "context": "Discurso sobre economía"
}
```

**Response:**
```json
{
  "claimId": "uuid",
  "status": "pending",
  "estimatedTime": "2-5 minutos"
}
```

---

#### GET /v1/indicators

Get current economic indicators.

**Response:**
```json
{
  "inflation": {
    "value": 4.2,
    "previousValue": 4.8,
    "change": -0.6,
    "changePercent": -12.5,
    "period": "2026-01",
    "source": "INDEC",
    "unit": "%"
  },
  "dollar": {
    "official": {
      "buy": 850.25,
      "sell": 890.50,
      "updated": "2026-01-15T10:00:00Z"
    },
    "blue": {
      "buy": 1200,
      "sell": 1250,
      "updated": "2026-01-15T10:00:00Z"
    }
  },
  "reserves": {
    "value": 28000000000,
    "previousValue": 29500000000,
    "change": -1500000000,
    "changePercent": -5.08,
    "period": "2026-01-15",
    "source": "BCRA",
    "unit": "USD"
  }
}
```

---

### Speakers Endpoints

#### GET /v1/speakers

List politicians/speakers.

**Query Parameters:**
- `q` (optional): Search query
- `limit` (optional): Max results (default: 20)

**Response:**
```json
[
  {
    "name": "Político X",
    "party": "Partido Y",
    "totalClaims": 150,
    "verifiedClaims": 120,
    "stats": {
      "verdadero": 45,
      "falso": 30,
      "parcial": 35,
      "sinDatos": 10
    }
  }
]
```

---

#### GET /v1/speakers/{name}

Get speaker statistics.

**Response:**
```json
{
  "name": "Político X",
  "party": "Partido Y",
  "totalClaims": 150,
  "verifiedClaims": 120,
  "stats": {
    "verdadero": 45,
    "falso": 30,
    "parcial": 35,
    "sinDatos": 10
  }
}
```

---

### Verifications Endpoints

#### GET /v1/verifications/{id}

Get verification by ID.

**Response:**
```json
{
  "id": "uuid",
  "claimId": "uuid",
  "verdict": "FALSO",
  "confidence": 0.92,
  "explanation": "Los datos oficiales muestran que la inflación aumentó, no bajó...",
  "simpleExplanation": "La afirmación es incorrecta según datos del INDEC.",
  "sources": [
    {
      "name": "INDEC",
      "url": "https://indec.gob.ar/...",
      "data": { "value": 4.2, "previous": 4.8 }
    }
  ],
  "verifiedAt": "2026-01-15T10:00:00Z"
}
```

---

### Billing Endpoints

#### GET /v1/billing/plans

Get available subscription plans.

**Security:** None (public endpoint)

**Response:**
```json
[
  {
    "id": "free",
    "name": "Gratis",
    "price": 0,
    "currency": "USD",
    "features": [
      { "id": "verifications", "name": "Verificaciones diarias", "included": true },
      { "id": "alerts", "name": "Alertas ilimitadas", "included": false }
    ]
  },
  {
    "id": "premium",
    "name": "Premium",
    "price": 5,
    "currency": "USD",
    "features": [
      { "id": "verifications", "name": "Verificaciones ilimitadas", "included": true },
      { "id": "alerts", "name": "Alertas ilimitadas", "included": true }
    ]
  },
  {
    "id": "professional",
    "name": "Professional",
    "price": 50,
    "currency": "USD",
    "features": [
      { "id": "verifications", "name": "Verificaciones ilimitadas", "included": true },
      { "id": "alerts", "name": "Alertas ilimitadas", "included": true },
      { "id": "api", "name": "Acceso API", "included": true },
      { "id": "dashboard", "name": "Dashboard B2B", "included": true }
    ]
  }
]
```

---

#### POST /v1/billing/checkout

Create checkout session.

**Body:**
```json
{
  "plan": "premium",
  "successUrl": "https://dato.ar/success",
  "cancelUrl": "https://dato.ar/cancel"
}
```

**Response:**
```json
{
  "checkoutUrl": "https://checkout.stripe.com/..."
}
```

---

#### POST /v1/billing/portal

Get customer portal URL.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "portalUrl": "https://billing.stripe.com/..."
}
```

---

### Protected Endpoints (Premium)

#### GET /v1/history

Get full verification history.

**Headers:**
```
Authorization: Bearer <token>
```

---

#### GET /v1/alerts

List user alerts.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
[
  {
    "id": "uuid",
    "type": "speaker",
    "value": "Político X",
    "channels": ["push", "email"],
    "active": true,
    "createdAt": "2026-01-15T10:00:00Z"
  }
]
```

---

#### POST /v1/alerts

Create custom alert.

**Body:**
```json
{
  "type": "speaker",
  "value": "Político X",
  "channels": ["push", "email", "telegram"]
}
```

**Response:**
```json
{
  "id": "uuid",
  "type": "speaker",
  "value": "Político X",
  "channels": ["push", "email", "telegram"],
  "active": true,
  "createdAt": "2026-01-15T10:00:00Z"
}
```

---

#### DELETE /v1/alerts/{id}

Delete alert.

---

#### GET /v1/dashboard

Get B2B dashboard data. Requires Professional plan.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "stats": {
    "totalClaims": 1250,
    "verifiedTrue": 420,
    "verifiedFalse": 380,
    "pending": 50
  },
  "trends": {
    "topics": ["inflation", "dollar", "employment"],
    "speakers": [
      { "name": "Político X", "count": 45 }
    ]
  },
  "period": {
    "start": "2026-01-01",
    "end": "2026-01-31"
  }
}
```

---

#### GET /v1/dashboard/export

Export dashboard data.

**Query Parameters:**
- `format` (required): csv or pdf
- `dateFrom` (optional): Start date (YYYY-MM-DD)
- `dateTo` (optional): End date (YYYY-MM-DD)

**Response:** CSV or PDF file

---

## Error Handling

All errors follow this format:

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Has excedido el límite de verificaciones diarias",
    "details": {
      "limit": 3,
      "remaining": 0,
      "reset_at": "2026-01-16T00:00:00Z"
    }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Invalid or missing token |
| `FORBIDDEN` | 403 | Premium feature required |
| `RATE_LIMIT_EXCEEDED` | 429 | Daily limit reached |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 400 | Invalid request data |

---

## Rate Limits

| Plan | Requests/min | Fact-checks/day |
|------|--------------|-----------------|
| Free | 60 | 3 |
| Premium | 300 | Unlimited |
| Professional | 1000 | Unlimited + API |

---

## Webhooks (Coming Soon)

### POST /webhook/verification

Triggered when a new verification is completed.

**Payload:**
```json
{
  "event": "verification.completed",
  "data": {
    "claim_id": "claim_abc123",
    "verdict": "FALSO",
    "timestamp": "2026-01-15T10:30:00Z"
  }
}
```
