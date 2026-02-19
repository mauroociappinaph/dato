# Global Skills Architecture

## Overview

This document describes the architectural design of the Global Skills system following the Phase 2 refactoring.

## Directory Structure

```
global_skills/
├── src/                          # Core source code
│   ├── __init__.py              # Root barrel file
│   ├── core/                     # Core abstractions
│   │   ├── __init__.py
│   │   ├── base_skill.py        # SkillBase abstract class
│   │   ├── interfaces.py        # Engine interfaces
│   │   ├── exceptions.py        # Exception hierarchy
│   │   └── barrel_generator.py  # Barrel file automation
│   ├── helpers/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── file_utils.py        # File operations
│   │   ├── validation_utils.py  # Validation functions
│   │   ├── http_utils.py        # HTTP utilities
│   │   └── system_utils.py      # System/os utilities (NEW)
│   └── types/                    # Shared types
│       ├── __init__.py
│       └── common_types.py      # Data classes
│
├── scripts/                      # Automation scripts
│   ├── generate_barrel_files.py
│   └── validate_architecture.py
│
├── docs/                         # Documentation
│   └── ARCHITECTURE.md
│
├── tests/                        # Test suite
│   ├── unit/
│   └── integration/
│
└── [skills]/                     # Individual skills
    ├── skill-name/
    │   ├── __init__.py          # Auto-generated barrel
    │   ├── SKILL.md
    │   └── scripts/
    └── ...
```

## Core Principles

### 1. DRY (Don't Repeat Yourself)

**Problem**: 248 duplicate `__init__.py` files

**Solution**: Centralized `BarrelGenerator` class auto-generates all barrel files from `skill_registry.json`

```python
from src.core.barrel_generator import generate_barrel_files

# Generate all barrel files
generate_barrel_files("/path/to/global_skills")
```

### 2. Single Responsibility Principle (SRP)

Each module has a single, well-defined purpose:

- `src/core/base_skill.py`: Skill abstraction
- `src/helpers/file_utils.py`: File operations
- `src/helpers/validation_utils.py`: Validation logic
- `src/helpers/http_utils.py`: HTTP operations

### 3. The 300 Rule

No file should exceed 300 lines of code. Files that exceed this limit should be split into smaller modules.

### 4. Barrel Files Pattern

Every module exposes its public API through `__init__.py`:

```python
# src/helpers/__init__.py
from .file_utils import read_skill_file, write_skill_file
from .validation_utils import validate_skill_name

__all__ = ['read_skill_file', 'write_skill_file', 'validate_skill_name']
```

## Key Components

### SkillBase

Abstract base class for all skills:

```python
from src.core import SkillBase, SkillResult

class MySkill(SkillBase):
    @property
    def name(self) -> str:
        return "my-skill"

    @property
    def description(self) -> str:
        return "Does something useful"

    @property
    def version(self) -> str:
        return "1.0.0"

    async def execute(self, inputs: Dict[str, Any]) -> SkillResult:
        # Implementation here
        return SkillResult(
            skill_name=self.name,
            status=SkillStatus.COMPLETED,
            outputs={"result": "success"}
        )
```

### Engine Interfaces

Clear separation between Skill Engine and Playbook Engine:

```python
# Skill Engine responsibilities
class SkillEngineInterface(ABC):
    async def execute_skill(self, request: SkillRequest) -> SkillResult
    async def validate_skill(self, skill_name: str) -> bool
    async def estimate_cost(self, skill_names: List[str]) -> CostEstimation

# Playbook Engine responsibilities
class PlaybookEngineInterface(ABC):
    async def execute_playbook(self, playbook_path: str) -> PlaybookResult
    async def validate_playbook(self, playbook_path: str) -> ValidationResult
```

### Helper Utilities

Reusable functions across all skills:

```python
from src.helpers import (
    read_skill_file,
    validate_skill_name,
    make_request_with_retry,
    get_env_var,
    ensure_dir,
)

# Read skill documentation
content = read_skill_file("path/to/skill", "SKILL.md")

# Validate skill name
is_valid, error = validate_skill_name("my-new-skill")

# Make HTTP request with retry
success, data = await make_request_with_retry(
    url="https://api.example.com/data",
    max_retries=3
)

# Get environment variable with default
api_key = get_env_var("API_KEY", "default_value")

# Ensure directory exists
ensure_dir("path/to/new/directory")
```

#### System Utilities (NEW)

Centralized system operations to eliminate code duplication:

```python
from src.helpers import (
    get_env_var,      # Environment variables with defaults
    get_env_int,      # Environment variables as integers
    get_env_bool,     # Environment variables as booleans
    ensure_dir,       # Create directories
    get_project_root, # Get project root path
    list_python_files,# List Python files recursively
    join_paths,       # Join path components
    path_exists,      # Check if path exists
)
```

## Usage

### Generating Barrel Files

```bash
# Generate all barrel files
python scripts/generate_barrel_files.py

# Preview changes
python scripts/generate_barrel_files.py --dry-run
```

### Validating Architecture

```bash
# Run all validations
python scripts/validate_architecture.py

# Check specific directory
python scripts/validate_architecture.py /path/to/global_skills
```

### Creating a New Skill

1. Create skill directory:
```bash
mkdir -p my-new-skill/scripts
```

2. Add SKILL.md:
```markdown
---
name: my-new-skill
description: What this skill does
---

# My New Skill

Description here...
```

3. Generate barrel file:
```bash
python scripts/generate_barrel_files.py
```

## Migration Guide

### From Old Structure

Before:
```
global_skills/
├── skill-a/
│   ├── __init__.py          # Empty or duplicate
│   └── SKILL.md
└── skill-b/
    ├── __init__.py          # Empty or duplicate
    └── SKILL.md
```

After:
```
global_skills/
├── src/                      # Centralized code
├── skill-a/
│   ├── __init__.py          # Auto-generated barrel
│   └── SKILL.md
└── skill-b/
    ├── __init__.py          # Auto-generated barrel
    └── SKILL.md
```

### Benefits

1. **Zero Breaking Changes**: Existing skills continue to work
2. **Centralized Code**: Common utilities in `src/helpers/`
3. **Auto-Generated**: Barrel files maintained automatically
4. **Type Safety**: Shared type definitions in `src/types/`
5. **Validation**: Automated architecture validation

## Testing

Run the test suite:

```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# Validate architecture
python scripts/validate_architecture.py
```

## Contributing

1. Follow The 300 Rule
2. Use barrel files for all modules
3. Add utilities to appropriate `src/helpers/` modules
4. Run validation before committing
5. Update this documentation for architectural changes

---

**Version**: 2.0.0
**Last Updated**: 2026-02-11
**Status**: ✅ Active
