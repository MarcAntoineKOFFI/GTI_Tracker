"""
Update notification service and dashboard to use smart follow-up logic
"""
from pathlib import Path

print("Integrating smart follow-up logic...")

# 1. Update notification service to use smart logic
notif_file = Path(__file__).parent / "utils" / "notification_service.py"
content = notif_file.read_text(encoding='utf-8')

# Replace old follow-up logic with smart logic
content = content.replace(
    "from db.models import NetworkingContact, NetworkingStatus, Settings",
    "from db.models import NetworkingContact, NetworkingStatus, Settings\nfrom utils.smart_followup import SmartFollowUpService"
)

content = content.replace(
    "        # Check for contacts needing follow-up\n        settings = session.query(Settings).filter_by(id=1).first()\n        follow_up_days = settings.follow_up_days if settings else 3\n        \n        cutoff_date = date.today() - timedelta(days=follow_up_days)\n        followup_contacts = session.query(NetworkingContact).filter(\n            NetworkingContact.status == NetworkingStatus.COLD_MESSAGE,\n            NetworkingContact.contact_date <= cutoff_date\n        ).all()",
    "        # Check for contacts needing follow-up using smart logic\n        followup_contacts = SmartFollowUpService.get_followup_contacts()"
)

notif_file.write_text(content, encoding='utf-8')
print("[OK] Updated notification service with smart follow-up")

# 2. Update dashboard to use smart logic
dashboard_file = Path(__file__).parent / "ui" / "networking_dashboard.py"
content = dashboard_file.read_text(encoding='utf-8')

# Replace follow-up count logic
old_import = "from db.models import NetworkingContact, NetworkingStatus"
new_import = "from db.models import NetworkingContact, NetworkingStatus\nfrom utils.smart_followup import SmartFollowUpService"

if old_import in content and new_import not in content:
    content = content.replace(old_import, new_import)

# Replace the follow-up count calculation
old_calc = """            # Follow-up count
            settings = session.query(Settings).filter_by(id=1).first()
            follow_up_days = settings.follow_up_days if settings else 3

            cutoff_date = date.today() - timedelta(days=follow_up_days)
            followup_count = session.query(NetworkingContact).filter(
                NetworkingContact.status == NetworkingStatus.COLD_MESSAGE,
                NetworkingContact.contact_date <= cutoff_date
            ).count()"""

new_calc = """            # Follow-up count using smart logic
            followup_count = SmartFollowUpService.get_followup_count()"""

if old_calc in content:
    content = content.replace(old_calc, new_calc)

dashboard_file.write_text(content, encoding='utf-8')
print("[OK] Updated dashboard with smart follow-up count")

print("\nSmart follow-up integration complete!")
