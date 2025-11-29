@echo off
echo Building eleven.exe...
echo.

REM Install PyInstaller if not present
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Build the executable
echo Building executable with PyInstaller...
pyinstaller eleven.spec

if errorlevel 1 (
    echo.
    echo Build failed!
    pause
    exit /b 1
)

echo.
echo Build successful!
echo Executable location: dist\eleven.exe
echo.
pause
