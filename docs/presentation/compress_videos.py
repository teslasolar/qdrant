#!/usr/bin/env python3
"""
Compress Videos to Smaller Sizes
Makes videos suitable for GitHub and easy sharing
"""

import os
import subprocess
import imageio_ffmpeg as ffmpeg

print("=" * 60)
print("VIDEO COMPRESSION TOOL")
print("Making videos smaller for easy upload")
print("=" * 60)

# Get ffmpeg from imageio
ffmpeg_exe = ffmpeg.get_ffmpeg_exe()
print(f"\n[FFMPEG] Using: {ffmpeg_exe}")

# Video compression configurations
compression_configs = [
    {
        "input": "chazon_clean_3min.mp4",
        "output": "chazon_3min_compressed.mp4",
        "target_size": "25MB",
        "bitrate": "1100k",
        "scale": "1280:720",
        "preset": "fast"
    },
    {
        "input": "chazon_concept_2min.mp4",
        "output": "chazon_2min_compressed.mp4",
        "target_size": "15MB",
        "bitrate": "1000k",
        "scale": "1280:720",
        "preset": "fast"
    },
    {
        "input": "chazon_concept_90s.mp4",
        "output": "chazon_90s_compressed.mp4",
        "target_size": "10MB",
        "bitrate": "900k",
        "scale": "1280:720",
        "preset": "fast"
    },
    {
        "input": "chazon_concept_60s.mp4",
        "output": "chazon_60s_compressed.mp4",
        "target_size": "8MB",
        "bitrate": "1000k",
        "scale": "960:540",
        "preset": "fast"
    },
    {
        "input": "chazon_concept_30s.mp4",
        "output": "chazon_30s_compressed.mp4",
        "target_size": "5MB",
        "bitrate": "1300k",
        "scale": "960:540",
        "preset": "fast"
    }
]

