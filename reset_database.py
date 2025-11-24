"""
Clean database reset for fresh schema
Run this to fix schema issues
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

def reset_database():
    """Delete old database and create fresh one"""
    from db.session import get_database_path, init_database

    db_path = get_database_path()

    print(f"Database path: {db_path}")

    if db_path.exists():
        print("Deleting old database...")
        db_path.unlink()
        print("Old database deleted")

    print("Initializing fresh database...")
    init_database()
    print("✓ Fresh database created successfully!")
    print("\nYou can now run the application or tests.")

if __name__ == "__main__":
    reset_database()

