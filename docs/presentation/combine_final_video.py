#!/usr/bin/env python3
"""
Combine all 36 chunks into final 3-minute video
Works without FFmpeg using Python libraries
"""

import os
import sys
import subprocess
from pathlib import Path

print("=" * 60)
print("FINAL VIDEO ASSEMBLY")
print("=" * 60)

# Check for chunks
chunk_dir = Path("ai_chunks")
chunks = sorted(chunk_dir.glob("chunk_*.mp4"))

print(f"\n[FOUND] {len(chunks)} video chunks")

if len(chunks) != 36:
    print(f"[WARNING] Expected 36 chunks, found {len(chunks)}")

# Method 1: Try FFmpeg first
def combine_with_ffmpeg():
    """Combine using FFmpeg"""
    print("\n[METHOD 1] Trying FFmpeg...")

    # Create concat file
    with open("chunks_list.txt", "w") as f:
        for chunk in chunks:
            f.write(f"file '{chunk.absolute()}'\n")

    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "chunks_list.txt",
        "-c", "copy",
        "chazon_video_no_audio.mp4", "-y"
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("[OK] Video combined with FFmpeg")

        # Add narration
        if os.path.exists("narration_3min.mp3"):
            print("[AUDIO] Adding narration...")
            cmd2 = [
                "ffmpeg",
                "-i", "chazon_video_no_audio.mp4",
                "-i", "narration_3min.mp3",
                "-c:v", "copy", "-c:a", "aac",
                "-map", "0:v:0", "-map", "1:a:0",
                "-shortest",
                "chazon_ai_final.mp4", "-y"
            ]
            subprocess.run(cmd2, check=True, capture_output=True)
            print("[SUCCESS] Created chazon_ai_final.mp4 with narration!")
        else:
            print("[SUCCESS] Created chazon_video_no_audio.mp4")

        return True
    except:
        print("[FAILED] FFmpeg not available")
        return False

# Method 2: Use Python moviepy
def combine_with_moviepy():
    """Combine using moviepy"""
    print("\n[METHOD 2] Using MoviePy...")

    try:
        from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

        print("[LOADING] Loading video chunks...")
        clips = []
        for i, chunk in enumerate(chunks, 1):
            print(f"  Loading chunk {i:02d}/{len(chunks)}")
            clip = VideoFileClip(str(chunk))
            clips.append(clip)

        print("[COMBINE] Concatenating clips...")
        final_video = concatenate_videoclips(clips, method="compose")

        # Add audio if available
        if os.path.exists("narration_3min.mp3"):
            print("[AUDIO] Adding narration...")
            audio = AudioFileClip("narration_3min.mp3")
            final_video = final_video.set_audio(audio)

        print("[EXPORT] Saving final video (this may take a few minutes)...")
        final_video.write_videofile(
            "chazon_ai_final.mp4",
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )

        print("[SUCCESS] Created chazon_ai_final.mp4!")
        return True

    except ImportError:
        print("[INSTALL] MoviePy not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "moviepy"])
        return combine_with_moviepy()
    except Exception as e:
        print(f"[ERROR] MoviePy failed: {e}")
        return False

# Method 3: Use OpenCV
def combine_with_opencv():
    """Combine using OpenCV"""
    print("\n[METHOD 3] Using OpenCV...")

    try:
        import cv2
        import numpy as np

        # Get video properties from first chunk
        cap = cv2.VideoCapture(str(chunks[0]))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()

        print(f"[INFO] Video properties: {width}x{height} @ {fps}fps")

        # Create output video
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('chazon_video_no_audio.mp4', fourcc, fps, (width, height))

        # Write all chunks
        for i, chunk in enumerate(chunks, 1):
            print(f"  Processing chunk {i:02d}/{len(chunks)}")
            cap = cv2.VideoCapture(str(chunk))

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)

            cap.release()

        out.release()
        print("[SUCCESS] Created chazon_video_no_audio.mp4")
        print("[NOTE] Add narration manually with video editor")
        return True

    except ImportError:
        print("[INSTALL] OpenCV not found, installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
        return combine_with_opencv()
    except Exception as e:
        print(f"[ERROR] OpenCV failed: {e}")
        return False

# Try all methods
success = False

# Try FFmpeg first (fastest)
if not success:
    success = combine_with_ffmpeg()

# Try MoviePy (has audio support)
if not success:
    success = combine_with_moviepy()

# Try OpenCV (fallback, no audio)
if not success:
    success = combine_with_opencv()

if success:
    print("\n" + "=" * 60)
    print("VIDEO CREATION COMPLETE!")
    print("=" * 60)
    print("\n[OUTPUT FILES]")

    if os.path.exists("chazon_ai_final.mp4"):
        size_mb = os.path.getsize("chazon_ai_final.mp4") / (1024*1024)
        print(f"  chazon_ai_final.mp4 ({size_mb:.1f} MB)")
        print("  - 3 minute AI-generated video")
        print("  - With narration")
        print("  - Ready for submission!")
    elif os.path.exists("chazon_video_no_audio.mp4"):
        size_mb = os.path.getsize("chazon_video_no_audio.mp4") / (1024*1024)
        print(f"  chazon_video_no_audio.mp4 ({size_mb:.1f} MB)")
        print("  - 3 minute AI-generated video")
        print("  - No audio (add narration_3min.mp3 manually)")

    print("\n[NEXT STEPS]")
    print("1. Review the final video")
    print("2. Upload to YouTube as unlisted")
    print("3. Add link to hackathon submission")
else:
    print("\n[MANUAL COMBINE REQUIRED]")
    print("All 36 chunks are in ai_chunks/ folder")
    print("Use any video editor to combine them")
    print("Add narration_3min.mp3 as audio track")