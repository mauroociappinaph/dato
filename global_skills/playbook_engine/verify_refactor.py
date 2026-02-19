import sys
from pathlib import Path

# Add project root to path
sys.path.append("/Users/mauroociappina/.gemini")

try:
    from anti_gravity.global_skills.playbook_engine.metrics_dashboard import MetricsDashboard
    print("✅ MetricsDashboard imported successfully")
    
    # Mock SkillEngineMaster
    class MockSkillEngine:
        pass
        
    engine = MetricsDashboard(MockSkillEngine())
    print("✅ MetricsDashboard instantiated successfully")
    
except Exception as e:
    print(f"❌ Verification failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
