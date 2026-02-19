---
name: test-automation-strategist
description: Arquitecto de calidad y automatización para DATO. Especialista en TDD, BDD y estrategias de testing E2E para plataforma de fact-checking político argentino.
---

# Test Automation Strategist: El Guardián de la Calidad DATO

> [!IMPORTANT]
> **Trigger**: Activar ANTES de escribir nueva lógica (TDD) o DESPUÉS de un bug crítico (Regression Testing).
> **Filosofía**: "Si no está probado, está roto".

## Estrategia de la Pirámide de Pruebas

### 1. Unit Tests (La Base - 70%)
- **Foco**: Lógica pura, funciones aisladas, helpers y hooks.
- **Herramientas**: Jest, Vitest.
- **Regla**: Deben correr en milisegundos. Mockear TODO lo externo (DB, API).

#### Ejemplos DATO - Unit Tests

**Agentes (Backend NestJS)**
```typescript
// apps/api/src/agents/collector/collector.service.spec.ts
describe('CollectorService', () => {
  it('should parse INDEC inflation CSV correctly', async () => {
    const csv = 'mes,valor\n2026-01,4.2';
    const result = service.parseINDECData(csv);
    expect(result).toEqual([{ mes: '2026-01', valor: 4.2 }]);
  });

  it('should handle BCRA API rate limiting gracefully', async () => {
    mockAxios.onGet('/bcra/reservas').reply(429);
    await expect(service.fetchBCRAData()).rejects.toThrow(RateLimitError);
  });
});

// apps/api/src/agents/extractor/ner.service.spec.ts
describe('NERService', () => {
  it('should extract politician entities from text', async () => {
    const text = 'Milei anunció un nuevo decreto';
    const entities = await service.extractEntities(text);
    expect(entities).toContainEqual({ type: 'POLITICIAN', name: 'Javier Milei' });
  });

  it('should normalize politician names with aliases', async () => {
    const text = 'El presidente anunció medidas';
    const entities = await service.extractEntities(text, { context: 'argentina_president' });
    expect(entities).toContainEqual({ type: 'POLITICIAN', name: 'Javier Milei' });
  });
});

// apps/api/src/agents/fact-checker/verification.service.spec.ts
describe('VerificationService', () => {
  it('should assign FALSE badge when source contradicts claim', async () => {
    const claim = 'La inflación bajó a 0%';
    const sources = [{ url: 'indec.gob.ar', data: { inflacion: 4.2 } }];
    const result = await service.verify(claim, sources);
    expect(result.badge).toBe('FALSE');
  });

  it('should assign PARTIALLY_TRUE badge with nuance', async () => {
    const claim = 'El déficit fiscal es cero';
    const sources = [{ url: 'mecon.gob.ar', data: { deficit: -0.5 } }];
    const result = await service.verify(claim, sources);
    expect(result.badge).toBe('PARTIALLY_TRUE');
    expect(result.nuance).toContain('primario');
  });
});
```

**API Endpoints (NestJS)**
```typescript
// apps/api/src/modules/claims/claims.controller.spec.ts
describe('ClaimsController', () => {
  it('POST /claims should create claim with politician detection', async () => {
    const dto = { text: 'Massa prometió eliminar impuestos' };
    const res = await request(app.getHttpServer())
      .post('/claims')
      .send(dto)
      .expect(201);
    expect(res.body.entities).toContainEqual({ type: 'POLITICIAN', name: 'Sergio Massa' });
  });

  it('GET /claims/:id should return 404 for non-existent claim', async () => {
    await request(app.getHttpServer())
      .get('/claims/non-existent-id')
      .expect(404);
  });
});
```

**UI Components (Next.js)**
```typescript
// apps/web/src/components/ClaimCard.test.tsx
describe('ClaimCard', () => {
  it('should render FALSE badge with red styling', () => {
    render(<ClaimCard badge="FALSE" text="Claim text" />);
    expect(screen.getByText('FALSO')).toHaveClass('bg-red-500');
  });

  it('should link to source URLs', () => {
    const sources = [{ url: 'https://indec.gob.ar', title: 'INDEC' }];
    render(<ClaimCard sources={sources} />);
    expect(screen.getByRole('link')).toHaveAttribute('href', 'https://indec.gob.ar');
  });
});
```

