> ⚠️ **ARCHIVO HISTÓRICO** - Este documento contiene la versión original del proyecto.
> Para documentación actualizada, ver los archivos en los subdirectorios de `docs/`.

# DATO - Plataforma de Inteligencia Política y Económica

## Producto que estás imaginando

Una app que haga **3 cosas**:

### 1. Noticias políticas y económicas de Argentina

- Resumen diario automático
- Solo temas relevantes (leyes, inflación, dólar, medidas, elecciones, etc.)
- Sin ruido mediático

### 2. Verificación de veracidad

**La parte más potente:**

- Detecta frases de políticos
- Busca:
  - datos oficiales
  - estadísticas
  - antecedentes históricos
- Devuelve algo tipo:

> "Esto es verdadero / engañoso / falso"
> Explicado en lenguaje simple.

> 👉 Esto casi no existe bien hecho en Argentina. Ahí hay oportunidad fuerte.

---

### 3. Explicaciones simples (clave)

**Tu idea más importante:**

- Traducir economía y política a:
  - lenguaje cotidiano
  - ejemplos reales
  - sin tecnicismos

**Ejemplo:**

En vez de:

> "Déficit fiscal primario del 2,1% del PBI"

La app diría:

> "El Estado gastó más de lo que le entró. Por cada `$100` que recibió, gastó `$102`."

> 👉 Esto genera muchísimo engagement.

---

## Cómo lo harían los agentes de IA

**Arquitectura simple y realista:**

### Agente 1 — Recolector Argentina

- Lee medios, boletín oficial, discursos
- Filtra solo política/economía

### Agente 2 — Detector de afirmaciones

- Encuentra frases verificables:
  - "bajamos la inflación"
  - "subieron los salarios"
  - etc.

### Agente 3 — Verificador con datos

- Compara con:
  - INDEC
  - BCRA
  - presupuesto
  - leyes votadas

**Devuelve:**

| Estado | Descripción |
|--------|-------------|
| ✅ Verdadero | Coincide con datos oficiales |
| ⚠️ Parcialmente verdadero | Tiene matices |
| ❌ Falso | No coincide con datos |
| ⚪ Sin datos | No hay información suficiente |

### Agente 4 — Traductor a lenguaje simple

- Reescribe todo para que lo entienda:
  - alguien sin secundaria completa
  - alguien que no sabe economía

> 👉 Este agente es **CLAVE** para que la gente use la app.

---

## Monetización real en Argentina

Esto sí puede dar plata si se enfoca bien:

### Modelo más viable

**Suscripción baja + alto volumen**

Ejemplo:

- `$2–5 USD` por mes equivalente en pesos
- Con `5.000` usuarios pagos → ingreso interesante en Argentina

---

### Donde está el dinero grande

No en lectores… sino en:

- periodistas
- consultoras
- políticos
- empresas

**Vendiendo:**

> dashboard de inteligencia política en tiempo real

Ahí podés cobrar mucho más.

---

## Lo importante

Tu idea tiene **3 puntos muy fuertes:**

| Punto | Descripción |
|-------|-------------|
| 🎯 Nicho claro | Argentina |
| 😰 Dolor real | No se entiende la economía |
| ⚡ Diferencial | Verificación + lenguaje simple |

Eso sí puede convertirse en producto real.

---

## APIs y fuentes reales de Argentina que necesitás

Las divido por tipo para que lo veas claro.

### 1️⃣ Datos económicos oficiales (CLAVE)

#### INDEC

Sirve para verificar:

- inflación
- pobreza
- salarios
- PBI
- empleo

> 👉 Fuente principal de veracidad económica.

---

#### Banco Central de la República Argentina (BCRA)

Datos de:

- dólar oficial / reservas
- tasas de interés
- emisión monetaria
- deuda

> 👉 Fundamental para análisis económico real.

---

#### Ministerio de Economía

Publica:

- medidas económicas
- presupuesto
- anuncios oficiales

> 👉 Sirve para detectar promesas vs realidad.

---

### 2️⃣ Actividad política y leyes

#### Senado de la Nación Argentina

Datos de:

- proyectos de ley
- votaciones
- sesiones

---

#### Cámara de Diputados de la Nación Argentina

Permite seguir:

- qué leyes avanzan
- quién vota qué
- debates parlamentarios

> 👉 Esto es oro para una app de inteligencia política.

---

#### Boletín Oficial de la República Argentina

Publica:

- decretos
- resoluciones
- leyes vigentes

> 👉 La verdad legal final está acá.

---

### 3️⃣ Noticias para alimentar la IA

#### NewsData.io

- Trae noticias de medios argentinos
- Te sirve para detectar frases de políticos a verificar

---

### 4️⃣ IA para explicar en lenguaje simple

**IA gratuitas:** Nvidia, Groq, Mistral, etc.

---

## Stack mínimo realista para tu app

Con lo justo para un MVP argentino funcional:

| Categoría | Tecnologías |
|-----------|-------------|
| **Datos** | INDEC, BCRA, Senado/Diputados, Boletín Oficial, NewsData |
| **IA** | OpenAI / Groq / Mistral |
| **Backend** | NestJS + Supabase |

---

## Visión del producto

> **Como ciudadano argentino,**  
> quiero entender si lo que dicen los políticos es verdad y cómo afecta mi bolsillo,  
> para tomar mejores decisiones sin ser experto en economía o política.

> 👉 Esa es la **user story madre**.

---

## Tipos de usuario (personas)

### 1. Ciudadano común

- No entiende economía
- Quiere explicaciones simples
- Usa el celular 5–10 min por día

### 2. Usuario político informado

- Quiere ver:
  - votaciones
  - leyes
  - datos reales
- Busca veracidad rápida

### 3. Profesional / periodista / consultor (futuro premium)

- Necesita dashboards y alertas
- Este es el que paga más

---

## User Stories del MVP (las importantes)

### 1. Feed simple de noticias verificadas

**Como usuario,**  
quiero ver un resumen diario de política y economía argentina,  
para entender rápidamente qué pasó hoy.

**Criterios de aceptación:**

- Resumen en menos de 1 minuto de lectura
- Lenguaje simple
- Solo temas relevantes

---

### 2. Verificación de frases de políticos

**Como usuario,**  
quiero saber si una afirmación de un político es verdadera, falsa o engañosa,  
para no depender de la opinión de los medios.

**Debe mostrar:**

- Etiqueta: verdadero / falso / parcial
- Explicación en palabras simples
- Fuente de datos oficial

> 👉 Esta es la **feature diferencial**.

---

### 3. Explicación económica fácil

**Como usuario sin conocimientos técnicos,**  
quiero que la app me explique inflación, dólar o medidas económicas con ejemplos cotidianos,  
para entender cómo me afecta en mi vida diaria.

**Ejemplo esperado:**

> "La inflación bajó" → "Los precios siguen subiendo, pero más lento que antes."

---

### 4. Búsqueda de temas o políticos

**Como usuario,**  
quiero buscar un político, ley o tema económico,  
para ver su historial verificado.

---

### 5. Notificación diaria corta

**Como usuario,**  
quiero recibir una notificación con el resumen más importante del día,  
para mantenerme informado en menos de 30 segundos.

---

## User Stories de monetización (post-MVP)

### 6. Suscripción premium

**Como usuario frecuente,**  
quiero pagar una suscripción económica,  
para acceder a análisis más profundos y sin publicidad.

---

### 7. Dashboard profesional

**Como consultor o periodista,**  
quiero ver tendencias, votaciones y métricas políticas en tiempo real,  
para tomar decisiones o escribir informes.

> 👉 Este es el producto que **realmente escala dinero**.

---

## Prioridad real de construcción

Si lo hacemos en modo startup real:

| Fase | Tiempo | Funcionalidades |
|------|--------|-----------------|
| **Fase 1** | 30 días | Feed resumido, Verificación básica, Explicación simple |
| **Fase 2** | 60 días | Búsqueda, Notificaciones, Mejor IA |
| **Fase 3** | 90+ días | Suscripción, Dashboard profesional |

---

## Lo importante

Tu idea sí tiene forma de producto real. Y además:

- ✅ Es técnicamente viable para vos
- ✅ Tiene diferencial claro
- ✅ Puede monetizarse

> 👉 No es humo. **Es construible.**

---

## Principio clave

Tu app no debe nacer como "medio de noticias" sino como:

> **herramienta de inteligencia política/económica con IA**

