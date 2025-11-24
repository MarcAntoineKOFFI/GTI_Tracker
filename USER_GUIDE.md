# GTI Tracker - Complete User Guide

## 🚀 Getting Started

### Launch the Application
```bash
cd C:\Users\marca\PycharmProjects\GTI_Tracker
python main.py
```

The app will open with a **pure black theme** for comfortable viewing!

---

## 📋 Main Features

### 1. NETWORKING TAB

#### Adding a Contact
1. Click the **orange "View All Contacts"** button
2. Click **"+ Add Activity"** button
3. Fill in the form:
   - **Name*** (required)
   - **Job Title*** (required)  
   - **Company*** (required) - Auto-suggests from history
   - **Contact Date** - Defaults to today
   - **Relevant Info** - Connection notes (optional)
   - **Status** - Defaults to "Cold message"
4. Click **"Add Contact"**
5. See **green success toast** ✓

#### Viewing Contacts
- **Dashboard**: Click "📇 View All Contacts"
- **Two View Modes**:
  - **Table View**: Classic spreadsheet layout
  - **Cards View**: Visual card layout with photos
- **Toggle**: Use "📋 Table" or "🗂️ Cards" buttons

#### Searching & Filtering
- **Search Box**: Type name, company, or title
- **Status Filter**: Filter by Cold message, Has responded, Call, Interview
- **Sort Options**: 
  - Recent first / Oldest first
  - Name A-Z / Z-A
  - Company A-Z / Z-A

#### Editing a Contact
- **From Table**: Click "Edit" button
- **From Cards**: Click ✏️ icon
- **From Details**: Double-click any row
- Make changes → Click **"Save"**
- See **success toast** ✓

#### Deleting a Contact
- Click **Delete** or 🗑️ icon
- **Confirmation dialog** appears
- Confirm → Contact deleted
- **Toast notification** shows success

#### View Contact Details
- **Double-click** any contact row
- See full information:
  - Contact details
  - Generated networking message
  - Follow-up status
  - Recent activity
- **Copy Message** button → Copies to clipboard
- **Edit/Delete** buttons available

---

### 2. INTERNSHIPS TAB

#### Adding an Application
1. Switch to **"Internships"** tab
2. Click **"+ Add Internship Application"**
3. Fill in details:
   - **Role Name*** (required)
   - **Company*** (required)
   - **Job Link** (optional URL)
   - **Linked Contact** - Select from your network
   - **Application Date** - Defaults to today
   - **Status** - Defaults to "Applied"
   - **Notes** - Any additional info
4. Click **"Add Application"**
5. **Success toast** appears ✓

#### Viewing Applications
- See dashboard with metrics:
  - Total Applications
  - Active Applications (not rejected/offer)
  - Status breakdown
- Click to see **full list**

#### Managing Applications
- **Edit**: Click Edit button
- **Delete**: With confirmation
- **Update Status**: Change from Applied → Screening → Interview → Offer/Rejected
- **Link Contacts**: Connect applications to your network
- **Add Notes**: Track interview questions, feedback

---

### 3. STATISTICS & ANALYTICS

#### Networking Stats
Click **"View Statistics"** to see:
- **Total Contacts** count
- **Response Rate** (% beyond cold message)
- **Average Response Time**
- **Conversion to Interview**
- **Activity Timeline** (last 7/30 days)
- **Status Breakdown** pie chart
- **Company Analysis**

#### Internship Stats
See comprehensive metrics:
- **Total Applications**
- **Interview Rate** (% that got interviews)
- **Offer Rate** (% that got offers)
- **Application Timeline**
- **Status Pipeline** visualization
- **Best Companies** (highest success rate)
- **Networking Impact** (applications with referrals vs without)

---

### 4. MESSAGE GENERATION

#### Auto-Generate Networking Messages
1. Open **Contact Details**
2. Scroll to **"Suggested Networking Message"**
3. Message generated using template with:
   - Contact's name, title, company
   - Your profile info (from Settings)
   - Relevant information you added
4. Click **"Copy to Clipboard"**
5. Paste in LinkedIn/Email

#### Customize Template
1. Click **⚙️ Settings**
2. Go to **"Message Template"** section
3. Edit template with placeholders:
   - `{name}` - Contact's name
   - `{job_title}` - Their title
   - `{company}` - Their company
   - `{user_name}` - Your name
   - `{user_school}` - Your school
   - `{user_ambitions}` - Your goals
4. Click **"Save Settings"**

---

### 5. FOLLOW-UP REMINDERS

#### Automatic Tracking
- App automatically flags contacts needing follow-up
- Default: **3 days** after initial contact
- Only contacts in "Cold message" status

#### Viewing Follow-Ups
1. Dashboard shows **"Needs Follow-Up (X)"** count
2. Click button to see **filtered list**
3. Each contact shows **days since contact**
4. Take action:
   - Send follow-up message
   - Update status to "Has responded"
   - Mark as complete

#### Customizing Threshold
1. Go to **Settings** → **"Notifications & Reminders"**
2. Adjust **follow-up days** (1-14 days)
3. Save changes

---

## ⌨️ KEYBOARD SHORTCUTS

### Global Shortcuts
- **Ctrl+N** - Add new contact/application (context-aware)
- **Ctrl+F** - Focus search box
- **Ctrl+,** - Open Settings
- **Ctrl+Q** - Quit application

### Dialog Shortcuts
- **Ctrl+S** - Save current form
- **Esc** - Close dialog/cancel
- **Enter** - Submit form (when button focused)

### Navigation
- **Tab** - Move between fields
- **Shift+Tab** - Move backwards
- **Space** - Activate buttons/checkboxes

