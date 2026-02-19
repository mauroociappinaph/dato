---
name: infrastructure-core
description: Core infrastructure abstractions for Supabase, Redis, and common data operations. Eliminates code duplication across skills.
---

# Infrastructure Core

## Purpose
Provides reusable, battle-tested abstractions for common infrastructure operations, eliminating code duplication and ensuring consistent error handling across all skills.

## Capabilities
- **Supabase Operations**: CRUD, context management, batch operations
- **Redis Operations**: Caching, sessions, pub/sub
- **Error Handling**: Centralized retry logic and error reporting
- **Logging**: Unified operation logging

## Usage

### Supabase
```python
from infrastructure_core.supabase_infra import store_result, load_by_id

# Store data
result = await store_result('leads', {'name': 'Acme Corp', 'status': 'new'})

# Load data
lead = await load_by_id('leads', 'uuid-here')
```

### Redis
```python
from infrastructure_core.redis_infra import cache_set, cache_get

# Cache data
await cache_set('user:123', user_data, ttl=3600)

# Retrieve cached data
user = await cache_get('user:123')
```

## Files
- `scripts/supabase_infra.py`: Supabase abstractions
- `scripts/redis_infra.py`: Redis abstractions
- `scripts/common.py`: Shared utilities
