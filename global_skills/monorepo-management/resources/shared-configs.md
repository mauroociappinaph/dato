# Configuraciones Compartidas

La estandarización es la clave para que un monorepo no se convierta en "muchos repositorios en una misma carpeta".

## 1. TypeScript Compartido
Crea un paquete `packages/tsconfig` que exporte configuraciones base.

```json
// packages/tsconfig/base.json
{
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "module": "ESNext",
    "moduleResolution": "bundler"
  }
}

// apps/web/tsconfig.json
{
  "extends": "@repo/tsconfig/base.json",
  "compilerOptions": {
    "outDir": "dist"
  }
}
```

## 2. ESLint & Prettier
Centraliza las reglas en `packages/config` o `.eslintrc.js` en la raíz que los paquetes hijos extiendan. Esto garantiza que el estilo de código sea idéntico en el Backend, Frontend y Paquetes de UI.

## 3. Tipos Compartidos (Single Source of Truth)
Capa fundamental para la seguridad:
```typescript
// packages/types/src/index.ts
export interface User {
  id: string;
  email: string;
}

// Importado tanto en apps/backend como en apps/frontend
import { User } from '@repo/types';
```
Esto evita errores donde el backend cambia un campo y el frontend se rompe en producción sin avisar en tiempo de compilación.
