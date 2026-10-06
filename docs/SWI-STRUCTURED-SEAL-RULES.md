# SWI Structured & Runtime Seal Rules

## Status

```
DEFINED: YES
IMPLEMENTED: YES (mechanism)
TESTED: (see test suite)
PROVEN: NO
SEALED: NO
AUTHORIZED: NO
PRODUCTION_AUTHORIZED: NO
```

## Purpose

This document is the canonical seal contract for SWI V3.

It defines the machinery that can later determine whether a specific SWI state is sealable.

It does **not** declare any SWI state sealed.

## Core Distinctions

```
DEFINED ≠ IMPLEMENTED
IMPLEMENTED ≠ TESTED
TESTED ≠ PROVEN
PROVEN ≠ SEALED
SEALED ≠ AUTHORIZED
AUTHORIZED ≠ PRODUCTION_AUTHORIZED

STRUCTURED_SEAL ≠ RUNTIME_SEAL
SEAL ≠ AUTHORIZATION
SEAL ≠ HUMAN_AUTHORITY
SEAL ≠ PERMISSION
SEAL ≠ PRODUCTION_READINESS
PASS(t0) ≠ AUTHORIZATION(t1)
SEALED(t0) ≠ SEALED(t1)
```

A seal describes a verified state at a defined point in time.
It does not create authority.

## Scope

### Structured Seal
Immutable verification record bound to an exact repository/specification state
(exact commit SHA, never a mutable alias).

### Runtime Seal
Verification that an observed runtime state still corresponds to a sealed specification.

## Inputs (Structured Seal)

- Exact commit identity (SHA)
- Tree SHA where available
- Contract document set and versions
- Required invariant definitions
- Required negative controls
- Status declarations
- Test manifest when tests exist
- Dependency / inheritance references
- Absence of prohibited status claims
- Seal policy version

Forbidden as permanent identity:

- `latest`, `current`, `main`, `HEAD`, or any mutable alias

## Required Conditions for Seal Creation

```
EXACT_STATE_IDENTIFIED = YES
CONTRACT_SET_IDENTIFIED = YES
CONTRACT_INTEGRITY_VALID = YES
REQUIRED_ARTIFACTS_PRESENT = YES
STATUS_SNAPSHOT_AVAILABLE = YES
SEAL_POLICY_VERSION_IDENTIFIED = YES
NO_CONFLICTING_SEAL_STATE = YES
```

If any required condition cannot be established: **NO SEAL**.

Do not substitute: "probably", "latest", "looks correct", "CI green",
"previously passed", or conversation memory.

## Forbidden Conditions

- Mutable alias as seal identity
- Prohibited status claims (SEALED/AUTHORIZED/PRODUCTION without evidence)
- Conflicting active seal on the same subject
- Missing policy version
- Nondeterministic hashed payload

## Seal Creation

1. Identify exact immutable state (commit SHA).
2. Build deterministic contract/test/status manifests.
3. Evaluate all required conditions.
4. If any fail → FAILED / NO SEAL.
5. If all pass → create seal record with state ACTIVE (or TEST_SEAL for fixtures).

## Seal Verification

```
VERIFY_SEAL(seal, current_state) → structured result
```

Results:

- VALID
- INVALID
- REVALIDATION_REQUIRED
- BLOCKED

Reason codes include:

EXACT_STATE_MISMATCH, CONTRACT_HASH_MISMATCH, TREE_MISMATCH,
RUNTIME_MISMATCH, MATERIAL_CHANGE, STALE_EVIDENCE,
AUTHORITY_BINDING_MISSING, AUTHORIZATION_INVALID,
POLICY_VERSION_MISMATCH, REQUIRED_ARTIFACT_MISSING, INTEGRITY_FAILURE,
SEAL_INVALIDATED, MALFORMED_SEAL, PRODUCTION_CLAIM_FORBIDDEN

## Seal Invalidation

```
ACTIVE
  → MATERIAL CHANGE              → INVALIDATED / REVALIDATION_REQUIRED
  → RUNTIME MISMATCH             → INVALIDATED
  → CRITICAL EVIDENCE INVALID/STALE → INVALIDATED / REVALIDATION_REQUIRED
  → AUTHORITY BINDING CHANGE     → INVALIDATED
```

An invalidated seal MUST NOT continue to be treated as active.

## Revalidation

```
OLD_SEAL
  → CURRENT_STATE_CHANGED?
      ├─ NO  → verify applicability
      └─ YES → REVALIDATE (new seal process required for ACTIVE)
```

INVALIDATED → ACTIVE is forbidden without a new valid sealing process.

## Runtime Seal

Compares:

```
SEALED_STATE
    ↕
OBSERVED_RUNTIME_STATE
```

Mismatch → RUNTIME_SEAL = INVALID → REVALIDATE or BLOCK.
Do not auto-repair. Do not auto-create a new seal.

Runtime considerations:
runtime version, implementation identity, dependency state,
configuration identity, workflow identity, required capabilities,
runtime match, authority binding, authorization state,
critical observations, material-change state, test result identity,
seal policy version.

## Material Change

Examples that invalidate or suspend applicability:

implementation, contract, workflow, authority, authorization,
critical dependency, security state, critical configuration,
material environment, runtime mismatch, required hardware/sensor,
stale critical observation, seal-policy change.

If materiality of a critical state cannot be determined: REVALIDATE / BLOCK.

## Authority Separation

```
SEAL ≠ HUMAN_AUTHORITY
SEAL ≠ AUTHORIZATION
SEAL ≠ PERMISSION
SEAL ≠ LEGAL_APPROVAL
SEAL ≠ GOVERNANCE_APPROVAL
SEAL ≠ CLINICAL_APPROVAL
SEAL ≠ PRODUCTION_AUTHORIZATION
```

The seal verifier may check whether a required binding exists.
It must not manufacture the binding.

## Conversation Boundary

```
TIMESTAMP ≠ TRUTH
CONVERSATION CONTINUITY ≠ AUTHORITY CONTINUITY
REPEATED AGREEMENT ≠ CUMULATIVE PROOF
CONVERSATION HEADER ≠ AUTHORIZATION
```

## Fail-Closed Integration

Canonical source: `docs/SWI-FAIL-CLOSED-RULES.md`

Seal verification fails closed when critical conditions are missing,
unknown, stale, invalid, materially changed, integrity-compromised,
runtime-mismatched, authority-unbound, or authorization-invalid.

Responses: BLOCK / PAUSE / REVALIDATE. Never silent continuation.

## Degraded Path

A degraded path never automatically preserves a seal.
Existence of a degraded path does not create or preserve a Seal.

## State Machine

```
UNSEALED → SEAL_ELIGIBLE → SEAL_CREATED → SEAL_VERIFIED → ACTIVE
SEAL_ELIGIBLE → FAILED → NO SEAL
ACTIVE → MATERIAL CHANGE → INVALIDATED → REVALIDATION_REQUIRED
```

Forbidden:
UNSEALED → ACTIVE (without creation+verification)
INVALIDATED → ACTIVE (without new sealing process)

## Test vs Production Seals

Synthetic fixtures must be labeled `TEST_SEAL`.
They must never be accepted as `PRODUCTION_SEAL`.

## Status Discipline

Implementing and testing the seal **mechanism** does not seal SWI.

Expected after this phase:

```
DEFINED = YES
IMPLEMENTED = YES
TESTED = YES (if tests pass)
PROVEN = NO
SEALED = NO
AUTHORIZED = NO
PRODUCTION_AUTHORIZED = NO
```
