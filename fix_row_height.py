"""
Quick fix: Increase table row height so buttons and status are fully visible
"""
from pathlib import Path

list_file = Path(__file__).parent / "ui" / "networking_list.py"
content = list_file.read_text(encoding='utf-8')

# Add row height setting after the table setup
insert_after = "        self.table.cellDoubleClicked.connect(self.on_row_double_clicked)"
new_code = """        self.table.cellDoubleClicked.connect(self.on_row_double_clicked)
        
        # Set generous row height for breathing room
        self.table.verticalHeader().setDefaultSectionSize(50)  # 50px row height
        self.table.verticalHeader().setMinimumSectionSize(45)"""

content = content.replace(insert_after, new_code)

list_file.write_text(content, encoding='utf-8')
print("[OK] Increased table row height to 50px for better visibility!")
