# User Stories - DATO

## User Stories con Gherkin (Definition of Done)

---

## US-001: Feed de Noticias Verificadas

**Como usuario,**  
quiero ver un resumen diario de política y economía argentina,  
para entender rápidamente qué pasó hoy.

**Prioridad:** Must Have  
**Story Points:** 5  
**Dependencias:** Agent 1 (Data Collector), Agent 4 (Simplifier)

### Escenarios Gherkin

```gherkin
Feature: Feed de Noticias Verificadas

  Background:
    Given el usuario tiene la app instalada
    And el dispositivo tiene conexión a internet

  Scenario: Usuario ve resumen diario exitosamente
    Given es un nuevo día con datos disponibles
    When el usuario abre la app
    Then el feed carga en menos de 2 segundos
    And muestra máximo 5 items del día
    And cada item tiene máximo 150 caracteres
    And cada item muestra fuente oficial (INDEC, BCRA, etc.)
    And cada item tiene badge de categoría (economía, política, social)
    And la hora de última actualización es visible

  Scenario: Feed vacío - Sin datos nuevos del día
    Given es un nuevo día
    And no hay datos nuevos disponibles aún
    When el usuario abre la app
    Then muestra estado vacío con ícono de calendario
    And muestra mensaje "Sin novedades hoy aún"
    And muestra última actualización con fecha de ayer
    And muestra botón "Ver ayer" para ver contenido previo

  Scenario: Error de conexión a internet
    Given el dispositivo no tiene conexión
    When el usuario intenta abrir la app
    Then muestra pantalla de error con ícono de WiFi
    And muestra mensaje "Sin conexión a internet"
    And muestra botón "Reintentar"
    And si hay cache disponible, muestra "Ver último resumen guardado"

  Scenario: Error del servidor (500)
    Given el servidor está caído
    When el usuario intenta cargar el feed
    Then muestra mensaje "Error al cargar noticias"
    And muestra botón "Reintentar"
    And registra el error en sistema de monitoreo
    And si hay cache, muestra contenido guardado con badge "Offline"

  Scenario: Usuario hace pull-to-refresh
    Given el usuario está viendo el feed
    When hace gesto de pull-to-refresh
    Then muestra indicador de carga animado
    And actualiza datos desde el servidor
    And muestra mensaje "Actualizado" o "Ya estás al día"

  Scenario: Loading state inicial
    Given el usuario abre la app por primera vez
    When los datos están cargando
    Then muestra skeleton loader con 5 placeholders
    And cada placeholder simula estructura de card
    And el skeleton desaparece en menos de 2 segundos
```

### Métricas de Aceptación

| Métrica | Valor Objetivo | Medición |
|---------|----------------|----------|
| Tiempo de carga (LCP) | < 2 segundos | Lighthouse |
| Items por día | Máximo 5 | Conteo automático |
| Longitud de item | < 150 caracteres | Validación backend |
| Disponibilidad | 99.5% uptime | Monitoring |

---

## US-002: Verificación de Frases de Políticos

**Como usuario,**  
quiero saber si una afirmación de un político es verdadera, falsa o engañosa,  
para no depender de la opinión de los medios.

**Prioridad:** Must Have  
**Story Points:** 8  
**Dependencias:** Agent 2 (Claim Extractor), Agent 3 (Fact Checker)

### Escenarios Gherkin

