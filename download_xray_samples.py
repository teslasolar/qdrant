#!/usr/bin/env python3
"""
Download sample X-ray images for testing Qdrant vector database
with medical imaging capabilities (Chazon project)
"""

import os
import requests
from pathlib import Path
import json

# Create base directory structure
BASE_DIR = Path("test-xrays")
CATEGORIES = ["normal", "pneumonia", "tuberculosis", "covid19"]

def ensure_directories():
    """Ensure all category directories exist"""
    for category in CATEGORIES:
        (BASE_DIR / category).mkdir(parents=True, exist_ok=True)
    print(f"[OK] Created directory structure in {BASE_DIR}")

def download_image(url, filepath):
    """Download an image from URL to filepath"""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  ✗ Failed to download {url}: {e}")
        return False

def download_sample_images():
    """
    Download sample X-ray images from publicly available sources
    Note: These are sample/demo images for testing purposes
    """

    # Sample public X-ray images (from open medical databases and research)
    # These are example URLs - replace with actual public dataset URLs
    sample_images = {
        "normal": [
            # Add URLs to normal chest X-ray images from public sources
            # Example: NIH dataset, Kaggle public samples, etc.
        ],
        "pneumonia": [
            # Add URLs to pneumonia X-ray images
        ],
        "tuberculosis": [
            # Add URLs to TB X-ray images
        ],
        "covid19": [
            # Add URLs to COVID-19 X-ray images
        ]
    }

    # Note: Since direct URLs to specific images aren't readily available,
    # you'll need to download from the datasets mentioned above

    print("\n" + "="*60)
    print("SAMPLE X-RAY IMAGE DOWNLOADER FOR QDRANT TESTING")
    print("="*60)

    print("\n📋 AVAILABLE FREE DATASETS:")
    print("\n1. KAGGLE - Paul Mooney's Chest X-ray Pneumonia Dataset")
    print("   URL: https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia")
    print("   Contents: 5,863 images (Normal & Pneumonia)")
    print("   Access: Free with Kaggle account")

    print("\n2. NIH Chest X-ray Dataset (ChestX-ray14)")
    print("   URL: https://nihcc.app.box.com/v/ChestXray-NIHCC")
    print("   Contents: 112,120 X-ray images with 14 disease labels")
    print("   Access: Free, no registration required")

    print("\n3. Montgomery County TB Dataset")
    print("   URL: http://archive.nlm.nih.gov/repos/chestImages.php")
    print("   Contents: 138 chest X-rays (80 normal, 58 TB)")
    print("   Access: Request form required")

    print("\n4. COVID-19 Radiography Database")
    print("   URL: https://www.kaggle.com/tawsifurrahman/covid19-radiography-database")
    print("   Contents: COVID-19, Normal, Viral Pneumonia images")
    print("   Access: Free with Kaggle account")

    print("\n5. Mendeley Data - COVID19, Pneumonia and Normal")
    print("   URL: https://data.mendeley.com/datasets/jctsfj2sfn/1")
    print("   Contents: 4,575 samples (1,525 each category)")
    print("   Access: Free with Mendeley account")

    print("\n" + "="*60)
    print("📥 DOWNLOAD INSTRUCTIONS:")
    print("="*60)

    print("\nFor quick testing, follow these steps:")
    print("\n1. KAGGLE DATASET (Recommended for quick start):")
    print("   a. Visit: https://www.kaggle.com/paultimothymooney/chest-xray-pneumonia")
    print("   b. Click 'Download' (requires free Kaggle account)")
    print("   c. Extract the zip file")
    print("   d. Copy sample images to test-xrays/ folders:")
    print("      - Normal images → test-xrays/normal/")
    print("      - Pneumonia images → test-xrays/pneumonia/")

    print("\n2. NIH DATASET (No registration required):")
    print("   a. Visit: https://nihcc.app.box.com/v/ChestXray-NIHCC")
    print("   b. Download images_001.tar.gz (or any subset)")
    print("   c. Extract and organize by disease labels")

    print("\n3. USING KAGGLE API (if installed):")
    print("   kaggle datasets download -d paultimothymooney/chest-xray-pneumonia")
    print("   unzip chest-xray-pneumonia.zip")

    print("\n" + "="*60)
    print("📊 SAMPLE IMAGE METADATA FORMAT")
    print("="*60)

    # Create sample metadata file
    sample_metadata = {
        "images": [
            {
                "filename": "normal_001.jpeg",
                "category": "normal",
                "patient_id": "P001",
                "body_part": "chest",
                "modality": "CR",  # Computed Radiography (X-Ray)
                "diagnosis": "Normal chest X-ray",
                "notes": "No abnormalities detected"
            },
            {
                "filename": "pneumonia_001.jpeg",
                "category": "pneumonia",
                "patient_id": "P002",
                "body_part": "chest",
                "modality": "CR",
                "diagnosis": "Bacterial pneumonia",
                "notes": "Consolidation in right lower lobe"
            },
            {
                "filename": "tb_001.jpeg",
                "category": "tuberculosis",
                "patient_id": "P003",
                "body_part": "chest",
                "modality": "CR",
                "diagnosis": "Pulmonary tuberculosis",
                "notes": "Cavitary lesion in upper lobe"
            },
            {
                "filename": "covid_001.jpeg",
                "category": "covid19",
                "patient_id": "P004",
                "body_part": "chest",
                "modality": "CR",
                "diagnosis": "COVID-19 pneumonia",
                "notes": "Bilateral ground-glass opacities"
            }
        ]
    }

    # Save sample metadata
    metadata_path = BASE_DIR / "sample_metadata.json"
    with open(metadata_path, 'w') as f:
        json.dump(sample_metadata, f, indent=2)
    print(f"\n✓ Created sample metadata file: {metadata_path}")

    print("\n" + "="*60)
    print("🔧 TESTING WITH QDRANT")
    print("="*60)

    print("\nOnce you have downloaded images, you can test with your Qdrant backend:")
    print("\n1. Upload and index images:")
    print("   POST https://qdrant-ygtw.onrender.com/medical/upload")
    print("   - Include image file and metadata")

    print("\n2. Search for similar cases:")
    print("   POST https://qdrant-ygtw.onrender.com/medical/search")
    print("   - Query with text or image similarity")

    print("\n3. Analyze images:")
    print("   POST https://qdrant-ygtw.onrender.com/medical/analyze")
    print("   - Get AI analysis and similar cases")

    print("\n" + "="*60)
    print("✅ Setup complete! Follow the instructions above to download X-ray images.")
    print("="*60)

