"""
Attendance marking and reporting routes.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy import and_, func, extract

from app.models import db, Attendance, Course, Student, Enrollment, User
from app.decorators import teacher_required, admin_required
from app.forms import AttendanceForm, AttendanceRecordForm

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')


def get_week_date_range(date_obj):
    """Get the start and end dates of the week containing the given date"""
    start = date_obj - timedelta(days=date_obj.weekday())
    end = start + timedelta(days=6)
    return start, end


def get_month_date_range(date_obj):
    """Get the start and end dates of the month containing the given date"""
    start = date_obj.replace(day=1)
    end = start + relativedelta(months=1) - timedelta(days=1)
    return start, end


@attendance_bp.route('/', methods=['GET', 'POST'])
@teacher_required
def mark_attendance():
    """Mark attendance for students in a course"""
    form = AttendanceForm()
    
    # Populate course choices
    form.course.choices = [(0, 'Select a Course')] + [
        (c.id, c.name) for c in Course.query.order_by(Course.name).all()
    ]
    
    students = []
    selected_course = None
    selected_date = None
    attendance_records = {}
    
    if form.validate_on_submit():
        selected_course = Course.query.get(form.course.data)
        selected_date = form.date.data
        
        if not selected_course:
            flash('Course not found', 'error')
            return redirect(url_for('attendance.mark_attendance'))
        
        # Get enrolled students for this course
        enrollments = Enrollment.query.filter_by(course_id=selected_course.id).all()
        students = [e.student for e in enrollments]
        
        # Get existing attendance records for this date
        existing = Attendance.query.filter(
            and_(
                Attendance.course_id == selected_course.id,
                Attendance.date == selected_date
            )
        ).all()
        attendance_records = {a.student_id: a.status for a in existing}
    
    return render_template('attendance.html', 
                         form=form, 
                         students=students,
                         selected_course=selected_course,
                         selected_date=selected_date,
                         attendance_records=attendance_records)


@attendance_bp.route('/record/<int:student_id>/<int:course_id>', methods=['POST'])
@teacher_required
def record_attendance(student_id, course_id):
    """Record attendance for a single student"""
    try:
        date_str = request.form.get('date')
        status = request.form.get('status')
        
        if not date_str or not status:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        attendance_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Check if student is enrolled in the course
        enrollment = Enrollment.query.filter_by(
            student_id=student_id,
            course_id=course_id
        ).first()
        
        if not enrollment:
            return jsonify({'success': False, 'error': 'Student not enrolled in this course'}), 400
        
        # Find or create attendance record
        attendance = Attendance.query.filter(
            and_(
                Attendance.student_id == student_id,
                Attendance.course_id == course_id,
                Attendance.date == attendance_date
            )
        ).first()
        
        if not attendance:
            attendance = Attendance(
                student_id=student_id,
                course_id=course_id,
                date=attendance_date,
                status=status,
                marked_by_user_id=current_user.id
            )
            db.session.add(attendance)
        else:
            attendance.status = status
            attendance.marked_by_user_id = current_user.id
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance recorded'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@attendance_bp.route('/bulk-save', methods=['POST'])
@teacher_required
def bulk_save_attendance():
    """Save attendance for multiple students at once"""
    try:
        data = request.get_json()
        course_id = data.get('course_id')
        attendance_date = datetime.strptime(data.get('date'), '%Y-%m-%d').date()
        records = data.get('records', [])
        
        if not course_id or not attendance_date or not records:
            return jsonify({'success': False, 'error': 'Missing required data'}), 400
        
        course = Course.query.get(course_id)
        if not course:
            return jsonify({'success': False, 'error': 'Course not found'}), 404
        
        for record in records:
            student_id = record.get('student_id')
            status = record.get('status')
            
            if not student_id or not status:
                continue
            
            # Find or create attendance record
            attendance = Attendance.query.filter(
                and_(
                    Attendance.student_id == student_id,
                    Attendance.course_id == course_id,
                    Attendance.date == attendance_date
                )
            ).first()
            
            if not attendance:
                attendance = Attendance(
                    student_id=student_id,
                    course_id=course_id,
                    date=attendance_date,
                    status=status,
                    marked_by_user_id=current_user.id
                )
                db.session.add(attendance)
            else:
                attendance.status = status
                attendance.marked_by_user_id = current_user.id
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Attendance saved successfully'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500


@attendance_bp.route('/report')
@login_required
def attendance_report():
    """View attendance report"""
    report_type = request.args.get('type', 'course')  # course or student
    item_id = request.args.get('item_id', type=int)
    
    data = []
    title = ''
    
    # Get all courses and students for the selector
    courses = Course.query.order_by(Course.name).all()
    students = Student.query.order_by(Student.first_name, Student.last_name).all()
    
    if report_type == 'course' and item_id:
        course = Course.query.get(item_id)
        if not course:
            flash('Course not found', 'error')
            return redirect(url_for('dashboard.index'))
        
        title = f'Attendance Report - {course.name}'
        
        # Get attendance statistics for this course
        enrollments = Enrollment.query.filter_by(course_id=item_id).all()
        
        for enrollment in enrollments:
            student = enrollment.student
            total_classes = Attendance.query.filter_by(
                course_id=item_id
            ).distinct(Attendance.date).count()
            
            present_count = Attendance.query.filter(
                and_(
                    Attendance.student_id == student.id,
                    Attendance.course_id == item_id,
                    Attendance.status == 'present'
                )
            ).count()
            
            absent_count = Attendance.query.filter(
                and_(
                    Attendance.student_id == student.id,
                    Attendance.course_id == item_id,
                    Attendance.status == 'absent'
                )
            ).count()
            
            leave_count = Attendance.query.filter(
                and_(
                    Attendance.student_id == student.id,
                    Attendance.course_id == item_id,
                    Attendance.status == 'leave'
                )
            ).count()
            
            percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
            
            data.append({
                'student': student,
                'total_classes': total_classes,
                'present': present_count,
                'absent': absent_count,
                'leave': leave_count,
                'percentage': round(percentage, 2)
            })
    
    elif report_type == 'student' and item_id:
        student = Student.query.get(item_id)
        if not student:
            flash('Student not found', 'error')
            return redirect(url_for('dashboard.index'))
        
        title = f'Attendance Report - {student.full_name}'
        
        # Get all courses this student is enrolled in
        enrollments = Enrollment.query.filter_by(student_id=item_id).all()
        
        for enrollment in enrollments:
            course = enrollment.course
            
            total_classes = Attendance.query.filter_by(
                course_id=course.id
            ).distinct(Attendance.date).count()
            
            present_count = Attendance.query.filter(
                and_(
                    Attendance.student_id == item_id,
                    Attendance.course_id == course.id,
                    Attendance.status == 'present'
                )
            ).count()
            
            absent_count = Attendance.query.filter(
                and_(
                    Attendance.student_id == item_id,
                    Attendance.course_id == course.id,
                    Attendance.status == 'absent'
                )
            ).count()
            
            leave_count = Attendance.query.filter(
                and_(
                    Attendance.student_id == item_id,
                    Attendance.course_id == course.id,
                    Attendance.status == 'leave'
                )
            ).count()
            
            percentage = (present_count / total_classes * 100) if total_classes > 0 else 0
            
            data.append({
                'course': course,
                'total_classes': total_classes,
                'present': present_count,
                'absent': absent_count,
                'leave': leave_count,
                'percentage': round(percentage, 2)
            })
    
    return render_template('attendance_report.html', 
                         report_type=report_type,
                         title=title,
                         data=data,
                         courses=courses,
                         students=students)


@attendance_bp.route('/course/<int:course_id>/attendance-history')
@login_required
def course_attendance_history(course_id):
    """View detailed attendance history for a course"""
    course = Course.query.get_or_404(course_id)
    page = request.args.get('page', 1, type=int)
    
    # Get all attendance records for this course, paginated by date
    attendance_query = Attendance.query.filter_by(course_id=course_id)\
        .order_by(Attendance.date.desc())\
        .paginate(page=page, per_page=20)
    
    return render_template('course_attendance_history.html',
                         course=course,
                         attendance=attendance_query)


@attendance_bp.route('/summary')
@login_required
def attendance_summary():
    """View attendance summary by week, month, or custom date range"""
    report_type = request.args.get('type', 'month')  # week, month, custom
    course_id = request.args.get('course_id', type=int)
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    courses = Course.query.order_by(Course.name).all()
    
    if not course_id and courses:
        course_id = courses[0].id
    
    course = Course.query.get(course_id) if course_id else None
    summary_data = []
    date_range = {}
    
    if course:
        today = date.today()
        
        # Determine date range based on report type
        if report_type == 'week':
            start_date, end_date = get_week_date_range(today)
            date_range['start'] = start_date
            date_range['end'] = end_date
        elif report_type == 'month':
            start_date, end_date = get_month_date_range(today)
            date_range['start'] = start_date
            date_range['end'] = end_date
        elif report_type == 'custom' and start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            date_range['start'] = start_date
            date_range['end'] = end_date
        else:
            start_date, end_date = get_month_date_range(today)
            date_range['start'] = start_date
            date_range['end'] = end_date
        
        # Get enrolled students
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        
        for enrollment in enrollments:
            student = enrollment.student
            
            # Count attendance in date range
            present = Attendance.query.filter(
                and_(
                    Attendance.student_id == student.id,
                    Attendance.course_id == course_id,
                    Attendance.status == 'present',
                    Attendance.date >= start_date,
                    Attendance.date <= end_date
                )
            ).count()
            
            absent = Attendance.query.filter(
                and_(
                    Attendance.student_id == student.id,
                    Attendance.course_id == course_id,
                    Attendance.status == 'absent',
                    Attendance.date >= start_date,
                    Attendance.date <= end_date
                )
            ).count()
            
            leave = Attendance.query.filter(
                and_(
                    Attendance.student_id == student.id,
                    Attendance.course_id == course_id,
                    Attendance.status == 'leave',
                    Attendance.date >= start_date,
                    Attendance.date <= end_date
                )
            ).count()
            
            total = present + absent + leave
            percentage = (present / total * 100) if total > 0 else 0
            
            summary_data.append({
                'student': student,
                'present': present,
                'absent': absent,
                'leave': leave,
                'total': total,
                'percentage': round(percentage, 2)
            })
    
    return render_template('attendance_summary.html',
                         courses=courses,
                         selected_course=course,
                         report_type=report_type,
                         date_range=date_range,
                         summary_data=summary_data)


@attendance_bp.route('/print/course/<int:course_id>')
@login_required
def print_course_attendance(course_id):
    """Print attendance report for a course"""
    report_type = request.args.get('type', 'month')  # week, month, custom
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    
    course = Course.query.get_or_404(course_id)
    today = date.today()
    
    # Determine date range
    if report_type == 'week':
        start_date, end_date = get_week_date_range(today)
    elif report_type == 'month':
        start_date, end_date = get_month_date_range(today)
    elif report_type == 'custom' and start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        start_date, end_date = get_month_date_range(today)
    
    # Get all attendance records for this period and course
    attendance_records = Attendance.query.filter(
        and_(
            Attendance.course_id == course_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        )
    ).order_by(Attendance.date, Attendance.student_id).all()
    
    # Get enrolled students
    enrollments = Enrollment.query.filter_by(course_id=course_id).all()
    students = [e.student for e in enrollments]
    
    # Build summary data
    summary_data = []
    for student in students:
        present = sum(1 for r in attendance_records 
                     if r.student_id == student.id and r.status == 'present')
        absent = sum(1 for r in attendance_records 
                    if r.student_id == student.id and r.status == 'absent')
        leave = sum(1 for r in attendance_records 
                   if r.student_id == student.id and r.status == 'leave')
        total = present + absent + leave
        percentage = (present / total * 100) if total > 0 else 0
        
        summary_data.append({
            'student': student,
            'present': present,
            'absent': absent,
            'leave': leave,
            'total': total,
            'percentage': round(percentage, 2)
        })
    
    return render_template('attendance_print.html',
                         course=course,
                         report_type=report_type,
                         start_date=start_date,
                         end_date=end_date,
                         summary_data=summary_data,
                         attendance_records=attendance_records,
                         now=datetime.now())
