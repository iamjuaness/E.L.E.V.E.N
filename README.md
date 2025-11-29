# ELEVEN - AI Voice Assistant

![ELEVEN Banner](assets/icon.ico)

## Description

**ELEVEN** is an advanced AI-powered voice assistant for Windows, inspired by JARVIS. It leverages the power of **Gemini 2.0 Flash** to understand you naturally, recognize your voice, speak realistically, and control your PC.

Unlike other assistants, ELEVEN features **memory**, **adjustable personality**, and **screen vision** capabilities.

## Key Features

- 🎙️ **Wake Word**: Activate hands-free by saying "Hey Eleven", "Eleven", or "Once".
- 🧠 **Advanced AI**: Natural and complex conversations powered by Gemini 2.0.
- 🗣️ **Neural Voice**: Ultra-realistic voices in English and Spanish.
- 👁️ **Vision**: Ask "What do you see on my screen?" and it will explain it.
- 📁 **Full Control**: Open folders, files, and applications instantly.
- ⚙️ **Personality**: Adjust humor, sarcasm, and professionalism levels.
- 🚀 **Background Mode**: Runs minimized in the system tray.

---

## Installation & Setup

### 1. Download

Download the latest version (`ELEVEN_v1.2.0.exe`) from the **[Releases](https://github.com/iamjuaness/E.L.E.V.E.N/releases)** section.

### 2. Prerequisites

- **Windows 10 or 11**.
- **Gemini API Key**: You need a free key from Google.
  - Go to [Google AI Studio](https://makersuite.google.com/app/apikey).
  - Create an API Key (it's free).

### 3. First Run

1. Run the `.exe` file (Windows might ask for permission, click "Run anyway").
2. The **Settings Panel** will open.
3. Paste your **API Key** in the corresponding field.
4. Select your preferred **Language** (English/Spanish).
5. (Optional) Enable "Start with Windows" to have it always ready.
6. Click **"Save & Restart"**.

### 4. File Indexing (Important)

For ELEVEN to open your folders instantly, you need to create the initial map:

1. When the assistant is active, say: **"Map folders"** (or "Mapear carpetas" if in Spanish).
2. Wait for confirmation.
3. Done! Now you can say "Open Downloads" and it will be instant.

---

## Usage Guide

### Voice Commands

_Commands adapt to your selected language._

#### 🔧 System & Control

- **Activation**: "Hey Eleven", "Eleven", "Once"
- **Sleep**: "Sleep", "Rest" (Pauses active listening)
- **Shutdown**: "Shutdown system", "Turn off" (Closes the app)
- **Interrupt**: "Stop", "Silence", "Quiet" (Stops speech immediately)
- **Volume**: "Volume up", "Volume down", "Mute"

#### 📂 Files & Folders

- **Open Folder**: "Open [Name] folder" (e.g., "Open Projects")
  - _If multiple matches_: It will list options. Say the number (e.g., "One").
- **Create Folder**: "Create folder named [Name] in [Location]"
- **Mapping**: "Map folders" (Updates the file index)

#### 🌐 Utilities

- **Screen Analysis**: "What is on my screen?", "Explain this error"
- **Web Search**: "Search Google for [Query]"
- **Open Apps**: "Open Spotify", "Open Chrome", "Open Notepad"

### Settings Panel

You can open the panel anytime from the system tray icon (near the clock) or by saying "Open settings" / "Open interface".

- **Personality**: Play with Humor, Sarcasm, and Sincerity sliders.
- **Voice**: Switch between different male and female voices.

---

## For Developers (Source Code)

If you prefer running from Python or contributing:

1. Clone the repo: `git clone https://github.com/iamjuaness/E.L.E.V.E.N.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python src/main.py`

## License

MIT License - Created by **Juanes Cardona** ([@iamjuaness](https://github.com/iamjuaness))
