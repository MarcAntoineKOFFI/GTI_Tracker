"""
Test adding a contact to verify database works
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from datetime import date
from db.session import get_session, init_database
from db.models import NetworkingContact, NetworkingStatus

def test_add_contact():
    """Test adding a contact"""
    # Initialize database first
    print("Initializing database...")
    init_database()
    print("✓ Database initialized\n")

    session = get_session()
    try:
        # Create test contact
        contact = NetworkingContact(
            name="Test Person",
            job_title="Software Engineer",
            company="Test Company",
            contact_date=date.today(),
            relevant_info="Test info",
            status=NetworkingStatus.COLD_MESSAGE,
            email="test@example.com",
            linkedin_url="https://linkedin.com/in/test",
            phone="555-1234"
        )

        session.add(contact)
        session.commit()

        print("✓ Contact added successfully!")
        print(f"  ID: {contact.id}")
        print(f"  Name: {contact.name}")
        print(f"  Created: {contact.created_at}")
        print(f"  Updated: {contact.updated_at}")

        # Verify it can be retrieved
        retrieved = session.query(NetworkingContact).filter_by(id=contact.id).first()
        if retrieved:
            print("\n✓ Contact can be retrieved from database")
            print(f"  Name: {retrieved.name}")
            print(f"  Email: {retrieved.email}")
            print(f"  LinkedIn: {retrieved.linkedin_url}")
        else:
            print("\n✗ Failed to retrieve contact")
            return False

        return True

    except Exception as e:
        session.rollback()
        print(f"\n✗ Error adding contact: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    print("=" * 60)
    print("TESTING DATABASE - ADD CONTACT")
    print("=" * 60)
    print()

    success = test_add_contact()

    print()
    print("=" * 60)
    if success:
        print("✅ DATABASE TEST PASSED")
    else:
        print("❌ DATABASE TEST FAILED")
    print("=" * 60)

    sys.exit(0 if success else 1)

