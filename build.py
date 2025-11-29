import os
import subprocess
import sys
from src.config.settings import Settings

def build():
    version = Settings.VERSION
    exe_name = f"eleven_v{version}"
    
    print(f"Building {exe_name}...")
    
    # PyInstaller command - simplified to avoid StopIteration errors
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", exe_name,
        "--add-data", "src;src",
        # Only include essential hidden imports that PyInstaller can reliably find
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "PIL.ImageDraw",
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
    
    # Run PyInstaller with error handling
    try:
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"\n✅ Build complete! Check dist/{exe_name}.exe")
        return 0
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with exit code {e.returncode}")
        print(f"Error output:\n{e.stderr}")
        if e.stdout:
            print(f"Standard output:\n{e.stdout}")
        return e.returncode
    except Exception as e:
        print(f"\n❌ Unexpected error during build: {e}")
        return 1

if __name__ == "__main__":
    exit_code = build()
    sys.exit(exit_code)
