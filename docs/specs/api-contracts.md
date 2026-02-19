# API Contracts - DATO

> **Relacionado:** [Validación](validation.md) | [Códigos de Error](errors.md) | [Types](types.md)

## 3. API Contracts

### 3.1 OpenAPI Specification

```yaml
openapi: 3.1.0
info:
  title: DATO API
  version: 1.0.0
  description: API para la plataforma de inteligencia política DATO

servers:
  - url: https://api.dato.ar/v1
    description: Production
  - url: http://localhost:3000/api/v1
    description: Development

security:
  - bearerAuth: []

paths:
  # ============================================================================
  # AUTH
  # ============================================================================
  
  /auth/register:
    post:
      summary: Registrar nuevo usuario
      tags: [Auth]
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
                  minLength: 8
                fullName:
                  type: string
      responses:
        '201':
          description: Usuario creado
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '400':
          $ref: '#/components/responses/ValidationError'
        '409':
          description: Email ya registrado

  /auth/login:
    post:
      summary: Iniciar sesión
      tags: [Auth]
      security: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [email, password]
              properties:
                email:
                  type: string
                  format: email
                password:
                  type: string
      responses:
        '200':
          description: Sesión iniciada
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '401':
          description: Credenciales inválidas

  /auth/me:
    get:
      summary: Obtener usuario actual
      tags: [Auth]
      responses:
        '200':
          description: Usuario actual
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

  # ============================================================================
  # FEED
  # ============================================================================

  /feed:
    get:
      summary: Obtener feed diario
      tags: [Feed]
      parameters:
        - name: date
          in: query
          schema:
            type: string
            format: date
        - name: category
          in: query
          schema:
            $ref: '#/components/schemas/ClaimCategory'
      responses:
        '200':
          description: Feed del día
          content:
            application/json:
              schema:
                type: object
                properties:
                  date:
                    type: string
                    format: date
                  items:
                    type: array
                    items:
                      $ref: '#/components/schemas/FeedItem'

  # ============================================================================
  # CLAIMS
  # ============================================================================

  /claims:
    get:
      summary: Listar claims
      tags: [Claims]
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
            maximum: 100
        - name: speaker
          in: query
          schema:
            type: string
        - name: category
          in: query
          schema:
            $ref: '#/components/schemas/ClaimCategory'
        - name: verdict
          in: query
          schema:
            $ref: '#/components/schemas/Verdict'
        - name: dateFrom
          in: query
          schema:
            type: string
            format: date
        - name: dateTo
          in: query
          schema:
            type: string
            format: date
      responses:
        '200':
          description: Lista de claims
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PaginatedClaims'

  /claims/{id}:
    get:
      summary: Obtener claim por ID
      tags: [Claims]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Claim encontrado
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Claim'
        '404':
          $ref: '#/components/responses/NotFound'

  /claims/search:
    get:
      summary: Buscar claims
      tags: [Claims]
      parameters:
        - name: q
          in: query
          required: true
          schema:
            type: string
            minLength: 3
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: Resultados de búsqueda
          content:
            application/json:
              schema:
                type: object
                properties:
                  results:
                    type: array
                    items:
                      $ref: '#/components/schemas/SearchResult'

  /claims/verify:
    post:
      summary: Solicitar verificación de frase
      tags: [Claims]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [claim, speaker, source]
              properties:
                claim:
                  type: string
                  minLength: 10
                  maxLength: 1000
                speaker:
                  type: string
                source:
                  type: string
                context:
                  type: string
      responses:
        '201':
          description: Verificación solicitada
          content:
            application/json:
              schema:
                type: object
                properties:
                  claimId:
                    type: string
                  status:
                    type: string
                  estimatedTime:
                    type: string
        '429':
          $ref: '#/components/responses/RateLimited'

  # ============================================================================
  # VERIFICATIONS
  # ============================================================================

  /verifications/{id}:
    get:
      summary: Obtener verificación por ID
      tags: [Verifications]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: Verificación encontrada
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Verification'

  # ============================================================================
  # INDICATORS
  # ============================================================================

  /indicators:
    get:
      summary: Obtener indicadores económicos actuales
      tags: [Indicators]
      responses:
        '200':
          description: Indicadores actuales
          content:
            application/json:
              schema:
                type: object
                properties:
                  inflation:
                    $ref: '#/components/schemas/IndicatorValue'
                  dollar:
                    type: object
                    properties:
                      official:
                        $ref: '#/components/schemas/DollarRate'
                      blue:
                        $ref: '#/components/schemas/DollarRate'
                  reserves:
                    $ref: '#/components/schemas/IndicatorValue'
                  unemployment:
                    $ref: '#/components/schemas/IndicatorValue'

  /indicators/{indicator}/history:
    get:
      summary: Historial de indicador
      tags: [Indicators]
      parameters:
        - name: indicator
          in: path
          required: true
          schema:
            $ref: '#/components/schemas/EconomicIndicator'
        - name: months
          in: query
          schema:
            type: integer
            default: 12
      responses:
        '200':
          description: Historial del indicador
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/EconomicDataPoint'

  # ============================================================================
  # SPEAKERS
  # ============================================================================

  /speakers:
    get:
      summary: Listar políticos/oradores
      tags: [Speakers]
      parameters:
        - name: q
          in: query
          schema:
            type: string
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: Lista de speakers
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/SpeakerStats'

  /speakers/{name}:
    get:
      summary: Obtener estadísticas de speaker
      tags: [Speakers]
      parameters:
        - name: name
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Estadísticas del speaker
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/SpeakerStats'

  # ============================================================================
  # ALERTS (Premium)
  # ============================================================================

  /alerts:
    get:
      summary: Listar alertas del usuario
      tags: [Alerts]
      responses:
        '200':
          description: Lista de alertas
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/Alert'

    post:
      summary: Crear alerta
      tags: [Alerts]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [type, value]
              properties:
                type:
                  type: string
                  enum: [speaker, topic, category, indicator]
                value:
                  type: string
                channels:
                  type: array
                  items:
                    type: string
                    enum: [push, email, telegram]
                  default: [push]
      responses:
        '201':
          description: Alerta creada
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Alert'
        '403':
          description: Plan no permite más alertas

  /alerts/{id}:
    delete:
      summary: Eliminar alerta
      tags: [Alerts]
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '204':
          description: Alerta eliminada

  # ============================================================================
  # BILLING
  # ============================================================================

  /billing/plans:
    get:
      summary: Obtener planes disponibles
      tags: [Billing]
      security: []
      responses:
        '200':
          description: Planes disponibles
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/SubscriptionPlan'

  /billing/checkout:
    post:
      summary: Crear sesión de checkout
      tags: [Billing]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [plan]
              properties:
                plan:
                  type: string
                  enum: [premium, professional]
                successUrl:
                  type: string
                cancelUrl:
                  type: string
      responses:
        '200':
          description: Sesión creada
          content:
            application/json:
              schema:
                type: object
                properties:
                  checkoutUrl:
                    type: string

  /billing/portal:
    post:
      summary: Crear enlace al portal de cliente
      tags: [Billing]
      responses:
        '200':
          description: URL del portal
          content:
            application/json:
              schema:
                type: object
                properties:
                  portalUrl:
                    type: string

  # ============================================================================
  # DASHBOARD (Professional)
  # ============================================================================

  /dashboard:
    get:
      summary: Obtener datos del dashboard
      tags: [Dashboard]
      responses:
        '200':
          description: Datos del dashboard
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DashboardData'
        '403':
          description: Requiere plan Professional

  /dashboard/export:
    get:
      summary: Exportar datos
      tags: [Dashboard]
      parameters:
        - name: format
          in: query
          schema:
            type: string
            enum: [csv, pdf]
        - name: dateFrom
          in: query
          schema:
            type: string
            format: date
        - name: dateTo
          in: query
          schema:
            type: string
            format: date
      responses:
        '200':
          description: Archivo exportado
          content:
            application/csv:
              schema:
                type: string
            application/pdf:
              schema:
                type: string
                format: binary

components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        fullName:
          type: string
          nullable: true
        plan:
          type: string
          enum: [free, premium, professional]
        verificationsUsedToday:
          type: integer
        createdAt:
          type: string
          format: date-time

    AuthResponse:
      type: object
      properties:
        user:
          $ref: '#/components/schemas/User'
        token:
          type: string
        refreshToken:
          type: string

    Claim:
      type: object
      properties:
        id:
          type: string
          format: uuid
        claimText:
          type: string
        speaker:
          type: string
        speakerParty:
          type: string
          nullable: true
        sourceType:
          $ref: '#/components/schemas/ClaimSourceType'
        category:
          $ref: '#/components/schemas/ClaimCategory'
        dateSaid:
          type: string
          format: date
        verification:
          $ref: '#/components/schemas/Verification'

    ClaimCategory:
      type: string
      enum: [economy, politics, social, international, other]

    ClaimSourceType:
      type: string
      enum: [speech, interview, social_media, news, official]

    Verdict:
      type: string
      enum: [VERDADERO, FALSO, PARCIALMENTE_VERDADERO, SIN_DATOS]

    Verification:
      type: object
      properties:
        id:
          type: string
          format: uuid
        claimId:
          type: string
          format: uuid
        verdict:
          $ref: '#/components/schemas/Verdict'
        confidence:
          type: number
          minimum: 0
          maximum: 1
        explanation:
          type: string
        simpleExplanation:
          type: string
        sources:
          type: array
          items:
            $ref: '#/components/schemas/VerificationSource'
        verifiedAt:
          type: string
          format: date-time

    VerificationSource:
      type: object
      properties:
        name:
          type: string
        url:
          type: string
          format: uri
        data:
          type: object

    FeedItem:
      type: object
      properties:
        id:
          type: string
          format: uuid
        type:
          type: string
          enum: [verification, indicator, news]
        title:
          type: string
        summary:
          type: string
        category:
          $ref: '#/components/schemas/ClaimCategory'
        source:
          type: string
        timestamp:
          type: string
          format: date-time
        url:
          type: string
        badge:
          type: object
          properties:
            type:
              $ref: '#/components/schemas/Verdict'
            color:
              type: string

    SearchResult:
      type: object
      properties:
        type:
          type: string
          enum: [claim, verification, speaker]
        id:
          type: string
          format: uuid
        title:
          type: string
        snippet:
          type: string
        relevance:
          type: number

    EconomicIndicator:
      type: string
      enum:
        - inflation_monthly
        - inflation_yearly
        - poverty
        - employment
        - unemployment
        - dollar_official_buy
        - dollar_official_sell
        - dollar_blue_buy
        - dollar_blue_sell
        - reserves
        - interest_rate
        - gdp
        - trade_balance

    IndicatorValue:
      type: object
      properties:
        value:
          type: number
        previousValue:
          type: number
          nullable: true
        change:
          type: number
          nullable: true
        changePercent:
          type: number
          nullable: true
        period:
          type: string
          format: date
        source:
          type: string
        unit:
          type: string

    DollarRate:
      type: object
      properties:
        buy:
          type: number
        sell:
          type: number
        updated:
          type: string
          format: date-time

    EconomicDataPoint:
      type: object
      properties:
        period:
          type: string
          format: date
        value:
          type: number

    SpeakerStats:
      type: object
      properties:
        name:
          type: string
        party:
          type: string
          nullable: true
        totalClaims:
          type: integer
        verifiedClaims:
          type: integer
        stats:
          type: object
          properties:
            verdadero:
              type: integer
            falso:
              type: integer
            parcial:
              type: integer
            sinDatos:
              type: integer

    Alert:
      type: object
      properties:
        id:
          type: string
          format: uuid
        type:
          type: string
          enum: [speaker, topic, category, indicator]
        value:
          type: string
        channels:
          type: array
          items:
            type: string
        active:
          type: boolean
        createdAt:
          type: string
          format: date-time

    SubscriptionPlan:
      type: object
      properties:
        id:
          type: string
          enum: [free, premium, professional]
        name:
          type: string
        price:
          type: number
        currency:
          type: string
        features:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              name:
                type: string
              included:
                type: boolean

    DashboardData:
      type: object
      properties:
        stats:
          type: object
          properties:
            totalClaims:
              type: integer
            verifiedTrue:
              type: integer
            verifiedFalse:
              type: integer
            pending:
              type: integer
        trends:
          type: object
          properties:
            topics:
              type: array
              items:
                type: string
            speakers:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                  count:
                    type: integer
        period:
          type: object
          properties:
            start:
              type: string
              format: date
            end:
              type: string
              format: date

    PaginatedClaims:
      type: object
      properties:
        data:
          type: array
          items:
            $ref: '#/components/schemas/Claim'
        pagination:
          type: object
          properties:
            page:
              type: integer
            limit:
              type: integer
            total:
              type: integer
            totalPages:
              type: integer
            hasMore:
              type: boolean

    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object

  responses:
    NotFound:
      description: Recurso no encontrado
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: RES-001
            message: Recurso no encontrado

    ValidationError:
      description: Error de validación
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: VAL-001
            message: Datos inválidos
            details:
              email: Email inválido

    RateLimited:
      description: Rate limit excedido
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
          example:
            code: RATE-002
            message: Has excedido el límite de verificaciones diarias
            details:
              limit: 3
              remaining: 0
              resetAt: "2026-02-14T00:00:00Z"
```

---

