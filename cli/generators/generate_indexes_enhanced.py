#!/usr/bin/env python3
"""
Enhanced index generator with full navigation hierarchy
Includes parent, child, sibling directories and file listings
"""

import os
import json
import uuid
from pathlib import Path
from typing import Dict, List, Any

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
    'scada': '📊',
    'plc': '⚙️',
    'hmi': '🎛️',
    'tags': '🏷️',
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
    """Get list of child directories with page counts"""
    children = []
    try:
        for item in sorted(dir_path.iterdir()):
            if item.is_dir() and not item.name.startswith('.') and item.name not in ['node_modules', '__pycache__', 'index']:
                rel_path = item.relative_to(ROOT_DIR)

                # Count pages in child directory
                page_count = len(list(item.glob('*.html'))) + len(list(item.glob('*.md')))

                children.append({
                    'path': f"/{rel_path}/",
                    'title': item.name.replace('_', ' ').replace('-', ' ').title(),
                    'description': f"{item.name} subsystem",
                    'icon': get_icon(item.name),
                    'page_count': page_count
                })
    except PermissionError:
        pass
    return children

def get_sibling_directories(dir_path: Path) -> List[Dict[str, str]]:
    """Get list of sibling directories"""
    siblings = []

    if dir_path == ROOT_DIR:
        return siblings

    parent_path = dir_path.parent

    try:
        for item in sorted(parent_path.iterdir()):
            if (item.is_dir() and
                item != dir_path and
                not item.name.startswith('.') and
                item.name not in ['node_modules', '__pycache__', 'index']):

                rel_path = item.relative_to(ROOT_DIR)
                siblings.append({
                    'path': f"/{rel_path}/",
                    'title': item.name.replace('_', ' ').replace('-', ' ').title(),
                    'description': f"{item.name} area",
                    'icon': get_icon(item.name)
                })
    except PermissionError:
        pass

    return siblings

def get_breadcrumb_trail(dir_path: Path) -> List[Dict[str, str]]:
    """Generate breadcrumb navigation trail"""
    breadcrumbs = []

    if dir_path == ROOT_DIR:
        return [{'path': '/', 'title': 'Home', 'icon': '🏠'}]

    rel_path = dir_path.relative_to(ROOT_DIR)
    parts = rel_path.parts

    # Add home
    breadcrumbs.append({'path': '/', 'title': 'Home', 'icon': '🏠'})

    # Add each level
    current_path = Path('/')
    for i, part in enumerate(parts):
        current_path = current_path / part
        breadcrumbs.append({
            'path': str(current_path) + '/',
            'title': part.replace('_', ' ').replace('-', ' ').title(),
            'icon': get_icon(part)
        })

    return breadcrumbs

def get_page_links(dir_path: Path) -> List[Dict[str, Any]]:
    """Get all page links in directory"""
    pages = []

    # HTML pages
    for html_file in sorted(dir_path.glob('*.html')):
        if html_file.name not in ['index.html', 'index-custom.html']:
            pages.append({
                'path': html_file.name,
                'name': html_file.stem.replace('_', ' ').replace('-', ' ').title(),
                'type': 'html',
                'icon': '🌐',
                'size': html_file.stat().st_size
            })

    # Markdown pages
    for md_file in sorted(dir_path.glob('*.md')):
        pages.append({
            'path': md_file.name,
            'name': md_file.stem.replace('_', ' ').replace('-', ' ').title(),
            'type': 'markdown',
            'icon': '📝',
            'size': md_file.stat().st_size
        })

    return pages

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
        'has_plc': (dir_path / 'plc.html').exists() or (dir_path / 'plc').is_dir(),
        'has_hmi': (dir_path / 'hmi.html').exists() or (dir_path / 'hmi').is_dir(),
        'has_scada': (dir_path / 'scada.html').exists() or (dir_path / 'scada').is_dir(),
        'plc_path': 'plc.html' if (dir_path / 'plc.html').exists() else ('plc/' if (dir_path / 'plc').is_dir() else None),
        'hmi_path': 'hmi.html' if (dir_path / 'hmi.html').exists() else ('hmi/' if (dir_path / 'hmi').is_dir() else None),
        'scada_path': 'scada.html' if (dir_path / 'scada.html').exists() else ('scada/' if (dir_path / 'scada').is_dir() else None),
    }

