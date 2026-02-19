"""
Migration Helper - The Dude S.A.S.
Helps migrate scripts to use centralized configuration.
"""
from typing import List
from pathlib import Path


OLD_PATTERNS = [
    (r'load_dotenv\(dotenv_path=[\'"].*?[\'"]\)', 'from anti_gravity.global_skills.infrastructure_core.scripts import get_config\nconfig = get_config()'),
    (r'SUPABASE_URL = "[^"]*"', '# Remove: Use get_supabase()'),
    (r'SUPABASE_KEY = os\.getenv\("SUPABASE_ANON_KEY"\)', '# Remove: Use get_supabase()'),
    (r'supabase = create_client\(SUPABASE_URL, SUPABASE_KEY\)', '# Remove: Use get_supabase()'),
    (r'API_ID = os\.getenv\("TELEGRAM_API_ID"\)', '# API_ID = config.telegram.api_id'),
    (r'API_HASH = os\.getenv\("TELEGRAM_API_HASH"\)', '# API_HASH = config.telegram.api_hash'),
    (r'/Users/mauroociappina/\.gemini/', '# Use config.paths.root_dir / ...'),
]


def check_script_migrated(script_path: Path) -> bool:
    """Check if script uses centralized config"""
    content = script_path.read_text()
    return "get_config()" in content or "get_supabase()" in content


def find_scripts_to_migrate(scripts_dir: Path = Path(__file__).parent.parent / "scripts") -> List[Path]:
    """Find all Python scripts that still use old patterns"""
    scripts = []
    for script in scripts_dir.rglob("*.py"):
        if script.name.startswith("_") or script.name.startswith("__"):
            continue
        
        if check_script_migrated(script):
            continue
        
        content = script.read_text()
        for pattern, _ in OLD_PATTERNS:
            if pattern in content:
                scripts.append(script)
                break
    
    return scripts


def migration_guide() -> str:
    """Generate migration guide"""
    return """
# Migration Guide to Centralized Configuration

## Old Pattern:
```python
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv(dotenv_path='/Users/mauroociappina/.gemini/.env')

SUPABASE_URL = "https://fmcgnrjkyecppxquijvj.supabase.co"
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

## New Pattern:
```python
from pathlib import Path
import sys

# Add infrastructure path
infrastructure_scripts = Path(__file__).parent.parent / "anti_gravity" / "global_skills" / "infrastructure-core" / "scripts"
sys.path.append(str(infrastructure_scripts))

try:
    from anti_gravity.global_skills.infrastructure_core.scripts import get_config, get_supabase
    config = get_config()
    supabase = get_supabase()
except ImportError:
    # Fallback for backward compatibility
    from dotenv import load_dotenv
    from supabase import create_client
    load_dotenv()
    SUPABASE_URL = "https://fmcgnrjkyecppxquijvj.supabase.co"
    SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

## Available Configuration:

### Config Sub-modules:
- `config.supabase.url`
- `config.telegram.api_id`, `config.telegram.api_hash`
- `config.redis.host`, `config.redis.port`
- `config.ollama.base_url`, `config.ollama.model`
- `config.groq.api_key`
- `config.paths.root_dir`, `config.paths.workspace_dir`

### Available Services:
- `get_supabase()` - Supabase client (connection pooled)
- `get_redis()` - Redis service (sync)
- `get_supabase_service()` - SupabaseService instance
- `LeadsTable` - Type-safe leads table access

## Benefits:
1. No hardcoded secrets
2. Type hints for all config values
3. Connection pooling (better performance)
4. One source of truth for configuration
5. Easy testing (can mock `get_config()`)

## Next Steps:
1. Run this script to find scripts to migrate
2. Apply the new pattern to each script
3. Test the scripts work correctly
4. Remove old dotenv.load() and variable definitions
"""


if __name__ == "__main__":
    print("=" * 60)
    print("Migration Helper - The Dude S.A.S.")
    print("=" * 60)
    
    scripts = find_scripts_to_migrate()
    
    if not scripts:
        print("✅ All scripts are already migrated to centralized configuration!")
    else:
        print(f"\nFound {len(scripts)} scripts to migrate:")
        for script in scripts:
            print(f"  - {script.relative_to(script.parent.parent)}")
        
        print("\n" + migration_guide())
