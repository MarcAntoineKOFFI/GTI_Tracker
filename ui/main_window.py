"""
Main application window
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QMessageBox
)
from PySide6.QtCore import Qt, QSettings
from PySide6.QtGui import QIcon, QKeySequence, QAction
from ui.networking_dashboard import NetworkingDashboard
from ui.networking_list import NetworkingListView
from ui.networking_stats import NetworkingStatsDialog
from ui.networking_dialogs import AddEditContactDialog
from ui.internship_dashboard import InternshipDashboard
from ui.internship_list import InternshipListView
from ui.internship_stats import InternshipStatsDialog
from ui.internship_dialogs import AddEditInternshipDialog
from ui.settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("GTI Tracker - GET-THAT-INTERNSHIP Tracker")
        self.setMinimumSize(1200, 800)

        # Set application icon
        try:
            from resources.icons import create_app_icon
            self.setWindowIcon(create_app_icon())
        except Exception:
            pass  # Ignore icon errors

        # QSettings for persistence
        self.app_settings = QSettings("GTI_Tracker", "GTI_Tracker")

        self.setup_ui()
        self.setup_shortcuts()
        self.restore_window_state()

    def setup_ui(self):
        """Setup the UI components"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout (horizontal: sidebar | content)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)

        # Content area with stacked widget
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #000000;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Settings button in top-right
        settings_bar = QWidget()
        settings_bar.setStyleSheet("background-color: #000000; border-bottom: 1px solid rgba(255, 255, 255, 0.15);")
        settings_bar_layout = QHBoxLayout(settings_bar)
        settings_bar_layout.setContentsMargins(12, 8, 12, 8)
        settings_bar_layout.addStretch()

        settings_btn = QPushButton("⚙️ Settings")
        settings_btn.setObjectName("settingsButton")
        settings_btn.clicked.connect(self.open_settings)
        settings_bar_layout.addWidget(settings_btn)

        content_layout.addWidget(settings_bar)

        # Stacked widget for different views
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("QStackedWidget { background-color: #000000; }")

        # Networking views
        self.networking_dashboard = NetworkingDashboard()
        self.networking_dashboard.show_add_contact.connect(self.add_networking_contact)
        self.networking_dashboard.show_contact_list.connect(self.show_networking_list)
        self.networking_dashboard.show_statistics.connect(self.show_networking_stats)

        self.networking_list = NetworkingListView()
        self.networking_list.go_back.connect(lambda: self.show_view("networking_dashboard"))

        # Internship views
        self.internship_dashboard = InternshipDashboard()
        self.internship_dashboard.show_add_internship.connect(self.add_internship)
        self.internship_dashboard.show_internship_list.connect(self.show_internship_list)
        self.internship_dashboard.show_statistics.connect(self.show_internship_stats)

        self.internship_list = InternshipListView()
        self.internship_list.go_back.connect(lambda: self.show_view("internship_dashboard"))

        # Add views to stacked widget
        self.view_indices = {}
        self.view_indices["networking_dashboard"] = self.stacked_widget.addWidget(self.networking_dashboard)
        self.view_indices["networking_list"] = self.stacked_widget.addWidget(self.networking_list)
        self.view_indices["internship_dashboard"] = self.stacked_widget.addWidget(self.internship_dashboard)
        self.view_indices["internship_list"] = self.stacked_widget.addWidget(self.internship_list)

        content_layout.addWidget(self.stacked_widget)

        main_layout.addWidget(content_widget, 1)  # stretch factor 1

        # Show networking dashboard by default
        last_tab = self.app_settings.value("last_tab", "networking")
        if last_tab == "internships":
            self.show_view("internship_dashboard")
            self.internship_btn.setChecked(True)
        else:
            self.show_view("networking_dashboard")
            self.networking_btn.setChecked(True)

    def create_sidebar(self) -> QWidget:
        """Create the sidebar with navigation buttons"""
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # App title/logo
        title_widget = QWidget()
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(20, 30, 20, 30)

        from PySide6.QtWidgets import QLabel
        title = QLabel("GTI Tracker")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #ecf0f1;
        """)
        title_layout.addWidget(title)

        subtitle = QLabel("Get That Internship!")
        subtitle.setStyleSheet("""
            font-size: 11px;
            color: #bdc3c7;
        """)
        title_layout.addWidget(subtitle)

        layout.addWidget(title_widget)

        # Navigation buttons
        self.networking_btn = QPushButton("📇 Networking")
        self.networking_btn.setCheckable(True)
        self.networking_btn.clicked.connect(lambda: self.switch_tab("networking"))
        layout.addWidget(self.networking_btn)

        self.internship_btn = QPushButton("💼 Internships")
        self.internship_btn.setCheckable(True)
        self.internship_btn.clicked.connect(lambda: self.switch_tab("internships"))
        layout.addWidget(self.internship_btn)

        layout.addStretch()

        # Version info at bottom
        version_label = QLabel("v1.0.0")
        version_label.setStyleSheet("""
            color: #7f8c8d;
            font-size: 10px;
            padding: 12px;
        """)
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)

        return sidebar

    def setup_shortcuts(self):
        """Setup keyboard shortcuts for common actions"""
        # Ctrl+N for new contact (when in networking view)
        new_contact_action = QAction("New Contact", self)
        new_contact_action.setShortcut(QKeySequence("Ctrl+N"))
        new_contact_action.triggered.connect(self.shortcut_new_item)
        self.addAction(new_contact_action)

        # Ctrl+F for focus search (delegates to current view)
        focus_search_action = QAction("Focus Search", self)
        focus_search_action.setShortcut(QKeySequence("Ctrl+F"))
        focus_search_action.triggered.connect(self.shortcut_focus_search)
        self.addAction(focus_search_action)

        # Ctrl+, for settings
        settings_action = QAction("Open Settings", self)
        settings_action.setShortcut(QKeySequence("Ctrl+,"))
        settings_action.triggered.connect(self.open_settings)
        self.addAction(settings_action)

        # Ctrl+1 for Networking tab
        networking_action = QAction("Networking Tab", self)
        networking_action.setShortcut(QKeySequence("Ctrl+1"))
        networking_action.triggered.connect(lambda: self.switch_tab("networking"))
        self.addAction(networking_action)

        # Ctrl+2 for Internships tab
        internships_action = QAction("Internships Tab", self)
        internships_action.setShortcut(QKeySequence("Ctrl+2"))
        internships_action.triggered.connect(lambda: self.switch_tab("internships"))
        self.addAction(internships_action)

    def shortcut_new_item(self):
        """Handle Ctrl+N shortcut - add new item based on current tab"""
        current_index = self.stacked_widget.currentIndex()

        # Check if we're in networking views
        if current_index in [self.view_indices["networking_dashboard"],
                             self.view_indices["networking_list"]]:
            self.add_networking_contact()
        # Check if we're in internship views
        elif current_index in [self.view_indices["internship_dashboard"],
                               self.view_indices["internship_list"]]:
            self.add_internship()

    def shortcut_focus_search(self):
        """Handle Ctrl+F shortcut - focus search field in list views"""
        current_index = self.stacked_widget.currentIndex()

        # Focus search in networking list
        if current_index == self.view_indices["networking_list"]:
            self.networking_list.search_input.setFocus()
            self.networking_list.search_input.selectAll()
        # Focus search in internship list
        elif current_index == self.view_indices["internship_list"]:
            self.internship_list.search_input.setFocus()
            self.internship_list.search_input.selectAll()

    def switch_tab(self, tab: str):
        """Switch between main tabs (networking/internships)"""
        if tab == "networking":
            self.networking_btn.setChecked(True)
            self.internship_btn.setChecked(False)
            self.show_view("networking_dashboard")
            self.app_settings.setValue("last_tab", "networking")
        elif tab == "internships":
            self.networking_btn.setChecked(False)
            self.internship_btn.setChecked(True)
            self.show_view("internship_dashboard")
            self.app_settings.setValue("last_tab", "internships")

    def show_view(self, view_name: str):
        """Show a specific view in the stacked widget"""
        if view_name in self.view_indices:
            self.stacked_widget.setCurrentIndex(self.view_indices[view_name])

            # Refresh dashboards when showing them
            if view_name == "networking_dashboard":
                self.networking_dashboard.refresh()
            elif view_name == "internship_dashboard":
                self.internship_dashboard.refresh()

    def add_networking_contact(self):
        """Open dialog to add a networking contact"""
        dialog = AddEditContactDialog(self)
        dialog.contact_saved.connect(self.on_data_changed)
        dialog.exec()

    def show_networking_list(self, filter_followup: bool = False):
        """Show networking contact list"""
        self.networking_list.set_filter_followup(filter_followup)
        self.networking_list.load_contacts()
        self.show_view("networking_list")

    def show_networking_stats(self):
        """Show networking statistics dialog"""
        dialog = NetworkingStatsDialog(self)
        dialog.exec()

    def add_internship(self):
        """Open dialog to add an internship"""
        dialog = AddEditInternshipDialog(self)
        dialog.internship_saved.connect(self.on_data_changed)
        dialog.exec()

    def show_internship_list(self):
        """Show internship list"""
        self.internship_list.load_internships()
        self.show_view("internship_list")

    def show_internship_stats(self):
        """Show internship statistics dialog"""
        dialog = InternshipStatsDialog(self)
        dialog.exec()

    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self)
        dialog.settings_saved.connect(self.on_settings_saved)
        dialog.exec()

    def on_data_changed(self):
        """Refresh views when data changes"""
        from PySide6.QtWidgets import QApplication

        # Refresh networking dashboard
        self.networking_dashboard.refresh()

        # Refresh internship dashboard
        self.internship_dashboard.refresh()

        # Force immediate UI update
        QApplication.processEvents()

        # If on list views, refresh them too
        current_view = self.stacked_widget.currentWidget()
        if current_view == self.networking_list:
            self.networking_list.load_contacts()
        elif current_view == self.internship_list:
            self.internship_list.load_internships()
        self.internship_dashboard.refresh()

    def on_settings_saved(self):
        """Handle settings saved"""
        # Could refresh views if needed
        pass

    def restore_window_state(self):
        """Restore window size and position"""
        geometry = self.app_settings.value("window_geometry")
        if geometry:
            self.restoreGeometry(geometry)
        else:
            # Default size if no saved state
            self.resize(1200, 800)

    def closeEvent(self, event):
        """Save window state on close"""
        self.app_settings.setValue("window_geometry", self.saveGeometry())
        event.accept()

