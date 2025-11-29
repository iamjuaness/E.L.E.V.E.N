# Changelog

## [1.2.0] - 2025-11-29 - Stability & Intelligence Update & Internationalization Update

### Added

- **Intelligent Folder Mapping**: New system to index all folders on the PC for instant search.
  - New command: "Mapear carpetas" to start indexing.
  - Database-backed search (< 0.1s response time).
  - Smart filtering of system folders (Windows, Program Files, etc.).
  - Interactive selection when multiple folders match (e.g., "Option 1: Documents in Users").
- **Spatial Audio Feedback**: Replaced annoying beeps with a futuristic spatial activation sound.
- **Microphone Thread Safety**: Implemented locking mechanism to prevent `context manager` errors.
- **Full Internationalization (i18n)**:
  - Complete support for English and Spanish (es-ES / en-US).
  - Documentation (`README.md`) translated to English.
  - Commands and responses adapt dynamically to the selected language in Settings.
  - New `locales.py` module to manage translations.
- **Bilingual Voice Commands**:
  - "Map folders" / "Mapear carpetas"
  - "Stop" / "Detente"
  - "Sleep" / "Duérmete"
  - "Shutdown" / "Apágate"

### Fixed

- **Critical Audio Crash**: Fixed `WinError 32` by using unique temporary filenames for TTS generation.
- **Infinite Listening Loop**: Added smart pauses to prevent log spam and high CPU usage when background noise is present.
- **"Stop" Command Logic**: "Detente" / "Stop" commands are now intercepted _before_ LLM processing, ensuring immediate silence without triggering web searches.
- **Wake Word Sensitivity**: Adjusted energy threshold (400) and re-added "Once" variation to reduce false positives.

## [1.1.2] - 2025-11-29

### Added

- **Windows Auto-Start**: Application can now start automatically with Windows
  - New `startup_manager` module to manage Windows Registry entries
  - GUI checkbox to enable/disable auto-start
  - Auto-start runs in headless mode (no GUI) by default
- **Headless Mode**: Command-line arguments to control GUI visibility
  - `--no-gui` or `--headless`: Run without showing the GUI
  - `--show-gui`: Explicitly show the GUI
  - Perfect for running as a background service
- **Voice Command to Show GUI**: New voice commands to open the interface from headless mode
  - "Mostrar interfaz" / "Muestra la interfaz"
  - "Abre la configuración" / "Open settings"
  - "Show interface"

### Changed

- Improved command-line argument handling with argparse
- **Improved Interruption Detection**: Increased timeout from 0.3s to 0.5s for better "stop" command detection while speaking

## [1.1.1] - 2025-11-29

### Fixed

- **GitHub Actions Build Workflow**: Fixed executable upload failure by replacing wildcard pattern with dynamic filename resolution
- **PyInstaller Build Error**: Fixed `StopIteration` exception during build process
  - Removed problematic `--copy-metadata pystray` flag that caused module discovery errors
  - Simplified hidden imports to only essential PIL modules
  - Added comprehensive error handling with detailed error messages
- **PyInstaller Dependencies**: Fixed `ModuleNotFoundError` for `pystray` module in built executables
  - Made `pystray` import conditional (lazy loading) to prevent startup crashes
  - System tray functionality now gracefully handles missing pystray module

### Changed

- Standardized executable naming to lowercase: `eleven_v{version}.exe`
- Updated all build scripts to reflect lowercase naming convention
- Improved build script error reporting and diagnostics

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
