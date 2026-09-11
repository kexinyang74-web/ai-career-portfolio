@echo off
cd /d "%~dp0"
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo Please run start.cmd once to install the environment.
    pause
    exit /b 1
)
"%~dp0.venv\Scripts\python.exe" "%~dp0launch_desktop.py"
if errorlevel 1 pause
