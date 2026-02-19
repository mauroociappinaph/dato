# SOP-001: Desarrollo - DATO

> **⚠️ IMPORTANTE:** Todas las operaciones con GitHub deben realizarse mediante **GitHub MCP (Kilo CLI)**, no con comandos git directos ni interfaz web.
>
> Ejemplos:
> - Crear issue → `kilo run "Crea issue en GitHub con título 'Bug fix'"`
> - Crear PR → `kilo run "Crear pull request desde feature/rama a main"`
> - Crear repositorio → `kilo run "Crear repositorio dato en GitHub"`

## SOP-001: Desarrollo

### 1.1 Git Workflow

#### Branch Naming Convention

```
<tipo>/<ticket-id>-<descripcion-corta>

Tipos:
- feature/  → Nueva funcionalidad
- fix/      → Bug fix
- docs/     → Documentación
- refactor/ → Refactorización
- test/     → Tests
- chore/    → Mantenimiento

Ejemplos:
- feature/US-001-feed-noticias
- fix/claim-extractor-timeout
- docs/api-endpoints
```

#### Flujo de Trabajo

```
1. Crear branch desde main
   git checkout main
   git pull origin main
   git checkout -b feature/US-001-feed-noticias

2. Desarrollar con commits atómicos
   git add .
   git commit -m "feat(feed): add daily news card component"

3. Push y crear Pull Request
   git push origin feature/US-001-feed-noticias
   gh pr create --title "US-001: Feed de noticias" --body "..."

4. Code Review (mínimo 1 aprobación)
   - Revisar código
   - Ejecutar tests
   - Aprobar o solicitar cambios

5. Merge a main
   git checkout main
   git merge --squash feature/US-001-feed-noticias
   git push origin main
```

### 1.2 Commit Message Format

```
<tipo>(<scope>): <descripción>

[optional body]

[optional footer]

Tipos:
- feat:     Nueva funcionalidad
- fix:      Bug fix
- docs:     Documentación
- style:    Formato (no afecta lógica)
- refactor: Refactorización
- test:     Tests
- chore:    Mantenimiento

Ejemplos:
- feat(agents): add Agent 1 data collector cron job
- fix(fact-check): handle missing INDEC data gracefully
- docs(api): document new /api/v1/search endpoint
```

### 1.3 Code Review Checklist

#### Antes de Solicitar Review

- [ ] Código compila sin errores
- [ ] Tests pasan (`npm test` o `pytest`)
- [ ] Lint pasa (`npm run lint`)
- [ ] Typecheck pasa (`npm run typecheck`)
- [ ] Sin secrets en código
- [ ] Documentación actualizada
- [ ] PR tiene descripción clara

#### Durante Review

- [ ] Lógica correcta
- [ ] Manejo de errores adecuado
- [ ] Performance aceptable
- [ ] Seguridad (no exponer datos)
- [ ] Código legible
- [ ] Sin código duplicado
- [ ] Tests cubren casos edge

### 1.4 Testing Requirements

```
Estructura de tests:
tests/
├── unit/           # Tests unitarios
│   ├── agents/     # Tests por agente
│   └── utils/      # Tests de utilidades
├── integration/    # Tests de integración
└── e2e/           # Tests end-to-end

Cobertura mínima: 80%

Ejecutar:
npm test                    # Todos los tests
npm run test:unit          # Solo unitarios
npm run test:integration   # Solo integración
npm run test:e2e           # Solo E2E
npm run test:coverage      # Con coverage
```

### 1.5 Comandos de Desarrollo

```bash
# Instalación
pnpm install

# Desarrollo
pnpm dev              # Frontend + Backend
pnpm dev:web          # Solo frontend
pnpm dev:api          # Solo backend

# Calidad
pnpm lint             # ESLint
pnpm typecheck        # TypeScript
pnpm test             # Jest/Vitest
pnpm format           # Prettier

# Build
pnpm build            # Producción
pnpm build:web        # Solo frontend
pnpm build:api        # Solo backend

# Database
pnpm db:migrate       # Ejecutar migraciones
pnpm db:seed          # Datos de prueba
pnpm db:reset         # Reset completo
```

