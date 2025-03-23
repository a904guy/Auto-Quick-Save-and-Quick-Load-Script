@echo off

:: Try python first (common default)
python --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    start "Monitor Script" cmd /k python "monitor.py"
    goto :EOF
)

:: Try py.exe (Python launcher)
py --version >nul 2>&1
if %ERRORLEVEL% equ 0 (
    start "Monitor Script" cmd /k py "monitor.py"
    goto :EOF
)

echo Python not found. Please install Python and ensure it's added to PATH.
pause
