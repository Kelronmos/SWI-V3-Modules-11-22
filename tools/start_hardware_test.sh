#!/usr/bin/env sh
# SWI hardware test launcher (POSIX)
# Do not invent environment-specific paths or package managers.
#
# Resolve:
#   <REPO_ROOT>  — this repository root
#   <PYTHON>     — Python interpreter available on the target host
#   <TEST_COMMAND> — repository hardware tests
#
# Example (fill placeholders for your environment):
#   <PYTHON> -m pytest tests/test_hardware_spec_interface.py tests/test_hardware_integration.py -q
#
# Preserve and return the test process exit code.
# A green launcher must not convert FAIL into PASS.

set -eu

REPO_ROOT=$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)
cd "${REPO_ROOT}"

# Placeholder resolution: use python3 if present, else python.
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "<PYTHON> not found on PATH" >&2
  exit 127
fi

export PYTHONPATH="${REPO_ROOT}${PYTHONPATH:+:$PYTHONPATH}"

echo "SWI hardware test"
echo "-----------------"
echo "REPO_ROOT=${REPO_ROOT}"
echo "PYTHON=${PYTHON}"

set +e
"${PYTHON}" -m pytest tests/test_hardware_spec_interface.py tests/test_hardware_integration.py -q
status=$?
set -e

echo "exit code = ${status}"
exit "${status}"
