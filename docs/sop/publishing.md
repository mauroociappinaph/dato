# SOP-007: Publicación - DATO

## SOP-007: Publicación

### 7.1 Canales de Distribución

| Canal | Formato | Frecuencia | Audiencia |
|-------|---------|------------|-----------|
| Web App | Card completo | Tiempo real | Todos |
| Twitter/X | 280 chars | 3-5/día | General |
| Newsletter | Email HTML | Diario 9 AM | Premium |
| Telegram | Mensaje 500 chars | Tiempo real | Suscriptores |

### 7.2 Flujo de Aprobación

```
Contenido generado
│
├── Verificación automática
│   ├── Confidence ≥ 85%
│   ├── Fuente citada
│   └── Sin PII
│
├── Si automático OK → Publicar
│
└── Si flag → Revisión manual
    ├── Checker 1 revisa
    ├── Si controversial → Checker 2 revisa
    └── Aprobar/Rechazar
```

### 7.3 Formato por Canal

#### Twitter/X

```
[Título del dato]

📊 El dato: [claim verificado]
✅ Veredicto: [VERDADERO/FALSO/PARCIAL]

📖 Explicación: [1-2 oraciones]

🔗 dato.ar/claim/[id]

#DatoVerificado #Argentina
```

#### Newsletter

```html
<h2>[Título]</h2>

<p><strong>El político dijo:</strong> "[claim]"</p>

<p><strong>Veredicto:</strong> ✅ VERDADERO</p>

<p><strong>Explicación:</strong> [texto simple]</p>

<p><strong>Fuente:</strong> <a href="[url]">INDEC</a></p>

<a href="https://dato.ar/claim/[id]">Ver detalle completo →</a>
```

#### Telegram

```
📌 [Título]

❌ El político mintió: "[claim]"

📊 Dato real: [dato oficial]

🔗 dato.ar/claim/[id]
```

### 7.4 Scheduling

```yaml
# Configuración de publicación

twitter:
  schedule:
    - "09:00"  # Mañana
    - "12:00"  # Mediodía
    - "18:00"  # Tarde
  max_per_day: 5

newsletter:
  schedule: "09:00"
  timezone: "America/Argentina/Buenos_Aires"

telegram:
  mode: realtime  # Inmediato
```

### 7.5 Engagement Tracking

| Métrica | Herramienta | Frecuencia |
|---------|-------------|------------|
| Impressions | Twitter Analytics | Diario |
| Clicks | Link shortener | Tiempo real |
| Opens | Email provider | Diario |
| Engagements | PostHog | Tiempo real |

---

