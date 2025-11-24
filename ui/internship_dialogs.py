"""
Internship-related dialogs
"""
from datetime import date, datetime
from typing import Optional
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QComboBox, QDateEdit, QPushButton,
    QLabel, QMessageBox, QCompleter, QWidget, QGroupBox,
    QTextBrowser
)
from PySide6.QtCore import Qt, QDate, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from db.models import InternshipApplication, InternshipStatus, NetworkingContact
from db.session import get_session
from utils.validators import validate_required_field, is_valid_url
from utils.date_helpers import format_date
from ui.toast import show_success, show_error


class AddEditInternshipDialog(QDialog):
    """Dialog for adding or editing an internship application"""

    internship_saved = Signal()

    def __init__(self, parent=None, internship: Optional[InternshipApplication] = None):
        super().__init__(parent)
        self.internship = internship
        self.is_edit_mode = internship is not None

        self.setWindowTitle("Edit Application" if self.is_edit_mode else "Add Application")
        self.setFixedSize(550, 620)
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

        # Role Name field
        self.role_input = QLineEdit()
        self.role_input.setPlaceholderText("e.g., Software Engineering Intern")
        self.role_error = QLabel()
        self.role_error.setStyleSheet("color: #e74c3c; font-size: 11px;")
        self.role_error.hide()

        role_widget = QWidget()
        role_layout = QVBoxLayout(role_widget)
        role_layout.setContentsMargins(0, 0, 0, 0)
        role_layout.setSpacing(4)
        role_layout.addWidget(self.role_input)
        role_layout.addWidget(self.role_error)

        form_layout.addRow("Role Name *", role_widget)

        # Company field with autocomplete
        self.company_input = QLineEdit()
        self.company_input.setPlaceholderText("e.g., Microsoft")
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

        # Job Link with validation and test button
        link_widget = QWidget()
        link_layout = QHBoxLayout(link_widget)
        link_layout.setContentsMargins(0, 0, 0, 0)
        link_layout.setSpacing(8)

        self.job_link_input = QLineEdit()
        self.job_link_input.setPlaceholderText("https://...")
        link_layout.addWidget(self.job_link_input)

        test_link_btn = QPushButton("Test Link")
        test_link_btn.setFixedWidth(80)
        test_link_btn.clicked.connect(self.test_link)
        link_layout.addWidget(test_link_btn)

        self.link_error = QLabel()
        self.link_error.setStyleSheet("color: #e74c3c; font-size: 11px;")
        self.link_error.hide()

        link_container = QWidget()
        link_container_layout = QVBoxLayout(link_container)
        link_container_layout.setContentsMargins(0, 0, 0, 0)
        link_container_layout.setSpacing(4)
        link_container_layout.addWidget(link_widget)
        link_container_layout.addWidget(self.link_error)

        form_layout.addRow("Job Link", link_container)

        # Application Date
        self.application_date_input = QDateEdit()
        self.application_date_input.setCalendarPopup(True)
        self.application_date_input.setDate(QDate.currentDate())
        form_layout.addRow("Application Date", self.application_date_input)

        # Linked Contact
        self.contact_combo = QComboBox()
        self.contact_combo.setEditable(True)
        self.setup_contact_combo()
        form_layout.addRow("Linked Contact", self.contact_combo)

        # Status
        self.status_input = QComboBox()
        for status in InternshipStatus:
            self.status_input.addItem(status.value, status)
        form_layout.addRow("Status", self.status_input)

        # Notes
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Any notes about the application...")
        self.notes_input.setMaximumHeight(100)
        form_layout.addRow("Notes", self.notes_input)

        layout.addLayout(form_layout)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save Changes" if self.is_edit_mode else "Add Application")
        save_btn.setProperty("class", "primary")
        save_btn.clicked.connect(self.save_internship)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def setup_company_completer(self):
        """Setup autocomplete for company field"""
        session = get_session()
        try:
            # Get distinct companies from both internships and contacts
            internship_companies = session.query(InternshipApplication.company).distinct().all()
            contact_companies = session.query(NetworkingContact.company).distinct().all()

            company_set = set()
            for c in internship_companies:
                if c[0]:
                    company_set.add(c[0])
            for c in contact_companies:
                if c[0]:
                    company_set.add(c[0])

            company_list = sorted(list(company_set))

            completer = QCompleter(company_list)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            self.company_input.setCompleter(completer)
        finally:
            session.close()

    def setup_contact_combo(self):
        """Setup contact combobox"""
        session = get_session()
        try:
            self.contact_combo.addItem("No linked contact", None)

            contacts = session.query(NetworkingContact).order_by(
                NetworkingContact.name
            ).all()

            for contact in contacts:
                display = f"{contact.name} – {contact.job_title} @ {contact.company}"
                self.contact_combo.addItem(display, contact.id)
        finally:
            session.close()

    def populate_fields(self):
        """Populate fields with existing internship data"""
        if not self.internship:
            return

        self.role_input.setText(self.internship.role_name)
        self.company_input.setText(self.internship.company)

        if self.internship.job_link:
            self.job_link_input.setText(self.internship.job_link)

        q_date = QDate(
            self.internship.application_date.year,
            self.internship.application_date.month,
            self.internship.application_date.day
        )
        self.application_date_input.setDate(q_date)

        # Set linked contact
        if self.internship.contact_id:
            for i in range(self.contact_combo.count()):
                if self.contact_combo.itemData(i) == self.internship.contact_id:
                    self.contact_combo.setCurrentIndex(i)
                    break

        # Set status
        for i in range(self.status_input.count()):
            if self.status_input.itemData(i) == self.internship.status:
                self.status_input.setCurrentIndex(i)
                break

        if self.internship.notes:
            self.notes_input.setPlainText(self.internship.notes)

    def test_link(self):
        """Test opening the job link"""
        link = self.job_link_input.text().strip()

        if not link:
            QMessageBox.warning(self, "No Link", "Please enter a job link first.")
            return

        if not is_valid_url(link):
            QMessageBox.warning(self, "Invalid URL", "The URL appears to be invalid.")
            return

        QDesktopServices.openUrl(QUrl(link))

    def validate_form(self) -> bool:
        """Validate form fields"""
        is_valid = True

        # Validate role
        role_valid, role_error = validate_required_field(
            self.role_input.text(), "Role Name"
        )
        if not role_valid:
            self.role_error.setText(role_error)
            self.role_error.show()
            self.role_input.setStyleSheet("border: 2px solid #e74c3c;")
            is_valid = False
        else:
            self.role_error.hide()
            self.role_input.setStyleSheet("")

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

        # Validate job link if provided
        link = self.job_link_input.text().strip()
        if link and not is_valid_url(link):
            self.link_error.setText("Invalid URL format")
            self.link_error.show()
            self.job_link_input.setStyleSheet("border: 2px solid #e74c3c;")
            is_valid = False
        else:
            self.link_error.hide()
            self.job_link_input.setStyleSheet("")

        return is_valid

    def save_internship(self):
        """Save the internship to database"""
        if not self.validate_form():
            return

        session = get_session()
        try:
            q_date = self.application_date_input.date()
            application_date = date(q_date.year(), q_date.month(), q_date.day())

            contact_id = self.contact_combo.currentData()
            job_link = self.job_link_input.text().strip() or None
            notes = self.notes_input.toPlainText().strip() or None

            if self.is_edit_mode:
                # Update existing internship
                self.internship.role_name = self.role_input.text().strip()
                self.internship.company = self.company_input.text().strip()
                self.internship.job_link = job_link
                self.internship.contact_id = contact_id
                self.internship.application_date = application_date
                self.internship.status = self.status_input.currentData()
                self.internship.notes = notes

                session.merge(self.internship)
                message = f"Application '{self.internship.role_name}' updated!"
            else:
                # Create new internship
                new_internship = InternshipApplication(
                    role_name=self.role_input.text().strip(),
                    company=self.company_input.text().strip(),
                    job_link=job_link,
                    contact_id=contact_id,
                    application_date=application_date,
                    status=self.status_input.currentData(),
                    notes=notes
                )
                session.add(new_internship)
                message = f"Application '{new_internship.role_name}' added!"

            session.commit()

            # Show success toast
            show_success(self.parent(), message)

            self.internship_saved.emit()
            self.accept()

        except Exception as e:
            session.rollback()
            show_error(self.parent(), f"Failed to save application: {str(e)}")
        finally:
            session.close()


