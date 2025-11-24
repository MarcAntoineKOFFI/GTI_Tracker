# Changelog

All notable changes to GTI Tracker will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-24

### Added - Initial Release

#### Core Features
- **Networking Management**
  - Add, edit, view, and delete professional contacts
  - Four-stage status tracking (Cold message, Has responded, Call, Interview)
  - Automatic follow-up reminders with configurable threshold (default 3 days)
  - Customizable message template with 7 dynamic placeholders
  - Message preview and one-click clipboard copy
  - Real-time search and filtering by status, name, company, or title
  - Multiple sort options (date, name, company - ascending/descending)
  
- **Internship Application Tracking**
  - Add, edit, view, and delete internship applications
  - Five-stage status tracking (Applied, Screening, Interview, Offer, Rejected)
  - Link applications to networking contacts for referral tracking
  - Job posting URL storage with test link functionality
  - Notes field for interview details and other information
  - Real-time search and filtering capabilities
  
- **Statistics & Analytics**
  - Networking statistics window with:
    - Overall metrics cards (total contacts, status breakdown, follow-ups needed)
    - Status distribution pie chart
    - Contacts per week bar chart (last 12 weeks)
    - Conversion funnel visualization
    - Top 10 companies list
    - CSV export functionality
  - Internship statistics window with:
    - Overall metrics (total, active, offers, rejection rate)
    - Status distribution pie chart
    - Applications per week bar chart (last 12 weeks)
    - Conversion funnel (Applied → Screening → Interview → Offer)
    - Networking impact analysis (with vs. without referrals)
    - Top 10 target companies
    - CSV export functionality
    
- **User Interface**
  - Modern, polished design with custom Qt stylesheet
  - Sidebar navigation with Networking and Internships tabs
  - Dashboard views with quick-action cards and metrics
  - List views with table-based display and empty states
  - Detail dialogs with comprehensive contact/application information
  - Settings dialog with 4 tabs (Personal Info, Message Template, Notifications, Data Management)
  - Responsive layouts and high-DPI display support
  
- **Data Management**
  - SQLite database with SQLAlchemy ORM
  - OS-appropriate data storage locations (AppData/Library/XDG)
  - Export contacts to CSV
  - Export applications to CSV
  - Export full database backup
  - Import contacts from CSV (with validation)
  - Import applications from CSV (with validation)
  - Database reset functionality (with safeguards)
  
- **Keyboard Shortcuts**
  - Ctrl+N - Add new contact/application (context-aware)
  - Ctrl+F - Focus search field in list views
  - Ctrl+, - Open settings
  - Ctrl+1 - Switch to Networking tab
  - Ctrl+2 - Switch to Internships tab
  - Esc - Close dialogs
  
- **Additional Features**
  - Auto-complete for company names (learns from existing data)
  - Character counter for text fields
  - Input validation with real-time error messages
  - Alternating row colors in tables for readability
  - Status badges with color coding
  - Clickable linked contacts in application views
  - Window state persistence (size, position, last tab)
  - Comprehensive logging for debugging

#### Technical Implementation
- **Architecture**: MVC pattern with separation of concerns
- **Database**: SQLAlchemy 2.0+ with SQLite backend
- **UI Framework**: PySide6 (Qt6) with custom QSS stylesheet
- **Charts**: QtCharts for visualizations (pie charts, bar charts)
- **Testing**: Comprehensive test suite covering all core functionality
- **Documentation**: README, FEATURES, QUICKSTART, and inline documentation
- **Cross-Platform**: Windows, macOS, and Linux support

### Technical Details

#### Database Schema
- **networking_contacts**: id, name, job_title, company, contact_date, relevant_info, status, created_at, last_updated
- **internship_applications**: id, role_name, company, job_link, contact_id (FK), application_date, status, notes, last_updated
- **settings**: id, message_template, follow_up_days, user_name, user_school, user_ambitions

#### Dependencies
- PySide6 >= 6.6.0
- SQLAlchemy >= 2.0.0

### Known Limitations
- No cloud sync (local database only)
- No mobile app (desktop only)
- No calendar integration
- No email integration
- Status history not tracked (only current status)

### Future Enhancements (Planned)
- Email integration for direct outreach from app
- Calendar sync for interview scheduling
- Attachment storage (resumes, cover letters)
- Company research integration (Glassdoor, LinkedIn data)
- Chrome extension for quick adds from LinkedIn/job boards
- Mobile companion app
- Cloud sync option
- Status change history tracking
- Reminder notifications
- Interview preparation tools
- Salary tracking and analysis

---

## Version History

**v1.0.0** - 2025-01-24 - Initial release with complete feature set

---

For detailed usage instructions, see:
- [README.md](README.md) - Full documentation
- [FEATURES.md](FEATURES.md) - Detailed feature guide
- [QUICKSTART.md](QUICKSTART.md) - Quick start tutorial

