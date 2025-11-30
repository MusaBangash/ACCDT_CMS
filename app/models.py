"""
SQLAlchemy ORM models for School Management System.
Defines: User, Student, Course, Enrollment, Attendance, Payment
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User model for authentication.
    Roles: 'admin', 'accountant', 'teacher'
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='teacher')  # admin, accountant, teacher
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    attendance_records = db.relationship('Attendance', backref='marked_by', lazy='dynamic',
                                        foreign_keys='Attendance.marked_by_user_id')
    payments = db.relationship('Payment', backref='recorded_by', lazy='dynamic',
                              foreign_keys='Payment.recorded_by_user_id')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def has_role(self, role):
        """Check if user has a specific role"""
        return self.role == role
    
    def is_admin(self):
        """Check if user is admin"""
        return self.role == 'admin'
    
    def is_accountant(self):
        """Check if user is accountant"""
        return self.role == 'accountant'
    
    def is_teacher(self):
        """Check if user is teacher"""
        return self.role == 'teacher'
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'


class Student(db.Model):
    """
    Student model with personal and admission details.
    Categories: regular, needy, orphan, sponsored, staff_child, other
    Admission types: day_scholar, hostel
    Status: active, inactive, graduated, leave
    """
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.String(20), unique=True, nullable=True)  # Auto-generated: ACCDT-YYYY-00001
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)  # M, F, Other
    admission_type = db.Column(db.String(20), nullable=False)  # day_scholar, hostel
    date_of_birth = db.Column(db.Date, nullable=True)
    admission_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    phone = db.Column(db.String(15), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    category = db.Column(db.String(20), nullable=False, default='regular')  # regular, needy, orphan, sponsored, staff_child, other
    status = db.Column(db.String(20), nullable=False, default='active')  # active, inactive, graduated, leave
    photo_path = db.Column(db.String(255), nullable=True)
    
    # Additional fields from admission form
    cnic = db.Column(db.String(20), unique=True, nullable=True)
    blood_group = db.Column(db.String(10), nullable=True)
    nationality = db.Column(db.String(50), nullable=True)
    emergency_contact = db.Column(db.String(15), nullable=True)
    permanent_address = db.Column(db.String(255), nullable=True)
    guardian_name = db.Column(db.String(100), nullable=True)
    guardian_cnic = db.Column(db.String(20), nullable=True)
    last_qualification = db.Column(db.String(100), nullable=True)
    current_qualification = db.Column(db.String(100), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='student', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def full_name(self):
        """Return full name"""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def gender_label(self):
        """Get gender label"""
        genders = {'M': 'Male', 'F': 'Female', 'O': 'Other'}
        return genders.get(self.gender, self.gender)
    
    @property
    def status_label(self):
        """Get status label with color code"""
        status_labels = {
            'active': 'Active',
            'inactive': 'Inactive',
            'graduated': 'Graduated',
            'leave': 'On Leave'
        }
        return status_labels.get(self.status, self.status)
    
    @property
    def status_badge_class(self):
        """Get Bootstrap badge class for status"""
        status_colors = {
            'active': 'bg-success',
            'inactive': 'bg-danger',
            'graduated': 'bg-info',
            'leave': 'bg-warning'
        }
        return status_colors.get(self.status, 'bg-secondary')
    
    def generate_registration_number(self):
        """Generate unique registration number using customizable prefix"""
        from datetime import datetime as dt
        
        # Get prefix from settings or use default
        prefix = Setting.get('reg_number_prefix', 'ACCDT')
        
        year = dt.utcnow().year
        # Count students registered in this year
        count = Student.query.filter(
            Student.registration_number.like(f'{prefix}-{year}-%')
        ).count() + 1
        self.registration_number = f'{prefix}-{year}-{count:05d}'
        return self.registration_number
    
    @property
    def age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = datetime.today().date()
            return today.year - self.date_of_birth.year - \
                   ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def get_enrolled_courses(self):
        """Get list of courses student is enrolled in"""
        return [enrollment.course for enrollment in self.enrollments.filter_by()]
    
    def total_fees_due(self):
        """Calculate total fees due (sum of course fees - paid amounts)"""
        enrollments = self.enrollments.all()
        total_fee = sum(e.course.fee for e in enrollments if e.course)
        paid = sum(p.amount for p in self.payments.all())
        return max(0, total_fee - paid)
    
    def __repr__(self):
        return f'<Student {self.full_name}>'


class Course(db.Model):
    """
    Course model for courses offered by school.
    """
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    instructor_name = db.Column(db.String(100), nullable=True)
    instructor_contact = db.Column(db.String(15), nullable=True)
    course_outline_path = db.Column(db.String(255), nullable=True)
    fee = db.Column(db.Float, nullable=False, default=0.0)
    seats = db.Column(db.Integer, nullable=False, default=30)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    attendance_records = db.relationship('Attendance', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='course', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def student_count(self):
        """Get number of students enrolled in this course"""
        return self.enrollments.count()
    
    @property
    def available_seats(self):
        """Get available seats"""
        return self.seats - self.student_count
    
    @property
    def is_full(self):
        """Check if course is at full capacity"""
        return self.available_seats <= 0
    
    def __repr__(self):
        return f'<Course {self.name}>'


class Enrollment(db.Model):
    """
    Enrollment model - links students to courses.
    """
    __tablename__ = 'enrollments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    enroll_date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint - student can only enroll once per course
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', name='uq_student_course'),)
    
    def __repr__(self):
        return f'<Enrollment {self.student.full_name} -> {self.course.name}>'


class Attendance(db.Model):
    """
    Attendance model - tracks student attendance per course per date.
    Status: present, absent, leave
    """
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False)  # present, absent, leave
    marked_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint - one attendance record per student per course per date
    __table_args__ = (db.UniqueConstraint('student_id', 'course_id', 'date', name='uq_attendance'),)
    
    def __repr__(self):
        return f'<Attendance {self.student.full_name} - {self.date} ({self.status})>'


class PaymentCategory(db.Model):
    """
    Payment Category model - defines different types of fees.
    Examples: Security, Admission, Monthly Fee, Lab Fee, etc.
    """
    __tablename__ = 'payment_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    description = db.Column(db.Text, nullable=True)
    default_amount = db.Column(db.Float, nullable=False, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    payments = db.relationship('Payment', backref='category', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<PaymentCategory {self.name} - Rs. {self.default_amount}>'


class Payment(db.Model):
    """
    Payment model - records student fee payments.
    Methods: cash, cheque, bank_transfer, online, other
    Status: paid, pending, partial_paid
    """
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('payment_categories.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=True, index=True)
    amount_due = db.Column(db.Float, nullable=False)  # Total amount due
    amount_paid = db.Column(db.Float, nullable=False, default=0)  # Amount paid so far
    security_fees = db.Column(db.Float, nullable=True, default=0)  # Optional security fees
    admission_fees = db.Column(db.Float, nullable=True, default=0)  # Optional admission fees
    status = db.Column(db.String(20), nullable=False, default='pending')  # paid, pending, partial_paid
    payment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    method = db.Column(db.String(20), nullable=False)  # cash, cheque, bank_transfer, online, other
    reference_no = db.Column(db.String(100), nullable=True)  # cheque no, transaction id, etc.
    recorded_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @property
    def amount_due_remaining(self):
        """Calculate remaining balance"""
        return self.amount_due - self.amount_paid
    
    @property
    def percentage_paid(self):
        """Calculate percentage paid"""
        return (self.amount_paid / self.amount_due * 100) if self.amount_due > 0 else 0
    
    def __repr__(self):
        return f'<Payment {self.student.full_name} - {self.category.name} - Rs. {self.amount_due}>'


class Setting(db.Model):
    """
    Settings model for storing system-wide configurations.
    Used for customizing registration number prefix, formats, and other settings.
    """
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get(cls, key, default=None):
        """Get setting value by key"""
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @classmethod
    def set(cls, key, value, description=None):
        """Set or update setting value"""
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = cls(key=key, value=value, description=description)
            db.session.add(setting)
        db.session.commit()
        return setting
    
    def __repr__(self):
        return f'<Setting {self.key}={self.value}>'