Porque:

- los lectores comunes tardan en pagar
- los profesionales pagan desde el primer día

---

## 4 formas de monetizar desde el día 1

### 1️⃣ Suscripción temprana barata (validación rápida)

**Modelo simple:**

| Plan | Características |
|------|-----------------|
| **Gratis** | 3 verificaciones por día |
| **Premium** | Verificaciones ilimitadas, Alertas económicas, Historial de políticos |

**Precio inicial realista en Argentina:** `USD 2–3 / mes` equivalente en pesos

> 👉 Objetivo NO es ganar mucho, sino probar que alguien paga.  
> Con **50 usuarios pagos** ya validaste negocio.

---

### 2️⃣ Reporte político semanal en PDF (la más rápida)

Esto es **CLAVE** porque podés venderlo antes de terminar la app.

**Producto:**

> "Resumen político-económico de Argentina explicado en simple – semanal"

**Clientes posibles:**

- periodistas freelance
- consultoras
- pymes
- gente interesada en economía

**Precio realista:** `USD 5–15` por semana

> 👉 Con **20 clientes** ya generás ingresos.  
> Esto se puede vender en **7 días**.

---

### 3️⃣ Servicio B2B de monitoreo (donde está la plata)

**Ofrecés algo así:**

> "Te avisamos en tiempo real cuando pasa algo político/económico que afecta tu negocio".

**Clientes:**

- estudios contables
- fintech
- empresas importadoras
- agencias de PR

**Precio:** `USD 50–200 / mes` por cliente

> 👉 Con **5 clientes** ya es ingreso serio en Argentina.  
> Este es el **camino más fuerte**.

---

### 4️⃣ Donaciones + comunidad (cash inmediato)

Podés lanzar con botón de apoyo en:

- Mercado Pago
- Stripe

**Mensaje claro:**

> "Si esta info te sirve para entender la economía, apoyá el proyecto."

Muchos proyectos políticos arrancan así.

---

## Estrategia realista (la que yo haría en tu lugar)

| Período | Acción | Resultado |
|---------|--------|-----------|
| **Semana 1–2** | Crear reporte semanal PDF, Vender por redes/contactos | 💰 Primer dinero |
| **Mes 1** | MVP simple de la app, Activar suscripción barata | ✅ Validación real |
| **Mes 2–3** | Ofrecer monitoreo B2B | 💪 Ingresos fuertes |

---

## Verdad importante

Si esto funciona, la plata NO vendrá de lectores, sino de:

> **empresas y profesionales que necesitan entender la política.**

Y eso encaja perfecto con:

- tu perfil técnico
- automatización con IA
- producto escalable

---

## ¿Conviene usar videos de YouTube?

### Ventajas reales

#### 1. Más credibilidad

Ver al político diciendo la frase exacta:

- evita acusaciones de manipulación
- aumenta confianza en tu verificación

> 👉 Esto es clave en política.

---

#### 2. Más retención de usuarios

La gente:

- mira más de lo que lee
- entiende mejor con video corto

Un clip de `20–40 segundos` funciona perfecto.

---

#### 3. Costo cero de contenido

No tenés que producir videos:

- usás material público
- solo agregás contexto y verificación con IA

> 👉 Muy buen modelo de producto.

---

### Riesgos a tener en cuenta

#### 1. Derechos y uso correcto

- Debés embeber el video, no descargarlo
- Usar siempre el reproductor oficial

> Así evitás problemas legales.

---

#### 2. Ruido político / propaganda

Muchos videos son:

- sesgados
- recortados
- fuera de contexto

Por eso tu valor no es el video, sino:

> **la verificación + explicación simple.**

---

### Forma inteligente de usarlos en tu app

**Modelo ideal de pantalla:**

Frase verificada:

1. Clip corto del político (YouTube embebido)
2. Etiqueta:
   - ✅ Verdadero
   - ⚠️ Engañoso
   - ❌ Falso
3. Explicación en lenguaje simple
4. Fuente oficial:
   - INDEC
   - BCRA
   - leyes

> 👉 Esa combinación es **muy potente**.

---

### Recomendación real

Sí, incluilos, pero así:

- solo clips cortos relevantes
- siempre con verificación debajo
- nunca como contenido principal

> Tu producto no es video. Tu producto es: **entender la política sin que te mientan.**

---

## API oficial: YouTube Data API v3

La principal es la **YouTube Data API v3**, que permite:

- Obtener metadatos de videos (título, descripción, duración, vistas, likes)
- Buscar videos por palabra clave
- Acceder a canales, playlists y comentarios
- Gestionar contenido si el usuario autoriza tu app

Esta API usa REST y requiere clave de Google Cloud + cuota diaria.

> 👉 Es la opción más segura y legal para integrar YouTube en apps o sistemas de IA.

---

### Obtener subtítulos / transcripciones

La Data API no siempre da directamente la transcripción, pero:

- Podés obtener el ID de captions del video
- Luego descargar subtítulos si están disponibles

Algunas librerías externas automatizan esto, pero no son oficiales y pueden romperse si YouTube cambia su sistema.

---

### Alternativas comunes usadas en IA

En proyectos de agentes o RAG se suele:

1. Usar YouTube Data API → metadatos + links
2. Usar librerías de transcripción → texto del video
3. Enviar el texto a un modelo de embeddings → búsqueda semántica

Esto es lo que hacen muchas apps de resumen automático de videos.

---

### ¿Conviene incluir videos de YouTube en tu producto?

| ✅ Sí conviene | ❌ No conviene |
|----------------|----------------|
| Querés enriquecer respuestas con contenido real | Dependés demasiado de transcripciones no oficiales |
| Vas a hacer RAG con videos educativos | Tu producto requiere datos 100% estables |
| Necesitás analytics de tendencias | |

---

## ¿Podés monetizar HOY MISMO?

**Respuesta honesta:**

> Sí, pero no con una app.  
> Sino con un **producto manual primero.**

Esto es fundamental en startups.

---

## Forma real de monetizar hoy (sin código)

**Producto vendible hoy:**

> "Resumen político-económico semanal explicado simple"

**Formato:**

- PDF de 5–8 páginas
- Hecho con IA + curaduría tuya
- Entregado por mail o WhatsApp

---

### A quién venderle hoy

No al público masivo. Sino a:

- contadores
- pymes
- gente que sigue dólar / inflación
- consultores

> 👉 Esa gente sí paga ya.

---

### Precio realista en Argentina

`USD 5–10` por semana equivalente en pesos.

**Con solo:**

- `10 clientes` → ya validaste negocio
- `30 clientes` → ya es ingreso real

Y todo antes de programar la app.

---

## Diagnóstico crudo del modelo

### Lo bueno ✅

- Problema real: nadie entiende la economía
- Diferencial: verificación + lenguaje simple
- Costos bajos con IA
- Escalable a B2B (donde está la plata)

> 👉 Sí tiene potencial real.

---

### Lo riesgoso ⚠️

- Si lo hacés como "medio de noticias" → muere
- Si esperás miles de usuarios → tardás años
- Si no cobrás desde el inicio → se enfría

---

### Veredicto honesto

Esto NO es una idea loca. Es un producto tech viable en Argentina si seguís este camino:

| Paso | Cuándo | Qué hacer |
|------|--------|-----------|
| 1 | Hoy | Vender reporte manual |
| 2 | Este mes | Validar que alguien paga |
| 3 | Después | Recién ahí construir app |

> **Ese orden cambia todo.**

---

## Análisis como INVERSOR TEMPRANO (modo brutal)

### Pregunta central

> ¿Pondría dinero en esto hoy?

### Lo bueno que veo

- Problema real en Argentina: nadie entiende economía ni política
- Diferencial claro: verificación + lenguaje simple
- Costos de producción muy bajos con IA
- Posible salida B2B (consultoras, empresas)

> 👉 Esto es lo que más me interesa como inversor.

### Lo malo (importante)

- No sos periodista ni figura pública → cero audiencia inicial
- Mercado político es altamente polarizado → difícil construir confianza
- Muchísimos proyectos "medios digitales" fracasan → alto riesgo de irrelevancia
- Sin distribución, la idea vale casi 0

### Veredicto inversor

- ❌ No invertiría dinero hoy
- ✅ Sí invertiría si:
  - conseguís 20–50 personas pagando un reporte
  - probás demanda sin app

> 👉 Para un inversor, **la tracción manda.**  
> Sin tracción = no existe.

