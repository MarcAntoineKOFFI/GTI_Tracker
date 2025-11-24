# GTI Tracker - GET-THAT-INTERNSHIP Tracker

<div align="center">

**A comprehensive desktop application designed to help students systematically manage their internship search through structured networking and application tracking.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PySide6](https://img.shields.io/badge/PySide6-6.6+-green.svg)](https://pypi.org/project/PySide6/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## ✨ Features Overview

GTI Tracker transforms the chaotic internship search process into a systematic, data-driven approach with actionable insights and clear organizational structures.

### 🤝 Networking Management

#### Core Features
- **📋 Contact Tracking**: Store and organize every professional you reach out to with comprehensive details
  - Name, job title, company, and contact date
  - Relevant information field for connection points and shared interests
  - Automatic timestamp tracking (created and last updated)
  
- **📊 Status Management**: Monitor relationship progression through four stages
  - **Cold message** - Initial outreach sent
  - **Has responded** - Professional replied
  - **Call** - Phone/video conversation scheduled or completed
  - **Interview** - Interview opportunity secured
  
- **⏰ Follow-up Reminders**: Never miss a networking opportunity
  - Automatic flagging of contacts needing follow-up (configurable threshold, default 3 days)
  - Visual indicators for contacts requiring attention
  - Quick filter to view all follow-up needed contacts
  
- **✉️ Message Generator**: Create personalized networking messages instantly
  - Customizable templates with dynamic placeholders
  - Preview functionality to see generated messages
  - One-click copy to clipboard
  - Placeholders: {name}, {job_title}, {company}, {user_name}, {user_school}, {user_ambitions}, {relevant_info}
  
- **📈 Statistics & Analytics**: 
  - Total contacts and status distribution
  - Contacts per week over last 12 weeks (bar chart)
  - Conversion funnel visualization
  - Response rate analysis
  - Top companies contacted
  - CSV export for detailed reporting

### 💼 Internship Application Tracking

#### Core Features
- **📝 Application Management**: Centralized tracking for all applications
  - Role name, company, and application date
  - Optional job posting URL with test link functionality
  - Notes field for interview details, salary info, etc.
  - Link applications to networking contacts
  
- **🔄 Status Tracking**: Monitor applications through five stages
  - **Applied** - Application submitted
  - **Screening** - Recruiter reviewing or phone screen
  - **Interview** - Interview rounds in progress
  - **Offer** - Offer received
  - **Rejected** - Application unsuccessful
  
- **🔗 Contact Linking**: Connect applications to networking relationships
  - Track which applications came through referrals
  - Quickly navigate between linked contacts and applications
  - Measure networking impact on success rates
  
- **🌐 Job Link Storage**: 
  - Store URLs to original job postings
  - Test links before saving
  - Quick access to job descriptions
  
- **📊 Comprehensive Statistics**:
  - Total applications, active applications, and offers
  - Rejection rate calculation
  - Applications per week over last 12 weeks (timeline chart)
  - Status distribution (pie chart)
  - Conversion funnel (Applied → Screening → Interview → Offer)
  - Networking impact comparison
  - Top target companies
  - CSV export functionality

### 📊 Data-Driven Insights

#### Advanced Analytics
- **🎯 Networking Impact Analysis**: 
  - Compare success rates for applications with vs. without referrals
  - Quantify the value of networking efforts
  - Data-driven motivation to build relationships
  
- **📈 Conversion Funnels**: 
  - Visualize progression through networking stages
  - Track application pipeline advancement
  - Identify bottlenecks in your process
  
- **📉 Status Distribution Charts**: 
  - Pie charts showing where contacts/applications stand
  - Understand where to focus efforts
  
- **📅 Timeline Tracking**:
  - Weekly bar charts for both networking and applications
  - Identify productivity patterns
  - Track consistency over time
  
- **💾 Export & Import**: 
  - CSV export for contacts and applications
  - Full database backup capability
  - Import historical data
  - Share data across devices

### ⚙️ Settings & Customization

- **👤 Personal Information**: Configure your name, school, and career ambitions
- **✉️ Message Templates**: Fully customizable networking message templates
- **🔔 Notifications**: Adjustable follow-up reminder threshold
- **📦 Data Management**: Import/export capabilities and database reset options

### ⌨️ Keyboard Shortcuts

- `Ctrl+N` - Add new contact/application (context-aware)
- `Ctrl+F` - Focus search field in list views
- `Ctrl+,` - Open settings
- `Ctrl+1` - Switch to Networking tab
- `Ctrl+2` - Switch to Internships tab
- `Esc` - Close dialogs

---

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

Adjust the number of days before flagging contacts for follow-up in Settings → Notifications & Reminders (default: 3 days)

---

## 🗂️ Project Structure

```
GTI_Tracker/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── FEATURES.md                  # Detailed feature documentation
├── QUICKSTART.md               # Quick start guide
├── test_components.py          # Component tests
│
├── db/                         # Database layer
│   ├── models.py               # SQLAlchemy ORM models
│   └── session.py              # Database session management
│
├── ui/                         # User interface components
│   ├── main_window.py          # Main application window
│   ├── networking_dashboard.py # Networking dashboard
│   ├── networking_list.py      # Contact list view
│   ├── networking_dialogs.py   # Contact dialogs
│   ├── networking_stats.py     # Networking statistics
│   ├── internship_dashboard.py # Internship dashboard
│   ├── internship_list.py      # Application list view
│   ├── internship_dialogs.py   # Application dialogs
│   ├── internship_stats.py     # Internship statistics
│   └── settings_dialog.py      # Settings dialog
│
├── utils/                      # Utility functions
│   ├── charts.py               # Chart helpers
│   ├── date_helpers.py         # Date utilities
│   ├── message_generator.py   # Message templates
│   └── validators.py           # Input validation
│
├── resources/                  # Application resources
│   └── icons.py                # Icon generation
│
└── styles/                     # Stylesheets
    └── main.qss                # Qt stylesheet
```

---

## 💾 Data Storage

### Database Location

The SQLite database is stored at OS-appropriate locations:

- **Windows**: `%APPDATA%\GTI_Tracker\gti_tracker.db`
- **macOS**: `~/Library/Application Support/GTI_Tracker/gti_tracker.db`
- **Linux**: `~/.local/share/GTI_Tracker/gti_tracker.db`

### Backup Your Data

**Recommended**: Settings → Data Management → "Export Full Database"

**Manual Backup**: Copy the `gti_tracker.db` file to a safe location

---

## 🐛 Troubleshooting

### Application won't start
- Ensure Python 3.8+ is installed: `python --version`
- Verify dependencies: `pip install -r requirements.txt`
- Check terminal for error messages

### Database errors
- Database is created automatically on first run
- To reset: Settings → Data Management → Reset All Data (⚠️ deletes all data!)
- Always backup before resetting

### UI issues
- Application supports high-DPI displays automatically
- Try resizing the window or restarting the application
- Verify PySide6 installation: `pip show PySide6`

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs via GitHub Issues
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

This project is provided as-is for educational and personal use under the MIT License.

---

## 🙏 Acknowledgments

- Built with [PySide6](https://pypi.org/project/PySide6/) - Qt for Python
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python SQL toolkit
- Designed to empower students in their internship search journey

---

## 📧 Support

For help and documentation:
- Check [FEATURES.md](FEATURES.md) for detailed features
- Review [QUICKSTART.md](QUICKSTART.md) for quick tips  
- Open GitHub Issues for bug reports

---

<div align="center">

**Version 1.0.0**  
**Made with ❤️ to help students GET THAT INTERNSHIP!!!**

⭐ Star this repo if it helped you!

</div>

