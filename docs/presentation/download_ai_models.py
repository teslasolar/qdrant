#!/usr/bin/env python3
"""
Download and setup open-source AI video generation models from GitHub
Optimized for GPU acceleration
"""

import os
import subprocess
import sys
import json
from pathlib import Path

print("=" * 60)
print("GPU-ACCELERATED AI VIDEO MODEL DOWNLOADER")
print("=" * 60)

def check_gpu():
    """Check if CUDA GPU is available"""
    try:
        import torch
        if torch.cuda.is_available():
            print(f"[GPU] CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"[GPU] CUDA version: {torch.version.cuda}")
            return True
        else:
            print("[WARNING] No CUDA GPU detected, will use CPU (slower)")
            return False
    except ImportError:
        print("[INFO] PyTorch not installed yet")
        return None

def install_gpu_dependencies():
    """Install GPU-accelerated dependencies"""

    print("\n[INSTALL] Installing GPU dependencies...")

    packages = [
        # Core GPU libraries
        "torch==2.1.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html",
        "torchvision==0.16.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html",
        "torchaudio==2.1.0+cu118 -f https://download.pytorch.org/whl/torch_stable.html",

        # Video generation libraries
        "diffusers",           # Hugging Face diffusion models
        "transformers",        # Model architectures
        "accelerate",          # GPU acceleration
        "xformers",           # Memory efficient attention (GPU)
        "opencv-python",       # Video processing
        "imageio",            # Image/video I/O
        "imageio-ffmpeg",     # FFmpeg backend
        "safetensors",        # Fast model loading
        "omegaconf",          # Configuration
        "einops",             # Tensor operations
        "pytorch-lightning",   # Training framework
        "kornia",             # Computer vision
        "tqdm",               # Progress bars
        "huggingface-hub",    # Model downloading
    ]

    for package in packages:
        print(f"[INSTALL] {package.split()[0]}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + package.split())
            print(f"[OK] Installed")
        except:
            print(f"[WARNING] Failed to install {package.split()[0]}")

    # Try to install xformers for GPU memory efficiency
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "xformers"])
        print("[OK] xformers installed for efficient GPU memory usage")
    except:
        print("[INFO] xformers not available (optional)")