---

## Análisis como ANALISTA DE NEGOCIO / MONETIZACIÓN

### Pregunta

> ¿Puede generar ingresos reales en Argentina?

### Respuesta corta

> Sí, pero **SOLO en B2B o nicho pago.**  
> No en público masivo al inicio.

---

### Escenarios reales de ingresos

#### Escenario pesimista (más probable al inicio)

- 10 clientes reporte semanal
- `USD 5` cada uno

➡️ `USD 50/semana`  
➡️ `~USD 200/mes`

> 👉 Validación, no negocio.

---

#### Escenario medio (si ejecutás bien)

- 40 clientes reporte
- 3 clientes B2B de monitoreo a `USD 80`

➡️ `~USD 700–900/mes`

> 👉 Ingreso real en Argentina.

---

#### Escenario bueno (6–12 meses)

- 100 suscriptores
- 10 clientes B2B

➡️ `USD 2.000–3.000/mes`

> 👉 Ya es micro-empresa viable.

---

### Riesgo clave de negocio

No es técnico. No es legal.

> **Es conseguir los primeros 10 pagos.**

Ahí mueren el **90%** de ideas.

---

## Análisis como PRODUCT MANAGER DE STARTUP

### Diagnóstico principal

Tu idea NO debe empezar como app.

Debe empezar como:

> **servicio manual pagado.**

Porque:

- necesitás validar dolor real
- necesitás aprender qué le importa a la gente
- necesitás caja rápida

---

### MVP real (no el técnico)

No es una app. Es esto:

> **PDF semanal simple**  
> "Qué pasó en la economía argentina explicado fácil".

5 páginas. Nada más.

**Eso es el verdadero MVP.**

---

### Métrica única que importa

No descargas.  
No likes.  
No visitas.

> 👉 **Gente pagando.**

---

## Cómo conseguir plata HOY

*(sin saber vender, sin contactos políticos, sin audiencia)*

Voy a ser extremadamente concreto.

---

### Paso 1 — Producto en 24 horas

Crear:

> **PDF de 5 páginas**  
> resumen económico semanal explicado simple.

Con IA lo hacés en `2–3 horas`.

---

### Paso 2 — Primeros clientes reales (sin vender "difícil")

No busques desconocidos. Buscá:

- amigos
- conocidos
- contadores
- dueños de negocio chicos
- gente que siempre habla del dólar

**Solo decir:**

> "Estoy probando un informe semanal de economía explicado simple.  
> ¿Te lo puedo mandar?  
> Si te sirve, sale X por semana."

Nada más.

No es venta agresiva. Es validación.

---

### Paso 3 — Objetivo realista

No 100 clientes. No viral.

> 👉 **3 personas que paguen.**

Con 3 pagos:

- ya no es idea
- ya es negocio real
- recién ahí conviene seguir

---

## Veredicto final (imparcial)

| Pregunta | Respuesta |
|----------|-----------|
| ¿Es buena idea? | ✅ Sí |
| ¿Es fácil? | ❌ No |
| ¿Puede darte plata? | ✅ Sí, pero solo si vendés antes de programar |
| ¿Tu mayor riesgo? | 👉 Es no salir a probar con gente real |

---

## APIs base de datos públicas (obligatorias)

Estas te dan veracidad y legitimidad.

### Portal de datos del Estado argentino

El sitio **Datos Argentina** (portal oficial) ofrece datasets abiertos, series, organizaciones y APIs en temas como economía, gobierno, población, transporte o justicia.

Los datos son públicos, reutilizables y pensados para crear aplicaciones y visualizaciones.

> 👉 **Uso en tu producto:**
> - Indicadores económicos automáticos
> - Datos oficiales para fact-checking
> - Gráficos simples para el lector común

Esto es la **columna vertebral de tu credibilidad**.

---

### Economía y finanzas (clave para tráfico)

Para un diario político argentino, esto genera la mayor demanda.

**APIs que necesitas:**

| API | Datos |
|-----|-------|
| **INDEC** | inflación, pobreza, empleo |
| **BCRA** | dólar, tasas, reservas |
| **Ministerio de Economía** | presupuesto, deuda |

*(No todos tienen API limpia; algunos salen del portal de datos abiertos)*

> 👉 **Valor productivo:**
> - Notas automáticas tipo:
>   - "Inflación de enero explicada fácil"
>   - "Qué significa la suba del dólar hoy"

Esto se puede generar **100%** con IA + datos oficiales.

---

### Noticias y contenido multimedia

Para que el diario no sea solo números.

#### API de YouTube

La YouTube Data API permite:

- buscar videos por tema o fecha
- subir videos
- gestionar playlists y canales
- integrar contenido en tu app

> 👉 **Uso ideal:**
> - Mostrar discursos de diputados
> - Resúmenes de debates
> - Videos explicativos generados por IA

> ⚠️ **Ojo:** investigaciones muestran que los resultados de búsqueda del API pueden variar según popularidad y momento, lo que dificulta obtener muestras históricas representativas.

Esto significa:
- → no usar YouTube como fuente única de verdad
- → solo como complemento visual

---

### Datos políticos institucionales

Para cubrir política real.

**APIs / fuentes útiles:**

| Fuente | Datos |
|--------|-------|
| **Senado argentino** | proyectos de ley |
| **Diputados** | votaciones y sesiones |
| **Boletín Oficial** | decretos |
| **Justicia electoral** | partidos y candidatos |

Muchos no tienen API formal, pero:

- se scrapean
- o están en datos abiertos del Estado

---

### Fact-checking automatizado (tu diferencial)

**Arquitectura recomendada:**

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    ENTRADAS     │────▶│ PROCESAMIENTO IA │────▶│     SALIDA      │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│ Datos oficiales │     │ Extracción de    │     │ Verdadero /     │
│ Noticias        │     │ afirmaciones     │     │ Engañoso /      │
│ Discursos       │     │ Comparación con  │     │ Falso           │
│ Videos YouTube  │     │ datos reales     │     │ Explicación     │
└─────────────────┘     │ Resumen simple   │     │ fácil           │
                        └──────────────────┘     └─────────────────┘
