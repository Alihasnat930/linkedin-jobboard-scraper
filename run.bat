@echo off
setlocal
cd /d "%~dp0"
set "PYTHON_EXE=C:/Users/hjiaz tr/AppData/Local/Microsoft/WindowsApps/python3.11.exe"
"%PYTHON_EXE%" main.py %*
if errorlevel 1 pause
endlocal
