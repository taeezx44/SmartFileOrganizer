@echo off
title Smart File Organizer Pro - Installer
color 0A
cls

echo.
echo  ==========================================
echo    Smart File Organizer Pro - Setup
echo  ==========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo  [!] Python not found. Opening download page...
    echo  [!] Please install Python 3.10+ from https://python.org
    echo      Make sure to check "Add Python to PATH"
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=2 delims= " %%v in ('python --version') do set PYVER=%%v
echo  [OK] Python %PYVER% found

:: Create virtual environment
echo.
echo  [*] Creating virtual environment...
if exist venv (
    echo  [OK] venv already exists, skipping...
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo  [!] Failed to create venv
        pause
        exit /b 1
    )
    echo  [OK] Virtual environment created
)

:: Activate venv
call venv\Scripts\activate.bat

:: Upgrade pip silently
echo  [*] Upgrading pip...
python -m pip install --upgrade pip -q

:: Install dependencies
echo  [*] Installing dependencies (PyQt6)...
pip install PyQt6 PyInstaller -q
if %errorlevel% neq 0 (
    echo  [!] Failed to install dependencies
    echo  [!] Check your internet connection and try again
    pause
    exit /b 1
)
echo  [OK] Dependencies installed

:: Create desktop shortcut
echo  [*] Creating desktop shortcut...
set SCRIPT_DIR=%~dp0
set SHORTCUT=%USERPROFILE%\Desktop\Smart File Organizer.lnk
set RUN_SCRIPT=%SCRIPT_DIR%run.bat

:: Write run.bat
echo @echo off > "%RUN_SCRIPT%"
echo cd /d "%SCRIPT_DIR%" >> "%RUN_SCRIPT%"
echo call venv\Scripts\activate.bat >> "%RUN_SCRIPT%"
echo python main.py >> "%RUN_SCRIPT%"

:: Create shortcut via PowerShell
powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%RUN_SCRIPT%'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Description = 'Smart File Organizer Pro'; $s.Save()" >nul 2>&1

echo  [OK] Desktop shortcut created

echo.
echo  ==========================================
echo    Installation Complete!
echo  ==========================================
echo.
echo  [*] Launching Smart File Organizer Pro...
echo.

:: Launch the app
python main.py

pause
