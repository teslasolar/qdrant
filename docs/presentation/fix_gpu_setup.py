#!/usr/bin/env python3
"""
Fix GPU Setup - Install CUDA-enabled PyTorch
"""

import subprocess
import sys
import torch

print("=" * 60)
print("FIXING GPU SETUP FOR RTX 4070 Ti SUPER")
print("=" * 60)

# Check current PyTorch
print("\n[CHECK] Current PyTorch status:")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")

if not torch.cuda.is_available():
    print("\n[FIX] Installing CUDA-enabled PyTorch...")

    # Uninstall CPU-only version
    print("[UNINSTALL] Removing CPU-only PyTorch...")
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "torch", "torchvision", "torchaudio", "-y"])

    # Install CUDA version for RTX 4070 Ti (CUDA 12.1)
    print("[INSTALL] Installing PyTorch with CUDA 12.1...")
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "torch", "torchvision", "torchaudio",
        "--index-url", "https://download.pytorch.org/whl/cu121"
    ])

    # Reinstall xformers for CUDA
    print("[INSTALL] Installing xformers for CUDA...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "xformers", "--upgrade"])

    print("\n[CHECK] Verifying GPU setup...")
    import torch
    if torch.cuda.is_available():
        print(f"✅ CUDA is now available!")
        print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
        print(f"✅ VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("❌ CUDA still not available - may need system restart")
else:
    print("✅ GPU is already properly configured!")

print("\n[DONE] GPU setup complete!")