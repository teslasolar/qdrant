#!/bin/bash
# CHAZON Medical Imaging SCADA - Quick Start Script
# For lablab.ai demo

set -e

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║       CHAZON Medical Imaging SCADA - Demo Mode           ║"
echo "║           Built for lablab.ai Hackathon                  ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "   Please install Python 3 and try again."
    exit 1
fi

# Convert config.yaml to config.json for browser access
echo "📝 Converting config.yaml to config.json..."
python3 << 'PYEOF'
import yaml
import json

try:
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("   ✓ Config converted successfully")
except ImportError:
    print("   ⚠️  PyYAML not installed. Installing...")
    import subprocess
    subprocess.check_call(['pip3', 'install', 'pyyaml'])
    
    # Try again
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("   ✓ Config converted successfully")
except Exception as e:
    print(f"   ❌ Error converting config: {e}")
    exit(1)
PYEOF

# Check port
PORT=8000
echo ""
echo "🚀 Starting development server on port $PORT..."
echo ""
echo "   Frontend Portal:    http://localhost:$PORT/screens/frontend/"
echo "   Enterprise Portal:  http://localhost:$PORT/screens/Enterprise/enterprise-portal.html"
echo "   Documentation:      http://localhost:$PORT/structure.md"
echo ""
echo "   Mode: DEMO (using mock AI, no GPU required)"
echo "   Sample data: Pre-loaded examples"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start Python HTTP server
python3 -m http.server $PORT
