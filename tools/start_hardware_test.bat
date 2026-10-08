@echo off
REM SWI hardware test launcher (Windows)
REM Do not invent unverified paths or package managers.
REM
REM Resolve:
REM   <REPO_ROOT> — repository root (parent of tools\)
REM   <PYTHON> — Python interpreter on the target host
REM   <TEST_COMMAND> — hardware unit + integration tests
REM
REM Preserve and return the test process exit code.
REM Do not convert FAIL into PASS.

setlocal
cd /d "%~dp0.."
set REPO_ROOT=%CD%
set PYTHONPATH=%REPO_ROOT%;%PYTHONPATH%

echo SWI hardware test
echo -----------------
echo REPO_ROOT=%REPO_ROOT%

where python >nul 2>&1
if errorlevel 1 (
  echo ^<PYTHON^> not found on PATH
  exit /b 127
)

python -m pytest tests/test_hardware_spec_interface.py tests/test_hardware_integration.py -q
set status=%ERRORLEVEL%
echo exit code = %status%
exit /b %status%