```gherkin
Feature: Fact-Checking de Afirmaciones Políticas

  Background:
    Given el usuario está en la app
    And el claim existe en la base de datos

  Scenario: Verificación exitosa - Afirmación verdadera
    Given un claim con veredicto "VERDADERO"
    And confianza del sistema >= 85%
    When el usuario ve el detail del claim
    Then muestra badge verde "✓ VERDADERO"
    And muestra explicación en máximo 100 palabras
    And muestra link clickeable a fuente oficial (INDEC, BCRA, Boletín Oficial)
    And muestra fecha del claim
    And muestra nombre del político que lo dijo
    And muestra contexto (discurso, entrevista, etc.)

  Scenario: Verificación exitosa - Afirmación falsa
    Given un claim con veredicto "FALSO"
    And confianza del sistema >= 85%
    When el usuario ve el detail del claim
    Then muestra badge rojo "✗ FALSO"
    And muestra explicación de por qué es falso
    And muestra dato correcto de fuente oficial
    And muestra contraste: "Dijo X, la realidad es Y"

  Scenario: Verificación exitosa - Afirmación parcialmente verdadera
    Given un claim con veredicto "PARCIALMENTE VERDADERO"
    When el usuario ve el detail del claim
    Then muestra badge amarillo "⚠ PARCIALMENTE VERDADERO"
    And explica qué parte es verdadera
    And explica qué parte es falsa o falta contexto
    And muestra matices necesarios

  Scenario: Sin datos suficientes para verificar
    Given un claim sin datos oficiales disponibles
    When el usuario ve el detail del claim
    Then muestra badge gris "⚪ SIN DATOS SUFICIENTES"
    And explica qué datos faltan
    And muestra fecha de última fuente disponible
    And muestra botón "Notificarme cuando haya datos"

  Scenario: Usuario busca claim que no existe
    Given el usuario busca una frase
    And la frase no está en la base de datos
    When presiona enter
    Then muestra mensaje "No encontramos esta frase"
    And muestra botón "Solicitar verificación"
    And sugiere 3 frases similares verificadas
    And envía notificación al equipo de contenido

  Scenario: Error en proceso de verificación
    Given el sistema no puede procesar el claim
    When el usuario intenta ver la verificación
    Then muestra mensaje "Verificación en proceso"
    And muestra badge de estado "Pendiente"
    Y ofrece notificación cuando esté listo

  Scenario: Verificación con baja confianza
    Given un claim procesado con confianza < 70%
    When el usuario ve el detail
    Then muestra badge con indicador "⚠ Confianza baja"
    And explica por qué la confianza es baja
    And sugiere esperar más datos
    Y no muestra veredicto definitivo
```

### Métricas de Aceptación

| Métrica | Valor Objetivo | Medición |
|---------|----------------|----------|
| Precisión de verificación | > 95% | Auditoría manual mensual |
| Confianza mínima mostrada | >= 70% | Validación backend |
| Tiempo de respuesta | < 5 segundos | APM |
| Fuente siempre citada | 100% | Validación automática |

---

## US-003: Explicación Económica Simple

**Como usuario sin conocimientos técnicos,**  
quiero que la app me explique inflación, dólar o medidas económicas con ejemplos cotidianos,  
para entender cómo me afecta en mi vida diaria.

**Prioridad:** Must Have  
**Story Points:** 5  
**Dependencias:** Agent 4 (Simplifier)

### Escenarios Gherkin

```gherkin
Feature: Explicaciones Económicas Simplificadas

  Background:
    Given el usuario está viendo un indicador económico

  Scenario: Explicación de inflación simple
    Given el usuario ve dato "Inflación mensual 4.2%"
    When el sistema genera explicación
    Then muestra título "¿Qué significa esto?"
    And muestra explicación: "Los precios subieron 4.2% este mes"
    And muestra ejemplo: "Si el pan costaba $100, ahora cuesta $104.20"
    And muestra máximo 3 oraciones
    Y no usa tecnicismos sin explicar

  Scenario: Explicación de dólar con comparación
    Given el usuario ve dato "Dólar oficial: $890"
    When el sistema genera explicación
    Then muestra comparación con dólar blue
    And muestra impacto: "Para viajar al exterior, necesitas..."
    And muestra gráfico de tendencia últimos 30 días
    And muestra botón "Ver más detalles"

  Scenario: Explicación de déficit fiscal
    Given el usuario ve dato "Déficit fiscal 2.1% PBI"
    When el sistema genera explicación
    Then traduce: "El Estado gastó más de lo que le entró"
    And muestra ejemplo: "Por cada $100 que recibió, gastó $102.10"
    Y no muestra el término "PBI" sin explicarlo primero

  Scenario: Usuario expande explicación
    Given el usuario lee explicación simple
    When toca botón "¿Querés más detalle?"
    Then muestra explicación extendida
    And muestra datos numéricos exactos
    And muestra fuentes oficiales
    And permite volver a versión simple

  Scenario: Sin explicación disponible
    Given un indicador sin plantilla de explicación
    When el usuario ve el dato
    Then muestra dato técnico sin simplificar
    And muestra badge "Explicación próximamente"
    And registra request para crear plantilla

  Scenario: Término técnico detectado
    Given el sistema detecta tecnicismo en texto
    When genera la explicación
    Then subraya el término
    And muestra tooltip al tocar
    And define el término en 1 frase simple
```

