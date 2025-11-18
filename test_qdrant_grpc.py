#!/usr/bin/env python3
"""
Test Qdrant Cloud connection using gRPC (port 6334)
"""
import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

load_dotenv()

QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Try gRPC connection (port 6334)
test_configs = [
    {
        "name": "gRPC with prefer_grpc=True",
        "url": "https://fb8ad99c-dfe1-4234-9f48-18b9155054d0.us-east-1-1.aws.cloud.qdrant.io:6334",
        "prefer_grpc": True
    },
    {
        "name": "gRPC without port (auto 6334)",
        "url": "https://fb8ad99c-dfe1-4234-9f48-18b9155054d0.us-east-1-1.aws.cloud.qdrant.io",
        "prefer_grpc": True
    },
    {
        "name": "HTTP with port 6333",
        "url": "https://fb8ad99c-dfe1-4234-9f48-18b9155054d0.us-east-1-1.aws.cloud.qdrant.io:6333",
        "prefer_grpc": False
    },
    {
        "name": "Just host, prefer gRPC",
        "host": "fb8ad99c-dfe1-4234-9f48-18b9155054d0.us-east-1-1.aws.cloud.qdrant.io",
        "port": 6334,
        "https": True,
        "prefer_grpc": True
    }
]

print("=" * 70)
print("🔌 Testing Qdrant Cloud - gRPC Connection")
print("=" * 70)
print(f"\nAPI Key: {'*' * 30}{QDRANT_API_KEY[-10:] if QDRANT_API_KEY else 'Not set'}")
print()

for config in test_configs:
    print("-" * 70)
    print(f"\n🧪 Testing: {config['name']}")

    try:
        if 'host' in config:
            print(f"   Host: {config['host']}")
            print(f"   Port: {config['port']}")
            print(f"   HTTPS: {config['https']}")
            print(f"   prefer_grpc: {config['prefer_grpc']}")

            client = QdrantClient(
                host=config['host'],
                port=config['port'],
                https=config['https'],
                api_key=QDRANT_API_KEY,
                prefer_grpc=config['prefer_grpc'],
                timeout=10
            )
        else:
            print(f"   URL: {config['url']}")
            print(f"   prefer_grpc: {config['prefer_grpc']}")

            client = QdrantClient(
                url=config['url'],
                api_key=QDRANT_API_KEY,
                prefer_grpc=config['prefer_grpc'],
                timeout=10
            )

        # Try to list collections
        collections = client.get_collections()

        print(f"   ✅ SUCCESS! Connected and fetched {len(collections.collections)} collections")

        for col in collections.collections:
            print(f"      • {col.name}")

        if not collections.collections:
            print("      (No collections yet - this is normal)")

        print(f"\n🎉 WORKING CONFIGURATION FOUND!")

        # Update .env with working config
        if 'host' in config:
            working_url = f"https://{config['host']}:{config['port']}"
        else:
            working_url = config['url']

        print(f"   Working URL: {working_url}")
        print(f"   Prefer gRPC: {config['prefer_grpc']}")
        print(f"\nUpdating configuration files...")

        env_content = f"""# AutomationGPT Environment Configuration

# Qdrant Cloud Configuration (WORKING)
QDRANT_URL={working_url}
QDRANT_API_KEY={QDRANT_API_KEY}
QDRANT_PREFER_GRPC={'true' if config['prefer_grpc'] else 'false'}

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
QDRANT_URL={working_url}
QDRANT_API_KEY={QDRANT_API_KEY}
QDRANT_PREFER_GRPC={'true' if config['prefer_grpc'] else 'false'}
""")

        print("   ✅ Configuration files updated!")
        break

    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        continue

else:
    print("\n" + "=" * 70)
    print("❌ ALL CONFIGURATIONS FAILED")
    print("=" * 70)
    print("\nThe cluster might be:")
    print("  1. Paused or stopped")
    print("  2. Using different authentication")
    print("  3. Configured with IP allowlist")
    print("\nPlease verify in your Qdrant Cloud dashboard")
