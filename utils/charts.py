"""
Chart creation utilities
"""
from typing import Optional
from PySide6.QtCharts import QChart, QBarSet, QBarSeries, QPieSeries, QLineSeries
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtCore import Qt


def create_bar_chart(
    data: dict[str, int],
    title: str = "",
    x_label: str = "",
    y_label: str = ""
) -> QChart:
    """
    Create a bar chart

    Args:
        data: Dictionary mapping labels to values
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label

    Returns:
        QChart object
    """
    series = QBarSeries()
    bar_set = QBarSet("Data")

    for value in data.values():
        bar_set.append(value)

    series.append(bar_set)

    chart = QChart()
    chart.addSeries(series)
    chart.setTitle(title)
    chart.setAnimationOptions(QChart.SeriesAnimations)

    return chart


def create_pie_chart(
    data: dict[str, int],
    title: str = "",
    colors: Optional[dict[str, QColor]] = None
) -> QChart:
    """
    Create a pie chart

    Args:
        data: Dictionary mapping labels to values
        title: Chart title
        colors: Optional dictionary mapping labels to colors

    Returns:
        QChart object
    """
    series = QPieSeries()

    for label, value in data.items():
        slice = series.append(label, value)
        if colors and label in colors:
            slice.setColor(colors[label])
        slice.setLabelVisible(True)

    chart = QChart()
    chart.addSeries(series)
    chart.setTitle(title)
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.legend().setAlignment(Qt.AlignBottom)

    return chart


def create_line_chart(
    data: dict[str, float],
    title: str = "",
    color: Optional[QColor] = None
) -> QChart:
    """
    Create a line chart

    Args:
        data: Dictionary mapping x-values (labels) to y-values
        title: Chart title
        color: Line color

    Returns:
        QChart object
    """
    series = QLineSeries()

    for i, (label, value) in enumerate(data.items()):
        series.append(i, value)

    chart = QChart()
    chart.addSeries(series)
    chart.setTitle(title)
    chart.setAnimationOptions(QChart.SeriesAnimations)
    chart.createDefaultAxes()

    if color:
        pen = QPen(color)
        pen.setWidth(2)
        series.setPen(pen)

    return chart


def get_status_colors() -> dict[str, str]:
    """
    Get standard status colors for the application

    Returns:
        Dictionary mapping status names to hex color codes
    """
    return {
        # Networking statuses
        "Cold message": "#9E9E9E",
        "Has responded": "#2196F3",
        "Call": "#FF9800",
        "Interview": "#4CAF50",

        # Internship statuses
        "Applied": "#9E9E9E",
        "Screening": "#2196F3",
        "Offer": "#4CAF50",
        "Rejected": "#F44336"
    }

