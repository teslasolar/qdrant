#!/usr/bin/env python3
"""
Test Qdrant Cloud connection
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

print("=" * 60)
print("🔌 Testing Qdrant Cloud Connection")
print("=" * 60)
print(f"\nQdrant URL: {QDRANT_URL}")
print(f"API Key: {'*' * 20}{QDRANT_API_KEY[-10:] if QDRANT_API_KEY else 'Not set'}")
print()

try:
    # Initialize client
    print("🔄 Connecting to Qdrant Cloud...")
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY,
        timeout=10
    )

    # Test connection by listing collections
    print("✅ Connected successfully!")
    print("\n📊 Fetching collections...")
    collections = client.get_collections()

    print(f"\n✅ Found {len(collections.collections)} collection(s):")
    for col in collections.collections:
        info = client.get_collection(col.name)
        print(f"  • {col.name}")
        print(f"    - Vectors: {info.points_count}")
        print(f"    - Dimension: {info.config.params.vectors.size if hasattr(info.config.params.vectors, 'size') else 'N/A'}")
        print(f"    - Distance: {info.config.params.vectors.distance if hasattr(info.config.params.vectors, 'distance') else 'N/A'}")

    if not collections.collections:
        print("  (No collections yet - this is normal for a new cluster)")

    print("\n" + "=" * 60)
    print("✅ CONNECTION TEST SUCCESSFUL!")
    print("=" * 60)
    print("\n🎉 Your Qdrant Cloud cluster is ready to use!")
    print("\nNext steps:")
    print("  1. Start backend: docker-compose up -d")
    print("  2. Load sample data: python collab/miracle/ingest_medical_data.py")
    print("  3. Open UI: open screens/frontend/medical-search.html")

except Exception as e:
    print("\n" + "=" * 60)
    print("❌ CONNECTION FAILED")
    print("=" * 60)
    print(f"\nError: {str(e)}")
    print("\nTroubleshooting:")
    print("  1. Check your QDRANT_URL is correct")
    print("  2. Verify your QDRANT_API_KEY is valid")
    print("  3. Ensure your Qdrant cluster is running")
    print("  4. Check your internet connection")
    exit(1)
