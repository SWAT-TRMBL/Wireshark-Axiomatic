@echo off
echo Checking Python installation...
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python not found. Please install Python from https://www.python.org/downloads/windows/
    pause
    exit /b 1
)

echo Installing required packages...
py -m pip install --upgrade pip

echo Setup complete!
pause