def compress_video(config):
    """Compress a video to smaller size"""

    input_file = config["input"]
    output_file = config["output"]

    if not os.path.exists(input_file):
        print(f"  [SKIP] {input_file} not found")
        return None

    # Get original size
    original_size = os.path.getsize(input_file) / (1024*1024)
    print(f"\n[COMPRESS] {input_file}")
    print(f"  Original: {original_size:.1f} MB")
    print(f"  Target: {config['target_size']}")

    # Compression command with multiple passes for quality
    cmd = [
        ffmpeg_exe,
        "-i", input_file,
        "-c:v", "libx264",  # H.264 codec
        "-preset", config["preset"],  # Encoding speed
        "-crf", "23",  # Quality (lower = better, 18-28 is good range)
        "-b:v", config["bitrate"],  # Video bitrate
        "-maxrate", config["bitrate"],
        "-bufsize", "2M",
        "-vf", f"scale={config['scale']}",  # Resolution
        "-c:a", "aac",  # Audio codec
        "-b:a", "128k",  # Audio bitrate
        "-ar", "44100",  # Audio sample rate
        "-movflags", "+faststart",  # Web optimization
        output_file,
        "-y"  # Overwrite
    ]

    try:
        print("  [PROCESSING] Compressing video...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            new_size = os.path.getsize(output_file) / (1024*1024)
            reduction = (1 - new_size/original_size) * 100
            print(f"  [SUCCESS] New size: {new_size:.1f} MB ({reduction:.1f}% reduction)")
            return output_file
        else:
            print(f"  [ERROR] Compression failed")
            return None

    except Exception as e:
        print(f"  [ERROR] {e}")
        return None

def create_ultra_compressed(input_file, output_file, max_size_mb=10):
    """Create ultra-compressed version for GitHub"""

    if not os.path.exists(input_file):
        return None

    print(f"\n[ULTRA] Creating ultra-compressed {output_file}")
    print(f"  Max size: {max_size_mb} MB")

    # Calculate bitrate for target size
    # Get video duration first
    probe_cmd = [
        ffmpeg_exe,
        "-i", input_file,
        "-f", "null", "-"
    ]

    # Ultra compression settings
    cmd = [
        ffmpeg_exe,
        "-i", input_file,
        "-c:v", "libx264",
        "-preset", "veryslow",  # Best compression
        "-crf", "28",  # Lower quality for smaller size
        "-vf", "scale=854:480",  # 480p resolution
        "-c:a", "aac",
        "-b:a", "96k",  # Lower audio bitrate
        "-ar", "22050",  # Lower sample rate
        "-ac", "1",  # Mono audio
        "-movflags", "+faststart",
        output_file,
        "-y"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            size = os.path.getsize(output_file) / (1024*1024)
            print(f"  [SUCCESS] Ultra-compressed: {size:.1f} MB")
            return output_file
    except:
        pass

    return None

def create_gif_preview(input_file, output_gif, duration=5):
    """Create animated GIF preview"""

    if not os.path.exists(input_file):
        return None

    print(f"\n[GIF] Creating preview GIF from {input_file}")

    # Create palette for better quality
    palette_file = "palette.png"

    # Generate palette
    cmd1 = [
        ffmpeg_exe,
        "-i", input_file,
        "-t", str(duration),
        "-vf", "fps=10,scale=320:-1:flags=lanczos,palettegen",
        palette_file,
        "-y"
    ]

    # Create GIF using palette
    cmd2 = [
        ffmpeg_exe,
        "-i", input_file,
        "-i", palette_file,
        "-t", str(duration),
        "-filter_complex", "fps=10,scale=320:-1:flags=lanczos[x];[x][1:v]paletteuse",
        output_gif,
        "-y"
    ]

    try:
        subprocess.run(cmd1, capture_output=True)
        subprocess.run(cmd2, capture_output=True)

        if os.path.exists(output_gif):
            size = os.path.getsize(output_gif) / (1024*1024)
            print(f"  [SUCCESS] GIF created: {size:.1f} MB")

            # Clean up palette
            if os.path.exists(palette_file):
                os.remove(palette_file)

            return output_gif
    except:
        pass

    return None

def main():
    """Main compression process"""

    print("\n[START] Compressing videos for easy sharing...")

    compressed_files = []

    # Regular compression
    for config in compression_configs:
        result = compress_video(config)
        if result:
            compressed_files.append(result)

    # Ultra-compressed versions for GitHub (under 10MB)
    print("\n[GITHUB] Creating ultra-compressed versions (<10MB)...")

    ultra_files = [
        ("chazon_clean_3min.mp4", "chazon_3min_github.mp4"),
        ("chazon_concept_60s.mp4", "chazon_60s_github.mp4"),
        ("chazon_concept_30s.mp4", "chazon_30s_github.mp4")
    ]

    for input_file, output_file in ultra_files:
        result = create_ultra_compressed(input_file, output_file, max_size_mb=10)
        if result:
            compressed_files.append(result)

    # Create GIF previews
    print("\n[PREVIEW] Creating animated GIF previews...")

    gif_files = [
        ("chazon_concept_30s.mp4", "preview_30s.gif", 10),
        ("final_emergency_triage_10s.mp4", "preview_emergency.gif", 5),
        ("final_rural_access_10s.mp4", "preview_rural.gif", 5)
    ]

    for input_file, output_gif, duration in gif_files:
        result = create_gif_preview(input_file, output_gif, duration)
        if result:
            compressed_files.append(result)

    # Summary
    print("\n" + "=" * 60)
    print("COMPRESSION COMPLETE!")
    print("=" * 60)

    print("\n[COMPRESSED FILES]")
    for file in compressed_files:
        if os.path.exists(file):
            size = os.path.getsize(file) / (1024*1024)
            print(f"  {file}: {size:.1f} MB")

    print("\n[FILE CATEGORIES]")
    print("  *_compressed.mp4 - High quality, smaller size")
    print("  *_github.mp4 - Ultra-compressed for GitHub (<10MB)")
    print("  *.gif - Animated previews for README")

    print("\n[RECOMMENDED USE]")
    print("  1. Use *_compressed.mp4 for main submission")
    print("  2. Upload *_github.mp4 directly to GitHub")
    print("  3. Use GIFs in README for visual preview")
    print("  4. Host original files on YouTube/Drive")

if __name__ == "__main__":
    main()