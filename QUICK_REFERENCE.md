# 📋 QUICK REFERENCE CARD

## 🚀 START / STOP

```powershell
# START
cd c:\Users\mmkb3\OneDrive\Desktop\ACCDT_CMS
python run.py

# STOP
Ctrl+C

# Open in browser
http://localhost:5000
```

---

## 🔐 LOGIN CREDENTIALS

```
ADMIN:
  Username: admin
  Password: admin123

TEACHER:
  Username: teacher1
  Password: teacher123

ACCOUNTANT:
  Username: accountant1
  Password: account123
```

---

## 📁 KEY FILES

| File | Purpose |
|---|---|
| `app/__init__.py` | App factory |
| `app/models.py` | Database models |
| `app/routes/*.py` | API routes |
| `app/templates/*.html` | HTML pages |
| `run.py` | Start app |
| `seed_database.py` | Load sample data |

---

## 🌐 KEY URLs

```
Login:       http://localhost:5000/login
Dashboard:   http://localhost:5000/dashboard
Admin:       http://localhost:5000/admin/users
API:         http://localhost:5000/api/dashboard
```

---

## 🛠️ COMMON COMMANDS

```powershell
# Reset database
python seed_database.py

# Run tests
python test_init.py

# Commit to git
git add -A
git commit -m "message"

# Push to repo
git push origin master

# Install packages
pip install -r requirements.txt
```

---

## 📊 DATABASE TABLES

1. **users** - Admin, Teacher, Accountant accounts
2. **students** - 8 sample students
3. **courses** - 5 courses
4. **enrollments** - Student-Course links
5. **attendance** - Attendance records
6. **payments** - Payment records

---

## ✅ WHAT'S BUILT

- [x] Login/Logout
- [x] Admin Registration
- [x] User Management
- [x] Dashboard with Charts
- [x] Database Models (7 tables)
- [x] API Endpoints
- [x] Role-Based Access
- [x] Beautiful UI (Bootstrap 5)
- [x] Sample Data

---

## ❌ WHAT'S NOT BUILT YET

- [ ] Student CRUD
- [ ] Course CRUD
- [ ] Enrollment System
- [ ] Attendance Marking
- [ ] Payment Recording
- [ ] Photo Upload
- [ ] CSV Import
- [ ] Detailed Reports

---

## 🎯 CHOOSE NEXT FEATURE

```
Option 1: Student Management (2-3 hours)
Option 2: Course & Enrollment (1-2 hours)
Option 3: Attendance System (1-2 hours)
Option 4: Payment System (1-2 hours)
Option 5: All Templates (3-4 hours)
```

---

## 🔧 STRUCTURE TO ADD NEW FEATURE

1. Create `app/routes/feature.py`
2. Add models to `app/models.py` if needed
3. Create templates in `app/templates/`
4. Register blueprint in `app/__init__.py`
5. Add CSS/JS as needed
6. Test with different roles

---

## 🚨 TROUBLESHOOTING

| Problem | Solution |
|---|---|
| Port 5000 in use | Edit `run.py` → `port=5001` |
| DB locked | Delete `school_dev.db` |
| Module not found | `pip install -r requirements.txt` |
| Login fails | Run `python seed_database.py` |

---

## 📞 IMPORTANT NUMBERS

- **Total Users**: 3 (admin, teacher1, accountant1)
- **Total Students**: 8
- **Total Courses**: 5
- **Total Enrollments**: 20
- **Total Attendance Records**: 50
- **Database File Size**: ~200KB

---

## 🔐 SECURITY CHECKLIST

- [x] Passwords hashed (PBKDF2)
- [x] Sessions secure (HttpOnly)
- [x] SQL injection protected (ORM)
- [x] CSRF ready (Flask-WTF)
- [x] Role-based access
- [ ] HTTPS enabled (TODO for production)
- [ ] Changed SECRET_KEY (TODO)
- [ ] PostgreSQL setup (TODO)

---

## 🎓 KEY CONCEPTS

**Role-Based Access**
```python
@admin_required         # Only admin
@teacher_required       # Teacher or admin
@roles_required('admin') # Specific role(s)
```

**Models**
```python
User (id, username, role, password_hash)
Student (id, first_name, last_name, category, status)
Course (id, name, fee, seats)
```

**Blueprints**
```python
auth_bp          # Authentication
dashboard_bp     # Dashboard
admin_bp         # Admin panel
students_bp      # Students (structure)
```

---

## 🎉 STATUS

```
✅ Project Structure
✅ Authentication System
✅ Role-Based Access Control
✅ Database Models
✅ Dashboard with Charts
✅ Admin User Management
✅ API Endpoints
⏳ Student Management
⏳ Course Management
⏳ Attendance System
⏳ Payment System
```

---

## 📈 NEXT PHASE COMMAND

```powershell
# When ready for next feature:
git add -A
git commit -m "feat: add [feature name]"
git push origin master
```

Then tell me which feature to build next!

---

**Created**: Nov 28, 2025
**Status**: ✅ WORKING
**App Running**: http://localhost:5000

🚀 **Ready to build more!**
