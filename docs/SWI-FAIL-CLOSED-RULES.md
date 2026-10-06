# SWI Canonical Fail-Closed Rules

## Status

```
DEFINED: YES
IMPLEMENTED: NO
TESTED: NO
PROVEN: NO
SEALED: NO
AUTHORIZED: NO
PRODUCTION_AUTHORIZED: NO
```

## Purpose

This document is the canonical fail-closed contract for SWI V3.

Subsystems may define failure triggers, but they MUST NOT create independent or conflicting fail-closed doctrines.

## Canonical Rule

Execution MUST NOT continue when any critical execution prerequisite is:

- unsatisfied;
- unknown;
- stale;
- invalid;
- materially changed without revalidation;
- integrity-compromised;
- runtime-mismatched;
- flow-unbound;
- authority-unbound; or
- unauthorized.

The system MUST enter the applicable controlled response:

- BLOCK
- PAUSE
- REVALIDATE

No valid execution may continue while the unresolved fail-closed condition remains.

## Response Semantics

**BLOCK**  
Execution is prohibited because a required condition is absent, invalid, or unauthorized.

**PAUSE**  
Execution is interrupted pending a defined recovery or revalidation decision.

**REVALIDATE**  
Previously acceptable state can no longer be relied upon because a relevant condition changed, became stale, or became uncertain.

REVALIDATE does not itself authorize execution.

## Required-Component Rule

```
REQUIRED COMPONENT MISSING
        ↓
VALID DEGRADED PATH DEFINED?
        ├─ NO  → BLOCK
        └─ YES → VALIDATE DEGRADED CONDITIONS
                       ↓
                  CONDITIONS FAIL?
                    ├─ YES → BLOCK
                    └─ NO  → continue to authority/authorization gates
```

A degraded path is not an automatic permission and MUST NOT create new authority.

```
DEGRADED PATH ≠ AUTOMATIC PERMISSION
DEGRADED PATH ≠ NEW AUTHORITY
```

## Critical State

```
CRITICAL STATE UNKNOWN → BLOCK
```

No assumption of safety may substitute for a required critical state.

## Evidence

```
REQUIRED EVIDENCE INVALID → BLOCK
REQUIRED EVIDENCE STALE   → REVALIDATE / BLOCK
```

Evidence does not become authority merely because it is present.

## Runtime

```
RUNTIME MATCH INVALID → REVALIDATE / BLOCK
```

Runtime match does not itself authorize an action.

## Material Change

A material change affecting execution conditions requires revalidation.

```
MATERIAL CHANGE
→ REVALIDATE
→ if unresolved → BLOCK / PAUSE
```

## Integrity

```
INTEGRITY FAILURE → BLOCK
```

## Authority

```
FLOW BINDING INVALID     → BLOCK
HUMAN AUTHORITY UNBOUND  → BLOCK
AUTHORIZATION INVALID    → BLOCK
```

## Temporal Control

Fail-closed evaluation applies independently across:

- BEFORE
- DURING
- AFTER

Therefore:

```
BEFORE PASS ≠ DURING PASS
DURING PASS ≠ AFTER PASS
```

A later successful state MUST NOT retroactively authorize an earlier action.

## Degraded Operation

A degraded path MUST be:

- explicitly defined;
- action-specific;
- condition-specific;
- bounded in scope;
- subject to human-authority requirements;
- subject to authorization requirements;
- subject to revalidation;
- recorded as degraded execution.

A degraded path MUST NOT silently expand the authorized action set.

## Canonical Invariant

```
FAIL_CLOSED(a, state)
```

applies whenever a critical execution prerequisite is not presently satisfied.

The existence of a recovery path does not mean the action is currently authorized.

## Separation

```
FAIL-CLOSED ≠ AUTHORIZATION
FAIL-CLOSED = CONTROL RESPONSE
AUTHORIZATION = HUMAN-AUTHORITY DECISION
```

The fail-closed mechanism may prevent execution, but it does not manufacture authorization.

## Durable Record

Fail-closed events MUST eventually be represented in the authoritative execution record when runtime implementation exists.

Conversation memory is not the authoritative record.

## Status Discipline

Documentation of this rule does not constitute implementation.

```
DEFINED ≠ IMPLEMENTED
IMPLEMENTED ≠ TESTED
TESTED ≠ PROVEN
PROVEN ≠ SEALED
SEALED ≠ AUTHORIZED
AUTHORIZED ≠ PRODUCTION_AUTHORIZED
```
