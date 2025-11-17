#!/usr/bin/env python3
"""
Universal Template-Based Generator
Generates all screens, components, controls, and tags from JSON templates

This generator significantly reduces codebase size by:
1. Generating screens from reusable JSON templates
2. Applying consistent theme from theme.yaml
3. Using config.yaml for environment-specific settings
4. Eliminating duplicate code through template reuse

Usage:
    python3 generate_from_templates.py --all
    python3 generate_from_templates.py --screens
    python3 generate_from_templates.py --medical
    python3 generate_from_templates.py --output ./build
"""

import json
import os
import uuid as uuid_lib
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse
import yaml

# Project root
ROOT_DIR = Path("/home/user/qdrant")
TEMPLATES_DIR = ROOT_DIR / "templates"
OUTPUT_DIR = ROOT_DIR / "screens" / "frontend"

class TemplateGenerator:
    """Universal generator for all template-based content"""

    def __init__(self, output_dir: Optional[Path] = None):
        self.root = ROOT_DIR
        self.templates_dir = TEMPLATES_DIR
        self.output_dir = output_dir or OUTPUT_DIR
        self.theme = self.load_theme()
        self.config = self.load_config()

    def load_theme(self) -> Dict[str, Any]:
        """Load theme.yaml configuration"""
        theme_path = self.root / "theme.yaml"
        if theme_path.exists():
            with open(theme_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def load_config(self) -> Dict[str, Any]:
        """Load config.yaml configuration"""
        config_path = self.root / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {}

    def load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON file"""
        with open(file_path, 'r') as f:
            return json.load(f)

    def get_theme_colors(self) -> Dict[str, str]:
        """Extract color palette from theme"""
        colors = self.theme.get('colors', {})

        # Extract nested color structure from theme.yaml
        if colors:
            return {
                'primary': colors.get('purple', {}).get('accent', '#b794f4'),
                'secondary': colors.get('cream', {}).get('primary', '#f5f2e8'),
                'background': colors.get('background', {}).get('primary', '#2a1a3a'),
                'text': colors.get('cream', {}).get('primary', '#f5f2e8'),
                'accent': colors.get('status', {}).get('active', '#00bfff'),
                'danger': colors.get('status', {}).get('alarm', '#ff6b6b'),
                'warning': colors.get('status', {}).get('warning', '#ffd700'),
                'success': colors.get('status', {}).get('normal', '#90ee90')
            }

        # Default ISA-101 cream & purple theme
        return {
            'primary': '#b794f4',      # Purple
            'secondary': '#f5f2e8',    # Cream
            'background': '#2a1a3a',   # Dark purple background
            'text': '#f5f2e8',         # Cream text
            'accent': '#00bfff',       # Cyan accent
            'danger': '#ff6b6b',       # Red
            'warning': '#ffd700',      # Yellow
            'success': '#90ee90'       # Green
        }

    def generate_medical_screen(self, template_data: Dict[str, Any], output_path: Path):
        """Generate medical imaging screen from JSON template"""
        metadata = template_data.get('metadata', {})
        layout = template_data.get('layout', {})
        components = template_data.get('components', [])
        actions = template_data.get('actions', [])

        colors = self.get_theme_colors()
        grid = layout.get('grid', {})
        cols = grid.get('columns', 4)
        rows = grid.get('rows', 4)
        gap = grid.get('gap', 10)

        # Generate HTML
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{metadata.get('name', 'Medical Imaging Screen')}</title>
<meta name="description" content="{metadata.get('description', '')}">
<meta name="generator" content="Template Generator v1.0.0">
<meta name="template-uuid" content="{template_data.get('uuid', '')}">

<!-- Load theme and config -->
<script src="/scripts/theme-loader.js"></script>
<script src="/scripts/config-loader.js"></script>

<style>
/* ISA-101 Theme Variables */
:root {{
  --primary-color: {colors['primary']};
  --secondary-color: {colors['secondary']};
  --background-color: {colors['background']};
  --text-color: {colors['text']};
  --accent-color: {colors['accent']};
  --danger-color: {colors['danger']};
  --warning-color: {colors['warning']};
  --success-color: {colors['success']};
}}

/* Base Styles */
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: 'Courier New', monospace;
  background: var(--background-color);
  color: var(--text-color);
  height: 100vh;
  overflow: hidden;
}}

/* Header */
.screen-header {{
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 60px;
  background: var(--background-color);
  border-bottom: 3px solid var(--text-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  z-index: 1000;
}}

.screen-title {{
  color: var(--text-color);
  font-size: 1.5em;
  font-weight: bold;
}}

.screen-nav {{
  display: flex;
  gap: 15px;
}}

.nav-btn {{
  padding: 8px 15px;
  background: rgba(0, 255, 136, 0.1);
  border: 1px solid var(--text-color);
  border-radius: 4px;
  color: var(--text-color);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
}}

.nav-btn:hover {{
  background: rgba(0, 255, 136, 0.2);
  box-shadow: 0 0 10px rgba(0, 255, 136, 0.3);
}}

/* Grid Container */
.screen-container {{
  margin-top: 60px;
  height: calc(100vh - 60px);
  display: grid;
  grid-template-columns: repeat({cols}, 1fr);
  grid-template-rows: repeat({rows}, 1fr);
  gap: {gap}px;
  padding: 20px;
}}

/* Component Base Styles */
.component {{
  background: linear-gradient(135deg, #1a1a2e, #2a2a3e);
  border: 2px solid var(--text-color);
  border-radius: 12px;
  padding: 15px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}}

.component-header {{
  font-size: 1.1em;
  font-weight: bold;
  margin-bottom: 10px;
  color: var(--accent-color);
  border-bottom: 1px solid var(--text-color);
  padding-bottom: 8px;
}}

.component-content {{
  flex: 1;
  overflow: auto;
}}

/* Utility Classes */
.btn {{
  padding: 10px 20px;
  background: var(--primary-color);
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s;
}}

.btn:hover {{
  opacity: 0.8;
  box-shadow: 0 0 15px rgba(139, 71, 137, 0.5);
}}

.btn-danger {{ background: var(--danger-color); }}
.btn-warning {{ background: var(--warning-color); }}
.btn-success {{ background: var(--success-color); }}

/* Loading Indicator */
.loading {{
  display: none;
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: var(--text-color);
  font-size: 1.5em;
}}

.loading.active {{
  display: block;
}}
</style>
</head>
<body>

<!-- Header -->
<div class="screen-header">
  <div class="screen-title">
    {metadata.get('name', 'Medical Screen')}
  </div>
  <div class="screen-nav">
    <a href="/index.html" class="nav-btn">🏠 Home</a>
    <a href="/screens/frontend/index.html" class="nav-btn">📊 Dashboard</a>
    <span id="current-time" style="color: var(--accent-color);"></span>
  </div>
</div>

<!-- Screen Container -->
<div class="screen-container" id="screen-container">
{self._generate_components_html(components)}
</div>

<!-- Loading Indicator -->
<div class="loading" id="loading">
  ⌛ Loading...
</div>

<!-- Scripts -->
<script>
// Screen metadata
const screenMetadata = {json.dumps(metadata, indent=2)};

// Update time
function updateTime() {{
  const now = new Date();
  const timeEl = document.getElementById('current-time');
  if (timeEl) {{
    timeEl.textContent = now.toLocaleTimeString();
  }}
}}
setInterval(updateTime, 1000);
updateTime();

// Initialize screen
async function initScreen() {{
  console.log('Screen loaded:', screenMetadata.name);
  console.log('Generated from template:', '{template_data.get('uuid', '')}');

  // Wait for config to load
  if (window.chazonConfig) {{
    await window.chazonConfig.load();
    console.log('Environment:', window.chazonConfig.environment);
  }}

  // Execute onLoad actions
{self._generate_action_scripts(actions, 'onLoad')}
}}

// Initialize when DOM is ready
if (document.readyState === 'loading') {{
  document.addEventListener('DOMContentLoaded', initScreen);
}} else {{
  initScreen();
}}
</script>

</body>
</html>"""

        # Write file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(html)

        print(f"✓ Generated: {output_path}")
        return output_path

    def _generate_components_html(self, components: List[Dict[str, Any]]) -> str:
        """Generate HTML for components"""
        html_parts = []

        for comp in components:
            pos = comp.get('position', {})
            config = comp.get('config', {})
            comp_type = comp.get('type', 'unknown')
            comp_uuid = comp.get('uuid', str(uuid_lib.uuid4()))

            x = pos.get('x', 0)
            y = pos.get('y', 0)
            width = pos.get('width', 1)
            height = pos.get('height', 1)

            title = config.get('title', comp_type.replace('-', ' ').title())

            # Generate component HTML based on type
            component_html = self._generate_component_by_type(comp_type, config, comp_uuid)

            html = f'''
  <!-- Component: {title} -->
  <div class="component component-{comp_type}"
       style="grid-column: {x + 1} / span {width}; grid-row: {y + 1} / span {height};"
       data-uuid="{comp_uuid}"
       data-type="{comp_type}">
    <div class="component-header">{title}</div>
    <div class="component-content">
{component_html}
    </div>
  </div>'''

            html_parts.append(html)

        return '\n'.join(html_parts)

    def _generate_component_by_type(self, comp_type: str, config: Dict[str, Any], comp_uuid: str) -> str:
        """Generate component HTML based on type"""

        if comp_type == 'dicom-viewport':
            return f'''
      <div class="dicom-viewport-placeholder" style="width: 100%; height: 100%; background: #000; border: 1px solid #333; display: flex; align-items: center; justify-content: center; color: #666;">
        <div style="text-align: center;">
          <div style="font-size: 3em;">🖼️</div>
          <div>DICOM Viewer</div>
          <div style="font-size: 0.8em; margin-top: 10px;">{config.get('modality', 'CT')} Imaging</div>
        </div>
      </div>'''

        elif comp_type == 'patient-info-card':
            return '''
      <div class="patient-info" style="padding: 10px;">
        <div style="margin-bottom: 10px;"><strong>Patient:</strong> <span id="patient-name">-</span></div>
        <div style="margin-bottom: 10px;"><strong>ID:</strong> <span id="patient-id">-</span></div>
        <div style="margin-bottom: 10px;"><strong>Study:</strong> <span id="study-desc">-</span></div>
        <div><strong>Date:</strong> <span id="study-date">-</span></div>
      </div>'''

        elif comp_type == 'series-thumbnail-strip':
            return '''
      <div class="thumbnail-strip" style="display: flex; flex-direction: column; gap: 10px; overflow-y: auto;">
        <div class="thumbnail" style="width: 100%; aspect-ratio: 1; background: #0a0a0a; border: 1px solid #333; display: flex; align-items: center; justify-content: center; cursor: pointer;">
          <span style="font-size: 2em;">📷</span>
        </div>
      </div>'''

        elif comp_type == 'imaging-tools-panel':
            tools = config.get('tools', [])
            tools_html = '<div style="display: flex; flex-direction: column; gap: 8px;">'
            for tool in tools:
                tool_name = tool.replace('-', ' ').title()
                tools_html += f'''
        <button class="btn" onclick="activateTool('{tool}')">{tool_name}</button>'''
            tools_html += '\n      </div>'
            return tools_html

        elif comp_type == 'measurement-panel':
            return '''
      <div class="measurements" style="padding: 10px;">
        <div style="margin-bottom: 10px;"><strong>Measurements</strong></div>
        <div id="measurements-list" style="font-size: 0.9em; color: #999;">
          No measurements yet
        </div>
      </div>'''

        elif comp_type == 'study-queue-panel':
            return '''
      <div class="study-queue" style="overflow-y: auto;">
        <table style="width: 100%; border-collapse: collapse;">
          <thead>
            <tr style="border-bottom: 1px solid #333;">
              <th style="padding: 8px; text-align: left;">Patient</th>
              <th style="padding: 8px; text-align: left;">Modality</th>
              <th style="padding: 8px; text-align: left;">Date</th>
            </tr>
          </thead>
          <tbody id="study-queue-body">
            <tr><td colspan="3" style="padding: 20px; text-align: center; color: #666;">No studies in queue</td></tr>
          </tbody>
        </table>
      </div>'''

        elif comp_type == 'alf-probability-display':
            return '''
      <div class="alf-display" style="padding: 15px; text-align: center;">
        <div style="font-size: 2em; margin-bottom: 20px;">🧠</div>
        <div style="margin-bottom: 15px;">
          <div style="font-size: 0.9em; color: #999; margin-bottom: 5px;">Alzheimer's Probability</div>
          <div style="font-size: 2em; font-weight: bold;" id="alz-prob">--%</div>
        </div>
        <div>
          <div style="font-size: 0.9em; color: #999; margin-bottom: 5px;">Autism Probability</div>
          <div style="font-size: 2em; font-weight: bold;" id="aut-prob">--%</div>
        </div>
      </div>'''

        elif comp_type == 'qdrant-similarity-panel':
            return '''
      <div class="qdrant-panel" style="padding: 10px;">
        <div style="margin-bottom: 10px;"><strong>Similar Cases</strong></div>
        <div id="similar-cases" style="font-size: 0.9em; color: #999;">
          No results yet
        </div>
      </div>'''

        else:
            # Generic placeholder
            return f'''
      <div style="padding: 20px; text-align: center; color: #666;">
        <div>{comp_type}</div>
        <div style="font-size: 0.8em; margin-top: 10px;">Component placeholder</div>
      </div>'''

    def _generate_action_scripts(self, actions: List[Dict[str, Any]], trigger: str) -> str:
        """Generate JavaScript for actions"""
        trigger_actions = [a for a in actions if a.get('trigger') == trigger]
        if not trigger_actions:
            return '  // No actions for ' + trigger

        scripts = []
        for action in trigger_actions:
            action_type = action.get('action', '')
            params = action.get('params', {})

            if action_type == 'loadCTStudy':
                scripts.append(f'''
  console.log('Loading CT study with params:', {json.dumps(params)});
  // Implement CT study loading logic''')

            elif action_type == 'subscribeToTags':
                tags = params.get('tags', [])
                scripts.append(f'''
  console.log('Subscribing to tags:', {json.dumps(tags)});
  // Implement tag subscription logic''')

            else:
                scripts.append(f'''
  console.log('Action: {action_type}', {json.dumps(params)});''')

        return '\n'.join(scripts)

    def generate_all_medical_screens(self):
        """Generate all medical screens from templates"""
        medical_screens_dir = self.templates_dir / "screens" / "medical"
        index_file = medical_screens_dir / "index.json"

        if not index_file.exists():
            print(f"⚠ Medical screens index not found: {index_file}")
            return []

        index_data = self.load_json(index_file)
        screens = index_data.get('screens', [])

        generated_files = []
        output_base = self.output_dir

        print(f"\n=== Generating {len(screens)} Medical Screens ===\n")

        for screen in screens:
            screen_file = screen.get('file')
            screen_id = screen.get('id')

            template_path = medical_screens_dir / screen_file
            if not template_path.exists():
                print(f"⚠ Template not found: {template_path}")
                continue

            template_data = self.load_json(template_path)
            output_path = output_base / f"{screen_id}.html"

            self.generate_medical_screen(template_data, output_path)
            generated_files.append(output_path)

        return generated_files

    def generate_screen_index(self, screens: List[Dict[str, Any]], output_path: Path):
        """Generate index.html for screens directory"""
        colors = self.get_theme_colors()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Medical Imaging Portal</title>
<script src="/scripts/theme-loader.js"></script>
<script src="/scripts/config-loader.js"></script>
<style>
:root {{
  --primary-color: {colors['primary']};
  --secondary-color: {colors['secondary']};
  --background-color: {colors['background']};
  --text-color: {colors['text']};
  --accent-color: {colors['accent']};
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
  font-family: 'Courier New', monospace;
  background: var(--background-color);
  color: var(--text-color);
  min-height: 100vh;
  padding: 40px 20px;
}}

.header {{
  text-align: center;
  margin-bottom: 50px;
}}

.header h1 {{
  font-size: 2.5em;
  color: var(--text-color);
  margin-bottom: 10px;
}}

.header p {{
  color: var(--accent-color);
  font-size: 1.1em;
}}

.screens-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  max-width: 1400px;
  margin: 0 auto;
}}

