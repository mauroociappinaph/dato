# Product Requirements Document (PRD)

## DATO - Plataforma de Inteligencia Política y Económica

**Versión:** 1.0  
**Fecha:** Febrero 2026  
**Autor:** Mauro Ciappina

---

## 1. Resumen Ejecutivo

### 1.1 Visión del producto

> **Como ciudadano argentino,** quiero entender si lo que dicen los políticos es verdad y cómo afecta mi bolsillo, para tomar mejores decisiones sin ser experto en economía o política.

### 1.2 Propuesta de valor

DATO es una plataforma de inteligencia política y económica que:

- **Verifica** afirmaciones de políticos con datos oficiales
- **Traduce** economía compleja a lenguaje simple
- **Democratiza** el acceso a información confiable en Argentina

### 1.3 Diferencial competitivo

| Diferencial | Descripción |
|-------------|-------------|
| **Verificación** | Fact-checking con fuentes oficiales argentinas |
| **Lenguaje simple** | Explicaciones sin tecnicismos |
| **Automatización** | 7 agentes de IA que producen contenido automáticamente |
| **Nicho claro** | Enfoque exclusivo en Argentina |

---

## 2. Objetivos

### 2.1 Objetivos de negocio

| Objetivo | Métrica | Target |
|----------|---------|--------|
| Validar demanda | Primeros 10 pagos | Mes 1 |
| Construir MVP funcional | App deployada | Mes 1 |
| Conseguir usuarios premium | 50 suscriptores | Mes 3 |
| Escalar a B2B | 5 clientes empresa | Mes 6 |

### 2.2 Objetivos de usuario

- Entender economía argentina en menos de 1 minuto por día
- Verificar afirmaciones políticas con fuentes confiables
- Recibir explicaciones sin sesgo político

---

## 3. Scope

### 3.1 In Scope (MVP)

| Feature | Prioridad | Fase |
|---------|-----------|------|
| Feed de noticias verificadas | MUST | Fase 1 |
| Verificación de frases de políticos | MUST | Fase 1 |
| Explicación económica simple | MUST | Fase 1 |
| Búsqueda de temas/políticos | SHOULD | Fase 2 |
| Notificaciones diarias | SHOULD | Fase 2 |
| Suscripción premium | COULD | Fase 3 |
| Dashboard profesional B2B | COULD | Fase 3 |

### 3.2 Out of Scope

- Cobertura internacional
- Opiniones o editoriales
- Contenido generado por usuarios
- Red social / comunidad

---

## 4. Requisitos Funcionales

### 4.1 Noticias políticas y económicas (RF-001)

| ID | RF-001 |
|----|--------|
| **Descripción** | Resumen diario automático de política y economía argentina |
| **Prioridad** | MUST |
| **Criterios de aceptación** | - Resumen en menos de 1 minuto de lectura<br>- Lenguaje simple<br>- Solo temas relevantes |

### 4.2 Verificación de veracidad (RF-002)

| ID | RF-002 |
|----|--------|
| **Descripción** | Fact-checking de afirmaciones de políticos |
| **Prioridad** | MUST |
| **Criterios de aceptación** | - Etiqueta: Verdadero / Engañoso / Falso / Sin datos<br>- Explicación en palabras simples<br>- Fuente de datos oficial citada |

### 4.3 Explicación económica simple (RF-003)

| ID | RF-003 |
|----|--------|
| **Descripción** | Traducir indicadores económicos a lenguaje cotidiano |
| **Prioridad** | MUST |
| **Criterios de aceptación** | - Ejemplos cotidianos<br>- Sin tecnicismos<br>- Impacto en la vida diaria |

### 4.4 Búsqueda (RF-004)

| ID | RF-004 |
|----|--------|
| **Descripción** | Búsqueda de políticos, leyes o temas económicos |
| **Prioridad** | SHOULD |
| **Criterios de aceptación** | - Historial verificado por político<br>- Resultados ordenados por relevancia |

### 4.5 Notificaciones (RF-005)

| ID | RF-005 |
|----|--------|
| **Descripción** | Notificación push con resumen del día |
| **Prioridad** | SHOULD |
| **Criterios de aceptación** | - Menos de 30 segundos de lectura<br>- Tappable para ver más detalle |