### Métricas de Aceptación

| Métrica | Valor Objetivo | Medición |
|---------|----------------|----------|
| Longitud máxima | 3 oraciones | Validación backend |
| Sin tecnicismos | 0 términos sin definir | NLP check |
| Comprensión usuario | > 80% | Encuesta post-lectura |
| Tiempo de lectura | < 30 segundos | Analytics |

---

## US-004: Búsqueda de Temas o Políticos

**Como usuario,**  
quiero buscar un político, ley o tema económico,  
para ver su historial verificado.

**Prioridad:** Should Have  
**Story Points:** 5  
**Dependencias:** Base de datos histórica, Pinecone

### Escenarios Gherkin

```gherkin
Feature: Búsqueda de Contenido Verificado

  Background:
    Given el usuario está en la app
    And hay al menos 100 claims en la base de datos

  Scenario: Búsqueda exitosa por nombre de político
    Given el usuario está en la pantalla de búsqueda
    When ingresa "Milei" en el campo de búsqueda
    Then muestra autocompletado con sugerencias
    And muestra resultados en menos de 1 segundo
    And muestra foto del político
    And muestra contador de claims verificados
    And muestra estadísticas: "X% verdadero, Y% falso"

  Scenario: Búsqueda exitosa por tema
    Given el usuario busca "inflación"
    When presiona enter
    Then muestra todos los claims sobre inflación
    And ordena por relevancia y fecha
    And permite filtrar por veredicto
    And permite filtrar por fecha

  Scenario: Búsqueda sin resultados
    Given el usuario busca "xyzabc123"
    When presiona enter
    Then muestra mensaje "No encontramos resultados"
    And sugiere búsquedas populares
    And sugiere términos similares
    And muestra botón "Explorar todos los temas"

  Scenario: Búsqueda con resultados lentos
    Given el usuario realiza búsqueda compleja
    When la respuesta toma más de 1 segundo
    Then muestra indicador de carga
    And muestra resultados parciales mientras carga
    Y no bloquea la UI

  Scenario: Ver historial de un político
    Given el usuario seleccionó un político
    When toca "Ver historial completo"
    Then muestra timeline de claims
    And muestra filtros por año
    And muestra estadísticas agregadas
    And permite exportar a PDF

  Scenario: Error en búsqueda vectorial
    Given Pinecone no está disponible
    When el usuario busca
    Then muestra búsqueda básica por texto
    And muestra badge "Resultados limitados"
    And registra error en logs
```

### Métricas de Aceptación

| Métrica | Valor Objetivo | Medición |
|---------|----------------|----------|
| Tiempo de respuesta | < 1 segundo | APM |
| Autocompletado | < 300ms | Medición frontend |
| Precisión de resultados | > 90% relevancia | Feedback usuario |
| Mínimo de claims | 100 para launch | DB count |

---

## US-005: Notificación Diaria Corta

**Como usuario,**  
quiero recibir una notificación con el resumen más importante del día,  
para mantenerme informado en menos de 30 segundos.

**Prioridad:** Should Have  
**Story Points:** 3  
**Dependencias:** Push notification service (OneSignal/Firebase)

### Escenarios Gherkin

```gherkin
Feature: Notificaciones Push Diarias

  Background:
    Given el usuario tiene notificaciones habilitadas
    And la app tiene permisos de notificación

  Scenario: Notificación diaria exitosa
    Given son las 9:00 AM (configurable por usuario)
    And hay nuevo contenido del día
    When el sistema envía notificación
    Then el usuario recibe push con máximo 2 oraciones
    And el título es "Resumen del día"
    And el cuerpo incluye el dato más relevante
    And al tocar, abre la app en el feed del día

  Scenario: Usuario configura horario personalizado
    Given el usuario está en configuración
    When selecciona "Notificarme a las 8:00 AM"
    Then guarda preferencia
    And envía notificación a las 8:00 AM
    And muestra confirmación "Guardado"

  Scenario: Usuario deshabilita notificaciones
    Given el usuario no quiere notificaciones
    When desactiva "Notificaciones diarias"
    Then deja de recibir pushes
    And muestra confirmación
    And mantiene acceso a historial

  Scenario: Sin contenido nuevo
    Given no hay datos nuevos del día
    When llega el horario de notificación
    Then NO envía push
    And registra "Sin contenido nuevo" en logs
    And reintenta en 2 horas si hay contenido

  Scenario: Error al enviar notificación
    Given el servicio de push falla
    When intenta enviar
    Then reintenta 3 veces con backoff exponencial
    And registra error en monitoring
    Y NO muestra error al usuario

  Scenario: Usuario toca notificación
    Given el usuario recibe notificación
    When toca la notificación
    Then abre la app
    And navega al contenido relevante
    Y marca notificación como leída

  Scenario: Permiso de notificación denegado
    Given el usuario no dio permisos de notificación
    When abre la app por primera vez
    Then muestra prompt de permiso
    And explica beneficio de notificaciones
    Y si deniega, muestra configuración manual
```