def get_related_files(dir_path: Path) -> List[Dict[str, str]]:
    """Get list of important files in directory"""
    files = []

    file_types = {
        'README.md': ('markdown', 'README'),
        'controls.md': ('markdown', 'Controls'),
        'status.md': ('markdown', 'Status'),
        'index.html': ('html', 'Index'),
        'index-custom.html': ('html', 'Custom Index'),
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
        'Sibling_Directories': get_sibling_directories(dir_path),
        'Breadcrumb_Trail': get_breadcrumb_trail(dir_path),

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
        'Page_Links': get_page_links(dir_path),
    }

    return tag_data

def create_index_loader() -> str:
    """Create enhanced generic index.html loader with navigation"""
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
    padding: 40px;
  }

  /* Breadcrumb Navigation */
  .breadcrumb {
    background: #1a1a2e;
    border: 2px solid #333;
    border-radius: 8px;
    padding: 15px 25px;
    margin-bottom: 30px;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
  }

  .breadcrumb a {
    color: #00ccff;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: color 0.3s;
  }

  .breadcrumb a:hover {
    color: #00ff88;
  }

  .breadcrumb-separator {
    color: #666;
    margin: 0 5px;
  }

  .breadcrumb-current {
    color: #00ff88;
    font-weight: 600;
  }

  header {
    text-align: center;
    margin-bottom: 40px;
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
    position: relative;
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

  .card-badge {
    position: absolute;
    top: 15px;
    right: 15px;
    background: #2a2a3e;
    border: 1px solid #00ff88;
    border-radius: 12px;
    padding: 4px 10px;
    font-size: 0.75em;
    color: #00ff88;
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
    box-shadow: 0 5px 20px rgba(0, 255, 136, 0.3);
  }

  .page-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 15px;
  }

  .page-item {
    background: #2a2a3e;
    border: 1px solid #444;
    border-radius: 8px;
    padding: 15px;
    transition: all 0.3s;
  }

  .page-item:hover {
    border-color: #00ccff;
    background: #333;
  }

  .page-item a {
    color: #00ccff;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .page-item-icon {
    font-size: 1.5em;
  }

  .page-item-size {
    font-size: 0.8em;
    color: #888;
    margin-top: 5px;
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

  /* Sidebar Navigation */
  .sidebar {
    position: fixed;
    right: 20px;
    top: 20px;
    background: #1a1a2e;
    border: 2px solid #333;
    border-radius: 12px;
    padding: 20px;
    max-width: 250px;
    max-height: 80vh;
    overflow-y: auto;
    z-index: 1000;
  }

  .sidebar h3 {
    color: #00ff88;
    font-size: 1.2em;
    margin-bottom: 15px;
  }

  .sidebar ul {
    list-style: none;
  }

  .sidebar li {
    margin-bottom: 10px;
  }

  .sidebar a {
    color: #00ccff;
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.9em;
    transition: color 0.3s;
  }

  .sidebar a:hover {
    color: #00ff88;
  }

  @media (max-width: 1200px) {
    .sidebar {
      display: none;
    }
  }
</style>
</head>
<body>

<div class="loader" id="loader">
  <div class="spinner"></div>
  <p>Loading index data...</p>
</div>

<div class="container" id="content" style="display: none;"></div>

<!-- Sidebar Navigation -->
<div class="sidebar" id="sidebar" style="display: none;"></div>

<script>
// Generic Index Loader with Enhanced Navigation
// Loads structured index data and renders with full navigation hierarchy

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

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

    // Build breadcrumb navigation
    let breadcrumbHTML = '';
    if (tag.Breadcrumb_Trail && tag.Breadcrumb_Trail.length > 0) {
      breadcrumbHTML = '<div class="breadcrumb">';
      tag.Breadcrumb_Trail.forEach((crumb, index) => {
        if (index > 0) {
          breadcrumbHTML += '<span class="breadcrumb-separator">›</span>';
        }
        if (index === tag.Breadcrumb_Trail.length - 1) {
          breadcrumbHTML += `<span class="breadcrumb-current">${crumb.icon} ${crumb.title}</span>`;
        } else {
          breadcrumbHTML += `<a href="${crumb.path}">${crumb.icon} ${crumb.title}</a>`;
        }
      });
      breadcrumbHTML += '</div>';
    }

    // Build sidebar navigation
    let sidebarHTML = '';
    if (tag.Child_Directories && tag.Child_Directories.length > 0) {
      sidebarHTML += '<h3>📂 Quick Nav</h3><ul>';
      tag.Child_Directories.forEach(dir => {
        sidebarHTML += `<li><a href="${dir.path}">${dir.icon} ${dir.title}</a></li>`;
      });
      sidebarHTML += '</ul>';
    }

    if (tag.Sibling_Directories && tag.Sibling_Directories.length > 0) {
      sidebarHTML += '<h3 style="margin-top: 20px;">🔗 Related</h3><ul>';
      tag.Sibling_Directories.slice(0, 8).forEach(dir => {
        sidebarHTML += `<li><a href="${dir.path}">${dir.icon} ${dir.title}</a></li>`;
      });
      sidebarHTML += '</ul>';
    }

    if (sidebarHTML) {
      document.getElementById('sidebar').innerHTML = sidebarHTML;
      document.getElementById('sidebar').style.display = 'block';
    }

    // Build main content
    const content = document.getElementById('content');
    content.innerHTML = `
      ${breadcrumbHTML}

      <header>
        <div class="icon">${tag.Icon}</div>
        <h1>${tag.Title}</h1>
        <p class="description">${tag.Description}</p>
        <div>
          <span class="badge">${tag.ISA_Level.replace('_', '-')}</span>
          <span class="badge">UUID: ${tag.UUID.substring(0, 8)}</span>
        </div>
      </header>

      ${tag.Page_Links && tag.Page_Links.length > 0 ? `
      <div class="section">
        <h2>📄 Pages in This Directory</h2>
        <div class="page-list">
          ${tag.Page_Links.map(page => `
            <div class="page-item">
              <a href="${page.path}">
                <span class="page-item-icon">${page.icon}</span>
                <div>
                  <div>${page.name}</div>
                  <div class="page-item-size">${formatSize(page.size)}</div>
                </div>
              </a>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${tag.Features && tag.Features.length > 0 ? `
      <div class="section">
        <h2>✨ Features</h2>
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
        <h2>📂 Subdirectories</h2>
        <div class="grid">
          ${tag.Child_Directories.map(d => `
            <div class="card">
              ${d.page_count ? `<span class="card-badge">${d.page_count} pages</span>` : ''}
              <div class="card-icon">${d.icon}</div>
              <h2><a href="${d.path}">${d.title}</a></h2>
              <p>${d.description}</p>
            </div>
          `).join('')}
        </div>
      </div>
      ` : ''}

      ${tag.Sibling_Directories && tag.Sibling_Directories.length > 0 ? `
      <div class="section">
        <h2>🔗 Related Directories</h2>
        <div class="grid">
          ${tag.Sibling_Directories.slice(0, 6).map(d => `
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
        <h2>🎛️ Control Interfaces</h2>
        <div style="text-align: center;">
          ${tag.has_scada ? `<a href="${tag.scada_path}" class="btn btn-primary">📊 SCADA</a>` : ''}
          ${tag.has_hmi ? `<a href="${tag.hmi_path}" class="btn btn-primary">🎛️ HMI</a>` : ''}
          ${tag.has_plc ? `<a href="${tag.plc_path}" class="btn btn-primary">⚙️ PLC</a>` : ''}
        </div>
      </div>
      ` : ''}

      ${tag.Related_Files && tag.Related_Files.length > 0 ? `
      <div class="section">
        <h2>📚 Documentation</h2>
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
        <h2>⚡ Quick Actions</h2>
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

def main():
    """Generate enhanced index directories and tag data for all directories"""
    print("Generating enhanced index directories with full navigation...")
    print()

    count = 0
    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip hidden directories, node_modules, and existing index directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'index', '__pycache__']]

        root_path = Path(root)

        # Create index directory
        index_dir = root_path / 'index'
        index_dir.mkdir(exist_ok=True)

        # Generate tag data with enhanced navigation
        tag_data = generate_index_tag(root_path)

        # Write tag.json
        tag_file = index_dir / 'tag.json'
        with open(tag_file, 'w') as f:
            json.dump(tag_data, f, indent=2)

        # Create generic index.html loader (only if doesn't exist or is old)
        index_html = root_path / 'index.html'
        if not index_html.exists() or index_html.stat().st_size < 10000:
            # Backup existing if it's a custom one
            if index_html.exists() and index_html.stat().st_size > 1000:
                backup = root_path / 'index-custom.html'
                if not backup.exists():
                    index_html.rename(backup)
                    print(f"  💾 Backed up custom index: {root_path.relative_to(ROOT_DIR)}/index-custom.html")

            # Write generic loader
            index_html.write_text(create_index_loader())

        count += 1
        rel_path = root_path.relative_to(ROOT_DIR) if root_path != ROOT_DIR else Path('.')
        print(f"  ✅ Enhanced index for: {rel_path}")

    print(f"\n✅ Generated {count} enhanced index directories with full navigation")

if __name__ == '__main__':
    main()
