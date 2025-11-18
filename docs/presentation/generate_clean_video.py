#!/usr/bin/env python3
"""
Generate Clean 3-Minute Concept Video
Pure prototype demonstration - no testing claims
"""

import os
import subprocess
import sys

print("=" * 60)
print("CLEAN CONCEPT VIDEO GENERATOR")
print("3-Minute Prototype Demonstration")
print("=" * 60)

def generate_narration():
    """Generate clean narration without testing claims"""

    print("\n[NARRATION] Generating clean concept narration...")

    # Read the clean script
    with open("narration_clean_3min.txt", "r", encoding="utf-8") as f:
        text = f.read()

    # Extract just the narration (no timestamps or comments)
    lines = []
    for line in text.split('\n'):
        if line.strip() and not line.startswith('#') and not line.startswith('['):
            lines.append(line.strip())

    clean_text = ' '.join(lines)

    # Generate using Edge TTS
    try:
        import edge_tts
        import asyncio

        async def generate():
            # Use professional voice
            communicate = edge_tts.Communicate(
                clean_text,
                'en-US-AriaNeural',  # Clear, professional female voice
                rate='-5%',  # Slightly slower for clarity
                pitch='+0Hz'
            )
            await communicate.save("narration_clean_3min.mp3")

        asyncio.run(generate())
        print("  [OK] Generated: narration_clean_3min.mp3")
        return True

    except ImportError:
        print("  [INSTALL] Installing edge-tts...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
        return generate_narration()

def combine_with_video():
    """Combine narration with existing video chunks"""

    print("\n[COMBINE] Creating clean concept video...")

    # Use existing 36 chunks
    chunks_dir = "ai_chunks"

    if not os.path.exists(chunks_dir):
        print("  [ERROR] No video chunks found. Run generate_video_now.py first")
        return False

    # Create chunks list
    with open("chunks_clean_list.txt", "w") as f:
        for i in range(1, 37):
            chunk_path = f"{chunks_dir}/chunk_{i:02d}.mp4"
            if os.path.exists(chunk_path):
                f.write(f"file '{os.path.abspath(chunk_path)}'\n")

    # Combine chunks
    cmd1 = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "chunks_clean_list.txt",
        "-c", "copy",
        "video_clean_silent.mp4", "-y"
    ]

    try:
        subprocess.run(cmd1, check=True, capture_output=True)
        print("  [OK] Combined video chunks")

        # Add narration
        cmd2 = [
            "ffmpeg",
            "-i", "video_clean_silent.mp4",
            "-i", "narration_clean_3min.mp3",
            "-c:v", "copy",
            "-c:a", "aac",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            "chazon_clean_3min.mp4", "-y"
        ]

        subprocess.run(cmd2, check=True, capture_output=True)
        print("  [OK] Created: chazon_clean_3min.mp4")

        # Clean up
        os.remove("video_clean_silent.mp4")
        return True

    except:
        print("  [ERROR] FFmpeg issue. Trying alternative method...")
        return combine_with_moviepy()

def combine_with_moviepy():
    """Alternative using MoviePy"""

    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

        print("  [MOVIEPY] Combining with MoviePy...")

        # Load chunks
        clips = []
        for i in range(1, 37):
            chunk_path = f"ai_chunks/chunk_{i:02d}.mp4"
            if os.path.exists(chunk_path):
                clips.append(VideoFileClip(chunk_path))

        # Combine
        video = concatenate_videoclips(clips)

        # Add audio
        audio = AudioFileClip("narration_clean_3min.mp3")
        final = video.set_audio(audio)

        # Export
        final.write_videofile(
            "chazon_clean_3min.mp4",
            codec='libx264',
            audio_codec='aac'
        )

        print("  [OK] Created: chazon_clean_3min.mp4")
        return True

    except Exception as e:
        print(f"  [ERROR] MoviePy failed: {e}")
        return False

def main():
    """Generate clean concept video"""

    print("\n[INFO] This video will:")
    print("  - Present only the prototype concept")
    print("  - Focus on technical architecture")
    print("  - Avoid any testing or deployment claims")
    print("  - Be exactly 3 minutes long")

    # Generate narration
    if generate_narration():
        # Combine with video
        if combine_with_video():
            print("\n" + "=" * 60)
            print("SUCCESS! Clean concept video created!")
            print("=" * 60)

            if os.path.exists("chazon_clean_3min.mp4"):
                size_mb = os.path.getsize("chazon_clean_3min.mp4") / (1024*1024)
                print(f"\n[OUTPUT]")
                print(f"  File: chazon_clean_3min.mp4")
                print(f"  Size: {size_mb:.1f} MB")
                print(f"  Duration: 3 minutes")
                print(f"  Content: Pure prototype demonstration")

            print("\n[FEATURES]")
            print("  - No testing claims")
            print("  - No accuracy statistics")
            print("  - No hospital mentions")
            print("  - Pure technical concept")
            print("  - Hackathon prototype focus")

            print("\n[NEXT STEPS]")
            print("  1. Review the video")
            print("  2. Upload to YouTube (unlisted)")
            print("  3. Submit link to hackathon")

if __name__ == "__main__":
    main()