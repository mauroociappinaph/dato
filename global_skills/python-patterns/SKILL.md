# Skill: python-patterns
**Description:** Python development principles and decision-making for 2025.
**Allowed-tools:** Read, Write, Edit, Glob, Grep

## ⚠️ How to Use This Skill
This skill teaches decision-making principles, not fixed code to copy.
- ASK user for framework preference when unclear.
- Choose async vs sync based on CONTEXT.
- Don't default to the same framework every time.

---

## 1. Framework Selection (2025)
### Decision Tree
- **API-first / Microservices:** FastAPI (async, modern, fast).
- **Full-stack web / CMS / Admin:** Django (batteries-included).
- **Simple / Script / Learning:** Flask (minimal, flexible).
- **AI/ML API serving:** FastAPI (Pydantic, async, uvicorn).
- **Background workers:** Celery + any framework.

---

## 2. Async vs Sync Decision
### When to Use Async
- I/O-bound operations (database, HTTP, file).
- Many concurrent connections.
- Real-time features.
- FastAPI/Starlette/Django ASGI.

### When to Use Sync
- CPU-bound operations.
- Simple scripts.
- Legacy codebase.
- Blocking libraries (no async version).

---

## 3. Type Hints & Pydantic
- **Always type:** Function parameters, return types, class attributes, public APIs.
- **Pydantic:** Use for API request/response models, configuration, and data validation.

---

## 4. Project Structure
- **Small:** `main.py`, `utils.py`, `requirements.txt`.
- **Medium API (App/):** `main.py`, `models/`, `routes/`, `services/`, `schemas/`.
- **Large:** `src/` layout with `core/`, `api/`, `services/`, `models/`.

---

## 5. Decision Checklist
- [ ] Asked user about framework preference?
- [ ] Chosen framework for THIS context?
- [ ] Decided async vs sync?
- [ ] Planned type hint strategy?
- [ ] Defined project structure?
