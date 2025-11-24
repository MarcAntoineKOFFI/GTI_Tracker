"""
Networking contact list view
"""
from datetime import date, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QMessageBox, QAbstractItemView,
    QScrollArea, QGridLayout, QFrame, QButtonGroup
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QFont, QCursor, QColor
from db.models import NetworkingContact, NetworkingStatus
from db.session import get_session
from utils.date_helpers import format_date, days_since
from sqlalchemy import or_
from ui.empty_state import EmptyState
from ui.toast import show_success, show_error


class NetworkingListView(QWidget):
    """List view for networking contacts"""

    go_back = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.filter_followup = False
        self.view_mode = "table"  # "table" or "cards"
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
        back_btn.setProperty("class", "secondary")
        back_btn.clicked.connect(self.go_back.emit)
        top_bar.addWidget(back_btn)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search contacts by name, company, or title")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #1E2330;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 6px;
                padding: 8px 12px;
                color: #FFFFFF;
                font-size: 14px;
            }
            QLineEdit::placeholder {
                color: #6B7280;
            }
            QLineEdit:focus {
                border: 2px solid #FF8B3D;
            }
        """)
        self.search_input.textChanged.connect(self.filter_contacts)
        self.search_input.setMinimumWidth(350)
        top_bar.addWidget(self.search_input)

        top_bar.addStretch()

        # View mode toggle
        view_mode_label = QLabel("View:")
        view_mode_label.setProperty("class", "secondary-text")
        top_bar.addWidget(view_mode_label)

        self.table_view_btn = QPushButton("📋 Table")
        self.table_view_btn.setProperty("class", "compact")
        self.table_view_btn.setCheckable(True)
        self.table_view_btn.setChecked(True)
        self.table_view_btn.clicked.connect(lambda: self.set_view_mode("table"))
        top_bar.addWidget(self.table_view_btn)

        self.card_view_btn = QPushButton("🗂️ Cards")
        self.card_view_btn.setProperty("class", "compact")
        self.card_view_btn.setCheckable(True)
        self.card_view_btn.clicked.connect(lambda: self.set_view_mode("cards"))
        top_bar.addWidget(self.card_view_btn)

        add_btn = QPushButton("+ Add Activity")
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
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0A0A0A;
                color: #FFFFFF;
                gridline-color: rgba(255, 255, 255, 0.05);
                border: none;
            }
            QTableWidget::item {
                color: #FFFFFF;
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #272D3D;
                color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #151923;
                color: #9BA3B1;
                padding: 8px;
                border: none;
                font-weight: 600;
            }
        """)
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

        # Card view container
        self.cards_scroll = QScrollArea()
        self.cards_scroll.setWidgetResizable(True)
        self.cards_scroll.setFrameShape(QScrollArea.NoFrame)

        self.cards_container = QWidget()
        self.cards_layout = QGridLayout(self.cards_container)
        self.cards_layout.setSpacing(16)
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_scroll.setWidget(self.cards_container)
        self.cards_scroll.hide()

        # Empty state
        self.empty_state = QWidget()
        empty_layout = QVBoxLayout(self.empty_state)
        empty_layout.setAlignment(Qt.AlignCenter)

        empty_icon = QLabel("📇")
        empty_icon.setAlignment(Qt.AlignCenter)
        font = empty_icon.font()
        font.setPointSize(48)
        empty_icon.setFont(font)
        empty_layout.addWidget(empty_icon)

        empty_label = QLabel("No contacts yet")
        empty_label.setAlignment(Qt.AlignCenter)
        empty_label.setProperty("class", "heading-3")
        empty_layout.addWidget(empty_label)

        empty_sublabel = QLabel("Click 'Add Activity' to start building your network")
        empty_sublabel.setAlignment(Qt.AlignCenter)
        empty_sublabel.setProperty("class", "secondary-text")
        empty_layout.addWidget(empty_sublabel)

        self.empty_state.hide()

        layout.addWidget(self.table)
        layout.addWidget(self.cards_scroll)
        layout.addWidget(self.empty_state)

    def set_view_mode(self, mode):
        """Switch between table and card view modes"""
        self.view_mode = mode

        self.table_view_btn.setChecked(mode == "table")
        self.card_view_btn.setChecked(mode == "cards")

        # Re-display contacts in new mode
        self.filter_contacts()

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
        """Display contacts in either table or card view"""
        if not contacts:
            self.table.hide()
            self.cards_scroll.hide()
            self.empty_state.show()
            return

        self.empty_state.hide()

        if self.view_mode == "table":
            self.display_table_view(contacts)
        else:
            self.display_card_view(contacts)

    def display_table_view(self, contacts):
        """Display contacts in table format"""
        self.table.show()
        self.cards_scroll.hide()

        self.table.setRowCount(len(contacts))

        for row, contact in enumerate(contacts):
            # Name
            name_item = QTableWidgetItem(contact.name)
            name_item.setData(Qt.UserRole, contact.id)
            name_item.setForeground(QColor("#FFFFFF"))  # White text
            font = name_item.font()
            font.setBold(True)
            name_item.setFont(font)
            self.table.setItem(row, 0, name_item)

            # Job Title
            title_item = QTableWidgetItem(contact.job_title)
            title_item.setForeground(QColor("#E8EAED"))  # Light gray text
            self.table.setItem(row, 1, title_item)

            # Company
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
            self.table.setCellWidget(row, 5, actions_widget)

    def display_card_view(self, contacts):
        """Display contacts as cards in grid layout"""
        self.table.hide()
        self.cards_scroll.show()

        # Clear existing cards
        while self.cards_layout.count():
            item = self.cards_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Display contacts as cards (3 per row)
        for idx, contact in enumerate(contacts):
            card = self.create_contact_card(contact)
            row = idx // 3
            col = idx % 3
            self.cards_layout.addWidget(card, row, col)

        # Add stretch to push cards to top
        self.cards_layout.setRowStretch(self.cards_layout.rowCount(), 1)

    def create_contact_card(self, contact: NetworkingContact) -> QFrame:
        """Create a professional contact card widget"""
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setCursor(QCursor(Qt.PointingHandCursor))
        card.setStyleSheet("""
            QFrame {
                background-color: #1E2330;
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 12px;
                padding: 20px;
            }
            QFrame:hover {
                border: 1px solid rgba(255, 139, 61, 0.3);
                background-color: #272D3D;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(12)

        # Header with initials circle and name
        header_layout = QHBoxLayout()

        # Initials circle
        initials = "".join([word[0].upper() for word in contact.name.split()[:2]])
        initials_label = QLabel(initials)
        initials_label.setAlignment(Qt.AlignCenter)
        initials_label.setFixedSize(48, 48)
        initials_label.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                        stop:0 #FF8B3D, stop:1 #FF9E54);
            color: #FFFFFF;
            border-radius: 24px;
            font-size: 18px;
            font-weight: 700;
        """)
        header_layout.addWidget(initials_label)

        # Name and title
        name_layout = QVBoxLayout()
        name_layout.setSpacing(2)

        name_label = QLabel(contact.name)
        name_label.setProperty("class", "heading-3")
        name_label.setWordWrap(True)
        name_layout.addWidget(name_label)

        title_label = QLabel(contact.job_title)
        title_label.setProperty("class", "secondary-text")
        title_label.setWordWrap(True)
        name_layout.addWidget(title_label)

        header_layout.addLayout(name_layout, 1)
        layout.addLayout(header_layout)

        # Company
        company_label = QLabel(f"🏢 {contact.company}")
        company_label.setProperty("class", "secondary-text")
        layout.addWidget(company_label)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("background-color: rgba(255, 255, 255, 0.05); max-height: 1px;")
        layout.addWidget(divider)

        # Status and date row
        status_date_layout = QHBoxLayout()

        # Status badge
        status_badge = QLabel(contact.status.value.upper())
        status_colors = {
            "Cold message": ("rgba(158, 158, 158, 0.15)", "#9E9E9E"),
            "Has responded": ("rgba(74, 158, 255, 0.15)", "#4A9EFF"),
            "Call": ("rgba(155, 89, 208, 0.15)", "#9B59D0"),
            "Interview": ("rgba(255, 139, 61, 0.15)", "#FF8B3D")
        }
        bg_color, text_color = status_colors.get(contact.status.value, ("rgba(158, 158, 158, 0.15)", "#9E9E9E"))
        status_badge.setStyleSheet(f"""
            background-color: {bg_color};
            color: {text_color};
            border-radius: 10px;
            padding: 4px 10px;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
        """)
        status_date_layout.addWidget(status_badge)

        status_date_layout.addStretch()

        # Days since contact
        days_ago = days_since(contact.contact_date)
        days_label = QLabel(f"{days_ago}d ago" if days_ago > 0 else "Today")
        days_label.setProperty("class", "tertiary-text")
        status_date_layout.addWidget(days_label)

        layout.addLayout(status_date_layout)

        # Relevant info preview (if exists)
        if contact.relevant_info:
            info_preview = contact.relevant_info[:80] + "..." if len(contact.relevant_info) > 80 else contact.relevant_info
            info_label = QLabel(f"📝 {info_preview}")
            info_label.setProperty("class", "tertiary-text")
            info_label.setWordWrap(True)
            layout.addWidget(info_label)

        layout.addStretch()

        # Action buttons - aligned at bottom
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        actions_layout.setContentsMargins(0, 12, 0, 0)  # Top margin for separation

        # View Details button
        message_btn = QPushButton("View")
        message_btn.setToolTip("View Details & Message")
        message_btn.setFixedSize(70, 32)  # Wider for text
        message_btn.setStyleSheet("""
            QPushButton {
                background-color: #4A9EFF;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #5AAFFF;
            }
        """)
        message_btn.clicked.connect(lambda: self.show_contact_detail(contact.id))
        actions_layout.addWidget(message_btn)

        # Edit button
        edit_btn = QPushButton("Edit")
        edit_btn.setToolTip("Edit Contact")
        edit_btn.setFixedSize(60, 32)  # Wider for text
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF8B3D;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #FF9E54;
            }
        """)
        edit_btn.clicked.connect(lambda: self.edit_contact(contact.id))
        actions_layout.addWidget(edit_btn)

        # Delete button
        delete_btn = QPushButton("Del")
        delete_btn.setToolTip("Delete Contact")
        delete_btn.setFixedSize(50, 32)  # Wider for text
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4757;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #FF5767;
            }
        """)
        delete_btn.clicked.connect(lambda: self.delete_contact(contact.id))
        actions_layout.addWidget(delete_btn)

        actions_layout.addStretch()  # Push buttons to the left

        layout.addLayout(actions_layout)

        # Make entire card clickable to open detail
        card.mousePressEvent = lambda e: self.show_contact_detail(contact.id)

        return card

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
        """Delete a contact with confirmation"""
        session = get_session()
        try:
            contact = session.query(NetworkingContact).filter_by(id=contact_id).first()
            if not contact:
                return

            # Confirmation dialog
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Confirm Deletion")
            msg.setText(f"Delete contact '{contact.name}'?")
            msg.setInformativeText("This action cannot be undone.")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)

            # Style the dialog for dark theme
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: #0A0A0A;
                }
                QMessageBox QLabel {
                    color: #FFFFFF;
                }
                QPushButton {
                    min-width: 80px;
                    padding: 8px 16px;
                }
            """)

            if msg.exec() == QMessageBox.Yes:
                contact_name = contact.name
                session.delete(contact)
                session.commit()
                show_success(self, f"Contact '{contact_name}' deleted")
                self.on_contact_changed()

        except Exception as e:
            session.rollback()
            show_error(self, f"Failed to delete contact: {str(e)}")
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