---


---

## 1.6 Code Standards (SRP, DRY, The 300 Rule)

### The 300 Rule (Obligatorio)

> **Ningún archivo debe exceder 300 líneas de código efectivo (LOC).**

**Razón:**
- Reduce consumo de tokens en reads secuenciales
- Facilita code review
- Mejora mantenibilidad

**Procedimiento cuando archivo > 300 líneas:**
1. Identificar "costuras" (seams) naturales
2. Extraer sub-componentes o hooks
3. Mover tipos a `packages/types/`
4. Crear barrel file (`index.ts`)

### SRP (Single Responsibility Principle)

**En Frontend:**
- Un componente = Una responsabilidad visual
- Un hook = Una responsabilidad de lógica
- Extraer lógica compleja a custom hooks

**En Backend:**
- Un service = Un dominio
- Un controller = Un recurso
- Un module = Una feature

**Ejemplo de violación SRP:**
```typescript
// ❌ BAD: Componente con múltiples responsabilidades
function UserProfile() {
  // Lógica de fetching
  const [user, setUser] = useState(null);
  useEffect(() => { fetchUser() }, []);
  
  // Lógica de forma
  const [form, setForm] = useState({});
  
  // Lógica de validación
  const validate = () => { ... };
  
  // Render de 3 UIs diferentes
  return (
    <div>
      {/* Profile Card */}
      {/* Edit Form */}
      {/* Stats Dashboard */}
    </div>
  );
}
```

**Refactor SRP:**
```typescript
// ✅ GOOD: Responsabilidades separadas
// packages/ui/src/UserProfile/UserProfile.tsx
function UserProfile() {
  const { user } = useUserProfile(); // Hook extraído
  return <ProfileCard user={user} />;
}

// packages/ui/src/UserProfile/useUserProfile.ts
function useUserProfile() {
  const [user, setUser] = useState(null);
  useEffect(() => { fetchUser() }, []);
  return { user };
}

// packages/ui/src/UserProfile/ProfileCard.tsx
function ProfileCard({ user }) {
  return <div>{user.name}</div>;
}

// packages/ui/src/UserProfile/index.ts (Barrel file)
export { UserProfile } from './UserProfile';
export { useUserProfile } from './useUserProfile';
```

### DRY (Don't Repeat Yourself)

**Identificar duplicación:**
- Código idéntico en 2+ lugares
- Lógica similar con pequeños cambios
- Componentes con estructura repetida

**Soluciones:**
1. **Extraer a helper:** Funciones puras a `packages/types/src/utils/`
2. **Crear componente base:** UI compartida a `packages/ui/`
3. **Usar composition:** Hooks reutilizables

**Ejemplo:**
```typescript
// ❌ BAD: Duplicación
function UserCard() {
  const formatDate = (d) => new Date(d).toLocaleDateString('es-AR');
  return <span>{formatDate(user.createdAt)}</span>;
}

function ClaimCard() {
  const formatDate = (d) => new Date(d).toLocaleDateString('es-AR');
  return <span>{formatDate(claim.dateSaid)}</span>;
}

// ✅ GOOD: Helper extraído
// packages/types/src/utils/format.ts
export const formatDate = (d: Date | string) => 
  new Date(d).toLocaleDateString('es-AR');

// Uso
import { formatDate } from '@dato/types';
```

### Barrel Files (index.ts)

**Obligatorio en:**
- `packages/ui/src/` - Exportar todos los componentes
- `packages/types/src/` - Exportar todos los tipos
- `packages/agents/src/` - Exportar todos los agentes

**Estructura:**
```
packages/ui/
├── src/
│   ├── FeedCard/
│   │   ├── FeedCard.tsx
│   │   ├── FeedCard.types.ts
│   │   └── index.ts          # Barrel local
│   ├── VerificationBadge/
│   └── index.ts              # Barrel global
└── package.json
```

