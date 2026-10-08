# Physical Components — Status (Evidence Only)

Baseline commit reference: `a702a828` (hardware bind + runtime integration).

## Reconciliation

| Item | Status |
|------|--------|
| Existing models / bind / scope lock / runtime evaluate_hardware | REUSED |
| Physical component observation types (mic/camera/fp/sensor) | IMPLEMENTED |
| PhysicalDeviceAdapter (acquisition) | NOT_IMPLEMENTED (explicit boundary) |
| Android physical sensor adapter | NOT_IMPLEMENTED |
| Software fixture tests | TESTED |
| Physical device tests | NOT_EXECUTED |
| Hardware evidence → seal payload | NOT_IMPLEMENTED |
| HARDWARE_GREEN → AUTHORIZATION | FORBIDDEN (enforced) |
| Biometric match → human authority | NOT_ESTABLISHED / FORBIDDEN |

## Invariants

```
AVAILABLE ≠ REQUIRED ≠ VALID ≠ CONFORMANT ≠ TRUSTED ≠ AUTHORIZED
BIOMETRIC MATCH ≠ HUMAN AUTHORITY ≠ AUTHORIZATION
MICROPHONE_PASS ≠ AUTHORIZATION
CAMERA_PASS ≠ AUTHORIZATION
SENSOR_PASS ≠ AUTHORIZATION
SOFTWARE FIXTURE TEST ≠ PHYSICAL DEVICE TEST
```

## Placeholders (not executed)

- `<ANDROID_SENSOR_COMMAND>`
- `<ANDROID_CAMERA_COMMAND>`
- `<ANDROID_MIC_COMMAND>`
- `<ANDROID_BIOMETRIC_COMMAND>`
- `<PHYSICAL_SENSOR_TEST>`

## Status ceiling

- PROVEN = NO
- SEALED = NO
- AUTHORIZED = NO
- PRODUCTION = NO
