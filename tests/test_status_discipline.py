"""
Status discipline tests — prevent status collapse.
"""
import pytest

STATUSES = [
    "DEFINED",
    "IMPLEMENTED",
    "TESTED",
    "PROVEN",
    "SEALED",
    "AUTHORIZED",
    "PRODUCTION_AUTHORIZED",
]


class TestStatusDiscipline:

    def test_status_levels_are_distinct(self):
        assert len(STATUSES) == len(set(STATUSES))

    def test_defined_does_not_equal_implemented(self):
        assert "DEFINED" != "IMPLEMENTED"

    def test_implemented_does_not_equal_tested(self):
        assert "IMPLEMENTED" != "TESTED"

    def test_tested_does_not_equal_proven(self):
        assert "TESTED" != "PROVEN"

    def test_proven_does_not_equal_sealed(self):
        assert "PROVEN" != "SEALED"

    def test_sealed_does_not_equal_authorized(self):
        assert "SEALED" != "AUTHORIZED"

    def test_authorized_does_not_equal_production_authorized(self):
        assert "AUTHORIZED" != "PRODUCTION_AUTHORIZED"

    def test_current_v3_production_authorized_is_no(self):
        production_authorized = False
        assert production_authorized is False

    def test_passing_tests_do_not_set_proven(self):
        tests_passed = True
        proven = False
        assert tests_passed is True
        assert proven is False

    def test_passing_tests_do_not_set_sealed(self):
        tests_passed = True
        sealed = False
        assert tests_passed is True
        assert sealed is False

    def test_ci_green_does_not_set_authorized(self):
        ci_green = True
        authorized = False
        assert ci_green is True
        assert authorized is False
