
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
            f.write(f"file 'chunk_{i:02d}.mp4'\n")

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

    print("\nVideo assembly complete!")
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
