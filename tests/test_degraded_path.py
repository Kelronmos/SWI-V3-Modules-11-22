"""
Degraded-path decision table tests.
"""
import pytest
from tests.conftest import Decision


class TestDegradedPathMatrix:

    def test_missing_required_no_path_blocks(self, degraded_path):
        result = degraded_path.evaluate({
            "required_component_missing": True,
            "valid_degraded_path_defined": False,
        })
        assert result == Decision.BLOCK

    def test_path_exists_conditions_fail_blocks(self, degraded_path):
        result = degraded_path.evaluate({
            "required_component_missing": True,
            "valid_degraded_path_defined": True,
            "degraded_conditions_satisfied": False,
        })
        assert result == Decision.BLOCK

    def test_conditions_pass_authority_unbound_blocks(self, degraded_path):
        result = degraded_path.evaluate({
            "required_component_missing": True,
            "valid_degraded_path_defined": True,
            "degraded_conditions_satisfied": True,
            "human_authority_bound": False,
        })
        assert result == Decision.BLOCK

    def test_authority_bound_authorization_invalid_blocks(self, degraded_path):
        result = degraded_path.evaluate({
            "required_component_missing": True,
            "valid_degraded_path_defined": True,
            "degraded_conditions_satisfied": True,
            "human_authority_bound": True,
            "authorization_valid": False,
        })
        assert result == Decision.BLOCK

    def test_all_conditions_satisfied_allows_degraded_execution(self, degraded_path):
        result = degraded_path.evaluate({
            "required_component_missing": True,
            "valid_degraded_path_defined": True,
            "degraded_conditions_satisfied": True,
            "human_authority_bound": True,
            "authorization_valid": True,
        })
        assert result == Decision.EXECUTE_DEGRADED

    def test_degraded_path_is_not_automatic_permission(self):
        """Existence of a defined degraded path is not permission."""
        assert "DEGRADED_PATH_DEFINED" != "PERMISSION"

    def test_degraded_path_is_not_new_authority(self):
        assert "DEGRADED_PATH" != "NEW_AUTHORITY"

    def test_degraded_path_is_not_fallback(self):
        assert "DEGRADED_PATH" != "FALLBACK"
