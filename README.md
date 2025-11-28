# School Management System (SMS)

A production-ready Flask-based School Management System for staff (admin, accountant, teacher) to manage students, courses, enrollment, attendance, and payments on a local intranet.

## Features

- ✅ Multi-role authentication (Admin, Accountant, Teacher)
- ✅ Student management (CRUD, categories, photo upload)
- ✅ Course management and enrollment
- ✅ Attendance tracking
- ✅ Payment recording and receipts
- ✅ Real-time dashboard with charts
- ✅ Admin panel for user management
- ✅ Secure (CSRF, password hashing, role-based access)
- ✅ SQLite (dev) / PostgreSQL (prod) support
- ✅ RESTful API endpoints
- ✅ Responsive Bootstrap 5 UI

## Tech Stack

- **Backend**: Flask + SQLAlchemy
- **Database**: SQLite / PostgreSQL
- **Auth**: Flask-Login + Werkzeug
- **Frontend**: Bootstrap 5, Chart.js, Vanilla JS
- **Deployment**: Gunicorn + Nginx (Ubuntu 22.04)

## Quick Start (Development)

### Prerequisites
- Python 3.9+
- Pip

### Setup

```bash
# Clone/create project
cd ACCDT_CMS

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
flask db upgrade

# Create first admin user
flask create-admin --username admin --password admin123

# Run development server
flask run
```

Visit `http://localhost:5000` and login with admin credentials.

## Documentation

- **PROJECT_STRUCTURE.md** - Detailed folder and file layout
- **DATABASE_SCHEMA.md** - SQL schema and data model explanation (coming next)

## Deployment

See deployment instructions in guide (Ubuntu 22.04 + Nginx + Gunicorn + systemd).

## Next Steps

1. Database schema and models
2. Configuration and app factory
3. Authentication
4. Core CRUD routes
5. Dashboard and APIs
6. Frontend templates
7. Deployment setup

---

**Status**: In development - Project structure initialized ✓
