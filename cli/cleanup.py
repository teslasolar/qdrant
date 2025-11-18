#!/usr/bin/env python3
"""
Cleanup Script - Remove Redundant Directory Structures
Removes duplicate controls/controls nesting and other redundancies
"""

import os
import shutil
from pathlib import Path

ROOT_DIR = Path("/home/user/qdrant")

def find_duplicate_controls():
    """Find all controls/controls duplicate patterns"""
    duplicates = []
    for root, dirs, files in os.walk(ROOT_DIR):
        if root.endswith('/controls/controls'):
            duplicates.append(Path(root))
    return duplicates

def remove_duplicate_controls(dry_run=True):
    """Remove duplicate controls/controls directories"""
    duplicates = find_duplicate_controls()

    print(f"Found {len(duplicates)} duplicate controls/controls directories:")
    for dup in duplicates:
        print(f"  - {dup}")

    if not duplicates:
        print("No duplicates found!")
        return

    if dry_run:
        print("\n[DRY RUN] No changes made. Run with dry_run=False to apply changes.")
        return

    print("\nRemoving duplicates...")
    for dup_dir in duplicates:
        parent_dir = dup_dir.parent  # This is the /controls/ directory

        # Move contents up one level
        if dup_dir.exists():
            # Check if there are subdirectories (hmi, plc, scada, tags)
            subdirs = [d for d in dup_dir.iterdir() if d.is_dir() and d.name != 'index']

            # Only remove if the subdirectories already exist at parent level
            all_exist_at_parent = all((parent_dir / d.name).exists() for d in subdirs)

            if all_exist_at_parent:
                print(f"  Removing redundant: {dup_dir}")
                shutil.rmtree(dup_dir)
            else:
                print(f"  Skipping (contents not duplicated): {dup_dir}")

    print("Cleanup complete!")

def find_other_redundancies():
    """Find other potential redundancies"""
    print("\n=== Checking for other redundancies ===\n")

    # Check for duplicate index.html files
    index_files = list(ROOT_DIR.rglob("index.html"))
    print(f"Found {len(index_files)} index.html files")

    # Check for duplicate index-custom.html files
    custom_files = list(ROOT_DIR.rglob("index-custom.html"))
    print(f"Found {len(custom_files)} index-custom.html files")

    # Check for empty directories
    empty_dirs = []
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip .git and node_modules
        if '.git' in root or 'node_modules' in root:
            continue
        if not dirs and not files:
            empty_dirs.append(root)

    print(f"Found {len(empty_dirs)} empty directories")
    for ed in empty_dirs[:10]:  # Show first 10
        print(f"  - {ed}")

if __name__ == "__main__":
    print("=== QDRANT Directory Cleanup Tool ===\n")

    # Find duplicates
    remove_duplicate_controls(dry_run=True)

    # Find other issues
    find_other_redundancies()

    print("\n=== Run with dry_run=False to apply changes ===")
