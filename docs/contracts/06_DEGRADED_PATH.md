# Contract 06 — Degraded Path Control

**Status:** DEFINED  
**PROVEN:** NO  
**SEALED:** NO  
**AUTHORIZED:** NO

## Default Rule

A missing required component is **BLOCK** by default.

A degraded path is permitted **only** when a degraded operating mode has been explicitly defined, validated, and authorized **before** execution.

## Decision Flow

```
MISSING REQUIRED COMPONENT
        ↓
DEGRADED MODE DEFINED?
        ├─ NO  → BLOCK
        └─ YES
              ↓
        DEGRADED MODE CONDITIONS SATISFIED?
              ├─ NO  → BLOCK
              └─ YES
                    ↓
             HUMAN AUTHORITY BOUND?
                    ├─ NO  → BLOCK
                    └─ YES
                          ↓
                   VALID AUTHORIZATION?
                          ├─ NO  → BLOCK
                          └─ YES
                                ↓
                         EXECUTE DEGRADED MODE ONLY
```

## Required Fields for Any Degraded Mode

- MODE_ID
- TRIGGER
- MISSING / DEGRADED COMPONENT
- PERMITTED ACTIONS
- PROHIBITED ACTIONS
- REQUIRED SUBSTITUTE EVIDENCE
- REQUIRED OBSERVATIONS
- ENVIRONMENT REQUIREMENTS
- RUNTIME MATCH REQUIREMENTS
- HUMAN AUTHORITY
- AUTHORIZATION REQUIREMENTS
- REVALIDATION REQUIREMENTS
- EXIT CONDITIONS
- FAIL-CLOSED CONDITIONS
- RECORDING REQUIREMENTS

## Explicit Prohibitions

```
DEGRADED_MODE_DEFINED   ≠ DEGRADED_MODE_ALLOWED
DEGRADED_MODE_ALLOWED   ≠ AUTHORIZED
DEGRADED_PATH           ≠ FALLBACK
DEGRADED_PATH           ≠ AUTOMATIC_PERMISSION
DEGRADED_PATH           ≠ NEW_AUTHORITY
```

A degraded path must never expand the permitted action set beyond the normal-mode permission set for that action.

## Component Classification

| Class                 | Missing behaviour |
|-----------------------|-------------------|
| CRITICAL              | BLOCK (no degraded path unless architecture explicitly reclassifies) |
| REQUIRED              | BLOCK unless an explicitly defined degraded mode exists and all its conditions pass |
| OPTIONAL              | CONTINUE if all other authorization and execution conditions remain valid |
| DEGRADED-SUBSTITUTABLE| Evaluate the defined degraded contract |

## Action-Specific

Degraded mode must be bound to a specific action:

```
SENSOR X missing + ACTION A → DEGRADED MODE D-A
```

The same missing sensor may be tolerable for one action and disqualifying for another.

## Substitute Evidence

If used, must define:

WHAT, SOURCE, IDENTITY, TIMESTAMP, CONTEXT, VALIDATION, FRESHNESS, INTEGRITY, LIMITATIONS

Substitute evidence does not inherit the authority of the missing component.

```
OBSERVATION ≠ AUTHORITY
EVIDENCE    ≠ AUTHORIZATION
```

## Exit Conditions

Degraded mode ends only when a defined exit condition is met (component restored, normal evidence restored, workflow completed, operator terminates, critical uncertainty appears, etc.).

Critical uncertainty → BLOCK / PAUSE (never automatic return to normal operation).

## Recording

Durable record must identify:

```
MODE = NORMAL
or
MODE = DEGRADED
DEGRADED_MODE_ID = <id>
```

Do not claim successful normal execution when degraded execution occurred.