class InternshipDetailDialog(QDialog):
    """Dialog showing detailed view of an internship application"""

    internship_updated = Signal()
    internship_deleted = Signal()

    def __init__(self, parent=None, internship_id: int = None):
        super().__init__(parent)
        self.internship_id = internship_id
        self.internship = None
        self.contact = None

        self.setWindowTitle("Application Details")
        self.setFixedSize(750, 700)
        self.setModal(True)

        self.load_data()
        self.setup_ui()

    def load_data(self):
        """Load internship and contact from database"""
        session = get_session()
        try:
            self.internship = session.query(InternshipApplication).filter_by(
                id=self.internship_id
            ).first()

            if self.internship and self.internship.contact_id:
                self.contact = session.query(NetworkingContact).filter_by(
                    id=self.internship.contact_id
                ).first()
        finally:
            session.close()

    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        if not self.internship:
            layout.addWidget(QLabel("Application not found"))
            return

        # Header section
        header_widget = self.create_header_section()
        layout.addWidget(header_widget)

        # Job link button
        if self.internship.job_link:
            view_job_btn = QPushButton("🔗 View Job Posting")
            view_job_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 12px;
                }
            """)
            view_job_btn.clicked.connect(self.open_job_link)
            layout.addWidget(view_job_btn)

        # Linked contact section
        contact_group = QGroupBox("Linked Contact")
        contact_layout = QVBoxLayout()

        if self.contact:
            contact_text = f"Referred by {self.contact.name} – {self.contact.job_title} @ {self.contact.company}"
            contact_label = QLabel(contact_text)
            contact_label.setWordWrap(True)
            contact_label.setStyleSheet("font-size: 13px;")
            contact_layout.addWidget(contact_label)

            view_contact_btn = QPushButton("View Contact Details")
            view_contact_btn.clicked.connect(self.view_contact)
            contact_layout.addWidget(view_contact_btn)
        else:
            no_contact_label = QLabel("No linked contact")
            no_contact_label.setStyleSheet("font-style: italic; color: #95a5a6;")
            contact_layout.addWidget(no_contact_label)

            link_contact_btn = QPushButton("Link Contact")
            link_contact_btn.clicked.connect(self.link_contact)
            contact_layout.addWidget(link_contact_btn)

        contact_group.setLayout(contact_layout)
        layout.addWidget(contact_group)

        # Status management
        status_group = QGroupBox("Status Management")
        status_layout = QHBoxLayout()

        status_layout.addWidget(QLabel("Current Status:"))

        self.status_combo = QComboBox()
        for status in InternshipStatus:
            self.status_combo.addItem(status.value, status)

        # Set current status
        for i in range(self.status_combo.count()):
            if self.status_combo.itemData(i) == self.internship.status:
                self.status_combo.setCurrentIndex(i)
                break

        self.status_combo.currentIndexChanged.connect(self.update_status)
        status_layout.addWidget(self.status_combo)
        status_layout.addStretch()

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        # Notes section
        notes_group = QGroupBox("Notes")
        notes_layout = QVBoxLayout()

        self.notes_edit = QTextEdit()
        self.notes_edit.setPlainText(self.internship.notes or "")
        self.notes_edit.setMaximumHeight(150)
        notes_layout.addWidget(self.notes_edit)

        save_notes_btn = QPushButton("Save Notes")
        save_notes_btn.clicked.connect(self.save_notes)
        notes_layout.addWidget(save_notes_btn)

        notes_group.setLayout(notes_layout)
        layout.addWidget(notes_group)

        layout.addStretch()

        # Bottom buttons
        button_layout = QHBoxLayout()

        delete_btn = QPushButton("Delete Application")
        delete_btn.setProperty("class", "danger")
        delete_btn.clicked.connect(self.delete_internship)
        button_layout.addWidget(delete_btn)

        button_layout.addStretch()

        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_internship)
        button_layout.addWidget(edit_btn)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        layout.addLayout(button_layout)

    def create_header_section(self) -> QWidget:
        """Create the header section with internship info"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Role name
        role_label = QLabel(self.internship.role_name)
        role_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(role_label)

        # Company
        company_label = QLabel(f"at {self.internship.company}")
        company_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        layout.addWidget(company_label)

        # Application date and status
        info_layout = QHBoxLayout()

        date_label = QLabel(f"Applied: {format_date(self.internship.application_date)}")
        date_label.setStyleSheet("font-size: 13px; color: #95a5a6;")
        info_layout.addWidget(date_label)

        info_layout.addStretch()

        # Status badge
        status_badge = QLabel(self.internship.status.value)
        status_badge.setAlignment(Qt.AlignCenter)
        status_badge.setStyleSheet(f"""
            background-color: {self.get_status_color(self.internship.status.value)};
            color: white;
            border-radius: 12px;
            padding: 6px 16px;
            font-size: 12px;
            font-weight: 600;
        """)
        info_layout.addWidget(status_badge)

        layout.addLayout(info_layout)

        return widget

    def get_status_color(self, status: str) -> str:
        """Get color for status"""
        colors = {
            "Applied": "#9E9E9E",
            "Screening": "#2196F3",
            "Interview": "#FF9800",
            "Offer": "#4CAF50",
            "Rejected": "#F44336"
        }
        return colors.get(status, "#9E9E9E")

    def open_job_link(self):
        """Open job posting in browser"""
        if self.internship.job_link:
            QDesktopServices.openUrl(QUrl(self.internship.job_link))

    def view_contact(self):
        """View linked contact details"""
        if self.contact:
            from ui.networking_dialogs import ContactDetailDialog
            dialog = ContactDetailDialog(self, self.contact.id)
            dialog.exec()

    def link_contact(self):
        """Link a contact to this internship"""
        # Simple implementation: reopen edit dialog
        self.edit_internship()

    def update_status(self):
        """Update internship status in database"""
        new_status = self.status_combo.currentData()

        session = get_session()
        try:
            internship = session.query(InternshipApplication).filter_by(
                id=self.internship_id
            ).first()
            if internship:
                internship.status = new_status
                internship.last_updated = datetime.now()
                session.commit()
                self.internship.status = new_status
                self.internship_updated.emit()
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to update status: {str(e)}")
        finally:
            session.close()

    def save_notes(self):
        """Save notes to database"""
        session = get_session()
        try:
            internship = session.query(InternshipApplication).filter_by(
                id=self.internship_id
            ).first()
            if internship:
                internship.notes = self.notes_edit.toPlainText().strip() or None
                internship.last_updated = datetime.now()
                session.commit()
                self.internship_updated.emit()
                QMessageBox.information(self, "Success", "Notes saved!")
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to save notes: {str(e)}")
        finally:
            session.close()

    def edit_internship(self):
        """Open edit dialog"""
        dialog = AddEditInternshipDialog(self, self.internship)
        dialog.internship_saved.connect(self.on_internship_edited)
        dialog.exec()

    def on_internship_edited(self):
        """Handle internship edited"""
        self.load_data()
        self.internship_updated.emit()
        self.close()
        # Reopen with updated data
        new_dialog = InternshipDetailDialog(self.parent(), self.internship_id)
        new_dialog.internship_updated.connect(lambda: self.internship_updated.emit())
        new_dialog.internship_deleted.connect(lambda: self.internship_deleted.emit())
        new_dialog.exec()

    def delete_internship(self):
        """Delete the internship application"""
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete this application for {self.internship.role_name}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            session = get_session()
            try:
                internship = session.query(InternshipApplication).filter_by(
                    id=self.internship_id
                ).first()
                if internship:
                    session.delete(internship)
                    session.commit()
                    self.internship_deleted.emit()
                    QMessageBox.information(
                        self,
                        "Success",
                        "Application deleted successfully!"
                    )
                    self.accept()
            except Exception as e:
                session.rollback()
                QMessageBox.critical(
                    self,
                    "Error",
                    f"Failed to delete application: {str(e)}"
                )
            finally:
                session.close()

