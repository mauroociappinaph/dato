# Turborepo: Orquestación y Caché

Turborepo transforma tus scripts de `package.json` en una pipeline inteligente que entiende las dependencias entre tus paquetes.

## Configuración: turbo.json
Define qué tareas dependen de otras y qué archivos deben recordarse (caché).

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "outputs": ["coverage/**"]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```
*Note: `^build` significa "compila primero mis dependencias antes de compilarme a mí".*

## Comandos Principales
```bash
# Ejecutar build en todo el repo (usa caché donde sea posible)
turbo run build

# Ejecutar tests solo en el paquete 'web'
turbo run test --filter=web

# Ejecutar build en 'web' y todas sus dependencias locales
turbo run build --filter=...web

# Limpiar caché local
turbo run clean
```

## Caché Remoto
Permite compartir la caché de compilación entre desarrolladores y la CI, reduciendo los tiempos de despliegue drásticamente.
1. `npx turbo login`
2. `npx turbo link` (conecta con Vercel o tu propio servidor de caché).
