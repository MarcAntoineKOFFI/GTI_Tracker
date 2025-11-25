"""
Fix table row height - increase to 80px for full visibility
"""
from pathlib import Path

list_file = Path(__file__).parent / "ui" / "networking_list.py"
content = list_file.read_text(encoding='utf-8')

# Replace the row height setting
content = content.replace(
    '        # Set generous row height for breathing room\n        self.table.verticalHeader().setDefaultSectionSize(50)  # 50px row height\n        self.table.verticalHeader().setMinimumSectionSize(45)',
    '        # Set very generous row height for full visibility\n        self.table.verticalHeader().setDefaultSectionSize(80)  # 80px row height\n        self.table.verticalHeader().setMinimumSectionSize(70)'
)

list_file.write_text(content, encoding='utf-8')
print("[OK] Increased table row height to 80px!")
