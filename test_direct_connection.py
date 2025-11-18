#!/usr/bin/env python3
"""
Direct connection test with detailed diagnostics
"""
from qdrant_client import QdrantClient
import requests

# Latest API key from user
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.oB5D0q9b0if9zSgqiTNwwh56fSpHUuZOYHyPrlq4URk"

# All URLs to test
test_urls = [
    "https://fb8ad99c-dfe1-4234-9f48-18b9155054d0.us-east-1-1.aws.cloud.qdrant.io:6333",
    "https://1804f7b8-0370-4139-abae-cda8196770f4.us-east4-0.gcp.cloud.qdrant.io:6333",
    "https://qdrant-ygtw.onrender.com"
]

print("=" * 70)
print("🔌 Direct Connection Test")
print("=" * 70)
print(f"\nAPI Key: ...{API_KEY[-20:]}")
print()

for url in test_urls:
    print("-" * 70)
    print(f"\n🧪 Testing: {url}")

    # First try raw HTTP request
    print("\n  Method 1: Direct HTTP GET /collections")
    try:
        headers = {"api-key": API_KEY}
        response = requests.get(f"{url}/collections", headers=headers, timeout=10)
        print(f"    Status: {response.status_code}")
        print(f"    Response: {response.text[:200]}")

        if response.status_code == 200:
            print(f"    ✅ SUCCESS via HTTP!")
            data = response.json()
            print(f"    Collections: {len(data.get('result', {}).get('collections', []))}")

    except Exception as e:
        print(f"    ❌ HTTP failed: {str(e)[:100]}")

    # Try with Qdrant client
    print("\n  Method 2: QdrantClient")
    try:
        client = QdrantClient(
            url=url,
            api_key=API_KEY,
            timeout=10,
            prefer_grpc=False
        )
        collections = client.get_collections()
        print(f"    ✅ SUCCESS via QdrantClient!")
        print(f"    Collections: {len(collections.collections)}")

        for col in collections.collections:
            print(f"      • {col.name}")

        # THIS IS THE WORKING CONFIGURATION
        print(f"\n🎉 WORKING CONFIGURATION FOUND!")
        print(f"    URL: {url}")
        print(f"    API Key: ...{API_KEY[-20:]}")
        break

    except Exception as e:
        print(f"    ❌ Client failed: {str(e)[:200]}")

print("\n" + "=" * 70)
