#!/usr/bin/env python3
"""
Download and Install FFmpeg for Windows
Automatically sets up FFmpeg for video processing
"""

import os
import sys
import zipfile
import urllib.request
import subprocess
from pathlib import Path

print("=" * 60)
print("FFMPEG INSTALLER FOR WINDOWS")
print("=" * 60)

def download_ffmpeg():
    """Download FFmpeg for Windows"""

    print("\n[DOWNLOAD] Fetching FFmpeg for Windows...")

    # FFmpeg download URL (latest stable release)
    ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"

    # Alternative URL if primary fails
    backup_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"

    download_path = "ffmpeg.zip"

    try:
        print(f"  Downloading from primary source...")
        print(f"  This may take a few minutes (file is ~80MB)")

        # Download with progress
        def download_with_progress(url, path):
            def report_progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(downloaded * 100 / total_size, 100)
                mb_downloaded = downloaded / 1024 / 1024
                mb_total = total_size / 1024 / 1024
                print(f"  Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)", end='\r')

            urllib.request.urlretrieve(url, path, report_progress)
            print()  # New line after progress

        download_with_progress(ffmpeg_url, download_path)
        print("  [OK] Download complete!")
        return download_path

    except Exception as e:
        print(f"  [ERROR] Primary download failed: {e}")
        print("  [RETRY] Trying backup source...")

        try:
            download_with_progress(backup_url, download_path)
            print("  [OK] Download complete from backup!")
            return download_path
        except Exception as e2:
            print(f"  [ERROR] Backup download also failed: {e2}")
            return None

def extract_ffmpeg(zip_path):
    """Extract FFmpeg from zip file"""

    print("\n[EXTRACT] Extracting FFmpeg...")

    extract_dir = "ffmpeg_extracted"

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        print("  [OK] Extraction complete!")

        # Find the ffmpeg.exe
        for root, dirs, files in os.walk(extract_dir):
            if "ffmpeg.exe" in files:
                ffmpeg_dir = root
                print(f"  [FOUND] FFmpeg at: {ffmpeg_dir}")
                return ffmpeg_dir

        print("  [ERROR] ffmpeg.exe not found in extracted files")
        return None

    except Exception as e:
        print(f"  [ERROR] Extraction failed: {e}")
        return None

def install_ffmpeg(ffmpeg_dir):
    """Install FFmpeg to a permanent location"""

    print("\n[INSTALL] Installing FFmpeg...")

    # Create installation directory
    install_dir = Path("C:/ffmpeg")

    try:
        install_dir.mkdir(exist_ok=True)

        # Copy FFmpeg files
        import shutil

        # Find and copy executables
        for file in ["ffmpeg.exe", "ffprobe.exe", "ffplay.exe"]:
            source = Path(ffmpeg_dir) / file
            if source.exists():
                dest = install_dir / file
                shutil.copy2(source, dest)
                print(f"  [COPY] {file} -> {dest}")

        print(f"  [OK] FFmpeg installed to: {install_dir}")
        return str(install_dir)

    except PermissionError:
        # Try user directory instead
        print("  [INFO] Cannot write to C:/, using user directory...")

        user_dir = Path.home() / "ffmpeg"
        user_dir.mkdir(exist_ok=True)

        for file in ["ffmpeg.exe", "ffprobe.exe", "ffplay.exe"]:
            source = Path(ffmpeg_dir) / file
            if source.exists():
                dest = user_dir / file
                shutil.copy2(source, dest)
                print(f"  [COPY] {file} -> {dest}")

        print(f"  [OK] FFmpeg installed to: {user_dir}")
        return str(user_dir)

