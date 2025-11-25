"""
Follow-up Notification Service
Monitors contacts and sends reminders for those needing follow-up
"""
from datetime import date, timedelta
from PySide6.QtCore import QObject, QTimer
from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from db.session import get_session
from db.models import NetworkingContact, NetworkingStatus, Settings
from utils.smart_followup import SmartFollowUpService


class FollowUpNotificationService(QObject):
    """Background service for follow-up notifications"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        
        # Timer to check every hour
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_followups)
        self.timer.start(3600000)  # 1 hour in milliseconds
        
        # System tray icon
        self.tray_icon = None
        self.setup_tray_icon()
        
        # Check immediately on startup
        QTimer.singleShot(5000, self.check_followups)  # 5 second delay after startup
    
    def setup_tray_icon(self):
        """Setup system tray icon"""
        if not QSystemTrayIcon.isSystemTrayAvailable():
            return
        
        self.tray_icon = QSystemTrayIcon(self.parent_window)
        
        # Use app icon or default
        try:
            icon = QIcon("resources/icon.png")
        except:
            icon = self.parent_window.style().standardIcon(self.parent_window.style().SP_MessageBoxInformation)
        
        self.tray_icon.setIcon(icon)
        self.tray_icon.setToolTip("GTI Tracker")
        
        # Create context menu
        tray_menu = QMenu()
        
        show_action = QAction("Show GTI Tracker", self.parent_window)
        show_action.triggered.connect(self.parent_window.show)
        tray_menu.addAction(show_action)
        
        quit_action = QAction("Quit", self.parent_window)
        quit_action.triggered.connect(self.parent_window.close)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Handle tray icon click
        self.tray_icon.activated.connect(self.on_tray_activated)
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.parent_window.show()
            self.parent_window.activateWindow()
    
    def check_followups(self):
        """Check for contacts needing follow-up"""
        session = get_session()
        try:
            # Get follow-up days setting
            settings = session.query(Settings).filter_by(id=1).first()
            follow_up_days = settings.follow_up_days if settings else 3
            
            # Calculate cutoff date
            cutoff_date = date.today() - timedelta(days=follow_up_days)
            
            # Find contacts needing follow-up
            contacts_needing_followup = session.query(NetworkingContact).filter(
                NetworkingContact.status == NetworkingStatus.COLD_MESSAGE,
                NetworkingContact.contact_date <= cutoff_date
            ).all()
            
            count = len(contacts_needing_followup)
            
            if count > 0:
                self.show_notification(count, contacts_needing_followup[:3])  # Show first 3
            
            # Update parent window badge/counter if available
            if hasattr(self.parent_window, 'update_followup_count'):
                self.parent_window.update_followup_count(count)
            
        finally:
            session.close()
    
    def show_notification(self, count, contacts):
        """Show desktop notification"""
        if not self.tray_icon:
            return
        
        title = f"⚠️ {count} Contact{'s' if count > 1 else ''} Need Follow-Up"
        
        # Build message with contact names
        names = [c.name for c in contacts]
        if count > 3:
            message = f"{', '.join(names)}, and {count - 3} more"
        else:
            message = ', '.join(names)
        
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.Warning,
            10000  # Show for 10 seconds
        )
    
    def get_followup_count(self):
        """Get current number of contacts needing follow-up"""
        session = get_session()
        try:
            settings = session.query(Settings).filter_by(id=1).first()
            follow_up_days = settings.follow_up_days if settings else 3
            cutoff_date = date.today() - timedelta(days=follow_up_days)
            
            count = session.query(NetworkingContact).filter(
                NetworkingContact.status == NetworkingStatus.COLD_MESSAGE,
                NetworkingContact.contact_date <= cutoff_date
            ).count()
            
            return count
        finally:
            session.close()
