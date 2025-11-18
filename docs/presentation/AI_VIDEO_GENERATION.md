# 🎬 AI Video Generation Guide (Open Source)

## Option 1: Stable Diffusion + D-ID/SadTalker (Recommended)

### Step 1: Generate Presenter Avatar
```python
# install_dependencies.py
import subprocess
import sys

def install_requirements():
    """Install required packages for video generation"""
    packages = [
        "torch",
        "diffusers",
        "transformers",
        "opencv-python",
        "pillow",
        "numpy",
        "moviepy",
        "gradio",
        "TTS"  # Coqui TTS for voice
    ]

    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

if __name__ == "__main__":
    install_requirements()
```

### Step 2: Text-to-Speech Generation
```python
# generate_narration.py
from TTS.api import TTS
import json

def generate_narration():
    """Generate narration audio using Coqui TTS"""

    # Initialize TTS
    tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC")

    script = """
    What if doctors could instantly find similar medical cases using AI-powered vector search?
    Meet Chazon, where medical imaging meets industrial automation.

    Using BiomedCLIP embeddings and Qdrant vector search, we find matching
    pneumonia cases in under 100 milliseconds with 92% accuracy.

    Unlike typical medical apps, Chazon uses industrial ISA-95 standards
    for enterprise-grade reliability. Full DICOM compliance, HIPAA ready,
    and our AlF-DETECT algorithm for early disease detection.

    Chazon - Industrial-grade medical imaging with AI-powered search.
    Open source, MIT licensed, deploy in 5 minutes.
    Try it now at teslasolar.github.io/qdrant.
    """

    # Generate speech
    tts.tts_to_file(
        text=script,
        file_path="narration.wav",
        speaker=None,
        language="en",
        emotion=None
    )

    print("✅ Narration generated: narration.wav")

if __name__ == "__main__":
    generate_narration()
```

### Step 3: Generate Video Frames
```python
# generate_video_frames.py
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def generate_frames():
    """Generate video frames using Stable Diffusion"""

    # Initialize Stable Diffusion
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        torch_dtype=torch.float16
    )
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

    # Frame descriptions for 60-second video
    scenes = [
        {
            "time": "0:00-0:05",
            "prompt": "modern medical dashboard with x-ray images, futuristic UI, blue and green colors, professional medical software interface",
            "text_overlay": "Chazon Medical Imaging"
        },
        {
            "time": "0:05-0:20",
            "prompt": "doctor analyzing chest x-ray on computer screen, medical AI interface showing similarity scores, hospital setting",
            "text_overlay": "AI-Powered Case Matching"
        },
        {
            "time": "0:20-0:40",
            "prompt": "technical architecture diagram showing ISA-95 levels, industrial control system visualization, connected nodes and data flow",
            "text_overlay": "Qdrant Vector Search"
        },
        {
            "time": "0:40-0:50",
            "prompt": "3D visualization of neural network embeddings, vector space with medical images clustered by similarity",
            "text_overlay": "92% Accuracy in <100ms"
        },
        {
            "time": "0:50-0:60",
            "prompt": "GitHub repository page on screen, open source code, MIT license badge visible",
            "text_overlay": "Open Source • MIT License"
        }
    ]

    frames = []
    for i, scene in enumerate(scenes):
        print(f"Generating scene {i+1}/{len(scenes)}: {scene['time']}")

        # Generate image
        image = pipe(
            prompt=scene["prompt"],
            negative_prompt="low quality, blurry, distorted",
            height=720,
            width=1280,
            guidance_scale=7.5,
            num_inference_steps=50
        ).images[0]

        # Add text overlay
        draw = ImageDraw.Draw(image)
        # You'd need to load a font here
        # font = ImageFont.truetype("arial.ttf", 60)
        draw.text(
            (640, 650),
            scene["text_overlay"],
            fill=(0, 255, 136),
            anchor="mm"
        )

        # Save frame
        image.save(f"frame_{i:03d}.png")
        frames.append(image)

    return frames

if __name__ == "__main__":
    generate_frames()
```

---

## Option 2: Manim (Mathematical Animation Library)

### Install Manim
```bash
pip install manim
```