def add_to_path(ffmpeg_path):
    """Add FFmpeg to system PATH"""

    print("\n[PATH] Configuring system PATH...")

    try:
        # Add to current session
        current_path = os.environ.get('PATH', '')
        if ffmpeg_path not in current_path:
            os.environ['PATH'] = f"{ffmpeg_path};{current_path}"
            print(f"  [OK] Added to current session PATH")

        # Try to add permanently (Windows)
        try:
            import winreg

            # Open the environment variables key
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Environment",
                0,
                winreg.KEY_ALL_ACCESS
            )

            # Get current PATH
            current_user_path, _ = winreg.QueryValueEx(key, "PATH")

            # Add ffmpeg if not already there
            if ffmpeg_path not in current_user_path:
                new_path = f"{ffmpeg_path};{current_user_path}"
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                print(f"  [OK] Added to permanent user PATH")
                print("  [NOTE] Restart your terminal for permanent PATH changes")

            winreg.CloseKey(key)

        except Exception as e:
            print(f"  [WARNING] Could not modify permanent PATH: {e}")
            print(f"  [MANUAL] Add this to your PATH manually: {ffmpeg_path}")

        return True

    except Exception as e:
        print(f"  [ERROR] PATH configuration failed: {e}")
        return False

def test_ffmpeg():
    """Test if FFmpeg is working"""

    print("\n[TEST] Testing FFmpeg installation...")

    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            print("  [OK] FFmpeg is working!")

            # Get version
            version_line = result.stdout.split('\n')[0]
            print(f"  [VERSION] {version_line}")

            return True
        else:
            print("  [ERROR] FFmpeg not working")
            return False

    except FileNotFoundError:
        print("  [ERROR] FFmpeg not found in PATH")
        return False
    except Exception as e:
        print(f"  [ERROR] Test failed: {e}")
        return False

def cleanup():
    """Clean up temporary files"""

    print("\n[CLEANUP] Removing temporary files...")

    try:
        if os.path.exists("ffmpeg.zip"):
            os.remove("ffmpeg.zip")
            print("  [DELETE] ffmpeg.zip")

        if os.path.exists("ffmpeg_extracted"):
            import shutil
            shutil.rmtree("ffmpeg_extracted")
            print("  [DELETE] ffmpeg_extracted/")

        print("  [OK] Cleanup complete!")

    except Exception as e:
        print(f"  [WARNING] Cleanup failed: {e}")

def main():
    """Main installation process"""

    print("\n[START] Beginning FFmpeg installation...")

    # Check if already installed
    if test_ffmpeg():
        print("\n[INFO] FFmpeg is already installed and working!")
        return True

    # Download FFmpeg
    zip_path = download_ffmpeg()
    if not zip_path:
        print("\n[FAILED] Could not download FFmpeg")
        print("\n[MANUAL] Please download manually from:")
        print("  https://ffmpeg.org/download.html")
        print("  Choose 'Windows' and download the essentials build")
        return False

    # Extract FFmpeg
    ffmpeg_dir = extract_ffmpeg(zip_path)
    if not ffmpeg_dir:
        print("\n[FAILED] Could not extract FFmpeg")
        return False

    # Install FFmpeg
    install_path = install_ffmpeg(ffmpeg_dir)
    if not install_path:
        print("\n[FAILED] Could not install FFmpeg")
        return False

    # Add to PATH
    add_to_path(install_path)

    # Test installation
    success = test_ffmpeg()

    # Cleanup
    cleanup()

    if success:
        print("\n" + "=" * 60)
        print("SUCCESS! FFmpeg installed successfully!")
        print("=" * 60)
        print("\n[READY] You can now generate videos!")
        print("\n[NEXT STEPS]")
        print("  1. Run: python generate_clean_video.py")
        print("  2. Run: python generate_concept_videos.py")
        print("  3. Videos will be created with narration!")

        return True
    else:
        print("\n" + "=" * 60)
        print("PARTIAL SUCCESS - Manual step required")
        print("=" * 60)
        print(f"\n[ACTION REQUIRED]")
        print(f"  FFmpeg is installed at: {install_path}")
        print(f"  But it's not in your PATH yet")
        print(f"\n[TO FIX]")
        print(f"  1. Close and reopen your terminal")
        print(f"  2. Or manually add to PATH: {install_path}")
        print(f"  3. Then run your video generation scripts")

        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)