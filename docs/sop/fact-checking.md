# SOP-003: Fact-Checking Manual - DATO

## SOP-003: Fact-Checking Manual

### 3.1 Fuentes Oficiales Prioritarias

| Prioridad | Fuente | Tipo de Datos |
|-----------|--------|---------------|
| 1 | INDEC | Inflación, pobreza, empleo, PBI |
| 2 | BCRA | Dólar, reservas, tasas |
| 3 | Boletín Oficial | Decretos, leyes, resoluciones |
| 4 | Senado/Diputados | Votaciones, proyectos |
| 5 | Ministerios | Datos sectoriales |

### 3.2 Procedimiento de Verificación

```
Paso 1: Identificar el claim
├── Extraer afirmación específica
├── Identificar quién lo dijo
├── Fecha y contexto
└── Categoría (economía, política, social)

Paso 2: Buscar datos oficiales
├── Consultar fuente primaria (INDEC, BCRA)
├── Verificar fecha del dato
├── Comparar con el claim
└── Documentar discrepancias

Paso 3: Calcular confidence
├── Coincidencia exacta → 95-100%
├── Coincidencia parcial → 70-94%
├── Dato contradictorio → 85-100% (Falso)
└── Sin datos → 0-69%

Paso 4: Asignar veredicto
├── VERDADERO: Confidence ≥ 85%, datos coinciden
├── FALSO: Confidence ≥ 85%, datos contradicen
├── PARCIALMENTE_VERDADERO: 70-84% coincidencia
└── SIN_DATOS: Confidence < 70%

Paso 5: Escribir explicación
├── Máximo 100 palabras
├── Lenguaje simple
├── Citar fuente oficial
└── Link a fuente original
```

### 3.3 Edge Cases

| Situación | Procedimiento |
|-----------|---------------|
| Fuentes contradictorias | Usar fuente oficial (INDEC > consultora) |
| Dato desactualizado | Buscar dato más reciente, marcar fecha |
| Dato parcial | Explicar qué falta, no inventar |
| Interpretación subjetiva | No verificar, marcar como "opinión" |

### 3.4 Quality Assurance

```
Antes de publicar:
□ Veredicto asignado correctamente
□ Confidence calculado
□ Fuente citada con link
□ Explicación en lenguaje simple
□ Sin opiniones personales
□ Revisado por segundo checker (si controversial)
```

---

