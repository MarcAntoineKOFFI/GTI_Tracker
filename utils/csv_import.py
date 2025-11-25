import csv
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
