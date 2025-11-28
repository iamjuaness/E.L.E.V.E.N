# Changelog

All notable changes to the **ELEVEN** project will be documented in this file.

## [0.2.0] - 2025-11-28 - JARVIS Evolution Phase

### Added

- **Neural Voice**: Integrated `edge-tts` for high-quality, natural-sounding speech (Spanish/English).
- **Natural Interaction**: Implemented LLM-based intent classification. You can now give natural instructions (e.g., "I want to code") instead of rigid commands.
- **Long-term Memory**: Added SQLite database (`src/brain/memory.py`) to store conversation history and user preferences across sessions.
- **Sound Effects (SFX)**: Added auditory feedback for "Listening" and "Processing" states using `pygame`.
- **Dynamic Personality**: Added personality sliders (Humor, Sarcasm, Sincerity) configurable via voice commands (e.g., "Set humor to 80%").
- **Model Fallback**: Implemented robust connection logic to try multiple Gemini models (`gemini-2.0-flash`, `gemini-1.5-flash`, etc.) if one fails.

### Changed

- **LLM Client**: Upgraded to use `gemini-2.0-flash` for faster and smarter responses.
- **Main Loop**: Refactored `main.py` to handle asynchronous audio and complex intent logic safely.
- **Audio Manager**: Replaced `pyttsx3` with `NeuralTTS` engine.

### Fixed

- Resolved 404 connection errors with Gemini API by implementing model fallback.
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
