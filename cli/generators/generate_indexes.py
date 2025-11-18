#!/usr/bin/env python3
"""
Generate index directories and tag data for all directories
Creates structured index data following ISA UDT specifications

This script generates index.html loaders and tag.json metadata files for
every directory in the project. It prevents duplicate directory creation
and validates the directory structure before making changes.

Features:
- Duplicate directory detection and prevention
- Dry-run mode for safe testing
- Comprehensive validation
- Detailed logging and statistics
- ISA-95 level categorization
- Automatic backup of custom index files

Usage:
    python generate_indexes.py          # Normal run
    python generate_indexes.py --dry-run  # Test without making changes
    python generate_indexes.py --verbose  # Detailed output
"""

import os
import sys
import json
import uuid
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict

ROOT_DIR = Path("/home/user/qdrant")

# Parse command-line arguments
DRY_RUN = '--dry-run' in sys.argv
VERBOSE = '--verbose' in sys.argv or DRY_RUN

# ISA-95 Level categorization
CATEGORY_MAP = {
    'cli': 'L3_MES',
    'docs': 'L4_Business',
    'collab': 'L4_Business',
    'os': 'L3_MES',
    'os/backend': 'L3_MES',
    'os/frontend': 'L3_MES',
    'os/modules': 'L3_MES',
    'os/boot': 'L3_MES',
    'os/models': 'L3_MES',
    'os/medical': 'L3_MES',
    'os/data': 'L3_MES',
    'os/language': 'L3_MES',
    'os/controls': 'L2_Supervisory',
    'os/equipment': 'L2_Supervisory',
    'os/logs': 'L2_Supervisory',
    'os/templates': 'L3_MES',
}

# Icon mapping
ICON_MAP = {
    'backend': '⚙️',
    'frontend': '🖥️',
    'modules': '📦',
    'boot': '🚀',
    'models': '🤖',
    'medical': '🏥',
    'data': '📊',
    'language': '🌐',
    'controls': '🎛️',
    'equipment': '🏭',
    'logs': '📝',
    'templates': '📄',
    'docs': '📚',
    'collab': '👥',
    'cli': '⌨️',
    'os': '💻',
}

# Color scheme mapping
COLOR_MAP = {
    'L4_Business': 'green',
    'L3_MES': 'blue',
    'L2_Supervisory': 'purple',
    'L1_Control': 'orange',
    'L0_Physical': 'red',
}

def get_category(dir_path: Path) -> str:
    """Determine ISA-95 category from path"""
    rel_path = dir_path.relative_to(ROOT_DIR)
    path_str = str(rel_path)

    # Check exact matches first
    for key, cat in CATEGORY_MAP.items():
        if path_str == key or path_str.startswith(key + '/'):
            return cat

    # Default categorization
    if 'controls' in path_str or 'tag-providers' in path_str:
        return 'L2_Supervisory'
    elif 'plc' in path_str.lower():
        return 'L1_Control'
    elif 'os/' in path_str:
        return 'L3_MES'
    elif 'docs/' in path_str:
        return 'L4_Business'

    return 'L4_Business'

def get_icon(dir_name: str) -> str:
    """Get icon for directory"""
    for key, icon in ICON_MAP.items():
        if key in dir_name.lower():
            return icon
    return '📁'

