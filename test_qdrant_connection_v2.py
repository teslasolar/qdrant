#!/usr/bin/env python3
"""
Test Qdrant Cloud connection with multiple configurations
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

# Load environment variables
load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Try different URL configurations
test_configs = [
    {
        "name": "With :6333 port",
        "url": "https://fb8ad99c-dfe1-4234-9f48-18b9155054d0.us-east-1-1.aws.cloud.qdrant.io:6333"
    },
    {
        "name": "Without port (default 6333)",
        "url": "https://fb8ad99c-dfe1-4234-9f48-18b9155054d0.us-east-1-1.aws.cloud.qdrant.io"
    },
    {
        "name": "With /api prefix",
        "url": "https://fb8ad99c-dfe1-4234-9f48-18b9155054d0.us-east-1-1.aws.cloud.qdrant.io/api"
    }
]

print("=" * 70)
print("🔌 Testing Qdrant Cloud Connection - Multiple Configurations")
print("=" * 70)
print(f"\nAPI Key: {'*' * 30}{QDRANT_API_KEY[-10:] if QDRANT_API_KEY else 'Not set'}")
print()

for config in test_configs:
    print("-" * 70)
    print(f"\n🧪 Testing: {config['name']}")
    print(f"   URL: {config['url']}")

    try:
        client = QdrantClient(
            url=config['url'],
            api_key=QDRANT_API_KEY,
            timeout=10,
            prefer_grpc=False
        )

        # Try to list collections
        collections = client.get_collections()

        print(f"   ✅ SUCCESS! Connected and fetched {len(collections.collections)} collections")

        for col in collections.collections:
            print(f"      • {col.name}")

        if not collections.collections:
            print("      (No collections yet)")

        print(f"\n✅ WORKING CONFIGURATION FOUND!")
        print(f"   URL: {config['url']}")
        print(f"\nUpdating .env file with working configuration...")

        # Update .env file
        env_content = f"""# AutomationGPT Environment Configuration

# Qdrant Cloud Configuration (WORKING)
QDRANT_URL={config['url']}
QDRANT_API_KEY={QDRANT_API_KEY}

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

        with open('os/backend/.env', 'w') as f:
            f.write(f"""# Qdrant Cloud Configuration
QDRANT_URL={config['url']}
QDRANT_API_KEY={QDRANT_API_KEY}
""")

        print("   ✅ .env files updated!")
        break

    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        continue

else:
    print("\n" + "=" * 70)
    print("❌ ALL CONFIGURATIONS FAILED")
    print("=" * 70)
    print("\nPossible issues:")
    print("  1. API key might be invalid or expired")
    print("  2. Cluster might be paused or deleted")
    print("  3. API key might have restricted permissions")
    print("\nPlease check:")
    print("  • Your Qdrant Cloud dashboard at https://cloud.qdrant.io")
    print("  • Verify the cluster is running")
    print("  • Check the API key permissions (should have 'Read' access)")
    print("  • Try generating a new API key")
