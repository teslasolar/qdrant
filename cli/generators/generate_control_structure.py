#!/usr/bin/env python3
"""
Generate controls directory structure for all areas
Creates controls/, scada/, plc/, hmi/, tags/ subdirectories with index system
"""

import os
import json
import uuid
from pathlib import Path

ROOT_DIR = Path("/home/user/qdrant")

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
}

# Control subdirectories to create
CONTROL_SUBDIRS = {
    'scada': {
        'icon': '📊',
        'title': 'SCADA',
        'description': 'Supervisory Control and Data Acquisition',
        'features': [
            {'title': 'Tag Provider', 'description': 'Central tag data source', 'icon': '🏷️'},
            {'title': 'Historian', 'description': 'Time-series data storage', 'icon': '📈'},
            {'title': 'Alarms', 'description': 'Priority-based notifications', 'icon': '🚨'},
        ]
    },
    'plc': {
        'icon': '⚙️',
        'title': 'PLC',
        'description': 'Programmable Logic Controller',
        'features': [
            {'title': 'Ladder Logic', 'description': 'Relay-based programming', 'icon': '🪜'},
            {'title': 'Structured Text', 'description': 'High-level programming', 'icon': '📝'},
            {'title': 'Function Blocks', 'description': 'Modular logic units', 'icon': '🧩'},
        ]
    },
    'hmi': {
        'icon': '🎛️',
        'title': 'HMI',
        'description': 'Human-Machine Interface',
        'features': [
            {'title': 'Operator Screens', 'description': 'Process visualization', 'icon': '🖥️'},
            {'title': 'Controls', 'description': 'Interactive elements', 'icon': '🎮'},
            {'title': 'Trends', 'description': 'Real-time charting', 'icon': '📉'},
        ]
    },
    'tags': {
        'icon': '🏷️',
        'title': 'Tags',
        'description': 'Tag Definitions and Data Points',
        'features': [
            {'title': 'Tag Browser', 'description': 'Browse all tags', 'icon': '🔍'},
            {'title': 'UDT Library', 'description': 'User Defined Types', 'icon': '📚'},
            {'title': 'Tag Groups', 'description': 'Organized collections', 'icon': '📂'},
        ]
    },
}

def get_category(dir_path: Path) -> str:
    """Determine ISA-95 category from path"""
    rel_path = dir_path.relative_to(ROOT_DIR)
    path_str = str(rel_path)

    # Check exact matches first
    for key, cat in CATEGORY_MAP.items():
        if path_str == key or path_str.startswith(key + '/'):
            return cat

    # Control subdirs are L2
    if '/controls/' in path_str or path_str.endswith('/controls'):
        return 'L2_Supervisory'

    # Default categorization
    if 'controls' in path_str or 'tag-providers' in path_str:
        return 'L2_Supervisory'
    elif 'plc' in path_str.lower():
        return 'L1_Control'
    elif 'os/' in path_str:
        return 'L3_MES'

    return 'L4_Business'

def get_color_scheme(category: str) -> str:
    """Get color scheme for ISA-95 level"""
    if 'L4' in category:
        return 'green'
    elif 'L3' in category:
        return 'blue'
    elif 'L2' in category:
        return 'purple'
    elif 'L1' in category:
        return 'orange'
    else:
        return 'red'

