# SOP-003: Fact-Checking Manual - DATO

> **Última actualización:** 2026-02-19
> **Versión:** 2.0

---

## 3.1 Checklist Pre-Ejecución Obligatorio

Antes de iniciar cualquier verificación, completar:

```
□ Claim identificado y extraído correctamente
□ Speaker identificado (nombre, cargo, partido)
□ Fecha del claim registrada
□ Contexto documentado
□ Categoría asignada (economía, política, social, internacional)
□ No es una opinión subjetiva (si lo es, NO verificar)
□ Fuente primaria identificada
```

---

## 3.2 Fuentes Oficiales Prioritarias

| Prioridad | Fuente | Tipo de Datos | URL |
|-----------|--------|---------------|-----|
| 1 | INDEC | Inflación, pobreza, empleo, PBI | https://www.indec.gob.ar |
| 2 | BCRA | Dólar, reservas, tasas | https://www.bcra.gob.ar |
| 3 | Boletín Oficial | Decretos, leyes, resoluciones | https://www.boletinoficial.gob.ar |
| 4 | Senado/Diputados | Votaciones, proyectos | https://www.senado.gob.ar |
| 5 | Ministerios | Datos sectoriales | Varios |

---

## 3.3 Procedimiento de Verificación

### Paso 1: Identificar el claim
```
├── Extraer afirmación específica
├── Identificar quién lo dijo
├── Fecha y contexto
└── Categoría (economía, política, social, internacional)
```

### Paso 2: Buscar datos oficiales
```
├── Consultar fuente primaria (INDEC, BCRA)
├── Verificar fecha del dato
├── Comparar con el claim
└── Documentar discrepancias
```

### Paso 3: Calcular confidence
```
├── Coincidencia exacta → 95-100%
├── Coincidencia parcial → 70-94%
├── Dato contradictorio → 85-100% (Falso)
└── Sin datos → 0-69%
```

### Paso 4: Asignar veredicto
```
├── VERDADERO: Confidence ≥ 85%, datos coinciden
├── FALSO: Confidence ≥ 85%, datos contradicen
├── PARCIALMENTE_VERDADERO: 70-84% coincidencia
└── SIN_DATOS: Confidence < 70%
```

### Paso 5: Escribir explicación
```
├── Máximo 100 palabras
├── Lenguaje simple (lectura fácil)
├── Citar fuente oficial
└── Link a fuente original
```

---

## 3.4 Flujo de Rollback (Fuente Primaria Falla)

```
INTENTO 1: Fuente primaria (INDEC, BCRA, etc.)
    │
    ├── ÉXITO → Continuar verificación
    │
    └── FALLO → INTENTO 2: Fuente secundaria oficial
                    │
                    ├── ÉXITO → Continuar + marcar "fuente secundaria"
                    │
                    └── FALLO → INTENTO 3: Búsqueda Exa/Google
                                    │
                                    ├── ÉXITO → Marcar "no verificado oficialmente"
                                    │           → Confidence máx: 70%
                                    │
                                    └── FALLO → Veredicto: SIN_DATOS
                                                → Confidence: 0%
```

**Tiempos de retry:**
- Intento 1 → 2: 5 segundos
- Intento 2 → 3: 10 segundos
- Timeout total máximo: 60 segundos

---

## 3.5 Templates de Output Estandarizados

### Formato JSON (para API)

```json
{
  "claim_id": "uuid",
  "verdict": "VERDADERO|FALSO|PARCIALMENTE_VERDADERO|SIN_DATOS",
  "confidence": 0.95,
  "explanation": "Explicación técnica detallada...",
  "simple_explanation": "En palabras simples: el dato es correcto según INDEC.",
  "sources": [
    {
      "name": "INDEC",
      "url": "https://indec.gob.ar/...",
      "data": {"value": 25.7, "unit": "%", "period": "2024-01"}
    }
  ],
  "verified_at": "2026-02-19T10:30:00Z",
  "llm_provider": "groq",
  "llm_model": "llama-3.3-70b"
}
```

### Formato Simple (para usuario final)

```
📌 AFIRMACIÓN: "La inflación fue del 25% en enero"

✅ VEREDICTO: Verdadero

📊 DATOS: Según INDEC, la inflación de enero 2024 fue 25.7%

📚 FUENTE: INDEC - https://indec.gob.ar/inflacion

💡 EXPLICACIÓN: El número mencionado es muy cercano al dato oficial.
```

---

## 3.6 Tabla de Edge Cases

| Situación | Procedimiento | Veredicto Posible |
|-----------|---------------|-------------------|
| Fuentes contradictorias | Usar fuente oficial (INDEC > consultora) | Según fuente oficial |
| Dato desactualizado | Buscar dato más reciente, marcar fecha | PARCIALMENTE_VERDADERO |
| Dato parcial | Explicar qué falta, NO inventar | PARCIALMENTE_VERDADERO o SIN_DATOS |
| Interpretación subjetiva | NO verificar, marcar como "opinión" | N/A (descartar) |
| Claim ambiguo | Solicitar clarificación antes de verificar | N/A (pendiente) |
| Fuente caída | Aplicar flujo de rollback | Según fuente alternativa |
| Dato de consultora | Usar como respaldo, priorizar oficial | Confidence máx 80% |
| Proyección/futuro | Marcar como "proyección", no verificar | N/A (descartar) |
| Claim sobre persona fallecida | Verificar contexto histórico | Normal |
| Claim sobre decreto no publicado | Esperar Boletín Oficial | SIN_DATOS temporal |

---

## 3.7 Quality Assurance Checklist

Antes de publicar, verificar:

```
□ Veredicto asignado correctamente (uno de 4 posibles)
□ Confidence calculado y justificado
□ Fuente citada con link funcional
□ Explicación en lenguaje simple (max 100 palabras)
□ Sin opiniones personales del verificador
□ JSON output válido si es para API
□ Revisado por segundo checker (si controversial)
□ Badge asignado (✅⚠️❌⚪)
```

---

## 3.8 Badges de Verificación

| Badge | Significado | Condición |
|-------|-------------|-----------|
| ✅ | Verdadero | Confidence ≥ 85%, datos coinciden |
| ⚠️ | Parcialmente verdadero | 70-84% coincidencia |
| ❌ | Falso | Confidence ≥ 85%, datos contradicen |
| ⚪ | Sin datos | Confidence < 70% |

---

*Fin del documento*
