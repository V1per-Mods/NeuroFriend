@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
python main.py
if errorlevel 1 (
  echo.
  echo NeuroFriend could not start. Check Python installation and error details above.
  pause
)
