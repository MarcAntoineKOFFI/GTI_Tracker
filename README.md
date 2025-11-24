# GTI Tracker - GET-THAT-INTERNSHIP Tracker

A comprehensive desktop application designed to help students manage their internship search through structured networking and application tracking.

## Features

### 🤝 Networking Management
- **Contact Tracking**: Track professionals you've reached out to with detailed information
- **Status Management**: Monitor contacts through stages (Cold message, Has responded, Call, Interview)
- **Follow-up Reminders**: Automatic flagging of contacts needing follow-up
- **Message Generator**: AI-powered networking message templates with customizable placeholders
- **Statistics & Analytics**: Visualize your networking progress with charts and metrics

### 💼 Internship Application Tracking
- **Application Management**: Track all your internship applications in one place
- **Status Tracking**: Monitor applications through the recruitment pipeline
- **Contact Linking**: Link applications to networking contacts to track referral effectiveness
- **Job Link Storage**: Quick access to original job postings
- **Comprehensive Statistics**: Analyze your application success rates and patterns

### 📊 Data-Driven Insights
- **Networking Impact Analysis**: Compare success rates for applications with vs. without referrals
- **Conversion Funnels**: Visualize your progress through networking and interview stages
- **Status Distribution**: See where your efforts are concentrated
- **Export & Import**: CSV export/import for data portability and backups

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python main.py
```

## Project Structure

```
GTI_Tracker/
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── db/                         # Database layer
│   ├── __init__.py
│   ├── models.py              # SQLAlchemy ORM models
│   └── session.py             # Database initialization & session management
│
├── ui/                         # User interface components
│   ├── __init__.py
│   ├── main_window.py         # Main application window
│   ├── networking_dashboard.py   # Networking dashboard view
│   ├── networking_list.py        # Networking contact list
│   ├── networking_dialogs.py     # Add/Edit contact dialogs
│   ├── networking_stats.py       # Networking statistics window
│   ├── internship_dashboard.py   # Internship dashboard view
│   ├── internship_list.py        # Internship application list
│   ├── internship_dialogs.py     # Add/Edit application dialogs
│   ├── internship_stats.py       # Internship statistics window
│   └── settings_dialog.py        # Application settings
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── message_generator.py   # Networking message generation
│   ├── date_helpers.py        # Date formatting and calculations
│   ├── validators.py          # Input validation utilities
│   └── charts.py              # Chart creation helpers
│
├── styles/                     # Stylesheets
│   └── main.qss               # Main application stylesheet
│
└── resources/                  # Resources (icons, images)
    └── __init__.py
```

## Database

The application uses SQLite for data storage, with the database file stored in an OS-appropriate location:

- **Windows**: `%APPDATA%\GTI_Tracker\gti_tracker.db`
- **macOS**: `~/Library/Application Support/GTI_Tracker/gti_tracker.db`
- **Linux**: `~/.local/share/GTI_Tracker/gti_tracker.db`

### Database Schema

**NetworkingContact**
- id (Primary Key)
- name, job_title, company
- contact_date
- relevant_info (notes)
- status (Cold message, Has responded, Call, Interview)
- created_at, last_updated

**InternshipApplication**
- id (Primary Key)
- role_name, company
- job_link (optional URL)
- contact_id (Foreign Key to NetworkingContact)
- application_date
- status (Applied, Screening, Interview, Offer, Rejected)
- notes
- last_updated

**Settings** (singleton)
- message_template
- follow_up_days
- user_name, user_school, user_ambitions

## Usage Guide

### Getting Started

1. **Configure Your Profile**: Go to Settings → Personal Information and fill in your details
2. **Customize Message Template**: In Settings → Message Template, customize your networking outreach template
3. **Start Networking**: Add contacts through the Networking tab
4. **Track Applications**: Add internship applications through the Internships tab

### Networking Workflow

1. **Add a Contact**: Click "Add Networking Activity" to create a new contact
2. **Generate Message**: Open contact details to see the auto-generated networking message
3. **Update Status**: As you receive responses, update the contact's status
4. **Follow Up**: The app will flag contacts that need follow-up based on your settings

### Application Tracking Workflow

1. **Add Application**: Click "Add Internship Application" to log a new application
2. **Link Contact** (Optional): Link the application to a networking contact if referred
3. **Track Progress**: Update the status as you move through the interview process
4. **Analyze Success**: View statistics to see which strategies are working

### Keyboard Shortcuts

- **Ctrl+N**: Add new contact (when in Networking view)
- **Ctrl+F**: Focus search field
- **Double-click row**: Open detail view

## Data Management

### Export Data
- Export contacts to CSV
- Export applications to CSV
- Export entire database for backup

### Import Data
- Import contacts from CSV
- Import applications from CSV

### Backup & Restore
Use Settings → Data Management → Export Full Database to create backups

## Customization

### Message Templates

Customize your networking message template with these placeholders:
- `{name}` - Contact's name
- `{job_title}` - Contact's job title
- `{company}` - Contact's company
- `{user_name}` - Your name
- `{user_school}` - Your university
- `{user_ambitions}` - Your career ambitions
- `{relevant_info}` - Contact-specific notes

### Follow-up Settings

Adjust the number of days before flagging contacts for follow-up in Settings → Notifications & Reminders

## Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check the console for error messages

### Database errors
- The app creates the database automatically on first run
- If issues persist, delete the database file and restart the app (WARNING: this deletes all data)

### UI issues
- Try resizing the window
- Check that PySide6 is properly installed
- Restart the application

## Contributing

This is a student project. Feel free to fork and customize for your needs!

## License

This project is provided as-is for educational and personal use.

## Credits

Developed as a comprehensive internship tracking solution for students.

---

**Version**: 1.0.0  
**Built with**: Python, PySide6, SQLAlchemy