---

## 5. Requisitos No Funcionales

### 5.1 Performance

| ID | Requisito | Métrica |
|----|-----------|---------|
| NFR-001 | Tiempo de carga del feed | < 2 segundos |
| NFR-002 | Tiempo de respuesta de fact-check | < 5 segundos |
| NFR-003 | Disponibilidad del sistema | 99% uptime |

### 5.2 Seguridad

| ID | Requisito |
|----|-----------|
| NFR-004 | Autenticación con JWT |
| NFR-005 | Encriptación de datos sensibles |
| NFR-006 | Rate limiting en APIs |

### 5.3 Usabilidad

| ID | Requisito |
|----|-----------|
| NFR-007 | Interfaz móvil-first |
| NFR-008 | Accesibilidad WCAG 2.1 AA |
| NFR-009 | Soporte offline básico |

---

## 6. Personas

### 6.1 Ciudadano común

| Atributo | Valor |
|----------|-------|
| **Edad** | 25-55 años |
| **Conocimiento económico** | Bajo |
| **Frecuencia de uso** | 5-10 min/día |
| **Dispositivo principal** | Mobile |
| **Pain point** | No entiende la economía |
| **Necesidad** | Explicaciones simples |

### 6.2 Usuario político informado

| Atributo | Valor |
|----------|-------|
| **Edad** | 30-60 años |
| **Conocimiento económico** | Medio-Alto |
| **Frecuencia de uso** | 15-30 min/día |
| **Dispositivo principal** | Mobile + Desktop |
| **Pain point** | Desconfianza en medios |
| **Necesidad** | Veracidad rápida |

### 6.3 Profesional / Periodista / Consultor

| Atributo | Valor |
|----------|-------|
| **Edad** | 30-55 años |
| **Conocimiento económico** | Alto |
| **Frecuencia de uso** | Variable |
| **Dispositivo principal** | Desktop |
| **Pain point** | Necesita datos confiables rápido |
| **Necesidad** | Dashboards y alertas |

---

## 7. Métricas de Éxito

### 7.1 Métricas de adopción

| Métrica | Target Fase 1 | Target Fase 3 |
|---------|---------------|---------------|
| Usuarios activos diarios | 100 | 1,000 |
| Verificaciones por día | 500 | 5,000 |
| Retención D7 | 30% | 50% |

### 7.2 Métricas de monetización

| Métrica | Target Mes 3 | Target Mes 6 |
|---------|--------------|--------------|
| Usuarios premium | 50 | 150 |
| Clientes B2B | 0 | 5 |
| MRR | $500 | $2000 |

### 7.3 Métricas de calidad

| Métrica | Target |
|---------|--------|
| Precisión de fact-check | > 95% |
| NPS | > 50 |
| Tiempo en app por sesión | > 3 min |

---

## 8. Constraints

### 8.1 Técnicas

- Backend: NestJS + Supabase
- Frontend: Next.js + React
- IA: OpenAI / Groq / Mistral (alternativas gratuitas)
- Pagos: Mercado Pago / Stripe

### 8.2 De negocio

- Sin opiniones políticas
- Solo fuentes oficiales argentinas
- Modelo freemium desde día 1

### 8.3 Legales

- Respetar derechos de autor en videos embebidos
- Citar siempre las fuentes
- Cumplir con leyes de protección de datos

---

## 9. Dependencias

| Dependencia | Tipo | Crítica |
|-------------|------|---------|
| API OpenAI | Externa | Sí |
| Datos INDEC | Externa | Sí |
| Datos BCRA | Externa | Sí |
| Supabase | Externa | Sí |
| Mercado Pago API | Externa | No |

---

## 10. Riesgos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|--------------|---------|------------|
| Sin audiencia inicial | Alta | Alto | Construir en público, contenido gratis |
| Mercado polarizado | Media | Medio | Neutralidad estricta, citar fuentes |
| APIs externas caen | Baja | Alto | Fallbacks, caching agresivo |
| Usuarios no pagan | Media | Alto | Validar con reporte PDF primero |

---

## 11. Timeline

Ver [ROADMAP.md](./ROADMAP.md) para detalles de fases y milestones.
