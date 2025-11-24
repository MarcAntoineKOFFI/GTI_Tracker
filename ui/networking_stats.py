"""
Networking statistics window
"""
import csv
from datetime import date, timedelta
from pathlib import Path
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QScrollArea, QWidget, QFileDialog,
    QMessageBox, QGroupBox
)
from PySide6.QtCore import Qt
from PySide6.QtCharts import (
    QChartView, QPieSeries, QChart, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis
)
from PySide6.QtGui import QPainter, QColor
from db.models import NetworkingContact, NetworkingStatus
from db.session import get_session
from utils.date_helpers import get_last_n_weeks
from sqlalchemy import func
from collections import defaultdict


class NetworkingStatsDialog(QDialog):
    """Statistics window for networking"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Networking Statistics")
        self.resize(950, 750)

        self.setup_ui()
        self.load_statistics()

    def setup_ui(self):
        """Setup the UI components"""
        main_layout = QVBoxLayout(self)

        # Title
        title = QLabel("Networking Statistics")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50;")
        main_layout.addWidget(title)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSpacing(20)

        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)

        # Bottom buttons
        button_layout = QHBoxLayout()

        export_btn = QPushButton("Export Report (CSV)")
        export_btn.clicked.connect(self.export_csv)
        button_layout.addWidget(export_btn)

        button_layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)

        main_layout.addLayout(button_layout)

    def load_statistics(self):
        """Load and display statistics"""
        session = get_session()
        try:
            # Overall metrics
            total_contacts = session.query(NetworkingContact).count()

            # Status counts
            status_counts = {}
            for status in NetworkingStatus:
                count = session.query(NetworkingContact).filter_by(status=status).count()
                status_counts[status.value] = count

            # Follow-up needed
            from db.models import Settings
            settings = session.query(Settings).filter_by(id=1).first()
            follow_up_days = settings.follow_up_days if settings else 3
            cutoff_date = date.today() - timedelta(days=follow_up_days)

            followup_count = session.query(NetworkingContact).filter(
                NetworkingContact.status == NetworkingStatus.COLD_MESSAGE,
                NetworkingContact.contact_date <= cutoff_date
            ).count()

            # Create metrics section
            self.create_metrics_section(
                total_contacts, status_counts, followup_count
            )

            # Status distribution pie chart
            self.create_status_chart_section(status_counts)

            # Weekly chart (last 12 weeks)
            all_contacts = session.query(NetworkingContact).all()
            self.create_weekly_chart_section(all_contacts)

            # Conversion funnel
            self.create_funnel_section(status_counts, total_contacts)

            # Top companies
            top_companies = session.query(
                NetworkingContact.company,
                func.count(NetworkingContact.id).label('count')
            ).group_by(NetworkingContact.company).order_by(
                func.count(NetworkingContact.id).desc()
            ).limit(10).all()

            self.create_top_companies_section(top_companies)

        finally:
            session.close()

    def create_metrics_section(self, total, status_counts, followup_count):
        """Create overall metrics section"""
        group = QGroupBox("Overall Metrics")
        layout = QGridLayout()

        # Total
        self.add_metric_card(layout, 0, 0, "Total Contacts", str(total), "#3498db")

        # Status breakdowns
        col = 1
        for status, count in status_counts.items():
            if col > 3:
                break
            percentage = (count / total * 100) if total > 0 else 0
            self.add_metric_card(
                layout, 0, col,
                status,
                f"{count} ({percentage:.1f}%)",
                self.get_status_color(status)
            )
            col += 1

        # Follow-up needed
        self.add_metric_card(
            layout, 1, 0,
            "Needs Follow-Up",
            str(followup_count),
            "#e67e22" if followup_count > 0 else "#95a5a6"
        )

        group.setLayout(layout)
        self.content_layout.addWidget(group)

    def add_metric_card(self, layout, row, col, label, value, color):
        """Add a metric card to grid"""
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 6px;
                padding: 12px;
            }}
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(value_label)

        label_widget = QLabel(label)
        label_widget.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        label_widget.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(label_widget)

        layout.addWidget(card, row, col)

    def create_status_chart_section(self, status_counts):
        """Create status distribution pie chart"""
        group = QGroupBox("Status Distribution")
        layout = QVBoxLayout()

        # Create pie chart
        series = QPieSeries()

        for status, count in status_counts.items():
            if count > 0:
                slice = series.append(status, count)
                slice.setColor(QColor(self.get_status_color(status)))
                slice.setLabelVisible(True)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(300)

        layout.addWidget(chart_view)
        group.setLayout(layout)
        self.content_layout.addWidget(group)

    def create_weekly_chart_section(self, contacts):
        """Create contacts per week bar chart"""
        group = QGroupBox("Contacts Over Last 12 Weeks")
        layout = QVBoxLayout()

        # Get last 12 weeks
        weeks = get_last_n_weeks(12)

        # Count contacts per week
        week_counts = defaultdict(int)
        for contact in contacts:
            contact_date = contact.contact_date
            for week_start, week_end in weeks:
                if week_start <= contact_date <= week_end:
                    week_key = f"{week_start.month}/{week_start.day}"
                    week_counts[week_key] += 1
                    break

        # Create bar chart
        series = QBarSeries()
        bar_set = QBarSet("Contacts")
        bar_set.setColor(QColor("#3498db"))

        categories = []
        counts_list = []
        for week_start, week_end in reversed(weeks):
            week_key = f"{week_start.month}/{week_start.day}"
            categories.append(week_key)
            count = week_counts.get(week_key, 0)
            bar_set.append(count)
            counts_list.append(count)

        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Contacts Per Week")
        chart.setAnimationOptions(QChart.SeriesAnimations)

        # X Axis
        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignBottom)
        series.attachAxis(axis_x)

        # Y Axis
        axis_y = QValueAxis()
        max_count = max(counts_list) if counts_list else 5
        axis_y.setRange(0, max_count + 2)
        axis_y.setLabelFormat("%d")
        chart.addAxis(axis_y, Qt.AlignLeft)
        series.attachAxis(axis_y)

        chart.legend().setVisible(False)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setMinimumHeight(300)

        layout.addWidget(chart_view)

        # Statistics below chart
        if counts_list:
            avg = sum(counts_list) / len(counts_list)
            best_count = max(counts_list)
            best_week_idx = counts_list.index(best_count)
            best_week = categories[best_week_idx]

            stats_label = QLabel(
                f"Average: {avg:.1f} contacts/week  |  "
                f"Best week: {best_week} with {best_count} contacts"
            )
            stats_label.setStyleSheet("color: #7f8c8d; font-size: 12px; padding: 8px;")
            layout.addWidget(stats_label)

        group.setLayout(layout)
        self.content_layout.addWidget(group)

    def create_funnel_section(self, status_counts, total):
        """Create conversion funnel section"""
        group = QGroupBox("Conversion Funnel")
        layout = QVBoxLayout()

        funnel_data = [
            ("Cold message", status_counts.get("Cold message", 0)),
            ("Has responded", status_counts.get("Has responded", 0)),
            ("Call", status_counts.get("Call", 0)),
            ("Interview", status_counts.get("Interview", 0))
        ]

        for i, (stage, count) in enumerate(funnel_data):
            percentage = (count / total * 100) if total > 0 else 0

            stage_widget = QWidget()
            stage_layout = QHBoxLayout(stage_widget)

            # Arrow for non-first items
            if i > 0:
                arrow = QLabel("↓")
                arrow.setStyleSheet("font-size: 20px; color: #95a5a6;")
                stage_layout.addWidget(arrow)

            label = QLabel(f"{stage}: {count} ({percentage:.1f}%)")
            label.setStyleSheet("font-size: 14px; padding: 8px;")
            stage_layout.addWidget(label)
            stage_layout.addStretch()

            layout.addWidget(stage_widget)

        group.setLayout(layout)
        self.content_layout.addWidget(group)

    def create_top_companies_section(self, top_companies):
        """Create top companies section"""
        group = QGroupBox("Top Companies")
        layout = QVBoxLayout()

        if not top_companies:
            label = QLabel("No data available")
            label.setStyleSheet("font-style: italic; color: #95a5a6;")
            layout.addWidget(label)
        else:
            for company, count in top_companies:
                company_widget = QWidget()
                company_layout = QHBoxLayout(company_widget)

                company_label = QLabel(company)
                company_label.setStyleSheet("font-weight: 500;")
                company_layout.addWidget(company_label)

                company_layout.addStretch()

                count_label = QLabel(str(count))
                count_label.setStyleSheet("color: #3498db; font-weight: bold;")
                company_layout.addWidget(count_label)

                layout.addWidget(company_widget)

        group.setLayout(layout)
        self.content_layout.addWidget(group)

    def get_status_color(self, status: str) -> str:
        """Get color for status"""
        colors = {
            "Cold message": "#9E9E9E",
            "Has responded": "#2196F3",
            "Call": "#FF9800",
            "Interview": "#4CAF50"
        }
        return colors.get(status, "#9E9E9E")

    def export_csv(self):
        """Export statistics to CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Statistics",
            str(Path.home() / "networking_statistics.csv"),
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
                    'Status', 'Relevant Info', 'Created At', 'Last Updated'
                ])

                for contact in contacts:
                    writer.writerow([
                        contact.name,
                        contact.job_title,
                        contact.company,
                        contact.contact_date.isoformat(),
                        contact.status.value,
                        contact.relevant_info or '',
                        contact.created_at.isoformat(),
                        contact.last_updated.isoformat()
                    ])

            session.close()

            QMessageBox.information(
                self,
                "Success",
                f"Statistics exported to {file_path}"
            )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to export statistics: {str(e)}"
            )

