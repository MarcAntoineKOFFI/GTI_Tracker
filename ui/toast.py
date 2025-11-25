"""
Toast Notification System
User-friendly success/error messages instead of QMessageBox
"""
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QFrame
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property, QPoint
from PySide6.QtGui import QFont


class Toast(QFrame):
    """Modern toast notification"""

    def __init__(self, message: str, toast_type: str = "success", parent=None, duration: int = 3000):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_DeleteOnClose)

        # Style based on type
        if toast_type == "success":
            bg_color = "#00D97E"
            icon = "✓"
        elif toast_type == "error":
            bg_color = "#FF4757"
            icon = "⚠"
        elif toast_type == "info":
            bg_color = "#4A9EFF"
            icon = "ℹ"
        else:
            bg_color = "#FFB020"
            icon = "⚡"

        self.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(26, 32, 44, 0.95);
                border: 2px solid {bg_color};
                border-radius: 8px;
                padding: 0px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(12)

        # Icon
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            QLabel {{
                color: {bg_color};
                font-size: 20px;
                font-weight: bold;
                background: transparent;
            }}
        """)
        layout.addWidget(icon_label)

        # Message
        msg_label = QLabel(message)
        msg_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: 500;
                background: transparent;
            }
        """)
        msg_label.setWordWrap(False)
        layout.addWidget(msg_label)

        # Set fixed size based on content
        self.adjustSize()
        self.setFixedSize(self.sizeHint())

        # Auto-hide after duration
        QTimer.singleShot(duration, self.fade_out)

        # Fade in animation
        self.setWindowOpacity(0)
        self.fade_in()

    def fade_in(self):
        """Fade in animation"""
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.start()

    def fade_out(self):
        """Fade out and close"""
        anim = QPropertyAnimation(self, b"windowOpacity")
        anim.setDuration(200)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setEasingCurve(QEasingCurve.InCubic)
        anim.finished.connect(self.close)
        anim.start()

    def showEvent(self, event):
        """Position at bottom-left of parent"""
        if self.parent():
            parent_rect = self.parent().rect()
            x = 20  # 20px from left edge
            y = parent_rect.height() - self.height() - 20  # 20px from bottom
            self.move(self.parent().mapToGlobal(self.parent().rect().topLeft()) + QPoint(x, y))
        super().showEvent(event)


def show_success(parent, message: str):
    """Show success toast"""
    toast = Toast(message, "success", parent)
    toast.show()


def show_error(parent, message: str):
    """Show error toast"""
    toast = Toast(message, "error", parent)
    toast.show()


def show_info(parent, message: str):
    """Show info toast"""
    toast = Toast(message, "info", parent)
    toast.show()


def show_warning(parent, message: str):
    """Show warning toast"""
    toast = Toast(message, "warning", parent)
    toast.show()

