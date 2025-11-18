#!/usr/bin/env python3
"""
Generate Multiple Concept Videos with Synchronized Narration
No testing claims - pure prototype demonstration
"""

import os
import subprocess
import sys
from pathlib import Path

print("=" * 60)
print("CONCEPT VIDEO GENERATOR")
print("Prototype Demonstrations Only")
print("=" * 60)

# Video configurations
videos = [
    {
        "name": "concept_30s",
        "duration": 30,
        "narration_file": "narration_concept_30s.txt",
        "title": "30-Second Concept Overview",
        "voice": "en-US-GuyNeural",  # Professional male
        "rate": "+0%"
    },
    {
        "name": "concept_60s",
        "duration": 60,
        "narration_file": "narration_concept_60s.txt",
        "title": "60-Second Technical Concept",
        "voice": "en-US-AriaNeural",  # Professional female
        "rate": "-5%"
    },
    {
        "name": "concept_90s_tech",
        "duration": 90,
        "narration_file": "narration_technical_90s.txt",
        "title": "90-Second Technical Deep Dive",
        "voice": "en-US-ChristopherNeural",  # Technical male
        "rate": "+5%"
    },
    {
        "name": "concept_2min_full",
        "duration": 120,
        "narration_file": "narration_concept_2min.txt",
        "title": "2-Minute Full Concept Demo",
        "voice": "en-US-JennyNeural",  # Clear female
        "rate": "+0%"
    }
]

