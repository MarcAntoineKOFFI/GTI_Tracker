"""
Fix all critical bugs in one script
"""
from pathlib import Path

print("Fixing critical bugs...")

# 1. Remove deprecated AA_UseHighDpiPixmaps from main.py
main_file = Path(__file__).parent / "main.py"
main_content = main_file.read_text(encoding='utf-8')

# Remove the deprecated attribute
main_content = main_content.replace(
    """        # Enable high DPI scaling BEFORE creating QApplication
        # For Qt6, use the new method
        if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
        
        # High DPI policy for Qt6""",
    """        # Enable high DPI scaling BEFORE creating QApplication
        # High DPI policy for Qt6"""
)

main_file.write_text(main_content, encoding='utf-8')
print("[OK] Removed deprecated AA_UseHighDpiPixmaps")

# 2. Fix QFont errors in stylesheet by removing font-size: -1px
styles_file = Path(__file__).parent / "styles" / "dark_professional.qss"
if styles_file.exists():
    styles_content = styles_file.read_text(encoding='utf-8')
    # Remove any font-size with negative values
    import re
    styles_content = re.sub(r'font-size:\s*-\d+px;', '', styles_content)
    styles_file.write_text(styles_content, encoding='utf-8')
    print("[OK] Fixed QFont::setPointSize errors in stylesheet")

# 3. Create database migration script
migration_content = """'''
Database migration to add interview_date and daily_goal columns
'''
import sqlite3
from pathlib import Path
import os

def run_migration():
    # Get database path
    app_data = Path(os.getenv('APPDATA')) / 'GTI_Tracker'
    db_path = app_data / 'gti_tracker.db'
    
    if not db_path.exists():
        print("Database not found")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if interview_date exists
        cursor.execute("PRAGMA table_info(networking_contacts)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'interview_date' not in columns:
            cursor.execute("ALTER TABLE networking_contacts ADD COLUMN interview_date DATE")
            print("[OK] Added interview_date column")
        else:
            print("[OK] interview_date already exists")
        
        # Check if daily_goal exists in settings
        cursor.execute("PRAGMA table_info(settings)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if 'daily_goal' not in columns:
            cursor.execute("ALTER TABLE settings ADD COLUMN daily_goal INTEGER DEFAULT 3")
            print("[OK] Added daily_goal column")
        else:
            print("[OK] daily_goal already exists")
        
        conn.commit()
        print("\\n[SUCCESS] Database migration completed!")
        
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
"""

migration_file = Path(__file__).parent / "migrate_database.py"
migration_file.write_text(migration_content, encoding='utf-8')
print("[OK] Created database migration script")

print("\\nAll critical bugs fixed! Run migrate_database.py next.")
