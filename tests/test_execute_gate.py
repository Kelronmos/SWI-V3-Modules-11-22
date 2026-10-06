"""
Authority / execution gate formula tests.

EXECUTE(a) ⇔
  FLOW_BIND(a)
  ∧ RUNTIME_MATCH(a)
  ∧ HUMAN_AUTHORITY_BOUND(a)
  ∧ AUTHORIZATION_VALID(a)
"""
import pytest


def execute_permitted(state: dict) -> bool:
    """Pure decision table for the documented execute gate.

    This is a test harness model, not SWI runtime.
    """
    return bool(
        state.get("flow_bind")
        and state.get("runtime_match")
        and state.get("human_authority_bound")
        and state.get("authorization_valid")
    )


class TestExecuteGate:

    def test_all_four_required_for_execute(self):
        state = {
            "flow_bind": True,
            "runtime_match": True,
            "human_authority_bound": True,
            "authorization_valid": True,
        }
        assert execute_permitted(state) is True

    def test_missing_flow_bind_blocks(self):
        state = {
            "flow_bind": False,
            "runtime_match": True,
            "human_authority_bound": True,
            "authorization_valid": True,
        }
        assert execute_permitted(state) is False

    def test_missing_runtime_match_blocks(self):
        state = {
            "flow_bind": True,
            "runtime_match": False,
            "human_authority_bound": True,
            "authorization_valid": True,
        }
        assert execute_permitted(state) is False

    def test_missing_human_authority_blocks(self):
        state = {
            "flow_bind": True,
            "runtime_match": True,
            "human_authority_bound": False,
            "authorization_valid": True,
        }
        assert execute_permitted(state) is False

    def test_missing_authorization_blocks(self):
        state = {
            "flow_bind": True,
            "runtime_match": True,
            "human_authority_bound": True,
            "authorization_valid": False,
        }
        assert execute_permitted(state) is False

    def test_runtime_match_alone_does_not_authorize(self):
        state = {
            "flow_bind": False,
            "runtime_match": True,
            "human_authority_bound": False,
            "authorization_valid": False,
        }
        assert execute_permitted(state) is False

    def test_no_shortcut_runtime_match_to_execute(self):
        """runtime match → mint permit → execute is forbidden."""
        state = {"runtime_match": True}
        assert execute_permitted(state) is False
