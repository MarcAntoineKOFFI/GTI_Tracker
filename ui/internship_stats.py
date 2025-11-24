"""
Internship statistics window
"""
import csv
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
from db.models import InternshipApplication, InternshipStatus
from db.session import get_session
from sqlalchemy import func
from utils.date_helpers import get_last_n_weeks
from collections import defaultdict


class InternshipStatsDialog(QDialog):
    """Statistics window for internships"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Internship Statistics")
        self.resize(950, 750)

        self.setup_ui()
        self.load_statistics()

    def setup_ui(self):
        """Setup the UI components"""
        main_layout = QVBoxLayout(self)

        # Title
        title = QLabel("Internship Statistics")
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
            total = session.query(InternshipApplication).count()

            # Active applications
            active = session.query(InternshipApplication).filter(
                InternshipApplication.status.notin_([
                    InternshipStatus.OFFER,
                    InternshipStatus.REJECTED
                ])
            ).count()

            # Offers
            offers = session.query(InternshipApplication).filter_by(
                status=InternshipStatus.OFFER
            ).count()

            # Rejected
            rejected = session.query(InternshipApplication).filter_by(
                status=InternshipStatus.REJECTED
            ).count()

            # Rejection rate
            rejection_rate = (rejected / total * 100) if total > 0 else 0

            # Status counts
            status_counts = {}
            for status in InternshipStatus:
                count = session.query(InternshipApplication).filter_by(
                    status=status
                ).count()
                status_counts[status.value] = count

            # Create sections
            self.create_metrics_section(total, active, offers, rejection_rate)
            self.create_status_chart_section(status_counts)

            # Timeline chart (last 12 weeks)
            all_applications = session.query(InternshipApplication).all()
            self.create_timeline_chart_section(all_applications)

            self.create_funnel_section(status_counts, total)

            # Networking impact
            with_contact = session.query(InternshipApplication).filter(
                InternshipApplication.contact_id.isnot(None)
            ).count()
            without_contact = total - with_contact

            self.create_networking_impact_section(with_contact, without_contact, total)

            # Top companies
            top_companies = session.query(
                InternshipApplication.company,
                func.count(InternshipApplication.id).label('count')
            ).group_by(InternshipApplication.company).order_by(
                func.count(InternshipApplication.id).desc()
            ).limit(10).all()

            self.create_top_companies_section(top_companies)

        finally:
            session.close()

    def create_metrics_section(self, total, active, offers, rejection_rate):
        """Create overall metrics section"""
        group = QGroupBox("Overall Metrics")
        layout = QGridLayout()

        self.add_metric_card(layout, 0, 0, "Total Applications", str(total), "#3498db")
        self.add_metric_card(layout, 0, 1, "Active", str(active), "#2196F3")
        self.add_metric_card(layout, 0, 2, "Offers", str(offers), "#4CAF50")
        self.add_metric_card(layout, 0, 3, "Rejection Rate", f"{rejection_rate:.1f}%", "#F44336")

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

        series = QPieSeries()

        colors = {
            "Applied": QColor("#9E9E9E"),
            "Screening": QColor("#2196F3"),
            "Interview": QColor("#FF9800"),
            "Offer": QColor("#4CAF50"),
            "Rejected": QColor("#F44336")
        }

        for status, count in status_counts.items():
            if count > 0:
                slice = series.append(status, count)
                if status in colors:
                    slice.setColor(colors[status])
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

    def create_timeline_chart_section(self, applications):
        """Create applications over time bar chart"""
        group = QGroupBox("Applications Over Last 12 Weeks")
        layout = QVBoxLayout()

        # Get last 12 weeks
        weeks = get_last_n_weeks(12)

        # Count applications per week
        week_counts = defaultdict(int)
        for app in applications:
            app_date = app.application_date
            for week_start, week_end in weeks:
                if week_start <= app_date <= week_end:
                    week_key = f"{week_start.month}/{week_start.day}"
                    week_counts[week_key] += 1
                    break

        # Create bar chart
        series = QBarSeries()
        bar_set = QBarSet("Applications")
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
        chart.setTitle("Applications Per Week")
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
                f"Average: {avg:.1f} applications/week  |  "
                f"Best week: {best_week} with {best_count} applications"
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
            ("Applied", status_counts.get("Applied", 0)),
            ("Screening", status_counts.get("Screening", 0)),
            ("Interview", status_counts.get("Interview", 0)),
            ("Offer", status_counts.get("Offer", 0))
        ]

        for i, (stage, count) in enumerate(funnel_data):
            percentage = (count / total * 100) if total > 0 else 0

            stage_widget = QWidget()
            stage_layout = QHBoxLayout(stage_widget)

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

    def create_networking_impact_section(self, with_contact, without_contact, total):
        """Create networking impact section"""
        group = QGroupBox("Networking Impact")
        layout = QVBoxLayout()

        # Calculate percentages
        with_pct = (with_contact / total * 100) if total > 0 else 0
        without_pct = (without_contact / total * 100) if total > 0 else 0

        with_label = QLabel(f"Applications with referrals: {with_contact} ({with_pct:.1f}%)")
        with_label.setStyleSheet("font-size: 14px; color: #3498db; padding: 8px;")
        layout.addWidget(with_label)

        without_label = QLabel(f"Applications without referrals: {without_contact} ({without_pct:.1f}%)")
        without_label.setStyleSheet("font-size: 14px; color: #95a5a6; padding: 8px;")
        layout.addWidget(without_label)

        info_label = QLabel("💡 Applications with networking contacts tend to have higher success rates!")
        info_label.setStyleSheet("font-style: italic; color: #7f8c8d; padding: 8px;")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        group.setLayout(layout)
        self.content_layout.addWidget(group)

    def create_top_companies_section(self, top_companies):
        """Create top companies section"""
        group = QGroupBox("Top Target Companies")
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

    def export_csv(self):
        """Export statistics to CSV"""
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Statistics",
            str(Path.home() / "internship_statistics.csv"),
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
                    'Status', 'Job Link', 'Contact ID', 'Notes', 'Last Updated'
                ])

                for internship in internships:
                    writer.writerow([
                        internship.role_name,
                        internship.company,
                        internship.application_date.isoformat(),
                        internship.status.value,
                        internship.job_link or '',
                        internship.contact_id or '',
                        internship.notes or '',
                        internship.last_updated.isoformat()
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

