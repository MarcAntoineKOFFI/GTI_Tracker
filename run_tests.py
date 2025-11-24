"""
GTI Tracker - Comprehensive Test Suite
Run this script to test core functionality
"""
import sys
from datetime import date, timedelta
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from db.session import init_database, get_session
from db.models import NetworkingContact, NetworkingStatus, InternshipApplication, InternshipStatus, Settings
from utils.message_generator import generate_networking_message
from utils.date_helpers import days_since, format_date, get_last_n_weeks


def print_section(title):
    """Print a test section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def test_database_initialization():
    """Test database initialization"""
    print_section("Testing Database Initialization")
    
    try:
        init_database()
        print("✓ Database initialized successfully")
        
        session = get_session()
        settings = session.query(Settings).filter_by(id=1).first()
        
        if settings:
            print("✓ Default settings created")
            print(f"  - Follow-up days: {settings.follow_up_days}")
            print(f"  - Template length: {len(settings.message_template)} characters")
        else:
            print("✗ Settings not found")
            
        session.close()
        return True
        
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False


def test_networking_crud():
    """Test CRUD operations for networking contacts"""
    print_section("Testing Networking Contact CRUD Operations")
    
    session = get_session()
    try:
        # Create
        contact = NetworkingContact(
            name="Test Contact",
            job_title="Software Engineer",
            company="Test Company",
            contact_date=date.today() - timedelta(days=5),
            relevant_info="Met at career fair",
            status=NetworkingStatus.COLD_MESSAGE
        )
        session.add(contact)
        session.commit()
        print(f"✓ Created contact: {contact.name} (ID: {contact.id})")
        
        # Read
        retrieved = session.query(NetworkingContact).filter_by(id=contact.id).first()
        if retrieved:
            print(f"✓ Retrieved contact: {retrieved.name}")
        else:
            print("✗ Failed to retrieve contact")
            return False
        
        # Update
        retrieved.status = NetworkingStatus.HAS_RESPONDED
        session.commit()
        print(f"✓ Updated contact status to: {retrieved.status.value}")
        
        # Count
        count = session.query(NetworkingContact).count()
        print(f"✓ Total contacts in database: {count}")
        
        # Delete test data
        session.delete(retrieved)
        session.commit()
        print("✓ Deleted test contact")
        
        return True
        
    except Exception as e:
        print(f"✗ Networking CRUD test failed: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def test_internship_crud():
    """Test CRUD operations for internship applications"""
    print_section("Testing Internship Application CRUD Operations")
    
    session = get_session()
    try:
        # Create
        app = InternshipApplication(
            role_name="Software Engineering Intern",
            company="Test Tech Corp",
            application_date=date.today(),
            status=InternshipStatus.APPLIED,
            notes="Found on company website"
        )
        session.add(app)
        session.commit()
        print(f"✓ Created application: {app.role_name} (ID: {app.id})")
        
        # Read
        retrieved = session.query(InternshipApplication).filter_by(id=app.id).first()
        if retrieved:
            print(f"✓ Retrieved application: {retrieved.role_name}")
        else:
            print("✗ Failed to retrieve application")
            return False
        
        # Update
        retrieved.status = InternshipStatus.SCREENING
        session.commit()
        print(f"✓ Updated application status to: {retrieved.status.value}")
        
        # Count
        count = session.query(InternshipApplication).count()
        print(f"✓ Total applications in database: {count}")
        
        # Delete test data
        session.delete(retrieved)
        session.commit()
        print("✓ Deleted test application")
        
        return True
        
    except Exception as e:
        print(f"✗ Internship CRUD test failed: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def test_contact_linking():
    """Test linking internship applications to contacts"""
    print_section("Testing Contact-Application Linking")
    
    session = get_session()
    try:
        # Create contact
        contact = NetworkingContact(
            name="Jane Referrer",
            job_title="Senior Engineer",
            company="Referral Company",
            contact_date=date.today() - timedelta(days=10),
            status=NetworkingStatus.HAS_RESPONDED
        )
        session.add(contact)
        session.commit()
        
        # Create linked application
        app = InternshipApplication(
            role_name="Engineering Intern",
            company="Referral Company",
            application_date=date.today(),
            contact_id=contact.id,
            status=InternshipStatus.APPLIED
        )
        session.add(app)
        session.commit()
        
        print(f"✓ Created linked contact and application")
        print(f"  Contact: {contact.name}")
        print(f"  Application: {app.role_name}")
        print(f"  Link ID: {app.contact_id}")
        
        # Test relationship
        retrieved_app = session.query(InternshipApplication).filter_by(id=app.id).first()
        if retrieved_app.contact:
            print(f"✓ Relationship verified: Application linked to {retrieved_app.contact.name}")
        else:
            print("✗ Relationship not working")
            return False
        
        # Cleanup
        session.delete(app)
        session.delete(contact)
        session.commit()
        print("✓ Cleaned up test data")
        
        return True
        
    except Exception as e:
        print(f"✗ Linking test failed: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def test_message_generation():
    """Test message template generation"""
    print_section("Testing Message Generation")
    
    session = get_session()
    try:
        # Update settings with test data
        settings = session.query(Settings).filter_by(id=1).first()
        if not settings:
            print("✗ Settings not found")
            return False
            
        settings.user_name = "Test Student"
        settings.user_school = "Test University"
        settings.user_ambitions = "Breaking into software engineering"
        session.commit()
        
        # Create test contact
        contact = NetworkingContact(
            name="John Doe",
            job_title="Senior Software Engineer",
            company="Google",
            contact_date=date.today(),
            relevant_info="We both studied Computer Science"
        )
        session.add(contact)
        session.commit()
        
        # Generate message
        message = generate_networking_message(contact, settings)
        
        print("✓ Message generated successfully")
        print("\nGenerated Message Preview:")
        print("-" * 70)
        print(message[:300] + "..." if len(message) > 300 else message)
        print("-" * 70)
        
        # Verify placeholders were replaced
        if "{name}" in message or "{company}" in message:
            print("✗ Placeholders not fully replaced")
            return False
        else:
            print("✓ All placeholders replaced correctly")
        
        # Cleanup
        session.delete(contact)
        session.commit()
        
        return True
        
    except Exception as e:
        print(f"✗ Message generation test failed: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def test_date_helpers():
    """Test date utility functions"""
    print_section("Testing Date Helper Functions")
    
    try:
        # Test days_since
        past_date = date.today() - timedelta(days=7)
        days = days_since(past_date)
        print(f"✓ days_since: {days} days ago")
        
        # Test format_date
        formatted = format_date(date.today())
        print(f"✓ format_date: {formatted}")
        
        # Test get_last_n_weeks
        weeks = get_last_n_weeks(4)
        print(f"✓ get_last_n_weeks: Retrieved {len(weeks)} weeks")
        for i, (start, end) in enumerate(weeks[:2], 1):
            print(f"  Week {i}: {start} to {end}")
        
        return True
        
    except Exception as e:
        print(f"✗ Date helpers test failed: {e}")
        return False


def test_follow_up_logic():
    """Test follow-up reminder logic"""
    print_section("Testing Follow-Up Reminder Logic")
    
    session = get_session()
    try:
        settings = session.query(Settings).filter_by(id=1).first()
        follow_up_days = settings.follow_up_days if settings else 3
        
        # Create contact needing follow-up
        old_contact = NetworkingContact(
            name="Needs Follow-up",
            job_title="Engineer",
            company="Test Co",
            contact_date=date.today() - timedelta(days=follow_up_days + 1),
            status=NetworkingStatus.COLD_MESSAGE
        )
        
        # Create contact not needing follow-up
        recent_contact = NetworkingContact(
            name="Recent Contact",
            job_title="Manager",
            company="Test Inc",
            contact_date=date.today() - timedelta(days=1),
            status=NetworkingStatus.COLD_MESSAGE
        )
        
        session.add_all([old_contact, recent_contact])
        session.commit()
        
        # Query for follow-ups needed
        cutoff_date = date.today() - timedelta(days=follow_up_days)
        needs_followup = session.query(NetworkingContact).filter(
            NetworkingContact.status == NetworkingStatus.COLD_MESSAGE,
            NetworkingContact.contact_date <= cutoff_date
        ).all()
        
        print(f"✓ Follow-up threshold: {follow_up_days} days")
        print(f"✓ Contacts needing follow-up: {len(needs_followup)}")
        
        if old_contact in needs_followup and recent_contact not in needs_followup:
            print("✓ Follow-up logic working correctly")
            result = True
        else:
            print("✗ Follow-up logic not working as expected")
            result = False
        
        # Cleanup
        session.delete(old_contact)
        session.delete(recent_contact)
        session.commit()
        
        return result
        
    except Exception as e:
        print(f"✗ Follow-up logic test failed: {e}")
        session.rollback()
        return False
    finally:
        session.close()


def run_all_tests():
    """Run all tests and summarize results"""
    print("\n" + "#"*70)
    print("#" + " "*68 + "#")
    print("#" + "  GTI TRACKER - COMPREHENSIVE TEST SUITE".center(68) + "#")
    print("#" + " "*68 + "#")
    print("#"*70)
    
    tests = [
        ("Database Initialization", test_database_initialization),
        ("Networking CRUD", test_networking_crud),
        ("Internship CRUD", test_internship_crud),
        ("Contact-Application Linking", test_contact_linking),
        ("Message Generation", test_message_generation),
        ("Date Helpers", test_date_helpers),
        ("Follow-Up Logic", test_follow_up_logic),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ CRITICAL ERROR in {test_name}: {e}")
            results[test_name] = False
    
    # Summary
    print_section("TEST SUMMARY")
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} - {test_name}")
    
    print("\n" + "-"*70)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    print("-"*70)
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! GTI Tracker is working correctly.")
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Please review the output above.")
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

