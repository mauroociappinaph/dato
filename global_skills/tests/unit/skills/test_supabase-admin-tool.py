"""
Tests for supabase-admin-tool skill.

Auto-generated test template. Customize as needed.
Generated: 2026-02-11T18:14:34.316917
"""

import pytest
from pathlib import Path


# Mark all tests in this file as skill tests
pytestmark = pytest.mark.skill


class TestSupabaseAdminToolSkill:
    """Test suite for supabase-admin-tool skill."""

    def test_skill_exists_in_registry(self, skill_registry):
        """Verify skill is registered."""
        skill_ids = [s["id"] for s in skill_registry]
        assert "supabase-admin-tool" in skill_ids, f"Skill supabase-admin-tool not found in registry"

    def test_skill_is_active(self, skill_registry):
        """Verify skill is active."""
        skill = next((s for s in skill_registry if s["id"] == "supabase-admin-tool"), None)
        assert skill is not None
        assert skill["status"] == "active"

    def test_skill_has_required_fields(self, skill_registry, skill_assertions):
        """Verify skill has all required fields."""
        skill = next((s for s in skill_registry if s["id"] == "supabase-admin-tool"), None)
        assert skill is not None
        skill_assertions.assert_valid_skill(skill)

    def test_skill_has_name(self, skill_registry):
        """Verify skill has a name."""
        skill = next((s for s in skill_registry if s["id"] == "supabase-admin-tool"), None)
        assert skill is not None
        assert skill.get("name")
        assert isinstance(skill["name"], str)

    def test_skill_has_description(self, skill_registry):
        """Verify skill has a description."""
        skill = next((s for s in skill_registry if s["id"] == "supabase-admin-tool"), None)
        assert skill is not None
        assert skill.get("description")
        assert isinstance(skill["description"], str)

    def test_skill_has_cluster(self, skill_registry):
        """Verify skill has a cluster assigned."""
        skill = next((s for s in skill_registry if s["id"] == "supabase-admin-tool"), None)
        assert skill is not None
        assert skill.get("cluster")
        assert isinstance(skill["cluster"], str)

    def test_skill_files_exist(self, skill_registry, project_root):
        """Verify skill files exist on disk."""
        skill = next((s for s in skill_registry if s["id"] == "supabase-admin-tool"), None)
        if skill and skill.get("path"):
            skill_path = Path(skill["path"])
            if not skill_path.is_absolute():
                skill_path = project_root / skill_path
            assert skill_path.exists(), f"Skill file not found: {skill_path}"

    def test_skill_has_documentation(self, project_root):
        """Verify skill has SKILL.md documentation."""
        skill_dir = project_root / "supabase-admin-tool"
        if skill_dir.exists():
            skill_md = skill_dir / "SKILL.md"
            assert skill_md.exists(), f"SKILL.md not found in {skill_dir}"

    def test_skill_has_version(self, skill_registry):
        """Verify skill has a version."""
        skill = next((s for s in skill_registry if s["id"] == "supabase-admin-tool"), None)
        assert skill is not None
        assert skill.get("version")
        # Version should follow semantic versioning (simplified check)
        version = skill["version"]
        assert "." in version, "Version should follow semantic versioning"

    def test_skill_has_cost_estimate(self, skill_registry):
        """Verify skill has cost estimate."""
        skill = next((s for s in skill_registry if s["id"] == "supabase-admin-tool"), None)
        assert skill is not None
        cost = skill.get("cost_estimate", {})
        assert "per_execution" in cost
        assert "currency" in cost

    def test_skill_has_preferred_agent(self, skill_registry):
        """Verify skill has preferred agent assigned."""
        skill = next((s for s in skill_registry if s["id"] == "supabase-admin-tool"), None)
        assert skill is not None
        assert skill.get("preferred_agent")
        assert skill["preferred_agent"].startswith("AGENT_")
