# Contract 07 — Hardware Spec Check Interface

## Status

```
DEFINED: YES
IMPLEMENTED: YES (library + runtime.evaluate_hardware)
TESTED: YES (unit + integration)
PROVEN: NO
SEALED: NO
AUTHORIZED: NO
PRODUCTION_AUTHORIZED: NO
```

## Purpose

Technical interface to check and verify hardware/environment specifications.

```
HARDWARE_GREEN ≠ AUTHORIZATION
SENSOR_PASS ≠ AUTHORIZATION
RUNTIME_DISCOVERY ⊬ WORKFLOW_SCOPE_EXPANSION
```

## Kernel integration

`RuntimeEngine.evaluate_hardware(...)` → ledger `HARDWARE_CHECK`

`RuntimeEngine.observe_and_gate(..., hardware_bind=...)` may feed technical failure into fail-closed signals; it must not set authorization from hardware green.

## Launchers

See `docs/HARDWARE_TEST_LAUNCHERS.md` and `tools/start_hardware_test.{sh,bat}`.

## Does not close

OPEN-015 · OPEN-016 · Wave 1 · production authorization
