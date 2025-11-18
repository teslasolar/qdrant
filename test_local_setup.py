#!/usr/bin/env python3
"""
Quick test of local Qdrant setup
"""
from dotenv import load_dotenv
from qdrant_client import QdrantClient
import os

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

print("=" * 60)
print("🧪 Testing Local Qdrant Setup")
print("=" * 60)
print(f"\nQdrant URL: {QDRANT_URL}")
print(f"API Key: {'Not required (local)' if not os.getenv('QDRANT_API_KEY') else 'Set'}")
print()

try:
    print("🔄 Connecting to local Qdrant...")
    client = QdrantClient(url=QDRANT_URL, timeout=5)

    collections = client.get_collections()

    print(f"✅ Connected successfully!")
    print(f"\n📊 Collections: {len(collections.collections)}")

    for col in collections.collections:
        info = client.get_collection(col.name)
        print(f"  • {col.name}: {info.points_count} points")

    if not collections.collections:
        print("  (No collections yet - run ingestion script)")

    print("\n" + "=" * 60)
    print("✅ LOCAL QDRANT IS READY!")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Load sample data: python collab/miracle/ingest_medical_data.py")
    print("  2. Open UI: open screens/frontend/medical-search.html")

except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nMake sure to start Qdrant first:")
    print("  docker-compose up -d")