### 2. Integration Tests (El Medio - 20%)
- **Foco**: Comunicación entre módulos (ej. Controller -> Service -> DB Mock).
- **Herramientas**: Supertest (API), React Testing Library (Componentes + Estado).
- **Regla**: Validar contratos de datos y manejo de errores.

#### Ejemplos DATO - Integration Tests

**Agent Pipeline Integration**
```typescript
// apps/api/src/agents/agent.pipeline.spec.ts
describe('AgentPipeline', () => {
  it('should process claim through all agents', async () => {
    const claim = await pipeline.process({
      text: 'El dólar blue superó los $1500',
      source: 'twitter'
    });
    
    expect(claim.entities).toBeDefined();        // Agent 2
    expect(claim.verification).toBeDefined();     // Agent 3
    expect(claim.simplified).toBeDefined();       // Agent 4
    expect(claim.published).toBe(true);           // Agent 5
  });
});
```

**Database Integration**
```typescript
// apps/api/src/modules/claims/claims.integration.spec.ts
describe('ClaimsModule (Integration)', () => {
  it('should persist claim with all relationships', async () => {
    const claim = await claimsService.create({
      text: 'Claim text',
      politician_id: 'milei-123',
      verification_status: 'VERIFIED'
    });
    
    const found = await claimsRepo.findOne({ 
      where: { id: claim.id },
      relations: ['politician', 'sources']
    });
    expect(found.politician.name).toBe('Javier Milei');
  });
});
```

### 3. E2E Tests (La Cima - 10%)
- **Foco**: Flujos críticos de usuario (Fact-checking completo, Newsletter subscription).
- **Herramientas**: Playwright.
- **Regla**: Tests "Smoke" que navegan como un usuario real. Pocos pero cruciales.

#### Ejemplos DATO - E2E Tests

**Fact-Checking Flow E2E**
```typescript
// e2e/fact-check-flow.spec.ts
test('complete fact-check flow', async ({ page }) => {
  await page.goto('/claims/new');
  
  // Submit claim
  await page.fill('[data-testid="claim-input"]', 'La inflación es del 2%');
  await page.click('[data-testid="submit-claim"]');
  
  // Wait for processing
  await page.waitForSelector('[data-testid="verification-result"]');
  
  // Verify badge assigned
  const badge = await page.textContent('[data-testid="badge"]');
  expect(['TRUE', 'FALSE', 'PARTIALLY_TRUE']).toContain(badge);
  
  // Verify sources linked
  const sources = await page.$$('[data-testid="source-link"]');
  expect(sources.length).toBeGreaterThan(0);
});
```

**Newsletter Subscription E2E**
```typescript
// e2e/newsletter.spec.ts
test('newsletter subscription flow', async ({ page }) => {
  await page.goto('/');
  
  await page.fill('[data-testid="email-input"]', 'test@example.com');
  await page.click('[data-testid="subscribe-button"]');
  
  await page.waitForSelector('[data-testid="success-message"]');
  expect(await page.textContent('[data-testid="success-message"]'))
    .toContain('Gracias por suscribirte');
});
```

## Tests Específicos DATO

### Agent 1 - Collector
```typescript
describe('Agent 1: Collector', () => {
  it('should scrape INDEC inflation data', async () => {
    const data = await collector.fetchINDECInflation();
    expect(data).toHaveProperty('fecha');
    expect(data).toHaveProperty('valor');
    expect(data.fuentes).toContain('indec.gob.ar');
  });

  it('should scrape BCRA reserves data', async () => {
    const data = await collector.fetchBCRAReservas();
    expect(data).toHaveProperty('fecha');
    expect(data).toHaveProperty('reservas_usd');
    expect(data.fuentes).toContain('bcra.gob.ar');
  });

  it('should handle scraping failures with retry', async () => {
    mockScrape.failNTimes(3);
    const data = await collector.fetchWithRetry('indec');
    expect(data).toBeDefined(); // Should eventually succeed
  });
});
```

### Agent 2 - Extractor
```typescript
describe('Agent 2: Extractor (NER)', () => {
  const politicians = [
    { name: 'Javier Milei', aliases: ['Milei', 'El León', 'el peluca'] },
    { name: 'Cristina Kirchner', aliases: ['CFK', 'Cristina'] },
    { name: 'Patricia Bullrich', aliases: ['Pato'] },
  ];

  it.each(politicians)('should detect $name', async ({ name, aliases }) => {
    const text = `${aliases[0]} anunció nuevas medidas`;
    const entities = await extractor.extract(text);
    expect(entities).toContainEqual({ type: 'POLITICIAN', name });
  });

  it('should extract numeric claims with context', async () => {
    const text = 'La inflación fue del 5.1%';
    const entities = await extractor.extract(text);
    expect(entities).toContainEqual({ 
      type: 'NUMERIC_CLAIM', 
      value: 5.1, 
      unit: '%', 
      topic: 'inflacion' 
    });
  });
});
```

