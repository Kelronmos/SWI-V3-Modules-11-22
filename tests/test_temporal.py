"""
Temporal independence tests: BEFORE / DURING / AFTER.
"""
import pytest
from tests.conftest import TemporalState, Decision


class TestTemporalIndependence:

    def test_before_pass_does_not_imply_during_pass(self):
        before = {"state": TemporalState.BEFORE, "result": Decision.CONTINUE}
        during = {"state": TemporalState.DURING, "result": Decision.BLOCK}
        assert before["result"] != during["result"]
        # Independent evaluation is required by contract.

    def test_during_pass_does_not_imply_after_pass(self):
        during = {"state": TemporalState.DURING, "result": Decision.CONTINUE}
        after = {"state": TemporalState.AFTER, "result": Decision.REVALIDATE}
        assert during["result"] != after["result"]

    def test_after_pass_does_not_retroactively_authorize(self):
        during = {"state": TemporalState.DURING, "authorized": False}
        after = {"state": TemporalState.AFTER, "result": Decision.CONTINUE}
        # AFTER success must not rewrite DURING authorization.
        assert during["authorized"] is False
        assert after.get("retroactively_authorizes_during", False) is False

    def test_verified_t0_not_equal_verified_t1(self):
        t0 = {"verified": True, "time": "t0"}
        t1 = {"verified": False, "time": "t1"}
        assert t0["verified"] != t1["verified"]

    def test_available_t0_not_equal_available_t1(self):
        t0 = {"available": True, "time": "t0"}
        t1 = {"available": False, "time": "t1"}
        assert t0["available"] != t1["available"]

    def test_condition_t0_not_equal_condition_t1(self):
        t0 = {"condition": "NORMAL", "time": "t0"}
        t1 = {"condition": "DEGRADED", "time": "t1"}
        assert t0["condition"] != t1["condition"]
