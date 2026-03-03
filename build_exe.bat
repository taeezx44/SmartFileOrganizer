@echo off
title Build Smart File Organizer Pro - EXE
color 0B
cls

echo.
echo  ==========================================
echo    Building SmartFileOrganizer.exe
echo  ==========================================
echo.

:: Activate venv
if not exist venv\Scripts\activate.bat (
    echo  [!] Please run install.bat first!
    pause
    exit /b 1
)
call venv\Scripts\activate.bat

:: Clean old build
echo  [*] Cleaning previous build...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build

:: Build with PyInstaller
echo  [*] Running PyInstaller...
pyinstaller build.spec --noconfirm

if %errorlevel% neq 0 (
    echo.
    echo  [!] PyInstaller build failed!
    pause
    exit /b 1
)

echo.
echo  ==========================================
echo    Build Complete!
echo  ==========================================
echo.
echo  EXE location: dist\SmartFileOrganizer\SmartFileOrganizer.exe
echo.
echo  [*] Next step: Open installer.iss with Inno Setup
echo      to create Setup.exe installer.
echo.
echo  Download Inno Setup: https://jrsoftware.org/issetup.php
echo.

:: Open dist folder
explorer dist\SmartFileOrganizer

pause
