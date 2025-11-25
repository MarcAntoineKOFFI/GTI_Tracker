"""
Email Client Integration Service
Detects installed email clients and creates draft emails
"""
import webbrowser
import urllib.parse
import platform
import subprocess
from pathlib import Path


class EmailIntegrationService:
    
    @staticmethod
    def detect_email_client() -> str:
        """Detect available email client"""
        system = platform.system()
        
        if system == "Windows":
            # Check for Outlook
            outlook_path = Path("C:/Program Files/Microsoft Office/root/Office16/OUTLOOK.EXE")
            if outlook_path.exists():
                return "outlook"
        
        # Default to mailto (opens default email client)
        return "mailto"
    
    @staticmethod
    def create_email_draft(to_email: str, subject: str = "", body: str = ""):
        """Create email draft in default client"""
        if not to_email:
            return False
        
        # Build mailto URL
        params = {}
        if subject:
            params['subject'] = subject
        if body:
            params['body'] = body
        
        param_string = urllib.parse.urlencode(params)
        mailto_url = f"mailto:{to_email}"
        if param_string:
            mailto_url += f"?{param_string}"
        
        try:
            webbrowser.open(mailto_url)
            return True
        except:
            return False
    
    @staticmethod
    def email_contact(contact_name: str, contact_email: str, template: str = "follow_up"):
        """Open email draft for a contact with template"""
        templates = {
            "follow_up": {
                "subject": f"Following up - {contact_name}",
                "body": f"Hi {contact_name.split()[0]},\\n\\nI wanted to follow up on our previous conversation...\\n\\nBest regards"
            },
            "introduction": {
                "subject": f"Introduction",
                "body": f"Hi {contact_name.split()[0]},\\n\\nI hope this email finds you well...\\n\\nBest regards"
            },
            "thank_you": {
                "subject": "Thank you",
                "body": f"Hi {contact_name.split()[0]},\\n\\nThank you for taking the time to speak with me...\\n\\nBest regards"
            }
        }
        
        template_data = templates.get(template, templates["follow_up"])
        return EmailIntegrationService.create_email_draft(
            contact_email,
            template_data["subject"],
            template_data["body"]
        )
