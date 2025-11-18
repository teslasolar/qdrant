#!/usr/bin/env python3
"""
Install open-source tools for video generation
"""

import subprocess
import sys
import os

def install_packages():
    """Install required Python packages"""

    print("[VIDEO] Installing open-source video generation tools...")
    print("-" * 50)

    packages = [
        "edge-tts",          # Microsoft Edge TTS (free, no API key needed!)
        "moviepy",           # Video editing
        "Pillow",            # Image processing
        "playwright",        # Web automation for screenshots
        "numpy",             # Array operations
        "selenium",          # Alternative web automation
        "webdriver-manager", # Auto-manage Chrome driver
    ]

    for package in packages:
        print(f"[INSTALL] Installing {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"[OK] {package} installed successfully")
        except Exception as e:
            print(f"[ERROR] Error installing {package}: {e}")
            print("   Try: pip install", package)

    # Install playwright browsers
    print("\n[INSTALL] Installing Playwright browsers...")
    try:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
        print("[OK] Playwright browsers installed")
    except Exception as e:
        print(f"[WARNING] Playwright browser install failed: {e}")
        print("   Run manually: python -m playwright install chromium")

    print("\n" + "=" * 50)
    print("[OK] Installation complete!")
    print("\nNext steps:")
    print("1. Run: python generate_narration.py")
    print("2. Run: python capture_screenshots.py")
    print("3. Run: python create_video.py")

    return True

if __name__ == "__main__":
    success = install_packages()
    if success:
        print("\n[READY] Ready to generate video!")
    else:
        print("\n[WARNING] Some packages may need manual installation")