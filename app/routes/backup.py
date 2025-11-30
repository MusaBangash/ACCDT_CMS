"""
Backup and database management routes.
"""

from flask import Blueprint, render_template, jsonify, send_file, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.decorators import admin_required
from app.models import db, Student, Course, Enrollment, Attendance, Payment, PaymentCategory, User
import json
import os
from datetime import datetime
from io import BytesIO, StringIO
import csv

backup_bp = Blueprint('backup', __name__, url_prefix='/backup')


@backup_bp.route('/')
@admin_required
def index():
    """Backup and database management page"""
    # Get statistics
    stats = {
        'students': Student.query.count(),
        'courses': Course.query.count(),
        'enrollments': Enrollment.query.count(),
        'attendance': Attendance.query.count(),
        'payments': Payment.query.count(),
        'payment_categories': PaymentCategory.query.count(),
        'users': User.query.count(),
    }
    
    total_records = sum(stats.values())
    
    return render_template('backup_dashboard.html', stats=stats, total_records=total_records)


@backup_bp.route('/download/students')
@admin_required
def download_students():
    """Download students backup as CSV"""
    try:
        students = Student.query.all()
        
        # Create CSV in memory using StringIO
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Full Name', 'Registration Number', 'Phone', 'Address', 'Category', 'Status', 'Date of Birth', 'Created At'])
        
        for student in students:
            writer.writerow([
                student.id,
                student.full_name,
                student.registration_number,
                student.phone or '',
                student.address or '',
                student.category or '',
                student.status or '',
                student.date_of_birth.strftime('%d-%m-%Y') if student.date_of_birth else '',
                student.created_at.strftime('%d-%m-%Y %H:%M:%S') if student.created_at else '',
            ])
        
        # Convert to BytesIO with UTF-8 BOM
        csv_bytes = BytesIO()
        csv_bytes.write('\ufeff'.encode('utf-8'))  # UTF-8 BOM for Excel
        csv_bytes.write(output.getvalue().encode('utf-8'))
        csv_bytes.seek(0)
        
        return send_file(
            csv_bytes,
            as_attachment=True,
            download_name=f"students_backup_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.csv",
            mimetype='text/csv'
        )
    except Exception as e:
        flash(f'Error downloading students: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))


@backup_bp.route('/download/courses')
@admin_required
def download_courses():
    """Download courses backup as CSV"""
    try:
        courses = Course.query.all()
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Course Name', 'Description', 'Instructor Name', 'Instructor Contact', 'Fee', 'Seats', 'Created At'])
        
        for course in courses:
            writer.writerow([
                course.id,
                course.name,
                course.description or '',
                course.instructor_name or '',
                course.instructor_contact or '',
                course.fee,
                course.seats,
                course.created_at.strftime('%d-%m-%Y %H:%M:%S') if course.created_at else '',
            ])
        
        # Convert to BytesIO with UTF-8 BOM
        csv_bytes = BytesIO()
        csv_bytes.write('\ufeff'.encode('utf-8'))
        csv_bytes.write(output.getvalue().encode('utf-8'))
        csv_bytes.seek(0)
        
        return send_file(
            csv_bytes,
            as_attachment=True,
            download_name=f"courses_backup_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.csv",
            mimetype='text/csv'
        )
    except Exception as e:
        flash(f'Error downloading courses: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))


@backup_bp.route('/download/payments')
@admin_required
def download_payments():
    """Download payments backup as CSV"""
    try:
        payments = Payment.query.all()
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Student', 'Course', 'Amount Due', 'Amount Paid', 'Security Fees', 'Admission Fees', 'Status', 'Method', 'Payment Date', 'Reference No', 'Created At'])
        
        for payment in payments:
            writer.writerow([
                payment.id,
                payment.student.full_name if payment.student else '',
                payment.course.name if payment.course else '',
                payment.amount_due,
                payment.amount_paid,
                payment.security_fees or 0,
                payment.admission_fees or 0,
                payment.status,
                payment.method,
                payment.payment_date.strftime('%d-%m-%Y') if payment.payment_date else '',
                payment.reference_no or '',
                payment.created_at.strftime('%d-%m-%Y %H:%M:%S') if payment.created_at else '',
            ])
        
        # Convert to BytesIO with UTF-8 BOM
        csv_bytes = BytesIO()
        csv_bytes.write('\ufeff'.encode('utf-8'))
        csv_bytes.write(output.getvalue().encode('utf-8'))
        csv_bytes.seek(0)
        
        return send_file(
            csv_bytes,
            as_attachment=True,
            download_name=f"payments_backup_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.csv",
            mimetype='text/csv'
        )
    except Exception as e:
        flash(f'Error downloading payments: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))


@backup_bp.route('/download/attendance')
@admin_required
def download_attendance():
    """Download attendance backup as CSV"""
    try:
        attendance = Attendance.query.all()
        
        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['ID', 'Student', 'Course', 'Date', 'Status', 'Notes', 'Created At'])
        
        for record in attendance:
            writer.writerow([
                record.id,
                record.student.full_name if record.student else '',
                record.course.name if record.course else '',
                record.attendance_date.strftime('%d-%m-%Y') if record.attendance_date else '',
                record.status,
                record.notes or '',
                record.created_at.strftime('%d-%m-%Y %H:%M:%S') if record.created_at else '',
            ])
        
        # Convert to BytesIO with UTF-8 BOM
        csv_bytes = BytesIO()
        csv_bytes.write('\ufeff'.encode('utf-8'))
        csv_bytes.write(output.getvalue().encode('utf-8'))
        csv_bytes.seek(0)
        
        return send_file(
            csv_bytes,
            as_attachment=True,
            download_name=f"attendance_backup_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.csv",
            mimetype='text/csv'
        )
    except Exception as e:
        flash(f'Error downloading attendance: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))


@backup_bp.route('/download/all')
@admin_required
def download_all():
    """Download complete database backup as JSON"""
    try:
        backup_data = {
            'backup_date': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            'students': [],
            'courses': [],
            'enrollments': [],
            'payments': [],
            'attendance': [],
            'payment_categories': [],
        }
        
        # Students
        for student in Student.query.all():
            backup_data['students'].append({
                'id': student.id,
                'full_name': student.full_name,
                'registration_number': student.registration_number,
                'phone': student.phone,
                'address': student.address,
                'category': student.category,
                'status': student.status,
                'date_of_birth': student.date_of_birth.strftime('%d-%m-%Y') if student.date_of_birth else None,
            })
        
        # Courses
        for course in Course.query.all():
            backup_data['courses'].append({
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'instructor_name': course.instructor_name,
                'instructor_contact': course.instructor_contact,
                'fee': course.fee,
                'seats': course.seats,
            })
        
        # Enrollments
        for enrollment in Enrollment.query.all():
            backup_data['enrollments'].append({
                'id': enrollment.id,
                'student_id': enrollment.student_id,
                'course_id': enrollment.course_id,
                'enroll_date': enrollment.enroll_date.strftime('%d-%m-%Y') if enrollment.enroll_date else None,
            })
        
        # Payments
        for payment in Payment.query.all():
            backup_data['payments'].append({
                'id': payment.id,
                'student_id': payment.student_id,
                'course_id': payment.course_id,
                'amount_due': payment.amount_due,
                'amount_paid': payment.amount_paid,
                'security_fees': payment.security_fees,
                'admission_fees': payment.admission_fees,
                'status': payment.status,
                'method': payment.method,
                'reference_no': payment.reference_no,
                'payment_date': payment.payment_date.strftime('%d-%m-%Y') if payment.payment_date else None,
            })
        
        # Attendance
        for attendance in Attendance.query.all():
            backup_data['attendance'].append({
                'id': attendance.id,
                'student_id': attendance.student_id,
                'course_id': attendance.course_id,
                'attendance_date': attendance.attendance_date.strftime('%d-%m-%Y') if attendance.attendance_date else None,
                'status': attendance.status,
                'notes': attendance.notes,
            })
        
        # Payment Categories
        for category in PaymentCategory.query.all():
            backup_data['payment_categories'].append({
                'id': category.id,
                'name': category.name,
                'description': category.description,
            })
        
        # Create JSON file
        output = BytesIO()
        output.write(json.dumps(backup_data, indent=2, ensure_ascii=False).encode('utf-8'))
        output.seek(0)
        
        return send_file(
            output,
            as_attachment=True,
            download_name=f"complete_backup_{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.json",
            mimetype='application/json'
        )
    except Exception as e:
        flash(f'Error downloading backup: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))


@backup_bp.route('/clear', methods=['POST'])
@admin_required
def clear_database():
    """Clear specific database tables"""
    try:
        table = request.form.get('table', '').lower()
        
        if table == 'payments':
            Payment.query.delete()
            db.session.commit()
            flash('✓ All payments deleted successfully', 'success')
        elif table == 'attendance':
            Attendance.query.delete()
            db.session.commit()
            flash('✓ All attendance records deleted successfully', 'success')
        elif table == 'enrollments':
            Enrollment.query.delete()
            db.session.commit()
            flash('✓ All enrollments deleted successfully', 'success')
        elif table == 'courses':
            Course.query.delete()
            db.session.commit()
            flash('✓ All courses deleted successfully', 'success')
        elif table == 'students':
            Student.query.delete()
            db.session.commit()
            flash('✓ All students deleted successfully', 'success')
        elif table == 'all':
            # Delete all data except admin user
            Attendance.query.delete()
            Payment.query.delete()
            Enrollment.query.delete()
            Course.query.delete()
            PaymentCategory.query.delete()
            Student.query.delete()
            
            # Delete non-admin users
            non_admin_users = User.query.filter(User.role != 'admin').all()
            for user in non_admin_users:
                db.session.delete(user)
            
            db.session.commit()
            flash('✓ All data cleared (admin user retained)', 'success')
        else:
            flash('Invalid table selection', 'warning')
        
        return redirect(url_for('backup.index'))
    
    except Exception as e:
        db.session.rollback()
        flash(f'Error clearing database: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))


@backup_bp.route('/restore', methods=['POST'])
@admin_required
def restore_database():
    """Restore database from JSON backup file"""
    try:
        # Check if file was uploaded
        if 'backup_file' not in request.files:
            flash('No file selected for restoration', 'warning')
            return redirect(url_for('backup.index'))
        
        file = request.files['backup_file']
        if file.filename == '':
            flash('No file selected for restoration', 'warning')
            return redirect(url_for('backup.index'))
        
        if not file.filename.endswith('.json'):
            flash('Only JSON backup files are supported', 'danger')
            return redirect(url_for('backup.index'))
        
        # Read and parse the JSON file
        backup_content = file.read().decode('utf-8')
        backup_data = json.loads(backup_content)
        
        # Validate backup structure
        required_keys = {'students', 'courses', 'enrollments', 'payments', 'attendance', 'payment_categories'}
        if not all(key in backup_data for key in required_keys):
            flash('Invalid backup file format', 'danger')
            return redirect(url_for('backup.index'))
        
        # Clear existing data first (except admin users)
        Attendance.query.delete()
        Payment.query.delete()
        Enrollment.query.delete()
        Course.query.delete()
        PaymentCategory.query.delete()
        Student.query.delete()
        
        # Delete non-admin users
        non_admin_users = User.query.filter(User.role != 'admin').all()
        for user in non_admin_users:
            db.session.delete(user)
        
        db.session.commit()
        
        # Restore Payment Categories first (no dependencies)
        for category_data in backup_data.get('payment_categories', []):
            category = PaymentCategory(
                name=category_data.get('name'),
                description=category_data.get('description')
            )
            db.session.add(category)
        db.session.commit()
        
        # Restore Courses (no dependencies)
        course_map = {}
        for course_data in backup_data.get('courses', []):
            course = Course(
                name=course_data.get('name'),
                description=course_data.get('description'),
                instructor_name=course_data.get('instructor_name'),
                instructor_contact=course_data.get('instructor_contact'),
                fee=course_data.get('fee'),
                seats=course_data.get('seats')
            )
            db.session.add(course)
            db.session.flush()
            course_map[course_data.get('id')] = course.id
        db.session.commit()
        
        # Restore Students (no dependencies)
        student_map = {}
        for student_data in backup_data.get('students', []):
            # Parse date fields
            dob = None
            if student_data.get('date_of_birth'):
                try:
                    dob = datetime.strptime(student_data.get('date_of_birth'), '%d-%m-%Y').date()
                except:
                    dob = None
            
            student = Student(
                registration_number=student_data.get('registration_number'),
                first_name=student_data.get('full_name', '').split()[0] if student_data.get('full_name') else '',
                last_name=student_data.get('full_name', '').split()[-1] if len(student_data.get('full_name', '').split()) > 1 else '',
                gender='M',
                admission_type='day_scholar',
                date_of_birth=dob,
                phone=student_data.get('phone'),
                address=student_data.get('address'),
                category=student_data.get('category', 'regular'),
                status=student_data.get('status', 'active')
            )
            db.session.add(student)
            db.session.flush()
            student_map[student_data.get('id')] = student.id
        db.session.commit()
        
        # Restore Enrollments (depends on students and courses)
        for enrollment_data in backup_data.get('enrollments', []):
            student_id = student_map.get(enrollment_data.get('student_id'))
            course_id = course_map.get(enrollment_data.get('course_id'))
            
            if student_id and course_id:
                # Parse date
                enroll_date = datetime.utcnow()
                if enrollment_data.get('enroll_date'):
                    try:
                        enroll_date = datetime.strptime(enrollment_data.get('enroll_date'), '%d-%m-%Y')
                    except:
                        enroll_date = datetime.utcnow()
                
                enrollment = Enrollment(
                    student_id=student_id,
                    course_id=course_id,
                    enroll_date=enroll_date
                )
                db.session.add(enrollment)
        db.session.commit()
        
        # Restore Payments (depends on students and courses)
        for payment_data in backup_data.get('payments', []):
            student_id = student_map.get(payment_data.get('student_id'))
            course_id = course_map.get(payment_data.get('course_id'))
            
            if student_id and course_id:
                # Parse date
                payment_date = None
                if payment_data.get('payment_date'):
                    try:
                        payment_date = datetime.strptime(payment_data.get('payment_date'), '%d-%m-%Y').date()
                    except:
                        payment_date = None
                
                payment = Payment(
                    student_id=student_id,
                    course_id=course_id,
                    amount_due=payment_data.get('amount_due', 0),
                    amount_paid=payment_data.get('amount_paid', 0),
                    security_fees=payment_data.get('security_fees'),
                    admission_fees=payment_data.get('admission_fees'),
                    status=payment_data.get('status', 'pending'),
                    method=payment_data.get('method'),
                    reference_no=payment_data.get('reference_no'),
                    payment_date=payment_date
                )
                db.session.add(payment)
        db.session.commit()
        
        # Restore Attendance (depends on students and courses)
        for attendance_data in backup_data.get('attendance', []):
            student_id = student_map.get(attendance_data.get('student_id'))
            course_id = course_map.get(attendance_data.get('course_id'))
            
            if student_id and course_id:
                # Parse date
                att_date = None
                if attendance_data.get('attendance_date'):
                    try:
                        att_date = datetime.strptime(attendance_data.get('attendance_date'), '%d-%m-%Y').date()
                    except:
                        att_date = datetime.utcnow().date()
                
                attendance = Attendance(
                    student_id=student_id,
                    course_id=course_id,
                    attendance_date=att_date or datetime.utcnow().date(),
                    status=attendance_data.get('status', 'present'),
                    notes=attendance_data.get('notes')
                )
                db.session.add(attendance)
        db.session.commit()
        
        flash('✓ Database restored successfully from backup!', 'success')
        return redirect(url_for('backup.index'))
    
    except json.JSONDecodeError:
        flash('Invalid JSON file format', 'danger')
        return redirect(url_for('backup.index'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error restoring database: {str(e)}', 'danger')
        return redirect(url_for('backup.index'))
