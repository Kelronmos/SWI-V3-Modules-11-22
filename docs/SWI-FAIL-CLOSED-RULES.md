# SWI V3 Canonical Fail-Closed Rules

**Status:** DEFINED  
**PROVEN:** NO  
**SEALED:** NO  
**AUTHORIZED:** NO  
**PRODUCTION_AUTHORIZED:** NO

## Canonical Invariant

```
FAIL_CLOSED(a, state) ⇔
    ANY_REQUIRED_PRECONDITION_UNSATISFIED
    OR CRITICAL_STATE_UNKNOWN
    OR REQUIRED_EVIDENCE_INVALID
    OR REQUIRED_EVIDENCE_STALE
    OR MATERIAL_CHANGE_UNREVALIDATED
    OR RUNTIME_MATCH_INVALID
    OR INTEGRITY_INVALID
    OR FLOW_BINDING_INVALID
    OR HUMAN_AUTHORITY_UNBOUND
    OR AUTHORIZATION_INVALID
    OR REQUIRED_COMPONENT_MISSING_WITHOUT_VALID_DEGRADED_PATH
```

When FAIL_CLOSED evaluates true:

- DO NOT EXECUTE
- Apply the appropriate response: BLOCK / PAUSE / REVALIDATE
- PRESERVE the failure state
- REQUIRE the defined recovery condition before any continuation

## Response Distinction

| Response    | Meaning |
|-------------|--------|
| **BLOCK**   | Execution prohibited. Recovery requires satisfying a missing prerequisite. |
| **PAUSE**   | Execution interrupted pending a defined revalidation/recovery decision. |
| **REVALIDATE** | Existing authorization cannot safely continue; relevant state/evidence/environment/binding has changed or become uncertain. |

Common rule: **NO VALID EXECUTION while any fail-closed condition remains unsatisfied.**

## Hierarchy

```
DOMAIN CONDITION
      ↓
FAIL-CLOSED TRIGGER
      ↓
CANONICAL FAIL-CLOSED RULE
      ↓
BLOCK / PAUSE / REVALIDATE
      ↓
DEFINED RECOVERY CONDITION
      ↓
REVALIDATION
      ↓
ONLY THEN → POSSIBLE CONTINUATION
```

Domain documents may identify additional triggers.  
They must **not** redefine the doctrine.

## Authorization Remains Distinct

```
FAIL-CLOSED = SAFETY / CONTROL RESPONSE
AUTHORIZATION = HUMAN-AUTHORITY DECISION
```

```
EXECUTE(a) ⇔
  FLOW_BIND(a)
  ∧ RUNTIME_MATCH(a)
  ∧ HUMAN_AUTHORITY_BOUND(a)
  ∧ AUTHORIZATION_VALID(a)
```

Fail-closed conditions can prevent execution whenever those prerequisites are not satisfied.

## No "Safest Available" Exception

Unknown critical state remains FAIL-CLOSED.  
Language such as "continue if probably safe" or "operator may decide" is prohibited unless the decision is part of an explicitly defined and authorized degraded mode.

## Temporal Application

The same canonical rule is applied independently to:

- BEFORE
- DURING
- AFTER

```
PASS(BEFORE) ≠ PASS(DURING) ≠ PASS(AFTER)
```

AFTER-state failure produces reconciliation/failure recording.  
It does **not** retroactively authorize the action.
