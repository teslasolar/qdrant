#!/usr/bin/env python3
"""
Chunked AI Video Generation - 36 segments for 3-minute video
Each chunk is 5 seconds, generated separately then combined
"""

import os
import json
import time
from pathlib import Path

print("=" * 60)
print("CHUNKED AI VIDEO GENERATION")
print("3 minutes = 36 chunks x 5 seconds")
print("=" * 60)

# Define the 36 chunks with prompts matching the narration timeline
video_chunks = [
    # Opening (0-20s) - 4 chunks
    {"id": 1, "start": 0, "end": 5, "prompt": "Futuristic hospital entrance with glowing blue holographic medical symbols"},
    {"id": 2, "start": 5, "end": 10, "prompt": "Doctor overwhelmed by floating paper medical records in dark room"},
    {"id": 3, "start": 10, "end": 15, "prompt": "Medical professional searching through endless filing cabinets, frustrated"},
    {"id": 4, "start": 15, "end": 20, "prompt": "Clock ticking fast over pile of medical scans, time pressure visualization"},

    # Problem Deep Dive (20-40s) - 4 chunks
    {"id": 5, "start": 20, "end": 25, "prompt": "X-ray and MRI scans floating in 3D space with red warning highlights"},
    {"id": 6, "start": 25, "end": 30, "prompt": "Multiple doctors looking at same scan with different colored annotations"},
    {"id": 7, "start": 30, "end": 35, "prompt": "Patient data transforming into geometric patterns and vectors"},
    {"id": 8, "start": 35, "end": 40, "prompt": "Emergency room chaos with medical monitors showing critical alerts"},

    # Solution Introduction (40-60s) - 4 chunks
    {"id": 9, "start": 40, "end": 45, "prompt": "Glowing AI brain analyzing medical scans with blue neural connections"},
    {"id": 10, "start": 45, "end": 50, "prompt": "Holographic interface showing Qdrant vector database with medical images"},
    {"id": 11, "start": 50, "end": 55, "prompt": "Medical scan transforming into colorful vector embeddings flowing into database"},
    {"id": 12, "start": 55, "end": 60, "prompt": "Doctor using futuristic AR glasses to view similar medical cases"},

    # Demo Visualization (60-80s) - 4 chunks
    {"id": 13, "start": 60, "end": 65, "prompt": "Brain MRI scan being analyzed with glowing similarity matches appearing"},
    {"id": 14, "start": 65, "end": 70, "prompt": "Chest X-ray with AI highlighting similar patterns from database"},
    {"id": 15, "start": 70, "end": 75, "prompt": "3D medical visualization rotating with data points connecting"},
    {"id": 16, "start": 75, "end": 80, "prompt": "Dashboard interface showing real-time medical image analysis"},

    # Technical Architecture (80-100s) - 4 chunks
    {"id": 17, "start": 80, "end": 85, "prompt": "Flowchart animation showing data pipeline from scanner to vectors"},
    {"id": 18, "start": 85, "end": 90, "prompt": "Server room with glowing connections to cloud infrastructure"},
    {"id": 19, "start": 90, "end": 95, "prompt": "Code visualization showing BiomedCLIP embedding generation"},
    {"id": 20, "start": 95, "end": 100, "prompt": "Network diagram showing DICOM compliance and security layers"},

    # Benefits Showcase (100-120s) - 4 chunks
    {"id": 21, "start": 100, "end": 105, "prompt": "Doctor smiling while AI instantly finds similar cases on screen"},
    {"id": 22, "start": 105, "end": 110, "prompt": "Time-lapse of diagnosis speed improving from hours to seconds"},
    {"id": 23, "start": 110, "end": 115, "prompt": "Multiple hospitals connected through glowing network sharing knowledge"},
    {"id": 24, "start": 115, "end": 120, "prompt": "Patient outcomes improving with green upward trending graphs"},

    # Use Cases (120-140s) - 4 chunks
    {"id": 25, "start": 120, "end": 125, "prompt": "Radiologist using AI to detect subtle tumor patterns in brain scan"},
    {"id": 26, "start": 125, "end": 130, "prompt": "Emergency room using AI for rapid trauma assessment"},
    {"id": 27, "start": 130, "end": 135, "prompt": "Researcher discovering rare disease patterns through AI clustering"},
    {"id": 28, "start": 135, "end": 140, "prompt": "Training simulation with AI teaching medical students"},

    # Future Vision (140-160s) - 4 chunks
    {"id": 29, "start": 140, "end": 145, "prompt": "Futuristic medical center with holographic AI assistants"},
    {"id": 30, "start": 145, "end": 150, "prompt": "Global medical network with real-time knowledge sharing"},
    {"id": 31, "start": 150, "end": 155, "prompt": "AI predicting health issues before symptoms appear"},
    {"id": 32, "start": 155, "end": 160, "prompt": "Personalized medicine with DNA and AI working together"},

    # Call to Action (160-180s) - 4 chunks
    {"id": 33, "start": 160, "end": 165, "prompt": "Hackathon logo transforming into medical innovation symbol"},
    {"id": 34, "start": 165, "end": 170, "prompt": "GitHub repository with code flowing into medical applications"},
    {"id": 35, "start": 170, "end": 175, "prompt": "Join us message with diverse medical professionals using technology"},
    {"id": 36, "start": 175, "end": 180, "prompt": "Chazon logo with tagline about transforming medical imaging future"},
]

