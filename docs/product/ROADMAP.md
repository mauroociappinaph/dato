# Roadmap - DATO

## Product Vision

> Democratize access to reliable political and economic information in Argentina through AI and official data.

---

## FASE 0: Setup Inicial (5-7 días)

**Goal:** Infraestructura lista para desarrollo

| Sección | Subtasks | Estado |
|---------|----------|--------|
| 0.1 Git & Repositorio | 5 | Pendiente |
| 0.2 Config Files | 5 | Pendiente |
| 0.3 Estructura Directorios | 4 | Pendiente |
| 0.4 CI/CD | 2 | Pendiente |
| 0.5 Supabase Setup | 3 | Pendiente |

**Total:** ~20 subtasks

---

## 🧪 CP0: Checkpoint Técnico (Día 7)

> **Objetivo:** Verificar que el setup está listo antes de codear features

| Item | Comando | Umbral |
|------|---------|--------|
| Dependencias | `pnpm install` | Sin errores |
| Linting | `pnpm lint` | Sin errores |
| Typecheck | `pnpm typecheck` | Sin errores |
| Supabase tablas | Table Editor | Todas creadas |
| CI | PR de prueba | Verde |
| Tiempo real | ___ días | ≤ 7 días |

**Si tiempo > 2x estimado:** Revisar scope FASE 1.

---

## FASE 1: MVP (6 semanas / 42 días)

**Goal:** Functional product with core features

### Sprint 1 (Week 1-2): Backend + Deploy temprano

| Task | Priority | Status |
|------|----------|--------|
| Setup NestJS backend | Must | Pending |
| Connect Supabase | Must | Pending |
| Deploy backend to Railway | Must | Pending |

### Sprint 2 (Week 3-4): Agents

| Task | Priority | Status |
|------|----------|--------|
| Agent 1: Data Collector | Must | Pending |
| Agent 2: Claim Extractor | Must | Pending |
| Agent 3: Fact Checker | Must | Pending |
| Agent 4: Simplifier | Must | Pending |

### Sprint 3 (Week 5-6): Frontend + Auth UI

| Task | Priority | Status |
|------|----------|--------|
| Next.js frontend setup | Must | Pending |
| UI Components | Must | Pending |
| Auth UI (Login/Signup) | Must | Pending |
| SEO Técnico (Core Web Vitals, Schema.org) | Must | Pending |
| Deploy completo | Must | Pending |
| Smoke Tests | Must | Pending |

### Deliverables Phase 1
- [ ] Backend API deployado
- [ ] 4 agentes operacionales
- [ ] Web app funcional
- [ ] Auth UI (login/signup)
- [ ] SEO optimizado (Lighthouse > 90)
- [ ] Smoke tests pasando

---

## 🧪 CP1: Checkpoint de Validación (Día 42 - Post Sprint 3)

> **Con quién:** 3-5 usuarios (amigos, colegas)

| Test | Umbral |
|------|--------|
| Badges interpretados | ≥ 80% |
| Simplificación entendible | ≥ 70% |
| Flujo completado sin ayuda | ≥ 60% |
| Bugs críticos | 0 |

---

## FASE 2: Growth (60 days)

**Goal:** User acquisition and engagement features

### Sprint 4 (Week 7-8): Auth + Búsqueda + Performance

| Task | Priority | Status |
|------|----------|--------|
| Sistema de Roles | Should | Pending |
| Búsqueda vectorial | Should | Pending |
| Performance Setup (Lighthouse CI) | Should | Pending |
| WebMCP Integration | Should | Pending |

### Sprint 5 (Week 9-10): Notifications + Publishing

| Task | Priority | Status |
|------|----------|--------|
| Push notifications | Should | Pending |
| Agent 5: Publisher | Should | Pending |
| Agent 9: Growth Engineer | Should | Pending |
| Newsletter integration | Should | Pending |

