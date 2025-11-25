"""
Networking Dashboard with scroll support
"""
from datetime import date, datetime, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QGridLayout, QScrollArea
)
from PySide6.QtCore import Qt, Signal, QMargins
from PySide6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter, QColor
from db.models import NetworkingContact, NetworkingStatus
from utils.smart_followup import SmartFollowUpService
from db.session import get_session
from utils.date_helpers import days_since, get_last_n_days, format_date_short
from sqlalchemy import func


class NetworkingDashboard(QWidget):
    """Dashboard view for networking activities"""

    show_add_contact = Signal()
    show_contact_list = Signal(bool)  # bool indicates filter for follow-ups
    show_statistics = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        """Setup the UI components with scroll support"""
        # Main layout for scroll area
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Create scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #000000;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #0A0A0A;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #272D3D;
                border-radius: 6px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #353B4D;
            }
        """)

        # Content widget inside scroll
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #000000;")
        layout = QVBoxLayout(content_widget)
        layout.setSpacing(24)  # Increased spacing
        layout.setContentsMargins(32, 32, 32, 32)  # Increased margins

        # Title
        title = QLabel("Networking")
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(title)
        
        # Goal tracking widget
        self.goal_widget = self.create_goal_widget()
        layout.addWidget(self.goal_widget)

        # Action bar with primary "View All Contacts" button
        action_bar = QHBoxLayout()

        # Primary action: View all contacts
        view_all_btn = QPushButton("📇 View All Contacts")
        view_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF8B3D;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #FF9E54;
            }
            QPushButton:pressed {
                background-color: #E67A2D;
            }
        """)
        view_all_btn.clicked.connect(lambda: self.show_contact_list.emit(False))
        action_bar.addWidget(view_all_btn)

        # Secondary actions
        stats_btn = QPushButton("View Statistics")
        stats_btn.setProperty("class", "secondary")
        stats_btn.clicked.connect(self.show_statistics.emit)
        action_bar.addWidget(stats_btn)

        self.followup_btn = QPushButton("Needs Follow-Up (0)")
        self.followup_btn.setProperty("class", "secondary")
        self.followup_btn.clicked.connect(lambda: self.show_contact_list.emit(True))
        action_bar.addWidget(self.followup_btn)

        action_bar.addStretch()
        layout.addLayout(action_bar)

        # Dashboard grid (2x2)
        grid = QGridLayout()
        grid.setSpacing(16)

        # Card 1: Add Networking Activity (large button)
        self.add_card = self.create_add_activity_card()
        grid.addWidget(self.add_card, 0, 0)

        # Card 2: Total Professionals Contacted
        self.total_card = self.create_total_card()
        grid.addWidget(self.total_card, 0, 1)

        # Card 3: Last 7 Days Chart
        self.chart_card = self.create_chart_card()
        grid.addWidget(self.chart_card, 1, 0)

        # Card 4: Needs Follow-Up
        self.followup_card = self.create_followup_card()
        grid.addWidget(self.followup_card, 1, 1)

        layout.addLayout(grid)
        layout.addStretch()

        # Add content widget to scroll area
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

    def create_card_frame(self) -> QFrame:
        """Create a standard card frame"""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setMinimumWidth(350)  # Increased for more breathing room
        frame.setMinimumHeight(220)  # Taller for better proportion
        frame.setStyleSheet("""
            QFrame {
                background-color: #0A0A0A;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 32px;
            }
        """)
        return frame

    def create_add_activity_card(self) -> QFrame:
        """Create the 'Add Networking Activity' card"""
        frame = self.create_card_frame()
        layout = QVBoxLayout(frame)

        btn = QPushButton("+ Add Networking Activity")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #0A0A0A;
                color: #FFFFFF;
                border: 2px dashed rgba(255, 139, 61, 0.6);
                border-radius: 12px;
                padding: 40px 20px;
                font-size: 18px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #151515;
                border: 2px dashed #FF8B3D;
                color: #FF8B3D;
            }
            QPushButton:pressed {
                background-color: #0A0A0A;
                border: 2px solid #FF8B3D;
            }
        """)
        btn.clicked.connect(self.show_add_contact.emit)
        layout.addWidget(btn)

        return frame

    def create_total_card(self) -> QFrame:
        """Create the 'Total Professionals' card"""
        frame = self.create_card_frame()
        layout = QVBoxLayout(frame)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignCenter)
        layout.setContentsMargins(24, 24, 24, 24)

        self.total_count_label = QLabel("0")
        self.total_count_label.setStyleSheet("""
            font-family: 'Inter', 'Segoe UI', sans-serif;
            font-size: 64px;
            font-weight: 600;
            color: #FFFFFF;
            margin: 0px;
            padding: 0px;
        """)
        self.total_count_label.setAlignment(Qt.AlignCenter)
        self.total_count_label.setWordWrap(False)
        layout.addWidget(self.total_count_label)

        label = QLabel("Professionals Contacted")
        label.setStyleSheet("""
            font-size: 14px; 
            color: #9BA3B1;
            margin: 0px;
            padding: 0px;
        """)
        label.setAlignment(Qt.AlignCenter)
        label.setWordWrap(True)
        layout.addWidget(label)

        return frame

    def create_chart_card(self) -> QFrame:
        """Create the 'Last 7 Days' chart card with modern design"""
        frame = self.create_card_frame()
        frame.setMinimumWidth(600)  # Even wider for better chart display
        frame.setMinimumHeight(350)  # Much taller
        layout = QVBoxLayout(frame)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Last 7 Days Activity")
        title.setStyleSheet("""
            font-size: 18px; 
            font-weight: 600; 
            color: #FFFFFF;
            margin-bottom: 4px;
        """)
        layout.addWidget(title)

        # Modern custom chart with rounded bars
        from ui.modern_chart import ModernBarChart
        self.chart_view = ModernBarChart()
        self.chart_view.setMinimumHeight(260)
        layout.addWidget(self.chart_view)

        return frame
    
    def create_goal_widget(self) -> QFrame:
        """Create daily goal tracking widget with progress bar"""
        from utils.goal_service import GoalTrackingService
        
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                            stop:0 rgba(255, 139, 61, 0.1),
                                            stop:1 rgba(255, 139, 61, 0.05));
                border: 1px solid rgba(255, 139, 61, 0.3);
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QHBoxLayout(frame)
        layout.setSpacing(16)
        
        # Goal info
        info_layout = QVBoxLayout()
        
        remaining = GoalTrackingService.get_remaining_today()
        today_count = GoalTrackingService.get_today_count()
        goal = GoalTrackingService.get_daily_goal()
        
        if remaining > 0:
            self.goal_label = QLabel(f"🎯 Only {remaining} contact{'s' if remaining != 1 else ''} left today to reach your goal!")
        else:
            self.goal_label = QLabel(f"🎉 Goal achieved! ({today_count}/{goal} contacts today)")
        
        self.goal_label.setStyleSheet("font-size: 14px; font-weight: 600; color: #FF8B3D;")
        info_layout.addWidget(self.goal_label)
        
        # Progress bar
        from PySide6.QtWidgets import QProgressBar
        self.goal_progress = QProgressBar()
        self.goal_progress.setMaximum(100)
        self.goal_progress.setValue(int(GoalTrackingService.get_progress_percentage()))
        self.goal_progress.setTextVisible(False)
        self.goal_progress.setFixedHeight(8)
        self.goal_progress.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.1);
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background-color: #FF8B3D;
                border-radius: 4px;
            }
        """)
        info_layout.addWidget(self.goal_progress)
        
        layout.addLayout(info_layout, 1)
        
        return frame

    def create_followup_card(self) -> QFrame:
        """Create the 'Needs Follow-Up' card"""
        frame = self.create_card_frame()
        frame.setCursor(Qt.PointingHandCursor)
        frame.mousePressEvent = lambda e: self.show_contact_list.emit(True)

        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)

        self.followup_count_label = QLabel("0")
        self.followup_count_label.setStyleSheet("""
            font-family: 'Inter', 'Segoe UI', sans-serif;
            font-size: 72px;
            font-weight: 500;
            color: #FFFFFF;
        """)
        self.followup_count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.followup_count_label)

        label = QLabel("Needs Follow-Up")
        label.setStyleSheet("font-size: 16px; color: #9BA3B1;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        return frame

    def load_data(self):
        """Load data from database and update UI"""
        session = get_session()
        try:
            # Force SQLAlchemy to fetch fresh data (not cached objects)
            session.expire_all()

            from db.models import Settings

            # Total contacts
            total = session.query(NetworkingContact).count()
            self.total_count_label.setText(str(total))

            # Last 7 days data
            last_7_days = get_last_n_days(7)
            daily_counts = {}

            for day in last_7_days:
                count = session.query(NetworkingContact).filter(
                    func.date(NetworkingContact.contact_date) == day
                ).count()
                daily_counts[format_date_short(day)] = count

            self.update_chart(daily_counts)

            # Follow-up count using smart logic
            followup_count = SmartFollowUpService.get_followup_count()

            self.followup_count_label.setText(str(followup_count))
            self.followup_btn.setText(f"Needs Follow-Up ({followup_count})")

            # Update follow-up card styling based on count
            if followup_count > 0:
                self.followup_count_label.setStyleSheet("""
                    font-size: 54px;
                    font-weight: 700;
                    color: #e67e22;
                """)
            else:
                self.followup_count_label.setStyleSheet("""
                    font-size: 54px;
                    font-weight: 700;
                    color: #95a5a6;
                """)

        finally:
            session.close()

    def update_chart(self, data: dict):
        """Update the modern bar chart"""
        self.chart_view.set_data(data)

    def refresh(self):
        """Refresh the dashboard data"""
        self.load_data()
        if hasattr(self, 'goal_widget'):
            self.refresh_goal_widget()

    def refresh_goal_widget(self):
        """Refresh goal widget with latest data"""
        from utils.goal_service import GoalTrackingService
        
        remaining = GoalTrackingService.get_remaining_today()
        today_count = GoalTrackingService.get_today_count()
        goal = GoalTrackingService.get_daily_goal()
        
        # Update label
        if remaining > 0:
            self.goal_label.setText(f"🎯 Only {remaining} contact{'s' if remaining != 1 else ''} left today to reach your goal!")
        else:
            self.goal_label.setText(f"🎉 Goal achieved! ({today_count}/{goal} contacts today)")
        
        # Update progress bar
        self.goal_progress.setValue(int(GoalTrackingService.get_progress_percentage()))

    
    def update_followup_count(self, count: int):
        """Update follow-up counter from notification service"""
        self.followup_count_label.setText(str(count))
        self.followup_btn.setText(f"Needs Follow-Up ({count})")
        
        # Update styling based on count
        if count > 0:
            self.followup_count_label.setStyleSheet("""
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 72px;
                font-weight: 500;
                color: #FF8B3D;
            """)
        else:
            self.followup_count_label.setStyleSheet("""
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 72px;
                font-weight: 500;
                color: #9BA3B1;
            """)


# Import QColor for chart colors
from PySide6.QtGui import QColor

