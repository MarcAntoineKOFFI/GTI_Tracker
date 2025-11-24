"""
Internship application list view
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QMessageBox, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from db.models import InternshipApplication, InternshipStatus, NetworkingContact
from db.session import get_session
from utils.date_helpers import format_date


class InternshipListView(QWidget):
    """List view for internship applications"""

    go_back = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_internships()

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
        self.search_input.setPlaceholderText("🔍 Search by role or company")
        self.search_input.textChanged.connect(self.filter_internships)
        self.search_input.setMinimumWidth(350)
        top_bar.addWidget(self.search_input)

        top_bar.addStretch()

        add_btn = QPushButton("+ Add Application")
        add_btn.setStyleSheet("background-color: #3498db; color: white;")
        add_btn.clicked.connect(self.add_internship)
        top_bar.addWidget(add_btn)

        layout.addLayout(top_bar)

        # Filter/Sort bar
        filter_bar = QHBoxLayout()

        filter_bar.addWidget(QLabel("Status:"))
        self.status_filter = QComboBox()
        self.status_filter.addItem("All statuses", None)
        for status in InternshipStatus:
            self.status_filter.addItem(status.value, status)
        self.status_filter.currentIndexChanged.connect(self.filter_internships)
        filter_bar.addWidget(self.status_filter)

        filter_bar.addWidget(QLabel("Sort by:"))
        self.sort_combo = QComboBox()
        self.sort_combo.addItem("Recent first", "date_desc")
        self.sort_combo.addItem("Oldest first", "date_asc")
        self.sort_combo.addItem("Company A–Z", "company_asc")
        self.sort_combo.addItem("Role A–Z", "role_asc")
        self.sort_combo.currentIndexChanged.connect(self.filter_internships)
        filter_bar.addWidget(self.sort_combo)

        filter_bar.addStretch()

        layout.addLayout(filter_bar)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Role Name", "Company", "Application Date", "Status", "Linked Contact", "Link", "Actions"
        ])

        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.cellDoubleClicked.connect(self.on_row_double_clicked)

        # Empty state
        self.empty_state = QWidget()
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignCenter)

        empty_label = QLabel("No applications yet.\nClick 'Add Application' to get started!")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setStyleSheet("font-size: 16px; color: #95a5a6;")
        empty_layout.addWidget(empty_label)

        self.empty_state.hide()

        layout.addWidget(self.table)
        layout.addWidget(self.empty_state)

    def load_internships(self):
        """Load internships from database"""
        session = get_session()
        try:
            self.all_internships = session.query(InternshipApplication).all()

            # Load contacts for display
            self.contacts_map = {}
            for internship in self.all_internships:
                if internship.contact_id:
                    contact = session.query(NetworkingContact).filter_by(
                        id=internship.contact_id
                    ).first()
                    if contact:
                        self.contacts_map[internship.contact_id] = contact

            self.filter_internships()
        finally:
            session.close()

    def filter_internships(self):
        """Filter and sort internships"""
        filtered = self.all_internships.copy()

        # Search filter
        search_text = self.search_input.text().lower()
        if search_text:
            filtered = [
                i for i in filtered
                if (search_text in i.role_name.lower() or
                    search_text in i.company.lower())
            ]

        # Status filter
        status_filter = self.status_filter.currentData()
        if status_filter:
            filtered = [i for i in filtered if i.status == status_filter]

        # Sorting
        sort_by = self.sort_combo.currentData()
        if sort_by == "date_desc":
            filtered.sort(key=lambda i: i.application_date, reverse=True)
        elif sort_by == "date_asc":
            filtered.sort(key=lambda i: i.application_date)
        elif sort_by == "company_asc":
            filtered.sort(key=lambda i: i.company.lower())
        elif sort_by == "role_asc":
            filtered.sort(key=lambda i: i.role_name.lower())

        self.display_internships(filtered)

    def display_internships(self, internships):
        """Display internships in the table"""
        if not internships:
            self.table.hide()
            self.empty_state.show()
            return

        self.table.show()
        self.empty_state.hide()

        self.table.setRowCount(len(internships))

        for row, internship in enumerate(internships):
            # Role Name
            role_item = QTableWidgetItem(internship.role_name)
            role_item.setData(Qt.UserRole, internship.id)
            font = role_item.font()
            font.setBold(True)
            role_item.setFont(font)
            self.table.setItem(row, 0, role_item)

            # Company
            self.table.setItem(row, 1, QTableWidgetItem(internship.company))

            # Application Date
            date_str = format_date(internship.application_date)
            self.table.setItem(row, 2, QTableWidgetItem(date_str))

            # Status
            status_widget = self.create_status_badge(internship.status.value)
            self.table.setCellWidget(row, 3, status_widget)

            # Linked Contact
            contact_widget = self.create_contact_widget(internship)
            self.table.setCellWidget(row, 4, contact_widget)

            # Link
            link_widget = self.create_link_widget(internship)
            self.table.setCellWidget(row, 5, link_widget)

            # Actions
            actions_widget = self.create_actions_widget(internship.id)
            self.table.setCellWidget(row, 6, actions_widget)

    def create_status_badge(self, status: str) -> QWidget:
        """Create a status badge widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)

        badge = QLabel(status)
        badge.setAlignment(Qt.AlignCenter)

        colors = {
            "Applied": "#9E9E9E",
            "Screening": "#2196F3",
            "Interview": "#FF9800",
            "Offer": "#4CAF50",
            "Rejected": "#F44336"
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

    def create_contact_widget(self, internship: InternshipApplication) -> QWidget:
        """Create linked contact widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)

        if internship.contact_id and internship.contact_id in self.contacts_map:
            contact = self.contacts_map[internship.contact_id]
            text = f"{contact.name} – {contact.job_title} @ {contact.company}"
            label = QLabel(text)
            label.setStyleSheet("font-size: 11px; color: #3498db; cursor: pointer;")
            label.mousePressEvent = lambda e: self.view_contact(contact.id)
            layout.addWidget(label)
        else:
            label = QLabel("—")
            label.setStyleSheet("color: #95a5a6;")
            layout.addWidget(label)

        return widget

    def create_link_widget(self, internship: InternshipApplication) -> QWidget:
        """Create job link widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)

        if internship.job_link:
            link_btn = QPushButton("🔗")
            link_btn.setFixedSize(30, 28)
            link_btn.setToolTip("Open job posting")
            link_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(internship.job_link)))
            layout.addWidget(link_btn)
        else:
            label = QLabel("—")
            label.setStyleSheet("color: #95a5a6;")
            layout.addWidget(label)

        return widget

    def create_actions_widget(self, internship_id: int) -> QWidget:
        """Create actions widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(8)

        edit_btn = QPushButton("Edit")
        edit_btn.setFixedSize(60, 28)
        edit_btn.clicked.connect(lambda: self.edit_internship(internship_id))
        layout.addWidget(edit_btn)

        delete_btn = QPushButton("Delete")
        delete_btn.setProperty("class", "danger")
        delete_btn.setStyleSheet("background-color: #e74c3c; color: white;")
        delete_btn.setFixedSize(60, 28)
        delete_btn.clicked.connect(lambda: self.delete_internship(internship_id))
        layout.addWidget(delete_btn)

        return widget

    def on_row_double_clicked(self, row, column):
        """Handle row double click"""
        if column in [5, 6]:  # Don't open detail if clicking link or actions
            return

        internship_id = self.table.item(row, 0).data(Qt.UserRole)
        self.show_internship_detail(internship_id)

    def add_internship(self):
        """Open add internship dialog"""
        from ui.internship_dialogs import AddEditInternshipDialog

        dialog = AddEditInternshipDialog(self)
        dialog.internship_saved.connect(self.on_internship_changed)
        dialog.exec()

    def edit_internship(self, internship_id: int):
        """Open edit internship dialog"""
        from ui.internship_dialogs import AddEditInternshipDialog

        session = get_session()
        try:
            internship = session.query(InternshipApplication).filter_by(
                id=internship_id
            ).first()
            if internship:
                dialog = AddEditInternshipDialog(self, internship)
                dialog.internship_saved.connect(self.on_internship_changed)
                dialog.exec()
        finally:
            session.close()

    def delete_internship(self, internship_id: int):
        """Delete an internship"""
        reply = QMessageBox.question(
            self,
            "Confirm Deletion",
            "Are you sure you want to delete this application?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            session = get_session()
            try:
                internship = session.query(InternshipApplication).filter_by(
                    id=internship_id
                ).first()
                if internship:
                    session.delete(internship)
                    session.commit()
                    self.on_internship_changed()
            except Exception as e:
                session.rollback()
                QMessageBox.critical(self, "Error", f"Failed to delete: {str(e)}")
            finally:
                session.close()

    def show_internship_detail(self, internship_id: int):
        """Open internship detail dialog"""
        from ui.internship_dialogs import InternshipDetailDialog

        dialog = InternshipDetailDialog(self, internship_id)
        dialog.internship_updated.connect(self.on_internship_changed)
        dialog.internship_deleted.connect(self.on_internship_changed)
        dialog.exec()

    def view_contact(self, contact_id: int):
        """View contact details"""
        from ui.networking_dialogs import ContactDetailDialog

        dialog = ContactDetailDialog(self, contact_id)
        dialog.exec()

    def on_internship_changed(self):
        """Reload when internship is added/edited/deleted"""
        self.load_internships()

