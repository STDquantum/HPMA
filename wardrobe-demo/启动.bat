@echo off
chcp 65001 >nul
cd /d "%~dp0"
title HPMA wardrobe demo - local server
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0serve.ps1"
if errorlevel 1 pause
exit /b 0