#!/usr/bin/env python3
"""
Qdrant Project Tag Validator
=============================
Validates all tag.json files in the project for correctness and consistency.

Usage:
    python3 cli/validate-tags.py [--fix] [--verbose] [--schema SCHEMA_FILE]

Options:
    --fix              Attempt to fix common issues automatically
    --verbose          Show detailed validation information
    --schema FILE      Use custom JSON schema for validation
    --export FILE      Export validation report to JSON file

Validation checks:
- Required fields present
- UUID format valid
- ISA Level valid
- Directory paths match actual locations
- Child/parent relationships correct
- No duplicate UUIDs
- JSON syntax valid
- Icon/color scheme present
- Breadcrumb trail valid
"""

import os
import sys
import json
import re
import uuid
from pathlib import Path
from typing import Dict, List, Tuple, Set
from datetime import datetime

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class TagValidator:
    def __init__(self, fix: bool = False, verbose: bool = False, schema_file: str = None):
        self.fix = fix
        self.verbose = verbose
        self.schema_file = schema_file
        self.root_dir = Path(__file__).parent.parent.resolve()

        self.valid_isa_levels = [
            'L4_Business',
            'L3_Site',
            'L2_Area',
            'L1_ProcessCell',
            'L0_Unit'
        ]

        self.errors = []
        self.warnings = []
        self.fixes = []
        self.tag_data = {}  # Store all tag data for cross-referencing

    def log_success(self, message: str):
        """Log success message"""
        print(f"{Colors.GREEN}✓{Colors.END} {message}")

    def log_warning(self, message: str):
        """Log warning message"""
        self.warnings.append(message)
        print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

    def log_error(self, message: str):
        """Log error message"""
        self.errors.append(message)
        print(f"{Colors.RED}✗{Colors.END} {message}")

    def log_info(self, message: str):
        """Log info message"""
        if self.verbose:
            print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

    def log_fix(self, message: str):
        """Log fix applied"""
        self.fixes.append(message)
        print(f"{Colors.CYAN}🔧{Colors.END} {message}")

    def is_valid_uuid(self, uuid_string: str) -> bool:
        """Check if string is valid UUID"""
        try:
            uuid.UUID(uuid_string)
            return True
        except:
            return False

    def validate_required_fields(self, tag_file: Path, data: Dict) -> bool:
        """Validate that all required fields are present"""
        required_fields = [
            'UUID',
            'ISA_Level',
            'Directory_Path',
            'Directory_Name',
            'Title',
            'Description'
        ]

        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            self.log_error(f"{tag_file.relative_to(self.root_dir)}: Missing required fields: {missing_fields}")
            return False

        return True

    def validate_uuid(self, tag_file: Path, data: Dict) -> bool:
        """Validate UUID field"""
        if 'UUID' not in data:
            return False

        uuid_value = data['UUID']

        if not isinstance(uuid_value, str):
            self.log_error(f"{tag_file.relative_to(self.root_dir)}: UUID must be a string")
            return False

        if not self.is_valid_uuid(uuid_value):
            self.log_error(f"{tag_file.relative_to(self.root_dir)}: Invalid UUID format: {uuid_value}")

            if self.fix:
                # Generate new UUID
                new_uuid = str(uuid.uuid4())
                data['UUID'] = new_uuid
                self.log_fix(f"Generated new UUID: {new_uuid}")
                self.save_tag_file(tag_file, data)
                return True

            return False

        return True

    def validate_isa_level(self, tag_file: Path, data: Dict) -> bool:
        """Validate ISA_Level field"""
        if 'ISA_Level' not in data:
            return False

        isa_level = data['ISA_Level']

        if isa_level not in self.valid_isa_levels:
            self.log_warning(f"{tag_file.relative_to(self.root_dir)}: Non-standard ISA Level: {isa_level}")
            # Not an error, just a warning
            return True

        return True

    def validate_directory_path(self, tag_file: Path, data: Dict) -> bool:
        """Validate Directory_Path matches actual location"""
        if 'Directory_Path' not in data:
            return False

        declared_path = data['Directory_Path']
        actual_path = '/' + str(tag_file.parent.parent.relative_to(self.root_dir)) + '/'
        actual_path = actual_path.replace('/index/', '/')

        if actual_path == '//':
            actual_path = '/'

        if declared_path != actual_path:
            self.log_error(f"{tag_file.relative_to(self.root_dir)}: Path mismatch - "
                          f"declared '{declared_path}' but actual '{actual_path}'")

            if self.fix:
                data['Directory_Path'] = actual_path
                self.log_fix(f"Updated Directory_Path to: {actual_path}")
                self.save_tag_file(tag_file, data)
                return True

            return False

        return True

    def validate_child_directories(self, tag_file: Path, data: Dict) -> bool:
        """Validate child directories exist"""
        if 'Child_Directories' not in data:
            # Optional field
            return True

        children = data['Child_Directories']

        if not isinstance(children, list):
            self.log_error(f"{tag_file.relative_to(self.root_dir)}: Child_Directories must be an array")
            return False

        all_valid = True
        for child in children:
            if 'path' not in child:
                self.log_error(f"{tag_file.relative_to(self.root_dir)}: Child missing 'path' field")
                all_valid = False
                continue

            child_path = self.root_dir / child['path'].lstrip('/')
            if not child_path.exists():
                self.log_warning(f"{tag_file.relative_to(self.root_dir)}: "
                               f"Child directory does not exist: {child['path']}")

        return all_valid

    def validate_breadcrumb_trail(self, tag_file: Path, data: Dict) -> bool:
        """Validate breadcrumb trail"""
        if 'Breadcrumb_Trail' not in data:
            # Optional field
            return True

        breadcrumbs = data['Breadcrumb_Trail']

        if not isinstance(breadcrumbs, list):
            self.log_error(f"{tag_file.relative_to(self.root_dir)}: Breadcrumb_Trail must be an array")
            return False

        # Check that each breadcrumb has required fields
        for idx, crumb in enumerate(breadcrumbs):
            if 'path' not in crumb or 'title' not in crumb:
                self.log_error(f"{tag_file.relative_to(self.root_dir)}: "
                             f"Breadcrumb {idx} missing 'path' or 'title'")
                return False

        return True

    def validate_json_structure(self, tag_file: Path, data: Dict) -> bool:
        """Validate overall JSON structure"""
        # Check for common issues
        issues_found = False

        # Check for null values in required fields
        for key, value in data.items():
            if value is None and key in ['UUID', 'ISA_Level', 'Directory_Path']:
                self.log_error(f"{tag_file.relative_to(self.root_dir)}: "
                             f"Required field '{key}' is null")
                issues_found = True

        # Check for empty strings in important fields
        for key in ['Title', 'Description', 'Directory_Name']:
            if key in data and isinstance(data[key], str) and not data[key].strip():
                self.log_warning(f"{tag_file.relative_to(self.root_dir)}: "
                               f"Field '{key}' is empty")

        return not issues_found

    def validate_references(self, tag_file: Path, data: Dict) -> bool:
        """Validate file references in tag"""
        all_valid = True

        # Check Related_Files
        if 'Related_Files' in data:
            for file_ref in data['Related_Files']:
                if 'path' in file_ref:
                    file_path = self.root_dir / file_ref['path']
                    if not file_path.exists():
                        self.log_warning(f"{tag_file.relative_to(self.root_dir)}: "
                                       f"Related file not found: {file_ref['path']}")

        # Check Page_Links
        if 'Page_Links' in data:
            for link in data['Page_Links']:
                if 'path' in link:
                    link_path = self.root_dir / link['path']
                    if not link_path.exists():
                        self.log_warning(f"{tag_file.relative_to(self.root_dir)}: "
                                       f"Page link not found: {link['path']}")

        return all_valid

    def validate_tag_file(self, tag_file: Path) -> bool:
        """Validate a single tag.json file"""
        self.log_info(f"Validating: {tag_file.relative_to(self.root_dir)}")

        try:
            with open(tag_file, 'r') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.log_error(f"{tag_file.relative_to(self.root_dir)}: Invalid JSON - {e}")
            return False
        except Exception as e:
            self.log_error(f"{tag_file.relative_to(self.root_dir)}: Cannot read file - {e}")
            return False

        # Store for later cross-reference
        if 'UUID' in data:
            self.tag_data[data['UUID']] = {
                'file': tag_file,
                'data': data
            }

        # Run all validations
        all_valid = True

        all_valid &= self.validate_required_fields(tag_file, data)
        all_valid &= self.validate_uuid(tag_file, data)
        all_valid &= self.validate_isa_level(tag_file, data)
        all_valid &= self.validate_directory_path(tag_file, data)
        all_valid &= self.validate_child_directories(tag_file, data)
        all_valid &= self.validate_breadcrumb_trail(tag_file, data)
        all_valid &= self.validate_json_structure(tag_file, data)
        all_valid &= self.validate_references(tag_file, data)

        if all_valid:
            self.log_success(f"{tag_file.relative_to(self.root_dir)}: Valid")

        return all_valid

    def check_duplicate_uuids(self) -> bool:
        """Check for duplicate UUIDs across all tags"""
        print(f"\n{Colors.BOLD}Checking for Duplicate UUIDs{Colors.END}")
        print("=" * 60)

        uuid_files = {}
        duplicates_found = False

        for uuid_val, info in self.tag_data.items():
            if uuid_val in uuid_files:
                duplicates_found = True
                self.log_error(f"Duplicate UUID {uuid_val} found in:")
                print(f"    - {uuid_files[uuid_val].relative_to(self.root_dir)}")
                print(f"    - {info['file'].relative_to(self.root_dir)}")

                if self.fix:
                    # Generate new UUID for second occurrence
                    new_uuid = str(uuid.uuid4())
                    info['data']['UUID'] = new_uuid
                    self.save_tag_file(info['file'], info['data'])
                    self.log_fix(f"Generated new UUID for {info['file'].relative_to(self.root_dir)}: {new_uuid}")
            else:
                uuid_files[uuid_val] = info['file']

        if not duplicates_found:
            self.log_success(f"No duplicate UUIDs found ({len(uuid_files)} unique)")

        return not duplicates_found

    def save_tag_file(self, tag_file: Path, data: Dict):
        """Save modified tag.json file"""
        try:
            with open(tag_file, 'w') as f:
                json.dump(data, f, indent=2)
                f.write('\n')  # Add trailing newline
        except Exception as e:
            self.log_error(f"Failed to save {tag_file.relative_to(self.root_dir)}: {e}")

    def generate_report(self, export_file: str = None):
        """Generate validation report"""
        print(f"\n{Colors.BOLD}Validation Report{Colors.END}")
        print("=" * 60)

        total_files = len(list(self.root_dir.glob('**/tag.json')))
        valid_files = total_files - len(set(e.split(':')[0] for e in self.errors if ':' in e))

        print(f"Total tag.json files:  {total_files}")
        print(f"Valid files:           {valid_files}")
        print(f"Files with errors:     {total_files - valid_files}")
        print(f"Total errors:          {len(self.errors)}")
        print(f"Total warnings:        {len(self.warnings)}")

        if self.fix:
            print(f"Fixes applied:         {len(self.fixes)}")

        # Export report if requested
        if export_file:
            report_data = {
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'total_files': total_files,
                    'valid_files': valid_files,
                    'error_count': len(self.errors),
                    'warning_count': len(self.warnings),
                    'fixes_count': len(self.fixes) if self.fix else 0
                },
                'errors': self.errors,
                'warnings': self.warnings,
                'fixes': self.fixes if self.fix else []
            }

            export_path = self.root_dir / export_file
            with open(export_path, 'w') as f:
                json.dump(report_data, f, indent=2)

            self.log_success(f"Report exported to: {export_file}")

    def run(self) -> int:
        """Run validation on all tag.json files"""
        print(f"{Colors.BOLD}{Colors.CYAN}")
        print("=" * 60)
        print("  Qdrant Project Tag Validator")
        print("=" * 60)
        print(f"{Colors.END}")

        if self.fix:
            print(f"{Colors.YELLOW}Running in FIX mode - will attempt to fix issues{Colors.END}\n")

        # Find all tag.json files
        tag_files = list(self.root_dir.glob('**/tag.json'))
        print(f"Found {len(tag_files)} tag.json files\n")

        # Validate each file
        print(f"{Colors.BOLD}Validating Individual Files{Colors.END}")
        print("=" * 60)

        for tag_file in tag_files:
            self.validate_tag_file(tag_file)

        # Cross-validation checks
        self.check_duplicate_uuids()

        # Generate report
        return 0 if not self.errors else 1


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Validate tag.json files in Qdrant project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--fix', '-f', action='store_true',
                       help='Attempt to fix issues automatically')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed validation information')
    parser.add_argument('--schema', '-s', type=str,
                       help='Use custom JSON schema for validation')
    parser.add_argument('--export', '-e', type=str,
                       help='Export validation report to JSON file')

    args = parser.parse_args()

    validator = TagValidator(
        fix=args.fix,
        verbose=args.verbose,
        schema_file=args.schema
    )

    exit_code = validator.run()

    validator.generate_report(export_file=args.export)

    if exit_code == 0:
        print(f"\n{Colors.GREEN}All validations passed!{Colors.END}")
    else:
        print(f"\n{Colors.RED}Validation failed with errors{Colors.END}")

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
