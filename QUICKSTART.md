# 🚀 QUICKSTART GUIDE - School Management System

## ⚡ Get Running in 5 Minutes (Windows)

### Step 1: Open PowerShell and Navigate to Project

```powershell
cd "c:\Users\mmkb3\OneDrive\Desktop\ACCDT_CMS"
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal.

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- SQLAlchemy (database ORM)
- Flask-Login (authentication)
- Flask-Migrate (database migrations)
- Flask-WTF (forms)
- Werkzeug (security utilities)
- Chart.js (data visualization)

### Step 4: Create .env File

```powershell
copy .env.example .env
```

Edit `.env` if needed (defaults are fine for development).

### Step 5: Run the Application

```powershell
python run.py
```

You should see:
```
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 6: Open in Browser

Visit: **http://localhost:5000**

---

## 📝 First Time Setup

### Create First Admin Account

1. Click **"Create one"** link on login page
   - Or go to: `http://localhost:5000/register-admin`

2. Fill in the form:
   ```
   Username:  admin
   Email:     admin@school.local
   Password:  admin123
   Confirm:   admin123
   ```

3. Click **"Create Admin Account"**

4. You'll be redirected to login page ✅

### Login

```
Username:  admin
Password:  admin123
☐ Remember me for 7 days
```

Click **Login**

### Create Additional Users

1. In navbar, click **Admin** → **Users**
2. Click **Create User**
3. Fill in details:

   **Teacher Account:**
   ```
   Username:  teacher1
   Email:     teacher@school.local
   Password:  teacher123
   Role:      Teacher
   ```

   **Accountant Account:**
   ```
   Username:  accountant1
   Email:     accountant@school.local
   Password:  account123
   Role:      Accountant
   ```

4. Click **Create** for each

---

## 🎯 Test Different Roles

### Admin Login
```
Username:  admin
Password:  admin123
```
✅ Full system access to all features

### Teacher Login
```
Username:  teacher1
Password:  teacher123
```
✅ Can access:
- Dashboard
- Students list
- Courses list
- Attendance marking

❌ Cannot access:
- Payments
- User management

### Accountant Login
```
Username:  accountant1
Password:  account123
```
✅ Can access:
- Dashboard
- Students list
- Courses list
- Payments

❌ Cannot access:
- Attendance
- User management

---

## 📊 Dashboard Features

After logging in as Admin, the Dashboard shows:

**Stats Cards:**
- 📊 Total Students
- 📚 Total Courses
- 💰 Fees Collected This Month
- ✅ Today's Attendance %

**Student Breakdown:**
- Total students
- Male / Female ratio
- Day Scholars vs Hostel
- Gender breakdown for each admission type

**Monthly Stats:**
- New admissions this month
- Total fees collected
- Fees pending

**Charts:**
- 📊 Bar chart: Students per course
- 📈 Line chart: Fee collection trend (last 6 months)

---

## 📁 Project Structure

```
ACCDT_CMS/
├── app/                          # Main Flask package
│   ├── __init__.py              # App factory
│   ├── models.py                # Database models
│   ├── config.py                # Configuration
│   ├── decorators.py            # Role decorators
│   ├── utils.py                 # Utility functions
│   ├── routes/                  # API routes (blueprints)
│   │   ├── auth.py              # Login/logout
│   │   ├── admin.py             # User management
│   │   ├── dashboard.py         # Dashboard
│   │   ├── students.py          # Students CRUD
│   │   ├── courses.py           # Courses CRUD
│   │   ├── attendance.py        # Attendance
│   │   └── payments.py          # Payments
│   ├── templates/               # HTML files
│   │   ├── base.html            # Master layout
│   │   ├── login.html           # Login page
│   │   ├── register_admin.html  # Admin registration
│   │   └── dashboard.html       # Dashboard
│   └── static/                  # CSS/JS/uploads
│       ├── css/styles.css       # Custom CSS
│       ├── js/
│       │   ├── dashboard.js     # Dashboard logic
│       │   └── common.js        # Utilities
│       └── uploads/             # Student photos
├── run.py                       # Start app
├── requirements.txt             # Dependencies
├── .env                         # Environment config
├── .gitignore                   # Git ignore
└── README.md                    # Documentation
```

---

## 🐛 Troubleshooting

### Port 5000 Already in Use
```powershell
# Option 1: Kill process using port 5000
Get-Process | Where-Object {$_.Name -eq "python"} | Stop-Process

# Option 2: Use different port
# Edit run.py, change: app.run(port=5001)
```

