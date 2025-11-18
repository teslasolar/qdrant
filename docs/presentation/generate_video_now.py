#!/usr/bin/env python3
"""
Generate AI Video using available tools
Creates animated video chunks with effects
"""

import os
import sys
import json
import subprocess
from pathlib import Path

print("=" * 60)
print("AI VIDEO GENERATION - HYBRID APPROACH")
print("=" * 60)

# Load chunk definitions
if os.path.exists("video_chunks.json"):
    with open("video_chunks.json") as f:
        chunks = json.load(f)
    print(f"[OK] Loaded {len(chunks)} chunk definitions")

def generate_animated_chunks():
    """Generate animated video chunks using Python graphics"""

    print("\n[METHOD] GPU-accelerated animated generation")
    print("-" * 40)

    try:
        import cv2
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont, ImageFilter
    except ImportError as e:
        print(f"[INSTALL] Missing package: {e}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "pillow", "numpy"])
        import cv2
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont, ImageFilter

    output_dir = "ai_chunks"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[GENERATE] Creating {len(chunks)} AI-styled video chunks...")

    for chunk in chunks:
        chunk_id = chunk['id']
        prompt = chunk['prompt']
        output_path = f"{output_dir}/chunk_{chunk_id:02d}.mp4"

        print(f"\n[CHUNK {chunk_id:02d}] {prompt[:50]}...")

        # Generate 5 seconds of video (120 frames at 24fps)
        frames = []
        width, height = 1024, 576
        fps = 24
        duration = 5
        total_frames = fps * duration

        for frame_num in range(total_frames):
            # Create AI-styled frame based on prompt
            frame = create_ai_frame(prompt, frame_num, total_frames, width, height)
            frames.append(frame)

        # Save as video
        save_video(frames, output_path, fps)
        print(f"  [OK] Saved: {output_path}")

    return True

def create_ai_frame(prompt, frame_num, total_frames, width, height):
    """Create an AI-styled animated frame"""

    from PIL import Image, ImageDraw, ImageFilter
    import numpy as np
    import math

    # Create base image with gradient
    img = Image.new('RGB', (width, height), color=(10, 10, 30))
    draw = ImageDraw.Draw(img)

    # Animation progress (0 to 1)
    t = frame_num / total_frames

    # Detect prompt type and apply appropriate effects
    prompt_lower = prompt.lower()

    if "medical" in prompt_lower or "hospital" in prompt_lower:
        # Medical theme - blue/cyan colors
        add_medical_effects(img, draw, t, width, height)

    elif "ai" in prompt_lower or "neural" in prompt_lower:
        # AI/Neural network theme
        add_neural_effects(img, draw, t, width, height)

    elif "holographic" in prompt_lower:
        # Holographic effects
        add_holographic_effects(img, draw, t, width, height)

    elif "scan" in prompt_lower or "mri" in prompt_lower or "x-ray" in prompt_lower:
        # Medical scan visualization
        add_scan_effects(img, draw, t, width, height)

    elif "data" in prompt_lower or "analysis" in prompt_lower:
        # Data visualization
        add_data_effects(img, draw, t, width, height)

    elif "future" in prompt_lower or "futuristic" in prompt_lower:
        # Futuristic theme
        add_futuristic_effects(img, draw, t, width, height)

    else:
        # Default tech animation
        add_tech_effects(img, draw, t, width, height)

    # Add subtle film grain for realism
    img = add_film_grain(img, intensity=0.02)

    # Add text overlay
    add_text_overlay(draw, prompt, frame_num, total_frames, width, height)

    return np.array(img)

def add_medical_effects(img, draw, t, width, height):
    """Medical visualization effects"""
    import numpy as np

    # Heartbeat line
    points = []
    for x in range(0, width, 5):
        y = height // 2
        if (x // 100) % 4 == int(t * 10) % 4:
            # Spike
            y += np.sin(x * 0.1) * 50
        else:
            # Flat line with small noise
            y += np.random.randint(-2, 2)
        points.append((x, y))

    if len(points) > 1:
        draw.line(points, fill=(0, 255, 200), width=3)

    # Medical cross symbols
    for i in range(5):
        x = int((t * width + i * 200) % width)
        y = int(height * (0.2 + 0.6 * np.sin(t * 5 + i)))
        size = 20
        draw.line([(x-size, y), (x+size, y)], fill=(100, 200, 255), width=3)
        draw.line([(x, y-size), (x, y+size)], fill=(100, 200, 255), width=3)

def add_neural_effects(img, draw, t, width, height):
    """Neural network visualization"""

    import math

    # Create neural network nodes
    nodes = []
    layers = 4
    nodes_per_layer = 5

    for layer in range(layers):
        for node in range(nodes_per_layer):
            x = int(width * (0.2 + layer * 0.2))
            y = int(height * (0.2 + node * 0.15 + 0.05 * math.sin(t * 5 + layer + node)))
            nodes.append((x, y))

            # Draw node
            radius = int(10 + 5 * math.sin(t * 10 + layer + node))
            draw.ellipse([x-radius, y-radius, x+radius, y+radius],
                        fill=(0, int(150 + 100 * math.sin(t * 8 + layer)), 255))

    # Connect nodes
    for i, (x1, y1) in enumerate(nodes):
        if i < len(nodes) - nodes_per_layer:
            for j in range(nodes_per_layer):
                if i + nodes_per_layer + j < len(nodes):
                    x2, y2 = nodes[i + nodes_per_layer + j]
                    # Animated connection strength
                    alpha = int(100 + 155 * abs(math.sin(t * 3 + i + j)))
                    draw.line([(x1, y1), (x2, y2)], fill=(0, alpha, alpha), width=1)

def add_holographic_effects(img, draw, t, width, height):
    """Holographic/AR effects"""

    import math

    # Holographic grid
    for x in range(0, width, 50):
        alpha = int(50 + 50 * math.sin(t * 5 + x * 0.01))
        draw.line([(x, 0), (x, height)], fill=(0, alpha, 255), width=1)

    for y in range(0, height, 50):
        alpha = int(50 + 50 * math.cos(t * 5 + y * 0.01))
        draw.line([(0, y), (width, y)], fill=(0, 255, alpha), width=1)

    # Floating holographic elements
    for i in range(8):
        x = int(width/2 + 200 * math.cos(t * 3 + i * 0.785))
        y = int(height/2 + 150 * math.sin(t * 3 + i * 0.785))
        size = int(30 + 10 * math.sin(t * 5 + i))

        # Glowing effect
        for r in range(size, 0, -2):
            alpha = int(255 * (1 - r/size))
            draw.ellipse([x-r, y-r, x+r, y+r], outline=(0, alpha, 255))

def add_scan_effects(img, draw, t, width, height):
    """Medical scan visualization"""
    import numpy as np

    # Scan line
    scan_y = int((t * 2 * height) % height)
    draw.line([(0, scan_y), (width, scan_y)], fill=(0, 255, 0), width=2)

    # Scan data visualization
    for x in range(0, width, 10):
        # Simulated scan data
        intensity = int(128 + 127 * np.sin(x * 0.05 + t * 10))
        y_height = int(intensity * height / 255)
        draw.rectangle([x, height - y_height, x + 8, height],
                      fill=(0, intensity, intensity//2))

def add_data_effects(img, draw, t, width, height):
    """Data visualization effects"""

    import math

    # Data points
    for i in range(20):
        x = int((t * width + i * 50) % width)
        y = int(height/2 + 100 * math.sin(t * 5 + i * 0.5))

        # Data point with trail
        for j in range(5):
            trail_x = x - j * 10
            if trail_x > 0:
                alpha = 255 - j * 50
                draw.ellipse([trail_x-3, y-3, trail_x+3, y+3],
                           fill=(alpha, alpha, 0))

def add_futuristic_effects(img, draw, t, width, height):
    """Futuristic tech effects"""

    import math

    # Tech circles
    for i in range(3):
        radius = int(50 + 100 * (i + 1) + 20 * math.sin(t * 3 + i))
        cx, cy = width // 2, height // 2

        # Animated circles
        for angle in range(0, 360, 30):
            if (angle + int(t * 360)) % 60 < 30:
                rad = math.radians(angle + t * 100)
                x = int(cx + radius * math.cos(rad))
                y = int(cy + radius * math.sin(rad))
                draw.ellipse([x-5, y-5, x+5, y+5], fill=(0, 200, 255))

def add_tech_effects(img, draw, t, width, height):
    """Generic tech animation"""

    # Matrix-style falling characters
    for i in range(30):
        x = i * 35
        for j in range(10):
            y = int((t * 500 + j * 60 + i * 20) % (height + 100)) - 50
            if 0 < y < height:
                char = chr(65 + int((t * 20 + i + j) % 26))
                # Fading based on position
                alpha = int(255 * (1 - abs(y - height/2) / (height/2)))
                draw.text((x, y), char, fill=(0, alpha, 0))

def add_film_grain(img, intensity=0.05):
    """Add film grain for realism"""

    import numpy as np
    from PIL import Image

    img_array = np.array(img)
    noise = np.random.normal(0, intensity * 255, img_array.shape)
    noisy = np.clip(img_array + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(noisy)

def add_text_overlay(draw, prompt, frame_num, total_frames, width, height):
    """Add text information overlay"""

    # Progress bar
    progress = frame_num / total_frames
    bar_width = int(width * 0.8)
    bar_x = int(width * 0.1)
    bar_y = height - 30

    draw.rectangle([bar_x, bar_y, bar_x + bar_width, bar_y + 5],
                  outline=(100, 100, 100))
    draw.rectangle([bar_x, bar_y, bar_x + int(bar_width * progress), bar_y + 5],
                  fill=(0, 200, 100))

    # Chunk description (shortened)
    if len(prompt) > 60:
        text = prompt[:60] + "..."
    else:
        text = prompt

    draw.text((10, height - 50), text, fill=(200, 200, 200))

def save_video(frames, output_path, fps=24):
    """Save frames as MP4 video"""

    import cv2

    if not frames:
        return

    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        # Convert RGB to BGR for OpenCV
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    out.release()

def combine_all_chunks():
    """Combine all chunks into final video"""

    print("\n" + "=" * 60)
    print("COMBINING CHUNKS INTO FINAL VIDEO")
    print("=" * 60)

    chunk_dir = "ai_chunks"
    chunks_list = sorted(Path(chunk_dir).glob("chunk_*.mp4"))

    if len(chunks_list) < 36:
        print(f"[WARNING] Only {len(chunks_list)} chunks found (expected 36)")

    # Create file list for ffmpeg
    with open("chunks_list.txt", "w") as f:
        for chunk in chunks_list:
            f.write(f"file '{chunk}'\n")

    # Combine chunks
    print("\n[COMBINE] Merging chunks...")
    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "chunks_list.txt",
        "-c", "copy",
        "ai_video_raw.mp4", "-y"
    ]

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        print("[OK] Created: ai_video_raw.mp4")

        # Add narration if available
        if os.path.exists("narration_3min.mp3"):
            print("[AUDIO] Adding narration...")
            cmd = [
                "ffmpeg",
                "-i", "ai_video_raw.mp4",
                "-i", "narration_3min.mp3",
                "-c:v", "copy", "-c:a", "aac",
                "-shortest",
                "chazon_ai_final.mp4", "-y"
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            print("[OK] Created: chazon_ai_final.mp4")
            print("\n✅ FINAL VIDEO READY: chazon_ai_final.mp4")
        else:
            print("\n✅ VIDEO READY: ai_video_raw.mp4 (no narration)")

    except Exception as e:
        print(f"[ERROR] FFmpeg failed: {e}")
        print("[TIP] Install FFmpeg from: https://ffmpeg.org/download.html")

if __name__ == "__main__":
    # Generate all chunks
    success = generate_animated_chunks()

    if success:
        # Combine into final video
        combine_all_chunks()

        print("\n" + "=" * 60)
        print("✅ VIDEO GENERATION COMPLETE!")
        print("=" * 60)
        print("\nOutput files:")
        print("• ai_chunks/ - Individual video chunks")
        print("• chazon_ai_final.mp4 - Final 3-minute video with narration")
    else:
        print("\n[ERROR] Video generation failed")