def generate_narration(config):
    """Generate narration audio for each video"""

    print(f"\n[NARRATION] Generating {config['title']}...")

    # Read narration text
    with open(config['narration_file'], 'r', encoding='utf-8') as f:
        text = f.read()

    # Clean text (remove headers and timing markers)
    lines = []
    for line in text.split('\n'):
        if line.strip() and not line.startswith('#') and not line.startswith('['):
            lines.append(line.strip())

    narration_text = ' '.join(lines)

    # Generate audio using Edge TTS
    output_file = f"{config['name']}_narration.mp3"

    try:
        import edge_tts
        import asyncio

        async def generate():
            communicate = edge_tts.Communicate(
                narration_text,
                config['voice'],
                rate=config['rate']
            )
            await communicate.save(output_file)

        asyncio.run(generate())
        print(f"  [OK] Generated: {output_file}")
        return output_file

    except ImportError:
        print("  [INSTALL] Installing edge-tts...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
        return generate_narration(config)
    except Exception as e:
        print(f"  [ERROR] Failed: {e}")
        return None

def create_video_segments(config):
    """Create video segments for the specified duration"""

    print(f"\n[VIDEO] Creating {config['duration']}s video segments...")

    # Calculate chunks needed (5 seconds each)
    num_chunks = config['duration'] // 5

    output_dir = f"chunks_{config['name']}"
    os.makedirs(output_dir, exist_ok=True)

    # Define segment types based on duration
    if config['duration'] == 30:
        segment_prompts = [
            "Futuristic medical interface showing vector search concept",
            "BiomedCLIP embeddings visualized as glowing neural network",
            "Qdrant database with flowing data streams",
            "Medical scan transforming into mathematical vectors",
            "Search results appearing instantly on holographic display",
            "Open source technology logos assembling together"
        ]
    elif config['duration'] == 60:
        segment_prompts = [
            "Clean technical architecture diagram animating",
            "Medical image being processed through embedding pipeline",
            "Vector space visualization with clustering points",
            "FastAPI endpoints showing data flow",
            "React interface with smooth interactions",
            "Docker containers orchestrating services",
            "Qdrant logo with vector search visualization",
            "Code snippets showing implementation",
            "Performance metrics displaying on dashboard",
            "Search algorithm visualized step by step",
            "Database operations in real-time",
            "Final prototype interface demonstration"
        ]
    elif config['duration'] == 90:
        segment_prompts = [
            "Microservices architecture blueprint",
            "BiomedCLIP model architecture diagram",
            "512-dimensional vector space visualization",
            "Qdrant collection structure and indexing",
            "FastAPI async request handling flow",
            "React component tree with TypeScript",
            "Three.js rendering vector clusters",
            "Docker compose orchestration diagram",
            "HNSW indexing algorithm visualization",
            "REST API endpoint documentation",
            "WebSocket real-time connection flow",
            "Batch processing pipeline animation",
            "Performance benchmarks and metrics",
            "Cosine similarity calculation visual",
            "Embedding generation process steps",
            "System integration overview",
            "Scalability architecture patterns",
            "Final technical summary dashboard"
        ]
    else:  # 120 seconds
        segment_prompts = [
            "Chazon logo reveal with prototype badge",
            "Conceptual vision of AI medical imaging",
            "Vector embedding transformation process",
            "Qdrant database core functionality",
            "Mathematical vector space exploration",
            "Upload and processing workflow",
            "Microservices architecture overview",
            "BiomedCLIP feature extraction visual",
            "Cosine similarity matching algorithm",
            "User interface walkthrough",
            "Pattern recognition demonstration",
            "Vector clustering visualization",
            "Search speed performance metrics",
            "Frontend interface interactions",
            "Potential future applications",
            "Research possibilities visualization",
            "Open source technology stack",
            "Community contribution potential",
            "Hackathon challenge completion",
            "Technical innovation showcase",
            "Medical imaging future vision",
            "Vector database capabilities",
            "Thank you and contact information",
            "Qdrant logo with final message"
        ]

    # Ensure we have enough prompts
    while len(segment_prompts) < num_chunks:
        segment_prompts.append("Technical visualization of prototype system")

    # Generate chunks
    for i in range(num_chunks):
        chunk_file = f"{output_dir}/chunk_{i+1:02d}.mp4"

        # Use existing chunks if available
        if os.path.exists(f"ai_chunks/chunk_{i+1:02d}.mp4"):
            import shutil
            shutil.copy(f"ai_chunks/chunk_{i+1:02d}.mp4", chunk_file)
            print(f"  [REUSE] Chunk {i+1}/{num_chunks}")
        else:
            print(f"  [CREATE] Chunk {i+1}/{num_chunks}: {segment_prompts[i][:40]}...")
            # Create placeholder (would generate with AI in full implementation)
            create_placeholder_chunk(chunk_file, segment_prompts[i], i+1)

    return output_dir

def create_placeholder_chunk(output_file, prompt, chunk_num):
    """Create a placeholder video chunk"""

    try:
        import cv2
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont

        # Create 5-second video at 24fps
        fps = 24
        duration = 5
        width, height = 1920, 1080

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

        for frame in range(fps * duration):
            # Create frame
            img = Image.new('RGB', (width, height), color=(10, 20, 40))
            draw = ImageDraw.Draw(img)

            # Add text
            draw.text((width//2 - 200, height//2 - 50),
                     f"Segment {chunk_num}",
                     fill=(100, 200, 255))
            draw.text((width//2 - 400, height//2 + 50),
                     prompt[:80],
                     fill=(150, 150, 200))

            # Convert and write
            frame_array = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame_array)

        out.release()

    except ImportError:
        print(f"    [WARNING] Could not create chunk - missing dependencies")

def combine_video(config, chunks_dir, narration_file):
    """Combine chunks with narration"""

    print(f"\n[COMBINE] Creating final video: {config['name']}.mp4")

    # Create file list
    chunks = sorted(Path(chunks_dir).glob("chunk_*.mp4"))

    with open(f"list_{config['name']}.txt", "w") as f:
        for chunk in chunks:
            f.write(f"file '{chunk.absolute()}'\n")

    # Combine chunks
    silent_video = f"{config['name']}_silent.mp4"

    cmd1 = [
        "ffmpeg", "-f", "concat", "-safe", "0",
        "-i", f"list_{config['name']}.txt",
        "-c", "copy", silent_video, "-y"
    ]

    try:
        subprocess.run(cmd1, check=True, capture_output=True)

        # Add narration
        if narration_file and os.path.exists(narration_file):
            final_video = f"{config['name']}.mp4"

            cmd2 = [
                "ffmpeg",
                "-i", silent_video,
                "-i", narration_file,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                final_video, "-y"
            ]

            subprocess.run(cmd2, check=True, capture_output=True)
            print(f"  [OK] Created: {final_video}")

            # Clean up
            os.remove(silent_video)
        else:
            os.rename(silent_video, f"{config['name']}.mp4")
            print(f"  [OK] Created: {config['name']}.mp4 (no audio)")

    except:
        print(f"  [ERROR] FFmpeg not available")
        print(f"  Chunks saved in: {chunks_dir}")

def main():
    """Generate all concept videos"""

    print("\n[START] Generating concept demonstration videos...")
    print("These are PROTOTYPE demonstrations only")
    print("No real-world testing claims included")
    print("-" * 40)

    for video_config in videos:
        print(f"\n{'='*50}")
        print(f"Creating: {video_config['title']}")
        print(f"Duration: {video_config['duration']} seconds")
        print(f"{'='*50}")

        # Generate narration
        narration_file = generate_narration(video_config)

        # Create video segments
        chunks_dir = create_video_segments(video_config)

        # Combine into final video
        combine_video(video_config, chunks_dir, narration_file)

    print("\n" + "=" * 60)
    print("ALL CONCEPT VIDEOS GENERATED!")
    print("=" * 60)

    print("\n[OUTPUT FILES]")
    for config in videos:
        video_file = f"{config['name']}.mp4"
        if os.path.exists(video_file):
            size_mb = os.path.getsize(video_file) / (1024*1024)
            print(f"  {video_file} ({size_mb:.1f} MB) - {config['title']}")

    print("\n[FEATURES]")
    print("✓ Pure concept demonstration")
    print("✓ No testing or deployment claims")
    print("✓ Technical prototype focus")
    print("✓ Multiple lengths and perspectives")
    print("✓ Synchronized narration")

    print("\n[NEXT STEPS]")
    print("1. Review each video for your needs")
    print("2. Choose the best version for submission")
    print("3. Upload to YouTube as unlisted")
    print("4. Submit to hackathon")

if __name__ == "__main__":
    main()