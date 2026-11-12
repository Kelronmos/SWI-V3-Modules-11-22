# SWI Patch Foundation Contract

**Status:** DESIGNED / ADOPTED AS ENGINEERING RULE (documentation)  
**Date:** 2026-11-12  
**Scope:** Cross-repository — Android, Termux, desktop, browser, inference, hardware bindings, Python governance spine  
**PROVEN = NO · SEALED = NO · PRODUCTION_AUTHORIZED = NO**

## Permanent architectural principle

> A patch must not merely remove an error. It must improve the system's ability to recognize, diagnose, prevent, contain and learn from the same class of failure in the future.

> Every failure must leave the system wiser, not merely running again.

```
DESIGNED ≠ IMPLEMENTED ≠ TESTED ≠ PROVEN ≠ SEALED ≠ AUTHORIZED
```

Intelligence must never be confused with authority.

---

## 1. Learning and defensive cycle

```
Failure → Evidence → Reflex → Governance
```

| Stage | Duty |
|-------|------|
| **DETECT** | Recognize error, anomaly, inconsistency, or unexpected transition |
| **HALT** | Stop the affected operation before propagation |
| **RECORD / SCAR** | Preserve original error, context, hashes, dependencies, conditions |
| **COMMON SENSE** | Compare expected vs observed; mark ambiguity and missing information |
| **REFLEX CANDIDATE** | Derive a defensive response from the recorded failure |
| **REPLAY / ADVERSARIAL TEST** | Reproduce failure; test whether the reflex prevents recurrence |
| **NEW ZERO / SEEDER** | Rebuild from a clean baseline while preserving evidence and lineage |
| **VERIFY** | Test repair, regression behaviour, bypass resistance |
| **GOVERN** | Human review; separately authorized promotion only |

---

## 2. Four cooperating intelligence layers

| Layer | Responsibility | Must never do |
|-------|----------------|---------------|
| **CEI – Common Error Intelligence** | Group errors, root causes, shared dependencies | Guess root causes |
| **Common Sense / CEK** | Observe consistency, anomalies, ambiguity, missing context | Declare truth or authority |
| **SCAR / S9** | Preserve failure history; develop defensive responses | Silently promote lessons into policy |
| **REFLEX / SADU** | Execute *tested* defensive responses | Bypass authorization |

Relationship:

- CEI identifies **what** failed.
- Common Sense interprets **what happened**.
- SCAR preserves **what was learned**.
- Reflex demonstrates **how to respond**.
- Seeder rebuilds from a **clean baseline**.
- S9 governs progression from failure evidence to **validated** defensive behaviour.

A scar is a **lesson record**, not a new law.  
A reflex is **tested defensive behaviour**, not authority.

---

## 3. Mandatory patch contract

Every SWI repository repair must satisfy:

```text
SWI_PATCH_FOUNDATION_CONTRACT

01. ORIGINAL_FAILURE_PRESERVED
02. ROOT_CAUSE_IDENTIFIED_OR_UNKNOWN
03. AFFECTED_COMPONENTS_MAPPED
04. SHARED_DEPENDENCIES_IDENTIFIED
05. EXISTING_SCARS_CHECKED
06. NEW_SCAR_CREATED_WHEN_JUSTIFIED
07. REFLEX_CANDIDATE_DEFINED
08. REGRESSION_TEST_ADDED
09. FAILURE_REPLAY_TESTED
10. BYPASS_RESISTANCE_TESTED
11. CLEAN_BASELINE_REBUILT
12. EVIDENCE_AND_LINEAGE_VERIFIED
13. HUMAN_REVIEW_RECORDED
14. AUTHORIZATION_SEPARATELY_VALIDATED
```

A patch that only removes an immediate symptom without reusable diagnostic or defensive improvement is **incomplete against this contract**.

Root cause may be recorded as **UNKNOWN**. Guessing is forbidden.

---

## 4. Continuous governance without uncontrolled self-learning

### Permitted learning

- Recognize recurring errors
- Detect suspicious patterns
- Preserve failure evidence
- Recommend repairs
- Test defensive reflexes
- Detect regressions
- Escalate unresolved risks

### Not automatically permitted

- Rewrite governing policies
- Grant itself new permissions
- Promote an untested reflex
- Change authorization boundaries
- Treat successful tests as production authorization

```
TESTED ≠ PROVEN ≠ SEALED ≠ PRODUCTION_AUTHORIZED
OBSERVATION ≠ AUTHORIZATION
SCAR ≠ POLICY
REFLEX ≠ AUTHORITY
```

---

## 5. Worked example seed — Termux / inference context overflow

**Original failure class:** request exceeds verified model context capacity  
(example observation: ~8,764-token request against 512-token capacity — preserve exact measured values in the scar when available).

### Required treatment (not merely “increase the limit”)

1. Preserve original request size and verified capacity numbers.
2. Identify inference runtime and model identity.
3. Inspect memory / runtime constraints.
4. Create a **context-capacity diagnostic**.
5. Build a **request-size guard**.
6. Test **safe request segmentation** where authorized.
7. Preserve evidence across segments.
8. Replay oversized requests.
9. Verify controlled HALT / report rather than crash.

### Reflex candidate

```text
IF REQUEST_SIZE > VERIFIED_CONTEXT_CAPACITY:
    HALT_SUBMISSION
    PRESERVE_REQUEST_EVIDENCE
    IDENTIFY_CONTEXT_LIMIT
    CHECK_SAFE_SEGMENTATION
    REQUEST_OR_APPLY_AUTHORIZED_RECOVERY
    REPLAY_VALIDATION
    REPORT_TRUE_STATE
```

This reflex remains a **candidate** until replay-tested, human-reviewed, and separately authorized for the target environment.

---

## 6. Implementation status of this document

| Claim | State |
|-------|--------|
| Principle named | YES |
| Contract text adopted in V3 docs | YES (this file) |
| Automated enforcement in CI | NO |
| CEI / SCAR / Reflex runtime modules | NOT CLAIMED HERE |
| Termux context-overflow reflex implemented | NO — candidate only |
| PROVEN / SEALED / PRODUCTION_AUTHORIZED | NO |

---

## 7. Cross-repository application

Apply this contract to repairs in:

- `Kelronmos/SWI-V3-Modules-11-22`
- `Kelronmos/SWI-V2-Modules-11-22`
- `Kelronmos/SWI-Android-Prototype`
- `Kelronmos/Cek`
- Termux / local runtime packages
- Inference and hardware-binding layers

Do not merge enforcement tooling to `main` without independent review.