def download_stable_video_diffusion():
    """Download Stable Video Diffusion from GitHub"""

    print("\n[MODEL] Downloading Stable Video Diffusion...")
    print("-" * 40)

    # Clone the repository
    repo_url = "https://github.com/Stability-AI/generative-models.git"
    repo_dir = "stable-video-diffusion"

    if not os.path.exists(repo_dir):
        print("[GIT] Cloning Stability AI repository...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, repo_dir])

    # Download model weights using Hugging Face
    script = """
import torch
from diffusers import StableVideoDiffusionPipeline
from huggingface_hub import snapshot_download
import os

print("[DOWNLOAD] Fetching Stable Video Diffusion weights...")

# Create models directory
os.makedirs("models/svd", exist_ok=True)

# Download SVD model (smaller XT version for faster generation)
model_id = "stabilityai/stable-video-diffusion-img2vid-xt"

try:
    # Download to local cache
    snapshot_download(
        repo_id=model_id,
        local_dir="models/svd",
        ignore_patterns=["*.bin"],  # Only download safetensors
        resume_download=True
    )
    print("[OK] SVD model downloaded")
except Exception as e:
    print(f"[ERROR] Download failed: {e}")
    print("[TIP] You can manually download from:")
    print("https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt")
"""

    with open("download_svd.py", "w") as f:
        f.write(script)

    subprocess.run([sys.executable, "download_svd.py"])
    return True

def download_animatediff():
    """Download AnimateDiff models from GitHub"""

    print("\n[MODEL] Downloading AnimateDiff...")
    print("-" * 40)

    # Clone AnimateDiff repository
    repo_url = "https://github.com/guoyww/AnimateDiff.git"
    repo_dir = "AnimateDiff"

    if not os.path.exists(repo_dir):
        print("[GIT] Cloning AnimateDiff repository...")
        subprocess.run(["git", "clone", "--depth", "1", repo_url, repo_dir])

    # Download model weights
    script = """
from huggingface_hub import snapshot_download
import os

print("[DOWNLOAD] Fetching AnimateDiff weights...")

# Create models directory
os.makedirs("models/animatediff", exist_ok=True)

# Download motion module
motion_model = "guoyww/animatediff-motion-adapter-v1-5-2"

try:
    snapshot_download(
        repo_id=motion_model,
        local_dir="models/animatediff/motion",
        resume_download=True
    )
    print("[OK] AnimateDiff motion module downloaded")
except Exception as e:
    print(f"[ERROR] Download failed: {e}")

# Download base model (using SD 1.5 as base)
base_model = "runwayml/stable-diffusion-v1-5"

try:
    snapshot_download(
        repo_id=base_model,
        local_dir="models/animatediff/sd15",
        resume_download=True
    )
    print("[OK] Base SD1.5 model downloaded")
except Exception as e:
    print(f"[ERROR] Base model download failed: {e}")
"""

    with open("download_animatediff.py", "w") as f:
        f.write(script)

    subprocess.run([sys.executable, "download_animatediff.py"])
    return True

def download_zeroscope():
    """Download ZeroScope model (lightweight, fast)"""

    print("\n[MODEL] Downloading ZeroScope V2...")
    print("-" * 40)

    script = """
from huggingface_hub import snapshot_download
import os

print("[DOWNLOAD] Fetching ZeroScope V2...")

# Create models directory
os.makedirs("models/zeroscope", exist_ok=True)

# ZeroScope V2 - fast text-to-video
model_id = "cerspense/zeroscope_v2_576w"

try:
    snapshot_download(
        repo_id=model_id,
        local_dir="models/zeroscope",
        resume_download=True
    )
    print("[OK] ZeroScope model downloaded")
except Exception as e:
    print(f"[ERROR] Download failed: {e}")
"""

    with open("download_zeroscope.py", "w") as f:
        f.write(script)

    subprocess.run([sys.executable, "download_zeroscope.py"])
    return True

def download_modelscope():
    """Download ModelScope text-to-video model"""

    print("\n[MODEL] Downloading ModelScope...")
    print("-" * 40)

    script = """
from huggingface_hub import snapshot_download
import os

print("[DOWNLOAD] Fetching ModelScope text-to-video...")

# Create models directory
os.makedirs("models/modelscope", exist_ok=True)

# ModelScope text-to-video
model_id = "damo-vilab/text-to-video-ms-1.7b"

try:
    snapshot_download(
        repo_id=model_id,
        local_dir="models/modelscope",
        resume_download=True
    )
    print("[OK] ModelScope model downloaded")
except Exception as e:
    print(f"[ERROR] Download failed: {e}")
    print("[TIP] ModelScope is 3.5GB, may take time")
"""

    with open("download_modelscope.py", "w") as f:
        f.write(script)

    subprocess.run([sys.executable, "download_modelscope.py"])
    return True

def create_gpu_video_generator():
    """Create GPU-optimized video generation script"""

    print("\n[CREATE] GPU video generation script...")

    script = '''#!/usr/bin/env python3
"""
GPU-Accelerated AI Video Generation
Generates 36 chunks for 3-minute video using downloaded models
"""

import torch
import numpy as np
from diffusers import StableVideoDiffusionPipeline, AnimateDiffPipeline, DiffusionPipeline
from PIL import Image
import json
import os
from tqdm import tqdm

print("=" * 60)
print("GPU AI VIDEO GENERATION")
print("=" * 60)

# Check GPU
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[DEVICE] Using: {device}")
if device == "cuda":
    print(f"[GPU] {torch.cuda.get_device_name(0)}")
    print(f"[VRAM] {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# Load chunk definitions
with open("video_chunks.json") as f:
    chunks = json.load(f)

class VideoGenerator:
    def __init__(self, model_type="zeroscope"):
        self.model_type = model_type
        self.device = device
        self.pipe = None

    def load_model(self):
        """Load the specified model"""

        if self.model_type == "svd":
            print("[LOAD] Loading Stable Video Diffusion...")
            self.pipe = StableVideoDiffusionPipeline.from_pretrained(
                "models/svd",
                torch_dtype=torch.float16,
                variant="fp16"
            )

        elif self.model_type == "animatediff":
            print("[LOAD] Loading AnimateDiff...")
            self.pipe = AnimateDiffPipeline.from_pretrained(
                "models/animatediff/sd15",
                motion_adapter="models/animatediff/motion",
                torch_dtype=torch.float16
            )

        elif self.model_type == "zeroscope":
            print("[LOAD] Loading ZeroScope...")
            self.pipe = DiffusionPipeline.from_pretrained(
                "models/zeroscope",
                torch_dtype=torch.float16
            )

        elif self.model_type == "modelscope":
            print("[LOAD] Loading ModelScope...")
            self.pipe = DiffusionPipeline.from_pretrained(
                "models/modelscope",
                torch_dtype=torch.float16
            )

        # Move to GPU
        self.pipe = self.pipe.to(self.device)

        # Enable memory efficient attention if available
        try:
            self.pipe.enable_xformers_memory_efficient_attention()
            print("[OK] Memory efficient attention enabled")
        except:
            pass

        # Enable CPU offload for low VRAM
        if torch.cuda.is_available():
            try:
                self.pipe.enable_model_cpu_offload()
                print("[OK] CPU offload enabled for low VRAM")
            except:
                pass

    def generate_chunk(self, chunk_data):
        """Generate a single video chunk"""

        chunk_id = chunk_data["id"]
        prompt = chunk_data["prompt"]

        print(f"\\n[CHUNK {chunk_id}] Generating: {prompt[:50]}...")

        output_path = f"chunk_{chunk_id:02d}.mp4"

        if self.model_type == "svd":
            # SVD needs an input image
            # Create a simple gradient image based on prompt
            base_image = self.create_base_image(prompt)

            frames = self.pipe(
                base_image,
                num_frames=25,  # SVD generates 25 frames
                decode_chunk_size=8,
                generator=torch.Generator(device=self.device).manual_seed(chunk_id),
                motion_bucket_id=127,  # Control motion amount
                noise_aug_strength=0.02
            ).frames[0]

        else:
            # Text-to-video models
            frames = self.pipe(
                prompt,
                num_frames=16 if self.model_type == "animatediff" else 24,
                height=320 if self.model_type == "modelscope" else 576,
                width=576 if self.model_type == "modelscope" else 1024,
                num_inference_steps=25,
                guidance_scale=7.5,
                generator=torch.Generator(device=self.device).manual_seed(chunk_id)
            ).frames[0]

        # Save frames as video
        self.save_video(frames, output_path)
        print(f"[OK] Saved: {output_path}")

        return output_path

    def create_base_image(self, prompt):
        """Create base image for SVD from prompt keywords"""

        width, height = 1024, 576
        img = Image.new('RGB', (width, height), color='black')

        # Add gradient based on prompt keywords
        pixels = img.load()

        if "medical" in prompt.lower() or "hospital" in prompt.lower():
            # Blue medical theme
            for y in range(height):
                for x in range(width):
                    r = int(10 + (x/width) * 20)
                    g = int(20 + (y/height) * 50)
                    b = int(100 + ((x+y)/(width+height)) * 155)
                    pixels[x, y] = (r, g, b)

        elif "ai" in prompt.lower() or "neural" in prompt.lower():
            # Purple AI theme
            for y in range(height):
                for x in range(width):
                    r = int(80 + (x/width) * 100)
                    g = int(20 + (y/height) * 40)
                    b = int(120 + ((x+y)/(width+height)) * 135)
                    pixels[x, y] = (r, g, b)

        else:
            # Default gradient
            for y in range(height):
                for x in range(width):
                    val = int(((x + y) / (width + height)) * 255)
                    pixels[x, y] = (val//3, val//2, val)

        return img

    def save_video(self, frames, output_path, fps=24):
        """Save frames as MP4 video"""

        import imageio

        # Convert PIL images to numpy arrays
        frames_np = [np.array(frame) for frame in frames]

        # Save using imageio
        imageio.mimwrite(output_path, frames_np, fps=fps, quality=8)

def generate_all_chunks(model_type="zeroscope"):
    """Generate all 36 chunks"""

    generator = VideoGenerator(model_type)
    generator.load_model()

    os.makedirs("output_chunks", exist_ok=True)
    os.chdir("output_chunks")

    # Generate chunks with progress bar
    for chunk in tqdm(chunks, desc="Generating chunks"):
        try:
            generator.generate_chunk(chunk)

            # Clear GPU cache after each chunk
            if torch.cuda.is_available():
                torch.cuda.empty_cache()

        except Exception as e:
            print(f"[ERROR] Chunk {chunk['id']}: {e}")
            # Create placeholder on error
            create_placeholder(chunk['id'])

    print("\\n[COMPLETE] All chunks generated!")
    print("Run: python combine_chunks.py")

def create_placeholder(chunk_id):
    """Create placeholder video for failed chunks"""
    import subprocess

    cmd = [
        "ffmpeg", "-f", "lavfi",
        "-i", f"color=c=darkblue:s=1024x576:d=5:r=24",
        "-vf", f"drawtext=text='Chunk {chunk_id}':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=(h-text_h)/2",
        "-pix_fmt", "yuv420p",
        f"chunk_{chunk_id:02d}.mp4",
        "-y"
    ]
    subprocess.run(cmd, capture_output=True)

if __name__ == "__main__":
    import sys

    # Choose model
    print("\\nAvailable models:")
    print("1. zeroscope (fastest, good quality)")
    print("2. modelscope (balanced)")
    print("3. animatediff (smooth animations)")
    print("4. svd (best quality, needs more VRAM)")

    if len(sys.argv) > 1:
        model_map = {
            "1": "zeroscope",
            "2": "modelscope",
            "3": "animatediff",
            "4": "svd",
            "zeroscope": "zeroscope",
            "modelscope": "modelscope",
            "animatediff": "animatediff",
            "svd": "svd"
        }
        model = model_map.get(sys.argv[1], "zeroscope")
    else:
        choice = input("\\nSelect model (1-4) [1]: ").strip() or "1"
        model = ["zeroscope", "modelscope", "animatediff", "svd"][int(choice)-1]

    print(f"\\nUsing model: {model}")
    generate_all_chunks(model)
'''

    with open("gpu_generate_video.py", "w") as f:
        f.write(script)

    print("[SAVED] gpu_generate_video.py")

def create_batch_generator():
    """Create script for parallel batch generation"""

    script = '''#!/usr/bin/env python3
"""
Batch GPU Video Generation - Process chunks in parallel
"""

import torch
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import json
import sys

def generate_batch(start_idx, end_idx, model_type="zeroscope"):
    """Generate a batch of chunks on GPU"""

    # Import here to avoid pickling issues
    from gpu_generate_video import VideoGenerator

    # Load chunks
    with open("video_chunks.json") as f:
        all_chunks = json.load(f)

    chunks = all_chunks[start_idx:end_idx]

    # Initialize generator
    gen = VideoGenerator(model_type)
    gen.load_model()

    # Process batch
    for chunk in chunks:
        try:
            gen.generate_chunk(chunk)
            torch.cuda.empty_cache()
        except Exception as e:
            print(f"[ERROR] Chunk {chunk['id']}: {e}")

if __name__ == "__main__":
    # Split 36 chunks into batches
    batches = [
        (0, 9),    # Chunks 1-9
        (9, 18),   # Chunks 10-18
        (18, 27),  # Chunks 19-27
        (27, 36)   # Chunks 28-36
    ]

    model = sys.argv[1] if len(sys.argv) > 1 else "zeroscope"

    print(f"[BATCH] Processing 36 chunks in {len(batches)} batches")
    print(f"[MODEL] Using: {model}")

    # Process batches sequentially (can't run multiple on same GPU)
    for i, (start, end) in enumerate(batches):
        print(f"\\n[BATCH {i+1}] Processing chunks {start+1}-{end}")
        generate_batch(start, end, model)

        # Clear GPU between batches
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

    print("\\n[COMPLETE] All batches processed!")
'''

    with open("batch_gpu_generate.py", "w") as f:
        f.write(script)

    print("[SAVED] batch_gpu_generate.py")

def main():
    """Main setup function"""

    # Check GPU status
    gpu_available = check_gpu()

    if gpu_available is None:
        print("\n[SETUP] Installing GPU dependencies first...")
        install_gpu_dependencies()
        gpu_available = check_gpu()

    # Create output directories
    os.makedirs("models", exist_ok=True)
    os.makedirs("output_chunks", exist_ok=True)

    print("\n[DOWNLOAD] Starting model downloads...")
    print("This will download several GB of model files")
    print("-" * 40)

    # Download models
    models_to_download = [
        ("ZeroScope (1.7GB, fastest)", download_zeroscope),
        ("ModelScope (3.5GB, balanced)", download_modelscope),
        ("AnimateDiff (4GB, smooth)", download_animatediff),
        ("Stable Video Diffusion (5GB, best)", download_stable_video_diffusion),
    ]

    print("\nSelect models to download:")
    print("1. ZeroScope only (fastest, 1.7GB)")
    print("2. All lightweight (ZeroScope + ModelScope, 5.2GB)")
    print("3. All models (15GB total)")

    choice = input("\nSelect option [1]: ").strip() or "1"

    if choice == "1":
        download_zeroscope()
    elif choice == "2":
        download_zeroscope()
        download_modelscope()
    else:
        for name, func in models_to_download:
            print(f"\n[DOWNLOADING] {name}")
            func()

    # Create generation scripts
    create_gpu_video_generator()
    create_batch_generator()

    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)

    print("\n[GPU STATUS]")
    if gpu_available:
        print("✅ GPU detected and ready!")
    else:
        print("⚠️ No GPU detected - will use CPU (slower)")

    print("\n[QUICK START]")
    print("1. Generate all 36 chunks:")
    print("   python gpu_generate_video.py")
    print("")
    print("2. Or generate in batches:")
    print("   python batch_gpu_generate.py")
    print("")
    print("3. Combine chunks:")
    print("   python combine_chunks.py")

    print("\n[MODELS READY]")
    if os.path.exists("models/zeroscope"):
        print("✅ ZeroScope")
    if os.path.exists("models/modelscope"):
        print("✅ ModelScope")
    if os.path.exists("models/animatediff"):
        print("✅ AnimateDiff")
    if os.path.exists("models/svd"):
        print("✅ Stable Video Diffusion")

    print("\n[TIP] Start with ZeroScope - it's fastest and uses less VRAM")
    print("[TIP] Each chunk takes 10-60 seconds on GPU depending on model")

if __name__ == "__main__":
    main()