### Deliverables Phase 2
- [ ] Sistema de roles
- [ ] Búsqueda por tema/político
- [ ] Push notifications
- [ ] Publicación automatizada
- [ ] Growth engine optimizando conversión

---

## 🧪 CP2: Checkpoint de Validación (Día 60)

> **Con quién:** 5-10 usuarios reales

| Test | Umbral |
|------|--------|
| Búsqueda exitosa | ≥ 70% |
| Notificaciones útiles | ≥ 60% |
| Retención 7 días | ≥ 30% |

---

## FASE 3: Monetization (90+ days)

**Goal:** Revenue generation and B2B features

### Sprint 6 (Week 11-14)

| Task | Priority | Status |
|------|----------|--------|
| Agent 8: Quality Assurance | Could | Pending |
| Agent 6: Billing & Access | Could | Pending |
| Mercado Pago integration | Could | Pending |
| Premium subscription | Could | Pending |
| Free tier limits | Could | Pending |

### Sprint 7 (Week 15-18)

| Task | Priority | Status |
|------|----------|--------|
| Agent 7: Learning Loop | Could | Pending |
| B2B Dashboard | Could | Pending |
| PDF reports | Could | Pending |
| API access for premium | Could | Pending |

### Deliverables Phase 3
- [ ] QA evaluando calidad automáticamente
- [ ] Working subscription system
- [ ] B2B dashboard
- [ ] Automated reports
- [ ] First paying customers

---

## 🧪 CP3: Checkpoint Pre-Orchestration (Post FASE 3)

> **Objetivo:** Validar si realmente se necesita un orquestador

### Checklist de Decisión

| Pregunta | Evaluar |
|----------|---------|
| ¿Paralelización necesaria? | □ |
| ¿Branching condicional? | □ |
| ¿Sincronización de múltiples fuentes? | □ |
| ¿Cancelación de workflows? | □ |
| ¿Visibilidad en tiempo real? | □ |
| ¿Retry logic complejo? | □ |

**Regla:** 5+ "Sí" → Implementar FASE 4

---

## FASE 4: Orchestration Layer (Conditional)

> **Prerrequisito:** CP3 validado con 5+ "Sí" + >1000 verificaciones/día

**Goal:** Advanced multi-agent orchestration with LangGraph

### Sprint 8-9 (Week 19-26)

| Task | Priority | Status |
|------|----------|--------|
| Agent 0: Orchestrator | Could | Pending |
| LangGraph setup | Could | Pending |
| Workflow: Verificación Compleja | Could | Pending |
| Workflow: Publicación Multi-Canal | Could | Pending |
| Workflow: Incident Response | Could | Pending |
| Dashboard de Orquestación | Could | Pending |

### Casos de Uso

1. **Verificación Multi-Fuente:** INDEC + BCRA + Oficial en paralelo
2. **Publicación Multi-Canal:** Twitter + Telegram + Newsletter paralelo
3. **Incident Response:** Detección → RCA → Fix → Verificación automática

### Deliverables Phase 4
- [ ] LangGraph operativo con 3+ workflows
- [ ] Dashboard de orquestación en tiempo real
- [ ] Verificación multi-fuente paralela
- [ ] Recovery automático de incidentes
- [ ] BullMQ deprecado para flujos complejos

### Métricas de Éxito

| Métrica | Target |
|---------|--------|
| Tiempo verificación compleja | < 5s (paralelo) |
| Visibilidad del flujo | 100% |
| Cancelaciones exitosas | 100% |
| Recovery automático | > 80% |
| Incidentes escalados | < 20% manual |

---

## Future Roadmap

### Q2 2026
- Mobile app (React Native)
- YouTube video integration
- Historical data analysis (10 years)
- Public API

### Q3 2026
- Browser extension
- WhatsApp bot
- Election coverage
- Comparative analysis with other countries

### Q4 2026
- Enterprise tier
- White-label solution
- Data marketplace
- International expansion (Uruguay, Chile)

---

## Milestones

