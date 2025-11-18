#!/usr/bin/env python3
"""
AI Video Generation with Open Source Models
Creates actual animated videos using AI models
"""

import os
import sys

def install_video_ai_packages():
    """Install packages for AI video generation"""

    print("[AI VIDEO] Installing AI video generation tools...")
    print("-" * 60)

    packages = [
        # Core AI packages
        "torch",                    # PyTorch for AI models
        "torchvision",             # Vision models
        "transformers",            # Hugging Face transformers
        "diffusers",               # Stable Diffusion models
        "accelerate",              # GPU acceleration
        "opencv-python",           # Video processing
        "imageio",                 # Image/video I/O
        "xformers",                # Memory efficient transformers

        # Additional tools
        "gradio",                  # Web UI
        "huggingface-hub",        # Model downloading
        "safetensors",            # Safe model loading
        "einops",                 # Tensor operations
        "omegaconf",              # Configuration
    ]

    import subprocess

    for package in packages:
        print(f"[INSTALL] {package}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--upgrade"])
            print(f"[OK] {package} installed")
        except Exception as e:
            print(f"[ERROR] Failed to install {package}: {e}")

    print("\n[AI VIDEO] Installation complete!")
    return True

# ============================================
# Option 1: Stable Video Diffusion (SVD)
# ============================================

def setup_stable_video_diffusion():
    """
    Stable Video Diffusion - Image to Video
    Creates short video clips from static images
    """

    print("\n" + "=" * 60)
    print("STABLE VIDEO DIFFUSION SETUP")
    print("=" * 60)

    code = '''
import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
from PIL import Image
import numpy as np

def generate_video_from_image(image_path, output_path="generated_video.mp4"):
    """Generate video from a single image using SVD"""

    print("[SVD] Loading Stable Video Diffusion model...")

    # Load the model (will download ~10GB on first run)
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid",
        torch_dtype=torch.float16,
        variant="fp16"
    )

    # Use GPU if available
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    # Memory optimization
    pipe.enable_model_cpu_offload()

    print("[SVD] Loading input image...")
    image = load_image(image_path)
    image = image.resize((1024, 576))  # Recommended resolution

    print("[SVD] Generating video frames...")
    generator = torch.manual_seed(42)

    frames = pipe(
        image,
        decode_chunk_size=8,
        generator=generator,
        num_frames=25,  # 25 frames
        motion_bucket_id=127,  # Controls motion amount
    ).frames[0]

    print(f"[SVD] Exporting video to {output_path}...")
    export_to_video(frames, output_path, fps=7)

    print(f"[SUCCESS] Video saved: {output_path}")
    return output_path

# Example usage for medical demo
if __name__ == "__main__":
    # Use one of your presentation slides as input
    generate_video_from_image(
        "slide_01.png",
        "medical_animation_svd.mp4"
    )
'''

    print(code)

    # Save the script
    with open("generate_svd_video.py", "w") as f:
        f.write(code)

    print("\n[SAVED] Script saved to generate_svd_video.py")
    print("[INFO] This creates smooth animations from static images")
    print("[INFO] First run will download ~10GB model")

# ============================================
# Option 2: AnimateDiff
# ============================================

