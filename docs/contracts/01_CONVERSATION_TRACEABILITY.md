# Contract 01 — Conversation Traceability Header

## Purpose
Provide context and sequence tracking only. Never authority.

## Minimum Fields
- timestamp (ISO 8601)
- conversation_id
- sequence

## Optional Fields
- previous_interaction
- source

## Explicit Prohibitions
```
TIMESTAMP ≠ TRUTH
HEADER ≠ AUTHORITY
CONVERSATION CONTINUITY ≠ AUTHORITY CONTINUITY
REPEATED AGREEMENT ≠ PROOF
TEMPORARY MEMORY ≠ DURABLE AUTHORIZATION
```

## INPUT
Conversation event.

## CONDITION
Header present and parseable.

## VALIDATION
Header is treated as observation only.

## FAILURE
Any attempt to use header fields as authorization input → BLOCK.

## OUTPUT
Trace record (non-authoritative).

## STATUS
DEFINED: YES  
IMPLEMENTED: NO (runtime)  
TESTED: NO  
PROVEN: NO  
SEALED: NO  
AUTHORIZED: NO
