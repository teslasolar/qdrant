#!/usr/bin/env python3
"""
Streamline QDRANT Project
Remove redundancies and optimize directory structure
"""

import os
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path("/home/user/qdrant")

def get_file_hash(filepath):
    """Get MD5 hash of file"""
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception:
        return None

def remove_duplicate_controls(dry_run=True):
    """Remove duplicate controls/controls directories"""
    print("=== Removing Duplicate controls/controls Directories ===\n")

    duplicates = []
    for root, dirs, files in os.walk(ROOT_DIR):
        if root.endswith('/controls/controls'):
            duplicates.append(Path(root))

    print(f"Found {len(duplicates)} duplicate controls/controls directories")

    removed = 0
    for dup_dir in duplicates:
        parent_dir = dup_dir.parent  # The /controls/ directory

        if not dup_dir.exists():
            continue

        # Get subdirectories (hmi, plc, scada, tags)
        subdirs = [d for d in dup_dir.iterdir() if d.is_dir() and d.name != 'index']

        # Check if these already exist at parent level
        all_exist_at_parent = all((parent_dir / d.name).exists() for d in subdirs)

        if all_exist_at_parent or len(subdirs) == 0:
            print(f"  Removing: {dup_dir.relative_to(ROOT_DIR)}")
            if not dry_run:
                shutil.rmtree(dup_dir)
            removed += 1

    print(f"\nWould remove {removed} directories" if dry_run else f"\nRemoved {removed} directories")
    return removed

def clean_duplicate_html_files(dry_run=True):
    """Remove duplicate index.html files, keeping only essential ones"""
    print("\n=== Cleaning Duplicate index.html Files ===\n")

    # Find all index.html files
    index_files = list(ROOT_DIR.rglob("index.html"))

    # Hash them
    hash_to_files = defaultdict(list)
    for f in index_files:
        h = get_file_hash(f)
        if h:
            hash_to_files[h].append(f)

    # Find the most common hash (the duplicate one)
    most_common_hash = max(hash_to_files.items(), key=lambda x: len(x[1]))[0]
    duplicate_files = hash_to_files[most_common_hash]

    print(f"Found {len(duplicate_files)} copies of the same index.html file")

    # Keep only essential locations
    essential_paths = [
        ROOT_DIR / "index.html",  # Root
        ROOT_DIR / "os" / "index.html",  # OS
        ROOT_DIR / "templates" / "example-hmi.html",  # Template example
    ]

    # Files to remove
    to_remove = []
    for f in duplicate_files:
        # Keep if it's in essential paths
        if f not in essential_paths:
            # Also keep if it's in a control structure we want (hmi, plc, scada)
            path_str = str(f)
            if not any(essential in path_str for essential in ['/hmi/', '/plc/', '/scada/', '/controls/']):
                to_remove.append(f)

    print(f"Will remove {len(to_remove)} duplicate index.html files")
    print(f"Keeping {len(duplicate_files) - len(to_remove)} essential copies")

    if not dry_run:
        for f in to_remove:
            f.unlink()
            print(f"  Removed: {f.relative_to(ROOT_DIR)}")

    return len(to_remove)

def create_symlinks_for_templates(dry_run=True):
    """Create symlinks to template files instead of duplicates"""
    print("\n=== Creating Symlinks for Templates ===\n")

    # Instead of copying index.html everywhere, create symlinks
    template_index = ROOT_DIR / "templates" / "example-hmi.html"

    if not template_index.exists():
        print("Template file not found, skipping")
        return 0

    print("Would create symlinks (not implemented in dry run)")
    return 0

def generate_summary():
    """Generate summary report"""
    print("\n" + "="*60)
    print("STREAMLINE SUMMARY")
    print("="*60 + "\n")

    # Count various items
    controls_dirs = len(list(ROOT_DIR.rglob("*/controls/controls")))
    index_files = len(list(ROOT_DIR.rglob("index.html")))
    custom_files = len(list(ROOT_DIR.rglob("index-custom.html")))
    tag_files = len(list(ROOT_DIR.rglob("*/index/tag.json")))

    print(f"Current State:")
    print(f"  - Duplicate controls/controls dirs: {controls_dirs}")
    print(f"  - index.html files: {index_files}")
    print(f"  - index-custom.html files: {custom_files}")
    print(f"  - tag.json files: {tag_files}")

    # Calculate sizes
    total_size = sum(f.stat().st_size for f in ROOT_DIR.rglob("*") if f.is_file())
    print(f"\n  Total project size: {total_size / (1024*1024):.1f} MB")

def main(dry_run=True):
    """Main streamline function"""
    print("="*60)
    print("QDRANT PROJECT STREAMLINING TOOL")
    print("="*60 + "\n")

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be made\n")
    else:
        print("⚠️  LIVE MODE - Changes will be applied!\n")

    # Show current state
    generate_summary()

    # Perform cleanup
    controls_removed = remove_duplicate_controls(dry_run)
    # html_removed = clean_duplicate_html_files(dry_run)

    print("\n" + "="*60)
    print("RESULTS")
    print("="*60 + "\n")

    print(f"Duplicate controls/controls removed: {controls_removed}")
    # print(f"Duplicate index.html files removed: {html_removed}")

    if dry_run:
        print("\n✅ Dry run complete. Run with --apply to make changes.")
    else:
        print("\n✅ Streamlining complete!")

if __name__ == "__main__":
    import sys
    dry_run = "--apply" not in sys.argv

    main(dry_run=dry_run)
