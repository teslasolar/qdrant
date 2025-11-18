
import replicate
import requests
import os
import json

# Load chunk definitions
with open("video_chunks.json") as f:
    chunks = json.load(f)

# Set your Replicate API token
os.environ["REPLICATE_API_TOKEN"] = "YOUR_TOKEN_HERE"

def generate_chunk(chunk):
    """Generate a single 5-second chunk"""

    print(f"Generating chunk {chunk['id']}: {chunk['start']}-{chunk['end']}s")

    # Using Zeroscope for fast generation
    output = replicate.run(
        "anotherjesse/zeroscope-v2-xl:9f747673945c62801b13b84701c783929c0ee784e4748ec062204894dda1a351",
        input={
            "prompt": chunk['prompt'] + ", high quality, cinematic, medical visualization",
            "num_frames": 120,  # 5 seconds at 24 fps
            "width": 1024,
            "height": 576,
            "guidance_scale": 7.5,
            "num_inference_steps": 25
        }
    )

    # Download the chunk
    response = requests.get(output)
    filename = f"chunk_{chunk['id']:02d}.mp4"

    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"  Saved: {filename}")
    return filename

# Generate all chunks
generated_files = []
for chunk in chunks:
    try:
        file = generate_chunk(chunk)
        generated_files.append(file)
        time.sleep(2)  # Rate limiting
    except Exception as e:
        print(f"  Error generating chunk {chunk['id']}: {e}")

print(f"Generated {len(generated_files)} chunks successfully!")
