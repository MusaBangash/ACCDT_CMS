"""
Dashboard routes and API endpoints.
"""

from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta

from app.models import db, Student, Course, Enrollment, Attendance, Payment

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
def index():
    """Dashboard page or redirect to guest courses if not authenticated"""
    if not current_user.is_authenticated:
        return redirect(url_for('courses.guest_browse_courses'))
    return render_template('dashboard.html')


@dashboard_bp.route('/api/dashboard')
@login_required
def api_dashboard():
    """
    API endpoint returning enhanced dashboard statistics.
    Includes:
    - Total students (male/female breakdown)
    - Day scholars (male/female breakdown)
    - Hostel students (male/female breakdown)
    - Students by course
    - Fee statistics
    - Attendance data
    """
    # Student statistics - Overall
    total_students = Student.query.count()
    total_male = Student.query.filter_by(gender='M').count()
    total_female = Student.query.filter_by(gender='F').count()
    
    # Day Scholar Statistics
    total_day_scholars = Student.query.filter_by(admission_type='day_scholar').count()
    total_day_scholars_male = Student.query.filter_by(admission_type='day_scholar', gender='M').count()
    total_day_scholars_female = Student.query.filter_by(admission_type='day_scholar', gender='F').count()
    
    # Hostel Statistics
    total_hostel = Student.query.filter_by(admission_type='hostel').count()
    total_hostel_male = Student.query.filter_by(admission_type='hostel', gender='M').count()
    total_hostel_female = Student.query.filter_by(admission_type='hostel', gender='F').count()
    
    # Course statistics
    total_courses = Course.query.count()
    
    # New admissions this month
    today = datetime.utcnow().date()
    month_start = today.replace(day=1)
    new_admissions_this_month = Student.query.filter(
        Student.admission_date >= month_start
    ).count()
    
    # Fees statistics
    this_month_payments = Payment.query.filter(
        db.func.date(Payment.payment_date) >= month_start
    ).all()
    fees_collected_month = sum(p.amount_paid for p in this_month_payments)
    
    # Calculate fees pending
    total_fee = sum(c.fee * Enrollment.query.filter_by(course_id=c.id).count()
                   for c in Course.query.all())
    fees_pending_month = total_fee - fees_collected_month
    
    # Attendance today
    today_attendance = Attendance.query.filter(
        db.func.date(Attendance.date) == today
    ).all()
    total_present = sum(1 for a in today_attendance if a.status == 'present')
    attendance_percent = (total_present / len(today_attendance) * 100) if today_attendance else 0
    
    # Students per course (for chart) with gender breakdown
    courses_data = []
    for course in Course.query.all():
        # Get male and female student counts for this course
        male_students = db.session.query(db.func.count(Student.id)).join(
            Enrollment
        ).filter(
            Enrollment.course_id == course.id,
            Student.gender == 'M'
        ).scalar()
        
        female_students = db.session.query(db.func.count(Student.id)).join(
            Enrollment
        ).filter(
            Enrollment.course_id == course.id,
            Student.gender == 'F'
        ).scalar()
        
        courses_data.append({
            'name': course.name,
            'total': course.student_count,
            'male': male_students or 0,
            'female': female_students or 0
        })
    
    # Sort by name for consistent display
    courses_data.sort(key=lambda x: x['name'])
    
    # Fee collection trend (last 6 months)
    fee_trend = []
    for i in range(6):
        month_date = today - timedelta(days=i*30)
        month_start_check = month_date.replace(day=1)
        month_end_check = (month_start_check + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        month_total = db.session.query(db.func.sum(Payment.amount_paid)).filter(
            db.func.date(Payment.payment_date) >= month_start_check,
            db.func.date(Payment.payment_date) <= month_end_check
        ).scalar() or 0
        
        fee_trend.append({
            'month': month_date.strftime('%b'),
            'amount': float(month_total)
        })
    
    fee_trend.reverse()
    
    return jsonify({
        'total_students': total_students,
        'total_male': total_male,
        'total_female': total_female,
        'total_day_scholars': total_day_scholars,
        'total_day_scholars_male': total_day_scholars_male,
        'total_day_scholars_female': total_day_scholars_female,
        'total_hostel': total_hostel,
        'total_hostel_male': total_hostel_male,
        'total_hostel_female': total_hostel_female,
        'total_courses': total_courses,
        'new_admissions_this_month': new_admissions_this_month,
        'fees_collected_month': float(fees_collected_month),
        'fees_pending_month': float(max(0, fees_pending_month)),
        'attendance_percent': round(attendance_percent, 2),
        'courses_data': courses_data,
        'fee_trend': fee_trend
    })
