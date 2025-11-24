# GTI Tracker - Complete Feature Guide

## Table of Contents
1. [Application Overview](#application-overview)
2. [Main Window & Navigation](#main-window--navigation)
3. [Networking Features](#networking-features)
4. [Internship Tracking Features](#internship-tracking-features)
5. [Statistics & Analytics](#statistics--analytics)
6. [Settings & Customization](#settings--customization)
7. [Data Management](#data-management)
8. [Keyboard Shortcuts](#keyboard-shortcuts)

---

## Application Overview

GTI Tracker is a comprehensive desktop application designed to help students systematically manage their internship search through two interconnected activities:

1. **Networking** - Track professional contacts and relationships
2. **Internship Applications** - Monitor application progress and outcomes

### Key Benefits
- **Data-Driven Insights**: Visualize your progress with charts and statistics
- **Follow-Up Reminders**: Never miss a networking opportunity
- **Networking Impact Analysis**: See how referrals affect success rates
- **Message Templates**: Generate personalized outreach messages automatically
- **Cross-Platform**: Works on Windows, macOS, and Linux

---

## Main Window & Navigation

### Sidebar Navigation
The left sidebar provides quick access to main sections:
- **📇 Networking** - Manage professional contacts
- **💼 Internships** - Track applications
- Keyboard shortcuts: `Ctrl+1` (Networking), `Ctrl+2` (Internships)

### Top Bar
- **⚙️ Settings** button in top-right corner
- Keyboard shortcut: `Ctrl+,`

### Window Persistence
The application remembers:
- Window size and position
- Last active tab
- Filter and sort preferences (where applicable)

---

## Networking Features

### Dashboard View

#### 1. Add Networking Activity Button
- Large, prominent call-to-action button
- Opens dialog to add new contact
- Keyboard shortcut: `Ctrl+N` (when in Networking tab)

#### 2. Metrics Cards
- **Total Professionals Contacted**: Overall contact count
- **Last 7 Days Chart**: Bar chart showing daily networking activity
- **Needs Follow-Up**: Contacts requiring attention (color-coded by urgency)

#### 3. Quick Actions
- **View All Statistics**: Opens comprehensive analytics window
- **Needs Follow-Up**: Filters list to show only contacts needing follow-up

### Contact List View

#### Features
- **Search**: Real-time filtering by name, company, or title (`Ctrl+F` to focus)
- **Status Filter**: Filter by contact status (Cold message, Has responded, Call, Interview)
- **Sorting Options**:
  - Recent first / Oldest first
  - Name A–Z / Name Z–A
  - Company A–Z / Company Z–A

#### Table Columns
1. **Name** (bold) - Primary identifier
2. **Job Title** - Professional position
3. **Company** - Current employer
4. **Contact Date** - Formatted date (e.g., "Jan 15, 2025")
5. **Status** - Colored badge indicating current stage
6. **Actions** - Edit and Delete buttons

#### Status Colors
- **Gray**: Cold message (initial outreach)
- **Blue**: Has responded
- **Yellow/Orange**: Call scheduled/completed
- **Green**: Interview opportunity

#### Interactions
- **Double-click** any row to view full contact details
- **Edit** button opens contact for editing
- **Delete** button removes contact (with confirmation)

### Add/Edit Contact Dialog

#### Required Fields
- **Name*** - Contact's full name
- **Job Title*** - Professional position
- **Company*** - Current employer (with autocomplete from existing entries)

#### Optional Fields
- **Contact Date** - Defaults to today (calendar picker available)
- **Relevant Information** - Notes about shared connections, interests (500 char limit with counter)
- **Status** - Defaults to "Cold message"

#### Features
- **Autocomplete**: Company field suggests previously entered companies
- **Character Counter**: Real-time feedback for relevant information field
- **Validation**: Highlights required fields if empty
- **Date Picker**: Calendar widget prevents future dates

### Contact Detail View

#### Information Display
- Contact name (large, bold)
- Job title and company
- Contact date and last updated
- Current status (large colored badge)
- Relevant information (if provided)

#### Suggested Networking Message
- **Auto-Generated**: Uses template from settings with your personal info
- **Placeholders Replaced**: Name, job title, company, your details, relevant info
- **Regenerate**: Updates message if contact info changed
- **Copy to Clipboard**: One-click copy for easy pasting into LinkedIn/email

#### Status Management
- **Dropdown**: Change status instantly
- **Auto-Update**: Last updated timestamp refreshes automatically

#### Follow-Up Alerts
- **Conditional Display**: Shows only when follow-up needed
- **Calculation**: Based on days since contact date vs. settings threshold
- **Alert Message**: "⏰ Follow-up needed – it has been X days with no response"
- **Mark as Followed Up**: Resets follow-up timer without changing status

#### Actions
- **Edit**: Opens contact in edit mode
- **Delete**: Removes contact (confirms first, handles linked applications)
- **Close**: Returns to previous view

### Networking Statistics

#### Overall Metrics Cards
- Total contacts
- Status breakdown with counts and percentages
- Contacts needing follow-up
- Average contacts per week

#### Charts & Visualizations
1. **Weekly Activity Chart**: Bar chart of last 12 weeks
2. **Status Distribution**: Pie chart with color-coded segments
3. **Conversion Funnel**: Flow from Cold message → Response → Call → Interview with percentages

#### Additional Insights
- Follow-up performance metrics
- Average response time (when status changes)
- Top companies by contact count

#### Export Options
- **Export Report (CSV)**: All contacts with full data
- Includes timestamps, status, and notes

---

## Internship Tracking Features

### Dashboard View

#### Metrics Cards
- **Add Internship Application**: Large action button (`Ctrl+N` when in Internships tab)
- **Total Applications**: Overall application count
- **Status Distribution Chart**: Pie chart showing Applied/Screening/Interview/Offer/Rejected
- **Active Applications**: Count excluding Offer and Rejected

#### Quick Actions
- **View Statistics**: Opens comprehensive analytics

### Application List View

#### Features
- **Search**: Filter by role name or company (`Ctrl+F`)
- **Status Filter**: Filter by application status
- **Sorting Options**: Recent first, Company A–Z, Role A–Z, etc.

#### Table Columns
1. **Role Name** (bold)
2. **Company**
3. **Application Date**
4. **Status** (colored badge)
5. **Linked Contact** (clickable to view contact details)
6. **Job Link** (🔗 icon opens in browser)
7. **Actions** (Edit, Delete)

#### Status Colors
- **Gray**: Applied
- **Blue**: Screening
- **Orange**: Interview
- **Green**: Offer
- **Red**: Rejected

### Add/Edit Internship Dialog

#### Required Fields
- **Role Name*** - Position title
- **Company*** - Organization (autocomplete from contacts and internships)

#### Optional Fields
- **Job Link** - URL to posting (validates URL format, includes "Test Link" button)
- **Application Date** - Defaults to today
- **Linked Contact** - Dropdown of all networking contacts (searchable)
- **Status** - Defaults to "Applied"
- **Notes** - Multi-line text area

#### Features
- **URL Validation**: Ensures job link is valid URL format
- **Test Link**: Opens URL in browser to verify
- **Contact Linking**: Searchable dropdown formatted as "Name – Title @ Company"
- **Rich Notes**: Unlimited text for tracking interview details, salary info, etc.

### Internship Detail View

#### Information Display
- Role name (large, bold)
- Company
- Application date and last updated
- Status badge (large, color-coded)
- **View Job Posting** button (if link exists)

#### Linked Contact Section
- **If Linked**: Shows "Referred by Name – Title @ Company" with view button
- **If Not Linked**: Shows "No linked contact" with "Link Contact" button

#### Status Management
- Dropdown to change status
- Instant database update

#### Notes Section
- Editable text area
- **Save Notes** button to persist changes
- Great for tracking interview questions, impressions, salary discussions

#### Actions
- **Edit**: Opens application in edit mode
- **Delete**: Removes application (with confirmation)
- **Close**: Returns to list

### Internship Statistics

#### Overall Metrics
- Total applications
- Active applications (non-final statuses)
- Offers received
- Rejection rate (percentage)

#### Charts & Visualizations
1. **Timeline Chart**: Applications over time (weekly/monthly bars)
2. **Status Distribution**: Pie chart of all statuses
3. **Conversion Funnel**: Applied → Screening → Interview → Offer with percentages

#### Networking Impact Analysis
Special section comparing applications with vs. without referrals:
- "Applications with referrals: X% interview rate"
- "Applications without referrals: Y% interview rate"
- Demonstrates value of networking

#### Company Insights
- Top 10 target companies by application count
- Response rates by company (if data available)

#### Export
- **Export Report (CSV)**: All applications with complete data

---

## Statistics & Analytics

### Data-Driven Insights

Both Networking and Internship statistics provide:
- **Visual Charts**: Easy-to-understand pie, bar, and line charts
- **Conversion Metrics**: Percentages showing progression through stages
- **Time Series**: Activity trends over weeks/months
- **Comparative Analysis**: Before/after, with/without metrics

### Conversion Funnels

#### Networking Funnel
```
Cold message (100%) 
    ↓ X% responded
Has responded 
    ↓ Y% progressed
Call 
    ↓ Z% progressed
Interview
```

#### Internship Funnel
```
Applied (100%)
    ↓ X% advanced
Screening
    ↓ Y% advanced
Interview
    ↓ Z% converted
Offer
```

### Motivational Design
Statistics are designed to:
- Show progress visually
- Highlight successes (offers, responses)
- Identify improvement areas (low conversion stages)
- Encourage consistency (weekly activity charts)

---

## Settings & Customization

### Personal Information Tab
Configure details used in message templates:
- **Your Name**: Inserted into networking messages
- **Your School**: Referenced in outreach
- **Your Ambitions**: Career goals and aspirations

### Message Template Tab

#### Template Editor
Large text area with your networking message template

#### Available Placeholders
- `{name}` - Contact's name
- `{job_title}` - Contact's job title
- `{company}` - Contact's company
- `{user_name}` - Your name
- `{user_school}` - Your school
- `{user_ambitions}` - Your career ambitions
- `{relevant_info}` - Contact-specific notes

#### Actions
- **Reset to Default**: Restores original template
- **Preview**: Shows template with sample data

#### Example Template
```
Hi {name},

I hope this message finds you well! My name is {user_name}, and I'm currently a student at {user_school}. I came across your profile and was really impressed by your work as a {job_title} at {company}.

{user_ambitions}

{relevant_info}

I would love to learn more about your experience and any advice you might have for someone looking to break into the field. Would you be open to a brief chat sometime?

Thank you for your time and consideration!

Best regards,
{user_name}
```

### Notifications & Reminders Tab
- **Follow-up Days**: Number of days before flagging contacts (1-30, default 3)
- Determines when "Needs Follow-Up" alert appears

### Data Management Tab

#### Export Options
1. **Export Contacts to CSV**: All networking contacts
2. **Export Internships to CSV**: All applications
3. **Export Full Database**: Complete SQLite database file (for backup)

#### Import Options
1. **Import Contacts from CSV**: Bulk import networking contacts
2. **Import Internships from CSV**: Bulk import applications

#### CSV Format
Exports use standard CSV with headers. Can be opened in Excel, Google Sheets, etc.

#### Danger Zone
**Reset All Data**:
- Permanently deletes ALL contacts and applications
- Requires typing "DELETE" to confirm
- Cannot be undone
- Use only to start fresh

---

## Data Management

### Database Location
SQLite database stored in OS-appropriate location:
- **Windows**: `%APPDATA%\GTI_Tracker\gti_tracker.db`
- **macOS**: `~/Library/Application Support/GTI_Tracker/gti_tracker.db`
- **Linux**: `~/.local/share/GTI_Tracker/gti_tracker.db`

### Backup Strategy
**Recommended Practice**:
1. Weekly: Export Full Database from Settings
2. Monthly: Export both CSV files for external analysis
3. Store backups in cloud storage (Dropbox, Google Drive, etc.)

### Database Relationships
- **One-to-Many**: Each contact can have multiple internship applications
- **Foreign Key**: Applications link to contacts via `contact_id`
- **Cascade Behavior**: Deleting contact removes link from applications (keeps application)

---

## Keyboard Shortcuts

### Global Shortcuts
- `Ctrl+1` - Switch to Networking tab
- `Ctrl+2` - Switch to Internships tab
- `Ctrl+,` - Open Settings
- `Escape` - Close dialogs

### Context-Sensitive Shortcuts
- `Ctrl+N` - Add new item (contact or application based on current tab)
- `Ctrl+F` - Focus search field (in list views)
- `Enter` - Submit forms
- `Tab` - Navigate between fields

### Navigation
- `Double-click` - Open detail view for any item
- `Click Status Badge` - No action (informational only)
- `Click Linked Contact` - Opens contact detail (in internship list)

---

## Tips & Best Practices

### Networking Workflow
1. **Daily**: Add 3-5 new contacts
2. **Check**: "Needs Follow-Up" each morning
3. **Update**: Status as soon as responses received
4. **Review**: Weekly statistics to track progress

### Application Tracking
1. **Immediate**: Log application as soon as submitted
2. **Link**: Connect to networking contact if referred
3. **Update**: Status promptly when hearing back
4. **Notes**: Record interview questions, impressions immediately after

### Maximizing Success
1. **Link Applications**: Always link to referral contact to track networking ROI
2. **Consistent Updates**: Update statuses promptly for accurate metrics
3. **Use Relevant Info**: Add shared connections/interests for personalized messages
4. **Review Statistics**: Weekly review to identify what's working
5. **Follow Up**: Respond to alerts within 24 hours

### Data Hygiene
1. **Deduplicate**: Check for duplicates before adding contacts
2. **Complete Info**: Fill all fields for best analytics
3. **Accurate Dates**: Backdate when entering historical data
4. **Regular Backups**: Export database weekly
5. **Meaningful Notes**: Record specifics, not just "had call"

---

## Troubleshooting

### Common Issues

**Q: Keyboard shortcuts not working**
A: Ensure the main window has focus (click on it first)

**Q: Search not filtering results**
A: Search is case-insensitive and searches name, company, title simultaneously

**Q: Follow-up alerts not appearing**
A: Check Settings > Notifications - follow_up_days threshold
A: Ensure contact status is still "Cold message"

**Q: Cannot delete contact with linked applications**
A: Feature allows deletion - removes link from applications but keeps them

**Q: Charts showing "No data"**
A: Add at least one contact/application to see charts populate

**Q: Message template not updating**
A: Must click "Save Settings" button after editing template

### Getting Help

Check files included with application:
- `README.md` - Technical documentation
- `QUICKSTART.md` - Getting started guide
- This file - Comprehensive feature guide

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Platform**: Windows, macOS, Linux

Happy internship hunting! 🚀

