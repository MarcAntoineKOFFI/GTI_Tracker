"""
Empty state component for when no data exists
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal


class EmptyState(QWidget):
    """Professional empty state widget"""

    action_clicked = Signal()

    def __init__(self, icon: str, title: str, subtitle: str,
                 action_text: str = None, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # Icon/Illustration
        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.3);
                font-size: 64px;
                background: transparent;
            }
        """)
        layout.addWidget(icon_label)

        # Title
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 24px;
                font-weight: 600;
                background: transparent;
            }
        """)
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel(subtitle)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setWordWrap(True)
        subtitle_label.setMaximumWidth(500)
        subtitle_label.setStyleSheet("""
            QLabel {
                color: #9BA3B1;
                font-size: 14px;
                background: transparent;
            }
        """)
        layout.addWidget(subtitle_label)

        # Action button (optional)
        if action_text:
            self.action_button = QPushButton(action_text)
            self.action_button.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #FF8B3D, stop:1 #FF7035);
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
                                                stop:0 #FFA04D, stop:1 #FF8545);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #E67A2D, stop:1 #E66025);
                }
            """)
            self.action_button.clicked.connect(self.action_clicked.emit)
            layout.addWidget(self.action_button, alignment=Qt.AlignCenter)
        else:
            self.action_button = None