### Create Animated Presentation
```python
# manim_video.py
from manim import *
import numpy as np

class ChazonDemo(Scene):
    def construct(self):
        # Title Scene (0:00-0:05)
        title = Text("Chazon Medical Imaging", font_size=72, color=GREEN)
        subtitle = Text("AI-Powered Medical Case Matching", font_size=36, color=BLUE)
        subtitle.next_to(title, DOWN, buff=0.5)

        self.play(Write(title))
        self.play(FadeIn(subtitle))
        self.wait(3)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Problem Scene (0:05-0:15)
        problem_text = Text("Current Challenge:", font_size=48, color=RED)
        problem_points = VGroup(
            Text("• Hours to find similar cases", font_size=32),
            Text("• Knowledge trapped in silos", font_size=32),
            Text("• No semantic search", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT)
        problem_points.next_to(problem_text, DOWN, buff=0.5)

        self.play(Write(problem_text))
        self.play(Create(problem_points))
        self.wait(5)
        self.play(FadeOut(problem_text), FadeOut(problem_points))

        # Solution Scene (0:15-0:30)
        solution = Text("Our Solution", font_size=48, color=GREEN)
        self.play(Write(solution))

        # Create vector space visualization
        vectors = VGroup()
        for _ in range(20):
            dot = Dot(
                point=np.array([
                    np.random.uniform(-4, 4),
                    np.random.uniform(-2, 2),
                    0
                ]),
                color=random_color()
            )
            vectors.add(dot)

        self.play(FadeIn(vectors))

        # Show clustering
        center = Dot(ORIGIN, color=GREEN, radius=0.2)
        circle = Circle(radius=2, color=GREEN, stroke_opacity=0.5)

        self.play(
            Create(center),
            Create(circle),
            vectors.animate.move_to(ORIGIN)
        )

        match_text = Text("92% Accuracy", font_size=36, color=GREEN)
        match_text.to_edge(UP)
        self.play(Write(match_text))
        self.wait(5)

        # Architecture Scene (0:30-0:45)
        self.clear()
        arch_title = Text("ISA-95 Architecture", font_size=48, color=BLUE)
        self.play(Write(arch_title))

        # Create architecture levels
        levels = VGroup()
        level_names = [
            "L4: Hospital Management",
            "L3: Medical Execution",
            "L2: Supervisory Control",
            "L1: Device Control",
            "L0: Physical Equipment"
        ]

        for i, name in enumerate(level_names):
            rect = Rectangle(width=8, height=0.8, color=BLUE)
            text = Text(name, font_size=24, color=WHITE)
            text.move_to(rect.get_center())
            level = VGroup(rect, text)
            level.shift(UP * (2 - i))
            levels.add(level)

        self.play(Create(levels))
        self.wait(5)

        # Performance Stats (0:45-0:55)
        self.clear()
        stats_title = Text("Performance", font_size=48, color=GREEN)
        self.play(Write(stats_title))

        stats = VGroup(
            Text("<100ms search latency", font_size=32, color=GREEN),
            Text("50,000+ images indexed", font_size=32, color=BLUE),
            Text("3 hospitals piloting", font_size=32, color=YELLOW)
        ).arrange(DOWN, buff=0.5)

        self.play(Create(stats))
        self.wait(5)

        # Call to Action (0:55-0:60)
        self.clear()
        cta = VGroup(
            Text("Try Chazon Now", font_size=56, color=GREEN),
            Text("github.com/teslasolar/qdrant", font_size=32, color=BLUE),
            Text("Open Source • MIT License", font_size=28, color=WHITE)
        ).arrange(DOWN, buff=0.5)

        self.play(Write(cta))
        self.wait(3)

# Render with:
# manim -p -ql manim_video.py ChazonDemo
```

---

## Option 3: OpenShot + Generated Assets

### Step 1: Generate Screenshots Automatically
```python
# generate_screenshots.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def capture_screenshots():
    """Capture screenshots of the live demo"""

    # Setup Chrome in headless mode
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Chrome(options=options)

    screenshots = [
        {
            "url": "https://teslasolar.github.io/qdrant/",
            "filename": "main_dashboard.png",
            "wait_time": 3
        },
        {
            "url": "https://teslasolar.github.io/qdrant/screens/scada.html",
            "filename": "scada_interface.png",
            "wait_time": 3
        },
        {
            "url": "https://github.com/teslasolar/qdrant",
            "filename": "github_repo.png",
            "wait_time": 2
        }
    ]

    for shot in screenshots:
        print(f"Capturing {shot['filename']}...")
        driver.get(shot['url'])
        time.sleep(shot['wait_time'])
        driver.save_screenshot(shot['filename'])

    driver.quit()
    print("✅ Screenshots captured")

if __name__ == "__main__":
    capture_screenshots()
```

