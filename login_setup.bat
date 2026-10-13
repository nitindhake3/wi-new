@echo off
cd /d "%~dp0"
echo ========================================================
echo   Google Account One-Time Login Setup
echo ========================================================
echo A browser window will open.
echo Please log into your nitin.dhake.s73@kalvium.community Google Account.
echo Once logged in and you see the Google Form, return here and press ENTER.
echo ========================================================
python main.py --setup-auth
pause