```

> Esto es **producto diferenciador real**.

---

### Stack mínimo viable (MVP realista)

Pensando en vos (React + Zustand + Nest + Prisma):

| Capa | Componentes |
|------|-------------|
| **Backend** | Cron jobs que llaman APIs públicas, Base histórica de indicadores, Motor IA de resumen |
| **Frontend** | Feed diario automático, Sección "economía fácil", Fact-check de frases políticas |

---

### Las 5 APIs mínimas para lanzar

Si tuviera que elegir SOLO las esenciales:

1. Datos abiertos del Estado argentino
2. INDEC
3. BCRA
4. YouTube Data API
5. Scraper de Boletín Oficial / Congreso

> Con eso ya podés lanzar.

---

## ¿Cuánto se pueden reducir los tiempos?

### Desarrollo tradicional

Un producto así normalmente tarda:

| Etapa | Tiempo |
|-------|--------|
| MVP usable | 3–6 meses |
| Producto monetizable | 9–12 meses |

Porque incluye:

- backend
- scraping/APIs
- IA
- frontend
- pagos
- UX
- iteración con usuarios

---

### Con vibecoding realista

Usando:

- generación de código con IA
- plantillas Next/Nest
- librerías listas
- RAG prearmado
- deploy automático

Los tiempos cambian muchísimo:

#### MVP funcional

➡️ `2–4 semanas`

Con:

- feed económico automático
- verificación simple
- explicación en lenguaje fácil
- login básico
- deploy online

> Esto ya se puede mostrar y cobrar.

---

#### Primera versión monetizable

➡️ `4–8 semanas`

Incluye:

- suscripción
- reportes PDF automáticos
- historial de verificaciones
- notificaciones

> 👉 Acá ya puede entrar plata real.

---

#### Producto sólido

➡️ `3 meses`

Con:

- dashboards
- mejor fact-checking
- B2B
- analytics

> Esto ya es micro-startup seria.

---

## Qué acelera MÁS con vibecoding

| Área | Antes | Ahora |
|------|-------|-------|
| **Backend y scraping** | semanas | horas–días |
| **IA de resumen/verificación** | investigación larga | plug & play |
| **Frontend** | 1–2 meses | días con componentes generados |

---

## Lo que NO acelera tanto

Esto es clave como PM honesto:

1. **Conseguir usuarios pagos** → esto sigue siendo lento
2. **Confianza política** → tarda meses sí o sí
3. **Definir qué contenido importa** → requiere iteración real con gente

> Nada de eso lo acelera la IA.

---

### Comparación de tiempos

| Etapa | Tradicional | Vibecoding |
|-------|-------------|------------|
| MVP visible | 3–6 meses | 2–4 semanas |
| Monetización inicial | 6–9 meses | 1–2 meses |
| Producto sólido | 12 meses | 3 meses |

> 👉 Reducción real: **70–80%** del tiempo técnico.

Pero:

> El cuello de botella deja de ser programar  
> y pasa a ser **validar negocio**.

---

## Veredicto como Product Manager

Sí, con vibecoding:

- podés lanzar en **30 días**
- podés cobrar en **60 días**

Lo difícil ya no es construir. Lo difícil es:

> **que alguien pague por entender la política.**

---

## Principio clave

Tu producto no es una app.

Es un **sistema de agentes** que produce información confiable automáticamente.

Si los agentes están bien diseñados:

- ➡️ la app casi se arma sola
- ➡️ el contenido sale todos los días
- ➡️ podés monetizar sin escribir nada manual

---

## Los 7 agentes indispensables (núcleo real)

### 1️⃣ Agente Recolector de Datos (Data Collector)

**Función:** Traer información cruda todos los días.

**Fuentes:**

- economía oficial
- leyes / decretos
- noticias políticas
- discursos / videos

> Sin este agente → **no existe producto.**

**Debe correr:** cada `1–3 horas` automático.

---

### 2️⃣ Agente Detector de Hechos Verificables (Claim Extractor)

Lee noticias, discursos, medidas, etc. Y detecta frases tipo:

- "bajó la inflación"
- "subieron los salarios"
- "no hay emisión"

Convierte texto largo en:

> ➡️ **afirmaciones chequeables**

> Este agente es **CRÍTICO.** Sin esto no hay fact-checking.

---

### 3️⃣ Agente Verificador con Datos Oficiales (Fact Checker)

Toma cada afirmación y la compara con:

- estadísticas reales
- series históricas
- leyes vigentes

**Devuelve:**

| Estado | Badge |
|--------|-------|
| Verdadero | ✅ |
| Engañoso | ⚠️ |
| Falso | ❌ |
| Sin datos | ⚪ |

> 👉 Este es el **corazón del producto.**

---

### 4️⃣ Agente Traductor a Lenguaje Simple (Simplifier)

Convierte economía/política técnica en:

> ➡️ **explicación que entienda alguien común.**

**Ejemplo:**

> "déficit primario 2% PBI" → "el Estado gastó más de lo que le entró"

> 👉 Este agente genera **engagement.** Sin esto, la gente abandona.

---

### 5️⃣ Agente Generador de Contenido (Publisher)

Arma automáticamente:

- resumen diario
- notas cortas
- reportes semanales
- PDF pagos

Y los publica en:

- web
- mail
- WhatsApp
- app

> 👉 Este agente convierte **IA en producto.**

---

### 6️⃣ Agente de Monetización (Billing & Access)

**Controla:**

- quién paga
- qué puede ver
- generación de reportes premium
- suscripciones

> Sin este agente: ➡️ **no hay negocio, solo hobby.**

---

### 7️⃣ Agente de Feedback y Mejora (Learning Loop)

**Mide:**

- qué leen más
- qué pagan
- qué abandonan
- qué temas interesan

**Y ajusta:**

- resúmenes
- temas
- frecuencia

> 👉 Este agente hace que el sistema **mejore solo.**

---

## Orden correcto de construcción (clave PM)

No los hagas todos juntos.

### Fase 1 — que funcione

1. Recolector
2. Verificador
3. Simplificador
4. Generador de resumen

> ➡️ Ya tenés producto usable.

---

### Fase 2 — que gane dinero

5. Monetización
6. Reportes PDF automáticos

> ➡️ Ya tenés negocio.

---

### Fase 3 — que escale

7. Feedback automático
8. Dashboards B2B (extra)

> ➡️ Ya tenés startup.

---

## API keys que necesitás sí o sí

Para que tu sistema de agentes funcione automático y monetizable.

Sin teoría. Solo lo esencial para construir.

---

### 1) IA y procesamiento de texto

**Proveedores LLM soportados**

El proyecto utiliza una estrategia multi-proveedor:

- **Groq** (proveedor principal por defecto)
- **NVIDIA NIM** (alternativa)
- **Mistral** (alternativa)
- **OpenRouter** (alternativa)
- **OpenAI** (opcional, no requerido)

Para:

- extraer afirmaciones políticas
- hacer fact-checking con contexto
- resumir economía en lenguaje simple
- generar reportes y PDFs

> 👉 Configura al menos uno de los proveedores soportados.  
> OpenAI NO es obligatorio.

---

### 2) Videos y discursos políticos

**YouTube Data API**

Para:

- buscar discursos de políticos
- obtener metadatos y subtítulos
- embeber clips en la app

> 👉 No es crítica para el MVP, pero sí para **credibilidad y engagement.**

---

### 3) Datos económicos oficiales (credibilidad)

- **INDEC**
- **Banco Central de la República Argentina**
- **Datos Argentina**

Para:

- inflación
- dólar / tasas
- empleo / pobreza
- series históricas

> 👉 Estas fuentes hacen que tu fact-checking sea **defendible y serio.**

*(A veces no usan API key directa, pero igual son core.)*

---

### 4) Noticias automáticas

**NewsData.io**

Para:

- traer titulares políticos argentinos
- detectar frases a verificar
- alimentar a los agentes IA

> 👉 Acelera muchísimo el sistema automático.

---

### 5) Pagos y monetización (NEGOCIO REAL)

- **Mercado Pago**
- **Stripe**

Para:

- suscripciones mensuales
- venta de reportes PDF
- control de acceso premium

> 👉 Sin esto **no hay ingresos.**

---

### 6) Infraestructura y backend

**Supabase** (opcional pero muy útil)

Para:

- base de datos
- auth
- storage de reportes

> Reduce semanas de trabajo.

---

## Resumen PM — solo lo mínimo para lanzar

### MVP REAL (podés construir en 2–4 semanas)

Necesitás solo:

1. OpenAI
2. Datos económicos oficiales
3. NewsData
4. Mercado Pago o Stripe

> 👉 Con eso ya podés:
> - generar contenido automático
> - verificar economía
> - vender reportes

**Eso ya es negocio funcional.**

---

### Fase siguiente (mejora de producto)

Agregar:

- YouTube API → credibilidad
- Supabase → velocidad de desarrollo

---

### Veredicto honesto

Tu stack de API keys no es grande. Con **4 claves bien usadas** ya podés:

> lanzar, validar y cobrar en Argentina.

Y eso es lo que importa.

---

## NUEVO PLAN (PARA ALGUIEN SIN AUDIENCIA)

### Fase 1: Construir audiencia MIENTRAS construís producto

**Mes 1-2: Construir + mostrar proceso**

**Qué hacer:**

1. Empezar un blog técnico / Twitter / LinkedIn  
   Tema: *"Cómo estoy construyendo un verificador político con IA en Argentina"*

2. Publicar TODO el proceso:
   - Día 1: "Armé el scraper de INDEC"
   - Día 5: "Primer fact-check automático funcionando"
   - Día 10: "La IA detectó 15 frases verificables hoy"
   - Día 20: "Así explico inflación en lenguaje simple"

3. Dar valor ANTES de pedir plata:
   - Publicar verificaciones gratis en redes
   - Subir reportes semanales a Medium/LinkedIn
   - Compartir hallazgos interesantes

**Ejemplo de posteo:**

> 🤖 Hice que GPT-4 verificara el discurso de [político]
>
> Frase: "La inflación bajó 50%"
> Dato real (INDEC): Bajó 12%
>
> Conclusión: Engañoso ⚠️
>
> [Mini explicación simple]

**Por qué funciona:**

- ✅ No necesitás vender nada
- ✅ La gente comparte contenido útil
- ✅ Vas construyendo confianza
- ✅ Generás audiencia orgánica

---

**Mes 2-3: Automatizar distribución**

Crear canales automáticos:

1. **Newsletter automático gratis**
   - 1 mail semanal
   - Resumen económico simple
   - Fact-checks de la semana

2. **Herramienta:** Substack (gratis, fácil)

3. **Bot de Telegram/WhatsApp**
   - Envía resumen diario
   - La gente se suscribe sola
   - Costo: `$0`

4. **Cuenta de Twitter/X automatizada**
   - 3 tweets diarios automáticos
   - Fact-checks + explicaciones
   - Engagement automático

**Objetivo:**

- ❌ NO vender todavía
- ✅ SÍ conseguir 100-500 personas siguiéndote

---

**Mes 3-4: Monetización SIN VENDER**

Acá es donde cambia todo.

**Modelo:** Valor primero, pago después

**Estructura:**

```
Gratis (80% del contenido):
├─ Resumen diario económico
├─ Fact-checks básicos
├─ Newsletter semanal
└─ Twitter/Telegram

