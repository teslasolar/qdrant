#!/usr/bin/env python3
"""
Combine video chunks using imageio_ffmpeg
Alternative to waiting for full FFmpeg installation
"""

import os
import sys
import imageio_ffmpeg as ffmpeg

print("=" * 60)
print("VIDEO COMBINATION USING IMAGEIO-FFMPEG")
print("=" * 60)

# Get ffmpeg executable from imageio
ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
print(f"\n[FOUND] FFmpeg at: {ffmpeg_exe}")

def combine_chunks_with_audio(output_name, narration_file):
    """Combine video chunks with narration"""

    print(f"\n[COMBINING] {output_name}")
    print(f"  Narration: {narration_file}")

    # Create file list
    chunks_list = f"chunks_list_{output_name}.txt"
    with open(chunks_list, "w") as f:
        for i in range(1, 37):
            chunk_path = os.path.abspath(f"ai_chunks/chunk_{i:02d}.mp4")
            if os.path.exists(chunk_path):
                f.write(f"file '{chunk_path}'\n")

    # Combine chunks first
    temp_video = f"temp_{output_name}_silent.mp4"
    cmd1 = [
        ffmpeg_exe,
        "-f", "concat",
        "-safe", "0",
        "-i", chunks_list,
        "-c", "copy",
        temp_video, "-y"
    ]

    print("  [1/2] Combining video chunks...")
    import subprocess
    result = subprocess.run(cmd1, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [ERROR] Failed to combine chunks: {result.stderr}")
        return False

    # Add narration if it exists
    if os.path.exists(narration_file):
        final_video = f"{output_name}.mp4"
        cmd2 = [
            ffmpeg_exe,
            "-i", temp_video,
            "-i", narration_file,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            final_video, "-y"
        ]

        print("  [2/2] Adding narration...")
        result = subprocess.run(cmd2, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  [ERROR] Failed to add audio: {result.stderr}")
            # Keep silent version
            os.rename(temp_video, final_video)
            print(f"  [OK] Created silent version: {final_video}")
        else:
            os.remove(temp_video)
            print(f"  [OK] Created with narration: {final_video}")

            # Get file size
            size_mb = os.path.getsize(final_video) / (1024*1024)
            print(f"  [SIZE] {size_mb:.1f} MB")
    else:
        # No narration, just rename
        final_video = f"{output_name}.mp4"
        os.rename(temp_video, final_video)
        print(f"  [OK] Created silent video: {final_video}")

    # Clean up
    if os.path.exists(chunks_list):
        os.remove(chunks_list)

    return True

# Main combinations to create
videos_to_create = [
    ("chazon_clean_3min", "narration_clean_3min.mp3"),
    ("chazon_concept_30s", "concept_30s_narration.mp3"),
    ("chazon_concept_60s", "concept_60s_narration.mp3"),
    ("chazon_concept_90s", "concept_90s_tech_narration.mp3"),
    ("chazon_concept_2min", "concept_2min_full_narration.mp3"),
]

print("\n[CREATING] Multiple concept videos...")

successful = []
failed = []

for video_name, narration_file in videos_to_create:
    if combine_chunks_with_audio(video_name, narration_file):
        successful.append(video_name)
    else:
        failed.append(video_name)

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if successful:
    print(f"\n[SUCCESS] Created {len(successful)} videos:")
    for video in successful:
        if os.path.exists(f"{video}.mp4"):
            size_mb = os.path.getsize(f"{video}.mp4") / (1024*1024)
            print(f"  - {video}.mp4 ({size_mb:.1f} MB)")

if failed:
    print(f"\n[FAILED] Could not create {len(failed)} videos:")
    for video in failed:
        print(f"  - {video}")

print("\n[NEXT STEPS]")
print("1. Review the generated videos")
print("2. Choose the best version for hackathon submission")
print("3. Upload to YouTube as unlisted")
print("4. Submit to lablab.ai Qdrant Challenge")