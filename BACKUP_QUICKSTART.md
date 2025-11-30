# Backup System - Quick Reference Guide ⚡

## 🚀 Quick Start for Admins

### Access Backup System:
1. Log in as admin
2. Click **"Backup"** in navigation menu (cloud-download icon)
3. Or navigate to: `http://yourserver/backup/`

---

## 📥 Download Backups

| What | Format | Records | Use Case |
|------|--------|---------|----------|
| **Students Backup** | CSV | All students | Offline records, audit trail |
| **Courses Backup** | CSV | All courses | Course listings, archival |
| **Payments Backup** | CSV | All payments | Financial reports, reconciliation |
| **Attendance Backup** | CSV | All attendance | Attendance reports, analysis |
| **Complete Backup** | JSON | Entire DB | Full system snapshot, disaster recovery |

### How to Download:
1. Go to **"Download Backups"** section
2. Click on the backup you want
3. File downloads automatically
4. Filename includes date/time stamp

---

## 🗑️ Clear Database

### Clearing Individual Tables:
```
Clear All Students → Removes all student records
Clear All Courses → Removes all course records
Clear All Payments → Removes all payment records
Clear All Attendance → Removes all attendance records
```

### Clear All Data:
```
Clear ALL Data → Removes everything except admin user
Use case: Reset database for fresh data entry
```

### How to Clear:
1. Go to **"Clear Database Tables"** section
2. Click on the operation you want
3. Confirm in the dialog
4. Data is deleted permanently
5. Confirmation message appears

---

## 📊 Dashboard Statistics

Shows real-time counts:
- **Students**: Total student records
- **Courses**: Total course records
- **Enrollments**: Total enrollments
- **Payments**: Total payment records
- **Attendance**: Total attendance records
- **Total Records**: Sum of all above

These update when you refresh the page.

---

## ⚠️ Safety Tips

✅ **Always backup before clearing**
✅ **Admin user is never deleted**
✅ **Confirmation required for destructive operations**
✅ **All operations logged with timestamp**
✅ **Error messages if operation fails**

---

## 📁 File Naming

Files download with this pattern:
```
TABLE_backup_DD_MM_YYYY_HH_MM_SS.csv
```

Example:
```
students_backup_15_01_2024_14_30_45.csv
```

Timestamp ensures each backup is unique.

---

## 🔄 Common Workflows

### Backup Before Reset:
```
1. Go to /backup/
2. Click "Complete Backup" → Save file
3. Wait for download
4. Then click "Clear ALL Data"
5. Confirm in dialog
```

### Monthly Data Export:
```
1. Go to /backup/
2. Download Students → Save
3. Download Courses → Save
4. Download Payments → Save
5. Download Attendance → Save
```

### Full System Backup:
```
1. Go to /backup/
2. Click "Complete Backup"
3. Save in secure location
4. Schedule monthly
```

---

## 🎯 When to Use Each Feature

| Situation | Action |
|-----------|--------|
| Regular backup | Download Complete Backup (JSON) |
| Financial audit | Download Payments (CSV) |
| End of semester | Download all individual tables |
| Testing new features | Clear individual tables |
| Reset entire system | Clear ALL Data |
| Student roster | Download Students (CSV) |
| Course catalog | Download Courses (CSV) |
| Attendance report | Download Attendance (CSV) |

---

## 🔐 Access Control

- **Who can use**: Admin users only
- **Route protection**: @admin_required decorator
- **Admin user**: Never deleted in "Clear All" operation
- **Other users**: Can view courses as guest (no admin features)

---

## 📞 Troubleshooting

| Problem | Solution |
|---------|----------|
| Can't see Backup link | Log in as admin user |
| 403 Forbidden error | Check user role, must be admin |
| Download fails | Check internet connection, disk space |
| Page not loading | Refresh browser (Ctrl+F5) |
| Statistics wrong | Click F5 to refresh page |
| CSV opens as text | Save as .csv and open in Excel |
| Data didn't clear | Refresh page to verify |

---

## 🔗 Related Routes

```
GET  /backup/                     Dashboard
GET  /backup/download/students    Student CSV
GET  /backup/download/courses     Course CSV
GET  /backup/download/payments    Payment CSV
GET  /backup/download/attendance  Attendance CSV
GET  /backup/download/all         Complete JSON
POST /backup/clear                Clear tables
```

---

## 📈 Dashboard Cards (Top of Page)

| Card | Shows |
|------|-------|
| 🔵 Students | Total student count |
| 🔵 Courses | Total course count |
| 🟢 Enrollments | Total enrollment count |
| 🟡 Payments | Total payment count |
| 🔴 Attendance | Total attendance records |
| ⚫ Total Records | Sum of all records |

Click refresh to update all cards.

---

## 💡 Tips & Tricks

1. **Before Testing**: Download Complete Backup
2. **Weekly Backups**: Set calendar reminder to download
3. **Organize Files**: Create backup folder with dates
4. **Excel Import**: CSV files work directly in Excel
5. **Archival**: Store backups in cloud for disaster recovery
6. **Documentation**: Note when and why you cleared data

---

## ✅ Feature Checklist

- [x] Download individual table backups (CSV)
- [x] Download complete database backup (JSON)
- [x] Clear individual tables safely
- [x] Clear entire database (with admin retention)
- [x] View real-time statistics
- [x] Confirmation dialogs for destructive operations
- [x] Timestamped filenames
- [x] Excel-compatible CSV format
- [x] Admin-only access
- [x] Flash messages for feedback

---

## 🎓 Best Practices

### Before Production:
- [ ] Test all backup functions
- [ ] Test all clear functions
- [ ] Verify admin user stays on clear all
- [ ] Check CSV files open in Excel
- [ ] Verify JSON backup contains all data

### During Operation:
- [ ] Monthly backups
- [ ] Before major data changes
- [ ] After semester ends
- [ ] Before system updates
- [ ] For audit trails

### Data Retention:
- [ ] Keep weekly backups for 1 month
- [ ] Keep monthly backups for 1 year
- [ ] Keep annual backups indefinitely
- [ ] Store encrypted in secure location

---

## 📍 Navigation Path

```
1. Home Dashboard
   ↓
2. Admin Navigation (top menu)
   ↓
3. Click "Backup" (cloud-download icon)
   ↓
4. Backup Dashboard (/backup/)
```

---

**Version**: 1.0
**Last Updated**: Latest Session
**Status**: Production Ready ✅