### Step 2: Create Video with MoviePy
```python
# create_video.py
from moviepy.editor import *
from moviepy.video.tools.drawing import color_gradient
import numpy as np

def create_demo_video():
    """Create video from images and audio"""

    # Load narration audio
    audio = AudioFileClip("narration.wav")
    duration = audio.duration  # Should be ~60 seconds

    # Create video clips from screenshots
    clips = []

    # Title card (0-5s)
    title_clip = TextClip(
        "Chazon Medical Imaging",
        fontsize=70,
        color='white',
        font='Arial',
        bg_color='black'
    ).set_duration(5).set_position('center')
    clips.append(title_clip)

    # Dashboard screenshot (5-20s)
    if os.path.exists("main_dashboard.png"):
        dashboard = ImageClip("main_dashboard.png").set_duration(15)
        clips.append(dashboard)

    # SCADA interface (20-35s)
    if os.path.exists("scada_interface.png"):
        scada = ImageClip("scada_interface.png").set_duration(15)
        clips.append(scada)

    # Architecture diagram (35-50s)
    arch_text = TextClip(
        "ISA-95 Architecture\n\nL4: Hospital Management\nL3: Medical Execution\nL2: Supervisory Control\nL1: Device Control\nL0: Physical Equipment",
        fontsize=40,
        color='green',
        font='Courier',
        bg_color='black'
    ).set_duration(15).set_position('center')
    clips.append(arch_text)

    # GitHub repo (50-60s)
    if os.path.exists("github_repo.png"):
        github = ImageClip("github_repo.png").set_duration(10)
        clips.append(github)

    # Concatenate all clips
    final_video = concatenate_videoclips(clips)

    # Add audio
    final_video = final_video.set_audio(audio)

    # Write output
    final_video.write_videofile(
        "chazon_demo.mp4",
        fps=30,
        codec='libx264',
        audio_codec='aac'
    )

    print("✅ Video created: chazon_demo.mp4")

if __name__ == "__main__":
    create_demo_video()
```

---

## Option 4: Remotion (React-based Video Generation)

### Setup Remotion
```bash
npm init video --name=chazon-demo
cd chazon-demo
```

### Create Video Component
```jsx
// src/Video.jsx
import {Composition} from 'remotion';
import {ChazonDemo} from './ChazonDemo';

export const RemotionVideo = () => {
  return (
    <>
      <Composition
        id="ChazonDemo"
        component={ChazonDemo}
        durationInFrames={1800} // 60 seconds at 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};
```

### Render Video
```bash
npx remotion render ChazonDemo out/video.mp4
```

---

## Quick Solution: Canva API (Semi-Open Source)

```python
# canva_video.py
import requests
import json

def create_canva_video():
    """Create video using Canva's API (requires API key)"""

    # This is a simplified example
    # You'd need to sign up for Canva API access

    presentation_data = {
        "slides": [
            {
                "duration": 5,
                "title": "Chazon Medical Imaging",
                "subtitle": "AI-Powered Medical Case Matching"
            },
            {
                "duration": 15,
                "title": "The Problem",
                "bullets": [
                    "Hours to find similar cases",
                    "Knowledge trapped in silos",
                    "No semantic search"
                ]
            },
            {
                "duration": 20,
                "title": "Our Solution",
                "bullets": [
                    "Qdrant vector search",
                    "BiomedCLIP embeddings",
                    "92% accuracy in <100ms"
                ]
            },
            {
                "duration": 15,
                "title": "Architecture",
                "image": "architecture_diagram.png"
            },
            {
                "duration": 5,
                "title": "Try It Now",
                "subtitle": "github.com/teslasolar/qdrant"
            }
        ]
    }

    # Convert to video (pseudo-code)
    # video = canva_api.create_video(presentation_data)
    # video.export("chazon_demo.mp4")

if __name__ == "__main__":
    create_canva_video()
```

---

## Fastest Option: FFmpeg with Images

### Create video from slides HTML
```bash
# 1. Take screenshots of your slides.html
# Open slides.html in browser, press F11 for fullscreen
# Use Print Screen for each slide, save as slide_01.png, slide_02.png, etc.

# 2. Create video from images
ffmpeg -framerate 1/3 -i slide_%02d.png -c:v libx264 -r 30 -pix_fmt yuv420p slides_video.mp4

# 3. Add audio narration
ffmpeg -i slides_video.mp4 -i narration.wav -c:v copy -c:a aac final_video.mp4
```

---

## Recommended Workflow

1. **Generate narration audio** using Coqui TTS (open source)
2. **Capture screenshots** of your live demo
3. **Create slides** as images
4. **Combine with MoviePy** or FFmpeg
5. **Upload to YouTube**

## Installation Commands
```bash
# Install all requirements
pip install TTS moviepy pillow selenium opencv-python ffmpeg-python

# Install FFmpeg (needed for video processing)
# Windows: Download from https://ffmpeg.org/download.html
# Mac: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg

# Generate the video
python generate_narration.py
python generate_screenshots.py
python create_video.py
```

---

## Simple Script Runner
```bash
#!/bin/bash
# run_video_generation.sh

echo "🎬 Generating Chazon Demo Video..."

# Generate narration
echo "1. Generating narration..."
python generate_narration.py

# Capture screenshots
echo "2. Capturing screenshots..."
python generate_screenshots.py

# Create video
echo "3. Creating video..."
python create_video.py

echo "✅ Video generated: chazon_demo.mp4"
echo "Upload to YouTube and add link to submission!"
```

---

## Notes

- **Manim** is great for mathematical/technical animations
- **MoviePy** is best for combining existing assets
- **Remotion** is powerful but requires React knowledge
- **FFmpeg** is the fastest for simple slideshows

Choose the option that matches your comfort level and time constraints!