**Contenido del barrel:**
```typescript
// packages/ui/src/index.ts
export { FeedCard } from './FeedCard';
export { VerificationBadge } from './VerificationBadge';
export type { FeedCardProps } from './FeedCard';
```

**Beneficio:**
```typescript
// ❌ Sin barrel
import { FeedCard } from '@dato/ui/src/FeedCard/FeedCard';

// ✅ Con barrel
import { FeedCard } from '@dato/ui';
```

---

## 1.7 State Management (Zustand)

### Estructura de Stores

```
apps/web/src/stores/
├── authStore.ts         # Estado de autenticación
├── feedStore.ts         # Estado del feed
├── searchStore.ts       # Estado de búsqueda
├── uiStore.ts           # Estado de UI (modals, theme)
└── index.ts             # Barrel file
```

### Patrón de Store

```typescript
// apps/web/src/stores/authStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  
  // Actions
  setUser: (user: User | null) => void;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      isAuthenticated: false,
      isLoading: false,
      
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      
      login: async (email, password) => {
        set({ isLoading: true });
        try {
          const user = await authService.login(email, password);
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error) {
          set({ isLoading: false });
          throw error;
        }
      },
      
      logout: () => {
        authService.logout();
        set({ user: null, isAuthenticated: false });
      },
    }),
    { name: 'auth-storage' }
  )
);
```

### Uso en Componentes

```typescript
// apps/web/src/components/Header.tsx
import { useAuthStore } from '@dato/stores';

function Header() {
  const { user, isAuthenticated, logout } = useAuthStore();
  
  // Solo suscribirse a lo necesario (evita re-renders innecesarios)
  const userName = useAuthStore((state) => state.user?.name);
  
  return (
    <header>
      {isAuthenticated ? (
        <button onClick={logout}>Logout {userName}</button>
      ) : (
        <Link href="/login">Login</Link>
      )}
    </header>
  );
}
```

### Reglas de Zustand

| Regla | Descripción |
|-------|-------------|
| Un store = Un dominio | No mezclar auth con feed |
| Actions inline | No crear actions separadas |
| Selectores específicos | `useStore((s) => s.x)` para evitar re-renders |
| Persist con cuidado | Solo datos serializables |

---

## 1.8 Git Conventions

### Conventional Commits (con Husky)

**Formato:**
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Tipos:**
| Tipo | Uso | Ejemplo |
|------|-----|---------|
| `feat` | Nueva funcionalidad | `feat(feed): add daily summary card` |
| `fix` | Bug fix | `fix(auth): handle expired tokens` |
| `docs` | Documentación | `docs(api): update endpoint docs` |
| `style` | Formato (no afecta lógica) | `style: format imports` |
| `refactor` | Refactorización | `refactor(agents): extract claim parser` |
| `test` | Tests | `test(feed): add unit tests` |
| `chore` | Mantenimiento | `chore: update dependencies` |

### Atomic Commits

**Regla:** Un commit = Un cambio lógico

```bash
# ❌ BAD: Múltiples cambios en un commit
git add .
git commit -m "Add feature, fix bug, update docs"

# ✅ GOOD: Commits atómicos
git add packages/agents/src/agent-1-collector/
git commit -m "feat(collector): add INDEC scraping"
git add apps/web/src/components/FeedCard/
git commit -m "feat(ui): add FeedCard component"
git add docs/
git commit -m "docs: update architecture diagram"
```

### Force with Lease (Obligatorio)

```bash
# ❌ NUNCA
git push --force

# ✅ SIEMPRE
git push --force-with-lease
```

### Pre-PR Checklist

Antes de crear PR:
- [ ] Todos los commits siguen conventional commits
- [ ] Squash de commits "typo" o "wip"
- [ ] `pnpm lint` pasa sin errores
- [ ] `pnpm typecheck` pasa sin errores
- [ ] `pnpm test` pasa
- [ ] No archivos > 300 líneas