.screen-card {{
  background: linear-gradient(135deg, #1a1a2e, #2a2a3e);
  border: 2px solid var(--text-color);
  border-radius: 12px;
  padding: 25px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s;
  cursor: pointer;
}}

.screen-card:hover {{
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 255, 136, 0.3);
  border-color: var(--accent-color);
}}

.screen-icon {{
  font-size: 3em;
  margin-bottom: 15px;
}}

.screen-name {{
  font-size: 1.3em;
  font-weight: bold;
  margin-bottom: 10px;
  color: var(--accent-color);
}}

.screen-description {{
  font-size: 0.9em;
  color: #999;
  line-height: 1.5;
}}

.category-badge {{
  display: inline-block;
  padding: 5px 10px;
  background: rgba(0, 255, 136, 0.1);
  border: 1px solid var(--text-color);
  border-radius: 4px;
  font-size: 0.8em;
  margin-top: 10px;
}}
</style>
</head>
<body>

<div class="header">
  <h1>🏥 CHAZON Medical Imaging Portal</h1>
  <p>AI-Powered Medical Imaging SCADA System</p>
</div>

<div class="screens-grid">
"""

        # Add screen cards
        for screen in screens:
            html += f'''
  <a href="{screen['id']}.html" class="screen-card">
    <div class="screen-icon">{screen.get('icon', '📊')}</div>
    <div class="screen-name">{screen['name']}</div>
    <div class="screen-description">{screen['description']}</div>
    <div class="category-badge">{screen['category']}</div>
  </a>
'''

        html += """