def generate_tag_data(dir_path: Path, subdir_name: str = None) -> dict:
    """Generate tag.json data for directory"""
    rel_path = dir_path.relative_to(ROOT_DIR)

    if subdir_name:
        # This is a control subdir
        config = CONTROL_SUBDIRS[subdir_name]
        category = 'L1_Control' if subdir_name == 'plc' else 'L2_Supervisory'

        return {
            'UUID': str(uuid.uuid4()),
            'ISA_Level': category,
            'Directory_Path': f"/{rel_path}/",
            'Directory_Name': config['title'],
            'Title': config['title'],
            'Description': config['description'],
            'Icon': config['icon'],
            'Color_Scheme': get_color_scheme(category),
            'Parent_Path': f"/{rel_path.parent}/",
            'Child_Directories': [],
            'Sibling_Directories': [],
            'README_Path': 'README.md' if (dir_path / 'README.md').exists() else None,
            'Controls_Path': None,
            'Status_Path': None,
            'has_plc': False,
            'has_hmi': False,
            'has_scada': False,
            'plc_path': None,
            'hmi_path': None,
            'scada_path': None,
            'Features': config['features'],
            'Quick_Actions': [
                {'label': 'View Tags', 'path': '../tags/', 'type': 'primary'},
                {'label': 'Documentation', 'path': 'README.md', 'type': 'secondary'},
            ],
            'Related_Files': []
        }
    else:
        # This is a controls directory
        category = get_category(dir_path)

        # Find child directories
        children = []
        for subdir in ['scada', 'plc', 'hmi', 'tags']:
            if (dir_path / subdir).is_dir():
                config = CONTROL_SUBDIRS[subdir]
                children.append({
                    'path': f"/{rel_path}/{subdir}/",
                    'title': config['title'],
                    'description': config['description'],
                    'icon': config['icon']
                })

        return {
            'UUID': str(uuid.uuid4()),
            'ISA_Level': category,
            'Directory_Path': f"/{rel_path}/",
            'Directory_Name': 'Controls',
            'Title': 'Controls',
            'Description': f'Control system for {dir_path.parent.name}',
            'Icon': '🎛️',
            'Color_Scheme': get_color_scheme(category),
            'Parent_Path': f"/{rel_path.parent}/",
            'Child_Directories': children,
            'Sibling_Directories': [],
            'README_Path': 'README.md' if (dir_path / 'README.md').exists() else None,
            'Controls_Path': None,
            'Status_Path': None,
            'has_plc': (dir_path / 'plc').is_dir(),
            'has_hmi': (dir_path / 'hmi').is_dir(),
            'has_scada': (dir_path / 'scada').is_dir(),
            'plc_path': f"/{rel_path}/plc/" if (dir_path / 'plc').is_dir() else None,
            'hmi_path': f"/{rel_path}/hmi/" if (dir_path / 'hmi').is_dir() else None,
            'scada_path': f"/{rel_path}/scada/" if (dir_path / 'scada').is_dir() else None,
            'Features': [
                {'title': 'SCADA System', 'description': 'Supervisory control', 'icon': '📊'},
                {'title': 'PLC Controllers', 'description': 'Logic automation', 'icon': '⚙️'},
                {'title': 'HMI Interfaces', 'description': 'Operator panels', 'icon': '🎛️'},
                {'title': 'Tag Definitions', 'description': 'Data points', 'icon': '🏷️'},
            ],
            'Quick_Actions': [
                {'label': 'SCADA', 'path': 'scada/', 'type': 'primary'},
                {'label': 'PLC', 'path': 'plc/', 'type': 'secondary'},
                {'label': 'HMI', 'path': 'hmi/', 'type': 'secondary'},
                {'label': 'Tags', 'path': 'tags/', 'type': 'secondary'},
            ],
            'Related_Files': []
        }

def create_readme(dir_path: Path, subdir_name: str = None) -> str:
    """Create README.md content"""
    if subdir_name:
        config = CONTROL_SUBDIRS[subdir_name]
        return f"""# {config['title']}
**ISA-95 L1/L2** | {config['description']}

## Overview

{config['description']} for the {dir_path.parent.parent.name}/{dir_path.parent.name} area.

## Features

{chr(10).join(f"- **{f['title']}** - {f['description']}" for f in config['features'])}

## Directory Structure

```
{dir_path.name}/
├── index/
│   └── tag.json          # Tag metadata
├── index.html            # Auto-loading interface
└── README.md             # This file
```

## Integration

This {subdir_name.upper()} interface integrates with:
- Tag provider system
- Parent control system
- Other control interfaces (SCADA/PLC/HMI/Tags)

## Usage

Visit the web interface to interact with this {config['title']} system.

---

**Auto-generated** by generate_control_structure.py
"""
    else:
        return f"""# Controls Directory
**ISA-95 L2 Supervisory** | Control System Structure

## Overview

This directory contains the complete control system structure with SCADA, PLC, HMI, and Tag subsystems.

## Subdirectories

- **scada/** - Supervisory Control and Data Acquisition
- **plc/** - Programmable Logic Controller
- **hmi/** - Human-Machine Interface
- **tags/** - Tag Definitions and Data Points

## Architecture

```
controls/
├── scada/           # L2 - Supervisory control
│   └── index/tag.json
├── plc/             # L1 - Direct control logic
│   └── index/tag.json
├── hmi/             # L2 - Operator interface
│   └── index/tag.json
└── tags/            # L2 - Tag provider
    └── index/tag.json
```

## ISA-95 Hierarchy

- **L2 Supervisory** - SCADA, HMI, Tags
- **L1 Control** - PLC logic execution

## Usage

Navigate to each subdirectory to access the specific control interface.

---

**Auto-generated** by generate_control_structure.py
"""

