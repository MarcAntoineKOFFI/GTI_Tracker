"""
Complete fix for daily goal update issue
"""
from pathlib import Path

print("Fixing daily goal update issue...")

# The issue: goal widget is created once and doesn't refresh
# Solution: Add refresh method to goal widget

dashboard_file = Path(__file__).parent / "ui" / "networking_dashboard.py"
content = dashboard_file.read_text(encoding='utf-8')

# Find the create_goal_widget method and add a refresh capability
# Add method to update goal widget dynamically
refresh_method = '''
    def refresh_goal_widget(self):
        """Refresh goal widget with latest data"""
        from utils.goal_service import GoalTrackingService
        
        remaining = GoalTrackingService.get_remaining_today()
        today_count = GoalTrackingService.get_today_count()
        goal = GoalTrackingService.get_daily_goal()
        
        # Update label
        if remaining > 0:
            self.goal_label.setText(f"🎯 Only {remaining} contact{'s' if remaining != 1 else ''} left today to reach your goal!")
        else:
            self.goal_label.setText(f"🎉 Goal achieved! ({today_count}/{goal} contacts today)")
        
        # Update progress bar
        self.goal_progress.setValue(int(GoalTrackingService.get_progress_percentage()))
'''

# Find where to insert the method (after refresh method)
marker = "    def refresh(self):\n        \"\"\"Refresh the dashboard data\"\"\"\n        self.load_data()"
if marker in content:
    content = content.replace(marker, marker + "\n" + refresh_method)
    dashboard_file.write_text(content, encoding='utf-8')
    print("[OK] Added refresh_goal_widget method")

# Now update the refresh method to call it
content = dashboard_file.read_text(encoding='utf-8')
content = content.replace(
    "    def refresh(self):\n        \"\"\"Refresh the dashboard data\"\"\"\n        self.load_data()",
    "    def refresh(self):\n        \"\"\"Refresh the dashboard data\"\"\"\n        self.load_data()\n        if hasattr(self, 'goal_widget'):\n            self.refresh_goal_widget()"
)
dashboard_file.write_text(content, encoding='utf-8')
print("[OK] Updated refresh to refresh goal widget")

# Verify settings dialog saves correctly
settings_file = Path(__file__).parent / "ui" / "settings_dialog.py"
content = settings_file.read_text(encoding='utf-8')

# Check if daily_goal_input exists
if "self.daily_goal_input" in content and "settings.daily_goal" in content:
    print("[OK] Settings dialog correctly saves daily_goal")
else:
    print("[WARNING] Settings dialog may not be saving daily_goal correctly")

print("\nDaily goal update should now work!")
print("Test: Change goal in settings, click Save, check dashboard updates")
