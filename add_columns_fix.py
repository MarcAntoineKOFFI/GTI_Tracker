"""
Comprehensive fix script: Add Phone/LinkedIn columns + proper spacing
"""
from pathlib import Path

list_file = Path(__file__).parent / "ui" / "networking_list.py"
content = list_file.read_text(encoding='utf-8')

# Fix 1: Change column count from 6 to 8
content = content.replace(
    'self.table.setColumnCount(6)',
    'self.table.setColumnCount(8)'
)

# Fix 2: Update headers to include Phone and LinkedIn
content = content.replace(
    '            "Name", "Job Title", "Company", "Contact Date", "Status", "Actions"',
    '            "Name", "Job Title", "Company", "Phone", "LinkedIn", "Contact Date", "Status", "Actions"'
)

# Fix 3: Replace column resize modes with proper widths for breathing room
old_resize = """        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)"""

new_resize = """        self.table.horizontalHeader().setStretchLastSection(False)
        
        # Use Interactive mode for flexible, spacious columns
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        # Set generous column widths for breathing room - no squeezing!
        self.table.setColumnWidth(0, 160)  # Name
        self.table.horizontalHeader().setMinimumSectionSize(100)
        self.table.setColumnWidth(1, 200)  # Job Title
        self.table.setColumnWidth(2, 180)  # Company
        self.table.setColumnWidth(3, 150)  # Phone
        self.table.setColumnWidth(4, 140)  # LinkedIn
        self.table.setColumnWidth(5, 130)  # Contact Date
        self.table.setColumnWidth(6, 160)  # Status
        self.table.setColumnWidth(7, 150)  # Actions
        
        # Enable horizontal scrolling for smaller screens
        self.table.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)"""

content = content.replace(old_resize, new_resize)

# Fix 4: Update display_table_view to add Phone and LinkedIn widgets
old_display = """            # Company
            company_item = QTableWidgetItem(contact.company)
            company_item.setForeground(QColor("#E8EAED"))  # Light gray text
            self.table.setItem(row, 2, company_item)

            # Contact Date
            date_str = format_date(contact.contact_date)
            date_item = QTableWidgetItem(date_str)
            date_item.setForeground(QColor("#9BA3B1"))  # Secondary text color
            self.table.setItem(row, 3, date_item)

            # Status (as badge)
            status_widget = self.create_status_badge(contact.status.value)
            self.table.setCellWidget(row, 4, status_widget)

            # Actions
            actions_widget = self.create_actions_widget(contact.id)
            self.table.setCellWidget(row, 5, actions_widget)"""

new_display = """            # Company
            company_item = QTableWidgetItem(contact.company)
            company_item.setForeground(QColor("#FFFFFF"))  # White text
            self.table.setItem(row, 2, company_item)

            # Phone - clickable button to copy
            phone_widget = self.create_phone_widget(contact.phone)
            self.table.setCellWidget(row, 3, phone_widget)

            # LinkedIn - clickable button to open
            linkedin_widget = self.create_linkedin_widget(contact.linkedin_url)
            self.table.setCellWidget(row, 4, linkedin_widget)

            # Contact Date
            date_str = format_date(contact.contact_date)
            date_item = QTableWidgetItem(date_str)
            date_item.setForeground(QColor("#FFFFFF"))  # White text
            self.table.setItem(row, 5, date_item)

            # Status - inline dropdown for editing
            status_widget = self.create_status_dropdown(contact.id, contact.status)
            self.table.setCellWidget(row, 6, status_widget)

            # Actions
            actions_widget = self.create_actions_widget(contact.id)
            self.table.setCellWidget(row, 7, actions_widget)"""

content = content.replace(old_display, new_display)

# Fix 5: Update double-click handler for new column count
content = content.replace(
    '        if column == 5:  # Don\'t open detail if clicking actions',
    '        if column == 7:  # Don\'t open detail if clicking actions'
)

# Fix 6: Make Job Title text white too
content = content.replace(
    '            title_item.setForeground(QColor("#E8EAED"))  # Light gray text',
    '            title_item.setForeground(QColor("#FFFFFF"))  # White text'
)

