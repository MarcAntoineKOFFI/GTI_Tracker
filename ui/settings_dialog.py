"""
Settings dialog
"""
import csv
import shutil
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QPushButton, QLabel, QTabWidget, QWidget,
    QLineEdit, QTextEdit, QSpinBox, QMessageBox,
    QFileDialog, QGroupBox
)
from PySide6.QtCore import Qt, Signal
from db.models import Settings, NetworkingContact, InternshipApplication
from db.session import get_session, get_database_path
from utils.message_generator import get_template_placeholders


class SettingsDialog(QDialog):
    """Settings dialog with multiple tabs"""

    settings_saved = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setFixedSize(700, 600)
        self.setModal(True)

        self.settings = None
        self.load_settings()
        self.setup_ui()

    def load_settings(self):
        """Load settings from database"""
        session = get_session()
        try:
            self.settings = session.query(Settings).filter_by(id=1).first()
        finally:
            session.close()

    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Settings")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(title)

        # Tab widget
        tabs = QTabWidget()

        # Personal Information tab
        personal_tab = self.create_personal_tab()
        tabs.addTab(personal_tab, "Personal Information")

        # Message Template tab
        template_tab = self.create_template_tab()
        tabs.addTab(template_tab, "Message Template")

        # Notifications tab
        notifications_tab = self.create_notifications_tab()
        tabs.addTab(notifications_tab, "Notifications & Reminders")

        # Data Management tab
        data_tab = self.create_data_tab()
        tabs.addTab(data_tab, "Data Management")

        layout.addWidget(tabs)

        # Bottom buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setProperty("class", "secondary")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Save Settings")
        save_btn.setProperty("class", "primary")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)

        layout.addLayout(button_layout)

    def create_personal_tab(self) -> QWidget:
        """Create personal information tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)

        self.user_name_input = QLineEdit()
        self.user_name_input.setPlaceholderText("Your full name")
        if self.settings and self.settings.user_name:
            self.user_name_input.setText(self.settings.user_name)
        layout.addRow("Your Name:", self.user_name_input)

        self.user_school_input = QLineEdit()
        self.user_school_input.setPlaceholderText("Your university or school")
        if self.settings and self.settings.user_school:
            self.user_school_input.setText(self.settings.user_school)
        layout.addRow("Your School:", self.user_school_input)

        self.user_ambitions_input = QTextEdit()
        self.user_ambitions_input.setPlaceholderText(
            "Your career ambitions and goals (used in networking messages)"
        )
        self.user_ambitions_input.setMaximumHeight(100)
        if self.settings and self.settings.user_ambitions:
            self.user_ambitions_input.setPlainText(self.settings.user_ambitions)
        layout.addRow("Your Ambitions:", self.user_ambitions_input)

        info_label = QLabel("This information will be used to personalize your networking messages.")
        info_label.setStyleSheet("font-style: italic; color: #7f8c8d; font-size: 12px;")
        info_label.setWordWrap(True)
        layout.addRow("", info_label)

        return widget

    def create_template_tab(self) -> QWidget:
        """Create message template tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)

        # Template editor
        label = QLabel("Networking Message Template:")
        label.setStyleSheet("font-weight: 500;")
        layout.addWidget(label)

        self.template_input = QTextEdit()
        if self.settings and self.settings.message_template:
            self.template_input.setPlainText(self.settings.message_template)
        layout.addWidget(self.template_input)

        # Placeholders legend
        legend_label = QLabel("Available Placeholders:")
        legend_label.setStyleSheet("font-weight: 500; margin-top: 8px;")
        layout.addWidget(legend_label)

        placeholders = get_template_placeholders()
        placeholders_text = ", ".join(placeholders)
        placeholders_label = QLabel(placeholders_text)
        placeholders_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        placeholders_label.setWordWrap(True)
        layout.addWidget(placeholders_label)

        # Buttons
        button_layout = QHBoxLayout()

        reset_btn = QPushButton("Reset to Default")
        reset_btn.clicked.connect(self.reset_template)
        button_layout.addWidget(reset_btn)

        preview_btn = QPushButton("Preview")
        preview_btn.clicked.connect(self.preview_template)
        button_layout.addWidget(preview_btn)

        button_layout.addStretch()

        layout.addLayout(button_layout)

        return widget

    def create_notifications_tab(self) -> QWidget:
        """Create notifications tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        layout.setSpacing(12)

        self.follow_up_days_input = QSpinBox()
        self.follow_up_days_input.setMinimum(1)
        self.follow_up_days_input.setMaximum(30)
        if self.settings:
            self.follow_up_days_input.setValue(self.settings.follow_up_days)
        else:
            self.follow_up_days_input.setValue(3)

        layout.addRow(
            "Flag contacts for follow-up after X days without response:",
            self.follow_up_days_input
        )

        info_label = QLabel(
            "Contacts in 'Cold message' status will be flagged for follow-up "
            "after this many days."
        )
        info_label.setStyleSheet("font-style: italic; color: #7f8c8d; font-size: 12px;")
        info_label.setWordWrap(True)
        layout.addRow("", info_label)
        
        # Daily goal setting
        self.daily_goal_input = QSpinBox()
        self.daily_goal_input.setMinimum(1)
        self.daily_goal_input.setMaximum(20)
        if self.settings and hasattr(self.settings, 'daily_goal'):
            self.daily_goal_input.setValue(self.settings.daily_goal)
        else:
            self.daily_goal_input.setValue(3)
        
        layout.addRow(
            "Daily Contact Goal:",
            self.daily_goal_input
        )
        
        goal_info_label = QLabel(
            "Set your daily goal for new networking contacts. Progress shown on dashboard."
        )
        goal_info_label.setStyleSheet("font-style: italic; color: #7f8c8d; font-size: 12px;")
        goal_info_label.setWordWrap(True)
        layout.addRow("", goal_info_label)

        return widget

    def create_data_tab(self) -> QWidget:
        """Create data management tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(16)

        # Export section
        export_group = QGroupBox("Export Data")
        export_layout = QVBoxLayout()

        export_contacts_btn = QPushButton("Export Contacts to CSV")
        export_contacts_btn.clicked.connect(self.export_contacts)
        export_layout.addWidget(export_contacts_btn)

        export_internships_btn = QPushButton("Export Internships to CSV")
        export_internships_btn.clicked.connect(self.export_internships)
        export_layout.addWidget(export_internships_btn)

        export_db_btn = QPushButton("Export Full Database")
        export_db_btn.clicked.connect(self.export_database)
        export_layout.addWidget(export_db_btn)

        export_group.setLayout(export_layout)
        layout.addWidget(export_group)

        # Import section
        import_group = QGroupBox("Import Data")
        import_layout = QVBoxLayout()

        import_contacts_btn = QPushButton("Import Contacts from CSV")
        import_contacts_btn.clicked.connect(self.import_contacts)
        import_layout.addWidget(import_contacts_btn)

        import_internships_btn = QPushButton("Import Internships from CSV")
        import_internships_btn.clicked.connect(self.import_internships)
        import_layout.addWidget(import_internships_btn)

        import_group.setLayout(import_layout)
        layout.addWidget(import_group)

        # Danger zone
        danger_group = QGroupBox("⚠️ Danger Zone")
        danger_group.setStyleSheet("QGroupBox { color: #e74c3c; font-weight: bold; }")
        danger_layout = QVBoxLayout()

        reset_btn = QPushButton("Reset All Data")
        reset_btn.setProperty("class", "danger")
        reset_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        reset_btn.clicked.connect(self.reset_all_data)
        danger_layout.addWidget(reset_btn)

        warning_label = QLabel("⚠️ This will permanently delete all contacts and applications!")
        warning_label.setStyleSheet("color: #e74c3c; font-size: 11px;")
        warning_label.setWordWrap(True)
        danger_layout.addWidget(warning_label)

        danger_group.setLayout(danger_layout)
        layout.addWidget(danger_group)

        layout.addStretch()

        return widget

    def reset_template(self):
        """Reset message template to default"""
        default_template = """Hi {name},

I hope this message finds you well! My name is {user_name}, and I'm currently a student at {user_school}. I came across your profile and was really impressed by your work as a {job_title} at {company}.

{user_ambitions}

{relevant_info}

I would love to learn more about your experience and any advice you might have for someone looking to break into the field. Would you be open to a brief chat sometime?

Thank you for your time and consideration!

Best regards,
{user_name}"""

        self.template_input.setPlainText(default_template)

    def preview_template(self):
        """Preview the message template"""
        # Create a sample preview
        template = self.template_input.toPlainText()

        preview = template.replace('{name}', 'John Smith')
        preview = preview.replace('{job_title}', 'Senior Software Engineer')
        preview = preview.replace('{company}', 'Tech Corp')
        preview = preview.replace('{user_name}', self.user_name_input.text() or 'Your Name')
        preview = preview.replace('{user_school}', self.user_school_input.text() or 'Your University')
        preview = preview.replace('{user_ambitions}', self.user_ambitions_input.toPlainText() or 'Your ambitions...')
        preview = preview.replace('{relevant_info}', 'We both studied at MIT and share an interest in AI.')

        msg = QMessageBox(self)
        msg.setWindowTitle("Message Preview")
        msg.setText("Preview with sample data:")
        msg.setDetailedText(preview)
        msg.exec()

    def export_contacts(self):
        """Export contacts to CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Contacts",
            str(Path.home() / "networking_contacts.csv"),
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            session = get_session()
            contacts = session.query(NetworkingContact).all()

            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Name', 'Job Title', 'Company', 'Contact Date',
                    'Status', 'Relevant Info'
                ])

                for contact in contacts:
                    writer.writerow([
                        contact.name,
                        contact.job_title,
                        contact.company,
                        contact.contact_date.isoformat(),
                        contact.status.value,
                        contact.relevant_info or ''
                    ])

            session.close()
            QMessageBox.information(self, "Success", f"Contacts exported to {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")

    def export_internships(self):
        """Export internships to CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Internships",
            str(Path.home() / "internship_applications.csv"),
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            session = get_session()
            internships = session.query(InternshipApplication).all()

            with open(file_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Role Name', 'Company', 'Application Date',
                    'Status', 'Job Link', 'Notes'
                ])

                for internship in internships:
                    writer.writerow([
                        internship.role_name,
                        internship.company,
                        internship.application_date.isoformat(),
                        internship.status.value,
                        internship.job_link or '',
                        internship.notes or ''
                    ])

            session.close()
            QMessageBox.information(self, "Success", f"Internships exported to {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export: {str(e)}")

    def export_database(self):
        """Export the entire database file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Database",
            str(Path.home() / "gti_tracker_backup.db"),
            "Database Files (*.db)"
        )

        if not file_path:
            return

        try:
            db_path = get_database_path()
            shutil.copy2(db_path, file_path)
            QMessageBox.information(self, "Success", f"Database exported to {file_path}")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export database: {str(e)}")

    def import_contacts(self):
        """Import contacts from CSV"""
        QMessageBox.information(
            self,
            "Import Contacts",
            "CSV should have columns: Name, Job Title, Company, Contact Date, Status, Relevant Info"
        )

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Contacts",
            str(Path.home()),
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            from datetime import datetime
            from db.models import NetworkingStatus

            session = get_session()
            imported = 0

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    try:
                        # Parse status
                        status_str = row.get('Status', 'Cold message')
                        status = NetworkingStatus.COLD_MESSAGE
                        for s in NetworkingStatus:
                            if s.value == status_str:
                                status = s
                                break

                        # Parse date
                        contact_date = datetime.fromisoformat(row['Contact Date']).date()

                        contact = NetworkingContact(
                            name=row['Name'],
                            job_title=row['Job Title'],
                            company=row['Company'],
                            contact_date=contact_date,
                            status=status,
                            relevant_info=row.get('Relevant Info', ''),
                            created_at=datetime.now(),
                            last_updated=datetime.now()
                        )

                        session.add(contact)
                        imported += 1

                    except Exception as e:
                        print(f"Skipping row due to error: {e}")
                        continue

            session.commit()
            session.close()

            QMessageBox.information(
                self,
                "Success",
                f"Imported {imported} contacts successfully!"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import: {str(e)}")

    def import_internships(self):
        """Import internships from CSV"""
        QMessageBox.information(
            self,
            "Import Internships",
            "CSV should have columns: Role Name, Company, Application Date, Status, Job Link, Notes"
        )

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Internships",
            str(Path.home()),
            "CSV Files (*.csv)"
        )

        if not file_path:
            return

        try:
            from datetime import datetime

            session = get_session()
            imported = 0

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    try:
                        # Parse status
                        status_str = row.get('Status', 'Applied')
                        status = InternshipStatus.APPLIED
                        for s in InternshipStatus:
                            if s.value == status_str:
                                status = s
                                break

                        # Parse date
                        application_date = datetime.fromisoformat(row['Application Date']).date()

                        internship = InternshipApplication(
                            role_name=row['Role Name'],
                            company=row['Company'],
                            application_date=application_date,
                            status=status,
                            job_link=row.get('Job Link', ''),
                            notes=row.get('Notes', ''),
                            last_updated=datetime.now()
                        )

                        session.add(internship)
                        imported += 1

                    except Exception as e:
                        print(f"Skipping row due to error: {e}")
                        continue

            session.commit()
            session.close()

            QMessageBox.information(
                self,
                "Success",
                f"Imported {imported} internships successfully!"
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import: {str(e)}")

    def reset_all_data(self):
        """Reset all data (with confirmation)"""
        # First confirmation
        reply1 = QMessageBox.warning(
            self,
            "⚠️ Confirm Reset",
            "This will permanently delete ALL contacts and internship applications!\n\n"
            "Are you absolutely sure?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply1 != QMessageBox.Yes:
            return

        # Second confirmation - user must type DELETE
        from PySide6.QtWidgets import QInputDialog
        text, ok = QInputDialog.getText(
            self,
            "Final Confirmation",
            "Type 'DELETE' to confirm:"
        )

        if not ok or text != "DELETE":
            QMessageBox.information(self, "Cancelled", "Reset cancelled.")
            return

        # Perform reset
        try:
            session = get_session()
            session.query(NetworkingContact).delete()
            session.query(InternshipApplication).delete()
            session.commit()
            session.close()

            QMessageBox.information(
                self,
                "Success",
                "All data has been reset."
            )

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to reset data: {str(e)}")

    def save_settings(self):
        """Save settings to database"""
        if not self.settings:
            QMessageBox.critical(self, "Error", "Settings not found in database")
            return

        session = get_session()
        try:
            settings = session.query(Settings).filter_by(id=1).first()

            if settings:
                settings.user_name = self.user_name_input.text().strip()
                settings.user_school = self.user_school_input.text().strip()
                settings.user_ambitions = self.user_ambitions_input.toPlainText().strip()
                settings.message_template = self.template_input.toPlainText().strip()
                settings.follow_up_days = self.follow_up_days_input.value()
                settings.daily_goal = self.daily_goal_input.value()

                session.commit()
                self.settings_saved.emit()

                QMessageBox.information(
                    self,
                    "Success",
                    "Settings saved successfully!"
                )

                self.accept()

        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")

        finally:
            session.close()

