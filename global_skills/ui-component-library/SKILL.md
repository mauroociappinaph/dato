---
name: ui-component-library
description: Reusable UI component architecture, design tokens, and Storybook integration. 2026 Edition.
inherited_from: [gemini-skill-creator, code-modularity-architect, brand-identity]
---

# UI Component Library (Compressed)

## Purpose
Build and maintain a scalable, accessible, and consistent UI component library.

## Core Capabilities
- **Component Architecture**: Atomic design, compound components, composition patterns
- **Design Tokens**: Colors, typography, spacing, shadows via CSS variables
- **Accessibility**: ARIA patterns, keyboard navigation, screen reader support
- **Storybook Integration**: Documentation, visual testing, interaction testing
- **Theming**: Dark mode, custom themes, CSS-in-JS patterns

## Component Standards
- **Props API**: Consistent naming, TypeScript interfaces
- **Composition**: Children-first, render props, slots pattern
- **States**: Loading, error, disabled, focus, hover
- **Variants**: Size, intent, variant props

## File Structure
```
components/
├── Button/
│   ├── Button.tsx
│   ├── Button.styles.ts
│   ├── Button.types.ts
│   ├── Button.stories.tsx
│   └── index.ts
```

## Technologies
- React/Next.js
- Tailwind CSS / CSS Modules
- Storybook
- Chromatic (visual testing)

## Related Skills
- `design-system/`: Design tokens source
- `brand-identity/`: Visual standards
- `typescript-pro/`: Type definitions
