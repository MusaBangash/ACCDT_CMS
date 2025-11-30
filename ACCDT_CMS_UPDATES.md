    # ACCDT CMS - Academy Management System
## Implementation Summary & Updates

### 🎉 Latest Updates (Phase 2 - Complete)

#### Branding Changes
- ✅ Changed all references from "School CMS" to **"ACCDT CMS - Academy Management System"**
- ✅ Updated login page with ACCDT branding
- ✅ Updated admin registration page with ACCDT branding
- ✅ Updated all templates and navbar

#### 8 ACCDT Courses Added
1. **Fashion Designing** - Rs. 15,000 (30 seats)
2. **Tailoring** - Rs. 10,000 (35 seats)
3. **Web Designing** - Rs. 12,000 (25 seats)
4. **Graphic Designing** - Rs. 12,000 (25 seats)
5. **Artificial Intelligence** - Rs. 18,000 (20 seats)
6. **Digital Marketing** - Rs. 13,000 (28 seats)
7. **E-Commerce** - Rs. 14,000 (25 seats)
8. **Basics of Computer** - Rs. 5,000 (40 seats)

#### Enhanced Dashboard Display

**Student Statistics Section:**
- ✅ **Total Students** - Overall count
- ✅ **Total Male Students** - Male count
- ✅ **Total Female Students** - Female count
- ✅ **Day Scholars**
  - Total day scholars
  - Male day scholars
  - Female day scholars
- ✅ **Hostel Students**
  - Total hostel students
  - Male hostel students
  - Female hostel students

**Charts:**
- ✅ **Students by Course** - Horizontal bar chart showing enrollment per course
- ✅ **Fee Collection Trend** - Line chart showing 6-month trend

#### Sample Data Added
- **16 Sample Students**
  - 9 Day Scholars (5 Male, 4 Female)
  - 7 Hostel Students (4 Male, 3 Female)
  - Multiple categories: regular, needy, orphan, sponsored, staff_child
  - From various cities across Pakistan

- **43 Enrollments** across 8 courses

#### Test Credentials
```
Username: admin
Password: admin123
Role: Admin (Full System Access)
```

---

## System Architecture

### Technology Stack
- **Backend**: Flask + SQLAlchemy
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Flask-Login + Werkzeug Password Hashing
- **Frontend**: Bootstrap 5 + Chart.js
- **Deployment**: Gunicorn + Nginx (Ubuntu 22.04)

### Database Models
1. **User** - System users with roles (admin, accountant, teacher)
2. **Student** - Student information with admission types and categories
3. **Course** - Available courses with fees and seat limits
4. **Enrollment** - Student-Course relationships
5. **Attendance** - Attendance tracking
6. **Payment** - Fee payment records

### Role-Based Access Control
- **Admin**: Full access (users, courses, students, payments, reports)
- **Accountant**: Payment recording and fee management
- **Teacher**: Attendance marking and student information

---

## How to Run ACCDT CMS

### Prerequisites
- Python 3.9+
- Flask and dependencies (see requirements.txt)

### Quick Start

```bash
# 1. Navigate to project directory
cd ACCDT_CMS

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database & seed data
python seed_courses.py
python seed_students.py

# 5. Create admin user
python -c "from app import create_app; from app.models import db, User; app = create_app(); ctx = app.app_context(); ctx.push(); admin = User(username='admin', email='admin@accdt.edu', role='admin'); admin.set_password('admin123'); db.session.add(admin); db.session.commit(); print('✅ Admin created')"

# 6. Run the application
python run.py

# 7. Access in browser
# http://localhost:5000
# Login with admin / admin123
```

---

## Project File Structure

```
ACCDT_CMS/
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models.py                   # SQLAlchemy models
│   ├── config.py                   # Configuration (dev/prod)
│   ├── decorators.py               # Role-based access decorators
│   ├── utils.py                    # Helper utilities
│   │
│   ├── routes/
│   │   ├── auth.py                 # Login, logout, registration
│   │   ├── dashboard.py            # Dashboard + API endpoints
│   │   ├── students.py             # Student CRUD
│   │   ├── courses.py              # Course CRUD
│   │   ├── attendance.py           # Attendance marking
│   │   ├── payments.py             # Payment recording
│   │   └── admin.py                # User management
│   │
│   ├── templates/
│   │   ├── base.html               # Base layout with navbar
│   │   ├── login.html              # Login page
│   │   ├── register_admin.html     # Admin registration
│   │   ├── dashboard.html          # Dashboard with stats & charts
│   │   └── (other templates)
│   │
│   └── static/
│       ├── css/
│       │   └── styles.css          # Custom Bootstrap overrides
│       ├── js/
│       │   ├── dashboard.js        # Chart.js rendering
│       │   └── common.js           # Shared utilities
│       └── uploads/                # Student photos storage
│
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
├── seed_courses.py                 # Seed ACCDT courses
├── seed_students.py                # Seed sample students
├── school_dev.db                   # SQLite database
└── README.md                       # Project documentation
```

