"""
Runtime presence after V3-0007.

Seal mechanism + runtime boundary modules exist.
Full production authorization still does not.
"""
import pytest
import importlib.util


def _module_exists(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except (ModuleNotFoundError, ValueError):
        return False


class TestRuntimePresence:

    def test_seal_package_exists(self):
        assert _module_exists("swi_v3.seal") is True

    def test_runtime_package_exists(self):
        assert _module_exists("swi_v3.runtime") is True

    def test_execution_gate_module_exists(self):
        assert _module_exists("swi_v3.runtime.gate") is True

    def test_observation_module_exists(self):
        assert _module_exists("swi_v3.runtime.observation") is True

    def test_ledger_module_exists(self):
        assert _module_exists("swi_v3.runtime.ledger") is True

    def test_no_authority_manufacture_module(self):
        # No module that grants production authorization
        assert _module_exists("swi_v3.production_authorization") is False

    @pytest.mark.not_implemented
    def test_distributed_ledger_backend_not_implemented(self):
        pytest.skip("BLOCKED_BY_MISSING_RUNTIME: no durable distributed ledger backend")

    @pytest.mark.not_implemented
    def test_physical_sensor_drivers_not_implemented(self):
        pytest.skip("BLOCKED_BY_MISSING_RUNTIME: no physical sensor drivers")

    @pytest.mark.not_implemented
    def test_production_authorization_service_not_implemented(self):
        pytest.skip("BLOCKED_BY_MISSING_RUNTIME: no production authorization service")
