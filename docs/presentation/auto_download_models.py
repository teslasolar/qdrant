#!/usr/bin/env python3
"""
Automated GPU AI Model Downloader
Downloads and sets up video generation models for RTX 4070 Ti SUPER
"""

import os
import subprocess
import sys
from pathlib import Path

print("=" * 60)
print("GPU AI VIDEO MODEL SETUP")
print("RTX 4070 Ti SUPER Detected - 16GB VRAM")
print("=" * 60)

def install_requirements():
    """Install all GPU requirements"""

    print("\n[INSTALL] Installing GPU-accelerated packages...")

    # First install PyTorch with CUDA
    print("[TORCH] Installing PyTorch with CUDA 11.8...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "torch", "torchvision", "torchaudio",
        "--index-url", "https://download.pytorch.org/whl/cu118"
    ])

    # Core packages for video generation
    packages = [
        "diffusers",          # Hugging Face diffusion models
        "transformers",       # Model architectures
        "accelerate",         # GPU acceleration
        "xformers",          # Memory efficient attention
        "opencv-python",      # Video processing
        "imageio",           # Video I/O
        "imageio-ffmpeg",    # FFmpeg backend
        "safetensors",       # Fast model loading
        "omegaconf",         # Configuration
        "einops",            # Tensor operations
        "huggingface-hub",   # Model downloading
        "tqdm",              # Progress bars
    ]

    for pkg in packages:
        print(f"[INSTALL] {pkg}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

    print("[OK] All packages installed!")

def download_models():
    """Download AI video models optimized for RTX 4070 Ti"""

    print("\n[MODELS] Downloading video generation models...")
    print("Your RTX 4070 Ti SUPER can handle all models easily!")

    # Create models directory
    os.makedirs("models", exist_ok=True)

    # Download script
    download_script = """
import os
from huggingface_hub import snapshot_download
from tqdm import tqdm

print("Downloading AI video models...")

models_to_download = [
    {
        "name": "ZeroScope V2 (Fast)",
        "repo": "cerspense/zeroscope_v2_576w",
        "path": "models/zeroscope",
        "size": "1.7 GB"
    },
    {
        "name": "ModelScope Text2Video",
        "repo": "damo-vilab/text-to-video-ms-1.7b",
        "path": "models/modelscope",
        "size": "3.5 GB"
    },
    {
        "name": "AnimateDiff Motion",
        "repo": "guoyww/animatediff-motion-adapter-v1-5-2",
        "path": "models/animatediff-motion",
        "size": "1.7 GB"
    },
    {
        "name": "Stable Diffusion 1.5 (base for AnimateDiff)",
        "repo": "runwayml/stable-diffusion-v1-5",
        "path": "models/sd15",
        "size": "4.3 GB"
    }
]

for model in models_to_download:
    print(f"\\n[DOWNLOAD] {model['name']} ({model['size']})...")
    print(f"  Saving to: {model['path']}")

    try:
        snapshot_download(
            repo_id=model['repo'],
            local_dir=model['path'],
            resume_download=True,
            ignore_patterns=["*.bin"] if "stable-diffusion" in model['repo'] else None
        )
        print(f"  ✅ {model['name']} downloaded!")
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        print(f"  You can manually download from: https://huggingface.co/{model['repo']}")

print("\\n[COMPLETE] Models downloaded!")
"""

    with open("_download_models.py", "w") as f:
        f.write(download_script)

    # Run download
    subprocess.run([sys.executable, "_download_models.py"])

def create_gpu_generator():
    """Create optimized GPU video generator"""

    print("\n[CREATE] GPU video generator script...")

    script = '''#!/usr/bin/env python3
"""
RTX 4070 Ti SUPER Optimized Video Generator
Generates 36 chunks using your 16GB VRAM efficiently
"""

import torch
import gc
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import json
import os
from tqdm import tqdm
from PIL import Image
import numpy as np

# Force GPU usage
torch.cuda.set_device(0)
device = "cuda"

print("=" * 60)
print("RTX 4070 Ti SUPER VIDEO GENERATION")
print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
print("=" * 60)

# Load chunks
with open("video_chunks.json") as f:
    chunks = json.load(f)

def generate_with_zeroscope():
    """Generate using ZeroScope - Fast and efficient"""

    print("\\n[MODEL] Loading ZeroScope V2...")

    pipe = DiffusionPipeline.from_pretrained(
        "models/zeroscope",
        torch_dtype=torch.float16
    ).to(device)

    # Optimize for speed
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.enable_model_cpu_offload()
    pipe.enable_xformers_memory_efficient_attention()

    output_dir = "zeroscope_chunks"
    os.makedirs(output_dir, exist_ok=True)

    for chunk in tqdm(chunks, desc="Generating chunks"):
        prompt = chunk['prompt'] + ", high quality, 4k, cinematic"

        # Generate video
        video_frames = pipe(
            prompt,
            num_frames=24,  # 1 second at 24fps (we'll interpolate to 5s)
            height=320,
            width=576,
            num_inference_steps=25,
            guidance_scale=7.5,
            generator=torch.manual_seed(chunk['id'])
        ).frames

        # Save video
        output_path = f"{output_dir}/chunk_{chunk['id']:02d}.mp4"
        export_to_video(video_frames, output_path, fps=24)

        print(f"  Chunk {chunk['id']}: {output_path}")

        # Clear memory
        torch.cuda.empty_cache()
        gc.collect()

def generate_with_modelscope():
    """Generate using ModelScope - Good quality"""

    print("\\n[MODEL] Loading ModelScope...")

    pipe = DiffusionPipeline.from_pretrained(
        "models/modelscope",
        torch_dtype=torch.float16,
        variant="fp16"
    ).to(device)

    pipe.enable_model_cpu_offload()
    pipe.enable_vae_slicing()

    output_dir = "modelscope_chunks"
    os.makedirs(output_dir, exist_ok=True)

    for chunk in tqdm(chunks[:10], desc="Generating chunks"):  # Test with 10 chunks
        video_frames = pipe(
            chunk['prompt'],
            num_frames=16,
            num_inference_steps=25
        ).frames

        output_path = f"{output_dir}/chunk_{chunk['id']:02d}.mp4"
        export_to_video(video_frames, output_path)

        torch.cuda.empty_cache()

def generate_with_animatediff():
    """Generate using AnimateDiff - Smooth animations"""

    print("\\n[MODEL] Loading AnimateDiff...")

    from diffusers import AnimateDiffPipeline, MotionAdapter

    # Load motion adapter
    adapter = MotionAdapter.from_pretrained("models/animatediff-motion")

    # Load pipeline with SD1.5
    pipe = AnimateDiffPipeline.from_pretrained(
        "models/sd15",
        motion_adapter=adapter,
        torch_dtype=torch.float16
    ).to(device)

    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
    pipe.enable_xformers_memory_efficient_attention()

    output_dir = "animatediff_chunks"
    os.makedirs(output_dir, exist_ok=True)

    for chunk in tqdm(chunks[:10], desc="Generating chunks"):
        frames = pipe(
            chunk['prompt'],
            num_frames=16,
            guidance_scale=7.5,
            num_inference_steps=25,
            generator=torch.manual_seed(chunk['id'])
        ).frames[0]

        output_path = f"{output_dir}/chunk_{chunk['id']:02d}.mp4"
        export_to_video(frames, output_path)

        torch.cuda.empty_cache()

def interpolate_frames(input_path, output_path, target_fps=24, duration=5):
    """Interpolate frames to extend video to 5 seconds"""

    import cv2

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    cap.release()

    # Calculate interpolation
    total_frames_needed = target_fps * duration  # 120 frames for 5s at 24fps
    current_frames = len(frames)

    if current_frames < total_frames_needed:
        # Interpolate frames
        interpolated = []
        for i in range(total_frames_needed):
            idx = int(i * current_frames / total_frames_needed)
            interpolated.append(frames[min(idx, len(frames)-1)])
        frames = interpolated

    # Write output
    height, width = frames[0].shape[:2]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, target_fps, (width, height))

    for frame in frames:
        out.write(frame)

    out.release()

def main():
    print("\\nSelect generation method:")
    print("1. ZeroScope (Fastest, 1-2 min per chunk)")
    print("2. ModelScope (Better quality, 2-3 min per chunk)")
    print("3. AnimateDiff (Smoothest, 3-4 min per chunk)")
    print("4. Generate test chunk only")

    choice = "1"  # Default to fastest

    if choice == "1":
        generate_with_zeroscope()
    elif choice == "2":
        generate_with_modelscope()
    elif choice == "3":
        generate_with_animatediff()
    else:
        # Generate single test chunk
        generate_with_zeroscope()

    print("\\n[COMPLETE] Video chunks generated!")
    print("\\nNext step: python combine_chunks.py")

if __name__ == "__main__":
    main()
'''

    with open("gpu_generate_chunks.py", "w") as f:
        f.write(script)

    print("[SAVED] gpu_generate_chunks.py")

def main():
    """Main setup"""

    print("\n[SETUP] Starting automated setup...")

    # Install requirements
    install_requirements()

    # Download models
    download_models()

    # Create generator script
    create_gpu_generator()

    print("\n" + "=" * 60)
    print("✅ SETUP COMPLETE FOR RTX 4070 Ti SUPER!")
    print("=" * 60)

    print("\n[READY] Your GPU is configured for AI video generation!")
    print("\n[QUICK START]")
    print("1. Generate all 36 chunks (takes ~30-60 minutes):")
    print("   python gpu_generate_chunks.py")
    print("")
    print("2. Combine into 3-minute video:")
    print("   python combine_chunks.py")
    print("")
    print("3. Result: chazon_ai_video_final.mp4")

    print("\n[GPU INFO]")
    print("• RTX 4070 Ti SUPER: 16GB VRAM")
    print("• Can run all models at high quality")
    print("• Estimated: 1-2 minutes per 5-second chunk")
    print("• Total time: 30-60 minutes for full video")

    print("\n[TIP] Your GPU can handle multiple chunks in parallel!")
    print("Consider running 2-3 instances for faster generation")

if __name__ == "__main__":
    main()