# Save chunk definitions
with open("video_chunks.json", "w") as f:
    json.dump(video_chunks, f, indent=2)
print(f"[SAVED] video_chunks.json - 36 segment definitions")

# Method 1: Using Replicate API (Best Quality)
def generate_with_replicate():
    """Generate chunks using Replicate API"""

    print("\n[REPLICATE] Generating 36 chunks via API")
    print("-" * 40)

    code = '''
import replicate
import requests
import os
import json

# Load chunk definitions
with open("video_chunks.json") as f:
    chunks = json.load(f)

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "YOUR_TOKEN_HERE"

def generate_chunk(chunk):
    """Generate a single 5-second chunk"""

    print(f"Generating chunk {chunk['id']}: {chunk['start']}-{chunk['end']}s")

    # Using Zeroscope for fast generation
    output = replicate.run(
        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        input={
            "prompt": chunk['prompt'] + ", high quality, cinematic, medical visualization",
            "num_frames": 120,  # 5 seconds at 24 fps
            "width": 1024,
            "height": 576,
            "guidance_scale": 7.5,
            "num_inference_steps": 25
        }
    )

    # Download the chunk
    response = requests.get(output)
    filename = f"chunk_{chunk['id']:02d}.mp4"

    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"  Saved: {filename}")
    return filename

# Generate all chunks
generated_files = []
for chunk in chunks:
    try:
        file = generate_chunk(chunk)
        generated_files.append(file)
        time.sleep(2)  # Rate limiting
    except Exception as e:
        print(f"  Error generating chunk {chunk['id']}: {e}")

print(f"Generated {len(generated_files)} chunks successfully!")
'''

    return code

# Method 2: Batch Generation with Hugging Face
def generate_with_huggingface_batch():
    """Generate chunks using Hugging Face Spaces in batches"""

    print("\n[HUGGING FACE] Batch chunk generation")
    print("-" * 40)

    code = '''
from gradio_client import Client
import json
import time
import subprocess

# Load chunk definitions
with open("video_chunks.json") as f:
    chunks = json.load(f)

def generate_batch(batch_chunks, batch_num):
    """Generate a batch of chunks"""

    print(f"\\nBatch {batch_num}: Generating {len(batch_chunks)} chunks")

    # Use ModelScope via Hugging Face
    client = Client("damo-vilab/modelscope-text-to-video-synthesis")

    generated = []
    for chunk in batch_chunks:
        try:
            print(f"  Chunk {chunk['id']}: {chunk['prompt'][:50]}...")

            result = client.predict(
                chunk['prompt'],
                8,  # frames (will interpolate later)
                fn_index=0
            )

            # Rename to numbered chunk
            output_file = f"chunk_{chunk['id']:02d}.mp4"
            subprocess.run(["cp", result, output_file])
            generated.append(output_file)

        except Exception as e:
            print(f"    Error: {e}")
            # Create placeholder
            create_placeholder(chunk['id'])

        time.sleep(5)  # Respect rate limits

    return generated

def create_placeholder(chunk_id):
    """Create a placeholder video for failed chunks"""

    # Use ffmpeg to create a 5-second black video
    cmd = [
        "ffmpeg", "-f", "lavfi", "-i",
        "color=c=black:s=1024x576:d=5",
        "-vf", f"drawtext=text='Chunk {chunk_id}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
        f"chunk_{chunk_id:02d}.mp4"
    ]
    subprocess.run(cmd)

# Process in batches of 6 (6 batches x 6 chunks = 36)
batch_size = 6
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i+batch_size]
    generate_batch(batch, i//batch_size + 1)
    print(f"  Batch complete. Waiting before next batch...")
    time.sleep(30)  # Longer wait between batches
'''

    return code

# Method 3: Local Fast Generation
def generate_local_fast():
    """Generate chunks locally using fast techniques"""

    print("\n[LOCAL] Fast chunk generation")
    print("-" * 40)

    code = '''
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

print(f"\\nGenerated all 36 chunks!")
'''

    return code

