"""
Test script to verify GTI Tracker components work correctly
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")

    try:
        from db import models, session
        print("✓ Database modules imported successfully")
    except Exception as e:
        print(f"✗ Failed to import database modules: {e}")
        return False

    try:
        from utils import message_generator, date_helpers, validators, charts
        print("✓ Utility modules imported successfully")
    except Exception as e:
        print(f"✗ Failed to import utility modules: {e}")
        return False

    try:
        from ui import (
            main_window, networking_dashboard, networking_list,
            networking_dialogs, networking_stats,
            internship_dashboard, internship_list,
            internship_dialogs, internship_stats,
            settings_dialog
        )
        print("✓ UI modules imported successfully")
    except Exception as e:
        print(f"✗ Failed to import UI modules: {e}")
        return False

    return True


def test_database():
    """Test database initialization"""
    print("\nTesting database...")

    try:
        from db.session import init_database, get_session, get_database_path
        from db.models import NetworkingContact, InternshipApplication, Settings

        # Initialize database
        init_database()
        print(f"✓ Database initialized at: {get_database_path()}")

        # Test session
        session = get_session()

        # Check settings
        settings = session.query(Settings).filter_by(id=1).first()
        if settings:
            print(f"✓ Settings found: follow_up_days={settings.follow_up_days}")
        else:
            print("✗ Settings not found")
            return False

        # Count existing data
        contact_count = session.query(NetworkingContact).count()
        internship_count = session.query(InternshipApplication).count()

        print(f"✓ Database working - Contacts: {contact_count}, Internships: {internship_count}")

        session.close()
        return True

    except Exception as e:
        print(f"✗ Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_utilities():
    """Test utility functions"""
    print("\nTesting utilities...")

    try:
        from utils.date_helpers import format_date, days_since, get_last_n_days
        from utils.validators import is_valid_url, validate_required_field
        from datetime import date

        # Test date helpers
        today = date.today()
        formatted = format_date(today)
        days = get_last_n_days(7)
        print(f"✓ Date helpers working - Today: {formatted}, Last 7 days count: {len(days)}")

        # Test validators
        assert is_valid_url("https://example.com") == True
        assert is_valid_url("not a url") == False
        valid, msg = validate_required_field("test", "field")
        assert valid == True
        print("✓ Validators working correctly")

        return True

    except Exception as e:
        print(f"✗ Utilities test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("GTI Tracker Component Tests")
    print("=" * 60)

    results = []

    results.append(("Imports", test_imports()))
    results.append(("Database", test_database()))
    results.append(("Utilities", test_utilities()))

    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)

    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")

    all_passed = all(result[1] for result in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("All tests passed! ✓")
        print("\nYou can now run the application with: python main.py")
    else:
        print("Some tests failed. Please check the errors above.")
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

