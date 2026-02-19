# Tech Stack & Reglas de Ingeniería: THE DUDE S.A.S.

## Core Stack 2026
- **Frontend**: Next.js 15 (App Router) + Tailwind CSS + Framer Motion.
- **Backend**: Node.js (Crypto AES-256-GCM) + Python (Agentes).
- **Inferencia**: Ollama Local (Llama 3.3 / DeepSeek-Coder).
- **Orquestación**: LangGraph + Sequential Thinking.
- **Persistencia**: Supabase (Postgres) + Redis (Context Sync).
- **Memoria**: Pinecone (Namespace: dude-central-brain).

## Reglas de Arquitectura
- **Regla del 300**: Ningún archivo operativo debe superar las 300 líneas.
- **Soberanía de Datos**: Queda terminantemente prohibido el envío de PII a nubes públicas sin scrubbing local previo.
- **Protocolo de Agentes**: Comunicación inter-agente vía bloques JSON compactos.
- **Modularidad**: Uso obligatorio de Barrel Files y separación estricta entre Lógica de Agente y UI.

## Calidad & Blindaje
- **Evaluación Obligatoria**: Todo código debe pasar por el `AGENTE_EVALUACION` antes de ser validado por el Dueño.
- **Zero-Trust**: Validación de contratos de API en el Edge.
- **Inmunización**: Documentar RCA en la memoria central tras cada fix.

---
*Estándar de Ingeniería - The Dude S.A.S.*