#!/usr/bin/env python3
"""
Generate a single test chunk to demonstrate the system works
"""

import numpy as np
import json
from PIL import Image, ImageDraw, ImageFont
import os

print("[TEST] Generating sample chunk #1...")

# Load chunk definition
with open("video_chunks.json") as f:
    chunks = json.load(f)
    chunk = chunks[0]  # First chunk

print(f"Prompt: {chunk['prompt']}")

# Create animated frames
width, height = 1024, 576
num_frames = 120  # 5 seconds at 24 fps

# Create frames directory
os.makedirs("test_frames", exist_ok=True)

for frame_num in range(num_frames):
    # Create frame with animated elements
    img = Image.new('RGB', (width, height), color=(10, 10, 30))
    draw = ImageDraw.Draw(img)

    # Animated hospital entrance
    t = frame_num / num_frames

    # Glowing blue holographic effect
    for i in range(5):
        x = width // 2 + int(200 * np.cos(t * 6.28 + i))
        y = height // 2 + int(200 * np.sin(t * 6.28 + i))
        radius = 20 + int(10 * np.sin(t * 10 + i))

        # Blue glow
        for r in range(radius, 0, -2):
            alpha = int(255 * (1 - r/radius))
            draw.ellipse([x-r, y-r, x+r, y+r],
                        fill=(0, alpha//2, alpha))

    # Medical symbols
    symbols = ['✚', '⚕', '♥', 'Rx', 'DNA']
    for i, symbol in enumerate(symbols):
        x = int(width * (0.1 + 0.8 * ((t * 2 + i/5) % 1)))
        y = height // 3 + int(50 * np.sin(t * 10 + i))

        # Draw symbol (using text as placeholder)
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        draw.text((x, y), symbol, fill=(100, 200, 255), font=font)

    # Title text
    draw.text((width//2 - 200, height - 100),
              "CHAZON MEDICAL AI",
              fill=(255, 255, 255), font=font)

    draw.text((10, 10),
              f"Chunk #1 | Frame {frame_num+1}/120",
              fill=(150, 150, 150))

    # Save frame
    img.save(f"test_frames/frame_{frame_num:03d}.png")

print(f"[OK] Generated {num_frames} frames")

# Create video using ffmpeg
print("[VIDEO] Creating test chunk video...")

# Windows-compatible ffmpeg command
import subprocess

cmd = [
    "ffmpeg", "-y",
    "-framerate", "24",
    "-i", "test_frames/frame_%03d.png",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "test_chunk_01.mp4"
]

try:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("[SUCCESS] Created test_chunk_01.mp4")
        print("This is what chunk #1 of your 36-chunk video looks like!")
    else:
        print(f"[ERROR] ffmpeg failed: {result.stderr}")
        print("\nBut frames were generated successfully in test_frames/")
except Exception as e:
    print(f"[INFO] ffmpeg not found: {e}")
    print("Frames saved in test_frames/ - install ffmpeg to create video")

print("\n" + "="*50)
print("NEXT STEPS:")
print("1. Run: python generate_chunks_local.py")
print("   (Generates all 36 chunks with different animations)")
print("2. Run: python combine_chunks.py")
print("   (Combines chunks + adds your 3-minute narration)")
print("3. Result: chazon_ai_video_final.mp4")
print("="*50)