Premium USD 3/mes (20% extra):
├─ Reporte PDF semanal profundo
├─ Alertas económicas personalizadas
├─ Acceso a histórico completo
└─ Dashboard con gráficos
```

**Forma de presentarlo (NO como venta):**

> 📢 Después de 3 meses construyendo esto en público, algunos me pidieron versión más completa.
>
> Armé una versión premium:
> - Reportes PDF semanales
> - Alertas personalizadas
> - Histórico completo
>
> `USD 3/mes` (precio de un café)
>
> Si te sirvió lo gratis, esto te va a re servir.  
> Si no, seguí usando gratis, cero drama.
>
> [Link]

**Por qué esto NO es "vender":**

- ✅ Ya diste valor gratis por meses
- ✅ La gente ya confía
- ✅ Es opcional, no agresivo
- ✅ El precio es irrisorio

---

**Mes 4-6: B2B orgánico**

Esperar a que vengan a vos.

Cuando tengas:

- ✅ Contenido constante
- ✅ 200-500 seguidores
- ✅ Producto funcionando

Van a pasar dos cosas:

1. **Consultoras/empresas te van a contactar:**  
   "Hola, estamos viendo tu contenido. ¿Hacés algo custom para empresas?"

2. **Periodistas te van a citar:**  
   Y ahí tu nombre empieza a valer.

**En ese momento, ofrecés servicio B2B:**

- Dashboard personalizado
- Alertas por tema
- API de datos
- Reportes a medida

**Precio:** `USD 100-300/mes` por cliente

> Con solo **3-5 clientes B2B:** → Ya tenés ingreso serio en Argentina

---

## MODELO COMPLETO (SIN SABER VENDER)

**Embudo automático:**

```
Contenido gratis en redes (IA automática)
         ↓
Gente descubre tu contenido
         ↓
Se suscriben a newsletter/Telegram
         ↓
Consumen gratis 1-2 meses
         ↓
5-10% pasan a premium (sin que vendas)
         ↓
Empresas te contactan (B2B orgánico)
```

---

## PROYECCIÓN REALISTA (SIN VENDER)

| Mes | Seguidores | Premium | B2B | Ingresos |
|-----|------------|---------|-----|----------|
| 1-2 | 50 | 0 | 0 | `$0` |
| 3 | 200 | 5 | 0 | `$15` |
| 4 | 400 | 15 | 0 | `$45` |
| 5 | 700 | 30 | 1 | `$190` |
| 6 | 1000 | 50 | 2 | `$350` |
| 9 | 2000 | 100 | 4 | `$700` |
| 12 | 3500 | 150 | 6 | `$1,050` |

> Esto es **ORGÁNICO**, sin vender activamente.

---

## STACK TÉCNICO PARA ESTO

Producto automático (haces una vez):

```
Backend (Nest.js):
├─ Cron jobs diarios
│  ├─ Scrapear INDEC/BCRA
│  ├─ Buscar noticias
│  └─ Generar fact-checks con IA
│
├─ API REST
│  ├─ Contenido gratis
│  └─ Premium (con auth)
│
└─ Workers
   ├─ Newsletter automático
   ├─ Bot Telegram
   └─ Posts Twitter

