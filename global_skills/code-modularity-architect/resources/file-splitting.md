# Estrategias de División de Archivos (File Splitting)

Este recurso define cómo atacar archivos que violan la Regla del 300 y cómo organizar el resultado.

## 1. Identificación de Costuras (Seams)
Busca "grietas" naturales en el código donde se puede separar la lógica:
- **Agrupación de Métodos**: ¿Hay un grupo de métodos que solo manipulan un subconjunto de propiedades? -> **Nueva Clase/Hook**.
- **Bloques de Renderizado**: En componentes UI, ¿hay un `renderModal()` o `renderList()` gigante? -> **Nuevo Componente**.

## 2. Organización de Tipos (Type Segregation)
Al dividir un archivo, lo primero que suele estorbar son las definiciones de tipos.
- **Regla**: Si una interfaz se usa en más de un archivo o tiene más de 5 propiedades, muévela.
- **Destino**: `src/types/{ModuleName}.types.ts` o `src/types/index.d.ts`.
- **Beneficio**: Permite importar interfaces sin crear dependencias circulares con la lógica del componente.

## 3. El Patrón "Barrel File" (index.ts)
Evita importaciones profundas y desordenadas (`import X from '../../components/User/UserList'`).
- **Implementación**: Crea un archivo `index.ts` en cada directorio que contenga componentes o lógica.
- **Ejemplo**:
  ```typescript
  // src/components/UserProfile/index.ts
  export * from './UserProfile';
  export * from './useUserData';
  // NO exportar sub-componentes internos si no se usan fuera
  ```
- **Resultado**: Importaciones limpias -> `import { UserProfile } from '@/components/UserProfile';`

## 4. El Patrón "Colocation" con Estructura
Al extraer, mantén lo relacionado cerca, pero organizado.
- **Antes**:
  `src/components/UserProfile.tsx` (500 líneas con interfaces y estilos)
- **Después**:
  ```text
  src/components/UserProfile/
  ├── index.ts              # Barrel file (Public API)
  ├── UserProfile.tsx       # Componente Principal (Limpio)
  ├── UserProfile.types.ts  # O mover a src/types/ si es global
  ├── UserStats.tsx         # Sub-componente extraído
  ├── useUserData.ts        # Hook de lógica de negocio
  └── styles.ts             # Estilos aislados
  ```

## 5. Extracción de Lógica de Negocio (Business Logic)
El código de UI no debe saber *cómo* se calcula un impuesto o se valida un email.
- Extrae la lógica pura a funciones fuera del componente.
- Si la lógica requiere estado, extráela a un **Custom Hook** (en React) o un **Service** (en Angular/NestJS).

## 6. Verificación Post-División
- Asegúrate de que las importaciones se actualicen correctamente apuntando a los nuevos `types/` o `index.ts`.
- Verifica que no haya dependencias circulares creadas por la división.