@echo off
setlocal
cd /d "%~dp0"
set "ENV_PYTHON=D:\conda\env3.10\python.exe"
if not exist "%ENV_PYTHON%" (
  echo Conda environment Python not found:
  echo %ENV_PYTHON%
  pause
  exit /b 1
)
"%ENV_PYTHON%" serve.py
