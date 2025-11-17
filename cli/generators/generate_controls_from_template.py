#!/usr/bin/env python3
"""
Control File Generator from Template
Generates plc.html, hmi.html, scada.html for all /os directories using template

This replaces 280+ duplicate control files with template-generated versions
that use the tag-based OS module loading system for GitHub Pages.

Usage:
    python3 generate_controls_from_template.py --all
    python3 generate_controls_from_template.py --section boot
    python3 generate_controls_from_template.py --dry-run
"""

import json
import argparse
from pathlib import Path
from typing import Dict, List

# Project root
ROOT_DIR = Path("/home/user/qdrant")
TEMPLATE_PATH = ROOT_DIR / "templates" / "controls" / "control-template.html"
OS_DIR = ROOT_DIR / "os"

# Control configuration per section
CONTROL_CONFIGS = {
    "boot": {
        "isa_level": "L0_Device",
        "tags": ["Boot", "System", "L0"],
        "status": "RUNNING"
    },
    "backend": {
        "isa_level": "L1_Control",
        "tags": ["Backend", "Services", "L1"],
        "status": "ACTIVE"
    },
    "frontend": {
        "isa_level": "L2_Supervisory",
        "tags": ["Frontend", "UI", "L2"],
        "status": "OPERATIONAL"
    },
    "medical": {
        "isa_level": "L3_MES",
        "tags": ["Medical", "Imaging", "L3"],
        "status": "READY"
    },
    "data": {
        "isa_level": "L2_Supervisory",
        "tags": ["Data", "Storage", "L2"],
        "status": "READY"
    },
    "models": {
        "isa_level": "L3_MES",
        "tags": ["Models", "AI", "L3"],
        "status": "LOADED"
    },
    "modules": {
        "isa_level": "L2_Supervisory",
        "tags": ["Modules", "Components", "L2"],
        "status": "READY"
    },
    "language": {
        "isa_level": "L3_MES",
        "tags": ["Language", "NLP", "L3"],
        "status": "READY"
    },
    "controls": {
        "isa_level": "L1_Control",
        "tags": ["Controls", "Automation", "L1"],
        "status": "ACTIVE"
    },
    "equipment": {
        "isa_level": "L1_Control",
        "tags": ["Equipment", "Hardware", "L1"],
        "status": "OPERATIONAL"
    },
    "logs": {
        "isa_level": "L2_Supervisory",
        "tags": ["Logs", "Monitoring", "L2"],
        "status": "LOGGING"
    },
    "debug": {
        "isa_level": "L2_Supervisory",
        "tags": ["Debug", "Development", "L2"],
        "status": "DEBUG"
    },
    "scada": {
        "isa_level": "L2_Supervisory",
        "tags": ["SCADA", "Monitoring", "L2"],
        "status": "MONITORING"
    }
}

# Control types
CONTROL_TYPES = {
    "plc": {
        "name": "PLC Interface",
        "description": "Programmable Logic Controller"
    },
    "hmi": {
        "name": "HMI Interface",
        "description": "Human Machine Interface"
    },
    "scada": {
        "name": "SCADA Interface",
        "description": "Supervisory Control and Data Acquisition"
    }
}


