# ✅ USER TESTING CHECKLIST

## Before You Start
- [ ] App is running (python main.py)
- [ ] You see the Networking dashboard
- [ ] Background is pure black
- [ ] All text is white/light gray (readable)

---

## Test 1: Visual Verification
- [ ] "Networking" title is WHITE (not dark/invisible)
- [ ] "0 Professionals Contacted" - number is FULLY VISIBLE
- [ ] "0 Needs Follow-Up" - number is FULLY VISIBLE  
- [ ] Cards have enough space (not squeezed)
- [ ] No white chunks visible
- [ ] Everything is on black background

**Expected**: All text readable, numbers visible, cards spacious ✓

---

## Test 2: Add Contact
- [ ] Click orange "View All Contacts" button → List opens
- [ ] Click "+ Add Activity" button → Dialog appears
- [ ] Dialog has black background
- [ ] All text in dialog is white/readable
- [ ] Fill in required fields:
  - Name: "Test Person"
  - Job Title: "Engineer"  
  - Company: "TestCo"
- [ ] Fill optional fields:
  - Email: "test@test.com"
  - LinkedIn: "linkedin.com/in/test"
  - Phone: "555-1234"
- [ ] Click "Add Contact" button
- [ ] **GREEN toast appears** (not error!)
- [ ] Toast says "Contact 'Test Person' added successfully!"
- [ ] Dialog closes automatically
- [ ] Contact appears in the table

**Expected**: Contact added successfully with green toast ✓

---

## Test 3: View Contact
- [ ] Double-click the contact you just added
- [ ] Detail view opens
- [ ] All text is white/readable
- [ ] Contact name is visible at top
- [ ] Email shows: test@test.com
- [ ] LinkedIn shows: linkedin.com/in/test
- [ ] Phone shows: 555-1234
- [ ] Close detail view

**Expected**: All information displayed correctly ✓

---

## Test 4: Edit Contact
- [ ] Click "Edit" button (pencil icon) on your contact
- [ ] Dialog opens with existing data filled in
- [ ] Change name to "Updated Person"
- [ ] Click "Save"
- [ ] GREEN toast appears
- [ ] Toast says "Contact 'Updated Person' updated successfully!"
- [ ] Name changes in the list

**Expected**: Edit works with success toast ✓

---

## Test 5: Delete Contact
- [ ] Click "Delete" button (trash icon)
- [ ] Confirmation dialog appears
- [ ] Dialog asks "Delete contact 'Updated Person'?"
- [ ] Click "Yes"
- [ ] Contact removed from list
- [ ] No errors

**Expected**: Contact deleted successfully ✓

---

## Test 6: Statistics
- [ ] Click "View Statistics" button
- [ ] Statistics window opens
- [ ] All text is white/readable
- [ ] No dark text on dark background
- [ ] Close statistics window

**Expected**: Statistics display correctly ✓

---

## Test 7: Internships Tab
- [ ] Click "Internships" in sidebar
- [ ] Dashboard switches to internships
- [ ] All text is white/readable
- [ ] Numbers are fully visible
- [ ] No visual issues

**Expected**: Internships tab works perfectly ✓

---

## If ANY Test Fails

**Check console for errors** and report:
1. Which test failed
2. What you saw vs what you expected
3. Any error messages in console

---

## If ALL Tests Pass ✅

**CONGRATULATIONS!** 🎉

The app is working perfectly:
- ✅ No visual issues
- ✅ Can add contacts
- ✅ Toast notifications work
- ✅ All features functional

**You're ready to track internships!**

---

## Quick Reference

### How to Launch
```bash
cd C:\Users\marca\PycharmProjects\GTI_Tracker
python main.py
```

### How to Add Contact
1. "View All Contacts" button
2. "+ Add Activity" button
3. Fill form
4. "Add Contact" button
5. See GREEN toast ✓

### What Fixed
- ✅ Toast QPoint error → Toasts work
- ✅ Dark text → All white now
- ✅ Squeezed numbers → 300px cards
- ✅ Database error → Fresh schema

---

**Everything should work now!** ✅

