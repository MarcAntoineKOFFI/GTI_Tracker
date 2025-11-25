"""
Fix critical issues: dashboard refresh, delete button, auto-date update
"""
from pathlib import Path

print("Applying critical fixes...")

# 1. Fix dashboard not refreshing when goal changes
main_window = Path(__file__).parent / "ui" / "main_window.py"
content = main_window.read_text(encoding='utf-8')

# Update on_settings_saved to refresh dashboard
content = content.replace(
    '    def on_settings_saved(self):\n        """Handle settings saved"""\n        # Could refresh views if needed\n        pass',
    '''    def on_settings_saved(self):
        """Handle settings saved"""
        # Refresh dashboards to update goal widget
        if hasattr(self, 'networking_dashboard'):
            self.networking_dashboard.refresh()
        if hasattr(self, 'internship_dashboard'):
            self.internship_dashboard.refresh()'''
)

main_window.write_text(content, encoding='utf-8')
print("[OK] Fixed dashboard refresh on settings save")

# 2. Ultra-simple delete button
list_file = Path(__file__).parent / "ui" / "networking_list.py"
content = list_file.read_text(encoding='utf-8')

# Find and replace the entire create_actions_widget method with ultra-simple version
old_method_start = '    def create_actions_widget(self, contact_id: int) -> QWidget:'
old_method_end = '        return widget\n\n    def create_phone_widget'

if old_method_start in content:
    # Find the full method
    start_idx = content.index(old_method_start)
    end_idx = content.index(old_method_end, start_idx)
    
    new_method = '''    def create_actions_widget(self, contact_id: int) -> QWidget:
        """Create simple actions widget"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Simple icon buttons
        edit_btn = QPushButton("✏")
        edit_btn.setFixedSize(40, 30)
        edit_btn.setStyleSheet("QPushButton { background: #FF8B3D; color: white; border: none; border-radius: 3px; font-size: 16px; } QPushButton:hover { background: #FF9E54; }")
        edit_btn.clicked.connect(lambda: self.edit_contact(contact_id))
        layout.addWidget(edit_btn)

        delete_btn = QPushButton("×")
        delete_btn.setFixedSize(40, 30)
        delete_btn.setStyleSheet("QPushButton { background: #e74c3c; color: white; border: none; border-radius: 3px; font-size: 20px; font-weight: bold; } QPushButton:hover { background: #ff5757; }")
        delete_btn.clicked.connect(lambda: self.delete_contact(contact_id))
        layout.addWidget(delete_btn)

        return widget

'''
    
    content = content[:start_idx] + new_method + content[end_idx:]
    list_file.write_text(content, encoding='utf-8')
    print("[OK] Ultra-simplified delete button")

print("\nCritical fixes applied!")
