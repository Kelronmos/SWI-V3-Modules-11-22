"""
Explicit tests that runtime is NOT implemented.

These tests document BLOCKED_BY_MISSING_RUNTIME rather than fabricating code.
"""
import pytest
import importlib.util


def _module_exists(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


class TestRuntimeAbsence:

    def test_no_swi_v3_runtime_package(self):
        assert _module_exists("swi_v3") is False

    def test_no_kernel_module(self):
        assert _module_exists("swi_v3.kernel") is False

    def test_no_authority_runtime(self):
        assert _module_exists("swi_v3.authority") is False

    def test_no_fail_closed_runtime(self):
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
