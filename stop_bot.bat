@echo off
echo ========================================================
echo   Stopping Daily Kalvium Form Bot (Windows Scheduler)
echo ========================================================
schtasks /delete /tn "DailyKalviumWIFormBot" /f
echo.
if %ERRORLEVEL% equ 0 (
    echo [SUCCESS] Local daily scheduled task has been removed from your PC!
) else (
    echo [INFO] Task was already removed or not found.
)
echo.
echo --------------------------------------------------------
echo To also stop GitHub Actions in the cloud:
echo 1. Go to: https://github.com/nitindhake3/wi-new/actions
echo 2. Click "Daily Google Form Auto-Fill Bot" on the left sidebar
echo 3. Click the three dots (...) and select "Disable workflow"
echo --------------------------------------------------------
echo ========================================================
pause
