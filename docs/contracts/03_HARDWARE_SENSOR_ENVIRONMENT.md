# Contract 03 — Hardware / Sensor / Environment

## Pipeline (mandatory order)
```
HARDWARE
↓
SENSORS
↓
OBSERVATION
↓
ENVIRONMENT CHECK
↓
RUNTIME MATCH
↓
FLOW BIND
↓
HUMAN AUTHORITY
↓
AUTHORIZATION
↓
ACTION
```

## Explicit Blocks
```
SENSOR → AUTHORIZATION          = BLOCK
HARDWARE → AUTHORIZATION        = BLOCK
CAPABILITY → PERMISSION         = BLOCK
OBSERVATION → AUTHORITY         = BLOCK
```

## Hardware
See existing: docs/SWI-HARDWARE-IDENTITY-SPECIFICATION.md

## Sensor Observation
Must carry identity, capability, observation value, timestamp, and context.
Stale or missing critical observations → REVALIDATE or BLOCK.

## Environment
Must be checked against required operating envelope.
Material environmental change → REVALIDATE.

## STATUS
DEFINED: YES (hardware) / PARTIAL (sensor & environment)  
IMPLEMENTED: NO (runtime)  
TESTED: NO  
PROVEN: NO  
SEALED: NO  
AUTHORIZED: NO
