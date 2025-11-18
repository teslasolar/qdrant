
import os
from huggingface_hub import snapshot_download
from tqdm import tqdm

print("\nDownloading AI video generation models...")
print("This will download approximately 11GB of models")
print("-" * 50)

# Create models directory
os.makedirs("models", exist_ok=True)

models_to_download = [
    {
        "name": "ZeroScope V2 (Fast, 1.7GB)",
        "repo": "cerspense/zeroscope_v2_576w",
        "path": "models/zeroscope"
    },
    {
        "name": "ModelScope Text2Video (3.5GB)",
        "repo": "damo-vilab/text-to-video-ms-1.7b",
        "path": "models/modelscope"
    },
    {
        "name": "AnimateDiff Motion Module (1.7GB)",
        "repo": "guoyww/animatediff-motion-adapter-v1-5-2",
        "path": "models/animatediff-motion"
    },
    {
        "name": "Stable Diffusion 1.5 Base (4.3GB)",
        "repo": "runwayml/stable-diffusion-v1-5",
        "path": "models/sd15"
    }
]

for i, model in enumerate(models_to_download, 1):
    print(f"\n[{i}/4] Downloading {model['name']}...")
    print(f"      Repository: {model['repo']}")
    print(f"      Saving to: {model['path']}")

    try:
        snapshot_download(
            repo_id=model['repo'],
            local_dir=model['path'],
            resume_download=True,
            ignore_patterns=["*.bin"] if "stable-diffusion" in model['repo'] else None
        )
        print(f"      [OK] Downloaded successfully!")
    except Exception as e:
        print(f"      [ERROR] Failed: {e}")
        print(f"      Manual download: https://huggingface.co/{model['repo']}")

print("\n" + "=" * 50)
print("MODEL DOWNLOAD COMPLETE!")
print("=" * 50)
