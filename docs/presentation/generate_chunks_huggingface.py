
from gradio_client import Client
import json
import time
import subprocess

# Load chunk definitions
with open("video_chunks.json") as f:
    chunks = json.load(f)

def generate_batch(batch_chunks, batch_num):
    """Generate a batch of chunks"""

    print(f"\nBatch {batch_num}: Generating {len(batch_chunks)} chunks")

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
