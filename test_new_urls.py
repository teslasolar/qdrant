#!/usr/bin/env python3
"""
Test new Qdrant URLs
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# New URLs to test
test_configs = [
    {
        "name": "Render deployment",
        "url": "https://qdrant-ygtw.onrender.com",
        "api_key_required": True
    },
    {
        "name": "Render deployment with port",
        "url": "https://qdrant-ygtw.onrender.com:6333",
        "api_key_required": True
    },
    {
        "name": "GCP Cloud (new cluster)",
        "url": "https://1804f7b8-0370-4139-abae-cda8196770f4.us-east4-0.gcp.cloud.qdrant.io",
        "api_key_required": True
    },
    {
        "name": "GCP Cloud with port",
        "url": "https://1804f7b8-0370-4139-abae-cda8196770f4.us-east4-0.gcp.cloud.qdrant.io:6333",
        "api_key_required": True
    },
    {
        "name": "Render without API key (public)",
        "url": "https://qdrant-ygtw.onrender.com",
        "api_key_required": False
    }
]

print("=" * 70)
print("🔌 Testing New Qdrant URLs")
print("=" * 70)
print(f"\nAPI Key: {'*' * 30}{QDRANT_API_KEY[-10:] if QDRANT_API_KEY else 'Not set'}")
print()

working_config = None

for config in test_configs:
    print("-" * 70)
    print(f"\n🧪 Testing: {config['name']}")
    print(f"   URL: {config['url']}")
    print(f"   API Key: {'Yes' if config['api_key_required'] else 'No (public)'}")

    try:
        if config['api_key_required']:
            client = QdrantClient(
                url=config['url'],
                api_key=QDRANT_API_KEY,
                timeout=15,
                prefer_grpc=False
            )
        else:
            client = QdrantClient(
                url=config['url'],
                timeout=15,
                prefer_grpc=False
            )

        # Try to list collections
        collections = client.get_collections()

        print(f"   ✅ SUCCESS! Connected and fetched {len(collections.collections)} collections")

        if collections.collections:
            for col in collections.collections:
                info = client.get_collection(col.name)
                print(f"      • {col.name}")
                print(f"        - Points: {info.points_count}")
                print(f"        - Dimension: {info.config.params.vectors.size if hasattr(info.config.params.vectors, 'size') else 'N/A'}")
        else:
            print("      (No collections yet - this is normal for a new cluster)")

        print(f"\n🎉 WORKING CONFIGURATION FOUND!")
        working_config = config
        break

    except Exception as e:
        error_msg = str(e)
        if len(error_msg) > 200:
            error_msg = error_msg[:200] + "..."
        print(f"   ❌ Failed: {error_msg}")
        continue

if working_config:
    print("\n" + "=" * 70)
    print("✅ SUCCESS - Updating Configuration")
    print("=" * 70)

    working_url = working_config['url']
    use_api_key = working_config['api_key_required']

    print(f"\nWorking URL: {working_url}")
    print(f"API Key Required: {use_api_key}")

    # Update .env files
    env_content = f"""# AutomationGPT Environment Configuration

# Qdrant Configuration (WORKING)
QDRANT_URL={working_url}
QDRANT_API_KEY={QDRANT_API_KEY if use_api_key else ''}

# AI API Keys (Optional - for text embeddings)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
"""

    with open('.env', 'w') as f:
        f.write(env_content)

    backend_env = f"""# Qdrant Configuration
QDRANT_URL={working_url}
QDRANT_API_KEY={QDRANT_API_KEY if use_api_key else ''}
"""

    with open('os/backend/.env', 'w') as f:
        f.write(backend_env)

    print("\n✅ Configuration files updated!")
    print("\n🚀 Next steps:")
    print("  1. Start backend: docker-compose up -d")
    print("  2. Load sample data: python collab/miracle/ingest_medical_data.py")
    print("  3. Open UI: open screens/frontend/medical-search.html")

else:
    print("\n" + "=" * 70)
    print("❌ NO WORKING CONFIGURATION FOUND")
    print("=" * 70)
    print("\nPlease verify:")
    print("  • The URLs are correct")
    print("  • The API key is valid")
    print("  • The clusters are running")
    print("  • Network connectivity is working")
