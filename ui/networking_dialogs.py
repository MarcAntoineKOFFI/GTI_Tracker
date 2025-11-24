"""
Networking-related dialogs with enterprise-grade validation
"""
from datetime import date, datetime
from typing import Optional
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QDateEdit, QPushButton,
    QLabel, QMessageBox, QCompleter, QWidget, QTextBrowser,
    QGroupBox
)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QClipboard
from db.models import NetworkingContact, NetworkingStatus
from db.session import get_session
from utils.validators import validate_required_field
from utils.enterprise_validators import InputValidator, FormValidator
from utils.message_generator import generate_networking_message
from utils.date_helpers import days_since, format_date
from utils.error_handler import handle_errors, activity_logger


class AddEditContactDialog(QDialog):
    """Dialog for adding or editing a networking contact"""

    contact_saved = Signal()

    def __init__(self, parent=None, contact: Optional[NetworkingContact] = None):
        super().__init__(parent)
        self.contact = contact
        self.is_edit_mode = contact is not None

        self.setWindowTitle("Edit Contact" if self.is_edit_mode else "Add Contact")
        self.setFixedSize(550, 650)
        self.setModal(True)

        self.setup_ui()

        if self.is_edit_mode:
            self.populate_fields()

    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # Form
        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        # Name field
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("e.g., John Smith")
        self.name_error = QLabel()
        self.name_error.setObjectName("error-label")
        self.name_error.setStyleSheet("color: #e74c3c; font-size: 11px;")
        self.name_error.hide()

        name_widget = QWidget()
        name_layout = QVBoxLayout(name_widget)
        name_layout.setContentsMargins(0, 0, 0, 0)
        name_layout.setSpacing(4)
        name_layout.addWidget(self.name_input)
        name_layout.addWidget(self.name_error)

        form_layout.addRow("Name *", name_widget)

        # Job Title field
        self.job_title_input = QLineEdit()
        self.job_title_input.setPlaceholderText("e.g., Senior Software Engineer")
        self.job_title_error = QLabel()
        self.job_title_error.setStyleSheet("color: #e74c3c; font-size: 11px;")
        self.job_title_error.hide()

        job_title_widget = QWidget()
        job_title_layout = QVBoxLayout(job_title_widget)
        job_title_layout.setContentsMargins(0, 0, 0, 0)
        job_title_layout.setSpacing(4)
        job_title_layout.addWidget(self.job_title_input)
        job_title_layout.addWidget(self.job_title_error)

        form_layout.addRow("Job Title *", job_title_widget)

        # Company field with autocomplete
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("e.g., Google")
        self.setup_company_completer()
        self.company_error = QLabel()
        self.company_error.setStyleSheet("color: #e74c3c; font-size: 11px;")
        self.company_error.hide()

        company_widget = QWidget()
        company_layout = QVBoxLayout(company_widget)
        company_layout.setContentsMargins(0, 0, 0, 0)
        company_layout.setSpacing(4)
        company_layout.addWidget(self.company_input)
        company_layout.addWidget(self.company_error)

        form_layout.addRow("Company *", company_widget)

        # Contact Date
        self.contact_date_input = QDateEdit()
        self.contact_date_input.setCalendarPopup(True)
        self.contact_date_input.setDate(QDate.currentDate())
        self.contact_date_input.setMaximumDate(QDate.currentDate())
        form_layout.addRow("Contact Date", self.contact_date_input)

        # Relevant Information with character counter
        self.relevant_info_input = QTextEdit()
        self.relevant_info_input.setPlaceholderText(
            "Any specific details about your connection, shared interests, or talking points..."
        )
        self.relevant_info_input.setMaximumHeight(120)
        self.relevant_info_input.textChanged.connect(self.update_char_count)

        self.char_count_label = QLabel("0 / 500")
        self.char_count_label.setAlignment(Qt.AlignRight)

        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(4)
        info_layout.addWidget(self.relevant_info_input)
        info_layout.addWidget(self.char_count_label)

        form_layout.addRow("Relevant Information", info_widget)

        # Status
        self.status_input = QComboBox()
        for status in NetworkingStatus:
            self.status_input.addItem(status.value, status)
        form_layout.addRow("Status", self.status_input)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save Changes" if self.is_edit_mode else "Add Contact")
        save_btn.setProperty("class", "primary")
        save_btn.clicked.connect(self.save_contact)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def setup_company_completer(self):
        """Setup autocomplete for company field"""
        session = get_session()
        try:
            # Get distinct companies from contacts
            companies = session.query(NetworkingContact.company).distinct().all()
            company_list = [c[0] for c in companies if c[0]]

            completer = QCompleter(company_list)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.company_input.setCompleter(completer)
        finally:
            session.close()

    def populate_fields(self):
        """Populate fields with existing contact data"""
        if not self.contact:
            return

        self.name_input.setText(self.contact.name)
        self.job_title_input.setText(self.contact.job_title)
        self.company_input.setText(self.contact.company)

        q_date = QDate(
            self.contact.contact_date.year,
            self.contact.contact_date.month,
            self.contact.contact_date.day
        )
        self.contact_date_input.setDate(q_date)

        if self.contact.relevant_info:
            self.relevant_info_input.setPlainText(self.contact.relevant_info)

        # Set status
        for i in range(self.status_input.count()):
            if self.status_input.itemData(i) == self.contact.status:
                self.status_input.setCurrentIndex(i)
                break

    def update_char_count(self):
        """Update character count label"""
        text = self.relevant_info_input.toPlainText()
        count = len(text)
        self.char_count_label.setText(f"{count} / 500")

        if count > 500:
            self.char_count_label.setStyleSheet("color: #e74c3c;")
        elif count > 450:
            self.char_count_label.setStyleSheet("color: #e67e22;")
        else:
            self.char_count_label.setStyleSheet("color: #95a5a6;")

    def validate_form(self) -> bool:
        """Validate form fields"""
        is_valid = True

        # Validate name
        name_valid, name_error = validate_required_field(
            self.name_input.text(), "Name"
        )
        if not name_valid:
            self.name_error.setText(name_error)
            self.name_error.show()
            self.name_input.setStyleSheet("border: 2px solid #e74c3c;")
            is_valid = False
        else:
            self.name_error.hide()
            self.name_input.setStyleSheet("")

        # Validate job title
        job_title_valid, job_title_error = validate_required_field(
            self.job_title_input.text(), "Job Title"
        )
        if not job_title_valid:
            self.job_title_error.setText(job_title_error)
            self.job_title_error.show()
            self.job_title_input.setStyleSheet("border: 2px solid #e74c3c;")
            is_valid = False
        else:
            self.job_title_error.hide()
            self.job_title_input.setStyleSheet("")

        # Validate company
        company_valid, company_error = validate_required_field(
            self.company_input.text(), "Company"
        )
        if not company_valid:
            self.company_error.setText(company_error)
            self.company_error.show()
            self.company_input.setStyleSheet("border: 2px solid #e74c3c;")
            is_valid = False
        else:
            self.company_error.hide()
            self.company_input.setStyleSheet("")

        return is_valid

    def save_contact(self):
        """Save the contact to database"""
        if not self.validate_form():
            return

        session = get_session()
        try:
            q_date = self.contact_date_input.date()
            contact_date = date(q_date.year(), q_date.month(), q_date.day())

            if self.is_edit_mode:
                # Update existing contact
                self.contact.name = self.name_input.text().strip()
                self.contact.job_title = self.job_title_input.text().strip()
                self.contact.company = self.company_input.text().strip()
                self.contact.contact_date = contact_date
                self.contact.relevant_info = self.relevant_info_input.toPlainText().strip()
                self.contact.status = self.status_input.currentData()
                self.contact.last_updated = datetime.now()

                session.merge(self.contact)
            else:
                # Create new contact
                new_contact = NetworkingContact(
                    name=self.name_input.text().strip(),
                    job_title=self.job_title_input.text().strip(),
                    company=self.company_input.text().strip(),
                    contact_date=contact_date,
                    relevant_info=self.relevant_info_input.toPlainText().strip(),
                    status=self.status_input.currentData(),
                    created_at=datetime.now(),
                    last_updated=datetime.now()
                )
                session.add(new_contact)

            session.commit()
            self.contact_saved.emit()
            self.accept()

        except Exception as e:
            session.rollback()
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to save contact: {str(e)}"
            )
        finally:
            session.close()