### "ModuleNotFoundError: No module named 'flask'"
```powershell
# Make sure virtual environment is activated
venv\Scripts\activate

# Install requirements again
pip install -r requirements.txt
```

### Database Issues
```powershell
# Delete the database and start fresh
Remove-Item school_dev.db -ErrorAction SilentlyContinue

# Restart the app - database will be recreated
python run.py
```

### Can't Remember Admin Password
```powershell
# Delete database (all data will be lost)
Remove-Item school_dev.db

# Restart app and create new admin
python run.py
```

---

## 🔐 Security Notes

✅ **Implemented:**
- Password hashing (Werkzeug PBKDF2)
- Secure sessions (HttpOnly, SameSite)
- Role-based access control
- SQL injection protection (SQLAlchemy ORM)
- CSRF protection ready

⚠️ **For Production:**
- Change `SECRET_KEY` in `.env`
- Use PostgreSQL instead of SQLite
- Enable HTTPS (set `SESSION_COOKIE_SECURE=True`)
- Use strong passwords for all users
- Regular database backups

---

## 📊 Database

**Default: SQLite** (for development)
- File: `school_dev.db`
- No setup needed
- Great for local development

**Production: PostgreSQL**
```powershell
# Update .env
DATABASE_URL=postgresql://user:password@localhost/school_db

# Then restart app
```

---

## 🔗 Important URLs

| URL | Purpose |
|---|---|
| `http://localhost:5000` | Home (redirects to dashboard if logged in) |
| `http://localhost:5000/login` | Login page |
| `http://localhost:5000/register-admin` | Create first admin |
| `http://localhost:5000/logout` | Logout |
| `http://localhost:5000/dashboard` | Dashboard |
| `http://localhost:5000/api/dashboard` | Dashboard data (JSON) |
| `http://localhost:5000/admin/users` | User management |

---

## 📚 What's Built So Far

✅ **Authentication & Authorization**
- Login/logout system
- Three user roles (admin, teacher, accountant)
- Role-based access control
- Admin user management
- Secure password hashing

✅ **Database Models**
- User, Student, Course, Enrollment, Attendance, Payment

✅ **Frontend**
- Bootstrap 5 responsive design
- Beautiful login page
- Admin registration
- Navbar with role-based menu
- Dashboard with statistics and charts

✅ **API Endpoints**
- `/api/dashboard` - Dashboard statistics
- `/api/users` - User list (JSON)
- Authentication endpoints

---

## 📋 What's Next (Future Steps)

- [ ] Complete Student CRUD (list, create, edit, delete)
- [ ] Student photo upload with validation
- [ ] Bulk student import from CSV
- [ ] Course management
- [ ] Enrollment system
- [ ] Attendance marking and reports
- [ ] Payment recording and receipts
- [ ] More admin features
- [ ] Email notifications
- [ ] PDF report generation
- [ ] Deployment to Ubuntu 22.04 with Nginx

---

## 💡 Tips & Tricks

### Keyboard Shortcuts
- `Tab` - Navigate login form quickly
- `Enter` - Submit forms

### Development Speed
- Changes to Python files auto-reload (Flask debug mode)
- Changes to HTML/CSS/JS require browser refresh
- Use browser DevTools (F12) to inspect elements

### Test User Roles Quickly
1. Open two browser tabs or windows
2. Login as different users in each tab
3. Compare what each role can access

### View Generated SQL Queries
```python
# In Python shell
from app import create_app
app = create_app()
app.config['SQLALCHEMY_ECHO'] = True
```

---

## 🎓 Learning Path

1. **Understand the structure**
   - Read `PROJECT_STRUCTURE.md`
   - Browse `app/__init__.py` (app factory)

2. **See authentication in action**
   - Try different roles
   - Check `app/decorators.py`
   - View `app/routes/auth.py`

3. **Add your own features**
   - Create new route in blueprint
   - Add database model
   - Create HTML template
   - Test with different roles

---

## ✅ You're Ready!

The authentication system is **production-ready**:
- ✅ Secure password hashing
- ✅ Session management
- ✅ Role-based access control
- ✅ Clean code structure
- ✅ Ready for deployment

**Enjoy building!** 🚀

---

## Support

**Common Issues?**
1. Check terminal error messages
2. Review the console in browser (F12 → Console)
3. Check `.env` file configuration
4. Restart Flask app

**Questions?**
- Review code comments
- Check model docstrings
- Read this guide again
- Check Flask documentation

---

**Happy coding! 🎉**