# Fix 7: Add the helper methods after create_actions_widget
helper_methods = '''
    def create_phone_widget(self, phone: str):
        """Create clickable phone widget that copies to clipboard"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        
        if phone:
            phone_btn = QPushButton(phone)
            phone_btn.setStyleSheet("""
                QPushButton {
                     background-color: transparent;
                    color: #4A9EFF;
                    border: none;
                    text-align: left;
                    padding: 4px 8px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: rgba(74, 158, 255, 0.1);
                    border-radius: 4px;
                }
            """)
            phone_btn.setCursor(Qt.PointingHandCursor)
            phone_btn.clicked.connect(lambda: self.copy_phone_to_clipboard(phone))
            layout.addWidget(phone_btn)
        else:
            label = QLabel("-")
            label.setStyleSheet("color: #6B7280; padding: 4px 8px;")
            layout.addWidget(label)
        
        return widget

    def create_linkedin_widget(self, linkedin_url: str):
        """Create clickable LinkedIn widget that opens URL in browser"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        
        if linkedin_url:
            linkedin_btn = QPushButton("🔗 Open")
            linkedin_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #0077B5;
                    border: 1px solid #0077B5;
                    border-radius: 4px;
                    padding: 4px 12px;
                    font-size: 11px;
                    font-weight: 600;
                }
                QPushButton:hover {
                    background-color: rgba(0, 119, 181, 0.1);
                }
            """)
            linkedin_btn.setCursor(Qt.PointingHandCursor)
            linkedin_btn.clicked.connect(lambda: self.open_linkedin_url(linkedin_url))
            layout.addWidget(linkedin_btn)
        else:
            label = QLabel("-")
            label.setStyleSheet("color: #6B7280; padding: 4px 8px;")
            layout.addWidget(label)
        
        return widget

    def create_status_dropdown(self, contact_id: int, current_status):
        """Create status dropdown for inline editing"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        
        status_combo = QComboBox()
        status_combo.setStyleSheet("""
            QComboBox {
                background-color: #1E2330;
                color: #FFFFFF;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                padding: 4px 12px;
                font-size: 11px;
                font-weight: 600;
                min-width: 130px;
            }
            QComboBox:hover {
                border: 1px solid #FF8B3D;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #FFFFFF;
                margin-right: 6px;
            }
        """)
        
        # Add all status options
        from db.models import NetworkingStatus
        for status in NetworkingStatus:
            status_combo.addItem(status.value, status)
            if status == current_status:
                status_combo.setCurrentText(status.value)
        
        # Connect to update handler
        status_combo.currentIndexChanged.connect(
            lambda index: self.update_contact_status(contact_id, status_combo.itemData(index))
        )
        
        layout.addWidget(status_combo)
        return widget

    def copy_phone_to_clipboard(self, phone: str):
        """Copy phone number to clipboard and show notification"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(phone)
        show_success(self, f"📋 Copied: {phone}")

    def open_linkedin_url(self, url: str):
        """Open LinkedIn URL in default browser"""
        import webbrowser
        
        # Add https:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            webbrowser.open(url)
            show_success(self, "🔗 Opening LinkedIn profile...")
        except Exception as e:
            from ui.toast import show_error
            show_error(self, f"Failed to open URL: {str(e)}")

    def update_contact_status(self, contact_id: int, new_status):
        """Update contact status in database"""
        from db.session import get_session
        from db.models import NetworkingContact
        from ui.toast import show_success, show_error
        
        session = get_session()
        try:
            contact = session.query(NetworkingContact).filter_by(id=contact_id).first()
            if contact:
                contact.status = new_status
                session.commit()
                
                # Custom congratulatory messages based on status
                messages = {
                    "Has responded": f"🎉 Great news! {contact.name} responded!",
                    "Call": f"📞 Congratulations on the call with {contact.name}!",
                    "Interview": f"🌟 Amazing! Interview scheduled with {contact.name}!"
                }
                message = messages.get(new_status.value, f"Status updated to: {new_status.value}")
                show_success(self, message)
                
                # Reload contacts to refresh the display
                self.load_contacts()
        except Exception as e:
            session.rollback()
            show_error(self, f"Failed to update status: {str(e)}")
        finally:
            session.close()
'''

# Find where to insert the helper methods (after create_actions_widget)
insert_point = "        return widget\n\n    def on_row_double_clicked"
if insert_point in content:
    content = content.replace(insert_point, f"        return widget\n{helper_methods}\n    def on_row_double_clicked")
else:
    print("WARNING: Could not find insertion point for helper methods")

list_file.write_text(content, encoding='utf-8')
print("[OK] Added Phone and LinkedIn columns with generous spacing!")
print("[OK] All table text is now white")
print("[OK] Added clickable phone (copy), LinkedIn (open), and status dropdown")
print("[OK] Added custom congratulatory messages for status changes")