### Métricas de Aceptación

| Métrica | Valor Objetivo | Medición |
|---------|----------------|----------|
| Tasa de entrega | > 95% | OneSignal dashboard |
| Tasa de apertura | > 40% | Analytics |
| Tasa de opt-in | > 60% | Analytics |
| Longitud máxima | 2 oraciones | Validación backend |

---

## US-006: Suscripción Premium

**Como usuario frecuente,**  
quiero pagar una suscripción económica,  
para acceder a análisis más profundos y sin publicidad.

**Prioridad:** Could Have  
**Story Points:** 8  
**Dependencias:** Agent 6 (Billing & Access), Mercado Pago, Stripe

### Escenarios Gherkin

```gherkin
Feature: Sistema de Suscripciones

  Background:
    Given el usuario está autenticado
    And tiene plan "Free"

  Scenario: Usuario ve beneficios premium
    Given el usuario alcanza límite diario (3 verificaciones)
    When intenta hacer otra verificación
    Then muestra modal "Límite alcanzado"
    And muestra beneficios de Premium
    And muestra botón "Ver planes"
    And muestra botón "Recordarme mañana"

  Scenario: Upgrade a Premium exitoso
    Given el usuario selecciona plan Premium
    And selecciona método de pago (Mercado Pago)
    When completa el pago exitosamente
    Then actualiza plan a "Premium"
    And desbloquea verificaciones ilimitadas
    And muestra mensaje de bienvenida
    And envía email de confirmación
    And habilita alertas personalizadas

  Scenario: Pago fallido
    Given el usuario intenta pagar
    And la tarjeta es rechazada
    When el proceso falla
    Then muestra mensaje "Pago rechazado"
    And sugiere intentar con otro método
    Y NO cambia el plan
    And registra intento fallido

  Scenario: Usuario cancela suscripción
    Given el usuario tiene plan Premium activo
    When cancela desde configuración
    Then mantiene acceso hasta fin de período
    And muestra fecha de fin de acceso
    And envía email de confirmación
    Y NO ofrece reembolso

  Scenario: Renovación automática
    Given el usuario tiene Premium con auto-renovación
    And llega fecha de renovación
    When el sistema procesa renovación
    Then cobra automáticamente
    And envía email de confirmación
    Y si falla, notifica al usuario

  Scenario: Período de prueba
    Given usuario nuevo se registra
    When completa el registro
    Then activa 7 días de prueba Premium
    And muestra contador de días restantes
    Y al finalizar, convierte a Free

  Scenario: Downgrade de plan
    Given usuario tiene Premium
    When cambia a Free
    Then muestra advertencia de pérdida de features
    And pide confirmación
    Y si confirma, aplica al final del período

  Scenario: Verificación de estado de suscripción
    Given usuario Premium sin conexión
    When abre la app
    Then verifica estado con servidor
    Y si no puede verificar, usa cache local por 24hs
    Y después de 24hs sin verificar, degrada a modo limitado
```

### Métricas de Aceptación

| Métrica | Valor Objetivo | Medición |
|---------|----------------|----------|
| Conversión a Premium | > 5% | Analytics |
| Churn mensual | < 10% | Analytics |
| Tasa de pago exitoso | > 95% | Payment provider |
| Tiempo de activación | < 30 segundos | APM |

---

## US-007: Dashboard Profesional

**Como consultor o periodista,**  
quiero ver tendencias, votaciones y métricas políticas en tiempo real,  
para tomar decisiones o escribir informes.

**Prioridad:** Could Have  
**Story Points:** 13  
**Dependencias:** Agent 7 (Learning Loop), Data warehouse

