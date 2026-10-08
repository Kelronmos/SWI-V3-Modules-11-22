# Contract 07 — Hardware Spec Check Interface

## Status

```
DEFINED: YES
IMPLEMENTED: YES (library interface)
TESTED: YES (unit tests)
PROVEN: NO
SEALED: NO
AUTHORIZED: NO
PRODUCTION_AUTHORIZED: NO
```

## Purpose

Provide a technical interface to check and verify hardware/environment
specifications for an operation.

```
HARDWARE_GREEN ≠ AUTHORIZATION
SENSOR_PASS ≠ AUTHORIZATION
CAPABILITY ≠ PERMISSION
RUNTIME_DISCOVERY ⊬ WORKFLOW_SCOPE_EXPANSION
```

## Module

`swi_v3.hardware`

- `SpecChecker` — measurement vs ComponentSpec
- `HardwareBindInterface.evaluate(...)` — aggregate bind result
- `WorkflowScopeLock` — fixed component set while ACTIVE

## Specs must come from

COMPONENT DATASHEET + SYSTEM SPEC + OPERATION SPEC

Do not invent universal voltage/current/drift thresholds in SWI core.

## Relation to execution gate

```
EXECUTE(a) ⟺
  FLOW_BIND(a)
  ∧ RUNTIME_MATCH(a)
  ∧ HUMAN_AUTHORITY_BOUND(a)
  ∧ AUTHORIZATION_VALID(a)
```

`HARDWARE_GREEN` is an environmental/hardware predicate only.
It does not mint a permit.

## Does not close

OPEN-015 · OPEN-016 · Wave 1 · production authorization
