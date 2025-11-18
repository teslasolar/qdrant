#!/usr/bin/env python3
"""
Analyze Duplicate Files
Check if index.html files are truly duplicates or unique
"""

import os
import hashlib
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path("/home/user/qdrant")

def get_file_hash(filepath):
    """Get MD5 hash of file"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return None

def analyze_index_files():
    """Analyze index.html and index-custom.html files"""
    print("=== Analyzing index.html files ===\n")

    index_files = list(ROOT_DIR.rglob("index.html"))
    custom_files = list(ROOT_DIR.rglob("index-custom.html"))

    # Hash all files
    hash_to_files = defaultdict(list)

    print(f"Analyzing {len(index_files)} index.html files...")
    for f in index_files:
        h = get_file_hash(f)
        if h:
            hash_to_files[h].append(str(f))

    # Find duplicates
    duplicates = {h: files for h, files in hash_to_files.items() if len(files) > 1}

    print(f"\nFound {len(duplicates)} unique content hashes with duplicates")
    print(f"Total duplicate files: {sum(len(files) for files in duplicates.values())}")
    print(f"Unique index.html files: {len(hash_to_files)}")

    # Show top 5 most duplicated files
    print("\nTop 5 most duplicated index.html files:")
    sorted_dups = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)
    for i, (h, files) in enumerate(sorted_dups[:5], 1):
        print(f"\n{i}. Hash {h[:8]}... ({len(files)} copies):")
        for f in files[:5]:  # Show first 5 locations
            print(f"   - {f}")
        if len(files) > 5:
            print(f"   ... and {len(files) - 5} more")

    # Analyze custom files
    print("\n\n=== Analyzing index-custom.html files ===\n")
    custom_hash_to_files = defaultdict(list)

    print(f"Analyzing {len(custom_files)} index-custom.html files...")
    for f in custom_files:
        h = get_file_hash(f)
        if h:
            custom_hash_to_files[h].append(str(f))

    custom_duplicates = {h: files for h, files in custom_hash_to_files.items() if len(files) > 1}

    print(f"\nFound {len(custom_duplicates)} unique content hashes with duplicates")
    print(f"Total duplicate files: {sum(len(files) for files in custom_duplicates.values())}")
    print(f"Unique index-custom.html files: {len(custom_hash_to_files)}")

    return duplicates, custom_duplicates

def analyze_tag_json_files():
    """Analyze tag.json files"""
    print("\n\n=== Analyzing tag.json files ===\n")

    tag_files = list(ROOT_DIR.rglob("*/index/tag.json"))
    print(f"Found {len(tag_files)} tag.json files")

    # Check structure
    sizes = [f.stat().st_size for f in tag_files]
    print(f"Average size: {sum(sizes) / len(sizes):.0f} bytes")
    print(f"Min size: {min(sizes)} bytes")
    print(f"Max size: {max(sizes)} bytes")

if __name__ == "__main__":
    analyze_index_files()
    analyze_tag_json_files()
