# 🧪 Global Skills Testing Infrastructure

Sistema completo de testing para Global Skills con soporte para 87+ skills individuales.

---

## 📁 Estructura

```
tests/
├── __init__.py              # Package init
├── conftest.py              # Fixtures y configuración pytest
├── test_runner.py           # Utilidades de testing (SkillValidator, etc.)
├── README.md                # Esta documentación
├── unit/                    # Tests unitarios
│   ├── __init__.py
│   ├── test_helpers.py      # Tests de src/helpers
│   └── skills/              # Tests individuales por skill
│       ├── test_ai-engineer.py
│       ├── test_security-auditor.py
│       └── ... (95 archivos)
├── integration/             # Tests de integración
└── e2e/                     # End-to-end tests
```

---

## 🚀 Uso Rápido

### Ejecutar todos los tests
```bash
python scripts/run_tests.py --all
```

### Tests específicos
```bash
python scripts/run_tests.py --unit              # Solo unit tests
python scripts/run_tests.py --integration       # Solo integration tests
python scripts/run_tests.py --skill ai-engineer # Tests de un skill
python scripts/run_tests.py --architecture      # Tests de arquitectura
python scripts/run_tests.py --validate          # Validar skills
```

### Con coverage
```bash
python scripts/run_tests.py --all --coverage
```

### Listar tests disponibles
```bash
python scripts/run_tests.py --list
```

---

## 🔄 Generar Tests para Skills

### Generar todos los tests faltantes
```bash
python scripts/generate_skill_tests.py --missing
```

### Generar test específico
```bash
python scripts/generate_skill_tests.py --skill security-auditor
```

### Ver cobertura de tests
```bash
python scripts/generate_skill_tests.py --coverage
```

### Listar tests existentes
```bash
python scripts/generate_skill_tests.py --list
```

---

## 📊 CI/CD Pipeline

El workflow `.github/workflows/test.yml` ejecuta:

1. **Lint & Format** - black, flake8, mypy, isort
2. **Unit Tests** - Python 3.10, 3.11, 3.12
3. **Integration Tests** - Tests de integración
4. **Skills Validation** - Valida todos los skills
5. **Architecture Tests** - Tests de arquitectura
6. **Coverage Report** - Genera reporte de cobertura

---

## 🎯 Tipos de Tests

### Unit Tests (`tests/unit/`)
Tests de componentes individuales en aislamiento:
- `test_helpers.py` - Tests de funciones utilitarias
- `skills/test_*.py` - Tests de cada skill (95 archivos)

### Integration Tests (`tests/integration/`)
Tests de integración entre componentes:
- Comunicación Playbook Engine ↔ Skill Engine
- Validación de playbooks
- Estimación de costos

### E2E Tests (`tests/e2e/`)
Tests de flujos completos de extremo a extremo.

### Architecture Tests
Tests existentes de arquitectura:
- `basic_test.py`
- `test_architecture.py`
- `final_architecture_test.py`
- `integration_tests.py`

---

## 🧪 Fixtures Disponibles

### Skill Registry
- `skill_registry` - Lista completa de skills
- `active_skills` - Solo skills activos
- `sample_skill` - Skill de ejemplo para tests

### Mocks
- `mock_skill_engine` - Mock del Skill Engine
- `mock_playbook_engine` - Mock del Playbook Engine

### Path
- `project_root` - Directorio raíz del proyecto
- `temp_dir` - Directorio temporal
- `test_data_dir` - Directorio de datos de test

### Assertions Personalizadas
- `skill_assertions` - Aserciones para validar skills

---

## 📈 Reportes

### Reporte JSON
Después de ejecutar tests, se genera `test_report.json`:
```json
{
  "timestamp": "2026-02-11T18:00:00",
  "results": {...},
  "summary": {
    "passed": 10,
    "total": 10,
    "elapsed_seconds": 45.2
  }
}
```

### Reporte HTML
Con `--coverage` se genera `test_report.html` con interfaz visual.

### Coverage
Con `--coverage` se genera:
- `htmlcov/` - Reporte HTML detallado
- `coverage.xml` - Reporte XML para Codecov

---

## 🔧 Configuración

### pyproject.toml
Configuración de pytest, coverage, black, isort, mypy.

### Marcadores pytest
- `@pytest.mark.unit` - Tests unitarios
- `@pytest.mark.integration` - Tests de integración
- `@pytest.mark.e2e` - End-to-end tests
- `@pytest.mark.skill` - Tests de skills
- `@pytest.mark.slow` - Tests lentos

---

## 🛠️ Desarrollo

### Añadir nuevo test de skill
```bash
python scripts/generate_skill_tests.py --skill nuevo-skill
```

### Añadir test unitario
Crear archivo en `tests/unit/test_*.py`:
```python
import pytest

pytestmark = pytest.mark.unit

def test_something():
    assert True
```

### Añadir test de integración
Crear archivo en `tests/integration/test_*.py`:
```python
import pytest

pytestmark = pytest.mark.integration

async def test_integration():
    result = await something_async()
    assert result is not None
```

---

## 📊 Estadísticas

- **Total Skills**: 95
- **Tests Generados**: 95 (100%)
- **Tests por Skill**: ~11 tests
- **Total Tests Estimados**: ~1000+ tests

---

## ✅ Requisitos

```bash
pip install -e ".[test]"
```

O manualmente:
```bash
pip install pytest pytest-asyncio pytest-cov pytest-xdist pytest-mock
```

---

## 🐛 Debugging

### Ver todos los tests disponibles
```bash
python -m pytest --collect-only
```

### Ejecutar test específico
```bash
python -m pytest tests/unit/test_helpers.py::TestSystemUtils::test_path_exists -v
```

### Ejecutar con debugger
```bash
python -m pytest --pdb
```

---

## 📚 Recursos

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

---

**Estado**: ✅ Operativo
**Última actualización**: Febrero 2026
**Skills cubiertos**: 95/95 (100%)
