#!/usr/bin/env python3
"""
Qdrant Project Statistics Generator
====================================
Generates comprehensive statistics about the project structure and content.

Usage:
    python3 cli/project-stats.py [--output FORMAT] [--export FILE]

Options:
    --output FORMAT    Output format: text, json, markdown, html (default: text)
    --export FILE      Export statistics to file
    --detailed         Show detailed breakdown by directory
    --chart            Generate ASCII charts (text mode only)

Statistics collected:
- File counts by type
- Directory structure depth
- Code metrics (lines, comments)
- ISA-95 hierarchy statistics
- Tag statistics
- Size analysis
- Recent activity
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

class ProjectStats:
    def __init__(self, detailed: bool = False, show_charts: bool = False):
        self.detailed = detailed
        self.show_charts = show_charts
        self.root_dir = Path(__file__).parent.parent.resolve()

        self.stats = {
            'files': defaultdict(int),
            'directories': {
                'total': 0,
                'by_depth': defaultdict(int),
                'largest': []
            },
            'code': {
                'total_lines': 0,
                'by_language': defaultdict(lambda: {'files': 0, 'lines': 0, 'size': 0})
            },
            'tags': {
                'total': 0,
                'by_isa_level': defaultdict(int),
                'valid': 0,
                'invalid': 0
            },
            'size': {
                'total': 0,
                'by_type': defaultdict(int),
                'largest_files': []
            },
            'activity': {
                'modified_last_day': 0,
                'modified_last_week': 0,
                'modified_last_month': 0
            },
            'controls': {
                'hmi_screens': 0,
                'hmi_templates': 0,
                'plc_files': 0,
                'scada_files': 0
            }
        }

        self.exclude_dirs = ['.git', 'node_modules', 'venv', '__pycache__', '.pytest_cache']

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        for exclude in self.exclude_dirs:
            if exclude in path.parts:
                return True
        return False

    def format_size(self, size: int) -> str:
        """Format size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}TB"

    def count_lines(self, file_path: Path) -> int:
        """Count lines in a text file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return sum(1 for _ in f)
        except:
            return 0

    def get_language_from_extension(self, ext: str) -> str:
        """Map file extension to language"""
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.html': 'HTML',
            '.css': 'CSS',
            '.json': 'JSON',
            '.md': 'Markdown',
            '.sql': 'SQL',
            '.sh': 'Shell',
            '.yaml': 'YAML',
            '.yml': 'YAML',
            '.xml': 'XML',
            '.c': 'C',
            '.cpp': 'C++',
            '.h': 'C/C++ Header',
            '.java': 'Java',
            '.go': 'Go',
            '.rs': 'Rust'
        }
        return lang_map.get(ext, 'Other')

    def collect_file_stats(self):
        """Collect statistics about files"""
        print(f"{Colors.BLUE}Collecting file statistics...{Colors.END}")

        now = datetime.now()
        one_day_ago = now - timedelta(days=1)
        one_week_ago = now - timedelta(days=7)
        one_month_ago = now - timedelta(days=30)

        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and not self.should_exclude(file_path):
                # Count by extension
                ext = file_path.suffix.lower()
                self.stats['files'][ext if ext else 'no_extension'] += 1

                # Get file size
                try:
                    size = file_path.stat().st_size
                    self.stats['size']['total'] += size
                    self.stats['size']['by_type'][ext] += size

                    # Track largest files
                    self.stats['size']['largest_files'].append((file_path, size))

                    # Check modification time
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime > one_day_ago:
                        self.stats['activity']['modified_last_day'] += 1
                    if mtime > one_week_ago:
                        self.stats['activity']['modified_last_week'] += 1
                    if mtime > one_month_ago:
                        self.stats['activity']['modified_last_month'] += 1

                    # Code statistics
                    language = self.get_language_from_extension(ext)
                    if ext in ['.py', '.js', '.ts', '.html', '.css', '.sql', '.sh', '.c', '.cpp', '.java', '.go', '.rs']:
                        lines = self.count_lines(file_path)
                        self.stats['code']['total_lines'] += lines
                        self.stats['code']['by_language'][language]['files'] += 1
                        self.stats['code']['by_language'][language]['lines'] += lines
                        self.stats['code']['by_language'][language]['size'] += size

                except:
                    pass

        # Sort largest files
        self.stats['size']['largest_files'].sort(key=lambda x: x[1], reverse=True)
        self.stats['size']['largest_files'] = self.stats['size']['largest_files'][:10]

    def collect_directory_stats(self):
        """Collect statistics about directories"""
        print(f"{Colors.BLUE}Collecting directory statistics...{Colors.END}")

        dir_sizes = []

        for dir_path in self.root_dir.rglob('*'):
            if dir_path.is_dir() and not self.should_exclude(dir_path):
                self.stats['directories']['total'] += 1

                # Calculate depth
                try:
                    depth = len(dir_path.relative_to(self.root_dir).parts)
                    self.stats['directories']['by_depth'][depth] += 1
                except:
                    pass

                # Calculate directory size
                try:
                    total_size = sum(f.stat().st_size for f in dir_path.rglob('*') if f.is_file())
                    dir_sizes.append((dir_path, total_size))
                except:
                    pass

        # Sort and store largest directories
        dir_sizes.sort(key=lambda x: x[1], reverse=True)
        self.stats['directories']['largest'] = dir_sizes[:10]

    def collect_tag_stats(self):
        """Collect statistics about tag.json files"""
        print(f"{Colors.BLUE}Collecting tag statistics...{Colors.END}")

        tag_files = list(self.root_dir.glob('**/tag.json'))
        self.stats['tags']['total'] = len(tag_files)

        for tag_file in tag_files:
            try:
                with open(tag_file, 'r') as f:
                    data = json.load(f)

                    # Count by ISA level
                    if 'ISA_Level' in data:
                        self.stats['tags']['by_isa_level'][data['ISA_Level']] += 1

                    # Check validity (basic check)
                    required_fields = ['UUID', 'ISA_Level', 'Directory_Path', 'Title']
                    if all(field in data for field in required_fields):
                        self.stats['tags']['valid'] += 1
                    else:
                        self.stats['tags']['invalid'] += 1

            except:
                self.stats['tags']['invalid'] += 1

    def collect_controls_stats(self):
        """Collect statistics about controls (HMI, PLC, SCADA)"""
        print(f"{Colors.BLUE}Collecting controls statistics...{Colors.END}")

        # Count HMI screens
        hmi_screens = list(self.root_dir.glob('**/HMI/screens/**/*.json'))
        self.stats['controls']['hmi_screens'] = len(hmi_screens)

        # Count HMI templates
        hmi_templates = list(self.root_dir.glob('**/HMI/templates/**/*.json'))
        self.stats['controls']['hmi_templates'] = len(hmi_templates)

        # Count PLC files
        plc_files = list(self.root_dir.glob('**/plc/**/*'))
        self.stats['controls']['plc_files'] = len([f for f in plc_files if f.is_file()])

        # Count SCADA files
        scada_files = list(self.root_dir.glob('**/scada/**/*'))
        self.stats['controls']['scada_files'] = len([f for f in scada_files if f.is_file()])

    def generate_ascii_chart(self, data: Dict[str, int], title: str, max_width: int = 40):
        """Generate ASCII bar chart"""
        if not data:
            return

        print(f"\n{Colors.BOLD}{title}{Colors.END}")
        print("-" * 60)

        max_value = max(data.values())
        for key, value in sorted(data.items(), key=lambda x: x[1], reverse=True)[:10]:
            bar_width = int((value / max_value) * max_width) if max_value > 0 else 0
            bar = '█' * bar_width
            print(f"{key:20s} {bar} {value}")

    def print_text_report(self):
        """Print statistics in text format"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}  Qdrant Project Statistics{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")

        # Overview
        print(f"{Colors.BOLD}Overview{Colors.END}")
        print("=" * 70)
        print(f"Total Files:           {sum(self.stats['files'].values()):,}")
        print(f"Total Directories:     {self.stats['directories']['total']:,}")
        print(f"Total Size:            {self.format_size(self.stats['size']['total'])}")
        print(f"Total Lines of Code:   {self.stats['code']['total_lines']:,}")

        # File Types
        print(f"\n{Colors.BOLD}File Types{Colors.END}")
        print("=" * 70)
        file_types = sorted(self.stats['files'].items(), key=lambda x: x[1], reverse=True)
        for ext, count in file_types[:15]:
            size = self.stats['size']['by_type'].get(ext, 0)
            print(f"{ext:20s} {count:6,} files  {self.format_size(size):>10s}")

        if self.show_charts:
            self.generate_ascii_chart(
                dict(file_types[:10]),
                "File Type Distribution"
            )

        # Code Statistics
        if self.stats['code']['by_language']:
            print(f"\n{Colors.BOLD}Code Statistics{Colors.END}")
            print("=" * 70)
            for lang, stats in sorted(self.stats['code']['by_language'].items(),
                                    key=lambda x: x[1]['lines'], reverse=True):
                print(f"{lang:20s} {stats['files']:4} files  "
                      f"{stats['lines']:8,} lines  "
                      f"{self.format_size(stats['size']):>10s}")

        # Tag Statistics
        print(f"\n{Colors.BOLD}Tag Statistics{Colors.END}")
        print("=" * 70)
        print(f"Total tag.json files:  {self.stats['tags']['total']}")
        print(f"Valid tags:            {self.stats['tags']['valid']}")
        print(f"Invalid tags:          {self.stats['tags']['invalid']}")

        if self.stats['tags']['by_isa_level']:
            print(f"\nISA-95 Level Distribution:")
            for level, count in sorted(self.stats['tags']['by_isa_level'].items(),
                                      key=lambda x: x[1], reverse=True):
                print(f"  {level:20s} {count:4} tags")

        # Controls Statistics
        print(f"\n{Colors.BOLD}Controls Statistics{Colors.END}")
        print("=" * 70)
        print(f"HMI Screens:           {self.stats['controls']['hmi_screens']}")
        print(f"HMI Templates:         {self.stats['controls']['hmi_templates']}")
        print(f"PLC Files:             {self.stats['controls']['plc_files']}")
        print(f"SCADA Files:           {self.stats['controls']['scada_files']}")

        # Directory Structure
        print(f"\n{Colors.BOLD}Directory Structure{Colors.END}")
        print("=" * 70)
        max_depth = max(self.stats['directories']['by_depth'].keys()) if self.stats['directories']['by_depth'] else 0
        print(f"Maximum depth:         {max_depth}")
        print(f"\nDepth distribution:")
        for depth in sorted(self.stats['directories']['by_depth'].keys()):
            count = self.stats['directories']['by_depth'][depth]
            print(f"  Level {depth}:            {count} directories")

        # Largest Directories
        if self.stats['directories']['largest']:
            print(f"\n{Colors.BOLD}Largest Directories{Colors.END}")
            print("=" * 70)
            for dir_path, size in self.stats['directories']['largest']:
                rel_path = dir_path.relative_to(self.root_dir)
                print(f"{str(rel_path):50s} {self.format_size(size):>10s}")

        # Largest Files
        if self.stats['size']['largest_files']:
            print(f"\n{Colors.BOLD}Largest Files{Colors.END}")
            print("=" * 70)
            for file_path, size in self.stats['size']['largest_files']:
                rel_path = file_path.relative_to(self.root_dir)
                print(f"{str(rel_path):50s} {self.format_size(size):>10s}")

        # Activity
        print(f"\n{Colors.BOLD}Recent Activity{Colors.END}")
        print("=" * 70)
        print(f"Modified in last 24h:  {self.stats['activity']['modified_last_day']}")
        print(f"Modified in last week: {self.stats['activity']['modified_last_week']}")
        print(f"Modified in last month:{self.stats['activity']['modified_last_month']}")

        print(f"\n{Colors.CYAN}{'='*70}{Colors.END}\n")

    def generate_json_report(self) -> Dict:
        """Generate statistics in JSON format"""
        # Convert defaultdicts to regular dicts for JSON serialization
        json_stats = {
            'timestamp': datetime.now().isoformat(),
            'files': dict(self.stats['files']),
            'directories': {
                'total': self.stats['directories']['total'],
                'by_depth': dict(self.stats['directories']['by_depth']),
                'largest': [
                    {
                        'path': str(p.relative_to(self.root_dir)),
                        'size': s,
                        'size_formatted': self.format_size(s)
                    }
                    for p, s in self.stats['directories']['largest']
                ]
            },
            'code': {
                'total_lines': self.stats['code']['total_lines'],
                'by_language': {
                    lang: dict(stats)
                    for lang, stats in self.stats['code']['by_language'].items()
                }
            },
            'tags': {
                'total': self.stats['tags']['total'],
                'by_isa_level': dict(self.stats['tags']['by_isa_level']),
                'valid': self.stats['tags']['valid'],
                'invalid': self.stats['tags']['invalid']
            },
            'size': {
                'total': self.stats['size']['total'],
                'total_formatted': self.format_size(self.stats['size']['total']),
                'by_type': {
                    ext: {'size': size, 'size_formatted': self.format_size(size)}
                    for ext, size in self.stats['size']['by_type'].items()
                },
                'largest_files': [
                    {
                        'path': str(p.relative_to(self.root_dir)),
                        'size': s,
                        'size_formatted': self.format_size(s)
                    }
                    for p, s in self.stats['size']['largest_files']
                ]
            },
            'activity': self.stats['activity'],
            'controls': self.stats['controls']
        }
        return json_stats

    def generate_markdown_report(self) -> str:
        """Generate statistics in Markdown format"""
        md = ["# Qdrant Project Statistics\n"]
        md.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")

        md.append("## Overview\n")
        md.append(f"- **Total Files:** {sum(self.stats['files'].values()):,}\n")
        md.append(f"- **Total Directories:** {self.stats['directories']['total']:,}\n")
        md.append(f"- **Total Size:** {self.format_size(self.stats['size']['total'])}\n")
        md.append(f"- **Total Lines of Code:** {self.stats['code']['total_lines']:,}\n")

        md.append("\n## File Types\n")
        md.append("| Extension | Count | Size |\n")
        md.append("|-----------|-------|------|\n")
        for ext, count in sorted(self.stats['files'].items(), key=lambda x: x[1], reverse=True)[:15]:
            size = self.stats['size']['by_type'].get(ext, 0)
            md.append(f"| {ext} | {count:,} | {self.format_size(size)} |\n")

        md.append("\n## Code Statistics\n")
        md.append("| Language | Files | Lines | Size |\n")
        md.append("|----------|-------|-------|------|\n")
        for lang, stats in sorted(self.stats['code']['by_language'].items(),
                                 key=lambda x: x[1]['lines'], reverse=True):
            md.append(f"| {lang} | {stats['files']} | {stats['lines']:,} | "
                     f"{self.format_size(stats['size'])} |\n")

        md.append("\n## Tag Statistics\n")
        md.append(f"- **Total tag.json files:** {self.stats['tags']['total']}\n")
        md.append(f"- **Valid tags:** {self.stats['tags']['valid']}\n")
        md.append(f"- **Invalid tags:** {self.stats['tags']['invalid']}\n")

        md.append("\n### ISA-95 Level Distribution\n")
        for level, count in sorted(self.stats['tags']['by_isa_level'].items(),
                                  key=lambda x: x[1], reverse=True):
            md.append(f"- **{level}:** {count}\n")

        md.append("\n## Controls Statistics\n")
        md.append(f"- **HMI Screens:** {self.stats['controls']['hmi_screens']}\n")
        md.append(f"- **HMI Templates:** {self.stats['controls']['hmi_templates']}\n")
        md.append(f"- **PLC Files:** {self.stats['controls']['plc_files']}\n")
        md.append(f"- **SCADA Files:** {self.stats['controls']['scada_files']}\n")

        return ''.join(md)

    def export_report(self, export_file: str, output_format: str):
        """Export report to file"""
        export_path = self.root_dir / export_file

        if output_format == 'json':
            with open(export_path, 'w') as f:
                json.dump(self.generate_json_report(), f, indent=2)
        elif output_format == 'markdown':
            with open(export_path, 'w') as f:
                f.write(self.generate_markdown_report())
        else:  # text
            # Redirect stdout to file
            original_stdout = sys.stdout
            with open(export_path, 'w') as f:
                sys.stdout = f
                self.print_text_report()
                sys.stdout = original_stdout

        print(f"{Colors.GREEN}✓{Colors.END} Report exported to: {export_file}")

    def run(self, output_format: str = 'text', export_file: str = None):
        """Run statistics collection and generate report"""
        self.collect_file_stats()
        self.collect_directory_stats()
        self.collect_tag_stats()
        self.collect_controls_stats()

        if output_format == 'json':
            print(json.dumps(self.generate_json_report(), indent=2))
        elif output_format == 'markdown':
            print(self.generate_markdown_report())
        else:  # text
            self.print_text_report()

        if export_file:
            self.export_report(export_file, output_format)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate project statistics',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--output', '-o', type=str, default='text',
                       choices=['text', 'json', 'markdown', 'html'],
                       help='Output format (default: text)')
    parser.add_argument('--export', '-e', type=str,
                       help='Export report to file')
    parser.add_argument('--detailed', '-d', action='store_true',
                       help='Show detailed breakdown')
    parser.add_argument('--chart', '-c', action='store_true',
                       help='Generate ASCII charts (text mode only)')

    args = parser.parse_args()

    stats = ProjectStats(detailed=args.detailed, show_charts=args.chart)
    stats.run(output_format=args.output, export_file=args.export)


if __name__ == '__main__':
    main()
