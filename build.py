import os
import subprocess
from src.config.settings import Settings

def build():
    version = Settings.VERSION
    exe_name = f"eleven_v{version}"
    
    print(f"Building {exe_name}...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", exe_name,
        "--add-data", "src;src",
        "--hidden-import", "pystray",
        "--hidden-import", "pystray._win32",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL._tkinter_finder",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "PIL.ImageDraw",
        "--hidden-import", "six",
        "--copy-metadata", "pystray",
        "src/main.py"
    ]
    
    # Check for icon
    icon_path = "assets/eleven.ico"
    if os.path.exists(icon_path):
        print(f"Using icon: {icon_path}")
        cmd.append(f"--icon={icon_path}")
    elif os.path.exists("eleven.ico"):
         print(f"Using icon: eleven.ico")
         cmd.append("--icon=eleven.ico")
    else:
        print("No icon found (checked assets/eleven.ico and eleven.ico). Using default.")
    
    subprocess.run(cmd, check=True)
    print(f"Build complete! Check dist/{exe_name}.exe")

if __name__ == "__main__":
    build()
