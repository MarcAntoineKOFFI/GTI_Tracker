"""
Script to fix contact management features:
1. Add email, phone, LinkedIn to save_contact method
2. Add Phone and LinkedIn columns to table
3. Update display_table_view to show new columns
"""

import sys
from pathlib import Path

# Fix networking_dialogs.py
dialogs_file = Path(__file__).parent / "ui" / "networking_dialogs.py"
content = dialogs_file.read_text(encoding='utf-8')

# Find and replace the create new contact section
old_create = """                # Create new contact
                new_contact = NetworkingContact(
                    name=self.name_input.text().strip(),
                    job_title=self.job_title_input.text().strip(),
                    company=self.company_input.text().strip(),
                    contact_date=contact_date,
                    relevant_info=self.relevant_info_input.toPlainText().strip(),
                    status=self.status_input.currentData()
                )"""

new_create = """                # Create new contact
                new_contact = NetworkingContact(
                    name=self.name_input.text().strip(),
                    job_title=self.job_title_input.text().strip(),
                    company=self.company_input.text().strip(),
                    email=self.email_input.text().strip() or None,
                    linkedin_url=self.linkedin_input.text().strip() or None,
                    phone=self.phone_input.text().strip() or None,
                    contact_date=contact_date,
                    relevant_info=self.relevant_info_input.toPlainText().strip(),
                    status=self.status_input.currentData()
                )"""

content = content.replace(old_create, new_create)

# Find and replace the update existing contact section
old_update = """                # Update existing contact
                self.contact.name = self.name_input.text().strip()
                self.contact.job_title = self.job_title_input.text().strip()
                self.contact.company = self.company_input.text().strip()
                self.contact.contact_date = contact_date
                self.contact.relevant_info = self.relevant_info_input.toPlainText().strip()
                self.contact.status = self.status_input.currentData()"""

new_update = """                # Update existing contact
                self.contact.name = self.name_input.text().strip()
                self.contact.job_title = self.job_title_input.text().strip()
                self.contact.company = self.company_input.text().strip()
                self.contact.email = self.email_input.text().strip() or None
                self.contact.linkedin_url = self.linkedin_input.text().strip() or None
                self.contact.phone = self.phone_input.text().strip() or None
                self.contact.contact_date = contact_date
                self.contact.relevant_info = self.relevant_info_input.toPlainText().strip()
                self.contact.status = self.status_input.currentData()"""

content = content.replace(old_update, new_update)
dialogs_file.write_text(content, encoding='utf-8')

print("[OK] Fixed networking_dialogs.py")

# Fix networking_list.py 
list_file = Path(__file__).parent / "ui" / "networking_list.py"
content = list_file.read_text(encoding='utf-8')

# Update column count and headers
content = content.replace(
    'self.table.setColumnCount(6)',
    'self.table.setColumnCount(8)'
)

content = content.replace(
    '\"Name\", \"Job Title\", \"Company\", \"Contact Date\", \"Status\", \"Actions\"',
    '\"Name\", \"Job Title\", \"Company\", \"Phone\", \"LinkedIn\", \"Contact Date\", \"Status\", \"Actions\"'
)

# Add resize modes for new columns
old_resize = """        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)"""

new_resize = """        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)"""

content = content.replace(old_resize, new_resize)

# Update display_table_view to add Phone and LinkedIn columns with white text
old_display = """            # Company
            company_item = QTableWidgetItem(contact.company)
            company_item.setForeground(QColor(\"#E8EAED\"))  # Light gray text
            self.table.setItem(row, 2, company_item)

            # Contact Date
            date_str = format_date(contact.contact_date)
            date_item = QTableWidgetItem(date_str)
            date_item.setForeground(QColor(\"#9BA3B1\"))  # Secondary text color
            self.table.setItem(row, 3, date_item)

            # Status (as badge)
            status_widget = self.create_status_badge(contact.status.value)
            self.table.setCellWidget(row, 4, status_widget)

            # Actions
            actions_widget = self.create_actions_widget(contact.id)
            self.table.setCellWidget(row, 5, actions_widget)"""

new_display = """            # Company
            company_item = QTableWidgetItem(contact.company)
            company_item.setForeground(QColor(\"#FFFFFF\"))  # White text
            self.table.setItem(row, 2, company_item)

            # Phone
            phone_text = contact.phone if contact.phone else \"-\"
            phone_item = QTableWidgetItem(phone_text)
            phone_item.setForeground(QColor(\"#FFFFFF\"))  # White text
            self.table.setItem(row, 3, phone_item)

            # LinkedIn
            linkedin_text = \"✓\" if contact.linkedin_url else \"-\"
            linkedin_item = QTableWidgetItem(linkedin_text)
            linkedin_item.setForeground(QColor(\"#FFFFFF\"))  # White text
            self.table.setItem(row, 4, linkedin_item)

            # Contact Date
            date_str = format_date(contact.contact_date)
            date_item = QTableWidgetItem(date_str)
            date_item.setForeground(QColor(\"#FFFFFF\"))  # White text
            self.table.setItem(row, 5, date_item)

            # Status (as badge)
            status_widget = self.create_status_badge(contact.status.value)
            self.table.setCellWidget(row, 6, status_widget)

            # Actions
            actions_widget = self.create_actions_widget(contact.id)
            self.table.setCellWidget(row, 7, actions_widget)"""

content = content.replace(old_display, new_display)

# Also update title text to white
content = content.replace(
    '# Job Title\n            title_item = QTableWidgetItem(contact.job_title)\n            title_item.setForeground(QColor(\"#E8EAED\"))  # Light gray text',
    '# Job Title\n            title_item = QTableWidgetItem(contact.job_title)\n            title_item.setForeground(QColor(\"#FFFFFF\"))  # White text'
)

# Fix double-click handler column check
content = content.replace(
    '        if column == 5:  # Don\'t open detail if clicking actions',
    '        if column == 7:  # Don\'t open detail if clicking actions'
)

list_file.write_text(content, encoding='utf-8')

print("[OK] Fixed networking_list.py")
print("\nAll fixes applied successfully!")