```
FASE 0 ────▶ Setup Completo
     │
     ├─ Git, config, CI/CD
     └─ Supabase listo

CP0 ───────▶ Checkpoint Técnico
     │
     ├─ pnpm install OK
     ├─ pnpm lint OK
     ├─ Supabase tablas OK
     └─ CI pasa

FASE 1 ────▶ MVP Launch (Día 42)
     │
     ├─ Backend deployado
     ├─ Agent 1-4 operational
     ├─ Frontend + Auth UI
     └─ Smoke tests pasando

CP1 ───────▶ Validación MVP (Día 42)
     │
     ├─ Badges OK
     ├─ Simplificación OK
     ├─ Auth UI funcional
     └─ Flujo login → feed OK

FASE 2 ────▶ Growth Phase
     │
     ├─ Sistema de roles
     ├─ Búsqueda vectorial
     ├─ Notifications
     ├─ Agent 5: Publisher
     └─ 500+ users

CP2 ───────▶ Validación Growth
     │
     ├─ Búsqueda OK
     ├─ Retención OK
     └─ Ready to monetize

FASE 3 ────▶ First Revenue
     │
     ├─ Subscriptions
     ├─ First B2B clients
     └─ $500 MRR

Month 6 ───▶ Product-Market Fit
     │
     ├─ 2000+ users
     ├─ Mobile app
     └─ $2000 MRR

Month 12 ───▶ Scale
     │
     ├─ 5000+ users
     ├─ Team expansion
     └─ $5000 MRR
```

---

## Success Metrics

### CP0 - Checkpoint Técnico (Día 7)
- [ ] `pnpm install` sin errores
- [ ] `pnpm lint` sin errores
- [ ] `pnpm typecheck` sin errores
- [ ] Supabase tablas creadas
- [ ] CI pasa en PR de prueba
- [ ] Tiempo real ≤ 7 días

### CP1 - Validación MVP (Día 42)
- [ ] 3-5 usuarios testean
- [ ] Badges interpretados ≥ 80%
- [ ] Simplificación entendible ≥ 70%
- [ ] Auth UI funcional
- [ ] Flujo login → feed funciona

### CP2 - Validación Growth (Día 60)
- [ ] 5-10 usuarios reales
- [ ] Búsqueda exitosa ≥ 70%
- [ ] Retención 7 días ≥ 30%

### MVP (Month 1)
| Metric | Target |
|--------|--------|
| Daily active users | 100 |
| Fact-checks generated | 500/day |
| User retention (7-day) | 30% |

### Growth (Month 3)
| Metric | Target |
|--------|--------|
| Monthly active users | 500 |
| Premium conversion | 3% |
| MRR | $500 |

### Scale (Month 12)
| Metric | Target |
|--------|--------|
| Monthly active users | 5000 |
| Premium users | 150 |
| B2B clients | 10 |
| MRR | $5000 |

---

## Risk Mitigation

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Data source API changes | Medium | High | Multiple sources, fallbacks |
| Low user adoption | High | High | Build in public, content marketing |
| AI hallucination | Medium | Critical | Human review, confidence scores |
| Political bias accusations | High | Medium | Transparent methodology, multiple sources |

---

## Dependencies

### FASE 0
- GitHub account
- Supabase account
- MCP servers configured (opencode.json)

### FASE 1
- Groq API key
- NVIDIA API key
- Mistral API key
- Supabase project
- INDEC/BCRA data access

### FASE 2
- Push notification service (OneSignal/Firebase)
- Email service (Resend/SendGrid)
- Twitter API

### FASE 3
- Mercado Pago / Stripe account
- PDF generation library
- Analytics (PostHog)

---

## Team Requirements

### MVP (Solo)
- Full-stack development
- AI/LLM integration
- Basic devops

### Growth (2 people)
- Frontend specialist
- Backend/AI specialist

### Scale (3-4 people)
- 2 Full-stack devs
- 1 ML/Data engineer
- 1 Marketing/Growth