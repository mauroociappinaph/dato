# Manual de Marca - DATO

> Política argentina verificada con datos reales

---

## 1. Identidad de Marca

### Posicionamiento

**DATO** es la plataforma de inteligencia política y económica que traduce la complejidad de Argentina a datos verificables y lenguaje simple.

### Promesa de Marca

> "No opiniones. Datos."

### Misión

Democratizar el acceso a información política y económica confiable en Argentina mediante IA y datos oficiales.

### Visión

Ser la fuente de verdad más confiable para entender la economía y política argentina.

### Valores

1. **Verificable** - Todo se respalda con datos oficiales
2. **Simple** - Complejidad traducida a lenguaje cotidiano
3. **Neutral** - Sin sesgo político
4. **Transparente** - Mostramos las fuentes siempre
5. **Automático** - Tecnología al servicio de la verdad

### Personalidad de Marca

Si DATO fuera una persona:

- 🧠 Inteligente pero no pedante
- 📊 Analítica pero accesible
- 🎯 Directa sin ser agresiva
- 🤝 Confiable como un amigo que sabe
- ⚡ Ágil y al día
- 🔍 Curiosa pero rigurosa

**NO es:**
- ❌ Político
- ❌ Sensacionalista
- ❌ Complicado
- ❌ Elitista
- ❌ Aburrido

---

## 2. Logo y Variantes

### Logo Principal

```
┌─────────────────────────┐
│                         │
│    D  A  T  O          │
│    ━━━━━━━━━━          │
│                         │
└─────────────────────────┘
```

**Construcción:**
- Wordmark: DATO
- Tipografía: Inter Black (tracking: +50)
- Elemento distintivo: Línea de datos (4 segmentos como barras de gráfico)

### Variantes

| Variante | Uso |
|----------|-----|
| Horizontal | Landing, web, documentos |
| Compacto (Isotipo) | App móvil, favicon, redes |
| Vertical | Stories, banners |
| Negativo | Fondo oscuro |

### Área de Protección

Espacio mínimo alrededor del logo = altura de la "D"

**Nunca:**
- Comprimir o estirar
- Rotar
- Añadir sombras o efectos
- Cambiar colores fuera de paleta
- Usar tamaño menor a 24px de altura

---

## 3. Paleta de Colores

### Colores Primarios

| Color | HEX | RGB | Uso |
|-------|-----|-----|-----|
| **DATO Black** | `#0A0A0A` | 10, 10, 10 | Logo, títulos, texto principal |
| **DATO Orange** | `#FF6B35` | 255, 107, 53 | Highlights, CTAs, datos verificados |

### Colores Secundarios

| Color | HEX | RGB | Uso |
|-------|-----|-----|-----|
| **Data Blue** | `#004E89` | 0, 78, 137 | Links, gráficos, información |
| **Neutral Gray** | `#F5F5F5` | 245, 245, 245 | Fondos, separadores |
| **Text Gray** | `#4A4A4A` | 74, 74, 74 | Texto secundario |

### Sistema de Verificación

| Estado | Color | HEX |
|--------|-------|-----|
| ✅ Verdadero | Verde | `#06D6A0` |
| ❌ Falso | Rojo | `#EF476F` |
| ⚠️ Parcialmente verdadero | Amarillo | `#FFD166` |
| ⚪ Sin datos | Gris | `#B8B8B8` |

### Gradientes

**Principal:**
```
De: #FF6B35 → A: #FF8C42 (135°)
Uso: Fondos hero, CTAs premium
```

**Datos:**
```
De: #004E89 → A: #1A659E (90°)
Uso: Gráficos, visualizaciones
```

---

## 4. Tipografía

### Familia Principal

**Inter** (Google Fonts - Gratis)

| Uso | Peso | Estilo |
|-----|------|--------|
| Títulos | Black (900) | Mayúsculas, tracking +2% |
| Subtítulos | Bold (700) | Sentence case |
| Cuerpo | Regular (400) | Line height 1.6 |
| Captions | Medium (500) | 12-14px |

### Jerarquía

