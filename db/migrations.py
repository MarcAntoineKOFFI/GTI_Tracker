"""
Database migration utility
Safely migrate existing databases to new schema
"""
import logging
from pathlib import Path
from sqlalchemy import text, inspect
from db.session import get_engine, get_database_path

logger = logging.getLogger('GTI_Tracker.Migration')


class DatabaseMigrator:
    """Handle database schema migrations"""

    def __init__(self):
        self.engine = get_engine()

    def column_exists(self, table_name: str, column_name: str) -> bool:
        """Check if a column exists in a table"""
        inspector = inspect(self.engine)
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        return column_name in columns

    def add_column_if_not_exists(self, table_name: str, column_name: str,
                                 column_type: str, default_value: str = None):
        """Add a column to a table if it doesn't exist"""
        if self.column_exists(table_name, column_name):
            logger.info(f"Column {table_name}.{column_name} already exists")
            return

        try:
            with self.engine.connect() as conn:
                if default_value:
                    sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type} DEFAULT {default_value}"
                else:
                    sql = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"

                conn.execute(text(sql))
                conn.commit()
                logger.info(f"Added column {table_name}.{column_name}")
        except Exception as e:
            logger.error(f"Failed to add column {table_name}.{column_name}: {e}")
            raise

    def migrate_to_v2(self):
        """Migrate database to version 2 schema"""
        logger.info("Starting migration to v2 schema...")

        # Add new columns to networking_contacts
        self.add_column_if_not_exists('networking_contacts', 'email', 'VARCHAR(255)')
        self.add_column_if_not_exists('networking_contacts', 'linkedin_url', 'VARCHAR(500)')
        self.add_column_if_not_exists('networking_contacts', 'phone', 'VARCHAR(20)')
        self.add_column_if_not_exists('networking_contacts', 'is_deleted', 'BOOLEAN', '0')
        self.add_column_if_not_exists('networking_contacts', 'deleted_at', 'DATETIME')

        # Handle updated_at / last_updated transition for networking_contacts
        if self.column_exists('networking_contacts', 'last_updated'):
            if not self.column_exists('networking_contacts', 'updated_at'):
                # Copy data from last_updated to updated_at
                try:
                    with self.engine.connect() as conn:
                        conn.execute(text(
                            "ALTER TABLE networking_contacts ADD COLUMN updated_at DATETIME"
                        ))
                        conn.execute(text(
                            "UPDATE networking_contacts SET updated_at = last_updated"
                        ))
                        conn.commit()
                        logger.info("Migrated last_updated to updated_at for networking_contacts")
                except Exception as e:
                    logger.error(f"Failed to migrate updated_at: {e}")
        else:
            self.add_column_if_not_exists('networking_contacts', 'updated_at', 'DATETIME', 'CURRENT_TIMESTAMP')

        # Add new columns to internship_applications
        self.add_column_if_not_exists('internship_applications', 'deadline', 'DATE')
        self.add_column_if_not_exists('internship_applications', 'salary_min', 'INTEGER')
        self.add_column_if_not_exists('internship_applications', 'salary_max', 'INTEGER')
        self.add_column_if_not_exists('internship_applications', 'location', 'VARCHAR(200)')
        self.add_column_if_not_exists('internship_applications', 'is_remote', 'BOOLEAN', '0')
        self.add_column_if_not_exists('internship_applications', 'is_deleted', 'BOOLEAN', '0')
        self.add_column_if_not_exists('internship_applications', 'deleted_at', 'DATETIME')
        self.add_column_if_not_exists('internship_applications', 'created_at', 'DATETIME', 'CURRENT_TIMESTAMP')

        # Handle updated_at / last_updated transition for internship_applications
        if self.column_exists('internship_applications', 'last_updated'):
            if not self.column_exists('internship_applications', 'updated_at'):
                try:
                    with self.engine.connect() as conn:
                        conn.execute(text(
                            "ALTER TABLE internship_applications ADD COLUMN updated_at DATETIME"
                        ))
                        conn.execute(text(
                            "UPDATE internship_applications SET updated_at = last_updated"
                        ))
                        conn.commit()
                        logger.info("Migrated last_updated to updated_at for internship_applications")
                except Exception as e:
                    logger.error(f"Failed to migrate updated_at: {e}")
        else:
            self.add_column_if_not_exists('internship_applications', 'updated_at', 'DATETIME', 'CURRENT_TIMESTAMP')

        logger.info("Migration to v2 completed successfully")

    def check_and_migrate(self):
        """Check schema version and migrate if needed"""
        try:
            # Check if new columns exist
            needs_migration = (
                not self.column_exists('networking_contacts', 'email') or
                not self.column_exists('internship_applications', 'deadline')
            )

            if needs_migration:
                logger.info("Database schema outdated, migrating...")
                self.migrate_to_v2()
            else:
                logger.info("Database schema is up to date")

        except Exception as e:
            logger.error(f"Migration check failed: {e}")
            raise


def run_migrations():
    """Run all pending migrations"""
    try:
        migrator = DatabaseMigrator()
        migrator.check_and_migrate()
        return True
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        return False

