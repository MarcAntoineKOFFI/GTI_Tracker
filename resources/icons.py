"""
Application icon and resource utilities
"""
from pathlib import Path
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt, QRect


def create_app_icon() -> QIcon:
    """
    Create a simple application icon programmatically

    Returns:
        QIcon object for the application
    """
    # Create a pixmap for the icon (256x256 for high quality)
    size = 256
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)

    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)

    # Draw background circle (blue)
    painter.setBrush(QColor("#3498db"))
    painter.setPen(Qt.NoPen)
    painter.drawEllipse(8, 8, size-16, size-16)

    # Draw GTI text
    painter.setPen(QColor("white"))
    font = QFont("Arial", 90, QFont.Bold)
    painter.setFont(font)

    text_rect = QRect(0, 60, size, 100)
    painter.drawText(text_rect, Qt.AlignCenter, "GTI")

    # Draw smaller "Tracker" text
    font.setPointSize(40)
    font.setWeight(QFont.Normal)
    painter.setFont(font)

    text_rect2 = QRect(0, 150, size, 60)
    painter.drawText(text_rect2, Qt.AlignCenter, "Tracker")

    painter.end()

    return QIcon(pixmap)


def get_resource_path(resource_name: str) -> Path:
    """
    Get path to a resource file

    Args:
        resource_name: Name of the resource file

    Returns:
        Path to the resource
    """
    return Path(__file__).parent / resource_name

