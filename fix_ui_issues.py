"""
Script to fix multiple UI issues in GTI Tracker
"""
from pathlib import Path

# Fix 1: Toast notifications - add background and move to bottom-left
toast_file = Path(__file__).parent / "ui" / "toast.py"
content = toast_file.read_text(encoding='utf-8')

# Update toast styling: dark background with border
content = content.replace(
    '        self.setStyleSheet(f"""\n            QFrame {{\n                background-color: {bg_color};\n                border-radius: 8px;\n                padding: 0px;\n            }}\n        """)',
    '        self.setStyleSheet(f"""\n            QFrame {{\n                background-color: rgba(26, 32, 44, 0.95);\n                border: 2px solid {bg_color};\n                border-radius: 8px;\n                padding: 0px;\n            }}\n        """)'
)

# Update icon color
content = content.replace(
    '        icon_label.setStyleSheet("""\n            QLabel {\n                color: white;\n                font-size: 20px;\n                font-weight: bold;\n                background: transparent;\n            }\n        """)',
    '        icon_label.setStyleSheet(f"""\n            QLabel {{\n                color: {bg_color};\n                font-size: 20px;\n                font-weight: bold;\n                background: transparent;\n            }}\n        """)'
)

# Move to bottom-left
content = content.replace(
    '    def showEvent(self, event):\n        """Position at top-center of parent"""\n        if self.parent():\n            parent_rect = self.parent().rect()\n            x = (parent_rect.width() - self.width()) // 2\n            y = 20\n            self.move(self.parent().mapToGlobal(self.parent().rect().topLeft()) + QPoint(x, y))',
    '    def showEvent(self, event):\n        """Position at bottom-left of parent"""\n        if self.parent():\n            parent_rect = self.parent().rect()\n            x = 20  # 20px from left edge\n            y = parent_rect.height() - self.height() - 20  # 20px from bottom\n            self.move(self.parent().mapToGlobal(self.parent().rect().topLeft()) + QPoint(x, y))'
)

toast_file.write_text(content, encoding='utf-8')
print("[OK] Fixed toast.py")

# Fix 2: Card buttons - emoji versions with consistent sizing
list_file = Path(__file__).parent / "ui" / "networking_list.py"
content = list_file.read_text(encoding='utf-8')

# View button
content = content.replace(
    '        message_btn = QPushButton("View")\n        message_btn.setToolTip("View Details & Message")\n        message_btn.setFixedSize(70, 32)',
    '        message_btn = QPushButton("\U0001F441\uFE0F")  # Eye emoji\n        message_btn.setToolTip("View Details")\n        message_btn.setFixedSize(60, 32)'
)
content = content.replace('                font-size: 12px;', '                font-size: 16px;', 3)  # First 3 occurrences in button styles

# Edit button
content = content.replace(
    '        edit_btn = QPushButton("Edit")\n        edit_btn.setToolTip("Edit Contact")\n        edit_btn.setFixedSize(60, 32)',
    '        edit_btn = QPushButton("\u270F\uFE0F")  # Pencil emoji\n        edit_btn.setToolTip("Edit Contact")\n        edit_btn.setFixedSize(60, 32)'
)

# Delete button
content = content.replace(
    '        delete_btn = QPushButton("Del")\n        delete_btn.setToolTip("Delete Contact")\n        delete_btn.setFixedSize(50, 32)',
    '        delete_btn = QPushButton("\U0001F5D1\uFE0F")  # Trash emoji\n        delete_btn.setToolTip("Delete Contact")\n        delete_btn.setFixedSize(60, 32)'
)

list_file.write_text(content, encoding='utf-8')
print("[OK] Fixed networking_list.py buttons")

print("\nAll UI fixes applied successfully!")