def setup_animatediff():
    """
    AnimateDiff - Text to Video
    Creates videos from text prompts
    """

    print("\n" + "=" * 60)
    print("ANIMATEDIFF SETUP")
    print("=" * 60)

    code = '''
import torch
from diffusers import AnimateDiffPipeline, DDIMScheduler, MotionAdapter
from diffusers.utils import export_to_gif, export_to_video
import os

def generate_animated_video(
    prompt="A doctor examining medical x-ray images on a futuristic holographic display",
    output_path="medical_animation.mp4"
):
    """Generate animated video from text prompt"""

    print("[AnimateDiff] Loading models...")

    # Load motion adapter
    adapter = MotionAdapter.from_pretrained(
        "guoyww/animatediff-motion-adapter-v1-5-2",
        torch_dtype=torch.float16
    )

    # Load pipeline
    model_id = "SG161222/Realistic_Vision_V5.1_noVAE"
    pipe = AnimateDiffPipeline.from_pretrained(
        model_id,
        motion_adapter=adapter,
        torch_dtype=torch.float16
    )

    scheduler = DDIMScheduler.from_pretrained(
        model_id,
        subfolder="scheduler",
        clip_sample=False,
        timestep_spacing="linspace",
        steps_offset=1
    )
    pipe.scheduler = scheduler

    # Move to GPU if available
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    # Enable memory efficient attention
    pipe.enable_vae_slicing()
    pipe.enable_model_cpu_offload()

    print(f"[AnimateDiff] Generating video for: {prompt}")

    output = pipe(
        prompt=prompt,
        negative_prompt="low quality, worst quality, blurry",
        num_frames=16,
        guidance_scale=7.5,
        num_inference_steps=25,
        generator=torch.Generator().manual_seed(42)
    )

    frames = output.frames[0]

    print(f"[AnimateDiff] Saving video to {output_path}...")
    export_to_video(frames, output_path, fps=8)

    print(f"[SUCCESS] Animated video saved: {output_path}")
    return output_path

# Medical visualization examples
medical_prompts = [
    "A 3D rotating brain scan showing neural activity with glowing pathways",
    "Medical robot performing precise surgery with holographic guidance",
    "Futuristic medical laboratory with floating holographic displays",
    "Doctor using AI to analyze chest x-rays on transparent screens",
    "DNA helix rotating with data visualization overlays"
]

if __name__ == "__main__":
    for i, prompt in enumerate(medical_prompts[:1]):  # Generate first prompt
        print(f"\\nGenerating: {prompt}")
        generate_animated_video(prompt, f"medical_anim_{i}.mp4")
'''

    print(code)

    with open("generate_animatediff_video.py", "w") as f:
        f.write(code)

    print("\n[SAVED] Script saved to generate_animatediff_video.py")
    print("[INFO] This creates videos from text descriptions")

# ============================================
# Option 3: Text2Video-Zero
# ============================================

def setup_text2video_zero():
    """
    Text2Video-Zero - Text to Video without training
    Leverages existing image models for video
    """

    print("\n" + "=" * 60)
    print("TEXT2VIDEO-ZERO SETUP")
    print("=" * 60)

    code = '''
import torch
from diffusers import TextToVideoZeroPipeline
import imageio
import numpy as np

def generate_zero_shot_video(
    prompt="Medical imaging system analyzing patient data in real-time",
    output_path="medical_zero_shot.mp4"
):
    """Generate video without any video training data"""

    print("[Text2Video-Zero] Initializing pipeline...")

    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = TextToVideoZeroPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16
    ).to("cuda" if torch.cuda.is_available() else "cpu")

    print(f"[Text2Video-Zero] Generating video for: {prompt}")

    # Generate video
    result = pipe(
        prompt=prompt,
        video_length=8,  # 8 frames
        height=512,
        width=512,
        num_inference_steps=50,
        guidance_scale=7.5,
        t0=44,  # Controls motion coherence
        t1=47,
        motion_field_strength_x=12,  # Horizontal motion
        motion_field_strength_y=12,  # Vertical motion
    ).images

    print("[Text2Video-Zero] Converting frames to video...")

    # Convert PIL images to numpy arrays
    result = [np.array(frame) for frame in result]

    # Save as video
    imageio.mimsave(output_path, result, fps=4)

    print(f"[SUCCESS] Zero-shot video saved: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_zero_shot_video()
'''

    print(code)

    with open("generate_text2video_zero.py", "w") as f:
        f.write(code)

    print("\n[SAVED] Script saved to generate_text2video_zero.py")
    print("[INFO] This creates videos without video training data")

# ============================================
# Option 4: Simple AI Animation with Gradio UI
# ============================================

