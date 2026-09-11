@echo off
rem One-click uninstaller for OptiScaler (Simplified Chinese edition).
rem All logic lives in uninstall-OptiScaler.ps1 - keep the two files together.
rem This file is ASCII on purpose: cmd mis-tracks line offsets in UTF-8 batch
rem files with multibyte characters, and starts executing comment fragments.
chcp 65001 >nul 2>nul
title Uninstall OptiScaler (Simplified Chinese)
if not exist "%~dp0uninstall-OptiScaler.ps1" (
    echo Missing uninstall-OptiScaler.ps1. Keep both uninstaller files in the same folder.
    echo.
    pause
    exit /b 1
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0uninstall-OptiScaler.ps1" %*
if errorlevel 1 exit /b %errorlevel%

rem Self-delete via a detached process: deleting while this file is still being
rem read makes cmd re-read it and execute comment fragments.
set "OPTI_SELF=%~f0"
start "" /min powershell -NoProfile -Command "Start-Sleep -Milliseconds 600; Remove-Item -LiteralPath $env:OPTI_SELF -Force -ErrorAction SilentlyContinue"
