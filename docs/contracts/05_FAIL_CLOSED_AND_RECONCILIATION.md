# Contract 05 — Fail-Closed & Post-Operation Reconciliation

## Fail-Closed Minimums
- required hardware missing → BLOCK
- required sensor missing → BLOCK (or explicitly defined degraded path)
- critical state unknown → BLOCK
- critical observation stale → REVALIDATE / BLOCK
- runtime mismatch → REVALIDATE / BLOCK
- material drift → REVALIDATE / BLOCK
- integrity failure → BLOCK
- invalid authority → BLOCK

No silent fallback.

## After / Reconciliation
```
BEFORE ↔ DURING ↔ AFTER
```
Record what actually occurred.  
AFTER state must never be used to retroactively authorize the action.

## Durable Record Events
RECEIVE → IDENTIFY → OBSERVE → VALIDATE → BIND → AUTHORIZE → EXECUTE → MONITOR → REVALIDATE → RECONCILE → CLOSE

Conversation memory is not the authoritative record.

## STATUS
DEFINED: YES  
IMPLEMENTED: NO  
TESTED: NO  
PROVEN: NO  
SEALED: NO  
AUTHORIZED: NO