def create_gradio_ui():
    """Create web UI for video generation"""

    print("\n" + "=" * 60)
    print("GRADIO WEB UI FOR VIDEO GENERATION")
    print("=" * 60)

    code = '''
import gradio as gr
import torch
from diffusers import DiffusionPipeline, DPMSolverMultistepScheduler
from diffusers.utils import export_to_video
import numpy as np

def generate_medical_animation(
    prompt,
    video_length=8,
    inference_steps=25,
    guidance_scale=7.5
):
    """Generate medical animation from text"""

    try:
        # For demo, we'll use a lightweight model
        pipe = DiffusionPipeline.from_pretrained(
            "damo-vilab/text-to-video-ms-1.7b",
            torch_dtype=torch.float16,
            variant="fp16"
        )

        pipe.scheduler = DPMSolverMultistepScheduler.from_config(
            pipe.scheduler.config
        )

        pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
        pipe.enable_model_cpu_offload()

        video_frames = pipe(
            prompt,
            num_inference_steps=inference_steps,
            height=256,
            width=256,
            num_frames=video_length,
            guidance_scale=guidance_scale
        ).frames

        output_path = "gradio_output.mp4"
        export_to_video(video_frames, output_path, fps=8)

        return output_path, f"✅ Generated: {prompt}"

    except Exception as e:
        return None, f"❌ Error: {str(e)}"

# Create Gradio interface
iface = gr.Interface(
    fn=generate_medical_animation,
    inputs=[
        gr.Textbox(
            label="Prompt",
            placeholder="Describe the medical scene to animate...",
            value="A futuristic medical scanner analyzing a patient"
        ),
        gr.Slider(4, 16, value=8, step=1, label="Video Length (frames)"),
        gr.Slider(10, 50, value=25, step=5, label="Quality (inference steps)"),
        gr.Slider(1, 15, value=7.5, step=0.5, label="Guidance Scale")
    ],
    outputs=[
        gr.Video(label="Generated Animation"),
        gr.Textbox(label="Status")
    ],
    title="🏥 Medical AI Video Generator",
    description="Generate medical animations using AI. Powered by Stable Diffusion.",
    examples=[
        ["A 3D brain scan rotating with highlighted neural pathways"],
        ["Doctor examining holographic x-ray display"],
        ["Medical nanorobots traveling through bloodstream"],
        ["AI analyzing multiple medical scans simultaneously"],
        ["Futuristic surgery room with robotic assistants"]
    ]
)

if __name__ == "__main__":
    print("Starting Gradio UI on http://localhost:7860")
    iface.launch(share=True)  # share=True for public URL
'''

    print(code)

    with open("medical_video_ui.py", "w") as f:
        f.write(code)

    print("\n[SAVED] Script saved to medical_video_ui.py")
    print("[INFO] Run this for a web interface to generate videos")

# ============================================
# Main execution
# ============================================

def main():
    print("\n" + "=" * 60)
    print("AI VIDEO GENERATION TOOLKIT")
    print("=" * 60)
    print("\nAvailable AI Video Generation Methods:\n")

    print("1. STABLE VIDEO DIFFUSION (Image → Video)")
    print("   - Best for: Animating static images")
    print("   - Quality: High")
    print("   - Speed: Medium")
    print("   - VRAM: 8GB+")

    print("\n2. ANIMATEDIFF (Text → Video)")
    print("   - Best for: Creating videos from descriptions")
    print("   - Quality: High")
    print("   - Speed: Slow")
    print("   - VRAM: 8GB+")

    print("\n3. TEXT2VIDEO-ZERO (Text → Video)")
    print("   - Best for: Quick prototypes")
    print("   - Quality: Medium")
    print("   - Speed: Fast")
    print("   - VRAM: 6GB+")

    print("\n4. MODELSCOPE (Text → Video)")
    print("   - Best for: Short clips")
    print("   - Quality: Good")
    print("   - Speed: Medium")
    print("   - VRAM: 4GB+")

    print("\n" + "-" * 60)

    choice = input("\nSetup which method? (1-4, or 'all'): ").strip()

    if choice == '1':
        setup_stable_video_diffusion()
    elif choice == '2':
        setup_animatediff()
    elif choice == '3':
        setup_text2video_zero()
    elif choice == '4':
        create_gradio_ui()
    elif choice == 'all':
        setup_stable_video_diffusion()
        setup_animatediff()
        setup_text2video_zero()
        create_gradio_ui()
    else:
        print("[INFO] Installing packages only...")
        install_video_ai_packages()

    print("\n" + "=" * 60)
    print("SETUP COMPLETE!")
    print("=" * 60)
    print("\nTo generate AI videos:")
    print("1. Run one of the generated scripts")
    print("2. First run will download models (2-10GB)")
    print("3. Requires GPU for best performance")
    print("\nFor quick test: python medical_video_ui.py")

if __name__ == "__main__":
    main()