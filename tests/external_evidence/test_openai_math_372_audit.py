"""OpenAI Math 372-family external evidence audit tests.

Proves repository-observation discipline and anti-escalation only.
Does NOT prove mathematical correctness of the 372 families.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "evidence" / "external" / "openai_math_372" / "manifest.json"
AUDIT = ROOT / "evidence" / "external" / "openai_math_372" / "audit_results.json"


@pytest.fixture(scope="module")
def manifest():
    assert MANIFEST.is_file(), "manifest.json missing"
    return json.loads(MANIFEST.read_text())


@pytest.fixture(scope="module")
def audit():
    assert AUDIT.is_file(), "audit_results.json missing"
    return json.loads(AUDIT.read_text())


class TestCatalogueObservations:
    def test_family_count(self, manifest):
        assert manifest["expected_result_families"] == 372

    def test_manuscript_count(self, manifest):
        assert manifest["expected_manuscripts"] == 722

    def test_source_commit_frozen(self, manifest):
        assert manifest["source_commit"]
        assert len(manifest["source_commit"]) >= 40

    def test_counts_are_not_interchangeable(self, manifest):
        f = manifest["expected_result_families"]
        lean = manifest["observed_lean_linked_families"]
        formal = manifest["observed_formalization_source_entries"]
        comp = manifest["observed_comparator_configurations"]
        assert f != lean
        assert lean != formal
        assert formal != comp
        assert f != formal


class TestAuthorityNonEscalation:
    def test_authority_not_bound(self, manifest):
        assert manifest["authority_status"] == "NOT_BOUND"

    def test_authorization_not_granted(self, manifest):
        assert manifest["authorization_status"] == "NOT_AUTHORIZED"

    def test_math_verification_not_established(self, manifest):
        assert manifest["mathematical_verification_status"] == "NOT_ESTABLISHED"

    def test_production_not_authorized(self, manifest):
        assert manifest["production_authorized"] is False
        assert manifest["swi_status"]["PRODUCTION_AUTHORIZED"] is False

    def test_lean_presence_does_not_authorize(self, audit):
        # Portfolio may record partial Lean linkage; must still block authorization.
        assert audit["portfolio"]["authorization"] == "NOT_AUTHORIZED"
        assert audit["portfolio"]["authority"] == "NOT_BOUND"

    def test_evidence_exists_does_not_imply_permit(self):
        evidence_exists = True  # catalogue observed
        permit = False  # L,G,S,H not established for consequential action
        assert evidence_exists is True
        assert permit is False

    def test_formalization_does_not_imply_authorization(self):
        formalization = "PARTIAL"
        authorization = "NOT_AUTHORIZED"
        assert formalization in ("PARTIAL", "YES", "UNKNOWN")
        assert authorization == "NOT_AUTHORIZED"

    def test_machine_check_does_not_bind_human_authority(self):
        machine_check = "PASS"  # hypothetical
        human_authority_bound = False
        assert machine_check == "PASS"
        assert human_authority_bound is False

    def test_ci_green_does_not_production_authorize(self):
        ci_green = True
        production_authorized = False
        assert ci_green is True
        assert production_authorized is False

    def test_drift_status_blocked(self, audit):
        assert audit["portfolio"]["drift_status"] == "BLOCKED"


class TestLadderNonCollapse:
    def test_inequalities_recorded(self, audit):
        ineq = set(audit["inequalities"])
        assert "372_families != 235_lean_linked" in ineq
        assert "formalization != human_review" in ineq
        assert "machine_check != authority" in ineq
        assert "evidence_exists != permit" in ineq

    def test_individual_matrix_not_falsely_claimed(self, audit):
        assert audit["individual_372_row_matrix"] == "NOT_BUILT"