### Agent 3 - Fact Checker
```typescript
describe('Agent 3: Fact Checker', () => {
  it('should assign TRUE badge for verified claims', async () => {
    const claim = { text: 'La inflación de enero fue 4.2%', date: '2026-01' };
    const result = await factChecker.verify(claim);
    expect(result.badge).toBe('TRUE');
    expect(result.confidence).toBeGreaterThan(0.9);
  });

  it('should assign FALSE badge with counter-evidence', async () => {
    const claim = { text: 'No hay inflación en Argentina', date: '2026-01' };
    const result = await factChecker.verify(claim);
    expect(result.badge).toBe('FALSE');
    expect(result.evidence).toContainEqual(
      expect.objectContaining({ type: 'COUNTER_EVIDENCE' })
    );
  });

  it('should assign PARTIALLY_TRUE with nuance', async () => {
    const claim = { text: 'El déficit es cero', date: '2026-01' };
    const result = await factChecker.verify(claim);
    expect(result.badge).toBe('PARTIALLY_TRUE');
    expect(result.nuance).toBeDefined();
  });

  it('should assign UNVERIFIABLE for subjective claims', async () => {
    const claim = { text: 'Argentina es el mejor país', date: '2026-01' };
    const result = await factChecker.verify(claim);
    expect(result.badge).toBe('UNVERIFIABLE');
  });
});
```

### Agent 4 - Simplifier
```typescript
describe('Agent 4: Simplifier', () => {
  it('should simplify technical content for general audience', async () => {
    const technical = 'El IPC aumentó 4.2% interanual';
    const result = await simplifier.simplify(technical);
    expect(result.simplified).toContain('precios');
    expect(result.simplified).not.toContain('IPC');
    expect(result.readabilityScore).toBeLessThan(8); // Flesch-Kincaid
  });

  it('should preserve key facts in simplification', async () => {
    const claim = 'La inflación fue del 4.2% según el INDEC';
    const result = await simplifier.simplify(claim);
    expect(result.simplified).toContain('4.2%');
    expect(result.simplified).toContain('INDEC');
  });
});
```

### Agent 5 - Publisher
```typescript
describe('Agent 5: Publisher', () => {
  it('should format newsletter content', async () => {
    const claim = { badge: 'FALSE', text: 'Claim text', simplified: 'Simple text' };
    const newsletter = await publisher.formatNewsletter([claim]);
    expect(newsletter.subject).toContain('Chequeo');
    expect(newsletter.html).toContain('FALSO');
  });

  it('should post to Twitter with character limit', async () => {
    const claim = { badge: 'FALSE', text: 'Long claim text...' };
    const tweet = await publisher.formatTwitter(claim);
    expect(tweet.length).toBeLessThanOrEqual(280);
    expect(tweet).toContain('#Dato');
  });

  it('should send to Telegram channel', async () => {
    const claim = { badge: 'TRUE', text: 'Claim text' };
    await publisher.publishTelegram(claim);
    expect(mockTelegram.sendMessage).toHaveBeenCalledWith(
      expect.objectContaining({ parse_mode: 'HTML' })
    );
  });
});
```

### Agent 6 - Billing
```typescript
describe('Agent 6: Billing', () => {
  it('should handle Stripe webhook for subscription created', async () => {
    const event = { type: 'checkout.session.completed', data: { customer: 'cus_123' } };
    await billing.handleStripeWebhook(event);
    expect(mockUserService.updateSubscription).toHaveBeenCalledWith(
      'cus_123',
      { status: 'active' }
    );
  });

  it('should handle MercadoPago webhook', async () => {
    const event = { type: 'payment', data: { status: 'approved', external_reference: 'user_123' } };
    await billing.handleMercadoPagoWebhook(event);
    expect(mockUserService.updateSubscription).toHaveBeenCalledWith(
      'user_123',
      { status: 'active' }
    );
  });

  it('should calculate tier limits correctly', async () => {
    const limits = billing.getTierLimits('premium');
    expect(limits.claimsPerMonth).toBe(100);
    expect(limits.newsletterEnabled).toBe(true);
  });
});
```

