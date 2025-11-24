"""
Professional UI components for GAFAM-level experience
Loading states, progress indicators, and microinteractions
"""
from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QProgressBar, QPushButton, QFrame
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPainter, QColor, QPen
import math


class LoadingSpinner(QWidget):
    """Elegant loading spinner with smooth animation"""

    def __init__(self, size: int = 32, color: str = "#FF8B3D", parent=None):
        super().__init__(parent)
        self.size = size
        self.color = QColor(color)
        self.angle = 0

        self.setFixedSize(size, size)

        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)  # 20 FPS

    def rotate(self):
        """Rotate the spinner"""
        self.angle = (self.angle + 15) % 360
        self.update()

    def paintEvent(self, event):
        """Paint the spinner"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw arc
        pen = QPen(self.color, 3, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)

        rect = self.rect().adjusted(2, 2, -2, -2)
        painter.drawArc(rect, self.angle * 16, 120 * 16)

    def stop(self):
        """Stop the spinner animation"""
        self.timer.stop()

    def start(self):
        """Start the spinner animation"""
        self.timer.start(50)


class LoadingOverlay(QWidget):
    """Full-screen loading overlay with spinner and message"""

    def __init__(self, message: str = "Loading...", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_StyledBackground)

        # Semi-transparent dark background
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(11, 14, 29, 0.85);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        # Spinner
        self.spinner = LoadingSpinner(48, "#FF8B3D")
        layout.addWidget(self.spinner, alignment=Qt.AlignCenter)

        # Message
        self.message_label = QLabel(message)
        self.message_label.setStyleSheet("""
            QLabel {
                color: #E8EAED;
                font-size: 16px;
                font-weight: 500;
                margin-top: 16px;
            }
        """)
        self.message_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.message_label)

    def set_message(self, message: str):
        """Update the loading message"""
        self.message_label.setText(message)

    def showEvent(self, event):
        """Center on parent when shown"""
        if self.parent():
            self.setGeometry(self.parent().rect())
        super().showEvent(event)


class SuccessToast(QWidget):
    """Toast notification for success messages"""

    def __init__(self, message: str, duration: int = 3000, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Container with rounded corners and shadow
        container = QFrame(self)
        container.setStyleSheet("""
            QFrame {
                background-color: #00D97E;
                border-radius: 8px;
                padding: 12px 20px;
            }
        """)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 12, 16, 12)

        # Success icon (checkmark)
        icon_label = QLabel("✓")
        icon_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        layout.addWidget(icon_label)

        # Message
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        layout.addWidget(message_label)

        # Set container size
        container.adjustSize()
        self.setFixedSize(container.size())

        # Auto-hide after duration
        QTimer.singleShot(duration, self.fade_out)

        # Fade in animation
        self.opacity = 0.0
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
        """Position at top-center of parent"""
        if self.parent():
            parent_rect = self.parent().rect()
            x = (parent_rect.width() - self.width()) // 2
            y = 20  # 20px from top
            self.move(x, y)
        super().showEvent(event)


class ErrorToast(QWidget):
    """Toast notification for error messages"""

    def __init__(self, message: str, duration: int = 5000, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        container = QFrame(self)
        container.setStyleSheet("""
            QFrame {
                background-color: #FF4757;
                border-radius: 8px;
                padding: 12px 20px;
            }
        """)

        layout = QHBoxLayout(container)
        layout.setContentsMargins(16, 12, 16, 12)

        # Error icon
        icon_label = QLabel("⚠")
        icon_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        layout.addWidget(icon_label)

        # Message
        message_label = QLabel(message)
        message_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: 500;
            }
        """)
        message_label.setWordWrap(True)
        message_label.setMaximumWidth(400)
        layout.addWidget(message_label)

        container.adjustSize()
        self.setFixedSize(container.size())

        QTimer.singleShot(duration, self.fade_out)

        # Fade in
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
        """Position at top-center of parent"""
        if self.parent():
            parent_rect = self.parent().rect()
            x = (parent_rect.width() - self.width()) // 2
            y = 20
            self.move(x, y)
        super().showEvent(event)


class ProgressButton(QPushButton):
    """Button that shows progress state"""

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        self.default_text = text
        self.spinner = None
        self.is_loading = False

    def set_loading(self, loading: bool, text: str = "Saving..."):
        """Set loading state"""
        self.is_loading = loading
        self.setEnabled(not loading)

        if loading:
            self.setText(f"⏳ {text}")
        else:
            self.setText(self.default_text)

    def set_success(self, duration: int = 1500):
        """Show success state briefly"""
        self.setText("✓ Saved!")
        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                            stop:0 #00D97E, stop:1 #00E98E);
                color: white;
            }
        """)

        # Reset after duration
        QTimer.singleShot(duration, self._reset)

    def _reset(self):
        """Reset to default state"""
        self.setText(self.default_text)
        self.setStyleSheet("")  # Clear inline style


class EmptyState(QWidget):
    """Professional empty state with illustration and CTA"""

    def __init__(self, title: str, subtitle: str, icon: str = "📭",
                 action_text: str = None, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Icon/Illustration
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        font = icon_label.font()
        font.setPointSize(64)
        icon_label.setFont(font)
        icon_label.setStyleSheet("color: #9BA3B1;")
        layout.addWidget(icon_label)

        # Title
        title_label = QLabel(title)
        title_label.setProperty("class", "heading-2")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #E8EAED;
                font-size: 24px;
                font-weight: 600;
            }
        """)
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setProperty("class", "secondary-text")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        subtitle_label.setMaximumWidth(500)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #9BA3B1;
                font-size: 14px;
            }
        """)
        layout.addWidget(subtitle_label)

        # Action button (optional)
        if action_text:
            self.action_button = QPushButton(action_text)
            self.action_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #FF8B3D, stop:1 #FF9E54);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 32px;
                    font-size: 15px;
                    font-weight: 600;
                    min-width: 200px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #FFA04D, stop:1 #FFB064);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #E67A2D, stop:1 #E68E44);
                }
            """)
            layout.addWidget(self.action_button, alignment=Qt.AlignCenter)
        else:
            self.action_button = None


class SkeletonLoader(QWidget):
    """Skeleton loading placeholder for content"""

    def __init__(self, width: int, height: int, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)

        # Animated shimmer effect
        self.shimmer_pos = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_shimmer)
        self.timer.start(50)

    def update_shimmer(self):
        """Update shimmer animation"""
        self.shimmer_pos = (self.shimmer_pos + 5) % (self.width() + 100)
        self.update()

    def paintEvent(self, event):
        """Paint skeleton with shimmer"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Base color
        painter.fillRect(self.rect(), QColor("#272D3D"))

        # Shimmer gradient
        gradient_width = 100
        x = self.shimmer_pos - gradient_width

        for i in range(gradient_width):
            alpha = int(30 * math.sin(math.pi * i / gradient_width))
            color = QColor(255, 255, 255, alpha)
            painter.setPen(QPen(color, 1))
            painter.drawLine(x + i, 0, x + i, self.height())

