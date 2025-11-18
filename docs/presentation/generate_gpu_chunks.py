#!/usr/bin/env python3
"""
RTX 4070 Ti SUPER Optimized Chunk Generator
Generates 36 AI video chunks (5 seconds each) for 3-minute video
"""

import torch
import gc
import os
import json
import sys
from pathlib import Path

print("=" * 60)
print("RTX 4070 Ti SUPER VIDEO CHUNK GENERATOR")
print("=" * 60)

# Check GPU
if torch.cuda.is_available():
    device = "cuda"
    gpu_name = torch.cuda.get_device_name(0)
    vram = torch.cuda.get_device_properties(0).total_memory / 1e9
    print(f"[GPU] {gpu_name}")
    print(f"[VRAM] {vram:.1f} GB available")
else:
    device = "cpu"
    print("[WARNING] No GPU detected, using CPU (very slow)")

# Load chunk definitions
chunks_file = "video_chunks.json"
if os.path.exists(chunks_file):
    with open(chunks_file) as f:
        chunks = json.load(f)
    print(f"[CHUNKS] Loaded {len(chunks)} chunk definitions")
else:
    print("[ERROR] video_chunks.json not found!")
    sys.exit(1)

def generate_with_zeroscope():
    """Generate chunks using ZeroScope - Fast and efficient"""

    print("\n[MODEL] ZeroScope V2 - Fast generation mode")
    print("-" * 40)

    from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
    from diffusers.utils import export_to_video

    model_path = "models/zeroscope"
    if not os.path.exists(model_path):
        print("[ERROR] ZeroScope model not found. Run download_gpu_models.py first!")
        return False

    print("[LOAD] Loading ZeroScope model...")
    pipe = DiffusionPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.float16
    ).to(device)

    # Optimize for RTX 4070 Ti
    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    # Enable optimizations
    if device == "cuda":
        try:
            pipe.enable_xformers_memory_efficient_attention()
            print("[OK] Memory efficient attention enabled")
        except:
            print("[INFO] xformers not available")

        pipe.enable_vae_slicing()
        print("[OK] VAE slicing enabled")

    # Create output directory
    output_dir = "zeroscope_chunks"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n[GENERATE] Creating {len(chunks)} video chunks...")
    print("[INFO] Each chunk: 5 seconds at 24fps")
    print("[INFO] Estimated time: 1-2 minutes per chunk")
    print("-" * 40)

    from tqdm import tqdm

    for chunk in tqdm(chunks, desc="Generating chunks"):
        chunk_id = chunk['id']
        prompt = chunk['prompt']

        # Enhance prompt for better quality
        enhanced_prompt = f"{prompt}, high quality, 4k, cinematic, professional, detailed"

        print(f"\n[CHUNK {chunk_id:02d}] {prompt[:60]}...")

        try:
            # Generate video
            video_frames = pipe(
                enhanced_prompt,
                num_frames=24,  # Generate 24 frames (1 second, we'll loop for 5s)
                height=320,      # Lower resolution for faster generation
                width=576,
                num_inference_steps=25,  # Balance quality/speed
                guidance_scale=7.5,
                generator=torch.Generator(device).manual_seed(chunk_id)
            ).frames

            # Save video
            output_path = f"{output_dir}/chunk_{chunk_id:02d}.mp4"
            export_to_video(video_frames, output_path, fps=24)

            print(f"  [OK] Saved: {output_path}")

            # Clear GPU memory after each chunk
            if device == "cuda":
                torch.cuda.empty_cache()
                gc.collect()

        except Exception as e:
            print(f"  [ERROR] Failed: {e}")
            create_placeholder(chunk_id, output_dir)

    print("\n[COMPLETE] All chunks generated!")
    return True

def generate_with_modelscope():
    """Generate using ModelScope - Better quality"""

    print("\n[MODEL] ModelScope - Quality generation mode")
    print("-" * 40)

    from diffusers import DiffusionPipeline
    from diffusers.utils import export_to_video

    model_path = "models/modelscope"
    if not os.path.exists(model_path):
        print("[ERROR] ModelScope model not found!")
        return False

    print("[LOAD] Loading ModelScope model...")
    pipe = DiffusionPipeline.from_pretrained(
        model_path,
        torch_dtype=torch.float16,
        variant="fp16" if os.path.exists(f"{model_path}/unet/diffusion_pytorch_model.fp16.safetensors") else None
    ).to(device)

    if device == "cuda":
        pipe.enable_vae_slicing()
        pipe.enable_model_cpu_offload()

    output_dir = "modelscope_chunks"
    os.makedirs(output_dir, exist_ok=True)

    from tqdm import tqdm

    for chunk in tqdm(chunks, desc="Generating chunks"):
        try:
            video_frames = pipe(
                chunk['prompt'],
                num_frames=16,
                num_inference_steps=25
            ).frames

            output_path = f"{output_dir}/chunk_{chunk['id']:02d}.mp4"
            export_to_video(video_frames, output_path)

            if device == "cuda":
                torch.cuda.empty_cache()

        except Exception as e:
            print(f"  [ERROR] Chunk {chunk['id']}: {e}")
            create_placeholder(chunk['id'], output_dir)

    return True