class ControlGenerator:
    """Generates control files from template"""

    def __init__(self, template_path: Path = TEMPLATE_PATH):
        self.template_path = template_path
        self.template = self._load_template()

    def _load_template(self) -> str:
        """Load control template"""
        with open(self.template_path, 'r') as f:
            return f.read()

    def generate_control_file(
        self,
        control_type: str,
        section_name: str,
        output_path: Path
    ) -> Path:
        """Generate a single control file from template"""

        # Get config for this section
        config = CONTROL_CONFIGS.get(section_name.lower(), {
            "isa_level": "L2_Supervisory",
            "tags": [section_name.title(), "System"],
            "status": "READY"
        })

        # Get control type info
        type_info = CONTROL_TYPES.get(control_type.lower(), {
            "name": f"{control_type.upper()} Interface",
            "description": f"{control_type.upper()} control interface"
        })

        # Build breadcrumb path
        breadcrumb = self._build_breadcrumb(output_path)

        # Replace template variables
        content = self.template
        replacements = {
            "{{CONTROL_NAME}}": f"{section_name.title()} {type_info['name']}",
            "{{SECTION_NAME}}": section_name.title(),
            "{{BREADCRUMB_PATH}}": breadcrumb,
            "{{CONTROL_TAGS}}": json.dumps(config["tags"]),
            "{{ISA_LEVEL}}": config["isa_level"],
            "{{STATUS}}": config["status"]
        }

        for placeholder, value in replacements.items():
            content = content.replace(placeholder, value)

        # Write file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(content)

        return output_path

    def _build_breadcrumb(self, file_path: Path) -> str:
        """Build breadcrumb navigation path"""
        rel_path = file_path.relative_to(ROOT_DIR)
        parts = list(rel_path.parts[:-1])  # Exclude filename

        # Build breadcrumb
        crumbs = []
        for i, part in enumerate(parts):
            if part == 'os':
                crumbs.append('OS')
            else:
                crumbs.append(part.title())

        return ' / '.join(crumbs) if crumbs else 'Root'

    def generate_for_directory(
        self,
        directory: Path,
        control_types: List[str] = None
    ) -> List[Path]:
        """Generate control files for a directory"""

        if control_types is None:
            control_types = ['plc', 'hmi', 'scada']

        generated = []
        section_name = directory.name

        for control_type in control_types:
            output_path = directory / f"{control_type}.html"
            self.generate_control_file(control_type, section_name, output_path)
            generated.append(output_path)
            print(f"✓ Generated: {output_path}")

        return generated

    def generate_for_all_os_directories(
        self,
        control_types: List[str] = None,
        dry_run: bool = False
    ) -> Dict[str, List[Path]]:
        """Generate control files for all /os subdirectories"""

        results = {}
        total_generated = 0

        # Get all immediate subdirectories of /os
        os_subdirs = [d for d in OS_DIR.iterdir() if d.is_dir()]

        print(f"\n=== Generating control files for {len(os_subdirs)} /os directories ===\n")

        for subdir in sorted(os_subdirs):
            section_name = subdir.name
            print(f"\n{section_name}:")

            if dry_run:
                print(f"  Would generate: plc.html, hmi.html, scada.html")
                results[section_name] = []
            else:
                generated = self.generate_for_directory(subdir, control_types)
                results[section_name] = generated
                total_generated += len(generated)

        if not dry_run:
            print(f"\n✓ Generated {total_generated} control files across {len(results)} directories")
        else:
            print(f"\n[DRY RUN] Would generate {len(os_subdirs) * 3} control files")

        return results

    def generate_nested_controls(
        self,
        root_dir: Path,
        control_types: List[str] = None,
        dry_run: bool = False
    ) -> int:
        """Recursively generate controls for nested directories"""

        count = 0

        # Generate for this directory if it has subdirectories
        subdirs = [d for d in root_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]

        if len(subdirs) > 0:
            section_name = root_dir.name

            print(f"{root_dir.relative_to(ROOT_DIR)}:")

            if not dry_run:
                generated = self.generate_for_directory(root_dir, control_types)
                count += len(generated)
            else:
                print(f"  Would generate: {', '.join(control_types or ['plc', 'hmi', 'scada'])}.html")
                count += len(control_types or 3)

        # Recurse into subdirectories
        for subdir in subdirs:
            if not subdir.name.startswith('.'):
                count += self.generate_nested_controls(subdir, control_types, dry_run)

        return count


def main():
    parser = argparse.ArgumentParser(description='Generate control files from template')
    parser.add_argument('--all', action='store_true', help='Generate for all /os directories')
    parser.add_argument('--section', type=str, help='Generate for specific section (e.g., boot, medical)')
    parser.add_argument('--nested', action='store_true', help='Generate recursively for nested directories')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be generated without creating files')
    parser.add_argument('--types', type=str, help='Control types to generate (comma-separated: plc,hmi,scada)')

    args = parser.parse_args()

    # Parse control types
    control_types = None
    if args.types:
        control_types = [t.strip() for t in args.types.split(',')]

    generator = ControlGenerator()

    if args.all:
        # Generate for all /os subdirectories
        generator.generate_for_all_os_directories(control_types, args.dry_run)

    elif args.section:
        # Generate for specific section
        section_dir = OS_DIR / args.section
        if not section_dir.exists():
            print(f"Error: Section directory not found: {section_dir}")
            return

        if args.nested:
            count = generator.generate_nested_controls(section_dir, control_types, args.dry_run)
            if not args.dry_run:
                print(f"\n✓ Generated {count} control files (recursive)")
        else:
            generated = generator.generate_for_directory(section_dir, control_types)
            print(f"\n✓ Generated {len(generated)} files for {args.section}")

    elif args.nested:
        # Generate recursively for entire /os directory
        print(f"\n=== Generating controls recursively for /os ===\n")
        count = generator.generate_nested_controls(OS_DIR, control_types, args.dry_run)
        if not args.dry_run:
            print(f"\n✓ Generated {count} control files (recursive)")
        else:
            print(f"\n[DRY RUN] Would generate {count} control files")

    else:
        print("Usage: python3 generate_controls_from_template.py [--all|--section NAME] [--nested] [--dry-run]")
        print("\nExamples:")
        print("  --all                    Generate for all /os directories")
        print("  --section boot           Generate for /os/boot only")
        print("  --section boot --nested  Generate recursively for /os/boot and subdirs")
        print("  --nested                 Generate recursively for entire /os tree")
        print("  --dry-run                Preview what would be generated")
        print("  --types plc,hmi          Generate only specific control types")


if __name__ == '__main__':
    main()
