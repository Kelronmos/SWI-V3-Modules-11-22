# Contract 02 — Authority Boundary

## Separation
```
DATA ≠ EVIDENCE
EVIDENCE ≠ ADMISSION
ADMISSION ≠ AUTHORIZATION
AUTHORIZATION ≠ ACTION
```

## INPUT
Proposed action + supporting evidence package.

## CONDITION
All required authority bindings present and current.

## VALIDATION
Authority must be bound to the exact:
- actor
- workflow
- action
- jurisdiction
- consequence

## FAILURE
Missing, stale, or mismatched authority binding → BLOCK.

## OUTPUT
Authority decision record (ALLOW / DENY / HALT) + evidence references.

## STATUS
DEFINED: YES  
IMPLEMENTED: NO  
TESTED: NO  
PROVEN: NO  
SEALED: NO  
AUTHORIZED: NO
