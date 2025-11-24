"""
Networking dashboard view
"""
from datetime import date, timedelta
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtCharts import QChartView, QChart, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter
from db.models import NetworkingContact, NetworkingStatus
from db.session import get_session
from utils.date_helpers import get_last_n_days, format_date_short
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
        """Setup the UI components"""
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("Networking")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # Action bar
        action_bar = QHBoxLayout()

        stats_btn = QPushButton("View All Statistics")
        stats_btn.clicked.connect(self.show_statistics.emit)
        action_bar.addWidget(stats_btn)

        self.followup_btn = QPushButton("Needs Follow-Up (0)")
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

    def create_card_frame(self) -> QFrame:
        """Create a standard card frame"""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 20px;
            }
            QFrame:hover {
                border-color: #3498db;
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
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 40px 20px;
                font-size: 18px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        btn.clicked.connect(self.show_add_contact.emit)
        layout.addWidget(btn)

        return frame

    def create_total_card(self) -> QFrame:
        """Create the 'Total Professionals' card"""
        frame = self.create_card_frame()
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)

        self.total_count_label = QLabel("0")
        self.total_count_label.setStyleSheet("""
            font-size: 54px;
            font-weight: 700;
            color: #2c3e50;
        """)
        self.total_count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.total_count_label)

        label = QLabel("Professionals Contacted")
        label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        return frame

    def create_chart_card(self) -> QFrame:
        """Create the 'Last 7 Days' chart card"""
        frame = self.create_card_frame()
        layout = QVBoxLayout(frame)

        title = QLabel("Last 7 Days")
        title.setStyleSheet("font-size: 16px; font-weight: 600; color: #2c3e50;")
        layout.addWidget(title)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.chart_view)

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
            font-size: 54px;
            font-weight: 700;
            color: #95a5a6;
        """)
        self.followup_count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.followup_count_label)

        label = QLabel("Needs Follow-Up")
        label.setStyleSheet("font-size: 14px; color: #7f8c8d;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        return frame

    def load_data(self):
        """Load data from database and update UI"""
        session = get_session()
        try:
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

            # Follow-up count
            settings = session.query(Settings).filter_by(id=1).first()
            follow_up_days = settings.follow_up_days if settings else 3

            cutoff_date = date.today() - timedelta(days=follow_up_days)
            followup_count = session.query(NetworkingContact).filter(
                NetworkingContact.status == NetworkingStatus.COLD_MESSAGE,
                NetworkingContact.contact_date <= cutoff_date
            ).count()

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
        """Update the bar chart with data"""
        # Create bar set
        bar_set = QBarSet("Contacts")
        bar_set.setColor(QColor("#3498db"))

        categories = []
        for label, value in data.items():
            categories.append(label)
            bar_set.append(value)

        # Create series
        series = QBarSeries()
        series.append(bar_set)

        # Create chart
        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(False)

        # Create axes
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        axis_y.setRange(0, max(data.values()) + 1 if data.values() else 5)
        axis_y.setLabelFormat("%d")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        self.chart_view.setChart(chart)

    def refresh(self):
        """Refresh the dashboard data"""
        self.load_data()


# Import QColor for chart colors
from PySide6.QtGui import QColor