Frontend (Next.js):
├─ Landing simple
├─ Blog de fact-checks
├─ Dashboard premium
└─ Paywall Mercado Pago
```

**Distribución automática:**

- ✅ Substack (newsletter)
- ✅ Telegram Bot
- ✅ Twitter API (auto-posteo)
- ✅ Medium (syndication)

> **Trabajo manual diario: 0 horas**  
> Todo corre solo.

---

## POR QUÉ ESTO SÍ FUNCIONA SIN SABER VENDER

Estás usando:

### 1. Contenido como distribución

- No vendés, educás
- La gente comparte valor
- Algoritmos te ayudan

### 2. Construcción en público

- Transparencia genera confianza
- Devs/tech respetan el proceso
- Te diferencia de medios tradicionales

### 3. Producto que se vende solo

- Si es útil, la gente paga
- No necesitás pitch
- El valor es obvio

### 4. Paciencia estratégica

- Primeros 3 meses: `$0` esperado
- Mes 6: primeros ingresos
- Mes 12: ingreso digno

---

## PLAN DE ACCIÓN CONCRETO (30 DÍAS)

| Semana | Acciones |
|--------|----------|
| **1-2** | Crear Twitter/LinkedIn, Primer post: "Voy a construir X en público", Armar MVP técnico básico, Primer fact-check automático |
| **3** | Publicar 1 fact-check/día gratis, Crear newsletter en Substack, Automatizar scraping INDEC |
| **4** | Bot de Telegram básico, 3 posts técnicos en LinkedIn, Landing page simple |

**Objetivo mes 1:**

- ✅ 50-100 seguidores
- ✅ Sistema automático funcionando
- ✅ 0 ventas (normal)

---

## VEREDICTO FINAL BRUTAL

**Tu situación (sin audiencia, sin saber vender):**

| ❌ NO hagas | ✅ SÍ hace |
|-------------|-----------|
| App política que necesita marketing | Producto automático + construir en público |

**Ventajas de tu perfil:**

- ✅ Sabés automatizar todo
- ✅ Podés construir rápido con IA
- ✅ Tech Twitter/LinkedIn valora construcción en público
- ✅ No necesitás ser famoso, necesitás ser útil

**La verdad:**

> No necesitás saber vender.  
> Necesitás construir algo tan útil que se venda solo.

Pero eso toma **6-12 meses** de construcción pública constante.

---

## LA PREGUNTA HONESTA

¿Estás dispuesto a:

- ✅ Publicar gratis por 3 meses
- ✅ Construir en público
- ✅ Tener paciencia hasta mes 6
- ✅ Automatizar todo con código

**Si SÍ:** → Esto puede funcionar sin saber vender

**Si NO:** → Mejor buscar otra idea

---

# MANUAL DE MARCA - DATO

> Política argentina verificada con datos reales

## ÍNDICE

1. Identidad de Marca
2. Logo y Variantes
3. Paleta de Colores
4. Tipografía
5. Elementos Gráficos
6. Tono y Voz
7. Aplicaciones Digitales
8. Usos Incorrectos
9. Assets y Recursos

---

## 1. IDENTIDAD DE MARCA

### Posicionamiento

**DATO** es la plataforma de inteligencia política y económica que traduce la complejidad de Argentina a datos verificables y lenguaje simple.

**Promesa de marca:**

> "No opiniones. Datos."
Misión:
Democratizar el acceso a información política y económica confiable en Argentina mediante IA y datos oficiales.
Visión:
Ser la fuente de verdad más confiable para entender la economía y política argentina.
Valores:
1. Verificable - Todo se respalda con datos oficiales
2. Simple - Complejidad traducida a lenguaje cotidiano
3. Neutral - Sin sesgo político
4. Transparente - Mostramos las fuentes siempre
5. Automático - Tecnología al servicio de la verdad

🎭 Personalidad de Marca
Si DATO fuera una persona:
* 🧠 Inteligente pero no pedante
* 📊 Analítica pero accesible
* 🎯 Directa sin ser agresiva
* 🤝 Confiable como un amigo que sabe
* ⚡ Ágil y al día
* 🔍 Curiosa pero rigurosa
NO es:
* ❌ Político
* ❌ Sensacionalista
* ❌ Complicado
* ❌ Elitista
* ❌ Aburrido

2. LOGO Y VARIANTES
Logo Principal

text


┌─────────────────────────┐
│                         │
│    D  A  T  O          │
│    ━━━━━━━━━━          │
│                         │
└─────────────────────────┘
Construcción:
Wordmark: DATO
* Tipografía: Inter Black (o similar sans-serif bold)
* Tracking: +50 (espaciado amplio)
* Mayúsculas
Elemento distintivo:
* Línea de datos debajo (representa gráfico/datos)
* 4 segmentos de diferente altura (como barras de gráfico)

Variantes del Logo
A. Logo Principal (Horizontal)

text


DATO
━━━━━━━━━━
el dato real
Uso: Landing, web, documentos

B. Logo Compacto (Isotipo)

text


┌────┐
│ D  │
│ ━━ │
└────┘
Uso: App móvil, favicon, redes sociales

C. Logo Vertical

text


   DATO
   ━━━━━━━━━━
el dato real de
  Argentina
Uso: Stories, banners verticales

D. Logo en Negativo (fondo oscuro)

text


DATO (blanco)
━━━━━━━━━━ (naranja)

Área de Protección
Espacio mínimo alrededor del logo = altura de la "D"

text


    [D altura]
    ↕
←→ DATO ←→
    ↕
Nunca:
* Comprimir o estirar
* Rotar
* Añadir sombras o efectos
* Cambiar colores fuera de la paleta
* Usar tamaño menor a 24px de altura

3. PALETA DE COLORES
Colores Primarios
DATO Black (Principal)

text


HEX: #0A0A0A
RGB: 10, 10, 10
CMYK: 0, 0, 0, 96

Uso: Logo, títulos, texto principal
DATO Orange (Acento)

text


HEX: #FF6B35
RGB: 255, 107, 53
CMYK: 0, 58, 79, 0

Uso: Highlights, CTAs, datos verificados

Colores Secundarios
Data Blue (Información)

text


HEX: #004E89
RGB: 0, 78, 137
CMYK: 100, 43, 0, 46

Uso: Links, gráficos, elementos informativos
Neutral Gray

text


HEX: #F5F5F5
RGB: 245, 245, 245
CMYK: 0, 0, 0, 4

Uso: Fondos, separadores
Text Gray

text


HEX: #4A4A4A
RGB: 74, 74, 74
CMYK: 0, 0, 0, 71

Uso: Texto secundario, descripciones

Colores de Sistema (Verificación)
Verdadero

text


HEX: #06D6A0
RGB: 6, 214, 160
CMYK: 68, 0, 42, 0

Uso: Fact-check verdadero ✓
Falso

text


HEX: #EF476F
RGB: 239, 71, 111
CMYK: 0, 82, 43, 0

Uso: Fact-check falso ✗
Engañoso

text


HEX: #FFD166
RGB: 255, 209, 102
CMYK: 0, 18, 60, 0

Uso: Fact-check parcial ⚠
Sin Datos

text


HEX: #B8B8B8
RGB: 184, 184, 184
CMYK: 0, 0, 0, 28

Uso: Sin información suficiente ○

Gradientes Permitidos
Gradiente Principal

text


De: DATO Orange (#FF6B35)
A:  #FF8C42
Ángulo: 135°

Uso: Fondos de hero, CTAs premium
Gradiente Datos

text


De: Data Blue (#004E89)
A:  #1A659E
Ángulo: 90°

Uso: Gráficos, visualizaciones

4. TIPOGRAFÍA
Tipografía Principal
Inter (Google Fonts - Gratis)
Títulos:
* Inter Black (900)
* Mayúsculas
* Tracking: +2%
Subtítulos:
* Inter Bold (700)
* Sentence case
Cuerpo:
* Inter Regular (400)
* Line height: 1.6
Caption/Etiquetas:
* Inter Medium (500)
* 12-14px

Jerarquía Tipográfica
Web/App:

text


H1: Inter Black, 48px, #0A0A0A
H2: Inter Bold, 32px, #0A0A0A
H3: Inter Bold, 24px, #0A0A0A
H4: Inter Semibold, 20px, #4A4A4A

Body: Inter Regular, 16px, #4A4A4A, line-height: 1.6
Small: Inter Regular, 14px, #4A4A4A
Caption: Inter Medium, 12px, #4A4A4A

Tipografía Alternativa (Sistemas)
Si Inter no disponible:
* System UI
* -apple-system
* Segoe UI
* Roboto
* Sans-serif

Tipografía de Datos
Para números grandes (inflación, dólar, etc.):
JetBrains Mono (monoespaciada)

text


Peso: Bold
Uso: Destacar cifras exactas
Ejemplo: "156.4%"

5. ELEMENTOS GRÁFICOS
Iconografía
Estilo:
* Líneas (outline), no rellenos
* Peso: 2px
* Bordes redondeados (border-radius: 2px)
* Tamaño base: 24x24px
* Color: DATO Black o DATO Orange
Set de iconos:
* Heroicons (gratis, open source)
* O Lucide Icons

Elementos de Dato
Barra de Datos (elemento distintivo)

text


━━━━━━━━━━
Especificaciones:
* Alto: 4px
* Color: DATO Orange
* Uso: Separadores, highlights, gráficos minimalistas
Variantes:

text


━━━━━ (datos completos)
━━━━  (datos parciales)
━━    (pocos datos)

Gráficos y Visualizaciones
Estilo:
* Minimalista
* Colores de la paleta oficial
* Sin efectos 3D
* Sin sombras
* Líneas limpias
* Tipografía: Inter
Tipos permitidos:
* Barras simples
* Líneas de tendencia
* Comparaciones antes/después
* Infografías flat
Librería recomendada: Recharts o Chart.js con tema custom

Fotografía
Criterios:
* NO usar fotos de políticos sonriendo o en actos
* SÍ usar:
    * Gráficos
    * Datos abstractos
    * Edificios institucionales (Congreso, Casa Rosada)
    * Personas comunes (diversidad)
Tratamiento:
* Filtro: +10% contraste
* Overlay: DATO Black al 20% (opcional)
* Siempre incluir crédito

Ilustraciones
Estilo:
* Flat design
* Colores: paleta DATO
* Geométricas, no orgánicas
* Sin gradientes complejos
Uso:
* Estados vacíos
* Onboarding
* Explicaciones de conceptos

6. TONO Y VOZ
Principios de Comunicación
Voz de DATO: (consistente siempre)
1. Directa - Al grano, sin rodeos
2. Clara - Lenguaje simple, sin tecnicismos
3. Precisa - Datos exactos, no estimaciones vagas
4. Neutral - Sin tomar partido político
5. Humana - No robótica, pero profesional

Tono (varía según contexto)
En fact-checking:
* Firme pero no agresivo
* Basado en evidencia
* Sin sarcasmo

text


❌ "El político mintió descaradamente"
✅ "La afirmación no coincide con datos del INDEC"

En explicaciones:
* Educativo
* Empático
* Conversacional

text


❌ "El déficit fiscal primario ascendió al 2.1% del PBI"
✅ "El Estado gastó más de lo que le entró.
    Por cada $100 que recibió, gastó $102."

En redes sociales:
* Ágil
* Actual
* Cercano pero serio

text


❌ "¡Mirá este dato loco! 🤯"
✅ "El dólar subió 8% en una semana.
    Te explicamos por qué: [link]"

En comunicación premium/B2B:
* Profesional
* Detallado
* Orientado a acción

text


"Su dashboard personalizado incluye:
- Alertas en tiempo real
- Histórico de 10 años
- API de integración"

Palabras y Frases Clave
Usar:
* "Según datos de [fuente oficial]"
* "Explicado simple"
* "El dato real"
* "Verificamos"
* "Comparado con"
* "Esto significa que..."
Evitar:
* "Creemos que"
* "Probablemente"
* "Dicen que"
* "Es una locura"
* "Impresionante"
* Tecnicismos sin explicar

Estructura de Contenido
Fact-Check:

text


1. AFIRMACIÓN
   "Frase textual del político"
   - Quién lo dijo
   - Cuándo
   - Contexto

2. VERIFICACIÓN
   ✓ Verdadero / ✗ Falso / ⚠ Engañoso

3. DATOS
   Según [fuente oficial]:
   - Dato 1
   - Dato 2

4. EXPLICACIÓN SIMPLE
   Esto significa que...

5. FUENTES
   [Links oficiales]

Resumen Económico:

text


1. QUÉ PASÓ HOY
   [1-2 oraciones]

2. POR QUÉ IMPORTA
   Explicación simple

3. DATOS CLAVE
   - Inflación: X%
   - Dólar: $X
   - [Indicador relevante]

4. QUÉ SIGNIFICA PARA VOS
   Impacto concreto

7. APLICACIONES DIGITALES
Website
Hero Section:

text


Fondo: Blanco
Logo: DATO (negro)
Título: Inter Black, 64px
CTA: Fondo DATO Orange, texto blanco
Cards de Fact-Check:

text


┌─────────────────────────────┐
│ ✓ VERDADERO                 │ (badge verde)
├─────────────────────────────┤
│ "Frase del político"        │
│                             │
│ Según INDEC: [dato]        │
│ [Mini explicación]          │
│                             │
│ Ver detalle →               │
└─────────────────────────────┘

Borde: 1px #F5F5F5
Border-radius: 8px
Padding: 24px
Hover: sombra suave

App Móvil
Tab Bar:

text


[Inicio] [Verificado] [Economía] [Buscar] [Premium]

Iconos: 24px, DATO Black
Seleccionado: DATO Orange + barra inferior
Notificaciones Push:

text


[Ícono DATO naranja]
Nuevo fact-check

"Frase verificada como FALSA"
Toca para ver los datos →

Redes Sociales
Twitter/X:
Header:
* Fondo: Gradiente DATO (naranja a negro)
* Logo: Blanco
Avatar:
* Logo compacto (D con barra)
* Fondo: DATO Orange
Bio:

text


Política argentina verificada 🔍
Datos reales. Lenguaje simple.
No opiniones. Datos.

📊 Inflación, dólar, fact-checking
🤖 Verificado con IA + datos oficiales

Instagram:
Feed:
* Plantillas consistentes
* Fondo blanco
* Acentos en DATO Orange
* Tipografía Inter
Stories:

text


┌─────────────┐
│   @dato     │
│   ━━━━━━━━━ │
│             │
│ [Contenido] │
│             │
│ Deslizá ↑  │
└─────────────┘

LinkedIn:
Banner:

text


DATO | Inteligencia Política con IA

[Fondo: pattern sutil de datos]
[Logo grande a la izquierda]
Tono: Más profesional, orientado a B2B

Email/Newsletter
Template:

text


┌────────────────────────────┐
│ DATO                       │
│ ━━━━━━━━━━                 │
│                            │
│ Resumen Semanal            │
│ [Fecha]                    │
├────────────────────────────┤
│                            │
│ 📊 ECONOMÍA                │
│ [Resumen + datos]          │
│                            │
│ ✓ VERIFICADO               │
│ [2-3 fact-checks]          │
│                            │
│ 📈 NÚMEROS CLAVE           │
│ Inflación: X%              │
│ Dólar: $X                  │
│                            │
├────────────────────────────┤
│ [CTA: Ver más en la app]   │
│                            │
│ dato.ar                    │
└────────────────────────────┘
Ancho máximo: 600pxTipografía: Inter (web-safe fallback)

Dashboard B2B
Estilo:
* Fondo: #FAFAFA
* Cards: blanco, sombra sutil
* Gráficos: colores DATO
* Sidebar: DATO Black
* Acentos: DATO Orange
Componentes:
* Tablas limpias
* Filtros minimalistas
* Exportar a PDF con branding DATO

8. USOS INCORRECTOS
❌ NO HACER
Logo:

text


❌ DATO (con gradiente arcoíris)
❌ dato (minúsculas)
❌ D A T O (exceso de espaciado)
❌ DATO© (símbolo pegado)
❌ [Logo rotado 45°]
❌ [Logo con sombra 3D]
❌ [Logo distorsionado]

Colores:

text


❌ Texto negro sobre DATO Orange (bajo contraste)
❌ Usar colores fuera de la paleta
❌ Más de 3 colores en un mismo diseño
❌ DATO Orange como fondo principal

Tipografía:

text


❌ Comic Sans
❌ Mezclar más de 2 familias tipográficas
❌ Texto justificado
❌ ALL CAPS en párrafos largos
❌ Line-height < 1.4

Tono:

text


❌ "Los políticos son todos chorros"
❌ "Este dato es una locura jajaja 🤪"
❌ "Creemos que probablemente..."
❌ Lenguaje técnico sin explicar
❌ Opiniones personales

Contenido:

text


❌ Compartir sin verificar fuente
❌ Titular clickbait
❌ Usar fotos sin crédito
❌ Fact-check sin fuente oficial
❌ Comparar sin contexto

9. ASSETS Y RECURSOS
Archivos de Logo
Formatos a exportar:

text


/brand/
├── logo/
│   ├── dato-logo-black.svg
│   ├── dato-logo-black.png (2x, 4x)
│   ├── dato-logo-white.svg
│   ├── dato-logo-white.png (2x, 4x)
│   ├── dato-logo-orange.svg
│   ├── dato-isotipo.svg
│   └── dato-isotipo.png (512x512)
│
├── colors/
│   └── dato-palette.ase (Adobe)
│
├── fonts/
│   ├── Inter-Black.woff2
│   ├── Inter-Bold.woff2
│   ├── Inter-Regular.woff2
│   └── JetBrainsMono-Bold.woff2
│
├── templates/
│   ├── fact-check-card.fig
│   ├── instagram-post.psd
│   ├── twitter-header.png
│   └── email-template.html
│
└── guidelines/
    └── manual-de-marca.pdf

Recursos Gratis Recomendados
Diseño:
* Figma (gratis)
* Canva Pro (templates)
* Excalidraw (diagramas)
Iconos:
* Heroicons
* Lucide Icons
* Phosphor Icons
Imágenes:
* Unsplash
* Pexels
* Pixabay
Tipografía:
* Google Fonts (Inter)
* Adobe Fonts (si tenés CC)

Quick Reference
Elevator Pitch:

text


"DATO verifica política argentina con IA.
Traducimos economía compleja a lenguaje simple
usando datos oficiales.

No opiniones. Datos."

One-liner para cada canal:
Twitter:
Política argentina verificada 🔍 Datos reales, lenguaje simple.
LinkedIn:
Inteligencia política automatizada con IA y datos oficiales
Email:
El resumen que necesitás para entender la economía argentina
App Store:
Fact-checking político + economía explicada simple

Hashtags oficiales:

text


#NoOpinionesDatos
#DatoVerificado
#EconomíaSimple
#FactCheckArgentina

Contacto y Consultas
Para uso del branding:
* ✅ Uso personal/educativo: libre
* ✅ Prensa citando a DATO: libre con crédito
* ❌ Uso comercial sin autorización: prohibido
* ❌ Modificación del logo: prohibido
Consultas: brand@dato.ar

Changelog
v1.0 - Enero 2025
* Manual inicial
* Identidad base
* Paleta de colores
* Guías de uso

ANEXO: CÓDIGO DE MARCA
CSS Variables

CSS


:root {
  /* Colores Primarios */
  --dato-black: #0A0A0A;
  --dato-orange: #FF6B35;

  /* Colores Secundarios */
  --data-blue: #004E89;
  --neutral-gray: #F5F5F5;
  --text-gray: #4A4A4A;

  /* Sistema de Verificación */
  --verified-true: #06D6A0;
  --verified-false: #EF476F;
  --verified-misleading: #FFD166;
  --verified-unknown: #B8B8B8;

  /* Tipografía */
  --font-primary: 'Inter', -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Espaciado */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;

  /* Bordes */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;

  /* Sombras */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}

Componentes React (Tailwind)

React


// Badge de Verificación
<span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
  ✓ VERDADERO
</span>

// Card de Fact-Check
<div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition">
  <div className="flex items-center gap-2 mb-3">
    <span className="px-2 py-1 bg-orange-100 text-orange-600 text-xs font-bold rounded">
      VERIFICADO
    </span>
  </div>
  <p className="text-gray-900 font-semibold mb-2">
    "Frase del político"
  </p>
  <p className="text-gray-600 text-sm">
    Según INDEC: [dato oficial]
  </p>
</div>

// Botón Primary
<button className="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3 rounded-lg transition">
  Ver más datos
</button>

FIN DEL MANUAL DE MARCA v1.0
LOGO DATO - ARCHIVOS SVG
Voy a generarte los SVGs del logo en todas las variantes necesarias.

1. LOGO PRINCIPAL (Horizontal)
dato-logo-principal.svg

svg


<svg width="200" height="80" viewBox="0 0 200 80" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Wordmark DATO -->
  <text x="10" y="45" font-family="Inter, sans-serif" font-weight="900" font-size="36" fill="#0A0A0A" letter-spacing="3">
    DATO
  </text>

  <!-- Barra de datos (4 segmentos de diferentes alturas) -->
  <rect x="10" y="55" width="28" height="4" fill="#FF6B35" rx="2"/>
  <rect x="42" y="52" width="28" height="7" fill="#FF6B35" rx="2"/>
  <rect x="74" y="50" width="28" height="9" fill="#FF6B35" rx="2"/>
  <rect x="106" y="48" width="28" height="11" fill="#FF6B35" rx="2"/>

  <!-- Tagline -->
  <text x="10" y="72" font-family="Inter, sans-serif" font-weight="500" font-size="10" fill="#4A4A4A" letter-spacing="0.5">
    el dato real
  </text>
</svg>

2. LOGO NEGRO (Sin tagline)
dato-logo-black.svg

svg


<svg width="180" height="60" viewBox="0 0 180 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Wordmark DATO -->
  <text x="5" y="40" font-family="Inter, sans-serif" font-weight="900" font-size="36" fill="#0A0A0A" letter-spacing="3">
    DATO
  </text>

  <!-- Barra de datos -->
  <rect x="5" y="48" width="28" height="4" fill="#FF6B35" rx="2"/>
  <rect x="37" y="45" width="28" height="7" fill="#FF6B35" rx="2"/>
  <rect x="69" y="43" width="28" height="9" fill="#FF6B35" rx="2"/>
  <rect x="101" y="41" width="28" height="11" fill="#FF6B35" rx="2"/>
</svg>

3. LOGO BLANCO (Para fondos oscuros)
dato-logo-white.svg

svg


<svg width="180" height="60" viewBox="0 0 180 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Wordmark DATO en blanco -->
  <text x="5" y="40" font-family="Inter, sans-serif" font-weight="900" font-size="36" fill="#FFFFFF" letter-spacing="3">
    DATO
  </text>

  <!-- Barra de datos en naranja -->
  <rect x="5" y="48" width="28" height="4" fill="#FF6B35" rx="2"/>
  <rect x="37" y="45" width="28" height="7" fill="#FF6B35" rx="2"/>
  <rect x="69" y="43" width="28" height="9" fill="#FF6B35" rx="2"/>
  <rect x="101" y="41" width="28" height="11" fill="#FF6B35" rx="2"/>
</svg>

4. LOGO MONOCROMÁTICO (Todo naranja)
dato-logo-orange.svg

svg


<svg width="180" height="60" viewBox="0 0 180 60" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Wordmark DATO en naranja -->
  <text x="5" y="40" font-family="Inter, sans-serif" font-weight="900" font-size="36" fill="#FF6B35" letter-spacing="3">
    DATO
  </text>

  <!-- Barra de datos en naranja -->
  <rect x="5" y="48" width="28" height="4" fill="#FF6B35" rx="2"/>
  <rect x="37" y="45" width="28" height="7" fill="#FF6B35" rx="2"/>
  <rect x="69" y="43" width="28" height="9" fill="#FF6B35" rx="2"/>
  <rect x="101" y="41" width="28" height="11" fill="#FF6B35" rx="2"/>
</svg>

5. ISOTIPO (Logo compacto cuadrado)
dato-isotipo.svg

svg


<svg width="100" height="100" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Fondo opcional (descomentar si se necesita) -->
  <!-- <rect width="100" height="100" fill="#FF6B35" rx="20"/> -->

  <!-- Letra D -->
  <text x="50" y="65" font-family="Inter, sans-serif" font-weight="900" font-size="48" fill="#0A0A0A" text-anchor="middle">
    D
  </text>

  <!-- Mini barra de datos debajo -->
  <rect x="25" y="75" width="12" height="3" fill="#FF6B35" rx="1.5"/>
  <rect x="40" y="73" width="12" height="5" fill="#FF6B35" rx="1.5"/>
  <rect x="55" y="72" width="12" height="6" fill="#FF6B35" rx="1.5"/>
</svg>

6. ISOTIPO CON FONDO (Para app icons)
dato-isotipo-bg.svg

svg


<svg width="512" height="512" viewBox="0 0 512 512" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Fondo degradado -->
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B35;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF8C42;stop-opacity:1" />
    </linearGradient>
  </defs>

  <!-- Fondo con border radius -->
  <rect width="512" height="512" fill="url(#bgGradient)" rx="112"/>

  <!-- Letra D en blanco -->
  <text x="256" y="340" font-family="Inter, sans-serif" font-weight="900" font-size="280" fill="#FFFFFF" text-anchor="middle">
    D
  </text>

  <!-- Barra de datos -->
  <rect x="140" y="380" width="50" height="12" fill="#FFFFFF" rx="6" opacity="0.9"/>
  <rect x="200" y="372" width="50" height="20" fill="#FFFFFF" rx="6" opacity="0.9"/>
  <rect x="260" y="368" width="50" height="24" fill="#FFFFFF" rx="6" opacity="0.9"/>
  <rect x="320" y="364" width="50" height="28" fill="#FFFFFF" rx="6" opacity="0.9"/>
</svg>

7. ISOTIPO CIRCULAR (Para redes sociales)
dato-isotipo-circle.svg

svg


<svg width="400" height="400" viewBox="0 0 400 400" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Fondo circular degradado -->
  <defs>
    <linearGradient id="circleGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B35;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#FF8C42;stop-opacity:1" />
    </linearGradient>
  </defs>

  <circle cx="200" cy="200" r="200" fill="url(#circleGradient)"/>

  <!-- D blanca centrada -->
  <text x="200" y="260" font-family="Inter, sans-serif" font-weight="900" font-size="180" fill="#FFFFFF" text-anchor="middle">
    D
  </text>

  <!-- Mini barra -->
  <rect x="110" y="280" width="35" height="8" fill="#FFFFFF" rx="4" opacity="0.9"/>
  <rect x="150" y="275" width="35" height="13" fill="#FFFFFF" rx="4" opacity="0.9"/>
  <rect x="190" y="272" width="35" height="16" fill="#FFFFFF" rx="4" opacity="0.9"/>
  <rect x="230" y="269" width="35" height="19" fill="#FFFFFF" rx="4" opacity="0.9"/>
</svg>

8. FAVICON (16x16)
dato-favicon.svg

svg


<svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- Fondo naranja -->
  <rect width="32" height="32" fill="#FF6B35" rx="6"/>

  <!-- D blanca simplificada -->
  <text x="16" y="24" font-family="Inter, sans-serif" font-weight="900" font-size="20" fill="#FFFFFF" text-anchor="middle">
    D
  </text>
</svg>

9. LOGO VERTICAL (Para banners)
dato-logo-vertical.svg

svg


<svg width="200" height="160" viewBox="0 0 200 160" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- DATO centrado -->
  <text x="100" y="50" font-family="Inter, sans-serif" font-weight="900" font-size="36" fill="#0A0A0A" text-anchor="middle" letter-spacing="3">
    DATO
  </text>

  <!-- Barra centrada -->
  <rect x="50" y="60" width="25" height="4" fill="#FF6B35" rx="2"/>
  <rect x="80" y="57" width="25" height="7" fill="#FF6B35" rx="2"/>
  <rect x="110" y="55" width="25" height="9" fill="#FF6B35" rx="2"/>

  <!-- Descripción -->
  <text x="100" y="85" font-family="Inter, sans-serif" font-weight="500" font-size="11" fill="#4A4A4A" text-anchor="middle">
    el dato real de
  </text>
  <text x="100" y="100" font-family="Inter, sans-serif" font-weight="600" font-size="13" fill="#0A0A0A" text-anchor="middle">
    Argentina
  </text>
</svg>

10. MARCA DE AGUA (Watermark)
dato-watermark.svg

svg


<svg width="120" height="40" viewBox="0 0 120 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <!-- DATO semi-transparente -->
  <text x="5" y="28" font-family="Inter, sans-serif" font-weight="900" font-size="24" fill="#0A0A0A" opacity="0.15" letter-spacing="2">
    DATO
  </text>

  <!-- Barra semi-transparente -->
  <rect x="5" y="32" width="18" height="3" fill="#FF6B35" rx="1.5" opacity="0.15"/>
  <rect x="26" y="30" width="18" height="5" fill="#FF6B35" rx="1.5" opacity="0.15"/>
  <rect x="47" y="29" width="18" height="6" fill="#FF6B35" rx="1.5" opacity="0.15"/>
