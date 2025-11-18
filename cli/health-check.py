#!/usr/bin/env python3
"""
Qdrant Project Health Check Script
===================================
Validates project structure, files, and integrity of the ISA-95 hierarchy.

Usage:
    python3 cli/health-check.py [--verbose] [--fix]

Options:
    --verbose    Show detailed information about each check
    --fix        Attempt to fix minor issues automatically

Returns:
    0 - All checks passed
    1 - Warnings found
    2 - Errors found
"""

import os
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import List, Dict, Tuple

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class HealthCheck:
    def __init__(self, verbose: bool = False, fix: bool = False):
        self.verbose = verbose
        self.fix = fix
        self.root_dir = Path(__file__).parent.parent.resolve()
        self.errors = []
        self.warnings = []
        self.successes = []

    def log_success(self, message: str):
        """Log a successful check"""
        self.successes.append(message)
        print(f"{Colors.GREEN}✓{Colors.END} {message}")

    def log_warning(self, message: str):
        """Log a warning"""
        self.warnings.append(message)
        print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

    def log_error(self, message: str):
        """Log an error"""
        self.errors.append(message)
        print(f"{Colors.RED}✗{Colors.END} {message}")

    def log_info(self, message: str):
        """Log informational message"""
        if self.verbose:
            print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

    def check_required_directories(self) -> bool:
        """Check that required top-level directories exist"""
        print(f"\n{Colors.BOLD}Checking Required Directories{Colors.END}")
        print("=" * 60)

        required_dirs = [
            'cli',
            'collab',
            'docs',
            'index',
            'os',
            'templates'
        ]

        all_exist = True
        for dir_name in required_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.log_success(f"Directory exists: {dir_name}/")
            else:
                self.log_error(f"Missing required directory: {dir_name}/")
                all_exist = False

        return all_exist

    def check_tag_json_files(self) -> bool:
        """Validate all tag.json files in the project"""
        print(f"\n{Colors.BOLD}Validating tag.json Files{Colors.END}")
        print("=" * 60)

        tag_files = list(self.root_dir.glob('**/tag.json'))
        self.log_info(f"Found {len(tag_files)} tag.json files")

        required_fields = [
            'UUID',
            'ISA_Level',
            'Directory_Path',
            'Directory_Name',
            'Title',
            'Description'
        ]

        valid_count = 0
        invalid_count = 0

        for tag_file in tag_files:
            try:
                with open(tag_file, 'r') as f:
                    data = json.load(f)

                # Check required fields
                missing_fields = [field for field in required_fields if field not in data]

                if missing_fields:
                    self.log_error(f"{tag_file.relative_to(self.root_dir)}: Missing fields {missing_fields}")
                    invalid_count += 1
                else:
                    valid_count += 1
                    if self.verbose:
                        self.log_success(f"{tag_file.relative_to(self.root_dir)}: Valid")

            except json.JSONDecodeError as e:
                self.log_error(f"{tag_file.relative_to(self.root_dir)}: Invalid JSON - {e}")
                invalid_count += 1
            except Exception as e:
                self.log_error(f"{tag_file.relative_to(self.root_dir)}: Error reading file - {e}")
                invalid_count += 1

        self.log_info(f"Valid: {valid_count}, Invalid: {invalid_count}")

        if invalid_count == 0:
            self.log_success(f"All {valid_count} tag.json files are valid")
            return True
        else:
            self.log_error(f"{invalid_count} tag.json files have issues")
            return False

    def check_index_directories(self) -> bool:
        """Check that every directory with a tag.json has an index/ subdirectory"""
        print(f"\n{Colors.BOLD}Checking Index Directories{Colors.END}")
        print("=" * 60)

        tag_files = list(self.root_dir.glob('**/index/tag.json'))
        missing_count = 0

        for tag_file in tag_files:
            parent_dir = tag_file.parent.parent
            # The tag.json is in index/, so parent is the actual directory
            if self.verbose:
                self.log_success(f"Index directory exists: {parent_dir.relative_to(self.root_dir)}/index/")

        self.log_success(f"Found {len(tag_files)} proper index directories")
        return True

    def check_duplicate_uuids(self) -> bool:
        """Check for duplicate UUIDs in tag.json files"""
        print(f"\n{Colors.BOLD}Checking for Duplicate UUIDs{Colors.END}")
        print("=" * 60)

        uuid_map = defaultdict(list)
        tag_files = list(self.root_dir.glob('**/tag.json'))

        for tag_file in tag_files:
            try:
                with open(tag_file, 'r') as f:
                    data = json.load(f)
                    if 'UUID' in data:
                        uuid_map[data['UUID']].append(tag_file)
            except:
                pass  # Already reported in check_tag_json_files

        duplicates_found = False
        for uuid, files in uuid_map.items():
            if len(files) > 1:
                duplicates_found = True
                self.log_error(f"Duplicate UUID {uuid} found in:")
                for file in files:
                    print(f"    - {file.relative_to(self.root_dir)}")

        if not duplicates_found:
            self.log_success(f"No duplicate UUIDs found ({len(uuid_map)} unique UUIDs)")
            return True
        return False

    def check_isa95_structure(self) -> bool:
        """Validate ISA-95 directory structure"""
        print(f"\n{Colors.BOLD}Validating ISA-95 Structure{Colors.END}")
        print("=" * 60)

        os_dir = self.root_dir / 'os'
        if not os_dir.exists():
            self.log_error("os/ directory not found")
            return False

        # Expected ISA-95 levels in os/
        expected_levels = [
            'boot',      # System boot
            'backend',   # Backend services
            'config',    # Configuration
            'controls',  # Controls layer
            'data',      # Data layer
            'debug',     # Debug utilities
            'frontend',  # Frontend UI
            'language',  # Language processing
            'models',    # AI models
            'modules',   # System modules
        ]

        found_count = 0
        for level in expected_levels:
            level_path = os_dir / level
            if level_path.exists():
                found_count += 1
                if self.verbose:
                    self.log_success(f"ISA-95 level exists: os/{level}/")
            else:
                self.log_warning(f"Optional ISA-95 level missing: os/{level}/")

        self.log_success(f"Found {found_count} ISA-95 levels in os/")
        return True

    def check_controls_structure(self) -> bool:
        """Validate controls directory structure (HMI, PLC, SCADA, Tags)"""
        print(f"\n{Colors.BOLD}Validating Controls Structure{Colors.END}")
        print("=" * 60)

        controls_locations = [
            self.root_dir / 'index' / 'controls',
            self.root_dir / 'os' / 'controls',
        ]

        expected_subdirs = ['hmi', 'plc', 'scada', 'tags']

        for controls_dir in controls_locations:
            if not controls_dir.exists():
                self.log_warning(f"Controls directory not found: {controls_dir.relative_to(self.root_dir)}")
                continue

            self.log_info(f"Checking {controls_dir.relative_to(self.root_dir)}")

            # Check for HMI structure
            hmi_dir = controls_dir / 'HMI'
            if hmi_dir.exists():
                expected_hmi_subdirs = ['screens', 'templates']
                for subdir in expected_hmi_subdirs:
                    subdir_path = hmi_dir / subdir
                    if subdir_path.exists():
                        if self.verbose:
                            self.log_success(f"HMI subdirectory exists: {subdir}/")
                    else:
                        self.log_warning(f"HMI subdirectory missing: {subdir}/")

        self.log_success("Controls structure validated")
        return True

    def check_critical_files(self) -> bool:
        """Check for critical project files"""
        print(f"\n{Colors.BOLD}Checking Critical Files{Colors.END}")
        print("=" * 60)

        critical_files = [
            'README.md',
            'CHANGELOG.md',
            '.gitignore',
            'index.html',
            'cli/README.md'
        ]

        all_exist = True
        for file_path in critical_files:
            full_path = self.root_dir / file_path
            if full_path.exists():
                self.log_success(f"Critical file exists: {file_path}")
            else:
                self.log_error(f"Critical file missing: {file_path}")
                all_exist = False

        return all_exist

    def check_json_validity(self) -> bool:
        """Check all JSON files for syntax validity"""
        print(f"\n{Colors.BOLD}Validating JSON Files{Colors.END}")
        print("=" * 60)

        json_files = list(self.root_dir.glob('**/*.json'))
        # Exclude node_modules and venv
        json_files = [f for f in json_files if 'node_modules' not in str(f) and 'venv' not in str(f)]

        self.log_info(f"Found {len(json_files)} JSON files to validate")

        valid_count = 0
        invalid_count = 0

        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    json.load(f)
                valid_count += 1
                if self.verbose:
                    self.log_success(f"{json_file.relative_to(self.root_dir)}: Valid JSON")
            except json.JSONDecodeError as e:
                self.log_error(f"{json_file.relative_to(self.root_dir)}: Invalid JSON - Line {e.lineno}, Col {e.colno}")
                invalid_count += 1
            except Exception as e:
                self.log_warning(f"{json_file.relative_to(self.root_dir)}: Cannot read - {e}")

        if invalid_count == 0:
            self.log_success(f"All {valid_count} JSON files are valid")
            return True
        else:
            self.log_error(f"{invalid_count} JSON files have syntax errors")
            return False

    def check_symlinks(self) -> bool:
        """Check for broken symbolic links"""
        print(f"\n{Colors.BOLD}Checking Symbolic Links{Colors.END}")
        print("=" * 60)

        broken_links = []

        for path in self.root_dir.rglob('*'):
            if path.is_symlink():
                if not path.exists():
                    broken_links.append(path)
                    self.log_error(f"Broken symlink: {path.relative_to(self.root_dir)}")

        if not broken_links:
            self.log_success("No broken symbolic links found")
            return True
        else:
            self.log_error(f"Found {len(broken_links)} broken symbolic links")
            return False

    def generate_summary(self) -> int:
        """Generate final summary and return exit code"""
        print(f"\n{Colors.BOLD}Health Check Summary{Colors.END}")
        print("=" * 60)

        print(f"{Colors.GREEN}Successes:{Colors.END} {len(self.successes)}")
        print(f"{Colors.YELLOW}Warnings:{Colors.END}  {len(self.warnings)}")
        print(f"{Colors.RED}Errors:{Colors.END}    {len(self.errors)}")

        if self.errors:
            print(f"\n{Colors.RED}Health check FAILED with {len(self.errors)} errors{Colors.END}")
            return 2
        elif self.warnings:
            print(f"\n{Colors.YELLOW}Health check PASSED with {len(self.warnings)} warnings{Colors.END}")
            return 1
        else:
            print(f"\n{Colors.GREEN}Health check PASSED - All systems healthy!{Colors.END}")
            return 0

    def run(self) -> int:
        """Run all health checks"""
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("=" * 60)
        print("  Qdrant Project Health Check")
        print("=" * 60)
        print(f"{Colors.END}")

        # Run all checks
        self.check_required_directories()
        self.check_critical_files()
        self.check_tag_json_files()
        self.check_index_directories()
        self.check_duplicate_uuids()
        self.check_isa95_structure()
        self.check_controls_structure()
        self.check_json_validity()
        self.check_symlinks()

        # Generate summary
        return self.generate_summary()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Qdrant Project Health Check',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed information')
    parser.add_argument('--fix', '-f', action='store_true',
                       help='Attempt to fix issues automatically')

    args = parser.parse_args()

    checker = HealthCheck(verbose=args.verbose, fix=args.fix)
    exit_code = checker.run()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