def create_generic_index_html() -> str:
    """Get the generic index.html loader content"""
    # Same as in generate_indexes.py
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

      ${(tag.has_plc || tag.has_hmi || tag.has_scada) ? `
      <div class="section">
        <h2>Control Interfaces</h2>
        <div style="text-align: center;">
          ${tag.has_scada ? `<a href="${tag.scada_path}" class="btn btn-primary">📊 SCADA</a>` : ''}
          ${tag.has_hmi ? `<a href="${tag.hmi_path}" class="btn btn-primary">🎛️ HMI</a>` : ''}
          ${tag.has_plc ? `<a href="${tag.plc_path}" class="btn btn-primary">⚙️ PLC</a>` : ''}
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

def should_have_controls(dir_path: Path) -> bool:
    """Determine if directory should have controls subdirectory"""
    rel_path = str(dir_path.relative_to(ROOT_DIR))

    # Skip these directories
    skip_patterns = [
        'index', 'node_modules', '__pycache__', '.git',
        'controls/scada', 'controls/plc', 'controls/hmi', 'controls/tags',
        'docs/', 'collab/', 'cli/'
    ]

    for pattern in skip_patterns:
        if pattern in rel_path:
            return False

    # Add controls to main os/ subdirectories
    main_areas = [
        'os/backend', 'os/frontend', 'os/medical', 'os/modules',
        'os/boot', 'os/data', 'os/language', 'os/models',
        'os/equipment', 'os/templates', 'os/sandbox', 'os/debug',
        'os/test-modules', 'os/scripts', 'os/config'
    ]

    # Check if this is a main area
    for area in main_areas:
        if rel_path == area:
            return True

    # Also add to any subdirectory under os/ that has more than 2 levels
    if rel_path.startswith('os/') and rel_path.count('/') >= 2:
        # It's a subdirectory of os/ (but not os/ itself)
        # Skip if already in controls hierarchy
        if '/controls/' not in rel_path:
            return True

    return False

def main():
    """Generate controls directory structure"""
    print("Generating controls directory structure...")
    print()

    controls_created = 0
    subdirs_created = 0

    # Walk through directories
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip hidden and special directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'index']]

        root_path = Path(root)

        # Check if this directory should have controls
        if should_have_controls(root_path):
            controls_dir = root_path / 'controls'

            # Create controls directory if it doesn't exist
            if not controls_dir.exists():
                controls_dir.mkdir(exist_ok=True)
                print(f"  📁 Created controls: {root_path.relative_to(ROOT_DIR)}/controls/")
                controls_created += 1

            # Create control subdirectories
            for subdir_name in ['scada', 'plc', 'hmi', 'tags']:
                subdir_path = controls_dir / subdir_name

                if not subdir_path.exists():
                    subdir_path.mkdir(exist_ok=True)
                    print(f"    ✅ Created {subdir_name}: {subdir_path.relative_to(ROOT_DIR)}")
                    subdirs_created += 1

                # Create index directory and tag.json
                index_dir = subdir_path / 'index'
                index_dir.mkdir(exist_ok=True)

                tag_data = generate_tag_data(subdir_path, subdir_name)
                tag_file = index_dir / 'tag.json'
                with open(tag_file, 'w') as f:
                    json.dump(tag_data, f, indent=2)

                # Create index.html
                index_html = subdir_path / 'index.html'
                index_html.write_text(create_generic_index_html())

                # Create README.md
                readme_file = subdir_path / 'README.md'
                readme_file.write_text(create_readme(subdir_path, subdir_name))

            # Create controls directory index
            index_dir = controls_dir / 'index'
            index_dir.mkdir(exist_ok=True)

            tag_data = generate_tag_data(controls_dir)
            tag_file = index_dir / 'tag.json'
            with open(tag_file, 'w') as f:
                json.dump(tag_data, f, indent=2)

            # Create controls index.html (if it doesn't exist or update it)
            index_html = controls_dir / 'index.html'
            if not index_html.exists() or index_html.stat().st_size < 5000:
                index_html.write_text(create_generic_index_html())

            # Create controls README.md
            readme_file = controls_dir / 'README.md'
            if not readme_file.exists():
                readme_file.write_text(create_readme(controls_dir))

    print()
    print(f"✅ Created {controls_created} controls directories")
    print(f"✅ Created {subdirs_created} control subdirectories (scada/plc/hmi/tags)")

if __name__ == '__main__':
    main()
