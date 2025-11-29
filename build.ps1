# Build ELEVEN executable
Write-Host "Building ELEVEN.exe..." -ForegroundColor Cyan
Write-Host ""

# Check if PyInstaller is installed
$pyinstaller = pip show pyinstaller 2>$null
if (-not $pyinstaller) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Build the executable using the Python build script (handles versioning)
Write-Host "Building executable with build.py..." -ForegroundColor Cyan
python build.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "Executable location: dist\ELEVEN.exe" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Build failed!" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to continue"