def get_child_directories(dir_path: Path) -> List[Dict[str, str]]:
    """Get list of child directories"""
    children = []
    try:
        for item in sorted(dir_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.') and item.name not in ['node_modules', '__pycache__', 'index']:
                rel_path = item.relative_to(ROOT_DIR)
                children.append({
                    'path': f"/{rel_path}/",
                    'title': item.name.replace('_', ' ').replace('-', ' ').title(),
                    'description': f"{item.name} subsystem",
                    'icon': get_icon(item.name)
                })
    except PermissionError:
        pass
    return children

def get_features(dir_name: str, category: str) -> List[Dict[str, str]]:
    """Get features for directory"""
    features = []

    if 'backend' in dir_name:
        features = [
            {'title': 'API Services', 'description': 'RESTful API endpoints', 'icon': '🔌'},
            {'title': 'Data Processing', 'description': 'Backend data operations', 'icon': '⚡'},
            {'title': 'Authentication', 'description': 'User auth and security', 'icon': '🔐'},
        ]
    elif 'frontend' in dir_name:
        features = [
            {'title': 'User Interface', 'description': 'React-based UI components', 'icon': '🎨'},
            {'title': 'State Management', 'description': 'Redux state handling', 'icon': '🔄'},
            {'title': 'Routing', 'description': 'Client-side navigation', 'icon': '🗺️'},
        ]
    elif 'medical' in dir_name:
        features = [
            {'title': 'DICOM Processing', 'description': 'Medical image handling', 'icon': '🏥'},
            {'title': 'AlF-DETECT', 'description': 'AI-powered detection', 'icon': '🧠'},
            {'title': 'Analysis Tools', 'description': 'Image analysis suite', 'icon': '🔬'},
        ]
    elif 'controls' in dir_name:
        features = [
            {'title': 'SCADA System', 'description': 'Supervisory control', 'icon': '📊'},
            {'title': 'Tag Providers', 'description': 'Data point management', 'icon': '🏷️'},
            {'title': 'Alarm Management', 'description': 'Priority-based alarms', 'icon': '🚨'},
        ]
    else:
        features = [
            {'title': 'Core Functionality', 'description': 'Primary system features', 'icon': '⚙️'},
            {'title': 'Data Management', 'description': 'Structured data handling', 'icon': '📊'},
            {'title': 'Monitoring', 'description': 'Real-time monitoring', 'icon': '👁️'},
        ]

    return features

def check_interfaces(dir_path: Path) -> Dict[str, Any]:
    """Check for PLC/HMI/SCADA interfaces"""
    return {
        'has_plc': (dir_path / 'plc.html').exists(),
        'has_hmi': (dir_path / 'hmi.html').exists(),
        'has_scada': (dir_path / 'scada.html').exists(),
        'plc_path': f"/{dir_path.relative_to(ROOT_DIR)}/plc.html" if (dir_path / 'plc.html').exists() else None,
        'hmi_path': f"/{dir_path.relative_to(ROOT_DIR)}/hmi.html" if (dir_path / 'hmi.html').exists() else None,
        'scada_path': f"/{dir_path.relative_to(ROOT_DIR)}/scada.html" if (dir_path / 'scada.html').exists() else None,
    }

def get_related_files(dir_path: Path) -> List[Dict[str, str]]:
    """Get list of important files in directory"""
    files = []

    file_types = {
        'README.md': ('markdown', 'README'),
        'controls.md': ('markdown', 'Controls'),
        'status.md': ('markdown', 'Status'),
        'index.html': ('html', 'Index'),
        'plc.html': ('html', 'PLC'),
        'hmi.html': ('html', 'HMI'),
        'scada.html': ('html', 'SCADA'),
        'package.json': ('json', 'Package'),
        'requirements.txt': ('text', 'Requirements'),
    }

    for filename, (file_type, name) in file_types.items():
        if (dir_path / filename).exists():
            files.append({
                'path': filename,
                'name': name,
                'type': file_type
            })

    return files

def generate_index_tag(dir_path: Path) -> Dict[str, Any]:
    """Generate index tag data following IndexTemplate UDT"""
    rel_path = dir_path.relative_to(ROOT_DIR)
    dir_name = dir_path.name if dir_path != ROOT_DIR else 'root'
    category = get_category(dir_path)

    # Parent path
    parent_path = f"/{rel_path.parent}/" if rel_path.parent != Path('.') else None

    # Generate tag data
    tag_data = {
        # Identity Tags
        'UUID': str(uuid.uuid4()),
        'ISA_Level': category,
        'Directory_Path': f"/{rel_path}/" if rel_path != Path('.') else "/",
        'Directory_Name': dir_name.replace('_', ' ').replace('-', ' ').title(),

        # Metadata Tags
        'Title': dir_name.replace('_', ' ').replace('-', ' ').title(),
        'Description': f"ISA-95 {category} - {dir_name} subsystem",
        'Icon': get_icon(dir_name),
        'Color_Scheme': COLOR_MAP.get(category, 'blue'),

        # Navigation Tags
        'Parent_Path': parent_path,
        'Child_Directories': get_child_directories(dir_path),
        'Sibling_Directories': [],

        # Documentation Tags
        'README_Path': 'README.md' if (dir_path / 'README.md').exists() else None,
        'Controls_Path': 'controls.md' if (dir_path / 'controls.md').exists() else None,
        'Status_Path': 'status.md' if (dir_path / 'status.md').exists() else None,

        # Interface Tags
        **check_interfaces(dir_path),

        # Content Tags
        'Features': get_features(dir_name, category),
        'Quick_Actions': [
            {'label': 'View Status', 'path': 'status.md', 'type': 'primary'},
            {'label': 'Controls', 'path': 'controls.md', 'type': 'secondary'},
            {'label': 'Documentation', 'path': 'README.md', 'type': 'secondary'},
        ],
        'Related_Files': get_related_files(dir_path),
    }

    return tag_data

def create_index_loader() -> str:
    """Create generic index.html loader"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Loading...</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%);
    color: #e0e0e0;
    min-height: 100vh;
  }

  .loader {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    flex-direction: column;
    gap: 20px;
  }

  .spinner {
    width: 50px;
    height: 50px;
    border: 5px solid #333;
    border-top-color: #00ff88;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .container {
    max-width: 1400px;
    margin: 0 auto;
    padding: 60px 40px;
  }

  header {
    text-align: center;
    margin-bottom: 60px;
  }

  .icon {
    font-size: 4em;
    margin-bottom: 20px;
  }

  h1 {
    font-size: 3em;
    margin-bottom: 15px;
    text-shadow: 0 0 30px rgba(0, 255, 136, 0.4);
  }

  .description {
    color: #888;
    font-size: 1.3em;
  }

  .badge {
    display: inline-block;
    padding: 8px 16px;
    background: #2a2a3e;
    border: 2px solid #00ff88;
    border-radius: 20px;
    font-size: 0.9em;
    font-weight: 600;
    color: #00ff88;
    margin: 10px 5px;
  }

  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 30px;
    margin-bottom: 40px;
  }

  .card {
    background: linear-gradient(135deg, #1a1a2e, #2a2a3e);
    border: 2px solid #333;
    border-left: 5px solid #00ff88;
    border-radius: 12px;
    padding: 30px;
    transition: all 0.3s;
  }

  .card:hover {
    border-color: #00ff88;
    box-shadow: 0 10px 40px rgba(0, 255, 136, 0.2);
    transform: translateY(-3px);
  }

  .card-icon {
    font-size: 2.5em;
    margin-bottom: 15px;
  }

  .card h2 {
    color: #00ff88;
    font-size: 1.6em;
    margin-bottom: 15px;
  }

  .card p {
    color: #aaa;
    line-height: 1.6;
  }

  .card a {
    color: #00ccff;
    text-decoration: none;
  }

  .card a:hover {
    text-decoration: underline;
  }

  .section {
    background: #1a1a2e;
    border: 2px solid #333;
    border-radius: 12px;
    padding: 40px;
    margin-bottom: 40px;
  }

  .section h2 {
    color: #00ff88;
    font-size: 2em;
    margin-bottom: 25px;
  }

  .btn {
    display: inline-block;
    padding: 12px 24px;
    border-radius: 8px;
    font-weight: 600;
    text-decoration: none;
    transition: all 0.3s;
    margin: 5px;
  }

  .btn-primary {
    background: linear-gradient(135deg, #00ff88, #00cc66);
    color: #000;
  }

  .btn-secondary {
    background: #2a2a3e;
    color: #00ccff;
    border: 2px solid #00ccff;
  }

  .btn:hover {
    transform: translateY(-2px);
  }

  footer {
    text-align: center;
    padding: 30px;
    color: #666;
    border-top: 2px solid #333;
    margin-top: 60px;
  }

  .color-green h1, .color-green .card { border-left-color: #00ff88; }
  .color-blue h1, .color-blue .card { border-left-color: #00ccff; }
  .color-purple h1, .color-purple .card { border-left-color: #ff88ff; }
  .color-orange h1, .color-orange .card { border-left-color: #ffaa00; }
  .color-red h1, .color-red .card { border-left-color: #ff6666; }
  .color-cyan h1, .color-cyan .card { border-left-color: #00ffff; }
</style>
</head>
<body>

<div class="loader" id="loader">
  <div class="spinner"></div>
  <p>Loading index data...</p>
</div>

<div class="container" id="content" style="display: none;"></div>

<script>
// Generic Index Loader
// Loads structured index data and renders the page

async function loadIndex() {
  try {
    // Load index tag data
    const response = await fetch('index/tag.json');
    if (!response.ok) {
      throw new Error('Index data not found');
    }

    const tag = await response.json();

    // Apply color scheme
    document.body.className = `color-${tag.Color_Scheme}`;
    document.title = tag.Title;

    // Build page content
    const content = document.getElementById('content');
    content.innerHTML = `
      <header>
        <div class="icon">${tag.Icon}</div>
        <h1>${tag.Title}</h1>
        <p class="description">${tag.Description}</p>
        <div>
          <span class="badge">${tag.ISA_Level.replace('_', '-')}</span>
          <span class="badge">UUID: ${tag.UUID.substring(0, 8)}</span>
        </div>
      </header>

      ${tag.Parent_Path ? `
      <div style="text-align: center; margin-bottom: 40px;">
        <a href="${tag.Parent_Path}" class="btn btn-secondary">← Parent Directory</a>
      </div>
      ` : ''}

      ${tag.Features && tag.Features.length > 0 ? `
      <div class="section">
        <h2>Features</h2>
        <div class="grid">
          ${tag.Features.map(f => `
            <div class="card">
              <div class="card-icon">${f.icon}</div>
              <h2>${f.title}</h2>
              <p>${f.description}</p>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${tag.Child_Directories && tag.Child_Directories.length > 0 ? `
      <div class="section">
        <h2>Subdirectories</h2>
        <div class="grid">
          ${tag.Child_Directories.map(d => `
            <div class="card">
              <div class="card-icon">${d.icon}</div>
              <h2><a href="${d.path}">${d.title}</a></h2>
              <p>${d.description}</p>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${(tag.Has_PLC || tag.Has_HMI || tag.Has_SCADA) ? `
      <div class="section">
        <h2>Control Interfaces</h2>
        <div style="text-align: center;">
          ${tag.Has_SCADA ? `<a href="${tag.SCADA_Path}" class="btn btn-primary">📊 SCADA</a>` : ''}
          ${tag.Has_HMI ? `<a href="${tag.HMI_Path}" class="btn btn-primary">🎛️ HMI</a>` : ''}
          ${tag.Has_PLC ? `<a href="${tag.PLC_Path}" class="btn btn-primary">⚙️ PLC</a>` : ''}
        </div>
      </div>
      ` : ''}

      ${tag.Related_Files && tag.Related_Files.length > 0 ? `
      <div class="section">
        <h2>Documentation</h2>
        <div class="grid">
          ${tag.Related_Files.map(f => `
            <div class="card">
              <h2><a href="${f.path}">${f.name}</a></h2>
              <p>Type: ${f.type}</p>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${tag.Quick_Actions && tag.Quick_Actions.length > 0 ? `
      <div class="section">
        <h2>Quick Actions</h2>
        <div style="text-align: center;">
          ${tag.Quick_Actions.map(a => `
            <a href="${a.path}" class="btn btn-${a.type}">${a.label}</a>
          `).join('')}
        </div>
      </div>
      ` : ''}

      <footer>
        <p>
          <strong>ISA-95 ${tag.ISA_Level.replace('_', '-')}</strong><br>
          ${tag.Directory_Path}
        </p>
      </footer>
    `;

    // Hide loader, show content
    document.getElementById('loader').style.display = 'none';
    content.style.display = 'block';

  } catch (error) {
    console.error('Error loading index:', error);
    document.getElementById('loader').innerHTML = `
      <div class="card" style="max-width: 500px;">
        <h2 style="color: #ff6666;">⚠️ Error Loading Index</h2>
        <p>${error.message}</p>
        <p style="margin-top: 20px;">
          <a href="../" class="btn btn-secondary">← Go Back</a>
        </p>
      </div>
    `;
  }
}

// Load on page ready
document.addEventListener('DOMContentLoaded', loadIndex);
</script>

</body>
</html>
"""

def is_duplicate_directory(dir_path: Path) -> bool:
    """
    Check if a directory appears to be a duplicate of its parent.

    A directory is considered duplicate if:
    1. Its name matches one of its ancestor directory names
    2. It's within 2 levels of a directory with the same name

    Examples of duplicates:
        /os/controls/controls -> True (parent is 'controls')
        /os/controls/tag-providers/controls -> False (legitimate structure)
        /backend/api/backend -> True (ancestor is 'backend')

    Args:
        dir_path: Path to check for duplication

    Returns:
        True if directory appears to be a duplicate, False otherwise
    """
    dir_name = dir_path.name

    # Check immediate parent
    parent = dir_path.parent
    if parent.name == dir_name:
        return True

    # Check grandparent (but allow some legitimate patterns)
    grandparent = parent.parent
    if grandparent.name == dir_name:
        # This might be legitimate if there's an intervening directory
        # Example: controls/tag-providers/controls is OK
        # But controls/index/controls is NOT OK
        if parent.name in ['index', 'backup', 'old', 'temp', 'cache']:
            return True

    return False


def validate_directory_structure(dir_path: Path) -> Dict[str, Any]:
    """
    Validate directory structure and check for issues.

    Returns dict with validation results:
    {
        'valid': bool,
        'issues': List[str],
        'warnings': List[str]
    }
    """
    issues = []
    warnings = []

    # Check if directory is a duplicate
    if is_duplicate_directory(dir_path):
        issues.append(f"Duplicate directory pattern detected: {dir_path}")

    # Check if directory is accessible
    if not os.access(dir_path, os.R_OK):
        issues.append(f"Directory not readable: {dir_path}")

    # Check if directory is writable (needed to create index)
    if not os.access(dir_path, os.W_OK):
        issues.append(f"Directory not writable: {dir_path}")

    # Check for nested index directories (potential issue)
    index_dir = dir_path / 'index'
    if index_dir.exists():
        if (index_dir / 'index').exists():
            warnings.append(f"Nested index directory found: {index_dir / 'index'}")

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings
    }


