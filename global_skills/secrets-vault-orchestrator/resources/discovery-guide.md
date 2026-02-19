# Guía de Descubrimiento de Secretos (Secrets Discovery)

Este recurso permite al agente guiar al usuario en la obtención de API Keys críticas para los servicios más comunes.

## 1. Stripe (Pagos)
- **STRIPE_SECRET_KEY**:
  - Dashboard: [https://dashboard.stripe.com/apikeys](https://dashboard.stripe.com/apikeys)
  - Paso: Ir a Developers -> API Keys -> Revelar "Secret key".
- **STRIPE_WEBHOOK_SECRET**:
  - Dashboard: [https://dashboard.stripe.com/webhooks](https://dashboard.stripe.com/webhooks)
  - Paso: Seleccionar el endpoint -> Revelar "Signing secret" (comienza con `whsec_`).

## 2. Daily.co (Video/Llamadas)
- **DAILY_API_KEY**:
  - Dashboard: [https://dashboard.daily.co/developers](https://dashboard.daily.co/developers)
  - Paso: Copiar la clave API del equipo.
- **DAILY_DOMAIN**:
  - El subdominio de tu cuenta (ej. `tu-empresa.daily.co`).
- **DAILY_WEBHOOK_SECRET**:
  - Se genera al crear un webhook vía API o Dashboard. Es el valor `hmac`.

## 3. Clerk (Autenticación)
- **CLERK_SECRET_KEY**:
  - Dashboard: [https://dashboard.clerk.com/](https://dashboard.clerk.com/)
  - Paso: API Keys -> Copiar "Secret Key".

## Protocolo de Inyección
Una vez que el usuario proporcione estos valores:
1. Validar formato (ej. Stripe keys empiezan con `sk_`).
2. Llamar a la herramienta de inyección del **Secrets Vault Orchestrator**.
3. Confirmar al usuario que los secretos están a salvo en la bóveda y en el `.env` local (ignorado).
