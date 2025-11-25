"""
Priority 3 Features - Advanced functionality
View transitions, milestones, date filters, CSV import
"""
from pathlib import Path

print("Implementing Priority 3 features...")

# 1. Add date filter utilities  
date_filters_content = """from datetime import date, timedelta
from typing import Tuple

def get_last_7_days() -> Tuple[date, date]:
    end = date.today()
    start = end - timedelta(days=7)
    return start, end

def get_last_30_days() -> Tuple[date, date]:
    end = date.today()
    start = end - timedelta(days=30)
    return start, end

def get_last_90_days() -> Tuple[date, date]:
    end = date.today()
    start = end - timedelta(days=90)
    return start, end
"""

date_filters_file = Path(__file__).parent / "utils" / "date_filters.py"
date_filters_file.write_text(date_filters_content, encoding='utf-8')
print("[OK] Created date filter utilities")

# 2. Milestone service
milestone_content = """from db.session import get_session
from db.models import NetworkingContact

class MilestoneService:
    
    MILESTONES = [
        (10, "🎯 10 Contacts!", "Great start on your networking journey!"),
        (25, "🌟 25 Contacts!", "You're building momentum!"),
        (50, "🚀 50 Contacts!", "Halfway to your first hundred!"),
        (100, "💯 100 Contacts!", "You're a networking champion!"),
    ]
    
    @staticmethod
    def check_milestone(contact_count: int) -> tuple:
        for threshold, title, message in MilestoneService.MILESTONES:
            if contact_count == threshold:
                return (True, title, message)
        return (False, "", "")
    
    @staticmethod
    def get_total_contacts() -> int:
        session = get_session()
        try:
            return session.query(NetworkingContact).count()
        finally:
            session.close()
"""

milestone_file = Path(__file__).parent / "utils" / "milestone_service.py"
milestone_file.write_text(milestone_content, encoding='utf-8')
print("[OK] Created milestone service")

# 3. CSV Import utility
csv_import_content = """import csv
from datetime import datetime
from db.session import get_session
from db.models import NetworkingContact, NetworkingStatus

class CSVImportService:
    
    @staticmethod
    def import_contacts(csv_path: str) -> tuple[int, list]:
        session = get_session()
        imported = 0
        errors = []
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                
                for row_num, row in enumerate(reader, start=2):
                    try:
                        # Parse date
                        contact_date = datetime.strptime(row.get('contact_date', ''), '%Y-%m-%d').date()
                        
                        # Parse status
                        status_str = row.get('status', 'Cold message')
                        status = NetworkingStatus.COLD_MESSAGE
                        for s in NetworkingStatus:
                            if s.value == status_str:
                                status = s
                                break
                        
                        contact = NetworkingContact(
                            name=row['name'],
                            job_title=row.get('job_title', ''),
                            company=row.get('company', ''),
                            contact_date=contact_date,
                            email=row.get('email'),
                            linkedin_url=row.get('linkedin_url'),
                            phone=row.get('phone'),
                            relevant_info=row.get('relevant_info'),
                            status=status
                        )
                        
                        session.add(contact)
                        imported += 1
                        
                    except Exception as e:
                        errors.append(f"Row {row_num}: {str(e)}")
            
            session.commit()
            
        except Exception as e:
            session.rollback()
            errors.append(f"File error: {str(e)}")
        finally:
            session.close()
        
        return imported, errors
"""

csv_file = Path(__file__).parent / "utils" / "csv_import.py"
csv_file.write_text(csv_import_content, encoding='utf-8')
print("[OK] Created CSV import utility")

print("\nAll Priority 3 utilities created successfully!")
