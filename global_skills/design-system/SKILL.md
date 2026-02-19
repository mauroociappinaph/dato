---
name: design-system
description: Comprehensive design system with tokens, components, and documentation. 2026 Edition.
inherited_from: [gemini-skill-creator, brand-identity, ui-component-library]
---

# Design System (Compressed)

## Purpose
Create and maintain a unified design system that ensures consistency across all products.

## Core Components
- **Design Tokens**: Primitive values (colors, spacing, typography)
- **Components**: UI building blocks with documented APIs
- **Patterns**: Common UI patterns and layouts
- **Guidelines**: Usage rules and best practices
- **Documentation**: Storybook, Figma integration

## Token Structure
```json
{
  "colors": {
    "primary": { "50": "#...", "500": "#...", "900": "#..." },
    "neutral": { "0": "#fff", "900": "#000" },
    "semantic": { "success": "...", "error": "...", "warning": "..." }
  },
  "typography": {
    "fontFamily": { "sans": "...", "mono": "..." },
    "fontSize": { "sm": "0.875rem", "md": "1rem", "lg": "1.125rem" }
  },
  "spacing": { "0": "0", "1": "0.25rem", "2": "0.5rem" },
  "borderRadius": { "sm": "0.25rem", "md": "0.5rem", "full": "9999px" }
}
```

## Figma Integration
- Tokens sync via Figma Tokens plugin
- Components as Figma variants
- Auto-layout for responsive design
- Design tokens as variables (2026)

## Documentation Standards
- Props table with types
- Usage examples
- Do's and Don'ts
- Accessibility notes
- Code snippets

## Version Control
- Semantic versioning
- Changelog generation
- Breaking change policy
- Migration guides

## Tools
- Storybook for documentation
- Figma for design
- Style Dictionary for tokens
- Chromatic for visual testing

## Related Skills
- `brand-identity/`: Brand guidelines source
- `ui-component-library/`: Component implementation
- `visual-learning-engine/`: Pattern analysis
