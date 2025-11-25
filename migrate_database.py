'''
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
        print("\n[SUCCESS] Database migration completed!")
        
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    run_migration()