### Escenarios Gherkin

```gherkin
Feature: Dashboard Profesional B2B

  Background:
    Given el usuario tiene plan "Professional"
    And está autenticado

  Scenario: Acceso al dashboard exitoso
    Given el usuario con plan Professional
    When navega a /dashboard
    Then muestra panel con métricas principales
    And muestra gráficos interactivos
    And carga en menos de 3 segundos
    And muestra fecha de última actualización

  Scenario: Visualización de tendencias
    Given el usuario está en el dashboard
    When selecciona "Tendencias"
    Then muestra gráfico de topics más mencionados
    And permite seleccionar rango de fechas
    And permite filtrar por categoría
    And permite comparar períodos

  Scenario: Exportar datos a CSV
    Given el usuario ve datos en el dashboard
    When hace clic en "Exportar CSV"
    Then descarga archivo CSV
    And incluye todos los datos visibles
    And incluye metadata (fecha exportación, filtros)
    And nombre del archivo incluye fecha

  Scenario: Exportar reporte PDF
    Given el usuario está en el dashboard
    When hace clic en "Generar reporte semanal"
    Then muestra indicador de carga
    And genera PDF con gráficos
    And descarga automáticamente
    Y si tarda más de 10 segundos, ofrece enviar por email

  Scenario: Alerta personalizada creada
    Given el usuario quiere alertas específicas
    When crea alerta para "menciones de dólar"
    Then guarda configuración
    Y envía notificación cuando hay matches
    And muestra en panel de alertas activas

  Scenario: API access para integración
    Given el usuario Professional
    When navega a "API Keys"
    Then puede generar API key
    And muestra documentación de endpoints
    And muestra límites de rate (1000 req/min)
    And muestra uso actual

  Scenario: Error de permisos - Usuario Free
    Given el usuario tiene plan Free
    When intenta acceder a /dashboard
    Then muestra mensaje "Funcionalidad Premium"
    And redirige a página de planes
    Y NO muestra contenido del dashboard

  Scenario: Dashboard sin datos suficientes
    Given la base de datos tiene < 100 claims
    When el usuario abre el dashboard
    Then muestra mensaje "Recopilando datos..."
    And muestra métricas parciales
    And muestra estimación de datos necesarios
    And ofrece notificación cuando esté listo

  Scenario: Timeout en consulta compleja
    Given el usuario hace consulta compleja
    When la query toma más de 30 segundos
    Then cancela la operación
    Y muestra mensaje "Consulta muy compleja"
    And sugiere reducir rango de fechas
    And sugiere usar filtros
```

### Métricas de Aceptación

| Métrica | Valor Objetivo | Medición |
|---------|----------------|----------|
| Tiempo de carga dashboard | < 3 segundos | Lighthouse |
| Exportación PDF | < 30 segundos | APM |
| API rate limit | 1000 req/min | Gateway |
| Clientes B2B activos | > 10 (mes 6) | DB count |

---

## Priorización MoSCoW

### Must Have (MVP - 30 días)
- US-001: Feed de noticias verificadas
- US-002: Verificación de frases
- US-003: Explicación económica simple

### Should Have (Fase 2 - 60 días)
- US-004: Búsqueda de temas
- US-005: Notificaciones

### Could Have (Fase 3 - 90+ días)
- US-006: Suscripción premium
- US-007: Dashboard profesional

---

## Checklist Definition of Done

| Criterio | Estado |
|----------|--------|
| ACs en formato Gherkin | ✅ |
| Escenarios de éxito definidos | ✅ |
| Escenarios de error definidos | ✅ |
| Empty states definidos | ✅ |
| Loading states definidos | ✅ |
| Métricas de performance | ✅ |
| Criterios medibles | ✅ |

---

## Métricas de Éxito

| Historia | Métrica | Target |
|----------|---------|--------|
| US-001 | Tiempo de lectura promedio | < 60 seg |
| US-002 | Tasa de engagement con fact-checks | > 30% |
| US-003 | Comprensión (encuesta) | > 80% |
| US-004 | Búsquedas por usuario/semana | > 5 |
| US-005 | Tasa de apertura notificaciones | > 40% |
| US-006 | Conversión a premium | > 5% |
| US-007 | Clientes B2B activos | > 10 |

---

*Última actualización: Febrero 2026*
*Validado con: acceptance-criteria-guardian v1.0*