# Method 4: Combine chunks into final video
def create_combination_script():
    """Script to combine all chunks into final video"""

    print("\n[COMBINE] Script to merge chunks")
    print("-" * 40)

    code = '''
import subprocess
import os
import glob

def combine_chunks():
    """Combine all 36 chunks into final 3-minute video"""

    print("Combining 36 chunks into final video...")

    # Check for all chunks
    chunks = []
    for i in range(1, 37):
        chunk_file = f"chunk_{i:02d}.mp4"
        if os.path.exists(chunk_file):
            chunks.append(chunk_file)
        else:
            print(f"  Warning: Missing {chunk_file}")

    print(f"Found {len(chunks)} chunks")

    if len(chunks) < 36:
        print("  Creating placeholders for missing chunks...")
        create_missing_placeholders()

    # Create concat file
    with open("chunks_list.txt", "w") as f:
        for i in range(1, 37):
            f.write(f"file 'chunk_{i:02d}.mp4'\\n")

    # Combine using ffmpeg
    cmd = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", "chunks_list.txt",
        "-c", "copy",
        "chazon_ai_video_raw.mp4"
    ]

    subprocess.run(cmd)
    print("Created: chazon_ai_video_raw.mp4")

    # Add narration
    if os.path.exists("narration_3min.mp3"):
        print("Adding narration track...")
        cmd = [
            "ffmpeg",
            "-i", "chazon_ai_video_raw.mp4",
            "-i", "narration_3min.mp3",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            "chazon_ai_video_final.mp4"
        ]
        subprocess.run(cmd)
        print("Created: chazon_ai_video_final.mp4")

    print("\\nVideo assembly complete!")
    print("Final video: chazon_ai_video_final.mp4")

def create_missing_placeholders():
    """Create placeholder videos for any missing chunks"""

    for i in range(1, 37):
        chunk_file = f"chunk_{i:02d}.mp4"
        if not os.path.exists(chunk_file):
            print(f"  Creating placeholder for chunk {i}")

            # Create 5-second placeholder
            cmd = [
                "ffmpeg", "-f", "lavfi",
                "-i", f"color=c=darkblue:s=1024x576:d=5:r=24",
                "-vf", f"drawtext=text='Segment {i}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
                "-pix_fmt", "yuv420p",
                chunk_file
            ]
            subprocess.run(cmd, capture_output=True)

if __name__ == "__main__":
    combine_chunks()
'''

    return code

# Save all generation scripts
def save_all_scripts():
    """Save all chunk generation scripts"""

    scripts = {
        "generate_chunks_replicate.py": generate_with_replicate(),
        "generate_chunks_huggingface.py": generate_with_huggingface_batch(),
        "generate_chunks_local.py": generate_local_fast(),
        "combine_chunks.py": create_combination_script()
    }

    for filename, code in scripts.items():
        with open(filename, "w") as f:
            f.write(code)
        print(f"[SAVED] {filename}")

    return scripts

# Main execution
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("CHUNK-BASED VIDEO GENERATION PLAN")
    print("=" * 60)

    print("\n36 CHUNKS BREAKDOWN:")
    print("- Chunks 1-4:   Opening & Problem (0-20s)")
    print("- Chunks 5-8:   Problem Deep Dive (20-40s)")
    print("- Chunks 9-12:  Solution Introduction (40-60s)")
    print("- Chunks 13-16: Demo Visualization (60-80s)")
    print("- Chunks 17-20: Technical Architecture (80-100s)")
    print("- Chunks 21-24: Benefits Showcase (100-120s)")
    print("- Chunks 25-28: Use Cases (120-140s)")
    print("- Chunks 29-32: Future Vision (140-160s)")
    print("- Chunks 33-36: Call to Action (160-180s)")

    print("\n[GENERATION METHODS:]")
    print("1. Replicate API - Best quality, needs API key")
    print("2. Hugging Face - Free, may have queues")
    print("3. Local Fast - Works on CPU, basic animations")

    # Save all scripts
    save_all_scripts()

    print("\n" + "=" * 60)
    print("QUICK START INSTRUCTIONS")
    print("=" * 60)

    print("\nFASTEST (Local animations):")
    print("1. Run: python generate_chunks_local.py")
    print("2. Run: python combine_chunks.py")
    print("3. Get: chazon_ai_video_final.mp4")

    print("\nBEST QUALITY (Replicate):")
    print("1. Get API key from replicate.com")
    print("2. Run: python generate_chunks_replicate.py")
    print("3. Run: python combine_chunks.py")

    print("\nFREE CLOUD (Hugging Face):")
    print("1. Run: python generate_chunks_huggingface.py")
    print("2. Wait for processing (may take time)")
    print("3. Run: python combine_chunks.py")

    print("\n[TIP] Generate chunks in parallel:")
    print("- Run multiple instances with different chunk ranges")
    print("- Edit scripts to process chunks 1-12, 13-24, 25-36 separately")
    print("- Combine all at the end")

    print("\n[Ready] All scripts saved. Start with local generation for quick test!")