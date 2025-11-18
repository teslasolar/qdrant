#!/usr/bin/env python3
"""
Quick AI Video Generation - Using Lightweight Models
Generates actual animated videos with minimal setup
"""

import os
import sys
import subprocess

print("=" * 60)
print("QUICK AI VIDEO GENERATION")
print("=" * 60)

# ============================================
# Option 1: Using Replicate API (Cloud-based)
# ============================================

def setup_replicate():
    """Use Replicate for cloud-based video generation"""

    print("\n[REPLICATE] Cloud-based AI video generation")
    print("-" * 40)

    code = '''
# Install: pip install replicate

import replicate
import requests
import os

# You can get a free API token at replicate.com
# Set as environment variable: REPLICATE_API_TOKEN
os.environ["REPLICATE_API_TOKEN"] = "YOUR_TOKEN_HERE"

def generate_with_stable_video():
    """Generate video using Stable Video Diffusion on Replicate"""

    # Using Stable Video Diffusion
    output = replicate.run(
        "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
        input={
            "input_image": "https://your-image-url.jpg",
            "cond_aug": 0.02,
            "decoding_t": 7,
            "video_length": "14_frames_with_svd",
            "sizing_strategy": "maintain_aspect_ratio",
            "motion_bucket_id": 127,
            "frames_per_second": 6
        }
    )

    print(f"Video URL: {output}")
    return output

def generate_with_animatediff():
    """Generate video using AnimateDiff on Replicate"""

    output = replicate.run(
        "lucataco/animate-diff:beecf59c4aee8d81bf04f0381033dfa10dc16e845b4ae00d281e2fa377e48a9f",
        input={
            "prompt": "A doctor examining holographic medical scans in a futuristic lab",
            "n_frames": 16,
            "guidance_scale": 7.5,
            "seed": 42
        }
    )

    print(f"Video URL: {output}")
    return output

def generate_with_zeroscope():
    """Generate video using Zeroscope (fast and free tier friendly)"""

    output = replicate.run(
        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        input={
            "prompt": "Medical AI system analyzing patient data with glowing holographic displays",
            "num_frames": 24,
            "width": 1024,
            "height": 576
        }
    )

    print(f"Video URL: {output}")
    return output

# Download the video
def download_video(url, filename):
    """Download video from URL"""
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)
    print(f"Downloaded: {filename}")

if __name__ == "__main__":
    print("Generating medical AI video...")

    # Choose your model
    video_url = generate_with_zeroscope()  # Free tier friendly

    # Download result
    download_video(video_url, "medical_ai_video.mp4")
'''

    print(code)
    print("\n[INFO] Replicate offers free tier with ~1000 predictions/month")
    print("[INFO] Sign up at https://replicate.com for API token")
    return code

# ============================================
# Option 2: Using Hugging Face Spaces (Free)
# ============================================

def setup_huggingface_spaces():
    """Use Hugging Face Spaces for free video generation"""

    print("\n[HUGGING FACE] Free AI video generation via Spaces")
    print("-" * 40)

    code = '''
import requests
from gradio_client import Client
import time

def generate_with_modelscope():
    """Use ModelScope text-to-video via Hugging Face Spaces"""

    # Connect to the public Space
    client = Client("damo-vilab/modelscope-text-to-video-synthesis")

    # Generate video
    result = client.predict(
        "A futuristic medical scanner analyzing a patient's brain with holographic display",
        8,  # Number of frames
        fn_index=0
    )

    print(f"Video saved at: {result}")
    return result

def generate_with_animatediff_space():
    """Use AnimateDiff via Hugging Face Spaces"""

    client = Client("guoyww/AnimateDiff")

    result = client.predict(
        prompt="Medical robot performing surgery with AI guidance",
        n_frames=16,
        guidance_scale=7.5,
        fn_index=0
    )

    print(f"Video saved at: {result}")
    return result

if __name__ == "__main__":
    print("Generating video via Hugging Face Spaces (free)...")

    # Generate video
    video_path = generate_with_modelscope()
    print(f"Success! Video at: {video_path}")
'''

    print(code)
    print("\n[INFO] Hugging Face Spaces are free but may have queues")
    print("[INFO] No API key needed!")
    return code

# ============================================
# Option 3: Simple Local Generation (CPU OK)
# ============================================

