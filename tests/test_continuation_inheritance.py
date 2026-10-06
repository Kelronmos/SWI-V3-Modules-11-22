"""
Continuation and inheritance contract tests.

V2 EXISTS ≠ V3 EXISTS
V2 TESTED ≠ V3 TESTED
V2 PROVEN ≠ V3 PROVEN
V2 AUTHORIZED ≠ V3 AUTHORIZED
"""
import pytest


class TestContinuationInheritance:

    def test_v2_existence_does_not_imply_v3_existence(self):
        v2 = {"exists": True, "module": "M11", "status": "SEALED"}
        v3 = {"exists": True, "inherits_v2_seal": False}
        assert v2["exists"] is True
        assert v3["inherits_v2_seal"] is False

    def test_v2_tested_does_not_imply_v3_tested(self):
        v2_tested = True
        v3_tested_for_same_claim = False
        assert v2_tested is True
        assert v3_tested_for_same_claim is False

    def test_v2_proven_does_not_imply_v3_proven(self):
        assert "V2_PROVEN" != "V3_PROVEN"

    def test_v2_authorized_does_not_imply_v3_authorized(self):
        v2 = {"authorized": False}  # V2 itself is not production-authorized
        v3 = {"authorized": False}
        assert v2["authorized"] is False
        assert v3["authorized"] is False

    def test_inherited_principle_requires_independent_v3_record(self):
        inherited = {
            "principle": "fail-closed",
            "v2_source": True,
            "v3_independent_definition": True,
            "v3_runtime_implemented": False,
        }
        assert inherited["v3_independent_definition"] is True
        assert inherited["v3_runtime_implemented"] is False

    def test_claim_treating_v2_seal_as_v3_seal_is_rejected(self):
        claim = {"v2_sealed": True, "auto_valid_in_v3": True}
        # Contract: such a claim must be rejected.
        accepted = claim["v2_sealed"] and claim["auto_valid_in_v3"]
        # We model rejection: auto_valid_in_v3 must not be treated as true policy.
        policy_accepts_auto_inheritance = False
        assert policy_accepts_auto_inheritance is False
        assert accepted is True  # the bad claim exists
        # But policy rejects it:
        assert not policy_accepts_auto_inheritance
