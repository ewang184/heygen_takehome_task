import os
import platform
import subprocess
import sys

def install_espeak_ng():
    os_type = platform.system()

    if os_type == "Linux":
        # For Linux (Ubuntu/Debian)
        try:
            print("Installing espeak-ng on Linux...")
            subprocess.check_call(['apt', 'update'])
            subprocess.check_call(['apt', 'install', 'espeak-ng', '-y'])
            print("espeak-ng installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing espeak-ng: {e}")
            sys.exit(1)

    elif os_type == "Darwin":
        # For macOS
        try:
            print("Installing espeak-ng on macOS...")
            subprocess.check_call(['brew', 'install', 'espeak-ng'])
            print("espeak-ng installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing espeak-ng: {e}")
            sys.exit(1)
    
    elif os_type == "Windows":
        # For Windows, use Chocolatey or download manually
        try:
            print("Installing espeak-ng on Windows...")
            # If Chocolatey is installed, we can use it
            subprocess.check_call(['choco', 'install', 'espeak-ng', '-y'])
            print("espeak-ng installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error installing espeak-ng with Chocolatey: {e}")
            print("Please consider installing espeak-ng manually.")
            sys.exit(1)

    else:
        print(f"Unsupported OS: {os_type}")
        sys.exit(1)

if __name__ == "__main__":
    install_espeak_ng()

