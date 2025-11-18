#!/usr/bin/env python3
"""
Qdrant Project Unused Files Finder
===================================
Finds and reports files that may be unused or orphaned in the project.

Usage:
    python3 cli/find-unused-files.py [--delete] [--extensions .py,.js,.json]

Options:
    --delete              Delete unused files (use with caution!)
    --extensions EXT      Comma-separated list of extensions to check (default: all)
    --min-size SIZE       Minimum file size in bytes to report (default: 0)
    --exclude-dirs DIRS   Comma-separated list of directories to exclude
    --report FILE         Save report to file

Categories of unused files:
- Orphaned files without parent index
- Empty directories
- Duplicate files (same content)
- Temporary/backup files (.bak, .tmp, ~)
- Old log files
"""

import os
import sys
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Set
from datetime import datetime, timedelta

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class UnusedFilesFinder:
    def __init__(self,
                 delete: bool = False,
                 extensions: List[str] = None,
                 min_size: int = 0,
                 exclude_dirs: List[str] = None,
                 report_file: str = None):
        self.delete = delete
        self.extensions = extensions
        self.min_size = min_size
        self.exclude_dirs = exclude_dirs or []
        self.report_file = report_file
        self.root_dir = Path(__file__).parent.parent.resolve()

        # Default exclusions
        self.exclude_dirs.extend([
            '.git',
            'node_modules',
            'venv',
            '__pycache__',
            '.pytest_cache'
        ])

        self.findings = {
            'temp_files': [],
            'empty_dirs': [],
            'duplicate_files': [],
            'old_logs': [],
            'orphaned_files': [],
            'large_files': []
        }

    def log_info(self, message: str):
        """Log informational message"""
        print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

    def log_warning(self, message: str):
        """Log warning message"""
        print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

    def log_success(self, message: str):
        """Log success message"""
        print(f"{Colors.GREEN}✓{Colors.END} {message}")

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded"""
        for exclude in self.exclude_dirs:
            if exclude in path.parts:
                return True
        return False

    def get_file_hash(self, file_path: Path) -> str:
        """Calculate MD5 hash of file content"""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return None

    def find_temp_files(self):
        """Find temporary and backup files"""
        print(f"\n{Colors.BOLD}Finding Temporary/Backup Files{Colors.END}")
        print("=" * 60)

        temp_patterns = [
            '*.bak',
            '*.tmp',
            '*.temp',
            '*~',
            '*.swp',
            '*.swo',
            '.DS_Store',
            'Thumbs.db',
            '*.pyc',
            '*.pyo'
        ]

        for pattern in temp_patterns:
            for file_path in self.root_dir.rglob(pattern):
                if not self.should_exclude(file_path):
                    self.findings['temp_files'].append(file_path)

        if self.findings['temp_files']:
            self.log_warning(f"Found {len(self.findings['temp_files'])} temporary/backup files:")
            for file_path in self.findings['temp_files']:
                size = file_path.stat().st_size if file_path.exists() else 0
                print(f"  - {file_path.relative_to(self.root_dir)} ({self.format_size(size)})")
        else:
            self.log_success("No temporary/backup files found")

    def find_empty_directories(self):
        """Find empty directories"""
        print(f"\n{Colors.BOLD}Finding Empty Directories{Colors.END}")
        print("=" * 60)

        for dir_path in self.root_dir.rglob('*'):
            if dir_path.is_dir() and not self.should_exclude(dir_path):
                # Check if directory is empty (no files, only empty subdirs allowed)
                has_files = False
                for item in dir_path.rglob('*'):
                    if item.is_file():
                        has_files = True
                        break

                if not has_files and dir_path != self.root_dir:
                    # Check if it's truly empty (no subdirs either)
                    if not any(dir_path.iterdir()):
                        self.findings['empty_dirs'].append(dir_path)

        if self.findings['empty_dirs']:
            self.log_warning(f"Found {len(self.findings['empty_dirs'])} empty directories:")
            for dir_path in self.findings['empty_dirs']:
                print(f"  - {dir_path.relative_to(self.root_dir)}/")
        else:
            self.log_success("No empty directories found")

    def find_duplicate_files(self):
        """Find files with identical content"""
        print(f"\n{Colors.BOLD}Finding Duplicate Files{Colors.END}")
        print("=" * 60)

        file_hashes = defaultdict(list)

        # Calculate hashes for all files
        file_count = 0
        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and not self.should_exclude(file_path):
                if self.extensions:
                    if file_path.suffix not in self.extensions:
                        continue

                file_hash = self.get_file_hash(file_path)
                if file_hash:
                    file_hashes[file_hash].append(file_path)
                    file_count += 1

        self.log_info(f"Analyzed {file_count} files")

        # Find duplicates
        duplicates = {h: files for h, files in file_hashes.items() if len(files) > 1}

        if duplicates:
            self.log_warning(f"Found {len(duplicates)} sets of duplicate files:")
            for file_hash, files in duplicates.items():
                size = files[0].stat().st_size
                print(f"\n  Duplicate set ({self.format_size(size)}):")
                for file_path in files:
                    print(f"    - {file_path.relative_to(self.root_dir)}")
                self.findings['duplicate_files'].extend(files[1:])  # Keep first, mark rest as duplicates
        else:
            self.log_success("No duplicate files found")

    def find_old_log_files(self, days: int = 30):
        """Find old log files"""
        print(f"\n{Colors.BOLD}Finding Old Log Files (>{days} days){Colors.END}")
        print("=" * 60)

        log_patterns = ['*.log', '*.log.*']
        cutoff_date = datetime.now() - timedelta(days=days)

        for pattern in log_patterns:
            for file_path in self.root_dir.rglob(pattern):
                if not self.should_exclude(file_path) and file_path.is_file():
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime < cutoff_date:
                        self.findings['old_logs'].append(file_path)

        if self.findings['old_logs']:
            self.log_warning(f"Found {len(self.findings['old_logs'])} old log files:")
            total_size = 0
            for file_path in self.findings['old_logs']:
                size = file_path.stat().st_size
                total_size += size
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                print(f"  - {file_path.relative_to(self.root_dir)} ({self.format_size(size)}, {mtime.strftime('%Y-%m-%d')})")
            print(f"\n  Total size: {self.format_size(total_size)}")
        else:
            self.log_success(f"No log files older than {days} days found")

    def find_orphaned_files(self):
        """Find files that might be orphaned (no references in index files)"""
        print(f"\n{Colors.BOLD}Finding Potentially Orphaned Files{Colors.END}")
        print("=" * 60)

        # Files that might be orphaned:
        # - HTML files without corresponding markdown
        # - Python scripts not imported anywhere
        # - JSON files not referenced in tag.json

        orphaned = []

        # Find HTML files without markdown
        html_files = list(self.root_dir.rglob('*.html'))
        for html_file in html_files:
            if self.should_exclude(html_file):
                continue

            # Check if there's a corresponding markdown or if it's referenced
            md_file = html_file.with_suffix('.md')
            if not md_file.exists() and html_file.name not in ['index.html', 'index-custom.html']:
                # Check if it's referenced in any tag.json
                referenced = False
                for tag_file in self.root_dir.rglob('**/tag.json'):
                    try:
                        import json
                        with open(tag_file) as f:
                            data = json.load(f)
                            if html_file.name in str(data):
                                referenced = True
                                break
                    except:
                        pass

                if not referenced:
                    orphaned.append(html_file)

        self.findings['orphaned_files'] = orphaned

        if orphaned:
            self.log_warning(f"Found {len(orphaned)} potentially orphaned files:")
            for file_path in orphaned:
                size = file_path.stat().st_size
                print(f"  - {file_path.relative_to(self.root_dir)} ({self.format_size(size)})")
        else:
            self.log_success("No obviously orphaned files found")

    def find_large_files(self, threshold_mb: int = 10):
        """Find unusually large files"""
        print(f"\n{Colors.BOLD}Finding Large Files (>{threshold_mb}MB){Colors.END}")
        print("=" * 60)

        threshold_bytes = threshold_mb * 1024 * 1024

        for file_path in self.root_dir.rglob('*'):
            if file_path.is_file() and not self.should_exclude(file_path):
                size = file_path.stat().st_size
                if size > threshold_bytes:
                    self.findings['large_files'].append((file_path, size))

        if self.findings['large_files']:
            # Sort by size
            self.findings['large_files'].sort(key=lambda x: x[1], reverse=True)

            self.log_warning(f"Found {len(self.findings['large_files'])} large files:")
            for file_path, size in self.findings['large_files']:
                print(f"  - {file_path.relative_to(self.root_dir)} ({self.format_size(size)})")
        else:
            self.log_success(f"No files larger than {threshold_mb}MB found")

    def format_size(self, size: int) -> str:
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}TB"

    def generate_summary(self):
        """Generate summary report"""
        print(f"\n{Colors.BOLD}Summary Report{Colors.END}")
        print("=" * 60)

        total_issues = sum(len(v) if isinstance(v, list) else 0
                          for v in self.findings.values())

        print(f"Temporary/Backup Files: {len(self.findings['temp_files'])}")
        print(f"Empty Directories:      {len(self.findings['empty_dirs'])}")
        print(f"Duplicate Files:        {len(self.findings['duplicate_files'])}")
        print(f"Old Log Files:          {len(self.findings['old_logs'])}")
        print(f"Orphaned Files:         {len(self.findings['orphaned_files'])}")
        print(f"Large Files:            {len(self.findings['large_files'])}")
        print(f"\nTotal items found:      {total_issues}")

        # Calculate potential space savings
        potential_savings = 0
        for file_list in [self.findings['temp_files'],
                         self.findings['duplicate_files'],
                         self.findings['old_logs']]:
            for file_path in file_list:
                if isinstance(file_path, Path) and file_path.exists():
                    potential_savings += file_path.stat().st_size

        if potential_savings > 0:
            print(f"\nPotential space savings: {self.format_size(potential_savings)}")

        # Save report if requested
        if self.report_file:
            self.save_report()

    def save_report(self):
        """Save findings to report file"""
        report_path = self.root_dir / self.report_file

        with open(report_path, 'w') as f:
            f.write("Qdrant Project - Unused Files Report\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            for category, files in self.findings.items():
                f.write(f"\n{category.replace('_', ' ').title()}\n")
                f.write("-" * 40 + "\n")
                if isinstance(files, list):
                    if files:
                        for item in files:
                            if isinstance(item, tuple):
                                file_path, size = item
                                f.write(f"  {file_path.relative_to(self.root_dir)} ({self.format_size(size)})\n")
                            else:
                                f.write(f"  {item.relative_to(self.root_dir)}\n")
                    else:
                        f.write("  None found\n")

        self.log_success(f"Report saved to: {report_path.relative_to(self.root_dir)}")

    def delete_files(self):
        """Delete unused files if --delete flag is set"""
        if not self.delete:
            return

        print(f"\n{Colors.BOLD}{Colors.RED}Deleting Unused Files{Colors.END}")
        print("=" * 60)

        files_to_delete = []
        files_to_delete.extend(self.findings['temp_files'])
        files_to_delete.extend(self.findings['old_logs'])

        if not files_to_delete:
            self.log_info("No files to delete")
            return

        # Confirm deletion
        print(f"{Colors.YELLOW}About to delete {len(files_to_delete)} files{Colors.END}")
        response = input("Are you sure? (yes/no): ")

        if response.lower() != 'yes':
            self.log_info("Deletion cancelled")
            return

        deleted_count = 0
        for file_path in files_to_delete:
            try:
                if file_path.exists():
                    file_path.unlink()
                    deleted_count += 1
                    print(f"  Deleted: {file_path.relative_to(self.root_dir)}")
            except Exception as e:
                self.log_warning(f"Could not delete {file_path.relative_to(self.root_dir)}: {e}")

        self.log_success(f"Deleted {deleted_count} files")

        # Delete empty directories
        for dir_path in self.findings['empty_dirs']:
            try:
                if dir_path.exists() and not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"  Removed directory: {dir_path.relative_to(self.root_dir)}")
            except Exception as e:
                self.log_warning(f"Could not remove directory {dir_path.relative_to(self.root_dir)}: {e}")

    def run(self):
        """Run all checks"""
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("=" * 60)
        print("  Qdrant Project - Unused Files Finder")
        print("=" * 60)
        print(f"{Colors.END}")

        self.find_temp_files()
        self.find_empty_directories()
        self.find_duplicate_files()
        self.find_old_log_files()
        self.find_orphaned_files()
        self.find_large_files()

        self.generate_summary()

        if self.delete:
            self.delete_files()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Find unused files in Qdrant project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--delete', '-d', action='store_true',
                       help='Delete unused files (with confirmation)')
    parser.add_argument('--extensions', '-e', type=str,
                       help='Comma-separated list of extensions to check')
    parser.add_argument('--min-size', '-m', type=int, default=0,
                       help='Minimum file size in bytes to report')
    parser.add_argument('--exclude-dirs', '-x', type=str,
                       help='Comma-separated list of directories to exclude')
    parser.add_argument('--report', '-r', type=str,
                       help='Save report to file')

    args = parser.parse_args()

    extensions = args.extensions.split(',') if args.extensions else None
    exclude_dirs = args.exclude_dirs.split(',') if args.exclude_dirs else []

    finder = UnusedFilesFinder(
        delete=args.delete,
        extensions=extensions,
        min_size=args.min_size,
        exclude_dirs=exclude_dirs,
        report_file=args.report
    )

    finder.run()


if __name__ == '__main__':
    main()