def create_test_script():
    """Create a script to test Qdrant with the downloaded images"""
    test_script = '''#!/usr/bin/env python3
"""
Test script for Qdrant medical image indexing and search
"""

import requests
import json
from pathlib import Path
import base64

QDRANT_API = "https://qdrant-ygtw.onrender.com"

def test_health():
    """Test API health"""
    response = requests.get(f"{QDRANT_API}/health")
    print(f"Health Check: {response.json()}")

def upload_image(image_path, metadata):
    """Upload and index a medical image"""
    with open(image_path, 'rb') as f:
        files = {'file': (image_path.name, f, 'image/jpeg')}
        data = metadata
        response = requests.post(
            f"{QDRANT_API}/medical/upload",
            files=files,
            data=data
        )
    return response.json()

def search_similar(query_text=None, limit=5):
    """Search for similar medical cases"""
    payload = {
        "query": query_text,
        "limit": limit
    }
    response = requests.post(
        f"{QDRANT_API}/medical/search",
        json=payload
    )
    return response.json()

def main():
    print("Testing Qdrant Medical Imaging API...")

    # Test health
    test_health()

    # Example: Upload a normal chest X-ray
    # Uncomment when you have images
    # normal_image = Path("test-xrays/normal/normal_001.jpeg")
    # if normal_image.exists():
    #     result = upload_image(normal_image, {
    #         "patient_id": "TEST001",
    #         "body_part": "chest",
    #         "modality": "CR",
    #         "diagnosis": "Normal",
    #         "notes": "Test upload"
    #     })
    #     print(f"Upload result: {result}")

    # Search for similar cases
    # results = search_similar("pneumonia chest x-ray", limit=3)
    # print(f"Search results: {json.dumps(results, indent=2)}")

if __name__ == "__main__":
    main()
'''

    test_script_path = BASE_DIR / "test_qdrant.py"
    with open(test_script_path, 'w') as f:
        f.write(test_script)
    print(f"\n✓ Created test script: {test_script_path}")

    # Make it executable on Unix-like systems
    try:
        os.chmod(test_script_path, 0o755)
    except:
        pass  # Windows doesn't support chmod

if __name__ == "__main__":
    ensure_directories()
    download_sample_images()
    create_test_script()