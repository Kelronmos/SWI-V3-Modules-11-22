# SWI V3 Hardware Identity Specification

## Purpose

Define the contract for hardware identity, availability, capability, and condition.

Hardware identity is necessary for verification but does not establish authorization.

```
HARDWARE IDENTITY ≠ AUTHORIZATION
HARDWARE AVAILABLE ≠ PERMISSION
HARDWARE CAPABLE ≠ AUTHORITY
```

## Hardware Identity Contract

Every hardware entity in SWI must be capable of expressing:

### Required Fields

```
hardware_id          (string, unique identifier)
hardware_type        (string, device category)
hardware_name        (string, human-readable name)
manufacturer         (string, optional)
model                (string, optional)
serial_number        (string, optional, if applicable)
firmware_version     (string, optional)
configuration_id     (string, reference to configuration)
integrity_status     (enum: VERIFIED, UNKNOWN, DEGRADED, FAILED)
last_verified        (ISO 8601 timestamp)
verification_method  (string, how integrity was established)
```

### Optional Fields

```
location             (string, physical location)
operational_mode     (enum: ACTIVE, IDLE, MAINTENANCE, FAILED)
power_status         (enum: ON, OFF, LOW, UNKNOWN)
connectivity_status  (enum: CONNECTED, DISCONNECTED, DEGRADED)
health_status        (string, implementation-specific)
```

## Hardware Availability Contract

Availability is the capability to detect and verify a hardware component exists.

It does not establish that the hardware is authorized for operation.

```
AVAILABLE ≠ AUTHORIZED
DETECTED ≠ PERMITTED
PRESENT ≠ VALIDATED
```

### Availability Fields

```
is_available         (boolean, hardware detectable now)
detection_timestamp  (ISO 8601, when availability was last checked)
detection_method     (string, how availability was determined)
availability_confidence (float 0.0-1.0, certainty of detection)
availability_evidence (string, reference to evidence)
required_for_workflow (boolean, is this hardware required for this workflow)
degraded_path_exists (boolean, can operation continue if unavailable)
```

## Hardware Capability Contract

Capability describes what the hardware can do, not whether it should be used.

```
CAPABILITY ≠ PERMISSION
CAN_DO ≠ SHALL_DO
AVAILABLE ≠ AUTHORIZED
```

### Capability Fields

```
capabilities        (array of strings, what this hardware supports)
capability_version  (string, version of capability set)
capability_source   (string, where capability is defined)
supported_workflows (array, which workflows this hardware can support)
performance_limits  (object, quantified limits)
known_constraints   (array, documented limitations)
```

## Hardware Condition Contract

Condition describes the current state, not authorization.

```
CONDITION ≠ AUTHORIZATION
STATE ≠ PERMISSION
NORMAL ≠ AUTHORIZED
```

### Condition Fields

```
condition_state      (enum: NORMAL, DEGRADED, FAULTY, UNKNOWN)
condition_timestamp  (ISO 8601, when condition was last assessed)
condition_check_method (string, how condition was determined)
environmental_match  (boolean, environment compatible with requirements)
environmental_drift  (boolean, environment has materially changed)
last_revalidation    (ISO 8601, last time condition was revalidated)
revalidation_interval (integer seconds, how often revalidation is required)
configuration_match  (boolean, current config matches expected)
firmware_current     (boolean, firmware is current/supported)
```

## Hardware Configuration Contract

Configuration is the binding of hardware to workflow requirements.

```
CONFIGURED ≠ AUTHORIZED
BOUND ≠ PERMITTED
MATCHES ≠ VALID
```

### Configuration Fields

```
configuration_id     (string, unique config identifier)
hardware_id          (string, which hardware this config applies to)
workflow_id          (string, which workflow this binds to)
binding_timestamp    (ISO 8601, when binding was established)
configuration_policy (string, reference to configuration rules)
required_fields      (array, fields that must match)
tolerance_range      (object, acceptable variation)
performance_thresholds (object, required performance levels)
environment_requirements (object, required environmental conditions)
sensor_requirements   (array, which sensors must be available)
```

## Hardware Integrity Contract

Integrity establishes that hardware identity and configuration have not been tampered with.

It does not establish authorization to operate.

```
INTEGRITY_VERIFIED ≠ AUTHORIZED
UNMODIFIED ≠ PERMITTED
SIGNATURE_VALID ≠ AUTHORITY
```

### Integrity Fields

```
integrity_method     (string, how integrity is verified)
integrity_source     (string, reference implementation/standard)
integrity_check_result (enum: PASSED, FAILED, UNKNOWN)
integrity_timestamp  (ISO 8601, when check was performed)
integrity_evidence   (string, reference to evidence)
signing_authority    (string, who signed the integrity evidence)
certificate_valid    (boolean, if certificate-based)
certificate_expires  (ISO 8601, if certificate-based)
```

## Temporal Model

Hardware state is temporal.

A verified state at t0 does not automatically remain valid at t1.

```
VERIFIED(t0) ≠ VERIFIED(t1)
AVAILABLE(t0) ≠ AVAILABLE(t1)
CONDITION(t0) ≠ CONDITION(t1)
```

Revalidation is required:
- Before consequential operation
- Periodically during operation
- After operation (to detect changes)
- When environment materially changes
- When material drift is detected

## Authority Boundary

Hardware contracts establish capability and condition.

Authority is bound separately:

```
HARDWARE_AVAILABLE + HARDWARE_CAPABLE + CONDITION_NORMAL
  ≠
AUTHORIZATION_TO_OPERATE

Authorization requires:
- Hardware contract fulfilled
- Sensor contract fulfilled
- Environment contract fulfilled
- Workflow binding established
- Human authority granted
- Execution conditions validated
- All revalidation checks passed
- Fail-closed conditions satisfied
```

## Status

```
SPECIFICATION: IMPLEMENTED
IMPLEMENTED: YES (as specification)
TESTED: NO (runtime implementation pending)
PROVEN: NO
SEALED: NO
AUTHORIZED: NO
PRODUCTION_AUTHORIZED: NO
```

## Next Steps

Subsequent V3 transactions will implement:
- Hardware detection and registration
- Hardware verification workflows
- Integrity checking mechanisms
- Revalidation scheduling
- Fail-closed enforcement

This specification defines the contract that implementations must satisfy.