---

## ⚙️ SETTINGS

### Personal Information
- **Your Name** - Used in message templates
- **School/University** - Mentioned in messages
- **Career Ambitions** - Personalize your outreach

### Message Template
- Customize networking message format
- Use placeholders for dynamic content
- Preview with sample data
- Reset to default if needed

### Notifications
- Set follow-up reminder threshold
- Choose notification preferences
- Configure alert timing

### Data Management
- **Export Contacts** to CSV
- **Export Applications** to CSV
- **Backup Database** - Manual backup
- **Reset All Data** - Fresh start (with confirmation)

---

## 💡 TIPS & BEST PRACTICES

### Networking
✅ **Add contacts immediately** after connecting
✅ **Include relevant info** - mutual connections, shared interests
✅ **Follow up within 3 days** of cold message
✅ **Update status promptly** when you get responses
✅ **Use generated messages** as templates, personalize further

### Applications
✅ **Link applications to contacts** when you have referrals
✅ **Track all details** in notes - interview questions, impressions
✅ **Update status regularly** to keep pipeline accurate
✅ **Add job links** for easy reference
✅ **Review statistics** to see what's working

### Organization
✅ **Use search** to find contacts/applications quickly
✅ **Filter by status** to focus on active opportunities
✅ **Check follow-ups daily** - consistency matters
✅ **Review stats weekly** - adjust strategy based on data
✅ **Back up regularly** - protect your data

---

## 🎨 INTERFACE GUIDE

### Color Meanings

**Status Colors:**
- **Gray** - Cold message / Applied (initial state)
- **Blue** - Has responded / Screening (progress)
- **Purple** - Call scheduled (active engagement)
- **Orange** - Interview scheduled (strong opportunity)
- **Green** - Offer received (success!)
- **Red** - Rejected (closed opportunity)

**UI Elements:**
- **Orange buttons** - Primary actions (Add, Save)
- **White text** - Primary information
- **Light gray** - Secondary information
- **Dark cards** - Content containers
- **Dashed borders** - Interactive areas

### Layout
- **Left Sidebar**: Navigation (Networking, Internships)
- **Top Bar**: Search, filters, action buttons
- **Main Area**: Dashboard or list view
- **Right Panel**: Quick stats, metrics

---

## 🔧 TROUBLESHOOTING

### App Won't Start
```bash
# Verify Python environment
python --version  # Should be 3.8+

# Check dependencies
pip install -r requirements.txt

# Run from project directory
cd C:\Users\marca\PycharmProjects\GTI_Tracker
python main.py
```

### Database Issues
- Database file location: `%APPDATA%\GTI_Tracker\gti_tracker.db`
- **Reset database**: Run `python reset_database.py`
- **Restore backup**: Settings → Data Management → Import

### Contact/Application Not Showing
1. Check if filters are active
2. Try searching for the name
3. Refresh view (switch tabs and back)
4. Check if accidentally deleted

### Can't Delete Item
- Confirm you clicked "Yes" in confirmation dialog
- Check if item has linked dependencies
- Try restarting the application

---

## 📊 UNDERSTANDING YOUR DATA

### Metrics Explained

**Networking:**
- **Total Contacts**: Everyone you've reached out to
- **Response Rate**: % who replied to initial message
- **Conversion Rate**: % who progressed to interview
- **Average Response Time**: Days until first response

**Internships:**
- **Total Applications**: All submitted applications
- **Active Applications**: Applied, Screening, Interview status
- **Interview Rate**: % of applications that led to interviews
- **Success Rate**: % that resulted in offers

### Using Statistics
- **Low response rate?** → Improve message quality
- **High applications, low interviews?** → Better targeting
- **Networking impact positive?** → Focus on referrals
- **Slow response time?** → Follow up more consistently

---

## 🎯 WORKFLOW EXAMPLES

### Daily Routine
1. **Open app** → Check dashboard
2. **Review "Needs Follow-Up"** → Send messages
3. **Update statuses** for any responses
4. **Add new contacts** from day's networking
5. **Log applications** submitted today

### Weekly Review
1. **Check statistics** → Analyze trends
2. **Review active applications** → Plan next steps
3. **Clean up statuses** → Mark stale contacts
4. **Export data** → Backup progress
5. **Adjust strategy** based on metrics

### Before Big Recruiting Events
1. **Export contacts** → Have list ready
2. **Update all statuses** → Clean slate
3. **Review message template** → Optimize
4. **Set follow-up reminders** → Stay organized
5. **Create application pipeline** → Track opportunities

---

## 💾 DATA BACKUP

### Automatic Backups
- **Daily backups**: Last 7 days kept
- **Weekly backups**: Last 4 weeks kept  
- **Monthly backups**: Last 12 months kept
- **Location**: `%APPDATA%\GTI_Tracker\backups\`

### Manual Backup
1. Settings → Data Management
2. Click **"Export Full Database"**
3. Choose save location
4. Keep safe copy!

### Restore from Backup
1. Close application
2. Copy backup file
3. Settings → Data Management → Import
4. Select backup file
5. Confirm restore

---

## 🎊 SUCCESS STORIES

Use GTI Tracker to:
- ✅ **Stay organized** during recruiting season
- ✅ **Never miss follow-ups** with automatic reminders
- ✅ **Track ROI** on networking efforts
- ✅ **Optimize strategy** with data-driven insights
- ✅ **Land more interviews** through better organization
- ✅ **Get that internship!** 🎉

---

**Need Help?**
- Check this guide
- Review tooltips in app
- Try keyboard shortcuts
- Export data regularly
- Have fun networking!

**Happy Internship Hunting!** 🚀