class ContactDetailDialog(QDialog):
    """Dialog showing detailed view of a networking contact"""

    contact_updated = Signal()
    contact_deleted = Signal()

    def __init__(self, parent=None, contact_id: int = None):
        super().__init__(parent)
        self.contact_id = contact_id
        self.contact = None
        self.settings = None

        self.setWindowTitle("Contact Details")
        self.setFixedSize(750, 850)
        self.setModal(True)

        self.load_data()
        self.setup_ui()

    def load_data(self):
        """Load contact and settings from database"""
        session = get_session()
        try:
            from db.models import Settings
            self.contact = session.query(NetworkingContact).filter_by(
                id=self.contact_id
            ).first()
            self.settings = session.query(Settings).filter_by(id=1).first()
        finally:
            session.close()

    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        if not self.contact:
            layout.addWidget(QLabel("Contact not found"))
            return

        # Header section
        header_widget = self.create_header_section()
        layout.addWidget(header_widget)

        # Relevant information section
        info_group = QGroupBox("Relevant Information")
        info_layout = QVBoxLayout()
        info_text = self.contact.relevant_info if self.contact.relevant_info else "No additional information"
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        if not self.contact.relevant_info:
            info_label.setStyleSheet("font-style: italic; color: #95a5a6;")
        info_layout.addWidget(info_label)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # Suggested message section
        message_group = QGroupBox("Suggested Networking Message")
        message_layout = QVBoxLayout()

        self.message_browser = QTextBrowser()
        self.message_browser.setMinimumHeight(200)
        self.update_message()
        message_layout.addWidget(self.message_browser)

        message_btn_layout = QHBoxLayout()
        regen_btn = QPushButton("Regenerate Message")
        regen_btn.clicked.connect(self.update_message)
        message_btn_layout.addWidget(regen_btn)

        copy_btn = QPushButton("Copy to Clipboard")
        copy_btn.clicked.connect(self.copy_message)
        message_btn_layout.addWidget(copy_btn)
        message_btn_layout.addStretch()

        message_layout.addLayout(message_btn_layout)
        message_group.setLayout(message_layout)
        layout.addWidget(message_group)

        # Status management
        status_group = QGroupBox("Status Management")
        status_layout = QVBoxLayout()

        status_row = QHBoxLayout()
        status_row.addWidget(QLabel("Current Status:"))

        self.status_combo = QComboBox()
        for status in NetworkingStatus:
            self.status_combo.addItem(status.value, status)

        # Set current status
        for i in range(self.status_combo.count()):
            if self.status_combo.itemData(i) == self.contact.status:
                self.status_combo.setCurrentIndex(i)
                break

        self.status_combo.currentIndexChanged.connect(self.update_status)
        status_row.addWidget(self.status_combo)
        status_row.addStretch()

        status_layout.addLayout(status_row)
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        # Follow-up section (conditional)
        self.follow_up_widget = self.create_follow_up_section()
        if self.follow_up_widget:
            layout.addWidget(self.follow_up_widget)

        # Bottom buttons
        button_layout = QHBoxLayout()

        delete_btn = QPushButton("Delete Contact")
        delete_btn.setProperty("class", "danger")
        delete_btn.clicked.connect(self.delete_contact)
        button_layout.addWidget(delete_btn)

        button_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def create_header_section(self) -> QWidget:
        """Create the header section with contact info"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Name
        name_label = QLabel(self.contact.name)
        name_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(name_label)

        # Job title and company
        title_label = QLabel(f"{self.contact.job_title} at {self.contact.company}")
        title_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        layout.addWidget(title_label)

        # Contact date and status
        info_layout = QHBoxLayout()

        date_label = QLabel(f"Contacted: {format_date(self.contact.contact_date)}")
        date_label.setStyleSheet("font-size: 13px; color: #95a5a6;")
        info_layout.addWidget(date_label)

        info_layout.addStretch()

        # Status badge
        status_badge = QLabel(self.contact.status.value)
        status_badge.setAlignment(Qt.AlignCenter)
        status_class = self.contact.status.value.lower().replace(" ", "-")
        status_badge.setStyleSheet(f"""
            background-color: {self.get_status_color(self.contact.status.value)};
            color: white;
            border-radius: 12px;
            padding: 6px 16px;
            font-size: 12px;
            font-weight: 600;
        """)
        info_layout.addWidget(status_badge)

        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_contact)
        info_layout.addWidget(edit_btn)

        layout.addLayout(info_layout)

        return widget

    def create_follow_up_section(self) -> Optional[QWidget]:
        """Create follow-up alert section if needed"""
        if not self.settings:
            return None

        days = days_since(self.contact.contact_date)

        if (self.contact.status == NetworkingStatus.COLD_MESSAGE and
            days >= self.settings.follow_up_days):

            widget = QWidget()
            widget.setStyleSheet("background-color: #fff3cd; border: 1px solid #ffc107; border-radius: 4px; padding: 12px;")
            layout = QHBoxLayout(widget)

            alert_label = QLabel(f"⏰ Follow-up needed – it has been {days} days with no response.")
            alert_label.setStyleSheet("color: #856404; font-weight: 500;")
            layout.addWidget(alert_label)

            layout.addStretch()

            followup_btn = QPushButton("Mark as Followed Up")
            followup_btn.clicked.connect(self.mark_followed_up)
            layout.addWidget(followup_btn)

            return widget

        return None

    def get_status_color(self, status: str) -> str:
        """Get color for status"""
        colors = {
            "Cold message": "#9E9E9E",
            "Has responded": "#2196F3",
            "Call": "#FF9800",
            "Interview": "#4CAF50"
        }
        return colors.get(status, "#9E9E9E")

    def update_message(self):
        """Update the generated message"""
        if self.contact and self.settings:
            message = generate_networking_message(self.contact, self.settings)
            self.message_browser.setPlainText(message)

    def copy_message(self):
        """Copy message to clipboard"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.message_browser.toPlainText())

        QMessageBox.information(
            self,
            "Copied",
            "Message copied to clipboard!"
        )

    def update_status(self):
        """Update contact status in database"""
        new_status = self.status_combo.currentData()

        session = get_session()
        try:
            contact = session.query(NetworkingContact).filter_by(
                id=self.contact_id
            ).first()
            if contact:
                contact.status = new_status
                contact.last_updated = datetime.now()
                session.commit()
                self.contact.status = new_status
                self.contact_updated.emit()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update status: {str(e)}")
        finally:
            session.close()

    def mark_followed_up(self):
        """Mark contact as followed up"""
        session = get_session()
        try:
            contact = session.query(NetworkingContact).filter_by(
                id=self.contact_id
            ).first()
            if contact:
                contact.last_updated = datetime.now()
                session.commit()
                self.contact_updated.emit()

                # Remove follow-up widget
                if self.follow_up_widget:
                    self.follow_up_widget.hide()

                QMessageBox.information(
                    self,
                    "Success",
                    "Contact marked as followed up!"
                )
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update: {str(e)}")
        finally:
            session.close()

    def edit_contact(self):
        """Open edit dialog"""
        dialog = AddEditContactDialog(self, self.contact)
        dialog.contact_saved.connect(self.on_contact_edited)
        dialog.exec()

    def on_contact_edited(self):
        """Handle contact edited"""
        self.load_data()
        self.contact_updated.emit()
        # Refresh UI
        self.close()
        # Reopen with updated data
        new_dialog = ContactDetailDialog(self.parent(), self.contact_id)
        new_dialog.contact_updated.connect(lambda: self.contact_updated.emit())
        new_dialog.contact_deleted.connect(lambda: self.contact_deleted.emit())
        new_dialog.exec()

    def delete_contact(self):
        """Delete the contact"""
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete {self.contact.name}?\n\n"
            "This will also remove any linked internship applications.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            session = get_session()
            try:
                contact = session.query(NetworkingContact).filter_by(
                    id=self.contact_id
                ).first()
                if contact:
                    session.delete(contact)
                    session.commit()
                    self.contact_deleted.emit()
                    QMessageBox.information(
                        self,
                        "Success",
                        "Contact deleted successfully!"
                    )
                    self.accept()
            except Exception as e:
                session.rollback()
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to delete contact: {str(e)}"
                )
            finally:
                session.close()

