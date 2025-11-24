"""
Internship dashboard view
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtCharts import QChartView, QPieSeries, QChart
from PySide6.QtGui import QPainter, QColor
from db.models import InternshipApplication, InternshipStatus
from db.session import get_session


class InternshipDashboard(QWidget):
    """Dashboard view for internship applications"""

    show_add_internship = Signal()
    show_internship_list = Signal()
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
        title = QLabel("Internships")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #FFFFFF;")
        layout.addWidget(title)

        # Action bar with primary button
        action_bar = QHBoxLayout()

        # Primary action: View all applications
        view_all_btn = QPushButton("💼 View All Applications")
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
        view_all_btn.clicked.connect(self.show_internship_list.emit)
        action_bar.addWidget(view_all_btn)

        # Secondary action
        stats_btn = QPushButton("View Statistics")
        stats_btn.setProperty("class", "secondary")
        stats_btn.clicked.connect(self.show_statistics.emit)
        action_bar.addWidget(stats_btn)

        action_bar.addStretch()
        layout.addLayout(action_bar)

        # Dashboard grid (2x2)
        grid = QGridLayout()
        grid.setSpacing(16)

        # Card 1: Add Internship Application (large button)
        self.add_card = self.create_add_application_card()
        grid.addWidget(self.add_card, 0, 0)

        # Card 2: Total Applications
        self.total_card = self.create_total_card()
        grid.addWidget(self.total_card, 0, 1)

        # Card 3: Status Distribution Chart
        self.chart_card = self.create_chart_card()
        grid.addWidget(self.chart_card, 1, 0)

        # Card 4: Active Applications
        self.active_card = self.create_active_card()
        grid.addWidget(self.active_card, 1, 1)

        layout.addLayout(grid)
        layout.addStretch()

    def create_card_frame(self) -> QFrame:
        """Create a standard card frame"""
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setMinimumWidth(300)  # Increased for more space
        frame.setMinimumHeight(180)  # Ensure vertical space
        frame.setStyleSheet("""
            QFrame {
                background-color: #0A0A0A;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 8px;
                padding: 20px;
            }
        """)
        return frame

    def create_add_application_card(self) -> QFrame:
        """Create the 'Add Application' card"""
        frame = self.create_card_frame()
        layout = QVBoxLayout(frame)

        btn = QPushButton("+ Add Internship Application")
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
        btn.clicked.connect(self.show_add_internship.emit)
        layout.addWidget(btn)

        return frame

    def create_total_card(self) -> QFrame:
        """Create the 'Total Applications' card"""
        frame = self.create_card_frame()
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)

        self.total_count_label = QLabel("0")
        self.total_count_label.setStyleSheet("""
            font-family: 'Inter', 'Segoe UI', sans-serif;
            font-size: 72px;
            font-weight: 500;
            color: #FFFFFF;
        """)
        self.total_count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.total_count_label)

        label = QLabel("Total Applications")
        label.setStyleSheet("font-size: 14px; color: #9BA3B1;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        return frame

    def create_chart_card(self) -> QFrame:
        """Create the status distribution chart card"""
        frame = self.create_card_frame()
        layout = QVBoxLayout(frame)

        title = QLabel("Status Distribution")
        title.setStyleSheet("font-size: 16px; font-weight: 600; color: #FFFFFF;")
        layout.addWidget(title)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(self.chart_view)

        return frame

    def create_active_card(self) -> QFrame:
        """Create the 'Active Applications' card"""
        frame = self.create_card_frame()
        layout = QVBoxLayout(frame)
        layout.setAlignment(Qt.AlignCenter)

        self.active_count_label = QLabel("0")
        self.active_count_label.setStyleSheet("""
            font-family: 'Inter', 'Segoe UI', sans-serif;
            font-size: 72px;
            font-weight: 500;
            color: #FFFFFF;
        """)
        self.active_count_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.active_count_label)

        label = QLabel("Active Applications")
        label.setStyleSheet("font-size: 14px; color: #9BA3B1;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        return frame

    def load_data(self):
        """Load data from database and update UI"""
        session = get_session()
        try:
            # Force SQLAlchemy to fetch fresh data
            session.expire_all()

            # Total applications
            total = session.query(InternshipApplication).count()
            self.total_count_label.setText(str(total))

            # Active applications (non-final statuses)
            active = session.query(InternshipApplication).filter(
                InternshipApplication.status.notin_([
                    InternshipStatus.OFFER,
                    InternshipStatus.REJECTED
                ])
            ).count()
            self.active_count_label.setText(str(active))

            # Status distribution
            status_counts = {}
            for status in InternshipStatus:
                count = session.query(InternshipApplication).filter_by(
                    status=status
                ).count()
                if count > 0:
                    status_counts[status.value] = count

            self.update_chart(status_counts)

        finally:
            session.close()

    def update_chart(self, data: dict):
        """Update the pie chart with data"""
        if not data:
            # Empty chart
            chart = QChart()
            chart.setTitle("No data yet")
            self.chart_view.setChart(chart)
            return

        series = QPieSeries()

        colors = {
            "Applied": QColor("#9E9E9E"),
            "Screening": QColor("#2196F3"),
            "Interview": QColor("#FF9800"),
            "Offer": QColor("#4CAF50"),
            "Rejected": QColor("#F44336")
        }

        for status, count in data.items():
            slice = series.append(status, count)
            if status in colors:
                slice.setColor(colors[status])
            slice.setLabelVisible(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chart_view.setChart(chart)

    def refresh(self):
        """Refresh the dashboard data"""
        self.load_data()

