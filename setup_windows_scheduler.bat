@echo off
setlocal
echo ========================================================
echo   Setting up Daily Google Form Bot Windows Scheduled Task
echo ========================================================

set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=python"

for /f "tokens=*" %%i in ('where python') do (
    set "PYTHON_EXE=%%i"
    goto :found_python
)

:found_python
echo Using Python at: "%PYTHON_EXE%"
echo Script at: "%SCRIPT_DIR%main.py"

schtasks /create /tn "DailyKalviumWIFormBot" /tr "\"%PYTHON_EXE%\" \"%SCRIPT_DIR%main.py\" --run-now" /sc daily /st 11:00 /f

if %ERRORLEVEL% equ 0 (
    echo.
    echo ========================================================
    echo [SUCCESS] Windows Task 'DailyKalviumWIFormBot' registered!
    echo It will trigger every day at 11:00 AM IST automatically.
    echo ========================================================
) else (
    echo.
    echo [ERROR] Could not register task. Please right-click and "Run as Administrator".
)

echo.
pause