---

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Process login
- `GET /logout` - Logout (requires auth)
- `GET /register-admin` - Admin registration
- `POST /register-admin` - Create first admin

### Dashboard
- `GET /` - Dashboard page (requires auth)
- `GET /dashboard` - Dashboard page (requires auth)
- `GET /api/dashboard` - Dashboard data as JSON (returns all statistics)

### Students
- `GET /students/` - List students
- `POST /students/create` - Create student
- `GET /students/<id>` - View student
- `POST /students/<id>/edit` - Edit student
- `POST /students/<id>/delete` - Delete student

### Courses
- `GET /courses/` - List courses
- `POST /courses/create` - Create course
- `POST /courses/<id>/edit` - Edit course
- `POST /courses/<id>/delete` - Delete course

### Admin
- `GET /admin/dashboard` - Admin overview
- `GET /admin/users` - List users
- `POST /admin/users/create` - Create user
- `POST /admin/users/<id>/edit` - Edit user
- `POST /admin/users/<id>/delete` - Delete user
- `GET /api/users` - Users as JSON

---

## Dashboard Features

### Widgets
1. **Total Students** - Overall student count
2. **Total Courses** - Available courses
3. **This Month Fees** - Fees collected in current month
4. **Today's Attendance** - Attendance percentage today

### Statistics Panel
- Student breakdown by gender
- Day scholar vs hostel split with gender breakdown
- New admissions this month
- Fees collected and pending

### Charts
1. **Students by Course** - Horizontal bar chart (auto-rotates for 8 courses)
   - Shows enrollment count per course
   - Color-coded bars

2. **Fee Collection Trend** - Line chart
   - Last 6 months of fee collection
   - Displays in PKR currency

---

## Next Steps for Development

### Phase 3 (Coming Soon)
- [ ] Create Students listing page with search/filter
- [ ] Student registration form (CRUD)
- [ ] Course management page
- [ ] Enrollment management
- [ ] Attendance marking interface
- [ ] Payment recording form
- [ ] Reports generation

### Phase 4 (Future)
- [ ] Export to Excel/PDF
- [ ] Bulk CSV upload for students
- [ ] SMS/Email notifications
- [ ] Advanced reporting
- [ ] Dashboard customization
- [ ] Mobile-responsive improvements

---

## Security Notes

1. **Password Storage**: Werkzeug password hashing (PBKDF2-SHA256)
2. **CSRF Protection**: Flask-WTF enabled
3. **Session Security**: Secure cookies with HttpOnly flag
4. **File Uploads**: Validated extensions, secure filename generation
5. **Path Traversal**: Protected against directory traversal attacks
6. **SQL Injection**: SQLAlchemy ORM protects against SQL injection

---

## Database Schema

### Tables Created
- `users` - System users
- `students` - Student records
- `courses` - Course offerings
- `enrollments` - Student-Course mappings
- `attendance` - Attendance records
- `payments` - Fee payments

### Key Relationships
- Students → Enrollments → Courses (Many-to-Many)
- Students ← Attendance → Courses
- Payments → Student, Course, User

---

## Deployment (Ubuntu 22.04)

### Using Gunicorn + Nginx

```bash
# Install Gunicorn
pip install gunicorn

# Run with Gunicorn (4 workers)
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Set up systemd service file for auto-start on boot
# (See gunicorn.service file in project)

# Configure Nginx as reverse proxy
# (See nginx.conf file in project)
```

---

## Support & Troubleshooting

### Common Issues

**Issue**: Database locked error
**Solution**: Delete `school_dev.db` and restart the app

**Issue**: Port 5000 already in use
**Solution**: `lsof -i :5000` and kill the process, or change port in `run.py`

**Issue**: Module not found
**Solution**: Ensure virtual environment is activated and `pip install -r requirements.txt` is run

**Issue**: Template not found
**Solution**: Check template file is in `app/templates/` folder

---

## Version Info
- **ACCDT CMS Version**: 1.0.0
- **Flask Version**: 2.3.3
- **SQLAlchemy Version**: 2.0.5
- **Python Version**: 3.9+
- **Database**: SQLite (Development)

---

## Contact & Support
For issues or questions, refer to the inline code documentation in each file.

**Last Updated**: November 28, 2025
**Status**: ✅ Fully Functional - Phase 2 Complete

---

## Key Features Implemented ✅

- [x] Multi-role authentication (Admin, Accountant, Teacher)
- [x] ACCDT branding and naming
- [x] 8 industry-relevant courses
- [x] Enhanced dashboard with detailed student statistics
- [x] Students by course chart (horizontal layout)
- [x] Fee collection trend chart
- [x] Sample data for testing
- [x] SQLite database
- [x] Role-based access control
- [x] Secure password storage
- [x] Session management
- [x] API endpoints for data
- [x] Responsive Bootstrap UI

---

**Happy Learning with ACCDT CMS! 🎓**
