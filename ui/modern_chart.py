"""
Custom Modern Bar Chart with rounded corners, labels, and tooltips
"""
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QBrush


class ModernBarChart(QWidget):
    """Modern bar chart with rounded corners, top labels, and hover tooltips"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = {}
        self.hovered_bar = -1
        self.setMouseTracking(True)
        self.setMinimumHeight(260)
        
    def set_data(self, data: dict):
        """Set chart data {label: value}"""
        self.data = data
        self.update()
    
    def paintEvent(self, event):
        if not self.data:
            return
            
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Chart dimensions
        width = self.width()
        height = self.height()
        padding = 40
        chart_height = height - padding * 2
        chart_width = width - padding * 2
        
        labels = list(self.data.keys())
        values = list(self.data.values())
        max_value = max(values) if values else 1
        
        # Bar dimensions
        bar_count = len(labels)
        bar_width = (chart_width / bar_count) * 0.7
        bar_spacing = chart_width / bar_count
        
        for i, (label, value) in enumerate(self.data.items()):
            # Calculate bar position and height
            x = padding + i * bar_spacing + (bar_spacing - bar_width) / 2
            bar_height = (value / max_value) * chart_height if max_value > 0 else 0
            y = height - padding - bar_height
            
            # Rounded rectangle for bar
            rect = QRectF(x, y, bar_width, bar_height)
            
            # Color - orange, brighter on hover
            if i == self.hovered_bar:
                color = QColor("#FF9E54")
            else:
                color = QColor("#FF8B3D")
            
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, 6, 6)
            
            # Draw value on top of bar
            if value > 0:
                painter.setPen(QPen(QColor("#FFFFFF")))
                font = QFont("Inter", 12, QFont.Bold)
                painter.setFont(font)
                value_text = str(int(value))
                text_rect = QRectF(x, y - 25, bar_width, 20)
                painter.drawText(text_rect, Qt.AlignCenter, value_text)
            
            # Draw label below chart
            painter.setPen(QPen(QColor("#9BA3B1")))
            font = QFont("Inter", 10)
            painter.setFont(font)
            label_rect = QRectF(x, height - padding + 10, bar_width, 20)
            painter.drawText(label_rect, Qt.AlignCenter, label)
    
    def mouseMoveEvent(self, event):
        """Handle mouse hover for tooltips"""
        if not self.data:
            return
            
        width = self.width()
        padding = 40
        chart_width = width - padding * 2
        
        bar_count = len(self.data)
        bar_spacing = chart_width / bar_count
        
        # Find which bar is hovered
        mouse_x = event.pos().x()
        old_hovered = self.hovered_bar
        self.hovered_bar = -1
        
        for i in range(bar_count):
            bar_start = padding + i * bar_spacing
            bar_end = bar_start + bar_spacing
            if bar_start <= mouse_x <= bar_end:
                self.hovered_bar = i
                break
        
        # Update if hover changed
        if old_hovered != self.hovered_bar:
            self.update()
            
        # Set tooltip
        if self.hovered_bar >= 0:
            labels = list(self.data.keys())
            values = list(self.data.values())
            label = labels[self.hovered_bar]
            value = int(values[self.hovered_bar])
            self.setToolTip(f"{label}: {value} contact{'s' if value != 1 else ''}")
        else:
            self.setToolTip("")
    
    def leaveEvent(self, event):
        """Clear hover when mouse leaves"""
        if self.hovered_bar >= 0:
            self.hovered_bar = -1
            self.update()