```css
H1: Inter Black, 48px, #0A0A0A
H2: Inter Bold, 32px, #0A0A0A
H3: Inter Bold, 24px, #0A0A0A
H4: Inter Semibold, 20px, #4A4A4A

Body: Inter Regular, 16px, #4A4A4A
Small: Inter Regular, 14px, #4A4A4A
Caption: Inter Medium, 12px, #4A4A4A
```

### Tipografía de Datos

**JetBrains Mono** (monoespaciada)

Para números grandes (inflación, dólar):
```
156.4%
```

---

## 5. Tono y Voz

### Principios de Comunicación

1. **Directa** - Al grano, sin rodeos
2. **Clara** - Lenguaje simple, sin tecnicismos
3. **Precisa** - Datos exactos, no estimaciones vagas
4. **Neutral** - Sin tomar partido político
5. **Humana** - No robótica, pero profesional

### Ejemplos de Tono

**En fact-checking:**

❌ "El político mintió descaradamente"
✅ "La afirmación no coincide con datos del INDEC"

**En explicaciones:**

❌ "El déficit fiscal primario ascendió al 2.1% del PBI"
✅ "El Estado gastó más de lo que le entró. Por cada $100 que recibió, gastó $102."

**En redes sociales:**

❌ "¡Mirá este dato loco! 🤯"
✅ "El dólar subió 8% en una semana. Te explicamos por qué: [link]"

### Palabras Clave

**Usar:**
- "Según datos de [fuente oficial]"
- "Explicado simple"
- "El dato real"
- "Verificamos"
- "Esto significa que..."

**Evitar:**
- "Creemos que"
- "Probablemente"
- "Dicen que"
- Tecnicismos sin explicar

---

## 6. CSS Variables

```css
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

  /* Bordes */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
}
```

---

## 7. Componentes UI

### Badge de Verificación

```jsx
<span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
  ✓ VERDADERO
</span>
```

### Card de Fact-Check

```jsx
<div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition">
  <span className="px-2 py-1 bg-orange-100 text-orange-600 text-xs font-bold rounded">
    VERIFICADO
  </span>
  <p className="text-gray-900 font-semibold mb-2">
    "Frase del político"
  </p>
  <p className="text-gray-600 text-sm">
    Según INDEC: [dato oficial]
  </p>
</div>
```

### Botón Primary

```jsx
<button className="bg-orange-500 hover:bg-orange-600 text-white font-semibold px-6 py-3 rounded-lg transition">
  Ver más datos
</button>
```

---

## 8. Usos Incorrectos

### Logo

❌ DATO (con gradiente arcoíris)
❌ dato (minúsculas)
❌ D A T O (exceso de espaciado)
❌ Logo rotado
❌ Logo con sombra 3D
❌ Logo distorsionado

### Colores

❌ Texto negro sobre DATO Orange
❌ Colores fuera de paleta
❌ Más de 3 colores en un diseño
❌ DATO Orange como fondo principal

### Contenido

❌ "Los políticos son todos chorros"
❌ "Este dato es una locura jajaja"
❌ "Creemos que probablemente..."
❌ Tecnicismos sin explicar
❌ Opiniones personales

---

## 9. Elevator Pitch

> "DATO verifica política argentina con IA. Traducimos economía compleja a lenguaje simple usando datos oficiales. No opiniones. Datos."

### One-liners por Canal

| Canal | Mensaje |
|-------|---------|
| Twitter | Política argentina verificada 🔍 Datos reales, lenguaje simple. |
| LinkedIn | Inteligencia política automatizada con IA y datos oficiales |
| Email | El resumen que necesitás para entender la economía argentina |
| App Store | Fact-checking político + economía explicada simple |

### Hashtags Oficiales

- #NoOpinionesDatos
- #DatoVerificado
- #EconomíaSimple
- #FactCheckArgentina

---

## 10. Contacto

Para consultas de branding: **brand@dato.ar**

**Uso permitido:**
- ✅ Personal/educativo: libre
- ✅ Prensa con crédito: libre

**Uso prohibido:**
- ❌ Comercial sin autorización
- ❌ Modificación del logo
