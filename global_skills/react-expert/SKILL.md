---
name: react-expert
description: Advanced React/Next.js patterns, performance optimization, and best practices. 2026 Edition.
inherited_from: [gemini-skill-creator, typescript-pro]
---

# React Expert (Compressed)

## Purpose
Master React ecosystem with focus on performance, accessibility, and modern patterns.

## Core Capabilities
- **Next.js 14+**: App Router, Server Components, Server Actions
- **State Management**: Zustand, Jotai, React Query, SWR
- **Performance**: Lazy loading, code splitting, Suspense, streaming
- **Patterns**: Custom hooks, compound components, render props
- **Testing**: Vitest, Testing Library, Playwright E2E

## 2026 Best Practices
- Server Components by default
- Client Components only when needed (`'use client'`)
- Parallel routes for loading states
- Intercepting routes for modals
- Partial prerendering (PPR)

## Performance Checklist
- [ ] Bundle size < 200KB initial
- [ ] Lighthouse score > 90
- [ ] Core Web Vitals pass
- [ ] Image optimization (next/image)
- [ ] Font optimization (next/font)

## Key Patterns
```tsx
// Server Component (default)
export default async function Page() {
  const data = await fetch(); // Server-side
  return <Component data={data} />;
}

// Client Component
'use client';
export function InteractiveComponent() {
  const [state, setState] = useState();
  return <div onClick={() => setState()} />;
}
```

## Related Skills
- `typescript-pro/`: Type safety
- `ui-component-library/`: Component patterns
- `seo-technical-master/`: Meta tags, sitemaps
