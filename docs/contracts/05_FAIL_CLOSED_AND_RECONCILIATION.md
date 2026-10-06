# Contract 05 — Fail-Closed & Post-Operation Reconciliation

## Fail-Closed

The canonical fail-closed doctrine is defined in:

**docs/SWI-FAIL-CLOSED-RULES.md**

This contract identifies domain-specific triggers only.

Triggers include:

- required hardware missing
- required sensor missing
- critical state unknown
- critical observation stale
- runtime mismatch
- material drift
- integrity failure
- invalid authority
- invalid authorization

All such triggers resolve through the canonical fail-closed rule.

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

```
DEFINED: YES
IMPLEMENTED: NO
TESTED: NO
PROVEN: NO
SEALED: NO
AUTHORIZED: NO
```