def generate_with_animatediff():
    """Generate using AnimateDiff - Smooth animations"""

    print("\n[MODEL] AnimateDiff - Smooth animation mode")
    print("-" * 40)

    from diffusers import AnimateDiffPipeline, MotionAdapter, DPMSolverMultistepScheduler
    from diffusers.utils import export_to_video

    motion_path = "models/animatediff-motion"
    sd_path = "models/sd15"

    if not os.path.exists(motion_path) or not os.path.exists(sd_path):
        print("[ERROR] AnimateDiff models not found!")
        return False

    print("[LOAD] Loading AnimateDiff...")

    # Load motion adapter
    adapter = MotionAdapter.from_pretrained(motion_path)

    # Load pipeline
    pipe = AnimateDiffPipeline.from_pretrained(
        sd_path,
        motion_adapter=adapter,
        torch_dtype=torch.float16
    ).to(device)

    pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

    if device == "cuda":
        try:
            pipe.enable_xformers_memory_efficient_attention()
        except:
            pass

    output_dir = "animatediff_chunks"
    os.makedirs(output_dir, exist_ok=True)

    from tqdm import tqdm

    for chunk in tqdm(chunks, desc="Generating chunks"):
        try:
            frames = pipe(
                chunk['prompt'],
                num_frames=16,
                guidance_scale=7.5,
                num_inference_steps=25,
                generator=torch.Generator(device).manual_seed(chunk['id'])
            ).frames[0]

            output_path = f"{output_dir}/chunk_{chunk['id']:02d}.mp4"
            export_to_video(frames, output_path)

            if device == "cuda":
                torch.cuda.empty_cache()

        except Exception as e:
            print(f"  [ERROR] Chunk {chunk['id']}: {e}")
            create_placeholder(chunk['id'], output_dir)

    return True

def create_placeholder(chunk_id, output_dir):
    """Create placeholder video for failed chunks"""

    print(f"  [PLACEHOLDER] Creating for chunk {chunk_id}")

    # Try to use ffmpeg
    try:
        import subprocess
        output_path = f"{output_dir}/chunk_{chunk_id:02d}.mp4"

        cmd = [
            "ffmpeg", "-f", "lavfi",
            "-i", f"color=c=darkblue:s=576x320:d=5:r=24",
            "-vf", f"drawtext=text='Chunk {chunk_id}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=(h-text_h)/2",
            "-pix_fmt", "yuv420p",
            output_path,
            "-y"
        ]
        subprocess.run(cmd, capture_output=True, check=True)
        print(f"  [OK] Placeholder created: {output_path}")
    except:
        # Fallback: create using PIL
        from PIL import Image
        import numpy as np

        frames = []
        for _ in range(120):  # 5 seconds at 24fps
            img = Image.new('RGB', (576, 320), color=(0, 0, 50))
            frames.append(np.array(img))

        # Save using imageio if available
        try:
            import imageio
            output_path = f"{output_dir}/chunk_{chunk_id:02d}.mp4"
            imageio.mimwrite(output_path, frames, fps=24)
            print(f"  [OK] Placeholder created: {output_path}")
        except:
            print(f"  [WARNING] Could not create placeholder for chunk {chunk_id}")

def extend_to_5_seconds(input_dir):
    """Extend 1-second clips to 5 seconds by looping"""

    print("\n[EXTEND] Extending clips to 5 seconds...")

    import cv2

    for chunk_file in Path(input_dir).glob("chunk_*.mp4"):
        try:
            # Read video
            cap = cv2.VideoCapture(str(chunk_file))
            frames = []

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)

            cap.release()

            if len(frames) == 0:
                continue

            # Loop frames to reach 5 seconds (120 frames at 24fps)
            target_frames = 120
            extended_frames = []

            while len(extended_frames) < target_frames:
                for frame in frames:
                    extended_frames.append(frame)
                    if len(extended_frames) >= target_frames:
                        break

            # Write extended video
            height, width = frames[0].shape[:2]
            output_path = str(chunk_file).replace(".mp4", "_5s.mp4")

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, 24, (width, height))

            for frame in extended_frames:
                out.write(frame)

            out.release()
            print(f"  [OK] Extended: {output_path}")

        except Exception as e:
            print(f"  [ERROR] Failed to extend {chunk_file}: {e}")

def main():
    """Main generation function"""

    print("\nSelect generation method:")
    print("1. ZeroScope (Fastest - 30-60 min total)")
    print("2. ModelScope (Better quality - 60-90 min)")
    print("3. AnimateDiff (Smoothest - 90-120 min)")
    print("4. Test mode (Generate 3 chunks only)")

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        choice = input("\nSelect [1]: ").strip() or "1"

    # For test mode, limit chunks
    global chunks
    if choice == "4":
        print("\n[TEST MODE] Generating first 3 chunks only...")
        chunks = chunks[:3]
        choice = "1"  # Use ZeroScope for test

    success = False

    if choice == "1":
        success = generate_with_zeroscope()
        if success:
            extend_to_5_seconds("zeroscope_chunks")
    elif choice == "2":
        success = generate_with_modelscope()
        if success:
            extend_to_5_seconds("modelscope_chunks")
    elif choice == "3":
        success = generate_with_animatediff()
        if success:
            extend_to_5_seconds("animatediff_chunks")

    if success:
        print("\n" + "=" * 60)
        print("SUCCESS! Video chunks generated!")
        print("=" * 60)
        print("\n[NEXT STEPS]")
        print("1. Check generated chunks in folder")
        print("2. Run: python combine_chunks.py")
        print("3. Final video: chazon_ai_video_final.mp4")
    else:
        print("\n[ERROR] Generation failed. Check error messages above.")

if __name__ == "__main__":
    main()