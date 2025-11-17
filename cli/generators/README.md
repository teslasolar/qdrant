# Generator Scripts
**CLI Tools** | Code Generation Utilities

## Overview

This directory contains Python scripts used to generate boilerplate code, directory structures, and configuration files for the CHAZON Medical Imaging SCADA system.

## Scripts

### ⭐ generate_from_templates.py (RECOMMENDED)
**Purpose:** Universal template-based generator for screens, components, and controls

**Features:**
- Generates all screens from JSON templates (templates/screens/)
- Automatic theme integration from theme.yaml
- Config-driven generation (demo/dev/prod modes)
- Reduces codebase size by 75% through template reuse
- Eliminates duplicate CSS/JS code across screens
- Consistent ISA-101 HMI design

**Size Reduction:**
- **5 Medical screens:** 16.5K templates → 40.6K generated HTML (vs 80K+ hand-written)
- **40+ JSON templates:** Reusable across entire project
- **~75% reduction** in total codebase size

**Usage:**
```bash
# Generate all medical screens
python3 cli/generators/generate_from_templates.py --medical

# Generate all screens from templates
python3 cli/generators/generate_from_templates.py --all

# Custom output directory
python3 cli/generators/generate_from_templates.py --medical --output ./build/screens
```

**Output:**
```
screens/frontend/
├── index.html (generated)
├── pacs-dashboard.html (generated)
├── ct-workstation.html (generated)
├── mri-workstation.html (generated)
├── xray-workstation.html (generated)
└── alf-screening.html (generated)
```

**Benefits:**
- **Maintainability:** Change template once, regenerate all screens
- **Consistency:** All screens use same theme, structure, and config system
- **Size:** Dramatically reduced file count and duplicate code
- **Integration:** Auto-loads theme.yaml and config.yaml

---

### generate_control_structure.py
**Purpose:** Creates complete control system directory structure

**Features:**
- Generates controls/, scada/, plc/, hmi/, tags/ subdirectories
- Creates index/tag.json metadata for each control interface
- Applies ISA-95 level categorization (L0-L4)
- Auto-generates README.md files for each control subsystem

**Usage:**
```bash
./cli/generators/generate_control_structure.py
```

**Output:**
```
os/scripts/controls/
├── scada/
│   ├── index/tag.json
│   ├── index.html
│   └── README.md
├── plc/
├── hmi/
└── tags/
```

---

### generate_controls.py
**Purpose:** Generates control interface boilerplate

**Features:**
- Creates standardized control interfaces
- ISA-95 L1/L2 control system templates
- Tag provider integration

**Usage:**
```bash
./cli/generators/generate_controls.py
```

---

### generate_indexes.py
**Purpose:** Basic index.html generator for directories

**Features:**
- Creates simple index.html files
- Directory navigation
- Basic file listings

**Usage:**
```bash
./cli/generators/generate_indexes.py
```

---

### generate_indexes_enhanced.py
**Purpose:** Enhanced index generator with full navigation hierarchy

**Features:**
- Parent, child, sibling directory navigation
- Comprehensive file listings
- ISA-95 level categorization
- JSON metadata generation (index/tag.json)

**Usage:**
```bash
./cli/generators/generate_indexes_enhanced.py
```

**Output:**
- Creates index/tag.json with UUID, title, ISA level
- Generates hierarchical navigation links
- Lists all files and subdirectories

---

### generate_interface_files.py
**Purpose:** Generate HMI, PLC, SCADA interface files (v1)

**Features:**
- Creates hmi.html, plc.html, scada.html for directories
- Basic navigation based on existing files
- Simple interface templates

**Usage:**
```bash
./cli/generators/generate_interface_files.py
```

---

### generate_interface_files_v2.py
**Purpose:** Enhanced interface file generator (v2)

**Features:**
- Improved HMI, PLC, SCADA interface generation
- Dynamic navigation based on actual file existence
- Checks for index.html, README.md presence
- Relative path calculation for nested directories
- ISA-101 compliant HMI design

**Usage:**
```bash
./cli/generators/generate_interface_files_v2.py
```

**Template Features:**
- Control buttons with visual indicators
- Status displays
- Responsive navigation
- Theme integration

---

### generate_status.py
**Purpose:** Generate system status reports

**Features:**
- Directory structure analysis
- File count statistics
- System health checks
- Status documentation generation

**Usage:**
```bash
./cli/generators/generate_status.py
```

## Common Patterns

### ISA-95 Level Categorization
All generators use consistent ISA-95 level mapping:

```python
CATEGORY_MAP = {
    'cli': 'L3_MES',
    'docs': 'L4_Business',
    'os': 'L3_MES',
    'os/controls': 'L2_Supervisory',
    'os/equipment': 'L2_Supervisory',
    'os/scripts': 'L1_Control',
    # ... etc
}
```

### Tag JSON Structure
Standard metadata format (index/tag.json):

```json
{
  "uuid": "generated-uuid-here",
  "title": "Descriptive Title",
  "isa_level": "L2_Supervisory",
  "type": "control_interface",
  "version": "1.0"
}
```

### Directory Scanning
Most scripts recursively scan from `/home/user/qdrant/`:

```python
ROOT_DIR = Path("/home/user/qdrant")

for root, dirs, files in os.walk(ROOT_DIR):
    # Process directories
```

## Best Practices

1. **Run from project root:**
   ```bash
   cd /home/user/qdrant
   ./cli/generators/script_name.py
   ```

2. **Backup before running:**
   - Generators may overwrite existing files
   - Use version control before generation

3. **Review generated files:**
   - Check for correct paths
   - Verify ISA-95 level assignments
   - Test navigation links

4. **Use v2 scripts when available:**
   - `generate_interface_files_v2.py` preferred over v1
   - `generate_indexes_enhanced.py` preferred over basic

## Migration Notes

**Previous location:** `/` (root directory)
**New location:** `/cli/generators/`
**Date moved:** 2025-11-17
**Reason:** Root directory cleanup - organizing legacy scripts

## Integration

These generators work with:
- **Tag System:** Creates index/tag.json metadata
- **Theme System:** Uses theme.yaml and ISA-101 styles
- **Database System:** Generated tags can be migrated to SQLite via database/migrate.py
- **Config System:** Respects config.yaml environment settings

## Development

### Adding New Generator

1. **Create script:**
   ```bash
   touch cli/generators/generate_new_feature.py
   chmod +x cli/generators/generate_new_feature.py
   ```

2. **Add shebang and docstring:**
   ```python
   #!/usr/bin/env python3
   """
   Description of what this generator does
   """
   ```

3. **Follow patterns:**
   - Use ROOT_DIR = Path("/home/user/qdrant")
   - Apply ISA-95 categorization
   - Generate index/tag.json metadata
   - Create comprehensive documentation

4. **Update this README:**
   - Add script description
   - Document usage
   - Note any special features

---

**Auto-generated documentation**
Last updated: 2025-11-17
