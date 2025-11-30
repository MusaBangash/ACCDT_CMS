"""
Student CRUD routes and bulk upload.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import login_required, current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from sqlalchemy import desc

from app.models import db, Student, Course, Enrollment
from app.forms import StudentRegistrationForm, StudentStatusForm
from app.decorators import admin_required, roles_required
from app.utils import save_upload_file, delete_upload_file, paginate_query

students_bp = Blueprint('students', __name__, url_prefix='/students')


@students_bp.route('/')
@login_required
def list_students():
    """List all students with pagination and search"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Student.query
    
    # Search filter
    if search:
        query = query.filter(
            db.or_(
                Student.first_name.ilike(f'%{search}%'),
                Student.last_name.ilike(f'%{search}%'),
                Student.cnic.ilike(f'%{search}%'),
                Student.phone.ilike(f'%{search}%')
            )
        )
    
    # Sort by latest first
    query = query.order_by(desc(Student.id))
    
    # Paginate
    items, total, pages = paginate_query(query, page, per_page=10)
    students = items
    
    return render_template('students.html', students=students, page=page, pages=pages, 
                          total=total, search=search)


@students_bp.route('/register', methods=['GET', 'POST'])
def register_student():
    """Register new student (public registration)"""
    form = StudentRegistrationForm()
    courses = Course.query.all()
    
    if form.validate_on_submit():
        try:
            # Create new student
            student = Student(
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
                gender=form.gender.data,
                date_of_birth=form.date_of_birth.data,
                phone=form.phone.data,
                address=form.address.data.strip(),
                city=form.city.data.strip(),
                admission_type=form.admission_type.data,
                category=form.category.data or 'regular',
                cnic=form.cnic.data.strip(),
                blood_group=form.blood_group.data or None,
                nationality=form.nationality.data.strip(),
                emergency_contact=form.emergency_contact.data or None,
                permanent_address=form.permanent_address.data.strip(),
                last_qualification=form.last_qualification.data or None,
                current_qualification=form.current_qualification.data or None,
                status='active'
            )
            
            # Store guardian info in a field (you can expand models if needed)
            # For now, we'll store it as part of student record
            student.guardian_name = form.guardian_name.data.strip()
            student.guardian_cnic = form.guardian_cnic.data.strip()
            
            db.session.add(student)
            db.session.flush()  # Get student ID
            
            # Handle registration number - manual or auto-generate
            if form.registration_number.data and form.registration_number.data.strip():
                student.registration_number = form.registration_number.data.strip()
            else:
                student.generate_registration_number()
            
            # Handle photo upload
            if form.photo.data:
                photo_file = form.photo.data
                photo_path = save_upload_file(photo_file, folder='students')
                student.photo_path = photo_path
            
            # Enroll student in selected courses
            if form.course_id.data:
                for course_id in form.course_id.data:
                    course = Course.query.get(course_id)
                    if course and not course.is_full:
                        enrollment = Enrollment(
                            student_id=student.id,
                            course_id=course.id,
                            enroll_date=datetime.utcnow()
                        )
                        db.session.add(enrollment)
                    else:
                        course_name = course.name if course else 'Unknown'
                        flash(f'Course {course_name} is full. Student not enrolled in this course.', 'warning')
            
            db.session.commit()
            flash(f'Student {student.full_name} registered successfully!', 'success')
            return redirect(url_for('students.view_student', student_id=student.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error registering student: {str(e)}', 'danger')
    
    return render_template('student_form.html', form=form, courses=courses)


@students_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create_student():
    """Create new student (admin only)"""
    form = StudentRegistrationForm()
    courses = Course.query.all()
    
    if form.validate_on_submit():
        try:
            student = Student(
                first_name=form.first_name.data.strip(),
                last_name=form.last_name.data.strip(),
                gender=form.gender.data,
                date_of_birth=form.date_of_birth.data,
                phone=form.phone.data,
                address=form.address.data.strip(),
                city=form.city.data.strip(),
                admission_type=form.admission_type.data,
                category=form.category.data or 'regular',
                cnic=form.cnic.data.strip(),
                blood_group=form.blood_group.data or None,
                nationality=form.nationality.data.strip(),
                emergency_contact=form.emergency_contact.data or None,
                permanent_address=form.permanent_address.data.strip(),
                last_qualification=form.last_qualification.data or None,
                current_qualification=form.current_qualification.data or None,
                status='active'
            )
            
            student.guardian_name = form.guardian_name.data.strip()
            student.guardian_cnic = form.guardian_cnic.data.strip()
            
            db.session.add(student)
            db.session.flush()
            
            # Handle registration number - manual or auto-generate
            if form.registration_number.data and form.registration_number.data.strip():
                student.registration_number = form.registration_number.data.strip()
            else:
                student.generate_registration_number()
            
            # Handle photo upload
            if form.photo.data:
                photo_file = form.photo.data
                photo_path = save_upload_file(photo_file, folder='students')
                student.photo_path = photo_path
            
            # Handle other document uploads
            documents = [
                ('character_certificate', form.character_certificate.data),
                ('cnic_copy', form.cnic_copy.data),
                ('qualification_certificate', form.qualification_certificate.data)
            ]
            
            for doc_name, doc_file in documents:
                if doc_file:
                    doc_path = save_upload_file(doc_file, folder='documents')
                    # You can store document paths in a separate model if needed
            
            # Enroll student in selected courses
            if form.course_id.data:
                for course_id in form.course_id.data:
                    course = Course.query.get(course_id)
                    if course and not course.is_full:
                        enrollment = Enrollment(
                            student_id=student.id,
                            course_id=course.id,
                            enroll_date=datetime.utcnow()
                        )
                        db.session.add(enrollment)
            
            db.session.commit()
            flash(f'Student {student.full_name} created successfully!', 'success')
            return redirect(url_for('students.list_students'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating student: {str(e)}', 'danger')
    
    return render_template('student_form.html', form=form, courses=courses, is_new=True)


@students_bp.route('/<int:student_id>')
@login_required
def view_student(student_id):
    """View student details"""
    student = Student.query.get_or_404(student_id)
    enrollments = student.enrollments.all()
    
    return render_template('student_detail.html', student=student, enrollments=enrollments)


@students_bp.route('/<int:student_id>/print')
@login_required
def print_student(student_id):
    """Print student profile"""
    student = Student.query.get_or_404(student_id)
    enrollments = student.enrollments.all()
    
    return render_template('student_print.html', student=student, enrollments=enrollments, now=datetime.now())


@students_bp.route('/print-list')
@login_required
def print_student_list():
    """Print all students list with filters"""
    search = request.args.get('search', '', type=str)
    status_filter = request.args.get('status', '', type=str)
    course_filter = request.args.get('course', '', type=str)
    timing_filter = request.args.get('timing', '', type=str)
    
    query = Student.query
    
    # Search filter
    if search:
        query = query.filter(
            db.or_(
                Student.first_name.ilike(f'%{search}%'),
                Student.last_name.ilike(f'%{search}%'),
                Student.cnic.ilike(f'%{search}%'),
                Student.phone.ilike(f'%{search}%')
            )
        )
    
    # Status filter
    if status_filter:
        query = query.filter(Student.status == status_filter)
    
    # Admission Type (timing) filter
    if timing_filter:
        query = query.filter(Student.admission_type == timing_filter)
    
    # Course filter
    if course_filter:
        query = query.join(Student.enrollments).join(Enrollment.course).filter(Course.id == int(course_filter))
    
    # Sort by registration number
    query = query.order_by(Student.registration_number)
    
    # Get all for print (no pagination)
    students = query.all()
    
    # Get all courses for filter dropdown
    courses = Course.query.all()
    
    return render_template('student_list_print.html', 
                         students=students, 
                         search=search,
                         status_filter=status_filter,
                         course_filter=course_filter,
                         timing_filter=timing_filter,
                         courses=courses,
                         now=datetime.now())


@students_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_student(student_id):
    """Edit student details"""
    student = Student.query.get_or_404(student_id)
    form = StudentRegistrationForm()
    courses = Course.query.all()
    
    if form.validate_on_submit():
        try:
            student.first_name = form.first_name.data.strip()
            student.last_name = form.last_name.data.strip()
            student.gender = form.gender.data
            student.date_of_birth = form.date_of_birth.data
            student.phone = form.phone.data
            student.address = form.address.data.strip()
            student.city = form.city.data.strip()
            student.admission_type = form.admission_type.data
            student.category = form.category.data or 'regular'
            student.cnic = form.cnic.data.strip()
            student.blood_group = form.blood_group.data or None
            student.nationality = form.nationality.data.strip()
            student.emergency_contact = form.emergency_contact.data or None
            student.permanent_address = form.permanent_address.data.strip()
            student.last_qualification = form.last_qualification.data or None
            student.current_qualification = form.current_qualification.data or None
            
            student.guardian_name = form.guardian_name.data.strip()
            student.guardian_cnic = form.guardian_cnic.data.strip()
            
            # Update registration number if provided
            if form.registration_number.data and form.registration_number.data.strip():
                student.registration_number = form.registration_number.data.strip()
            
            # Update status if provided
            if form.status.data:
                student.status = form.status.data
            
            # Update admission date if provided
            if form.admission_date.data:
                student.admission_date = form.admission_date.data
            
            # Handle photo upload
            if form.photo.data:
                if student.photo_path:
                    delete_upload_file(student.photo_path)
                photo_file = form.photo.data
                photo_path = save_upload_file(photo_file, folder='students')
                student.photo_path = photo_path
            
            # Update course enrollments if provided
            if form.course_id.data:
                # Get current course IDs
                current_course_ids = {e.course_id for e in student.enrollments}
                new_course_ids = set(form.course_id.data)
                
                # Remove enrollments not in new list
                for enrollment in list(student.enrollments):
                    if enrollment.course_id not in new_course_ids:
                        db.session.delete(enrollment)
                
                # Add new enrollments
                for course_id in new_course_ids:
                    if course_id not in current_course_ids:
                        course = Course.query.get(course_id)
                        if course:
                            enrollment = Enrollment(
                                student_id=student.id,
                                course_id=course_id,
                                enroll_date=datetime.utcnow()
                            )
                            db.session.add(enrollment)
            
            db.session.commit()
            flash(f'Student {student.full_name} updated successfully!', 'success')
            return redirect(url_for('students.view_student', student_id=student.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'danger')
    
    elif request.method == 'GET':
        form.first_name.data = student.first_name
        form.last_name.data = student.last_name
        form.gender.data = student.gender
        form.date_of_birth.data = student.date_of_birth
        form.phone.data = student.phone
        form.address.data = student.address
        form.city.data = student.city
        form.admission_type.data = student.admission_type
        form.category.data = student.category
        form.cnic.data = student.cnic
        form.blood_group.data = student.blood_group or ''
        form.nationality.data = student.nationality
        form.emergency_contact.data = student.emergency_contact or ''
        form.permanent_address.data = student.permanent_address
        form.last_qualification.data = student.last_qualification or ''
        form.current_qualification.data = student.current_qualification or ''
        form.guardian_name.data = student.guardian_name or ''
        form.guardian_cnic.data = student.guardian_cnic or ''
        form.status.data = student.status
        form.admission_date.data = student.admission_date
        # Pre-populate courses with current enrollments
        form.course_id.data = [e.course_id for e in student.enrollments]
    
    return render_template('student_form.html', form=form, courses=courses, student=student, is_edit=True)


@students_bp.route('/<int:student_id>/delete', methods=['POST'])
@admin_required
def delete_student(student_id):
    """Delete student"""
    student = Student.query.get_or_404(student_id)
    
    try:
        # Delete photo if exists
        if student.photo_path:
            delete_upload_file(student.photo_path)
        
        # Delete enrollments
        Enrollment.query.filter_by(student_id=student.id).delete()
        
        # Delete student
        db.session.delete(student)
        db.session.commit()
        
        flash('Student deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    
    return redirect(url_for('students.list_students'))


@students_bp.route('/api/students')
@login_required
def api_students():
    """API endpoint for students data"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Student.query
    
    if search:
        query = query.filter(
            db.or_(
                Student.first_name.ilike(f'%{search}%'),
                Student.last_name.ilike(f'%{search}%'),
                Student.cnic.ilike(f'%{search}%')
            )
        )
    
    paginated_items, total, pages = paginate_query(query, page, per_page=20)
    
    students_data = [{
        'id': student.id,
        'name': student.full_name,
        'gender': student.gender,
        'phone': student.phone,
        'cnic': student.cnic,
        'admission_type': student.admission_type,
        'status': student.status,
        'courses': len(student.enrollments)
    } for student in paginated_items]
    
    return jsonify({
        'success': True,
        'students': students_data,
        'page': page,
        'pages': pages,
        'total': total
    })


@students_bp.route('/bulk-upload', methods=['GET', 'POST'])
@admin_required
def bulk_upload():
    """Bulk upload students from CSV"""
    return render_template('bulk_upload.html')


@students_bp.route('/<int:student_id>/status', methods=['POST'])
@admin_required
def update_student_status(student_id):
    """Update student status (active, inactive, graduated, leave)"""
    student = Student.query.get_or_404(student_id)
    
    # Get status from form data or request args
    new_status = request.form.get('status') or request.args.get('status')
    
    if not new_status or new_status not in ['active', 'inactive', 'graduated', 'leave']:
        flash('Invalid status provided.', 'error')
        return redirect(url_for('students.view_student', student_id=student_id))
    
    old_status = student.status
    student.status = new_status
    student.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        
        # Status-specific messages
        status_messages = {
            'active': 'Student marked as Active',
            'inactive': 'Student marked as Inactive',
            'graduated': 'Student marked as Graduated',
            'leave': 'Student marked as On Leave'
        }
        
        flash(f"✓ {status_messages.get(new_status, 'Status updated')} (from: {old_status})", 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating student status: {str(e)}', 'error')
    
    return redirect(url_for('students.view_student', student_id=student_id))

