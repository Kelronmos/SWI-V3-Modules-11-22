"""
Explicit tests distinguishing seal *mechanism* from full SWI runtime.

swi_v3.seal exists (mechanism).
Full execution gate / sensor pipeline / durable ledger runtime do not.
"""
import pytest
import importlib.util


def _module_exists(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except (ModuleNotFoundError, ValueError):
        return False


class TestRuntimeAbsence:

    def test_seal_mechanism_package_exists(self):
        assert _module_exists("swi_v3") is True
        assert _module_exists("swi_v3.seal") is True

    def test_no_kernel_execution_runtime(self):
        assert _module_exists("swi_v3.kernel") is False

    def test_no_authority_runtime(self):
        assert _module_exists("swi_v3.authority") is False

    def test_no_fail_closed_runtime_module(self):
        # Decision tables may exist in tests; production fail-closed runtime module does not.
        assert _module_exists("swi_v3.fail_closed") is False

    @pytest.mark.not_implemented
    def test_runtime_execution_gate_not_implemented(self):
        pytest.skip("BLOCKED_BY_MISSING_RUNTIME: no SWI V3 execution gate exists")

    @pytest.mark.not_implemented
    def test_runtime_sensor_pipeline_not_implemented(self):
        pytest.skip("BLOCKED_BY_MISSING_RUNTIME: no sensor pipeline runtime exists")

    @pytest.mark.not_implemented
    def test_runtime_durable_ledger_not_implemented(self):
        pytest.skip("BLOCKED_BY_MISSING_RUNTIME: no durable validation ledger exists")
