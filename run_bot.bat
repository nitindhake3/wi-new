@echo off
cd /d "%~dp0"
echo ========================================================
echo   Running Google Form Bot (Test / Manual Submission)
echo ========================================================
python main.py --run-now
pause
