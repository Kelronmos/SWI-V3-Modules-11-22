# SWI V3 PLATFORM PORTABILITY

## Goal

Run the SWI runtime through different execution environments without
changing the governance semantics.

## Supported targets

- Linux
- macOS
- Android / Termux
- iOS (scaffold only)

## Architectural rule

```
PLATFORM CAPABILITY ≠ PERMISSION
PERMISSION ≠ AUTHORITY
AUTHORITY ≠ AUTHORIZATION
AUTHORIZATION ≠ EXECUTION
```

The platform adapter may describe the environment.

The platform adapter must **not**:

- mint permits
- create human authority
- create authorization
- bypass FLOW_BIND
- bypass RUNTIME_MATCH
- bypass HUMAN_AUTHORITY_BOUND
- bypass AUTHORIZATION_VALID
- execute consequential actions merely because a capability exists

## Architecture

```
SWI GOVERNANCE CORE
         │
    PLATFORM ADAPTER
         │
  ┌──────┼──────┬──────┐
Linux  macOS  Android  iOS
```

## Note on existing runtime

Public baseline `55d843b` does not yet contain `swi_v3/runtime/`.
This portability layer is designed to sit **around** the runtime pipe
when that pipe is present; it does not replace or authorize it.

## STATUS

| Component | Status |
|-----------|--------|
| Platform contract | DESIGNED / IMPLEMENTATION STARTED |
| Linux adapter | IMPLEMENTED (observation only) |
| macOS adapter | IMPLEMENTED (observation only) |
| Android adapter | IMPLEMENTED (observation only) |
| iOS adapter | SCAFFOLD ONLY |
| CLI | IMPLEMENTATION STARTED (inspection only) |
| Cross-platform tests | IMPLEMENTATION STARTED |
| Evidence | NOT ESTABLISHED |
| Proof | NOT ESTABLISHED |
| Seal | NOT ESTABLISHED |
| Authorization | NOT AUTHORIZED |
| Production | NOT AUTHORIZED |
