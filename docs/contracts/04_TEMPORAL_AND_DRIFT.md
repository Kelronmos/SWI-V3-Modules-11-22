# Contract 04 — Temporal Control & Expected Match Drift

## Temporal States
```
BEFORE
↓
DURING
↓
AFTER
```

## Required Tests
```
BEFORE PASS ≠ DURING PASS
DURING PASS ≠ AFTER PASS
```

A material state change during execution must trigger REVALIDATE / PAUSE / BLOCK as appropriate.

## Expected Match Drift Process
```
EXPECTED
↓
OBSERVED
↓
COMPARE
↓
DRIFT?
├─ NO  → CONTINUE
└─ YES → REVALIDATE / PAUSE / BLOCK / ESCALATE
```

Expected Match Drift is a caution/revalidation mechanism.  
It is **not** proof of authorization.

## STATUS
DEFINED: YES  
IMPLEMENTED: NO  
TESTED: NO  
PROVEN: NO  
SEALED: NO  
AUTHORIZED: NO