def get_directories_to_process(root_dir: Path) -> List[Path]:
    """
    Get list of directories to process, excluding duplicates and invalid directories.

    This function walks the directory tree and collects all valid directories
    while filtering out:
    - Hidden directories (starting with .)
    - Common exclude patterns (node_modules, __pycache__, etc.)
    - Duplicate directories
    - Index directories themselves

    Args:
        root_dir: Root directory to start walking from

    Returns:
        List of Path objects for directories to process
    """
    directories = []
    skipped = defaultdict(list)

    # Directories to always skip
    SKIP_DIRS = {
        'node_modules', '__pycache__', 'index', '.git',
        '.venv', 'venv', 'env', 'dist', 'build',
        '.next', '.nuxt', 'coverage', '.pytest_cache'
    }

    for root, dirs, files in os.walk(root_dir):
        root_path = Path(root)

        # Filter directories in-place to control os.walk descent
        original_dirs = dirs.copy()
        dirs[:] = []

        for d in original_dirs:
            dir_path = root_path / d

            # Skip hidden directories
            if d.startswith('.'):
                skipped['hidden'].append(dir_path)
                continue

            # Skip common exclude patterns
            if d in SKIP_DIRS:
                skipped['excluded'].append(dir_path)
                continue

            # Skip if it's a duplicate
            if is_duplicate_directory(dir_path):
                skipped['duplicate'].append(dir_path)
                continue

            # This directory is OK to process
            dirs.append(d)

        # Add current directory to process list
        # (but skip root if it's the project root to avoid issues)
        if root_path == root_dir:
            directories.append(root_path)
        else:
            validation = validate_directory_structure(root_path)
            if validation['valid']:
                directories.append(root_path)
            else:
                skipped['invalid'].append(root_path)
                if VERBOSE:
                    for issue in validation['issues']:
                        print(f"  ⚠️  {issue}")

    return directories, skipped


