# Principios y Feedback Efectivo

## La Mentalidad de Revisión
- **Objetivos**: Detectar bugs, garantizar mantenibilidad, compartir conocimiento, aplicar estándares y mejorar el diseño.
- **No son objetivos**: Demostrar superioridad técnica, ser quisquilloso con el formato (usa linters) o bloquear el progreso innecesariamente.

## Retroalimentación que Construye
- **Específica y accionable**: Proporciona ejemplos claros.
- **Educativa**: Explica el "por qué".
- **Centrada en el código**: No en el autor del código.
- **Equilibrada**: Elogia cuando veas un buen trabajo (`🎉 [praise]`).

### Ejemplos de lenguaje constructivo:
❌ Bad: "Rename this variable."
✅ Good: "[nit] Consider `userCount` instead of `uc` for clarity. Not blocking if you prefer to keep it."

❌ Bad: "Why didn't you use X pattern?"
✅ Good: "Have you considered the Repository pattern? It would make this easier to test. Here's an example: [link]"

## Categorización de Comentarios
Usa etiquetas para indicar prioridad y urgencia:
- 🔴 **[blocking]** - Debe corregirse antes del merge.
- 🟡 **[important]** - Debería corregirse; discutir si hay desacuerdo.
- 🟢 **[nit]** - Sugerencia menor, no bloqueante.
- 💡 **[suggestion]** - Enfoque alternativo para considerar.
- 🎉 **[praise]** - ¡Excelente trabajo!
