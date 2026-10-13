@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
title NeuroFriend 2.0.0 - EXE Builder
echo ==========================================
echo       NeuroFriend 2.0.0 - EXE Builder
echo ==========================================
echo.
set "PY=py -3.13"
%PY% --version >nul 2>&1
if errorlevel 1 (
  set "PY=py -3.12"
  %PY% --version >nul 2>&1
)
if errorlevel 1 (
  set "PY=py -3.15"
  %PY% --version >nul 2>&1
)
if errorlevel 1 (
  set "PY=py"
  %PY% --version >nul 2>&1
)
if errorlevel 1 (
  echo ERROR: Python was not found. Install Python 3.12, 3.13, or 3.15.
  echo https://www.python.org/downloads/windows/
  pause
  exit /b 1
)
echo Using %PY%
%PY% -m pip install --upgrade pip pyinstaller
if errorlevel 1 goto error
%PY% -m compileall -q main.py
if errorlevel 1 goto error
%PY% -m PyInstaller --noconfirm --clean --onefile --windowed --name NeuroFriend main.py
if errorlevel 1 goto error
if not exist "dist\NeuroFriend.exe" goto error
echo.
echo BUILD SUCCESS: %CD%\dist\NeuroFriend.exe
echo Ollama and the model must be installed separately.
start "" "%CD%\dist"
pause
exit /b 0
:error
echo.
echo BUILD FAILED. Success is not reported because the build did not finish.
pause
exit /b 1
