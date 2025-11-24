"""
Enterprise-grade automatic backup system
Multi-location backups with scheduled rotation
"""
import shutil
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import gzip
import logging


class BackupManager:
    """Automatic backup system with rotation and multiple locations"""

    def __init__(self, database_path: Path, backup_dir: Path = None):
        """
        Initialize backup manager

        Args:
            database_path: Path to the SQLite database
            backup_dir: Directory for backups (default: ~/.gti_tracker/backups)
        """
        self.database_path = Path(database_path)

        if backup_dir is None:
            backup_dir = Path.home() / '.gti_tracker' / 'backups'

        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for different backup types
        self.daily_dir = self.backup_dir / 'daily'
        self.weekly_dir = self.backup_dir / 'weekly'
        self.monthly_dir = self.backup_dir / 'monthly'

        for dir in [self.daily_dir, self.weekly_dir, self.monthly_dir]:
            dir.mkdir(exist_ok=True)

        self.logger = logging.getLogger('GTI_Tracker.Backup')

        # Backup metadata file
        self.metadata_file = self.backup_dir / 'backup_metadata.json'

    def create_backup(self, backup_type: str = 'manual', compress: bool = True) -> Optional[Path]:
        """
        Create a backup of the database

        Args:
            backup_type: Type of backup (manual, daily, weekly, monthly)
            compress: Whether to compress the backup

        Returns:
            Path to the created backup file, or None if failed
        """
        try:
            if not self.database_path.exists():
                self.logger.error(f"Database file not found: {self.database_path}")
                return None

            # Determine backup location based on type
            if backup_type == 'daily':
                backup_dir = self.daily_dir
            elif backup_type == 'weekly':
                backup_dir = self.weekly_dir
            elif backup_type == 'monthly':
                backup_dir = self.monthly_dir
            else:
                backup_dir = self.backup_dir

            # Create backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"gti_tracker_{backup_type}_{timestamp}.db"

            if compress:
                backup_name += '.gz'

            backup_path = backup_dir / backup_name

            # Perform backup
            if compress:
                with open(self.database_path, 'rb') as f_in:
                    with gzip.open(backup_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(self.database_path, backup_path)

            # Update metadata
            self._update_metadata(backup_path, backup_type)

            self.logger.info(f"Backup created successfully: {backup_path}")
            return backup_path

        except Exception as e:
            self.logger.error(f"Backup failed: {e}")
            return None

    def _update_metadata(self, backup_path: Path, backup_type: str):
        """Update backup metadata file"""
        try:
            # Read existing metadata
            if self.metadata_file.exists():
                with open(self.metadata_file, 'r') as f:
                    metadata = json.load(f)
            else:
                metadata = {'backups': []}

            # Add new backup info
            backup_info = {
                'path': str(backup_path),
                'type': backup_type,
                'timestamp': datetime.now().isoformat(),
                'size_bytes': backup_path.stat().st_size
            }

            metadata['backups'].append(backup_info)
            metadata['last_backup'] = datetime.now().isoformat()

            # Write updated metadata
            with open(self.metadata_file, 'w') as f:
                json.dump(metadata, f, indent=2)

        except Exception as e:
            self.logger.error(f"Failed to update metadata: {e}")

    def restore_backup(self, backup_path: Path) -> bool:
        """
        Restore database from a backup

        Args:
            backup_path: Path to the backup file

        Returns:
            True if restore successful, False otherwise
        """
        try:
            if not backup_path.exists():
                self.logger.error(f"Backup file not found: {backup_path}")
                return False

            # Create a backup of current database before restoring
            current_backup = self.backup_dir / f"pre_restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            if self.database_path.exists():
                shutil.copy2(self.database_path, current_backup)
                self.logger.info(f"Created safety backup before restore: {current_backup}")

            # Restore from backup
            if backup_path.suffix == '.gz':
                # Decompress first
                with gzip.open(backup_path, 'rb') as f_in:
                    with open(self.database_path, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
            else:
                shutil.copy2(backup_path, self.database_path)

            self.logger.info(f"Database restored from: {backup_path}")
            return True

        except Exception as e:
            self.logger.error(f"Restore failed: {e}")
            return False

    def rotate_backups(self):
        """
        Rotate backups to manage disk space
        - Keep last 7 daily backups
        - Keep last 4 weekly backups
        - Keep last 12 monthly backups
        """
        try:
            self._rotate_directory(self.daily_dir, keep_count=7)
            self._rotate_directory(self.weekly_dir, keep_count=4)
            self._rotate_directory(self.monthly_dir, keep_count=12)

            self.logger.info("Backup rotation completed")

        except Exception as e:
            self.logger.error(f"Backup rotation failed: {e}")

    def _rotate_directory(self, directory: Path, keep_count: int):
        """Rotate backups in a directory, keeping only the most recent"""
        try:
            # Get all backup files sorted by modification time
            backups = sorted(
                directory.glob('*.db*'),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            # Delete old backups beyond keep_count
            for backup in backups[keep_count:]:
                backup.unlink()
                self.logger.info(f"Deleted old backup: {backup}")

        except Exception as e:
            self.logger.error(f"Failed to rotate backups in {directory}: {e}")

    def should_create_backup(self, backup_type: str) -> bool:
        """
        Check if a backup should be created based on schedule

        Args:
            backup_type: Type of backup to check (daily, weekly, monthly)

        Returns:
            True if backup should be created
        """
        try:
            if not self.metadata_file.exists():
                return True

            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)

            # Find last backup of this type
            backups = [b for b in metadata.get('backups', []) if b['type'] == backup_type]

            if not backups:
                return True

            last_backup = max(backups, key=lambda b: b['timestamp'])
            last_backup_time = datetime.fromisoformat(last_backup['timestamp'])

            # Check if enough time has passed
            now = datetime.now()

            if backup_type == 'daily':
                return (now - last_backup_time) >= timedelta(days=1)
            elif backup_type == 'weekly':
                return (now - last_backup_time) >= timedelta(weeks=1)
            elif backup_type == 'monthly':
                return (now - last_backup_time) >= timedelta(days=30)

            return False

        except Exception as e:
            self.logger.error(f"Failed to check backup schedule: {e}")
            return True  # If unsure, create backup

    def perform_scheduled_backups(self):
        """
        Perform all scheduled backups that are due
        """
        # Daily backup
        if self.should_create_backup('daily'):
            self.create_backup('daily')

        # Weekly backup
        if self.should_create_backup('weekly'):
            self.create_backup('weekly')

        # Monthly backup
        if self.should_create_backup('monthly'):
            self.create_backup('monthly')

        # Rotate old backups
        self.rotate_backups()

    def get_backup_info(self) -> dict:
        """
        Get information about available backups

        Returns:
            Dictionary with backup statistics
        """
        try:
            if not self.metadata_file.exists():
                return {
                    'total_backups': 0,
                    'last_backup': None,
                    'total_size_mb': 0
                }

            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)

            backups = metadata.get('backups', [])
            total_size = sum(b.get('size_bytes', 0) for b in backups)

            return {
                'total_backups': len(backups),
                'last_backup': metadata.get('last_backup'),
                'total_size_mb': total_size / (1024 * 1024),
                'daily_backups': len([b for b in backups if b['type'] == 'daily']),
                'weekly_backups': len([b for b in backups if b['type'] == 'weekly']),
                'monthly_backups': len([b for b in backups if b['type'] == 'monthly'])
            }

        except Exception as e:
            self.logger.error(f"Failed to get backup info: {e}")
            return {
                'total_backups': 0,
                'last_backup': None,
                'total_size_mb': 0
            }

    def list_backups(self, backup_type: Optional[str] = None) -> list:
        """
        List available backups

        Args:
            backup_type: Filter by backup type (optional)

        Returns:
            List of backup information dictionaries
        """
        try:
            if not self.metadata_file.exists():
                return []

            with open(self.metadata_file, 'r') as f:
                metadata = json.load(f)

            backups = metadata.get('backups', [])

            if backup_type:
                backups = [b for b in backups if b['type'] == backup_type]

            # Sort by timestamp, newest first
            backups.sort(key=lambda b: b['timestamp'], reverse=True)

            return backups

        except Exception as e:
            self.logger.error(f"Failed to list backups: {e}")
            return []

