
import json
import subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

# Load chunk definitions
with open("video_chunks.json") as f:
    chunks = json.load(f)

def generate_animated_chunk(chunk):
    """Generate animated chunk using OpenCV effects"""

    print(f"Generating chunk {chunk['id']}: {chunk['start']}-{chunk['end']}s")

    # Create frames for the chunk
    fps = 24
    duration = 5
    num_frames = fps * duration

    # Create base visualization
    width, height = 1024, 576

    # Output file
    output = f"chunk_{chunk['id']:02d}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output, fourcc, fps, (width, height))

    # Generate frames based on chunk theme
    for frame_num in range(num_frames):
        # Create frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)

        # Add animated elements based on prompt keywords
        if "AI" in chunk['prompt'] or "neural" in chunk['prompt']:
            # Neural network animation
            add_neural_network(frame, frame_num)
        elif "scan" in chunk['prompt'] or "MRI" in chunk['prompt']:
            # Medical scan animation
            add_scan_animation(frame, frame_num)
        elif "holographic" in chunk['prompt']:
            # Holographic effect
            add_holographic(frame, frame_num)
        else:
            # Default tech animation
            add_tech_animation(frame, frame_num)

        # Add text overlay
        add_text_overlay(frame, chunk['prompt'], chunk['id'])

        video.write(frame)

    video.release()
    print(f"  Saved: {output}")
    return output

def add_neural_network(frame, t):
    """Add neural network visualization"""
    h, w = frame.shape[:2]

    # Draw nodes
    num_nodes = 10
    for i in range(num_nodes):
        x = int(w * (0.2 + 0.6 * np.sin(t/10 + i)))
        y = int(h * (0.2 + 0.6 * np.cos(t/10 + i)))
        cv2.circle(frame, (x, y), 5, (0, 200, 255), -1)

        # Draw connections
        if i > 0:
            x2 = int(w * (0.2 + 0.6 * np.sin(t/10 + i-1)))
            y2 = int(h * (0.2 + 0.6 * np.cos(t/10 + i-1)))
            cv2.line(frame, (x, y), (x2, y2), (0, 100, 200), 1)

def add_scan_animation(frame, t):
    """Add medical scan animation"""
    h, w = frame.shape[:2]

    # Scanning line
    scan_pos = int((t % 24) * w / 24)
    cv2.line(frame, (scan_pos, 0), (scan_pos, h), (0, 255, 0), 2)

    # Grid
    for i in range(0, w, 50):
        cv2.line(frame, (i, 0), (i, h), (50, 50, 50), 1)
    for i in range(0, h, 50):
        cv2.line(frame, (0, i), (w, i), (50, 50, 50), 1)

def add_holographic(frame, t):
    """Add holographic effect"""
    h, w = frame.shape[:2]

    # Holographic layers
    for layer in range(3):
        offset = layer * 20
        color = [(0, 100, 255), (0, 255, 100), (255, 100, 0)][layer]

        points = []
        for i in range(10):
            x = int(w/2 + 200 * np.cos(t/10 + i * 0.628 + offset))
            y = int(h/2 + 200 * np.sin(t/10 + i * 0.628 + offset))
            points.append([x, y])

        points = np.array(points, np.int32)
        cv2.polylines(frame, [points], True, color, 2)

def add_tech_animation(frame, t):
    """Add generic tech animation"""
    h, w = frame.shape[:2]

    # Matrix rain effect
    for i in range(20):
        x = (i * 50 + int(t * 5)) % w
        for j in range(10):
            y = (j * 60 + int(t * 10)) % h
            char = chr(65 + (t + i + j) % 26)
            cv2.putText(frame, char, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                       0.5, (0, 255, 0), 1)

def add_text_overlay(frame, text, chunk_id):
    """Add text description"""
    h, w = frame.shape[:2]

    # Chunk number
    cv2.putText(frame, f"#{chunk_id:02d}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Description (truncated)
    short_text = text[:60] + "..." if len(text) > 60 else text
    cv2.putText(frame, short_text, (10, h-10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)

# Generate all chunks
for chunk in chunks:
    generate_animated_chunk(chunk)

print(f"\nGenerated all 36 chunks!")