def setup_simple_local():
    """Lightweight local video generation that works on CPU"""

    print("\n[LOCAL] Lightweight AI video generation")
    print("-" * 40)

    code = '''
import torch
import numpy as np
from PIL import Image
import cv2
import os

def install_requirements():
    """Install minimal requirements"""
    import subprocess
    packages = ["torch", "torchvision", "opencv-python", "pillow", "transformers"]

    for pkg in packages:
        subprocess.check_call(["pip", "install", pkg])

def create_morphing_video(image_paths, output_path="morph_video.mp4"):
    """Create video by morphing between images"""

    import cv2
    from PIL import Image
    import numpy as np

    frames = []
    fps = 30
    duration_per_image = 2  # seconds

    for i in range(len(image_paths) - 1):
        img1 = cv2.imread(image_paths[i])
        img2 = cv2.imread(image_paths[i + 1])

        # Resize to same size
        height, width = 512, 512
        img1 = cv2.resize(img1, (width, height))
        img2 = cv2.resize(img2, (width, height))

        # Generate morphing frames
        num_frames = fps * duration_per_image
        for frame in range(num_frames):
            alpha = frame / num_frames
            morphed = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
            frames.append(morphed)

    # Write video
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()
    print(f"Video saved: {output_path}")

def create_ken_burns_effect(image_path, output_path="ken_burns.mp4"):
    """Create video with Ken Burns effect (zoom/pan)"""

    img = cv2.imread(image_path)
    height, width = img.shape[:2]

    fps = 30
    duration = 5  # seconds
    num_frames = fps * duration

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (1280, 720))

    for i in range(num_frames):
        # Calculate zoom
        scale = 1.0 + (i / num_frames) * 0.3  # Zoom from 1.0 to 1.3

        # Calculate pan
        center_x = width // 2 + int((i / num_frames) * 100)
        center_y = height // 2

        # Apply zoom and pan
        M = cv2.getRotationMatrix2D((center_x, center_y), 0, scale)
        zoomed = cv2.warpAffine(img, M, (width, height))

        # Crop to output size
        cropped = cv2.resize(zoomed, (1280, 720))
        out.write(cropped)

    out.release()
    print(f"Video saved: {output_path}")

if __name__ == "__main__":
    print("Creating AI-enhanced videos...")

    # Create morphing video from your slides
    slides = [f"slide_{i:02d}.png" for i in range(1, 21)]
    if all(os.path.exists(s) for s in slides[:3]):
        create_morphing_video(slides[:3], "slide_morph.mp4")

    # Create Ken Burns effect
    if os.path.exists("slide_01.png"):
        create_ken_burns_effect("slide_01.png", "slide_zoom.mp4")
'''

    print(code)
    print("\n[INFO] This works on CPU - no GPU required!")
    print("[INFO] Creates smooth transitions and effects")
    return code

# ============================================
# Option 4: Quick Web Tools (No Code)
# ============================================

def show_web_tools():
    """List web-based AI video generators"""

    print("\n[WEB TOOLS] Browser-based AI video generation")
    print("-" * 40)

    tools = """
FREE AI VIDEO GENERATION TOOLS (No coding required):

1. **Runway ML** (runway.ml)
   - Gen-2: Text/Image to Video
   - Free tier: 125 credits
   - Quality: Excellent

2. **Pika Labs** (pika.art)
   - Text to Video
   - Free tier available
   - Discord-based

3. **Stable Video Diffusion Web** (clipdrop.co/stable-video)
   - Image to Video
   - Free tier available
   - By Stability AI

4. **ModelScope** (modelscope.cn/models/damo/text-to-video-synthesis)
   - Text to Video
   - Completely free
   - Hugging Face mirror available

5. **AnimateDiff Web** (huggingface.co/spaces/guoyww/AnimateDiff)
   - Text to Video
   - Free via Hugging Face
   - No signup required

6. **Kaiber AI** (kaiber.ai)
   - Audio reactive videos
   - 7-day free trial
   - Good for music videos

7. **D-ID** (d-id.com)
   - Talking avatars
   - Free trial
   - Good for presentations

HOW TO USE:
1. Go to website
2. Upload image or enter text prompt
3. Click generate
4. Download video

PROMPT SUGGESTIONS FOR MEDICAL DEMO:
- "Futuristic medical AI analyzing holographic brain scans"
- "Doctor using augmented reality to examine patient data"
- "Medical nanorobots traveling through bloodstream"
- "AI-powered surgery room with robotic assistants"
- "3D medical imaging rotating with data overlays"
"""

    print(tools)
    return tools

# ============================================
# Main Menu
# ============================================

def main():
    print("\nChoose AI Video Generation Method:\n")
    print("1. Replicate API (Cloud, needs API key)")
    print("2. Hugging Face Spaces (Free, no key)")
    print("3. Local Generation (CPU OK)")
    print("4. Web Tools (No code)")
    print("5. Install all scripts")

    choice = input("\nSelect option (1-5): ").strip()

    scripts = {}

    if choice == "1":
        scripts["replicate_video.py"] = setup_replicate()
    elif choice == "2":
        scripts["huggingface_video.py"] = setup_huggingface_spaces()
    elif choice == "3":
        scripts["local_video.py"] = setup_simple_local()
    elif choice == "4":
        show_web_tools()
    elif choice == "5":
        scripts["replicate_video.py"] = setup_replicate()
        scripts["huggingface_video.py"] = setup_huggingface_spaces()
        scripts["local_video.py"] = setup_simple_local()
        show_web_tools()

    # Save scripts
    for filename, code in scripts.items():
        with open(filename, "w") as f:
            f.write(code)
        print(f"\n[SAVED] {filename}")

    print("\n" + "=" * 60)
    print("QUICK START GUIDE")
    print("=" * 60)

    print("\nFASTEST OPTION (No coding):")
    print("1. Go to: huggingface.co/spaces/damo-vilab/modelscope-text-to-video-synthesis")
    print("2. Enter: 'Medical AI system analyzing patient data'")
    print("3. Click Generate")
    print("4. Download video")

    print("\nLOCAL OPTION (Works now):")
    print("1. Run: python local_video.py")
    print("2. Uses your existing slide images")
    print("3. Creates smooth animations")

    print("\nCLOUD OPTION (Best quality):")
    print("1. Sign up at replicate.com (free)")
    print("2. Get API token")
    print("3. Run: python replicate_video.py")

if __name__ == "__main__":
    main()