def print_statistics(processed: int, skipped: Dict[str, List[Path]],
                    created: int, updated: int, backed_up: int):
    """Print detailed statistics about the operation"""
    print("\n" + "="*60)
    print("STATISTICS")
    print("="*60)
    print(f"\nProcessed Directories: {processed}")
    print(f"  - Created new indexes: {created}")
    print(f"  - Updated existing indexes: {updated}")
    print(f"  - Backed up custom files: {backed_up}")

    print(f"\nSkipped Directories: {sum(len(v) for v in skipped.values())}")
    for reason, dirs in skipped.items():
        if dirs:
            print(f"  - {reason.title()}: {len(dirs)}")
            if VERBOSE:
                # Show first 10 directories for this skip reason
                for d in dirs[:10]:
                    rel_path = d.relative_to(ROOT_DIR) if d != ROOT_DIR else Path('.')
                    print(f"      • {rel_path}")
                if len(dirs) > 10:
                    print(f"      ... and {len(dirs) - 10} more")

    print("="*60 + "\n")


def main():
    """
    Generate index directories and tag data for all directories.

    This is the main entry point that orchestrates the index generation process:
    1. Scans directory tree to find all valid directories
    2. Validates each directory for duplicates and accessibility
    3. Generates index data and files for each valid directory
    4. Reports statistics and any issues found
    """
    print("="*60)
    print("INDEX GENERATOR - ISA-95 Structured Index System")
    print("="*60)

    if DRY_RUN:
        print("🔍 DRY RUN MODE - No files will be modified")

    print(f"\nRoot Directory: {ROOT_DIR}")
    print(f"Scanning directory tree...\n")

    # Get directories to process
    directories, skipped = get_directories_to_process(ROOT_DIR)

    print(f"Found {len(directories)} directories to process")
    if skipped:
        total_skipped = sum(len(v) for v in skipped.values())
        print(f"Skipping {total_skipped} directories (duplicates, hidden, etc.)")
    print()

    # Statistics
    created_count = 0
    updated_count = 0
    backed_up_count = 0

    # Process each directory
    for dir_path in directories:
        try:
            rel_path = dir_path.relative_to(ROOT_DIR) if dir_path != ROOT_DIR else Path('.')

            # Validate before processing
            validation = validate_directory_structure(dir_path)
            if not validation['valid']:
                if VERBOSE:
                    print(f"  ⚠️  Skipping {rel_path}: {validation['issues'][0]}")
                skipped['invalid'].append(dir_path)
                continue

            # Create index directory
            index_dir = dir_path / 'index'
            if not DRY_RUN:
                index_dir.mkdir(exist_ok=True)

            is_new = not (index_dir / 'tag.json').exists()

            # Generate tag data
            tag_data = generate_index_tag(dir_path)

            # Write tag.json
            tag_file = index_dir / 'tag.json'
            if not DRY_RUN:
                with open(tag_file, 'w') as f:
                    json.dump(tag_data, f, indent=2)

            # Create generic index.html loader (only if doesn't exist or is old)
            index_html = dir_path / 'index.html'
            needs_update = (not index_html.exists() or
                          'Generic Index Loader' not in index_html.read_text())

            if needs_update:
                # Backup existing if it's a custom one
                if index_html.exists() and index_html.stat().st_size > 1000:
                    backup = dir_path / 'index-custom.html'
                    if not backup.exists():
                        if not DRY_RUN:
                            index_html.rename(backup)
                        backed_up_count += 1
                        if VERBOSE:
                            print(f"  💾 Backed up custom index: {rel_path}/index-custom.html")

                # Write generic loader
                if not DRY_RUN:
                    index_html.write_text(create_index_loader())

            # Update statistics
            if is_new:
                created_count += 1
            else:
                updated_count += 1

            # Print progress
            status = "✅ Created" if is_new else "🔄 Updated"
            print(f"  {status} index for: {rel_path}")

            # Show warnings if any
            if validation['warnings'] and VERBOSE:
                for warning in validation['warnings']:
                    print(f"      ⚠️  {warning}")

        except Exception as e:
            print(f"  ❌ Error processing {dir_path}: {e}")
            if VERBOSE:
                import traceback
                traceback.print_exc()

    # Print statistics
    print_statistics(
        processed=len(directories),
        skipped=skipped,
        created=created_count,
        updated=updated_count,
        backed_up=backed_up_count
    )

    if DRY_RUN:
        print("🔍 DRY RUN COMPLETE - No files were modified")
        print("    Run without --dry-run to apply changes")
    else:
        print("✅ INDEX GENERATION COMPLETE")

if __name__ == '__main__':
    main()