### Agent 7 - Learning
```typescript
describe('Agent 7: Learning (Feedback Loop)', () => {
  it('should store user corrections for retraining', async () => {
    const correction = {
      claimId: 'claim_123',
      suggestedBadge: 'TRUE',
      previousBadge: 'FALSE',
      reason: 'Fuente actualizada'
    };
    await learning.storeCorrection(correction);
    expect(mockFeedbackRepo.save).toHaveBeenCalledWith(
      expect.objectContaining({ status: 'PENDING_REVIEW' })
    );
  });

  it('should aggregate feedback for accuracy metrics', async () => {
    const metrics = await learning.getAccuracyMetrics();
    expect(metrics).toHaveProperty('totalVerifications');
    expect(metrics).toHaveProperty('correctionsReceived');
    expect(metrics).toHaveProperty('accuracyRate');
  });
});
```

## Protocolos de Actuación
- **TDD Riguroso**: 
    1. Escribir test que falla.
    2. Escribir código mínimo.
    3. Refactorizar.
- **Priorización Basada en Riesgo**: Enfatizar tests en agentes críticos (Fact Checker, Collector).
- **Coverage Gate**: Ningún PR se aprueba con < 80% de cobertura en backend, < 70% en frontend.

## Token Cost en Tests

Los tests deben verificar que los agentes respeten los presupuestos de tokens:

```typescript
describe('Token Budget Enforcement', () => {
  it('should not exceed token budget for Agent 3', async () => {
    const claim = { text: 'Long claim text...' };
    const result = await factChecker.verify(claim);
    expect(result.tokenUsage.total).toBeLessThanOrEqual(
      process.env.AGENT3_MAX_TOKENS || 2000
    );
  });

  it('should log token usage for monitoring', async () => {
    await pipeline.process({ text: 'Claim' });
    expect(mockLogger.info).toHaveBeenCalledWith(
      expect.objectContaining({ tokenUsage: expect.any(Object) })
    );
  });

  it('should fail gracefully when budget exceeded', async () => {
    mockTokenBudget.exhaust();
    const result = await factChecker.verify({ text: 'Claim' });
    expect(result.status).toBe('BUDGET_EXCEEDED');
    expect(result.fallback).toBeDefined();
  });
});
```

## Ejecución

| Modo | Comando | Cuándo |
|------|---------|--------|
| **Automática** | Pre-push hooks → `pnpm test` | Antes de cada push |
| **CI/CD** | GitHub Actions → `pnpm test:ci` | En cada PR y merge |
| **Manual** | `pnpm test:watch` | Durante desarrollo |
| **Coverage** | `pnpm test:coverage` | Antes de merge |

```bash
# Comandos disponibles
pnpm test              # Todos los tests
pnpm test:watch        # Watch mode
pnpm test:coverage     # Con reporte de cobertura
pnpm test:e2e          # Tests E2E con Playwright
pnpm test:ci           # Suite completa para CI
```

## Recursos

### Ejemplo Completo: Test de Integración Agente
```typescript
// apps/api/src/agents/__tests__/agent-integration.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { AgentPipeline } from '../pipeline';
import { CollectorService } from '../collector';
import { ExtractorService } from '../extractor';
import { FactCheckerService } from '../fact-checker';

describe('AgentPipeline Integration', () => {
  let pipeline: AgentPipeline;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [AgentPipeline, CollectorService, ExtractorService, FactCheckerService],
    }).compile();
    pipeline = module.get(AgentPipeline);
  });

  describe('full pipeline', () => {
    it('processes claim end-to-end', async () => {
      const input = { text: 'La inflación es 0%', source: 'twitter' };
      const result = await pipeline.process(input);
      
      expect(result.badge).toBeDefined();
      expect(result.entities).toBeArray();
      expect(result.sources).toBeArray();
      expect(result.simplified).toBeString();
    });
  });
});
```

### Ejemplo Completo: Test E2E Playwright
```typescript
// e2e/admin-claims.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Admin Claims Management', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'admin@dato.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/admin');
  });

  test('admin can review pending claims', async ({ page }) => {
    await page.goto('/admin/claims?status=pending');
    const count = await page.locator('[data-testid="claim-row"]').count();
    expect(count).toBeGreaterThan(0);
  });
});
```