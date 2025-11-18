#!/usr/bin/env python3
"""
Test script to verify image embedding models are working
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'os', 'backend'))

import numpy as np
from PIL import Image

# Import from api.py
from api import load_image_model, generate_image_embedding, IMAGE_MODEL_TYPE

def create_test_image():
    """Create a simple test medical image"""
    # Create a 224x224 grayscale image (simulated X-ray)
    image = np.random.randint(100, 200, (224, 224, 3), dtype=np.uint8)

    # Add a circular "abnormality"
    center_x, center_y = 112, 112
    radius = 30
    for x in range(224):
        for y in range(224):
            if (x - center_x)**2 + (y - center_y)**2 < radius**2:
                image[x, y] = [255, 255, 255]  # Bright spot

    return image

def main():
    print("=" * 60)
    print("🧪 Testing Image Embedding Models")
    print("=" * 60)

    # Load model
    print("\n1️⃣  Loading model...")
    load_image_model()
    print(f"   ✅ Model loaded: {IMAGE_MODEL_TYPE}")

    # Create test image
    print("\n2️⃣  Creating test medical image...")
    test_image = create_test_image()
    print(f"   ✅ Test image created: {test_image.shape}")

    # Generate embedding
    print("\n3️⃣  Generating embedding...")
    embedding = generate_image_embedding(test_image)
    print(f"   ✅ Embedding generated: {len(embedding)}-D")
    print(f"   📊 Sample values: {embedding[:5]}")
    print(f"   📊 Range: [{min(embedding):.4f}, {max(embedding):.4f}]")
    print(f"   📊 Mean: {np.mean(embedding):.4f}, Std: {np.std(embedding):.4f}")

    # Verify embedding
    print("\n4️⃣  Verifying embedding...")
    assert len(embedding) == 512, f"Expected 512-D, got {len(embedding)}-D"
    assert all(isinstance(x, (int, float)) for x in embedding), "Embedding contains non-numeric values"
    print(f"   ✅ Embedding is valid")

    # Test with different images
    print("\n5️⃣  Testing similarity...")
    test_image2 = create_test_image()
    embedding2 = generate_image_embedding(test_image2)

    # Cosine similarity
    dot_product = np.dot(embedding, embedding2)
    norm1 = np.linalg.norm(embedding)
    norm2 = np.linalg.norm(embedding2)
    similarity = dot_product / (norm1 * norm2)

    print(f"   📊 Similarity between two images: {similarity:.4f}")
    print(f"   ℹ️  (Should be high for similar images, low for different)")

    print("\n" + "=" * 60)
    print(f"✅ All tests passed! Model: {IMAGE_MODEL_TYPE}")
    print("=" * 60)

    # Performance test
    print("\n🚀 Performance Test...")
    import time

    num_images = 10
    start = time.time()
    for i in range(num_images):
        test_img = create_test_image()
        embedding = generate_image_embedding(test_img)
    end = time.time()

    avg_time = (end - start) / num_images * 1000  # ms
    print(f"   📊 Average embedding time: {avg_time:.1f} ms per image")

    if avg_time < 100:
        print(f"   🔥 Excellent! Very fast")
    elif avg_time < 500:
        print(f"   ✅ Good performance")
    else:
        print(f"   ⚠️  Slow - consider using GPU or simpler model")

    print("\nModel Summary:")
    print(f"  • Type: {IMAGE_MODEL_TYPE}")
    print(f"  • Embedding dimension: 512")
    print(f"  • Average speed: {avg_time:.1f} ms/image")
    print(f"  • Throughput: {1000/avg_time:.1f} images/second")

    if IMAGE_MODEL_TYPE == "biomedclip":
        print("\n🔥 Using BiomedCLIP - Best for medical images!")
    elif IMAGE_MODEL_TYPE == "resnet50":
        print("\n✅ Using ResNet50 - Good general purpose model")
    else:
        print("\n⚠️  Using statistical features - Consider installing PyTorch for better accuracy")

if __name__ == "__main__":
    main()
