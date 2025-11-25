"""
Add table hover animations and goal tracking widget
"""
from pathlib import Path

print("Adding Priority 1 features...")

# Add table hover styling
list_file = Path(__file__).parent / "ui" / "networking_list.py"
content = list_file.read_text(encoding='utf-8')

# Add hover effect to table stylesheet
if "QTableWidget::item:hover" not in content:
    # Find table stylesheet section
    table_style_marker = "QTableWidget::item {"
    if table_style_marker in content:
        content = content.replace(
            table_style_marker,
            """QTableWidget::item {
            }
            QTableWidget::item:hover {
                background-color: rgba(255, 139, 61, 0.15);
            }
            QTableWidget::item:selected {
                background-color: rgba(255, 139, 61, 0.25);
            }
            QTableWidget::item {"""
        )
        list_file.write_text(content, encoding='utf-8')
        print("[OK] Added table hover animations")
else:
    print("[OK] Table hover already exists")

# Add daily goal field to Settings model
models_file = Path(__file__).parent / "db" / "models.py"
models_content = models_file.read_text(encoding='utf-8')

if "daily_goal" not in models_content:
    # Find Settings class and add daily_goal field
    settings_class_marker = "class Settings(Base):"
    if settings_class_marker in models_content:
        # Find the end of existing fields and add daily_goal
        models_content = models_content.replace(
            "follow_up_days = Column(Integer, default=3)",
            """follow_up_days = Column(Integer, default=3)
    daily_goal = Column(Integer, default=3)  # Daily contact goal"""
        )
        models_file.write_text(models_content, encoding='utf-8')
        print("[OK] Added daily_goal to Settings model")
else:
    print("[OK] daily_goal already exists in Settings")

print("\nPriority 1 utilities complete!")
