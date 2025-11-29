# Changelog

## [1.1.1] - 2025-11-29

### Fixed

- **GitHub Actions Build Workflow**: Fixed executable upload failure by replacing wildcard pattern with dynamic filename resolution
- **PyInstaller Dependencies**: Fixed `ModuleNotFoundError` for `pystray` module in built executables
  - Made `pystray` import conditional (lazy loading) to prevent startup crashes
  - Added comprehensive hidden imports: `pystray._win32`, `PIL._tkinter_finder`, `PIL.Image`, `PIL.ImageDraw`, `six`
  - Added `--copy-metadata pystray` to ensure metadata is included
  - System tray functionality now gracefully handles missing pystray module

### Changed

- Standardized executable naming to lowercase: `eleven_v{version}.exe`
- Updated all build scripts to reflect lowercase naming convention

## [1.1.0] - 2025-11-29 - Enhanced GUI & Persistence

### Added

- **SQLite Database**: Settings are now persisted in `memory.db` across restarts.
- **System Tray**: Application can now run in background ("Ocultar en Bandeja").
- **Wake Word**: Added "Once" as an alternative wake word.
- **Shutdown Command**: Added "Apagar sistema" / "Shutdown system" to fully terminate the app.
- **Model Fallback**: Automatically switches Gemini models if API quota is exceeded (429 Error).
- **Restart Button**: Added button in GUI to restart application.
- **Build Script**: `build.py` to generate versioned executables (e.g., `ELEVEN_v1.1.0.exe`).

### Changed

- **GUI Architecture**: Refactored to run on the main thread for stability.
- **Console Output**: Redirected logs to a new "Consola" tab in the GUI.
- **Speech Interruption**: Optimized detection speed for "stop" commands.

### Fixed

- Fixed `ModuleNotFoundError` for `src` imports.
- Improved application launching logic for Windows.

## [0.1.0] - 2025-11-28 - Initial Release

### Added

- Core application structure.
- Basic Speech Recognition (`SpeechRecognition` library).
- Basic Text-to-Speech (`pyttsx3`).
- Integration with Google Gemini API.
- Command Execution Engine (`CommandExecutor`).
- Basic System Control (Volume, App Launching).
- Web Browser capabilities (Search, Open URL).
