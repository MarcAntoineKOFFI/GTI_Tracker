"""
Networking contact list view
"""
from datetime import date, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from db.models import NetworkingContact, NetworkingStatus
from db.session import get_session
from utils.date_helpers import format_date
from sqlalchemy import or_


class NetworkingListView(QWidget):
    """List view for networking contacts"""

    go_back = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_followup = False
        self.setup_ui()
        self.load_contacts()

    def setup_ui(self):
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Top bar
        top_bar = QHBoxLayout()

        back_btn = QPushButton("← Back to Dashboard")
        back_btn.clicked.connect(self.go_back.emit)
        top_bar.addWidget(back_btn)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search contacts by name, company, or title")
        self.search_input.textChanged.connect(self.filter_contacts)
        self.search_input.setMinimumWidth(350)
        top_bar.addWidget(self.search_input)

        top_bar.addStretch()

        add_btn = QPushButton("+ Add Activity")
        add_btn.setStyleSheet("background-color: #3498db; color: white;")
        add_btn.clicked.connect(self.add_contact)
        top_bar.addWidget(add_btn)

        layout.addLayout(top_bar)

        # Filter/Sort bar
        filter_bar = QHBoxLayout()

        filter_bar.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItem("All statuses", None)
        for status in NetworkingStatus:
            self.status_filter.addItem(status.value, status)
        self.status_filter.currentIndexChanged.connect(self.filter_contacts)
        filter_bar.addWidget(self.status_filter)

        filter_bar.addWidget(QLabel("Sort by:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Recent first", "date_desc")
        self.sort_combo.addItem("Oldest first", "date_asc")
        self.sort_combo.addItem("Name A–Z", "name_asc")
        self.sort_combo.addItem("Name Z–A", "name_desc")
        self.sort_combo.addItem("Company A–Z", "company_asc")
        self.sort_combo.addItem("Company Z–A", "company_desc")
        self.sort_combo.currentIndexChanged.connect(self.filter_contacts)
        filter_bar.addWidget(self.sort_combo)

        filter_bar.addStretch()

        layout.addLayout(filter_bar)

        # Table or empty state
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Name", "Job Title", "Company", "Contact Date", "Status", "Actions"
        ])
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeToContents)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.cellDoubleClicked.connect(self.on_row_double_clicked)

        # Empty state
        self.empty_state = QWidget()
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignCenter)

        empty_label = QLabel("No contacts yet.\nClick 'Add Activity' to get started!")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet("font-size: 16px; color: #95a5a6;")
        empty_layout.addWidget(empty_label)

        self.empty_state.hide()

        layout.addWidget(self.table)
        layout.addWidget(self.empty_state)

    def load_contacts(self):
        """Load contacts from database"""
        session = get_session()
        try:
            query = session.query(NetworkingContact)

            # Apply follow-up filter if set
            if self.filter_followup:
                from db.models import Settings
                settings = session.query(Settings).filter_by(id=1).first()
                follow_up_days = settings.follow_up_days if settings else 3
                cutoff_date = date.today() - timedelta(days=follow_up_days)

                query = query.filter(
                    NetworkingContact.status == NetworkingStatus.COLD_MESSAGE,
                    NetworkingContact.contact_date <= cutoff_date
                )

            self.all_contacts = query.all()
            self.filter_contacts()

        finally:
            session.close()

    def filter_contacts(self):
        """Filter and sort contacts based on current filters"""
        filtered = self.all_contacts.copy()

        # Apply search filter
        search_text = self.search_input.text().lower()
        if search_text:
            filtered = [
                c for c in filtered
                if (search_text in c.name.lower() or
                    search_text in c.company.lower() or
                    search_text in c.job_title.lower())
            ]

        # Apply status filter
        status_filter = self.status_filter.currentData()
        if status_filter:
            filtered = [c for c in filtered if c.status == status_filter]

        # Apply sorting
        sort_by = self.sort_combo.currentData()
        if sort_by == "date_desc":
            filtered.sort(key=lambda c: c.contact_date, reverse=True)
        elif sort_by == "date_asc":
            filtered.sort(key=lambda c: c.contact_date)
        elif sort_by == "name_asc":
            filtered.sort(key=lambda c: c.name.lower())
        elif sort_by == "name_desc":
            filtered.sort(key=lambda c: c.name.lower(), reverse=True)
        elif sort_by == "company_asc":
            filtered.sort(key=lambda c: c.company.lower())
        elif sort_by == "company_desc":
            filtered.sort(key=lambda c: c.company.lower(), reverse=True)

        self.display_contacts(filtered)

    def display_contacts(self, contacts):
        """Display contacts in the table"""
        if not contacts:
            self.table.hide()
            self.empty_state.show()
            return

        self.table.show()
        self.empty_state.hide()

        self.table.setRowCount(len(contacts))

        for row, contact in enumerate(contacts):
            # Name
            name_item = QTableWidgetItem(contact.name)
            name_item.setData(Qt.UserRole, contact.id)
            font = name_item.font()
            font.setBold(True)
            name_item.setFont(font)
            self.table.setItem(row, 0, name_item)

            # Job Title
            self.table.setItem(row, 1, QTableWidgetItem(contact.job_title))

            # Company
            self.table.setItem(row, 2, QTableWidgetItem(contact.company))

            # Contact Date
            date_str = format_date(contact.contact_date)
            self.table.setItem(row, 3, QTableWidgetItem(date_str))

            # Status (as badge)
            status_widget = self.create_status_badge(contact.status.value)
            self.table.setCellWidget(row, 4, status_widget)

            # Actions
            actions_widget = self.create_actions_widget(contact.id)
            self.table.setCellWidget(row, 5, actions_widget)

    def create_status_badge(self, status: str) -> QWidget:
        """Create a status badge widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)

        badge = QLabel(status)
        badge.setAlignment(Qt.AlignCenter)

        colors = {
            "Cold message": "#9E9E9E",
            "Has responded": "#2196F3",
            "Call": "#FF9800",
            "Interview": "#4CAF50"
        }

        color = colors.get(status, "#9E9E9E")
        badge.setStyleSheet(f"""
            background-color: {color};
            color: white;
            border-radius: 10px;
            padding: 4px 12px;
            font-size: 11px;
            font-weight: 600;
        """)

        layout.addWidget(badge)
        return widget

    def create_actions_widget(self, contact_id: int) -> QWidget:
        """Create actions widget with edit and delete buttons"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        edit_btn = QPushButton("Edit")
        edit_btn.setFixedSize(60, 28)
        edit_btn.clicked.connect(lambda: self.edit_contact(contact_id))
        layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setProperty("class", "danger")
        delete_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        delete_btn.setFixedSize(60, 28)
        delete_btn.clicked.connect(lambda: self.delete_contact(contact_id))
        layout.addWidget(delete_btn)

        return widget

    def on_row_double_clicked(self, row, column):
        """Handle row double click"""
        if column == 5:  # Don't open detail if clicking actions
            return

        contact_id = self.table.item(row, 0).data(Qt.UserRole)
        self.show_contact_detail(contact_id)

    def add_contact(self):
        """Open add contact dialog"""
        from ui.networking_dialogs import AddEditContactDialog

        dialog = AddEditContactDialog(self)
        dialog.contact_saved.connect(self.on_contact_changed)
        dialog.exec()

    def edit_contact(self, contact_id: int):
        """Open edit contact dialog"""
        from ui.networking_dialogs import AddEditContactDialog

        session = get_session()
        try:
            contact = session.query(NetworkingContact).filter_by(id=contact_id).first()
            if contact:
                dialog = AddEditContactDialog(self, contact)
                dialog.contact_saved.connect(self.on_contact_changed)
                dialog.exec()
        finally:
            session.close()

    def delete_contact(self, contact_id: int):
        """Delete a contact"""
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this contact?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            session = get_session()
            try:
                contact = session.query(NetworkingContact).filter_by(id=contact_id).first()
                if contact:
                    session.delete(contact)
                    session.commit()
                    self.on_contact_changed()
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, "Error", f"Failed to delete contact: {str(e)}")
            finally:
                session.close()

    def show_contact_detail(self, contact_id: int):
        """Open contact detail dialog"""
        from ui.networking_dialogs import ContactDetailDialog

        dialog = ContactDetailDialog(self, contact_id)
        dialog.contact_updated.connect(self.on_contact_changed)
        dialog.contact_deleted.connect(self.on_contact_changed)
        dialog.exec()

    def on_contact_changed(self):
        """Reload contacts when one is added/edited/deleted"""
        self.load_contacts()

    def set_filter_followup(self, enabled: bool):
        """Set whether to filter for follow-ups"""
        self.filter_followup = enabled
        self.load_contacts()

