#!/usr/bin/env python3
"""
Qdrant Project Backup & Restore Utility
========================================
Creates backups and restores the project with versioning support.

Usage:
    python3 cli/backup-restore.py backup [--name NAME] [--compress]
    python3 cli/backup-restore.py restore BACKUP_ID [--force]
    python3 cli/backup-restore.py list
    python3 cli/backup-restore.py info BACKUP_ID
    python3 cli/backup-restore.py delete BACKUP_ID
    python3 cli/backup-restore.py clean [--keep N]

Commands:
    backup              Create a new backup
    restore             Restore from a backup
    list                List all available backups
    info                Show detailed info about a backup
    delete              Delete a specific backup
    clean               Clean old backups, keeping N most recent

Options:
    --name NAME         Custom name for backup (default: timestamp)
    --compress          Compress backup with gzip
    --force             Force restore without confirmation
    --keep N            Number of backups to keep when cleaning (default: 5)
    --incremental       Create incremental backup (only changed files)
    --exclude PATTERNS  Comma-separated patterns to exclude
"""

import os
import sys
import json
import shutil
import tarfile
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

class BackupRestore:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent.resolve()
        self.backup_dir = self.root_dir / 'cli' / 'backup' / 'archives'
        self.metadata_file = self.backup_dir / 'metadata.json'

        # Default exclusions
        self.default_excludes = [
            '.git',
            'node_modules',
            'venv',
            '__pycache__',
            '.pytest_cache',
            '*.pyc',
            '*.pyo',
            '*.log',
            'cli/backup/archives',
            'cli/logs'
        ]

        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Load metadata
        self.metadata = self.load_metadata()

    def log_success(self, message: str):
        """Log success message"""
        print(f"{Colors.GREEN}✓{Colors.END} {message}")

    def log_error(self, message: str):
        """Log error message"""
        print(f"{Colors.RED}✗{Colors.END} {message}")

    def log_warning(self, message: str):
        """Log warning message"""
        print(f"{Colors.YELLOW}⚠{Colors.END} {message}")

    def log_info(self, message: str):
        """Log info message"""
        print(f"{Colors.BLUE}ℹ{Colors.END} {message}")

    def format_size(self, size: int) -> str:
        """Format size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}TB"

    def load_metadata(self) -> Dict:
        """Load backup metadata"""
        if self.metadata_file.exists():
            try:
                with open(self.metadata_file, 'r') as f:
                    return json.load(f)
            except:
                return {'backups': []}
        return {'backups': []}

    def save_metadata(self):
        """Save backup metadata"""
        try:
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            self.log_error(f"Failed to save metadata: {e}")

    def generate_backup_id(self) -> str:
        """Generate unique backup ID"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"backup_{timestamp}"

    def calculate_checksum(self, file_path: Path) -> str:
        """Calculate MD5 checksum of file"""
        try:
            hasher = hashlib.md5()
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except:
            return None

    def should_exclude(self, path: Path, custom_excludes: List[str] = None) -> bool:
        """Check if path should be excluded from backup"""
        excludes = self.default_excludes + (custom_excludes or [])

        path_str = str(path.relative_to(self.root_dir))

        for pattern in excludes:
            # Simple pattern matching
            if pattern.startswith('*'):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path.parts or pattern in path_str:
                return True

        return False

    def create_backup(self,
                     name: Optional[str] = None,
                     compress: bool = False,
                     incremental: bool = False,
                     custom_excludes: List[str] = None) -> Optional[str]:
        """Create a new backup"""
        print(f"\n{Colors.BOLD}Creating Backup{Colors.END}")
        print("=" * 60)

        backup_id = self.generate_backup_id()
        backup_name = name or backup_id

        # Determine file extension
        ext = '.tar.gz' if compress else '.tar'
        backup_file = self.backup_dir / f"{backup_id}{ext}"

        self.log_info(f"Backup ID: {backup_id}")
        self.log_info(f"Name: {backup_name}")
        self.log_info(f"Destination: {backup_file.name}")

        try:
            # Create tar archive
            mode = 'w:gz' if compress else 'w'

            with tarfile.open(backup_file, mode) as tar:
                file_count = 0
                total_size = 0

                # Walk through project
                for item in self.root_dir.rglob('*'):
                    if item.is_file() and not self.should_exclude(item, custom_excludes):
                        # For incremental backups, check if file changed
                        if incremental:
                            # TODO: Implement incremental logic
                            pass

                        arcname = item.relative_to(self.root_dir)
                        tar.add(item, arcname=arcname)
                        file_count += 1
                        total_size += item.stat().st_size

                        if file_count % 100 == 0:
                            print(f"  Backed up {file_count} files...", end='\r')

            backup_size = backup_file.stat().st_size

            self.log_success(f"Backed up {file_count} files ({self.format_size(total_size)})")
            self.log_success(f"Archive size: {self.format_size(backup_size)}")

            # Calculate compression ratio
            if compress and total_size > 0:
                ratio = (1 - backup_size / total_size) * 100
                self.log_info(f"Compression ratio: {ratio:.1f}%")

            # Store metadata
            backup_meta = {
                'id': backup_id,
                'name': backup_name,
                'timestamp': datetime.now().isoformat(),
                'file': backup_file.name,
                'compressed': compress,
                'incremental': incremental,
                'file_count': file_count,
                'original_size': total_size,
                'backup_size': backup_size,
                'checksum': self.calculate_checksum(backup_file)
            }

            self.metadata['backups'].append(backup_meta)
            self.save_metadata()

            self.log_success(f"Backup created successfully: {backup_id}")
            return backup_id

        except Exception as e:
            self.log_error(f"Backup failed: {e}")
            # Clean up partial backup
            if backup_file.exists():
                backup_file.unlink()
            return None

    def list_backups(self):
        """List all available backups"""
        print(f"\n{Colors.BOLD}Available Backups{Colors.END}")
        print("=" * 80)

        if not self.metadata['backups']:
            self.log_info("No backups found")
            return

        print(f"\n{'ID':<25} {'Name':<20} {'Date':<20} {'Size':<10} {'Files'}")
        print("-" * 80)

        for backup in sorted(self.metadata['backups'],
                           key=lambda x: x['timestamp'],
                           reverse=True):
            backup_id = backup['id']
            name = backup['name']
            timestamp = datetime.fromisoformat(backup['timestamp']).strftime('%Y-%m-%d %H:%M')
            size = self.format_size(backup['backup_size'])
            file_count = backup['file_count']

            print(f"{backup_id:<25} {name:<20} {timestamp:<20} {size:<10} {file_count}")

        print(f"\nTotal backups: {len(self.metadata['backups'])}")

    def get_backup_info(self, backup_id: str) -> Optional[Dict]:
        """Get backup metadata"""
        for backup in self.metadata['backups']:
            if backup['id'] == backup_id:
                return backup
        return None

    def show_backup_info(self, backup_id: str):
        """Show detailed backup information"""
        backup = self.get_backup_info(backup_id)

        if not backup:
            self.log_error(f"Backup not found: {backup_id}")
            return

        print(f"\n{Colors.BOLD}Backup Information{Colors.END}")
        print("=" * 60)

        print(f"ID:              {backup['id']}")
        print(f"Name:            {backup['name']}")
        print(f"Created:         {datetime.fromisoformat(backup['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"File:            {backup['file']}")
        print(f"Compressed:      {'Yes' if backup['compressed'] else 'No'}")
        print(f"Incremental:     {'Yes' if backup['incremental'] else 'No'}")
        print(f"File Count:      {backup['file_count']:,}")
        print(f"Original Size:   {self.format_size(backup['original_size'])}")
        print(f"Backup Size:     {self.format_size(backup['backup_size'])}")

        if backup['compressed']:
            ratio = (1 - backup['backup_size'] / backup['original_size']) * 100
            print(f"Compression:     {ratio:.1f}%")

        print(f"Checksum:        {backup['checksum']}")

        # Check if backup file exists
        backup_file = self.backup_dir / backup['file']
        if backup_file.exists():
            self.log_success("Backup file exists")
        else:
            self.log_error("Backup file is missing!")

    def restore_backup(self, backup_id: str, force: bool = False):
        """Restore from backup"""
        backup = self.get_backup_info(backup_id)

        if not backup:
            self.log_error(f"Backup not found: {backup_id}")
            return False

        backup_file = self.backup_dir / backup['file']

        if not backup_file.exists():
            self.log_error(f"Backup file not found: {backup_file}")
            return False

        print(f"\n{Colors.BOLD}Restoring Backup{Colors.END}")
        print("=" * 60)

        print(f"Backup ID:       {backup['id']}")
        print(f"Name:            {backup['name']}")
        print(f"Created:         {datetime.fromisoformat(backup['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Files:           {backup['file_count']:,}")
        print(f"Size:            {self.format_size(backup['backup_size'])}")

        # Verify checksum
        self.log_info("Verifying backup integrity...")
        current_checksum = self.calculate_checksum(backup_file)
        if current_checksum != backup['checksum']:
            self.log_error("Backup checksum mismatch! File may be corrupted.")
            if not force:
                return False
            self.log_warning("Continuing due to --force flag")

        # Confirmation
        if not force:
            print(f"\n{Colors.YELLOW}WARNING: This will overwrite existing files!{Colors.END}")
            response = input("Continue? (yes/no): ")
            if response.lower() != 'yes':
                self.log_info("Restore cancelled")
                return False

        try:
            # Extract backup
            mode = 'r:gz' if backup['compressed'] else 'r'

            self.log_info("Extracting backup...")

            with tarfile.open(backup_file, mode) as tar:
                # Extract to project root
                tar.extractall(path=self.root_dir)

            self.log_success(f"Restored {backup['file_count']} files")
            self.log_success("Backup restored successfully!")

            return True

        except Exception as e:
            self.log_error(f"Restore failed: {e}")
            return False

    def delete_backup(self, backup_id: str):
        """Delete a backup"""
        backup = self.get_backup_info(backup_id)

        if not backup:
            self.log_error(f"Backup not found: {backup_id}")
            return False

        backup_file = self.backup_dir / backup['file']

        print(f"\n{Colors.BOLD}Deleting Backup{Colors.END}")
        print("=" * 60)
        print(f"ID:   {backup['id']}")
        print(f"Name: {backup['name']}")

        response = input("\nAre you sure? (yes/no): ")
        if response.lower() != 'yes':
            self.log_info("Deletion cancelled")
            return False

        try:
            # Delete file
            if backup_file.exists():
                backup_file.unlink()
                self.log_success(f"Deleted backup file: {backup_file.name}")

            # Remove from metadata
            self.metadata['backups'] = [
                b for b in self.metadata['backups']
                if b['id'] != backup_id
            ]
            self.save_metadata()

            self.log_success("Backup deleted successfully")
            return True

        except Exception as e:
            self.log_error(f"Failed to delete backup: {e}")
            return False

    def clean_old_backups(self, keep: int = 5):
        """Clean old backups, keeping N most recent"""
        print(f"\n{Colors.BOLD}Cleaning Old Backups{Colors.END}")
        print("=" * 60)

        if len(self.metadata['backups']) <= keep:
            self.log_info(f"No cleanup needed (have {len(self.metadata['backups'])}, keeping {keep})")
            return

        # Sort by timestamp
        backups_sorted = sorted(
            self.metadata['backups'],
            key=lambda x: x['timestamp'],
            reverse=True
        )

        to_keep = backups_sorted[:keep]
        to_delete = backups_sorted[keep:]

        print(f"Keeping {len(to_keep)} most recent backups")
        print(f"Deleting {len(to_delete)} old backups:")

        for backup in to_delete:
            print(f"  - {backup['id']} ({backup['name']})")

        response = input("\nContinue? (yes/no): ")
        if response.lower() != 'yes':
            self.log_info("Cleanup cancelled")
            return

        deleted_count = 0
        freed_space = 0

        for backup in to_delete:
            backup_file = self.backup_dir / backup['file']
            try:
                if backup_file.exists():
                    size = backup_file.stat().st_size
                    backup_file.unlink()
                    freed_space += size
                    deleted_count += 1
            except Exception as e:
                self.log_warning(f"Could not delete {backup_file.name}: {e}")

        # Update metadata
        self.metadata['backups'] = to_keep
        self.save_metadata()

        self.log_success(f"Deleted {deleted_count} backups")
        self.log_success(f"Freed {self.format_size(freed_space)} of space")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Backup and restore Qdrant project',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Backup command
    backup_parser = subparsers.add_parser('backup', help='Create a new backup')
    backup_parser.add_argument('--name', '-n', type=str, help='Custom backup name')
    backup_parser.add_argument('--compress', '-c', action='store_true', help='Compress backup')
    backup_parser.add_argument('--incremental', '-i', action='store_true', help='Incremental backup')
    backup_parser.add_argument('--exclude', '-x', type=str, help='Additional exclude patterns')

    # Restore command
    restore_parser = subparsers.add_parser('restore', help='Restore from backup')
    restore_parser.add_argument('backup_id', type=str, help='Backup ID to restore')
    restore_parser.add_argument('--force', '-f', action='store_true', help='Force restore')

    # List command
    subparsers.add_parser('list', help='List all backups')

    # Info command
    info_parser = subparsers.add_parser('info', help='Show backup info')
    info_parser.add_argument('backup_id', type=str, help='Backup ID')

    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a backup')
    delete_parser.add_argument('backup_id', type=str, help='Backup ID to delete')

    # Clean command
    clean_parser = subparsers.add_parser('clean', help='Clean old backups')
    clean_parser.add_argument('--keep', '-k', type=int, default=5, help='Number of backups to keep')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    br = BackupRestore()

    if args.command == 'backup':
        custom_excludes = args.exclude.split(',') if args.exclude else None
        br.create_backup(
            name=args.name,
            compress=args.compress,
            incremental=args.incremental,
            custom_excludes=custom_excludes
        )

    elif args.command == 'restore':
        br.restore_backup(args.backup_id, force=args.force)

    elif args.command == 'list':
        br.list_backups()

    elif args.command == 'info':
        br.show_backup_info(args.backup_id)

    elif args.command == 'delete':
        br.delete_backup(args.backup_id)

    elif args.command == 'clean':
        br.clean_old_backups(keep=args.keep)


if __name__ == '__main__':
    main()
