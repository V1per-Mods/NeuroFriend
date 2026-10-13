@echo off
chcp 65001 >nul
cd /d "%~dp0"
python main.py
if errorlevel 1 (
  echo.
  echo Could not start NeuroFriend. Check that Python is installed and added to PATH.
  pause
)
