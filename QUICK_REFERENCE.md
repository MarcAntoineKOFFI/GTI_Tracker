# GTI Tracker v2.0 - Quick Reference

## 🚀 Launch Application
```bash
cd C:\Users\marca\PycharmProjects\GTI_Tracker
python main.py
```

## 🎨 New Features (v2.0)

### Bloomberg Terminal Dark Theme
- **Background**: Deep navy `#0B0E1D` - easy on eyes
- **Orange accents**: `#FF8B3D` for actions
- **Status colors**: Green (success), Red (rejected), Blue (info), Purple (interview)

### Contact Card View
1. Navigate to **Networking** → **Contact List**
2. Click **🗂️ Cards** button (top right)
3. See professional contact cards with:
   - Gradient initials circles
   - Color-coded status badges
   - Days since contact
   - Quick action buttons
   - Click any card to see details

### View Modes
- **📋 Table**: Traditional sortable table
- **🗂️ Cards**: Visual card layout (NEW!)

## 🎨 Color Meanings

| Color | Meaning | Use Case |
|-------|---------|----------|
| 🟠 Orange | Action Required | Primary buttons, CTAs |
| 🟢 Green | Success | Offers, completed tasks |
| 🔵 Blue | Information | Screening, neutral states |
| 🟣 Purple | Progress | Calls, interviews |
| 🟡 Amber | Warning | Follow-ups needed |
| 🔴 Red | Critical | Rejections, errors |

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+N` | New contact/application |
| `Ctrl+F` | Focus search |
| `Ctrl+,` | Open settings |
| `Ctrl+1` | Networking tab |
| `Ctrl+2` | Internships tab |
| `Esc` | Close dialog |

## 📊 Status System

### Networking Statuses
- **Cold message** - Initial outreach (Gray)
- **Has responded** - Got a reply (Blue)
- **Call** - Phone/video call scheduled (Purple)
- **Interview** - Interview opportunity (Orange)

### Internship Statuses
- **Applied** - Application submitted (Gray)
- **Screening** - In review process (Blue)
- **Interview** - Interview rounds (Purple)
- **Offer** - Offer received! (Green)
- **Rejected** - Application declined (Red)

## 🗂️ Card View Tips

### Quick Actions
- **✉️ Message**: Generate personalized outreach message
- **✏️ Edit**: Modify contact details
- **🗑️ Delete**: Remove contact (with confirmation)
- **Click Card**: Open full detail view

### Card Information
- **Circle**: Contact initials with gradient
- **Top**: Name, job title
- **Middle**: Company, status badge
- **Bottom**: Days since contact, relevant info preview
- **Actions**: Quick access buttons

## 🎯 Workflow Tips

### Adding Contacts
1. Click **+ Add Activity**
2. Fill required fields (name, title, company)
3. Add relevant info (shared connections, interests)
4. Generate message from detail view

### Tracking Applications
1. Switch to **Internships** tab
2. Click **+ Add Application**
3. Link to networking contact (if applicable)
4. Track through status pipeline

### Following Up
1. Dashboard shows "Needs Follow-Up" count
2. Click to filter contacts
3. Update status after following up
4. System tracks days since contact

## 📁 Files & Locations

### Database
- **Windows**: `%APPDATA%\GTI_Tracker\gti_tracker.db`
- **Backup**: Settings → Data Management → Export Database

### Stylesheets
- **Dark Theme**: `styles/dark_professional.qss` (active)
- **Light Theme**: `styles/main.qss` (fallback)

### Documentation
- `README.md` - Full documentation
- `TRANSFORMATION_SUMMARY.md` - v2.0 changes
- `TRANSFORMATION_GUIDE.md` - Implementation roadmap
- `QUICKSTART.md` - Beginner guide

## 🔧 Customization

### Change Theme
Edit `main.py` line ~26 to switch stylesheets

### Adjust Colors
Edit `styles/dark_professional.qss` color values

### Follow-up Threshold
Settings → Notifications → Adjust days (default: 3)

## 🐛 Troubleshooting

### Theme Not Loading
- Check `styles/dark_professional.qss` exists
- Look for errors in terminal
- Fallback to `main.qss` automatically

### Cards Not Showing
- Click **🗂️ Cards** button in contact list
- Add contacts if list is empty
- Check view mode is set to "cards"

### Data Not Saving
- Check database file has write permissions
- Look for errors in terminal
- Try exporting/importing data

## 📞 Getting Help

1. Check `TRANSFORMATION_SUMMARY.md` for features
2. Review `README.md` for detailed docs
3. Run `python run_tests.py` to verify installation
4. Check terminal for error messages

## 🎉 What's New in v2.0

### Visual Overhaul
✅ Bloomberg Terminal-inspired dark theme  
✅ Professional color system  
✅ Enhanced typography hierarchy  

### Contact Management
✅ Card view with professional design  
✅ Dual-mode display (table/cards)  
✅ Improved status badges  
✅ Better empty states  

### Under the Hood
✅ Enhanced database models (ready)  
✅ Activity logging system (ready)  
✅ Task management models (ready)  
✅ Interview tracking models (ready)  

### Coming Soon
🚧 Comprehensive dashboard  
🚧 Task management UI  
🚧 Calendar integration  
🚧 Kanban board views  
🚧 Advanced analytics  

---

**Version**: 2.0.0-dev  
**Updated**: 2025-01-24  
**Theme**: Dark Professional (Bloomberg-inspired)

