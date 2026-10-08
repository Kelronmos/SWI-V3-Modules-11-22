# Hardware test launchers

**Status:** DOCUMENTED LAUNCHERS · NOT physical sensor validation

```
ANDROID SOFTWARE TEST ≠ PHYSICAL ANDROID SENSOR VALIDATION
LAUNCHER WORKS ≠ HARDWARE PROVEN
HARDWARE_GREEN ≠ AUTHORIZATION
```

## Placeholders

| Placeholder | Meaning |
|-------------|--------|
| `<REPO_ROOT>` | Repository root |
| `<PYTHON>` | Host Python interpreter |
| `<TEST_COMMAND>` | Hardware pytest suite |
| `<ANDROID_TERMINAL>` | e.g. Termux shell |
| `<ANDROID_TEST_COMMAND>` | Software tests only unless physical adapter exists |

## POSIX

```
./tools/start_hardware_test.sh
```

Or:

```
<PYTHON> -m pytest tests/test_hardware_spec_interface.py tests/test_hardware_integration.py -q
```

## Windows

```
tools\start_hardware_test.bat
```

## Android / Termux (software only)

```
<ANDROID_TERMINAL>
cd <REPO_ROOT>
<PYTHON> -m pytest tests/test_hardware_spec_interface.py tests/test_hardware_integration.py -q
```

```
PHYSICAL ANDROID SENSOR ACCESS = NOT IMPLEMENTED
ANDROID_PHYSICAL_SENSOR_ADAPTER = NOT IMPLEMENTED
```

## Seal readiness

Hardware bind records are technical evidence only.

```
SEAL INTEGRATION = NOT IMPLEMENTED (hardware evidence not wired into seal payload)
SEAL READINESS = NOT_READY
```
