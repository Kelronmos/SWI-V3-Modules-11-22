# Contract 00 — Continuation and Inheritance

## INPUT
- V2 historical artifacts (read-only reference)
- V3 baseline commit 55d843b8...

## CONDITION
V3 does not automatically inherit any V2 status claim.

## VALIDATION
Every capability claimed in V3 must have an independent V3 definition, implementation record, and test record.

## FAILURE
Any claim that treats a V2 seal or authorization as automatically valid in V3 → BLOCK / REJECT claim.

## OUTPUT
Inheritance map + explicit status for each capability (DEFINED / PARTIAL / MISSING / IMPLEMENTED / TESTED / PROVEN / SEALED / AUTHORIZED).

## STATUS
DEFINED: YES  
IMPLEMENTED: PARTIAL (this document)  
TESTED: NO  
PROVEN: NO  
SEALED: NO  
AUTHORIZED: NO
