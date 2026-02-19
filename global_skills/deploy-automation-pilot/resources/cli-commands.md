# Comandos de Despliegue Rápido

## Vercel (Frontend/Fullstack)
- `vercel login`: Inicio de sesión (si es necesario).
- `vercel link`: Vincular carpeta local con proyecto en la nube.
- `vercel env pull .env.local`: Traer variables del dashboard a local.
- `vercel deploy --prod`: Despliegue directo a producción.

## Railway (Backend/Infra)
- `railway login`: Inicio de sesión.
- `railway link`: Vincular con proyecto de Railway.
- `railway run <command>`: Ejecutar comando con variables de entorno del cloud.
- `railway up`: Subir el servicio actual.
- `railway variables get`: Listar variables activas.

## Protocolo de Error
1. Leer `vercel logs` o `railway logs`.
2. Identificar si el error es de:
   - **Environment**: ¿Falta una API Key? (Llamar a `secrets-vault-orchestrator`).
   - **Build**: ¿Error de TS/Lint? (Llamar a `code-reviewer`).
   - **Runtime**: ¿Error de base de datos? (Llamar a `database-performance-tuner`).