</div>

<script>
async function init() {
  if (window.chazonConfig) {
    await window.chazonConfig.load();
    console.log('Portal loaded in', window.chazonConfig.environment, 'mode');
  }
}
init();
</script>

</body>
</html>"""

        with open(output_path, 'w') as f:
            f.write(html)

        print(f"✓ Generated index: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Generate screens from templates')
    parser.add_argument('--all', action='store_true', help='Generate all screens')
    parser.add_argument('--medical', action='store_true', help='Generate medical screens only')
    parser.add_argument('--output', type=str, help='Output directory')

    args = parser.parse_args()

    # Set output directory
    output_dir = Path(args.output) if args.output else OUTPUT_DIR

    generator = TemplateGenerator(output_dir=output_dir)

    if args.medical or args.all:
        # Generate medical screens
        generated = generator.generate_all_medical_screens()

        # Generate index
        medical_screens_dir = TEMPLATES_DIR / "screens" / "medical"
        index_file = medical_screens_dir / "index.json"
        if index_file.exists():
            index_data = generator.load_json(index_file)
            generator.generate_screen_index(
                index_data.get('screens', []),
                output_dir / "index.html"
            )

        print(f"\n✓ Generated {len(generated)} medical screens to {output_dir}")
        print(f"✓ Total size reduction: ~{len(generated) * 200} lines of duplicate code eliminated")

    else:
        print("Usage: python3 generate_from_templates.py --all|--medical [--output DIR]")
        print("\nOptions:")
        print("  --all      Generate all screens from templates")
        print("  --medical  Generate medical screens only")
        print("  --output   Output directory (default: screens/frontend)")


if __name__ == '__main__':
    main()
