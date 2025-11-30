"""
Course CRUD routes.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file
from flask_login import login_required
from datetime import datetime

from app.models import db, Course
from app.forms import CourseForm
from app.decorators import admin_required
from app.utils import save_upload_file, delete_upload_file

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')


# ============================================================================
# GUEST ROUTES (No Authentication Required)
# ============================================================================

@courses_bp.route('/guest/browse', methods=['GET'])
def guest_browse_courses():
    """Guest view: Browse all courses without authentication"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Course.query
    
    # Search filter
    if search:
        query = query.filter(
            db.or_(
                Course.name.ilike(f'%{search}%'),
                Course.description.ilike(f'%{search}%'),
                Course.instructor_name.ilike(f'%{search}%')
            )
        )
    
    # Sort by name
    query = query.order_by(Course.name)
    
    # Paginate
    paginated = query.paginate(page=page, per_page=12)
    courses = paginated.items
    total = paginated.total
    pages = paginated.pages
    
    return render_template('guest_courses.html', courses=courses, page=page, pages=pages, 
                          total=total, search=search)


@courses_bp.route('/guest/view/<int:course_id>', methods=['GET'])
def guest_view_course(course_id):
    """Guest view: View course details without authentication"""
    course = Course.query.get_or_404(course_id)
    return render_template('guest_course_detail.html', course=course)


@courses_bp.route('/guest/<int:course_id>/outline/download')
def guest_download_outline(course_id):
    """Guest download: Download course outline PDF without authentication"""
    try:
        import os
        from flask import current_app
        
        course = Course.query.get_or_404(course_id)
        
        if not course.course_outline_path:
            flash('No course outline available for download.', 'warning')
            return redirect(url_for('courses.guest_view_course', course_id=course.id))
        
        # Build the full file path
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], course.course_outline_path)
        
        # Normalize the path
        file_path = os.path.normpath(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            flash(f'Course outline file not found.', 'danger')
            return redirect(url_for('courses.guest_view_course', course_id=course.id))
        
        # Send file directly
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"{course.name.replace(' ', '_')}_Outline.pdf",
            mimetype='application/pdf'
        )
            
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('courses.guest_view_course', course_id=course_id))


# ============================================================================
# AUTHENTICATED ROUTES (Login Required)
# ============================================================================

@courses_bp.route('/')
@login_required
def list_courses():
    """List all courses"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Course.query
    
    # Search filter
    if search:
        query = query.filter(
            db.or_(
                Course.name.ilike(f'%{search}%'),
                Course.description.ilike(f'%{search}%'),
                Course.instructor_name.ilike(f'%{search}%')
            )
        )
    
    # Sort by name
    query = query.order_by(Course.name)
    
    # Paginate
    paginated = query.paginate(page=page, per_page=10)
    courses = paginated.items
    total = paginated.total
    pages = paginated.pages
    
    return render_template('courses.html', courses=courses, page=page, pages=pages, 
                          total=total, search=search)


@courses_bp.route('/view/<int:course_id>')
@login_required
def view_course(course_id):
    """View course details"""
    course = Course.query.get_or_404(course_id)
    return render_template('course_detail.html', course=course)


@courses_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    """Create new course"""
    form = CourseForm()
    
    if form.validate_on_submit():
        try:
            course = Course(
                name=form.name.data.strip(),
                description=form.description.data.strip() if form.description.data else None,
                instructor_name=form.instructor_name.data.strip() if form.instructor_name.data else None,
                instructor_contact=form.instructor_contact.data.strip() if form.instructor_contact.data else None,
                fee=form.fee.data,
                seats=form.seats.data
            )
            
            # Handle course outline upload
            if form.course_outline.data:
                outline_file = form.course_outline.data
                outline_path = save_upload_file(outline_file, folder='courses')
                course.course_outline_path = outline_path
            
            db.session.add(course)
            db.session.commit()
            flash(f'Course "{course.name}" created successfully!', 'success')
            return redirect(url_for('courses.view_course', course_id=course.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating course: {str(e)}', 'danger')
    
    return render_template('course_form.html', form=form, is_new=True)


@courses_bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    """Edit course"""
    course = Course.query.get_or_404(course_id)
    form = CourseForm()
    
    if form.validate_on_submit():
        try:
            course.name = form.name.data.strip()
            course.description = form.description.data.strip() if form.description.data else None
            course.instructor_name = form.instructor_name.data.strip() if form.instructor_name.data else None
            course.instructor_contact = form.instructor_contact.data.strip() if form.instructor_contact.data else None
            course.fee = form.fee.data
            course.seats = form.seats.data
            course.updated_at = datetime.utcnow()
            
            # Handle course outline upload
            if form.course_outline.data:
                if course.course_outline_path:
                    delete_upload_file(course.course_outline_path)
                outline_file = form.course_outline.data
                outline_path = save_upload_file(outline_file, folder='courses')
                course.course_outline_path = outline_path
            
            db.session.commit()
            flash(f'Course "{course.name}" updated successfully!', 'success')
            return redirect(url_for('courses.view_course', course_id=course.id))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating course: {str(e)}', 'danger')
    
    elif request.method == 'GET':
        form.name.data = course.name
        form.description.data = course.description or ''
        form.instructor_name.data = course.instructor_name or ''
        form.instructor_contact.data = course.instructor_contact or ''
        form.fee.data = course.fee
        form.seats.data = course.seats
    
    return render_template('course_form.html', form=form, course=course, is_edit=True)


@courses_bp.route('/<int:course_id>/delete', methods=['POST'])
@admin_required
def delete_course(course_id):
    """Delete course"""
    course = Course.query.get_or_404(course_id)
    
    try:
        # Delete course outline if exists
        if course.course_outline_path:
            delete_upload_file(course.course_outline_path)
        
        # Delete course (cascades will handle related records)
        db.session.delete(course)
        db.session.commit()
        flash(f'Course "{course.name}" deleted successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting course: {str(e)}', 'danger')
    
    return redirect(url_for('courses.list_courses'))


@courses_bp.route('/<int:course_id>/outline/download')
@login_required
def download_outline(course_id):
    """Download course outline PDF"""
    try:
        import os
        from flask import current_app
        
        course = Course.query.get_or_404(course_id)
        
        if not course.course_outline_path:
            flash('No course outline available for download.', 'warning')
            return redirect(url_for('courses.view_course', course_id=course.id))
        
        # Build the full file path
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], course.course_outline_path)
        
        # Normalize the path
        file_path = os.path.normpath(file_path)
        
        # Check if file exists
        if not os.path.exists(file_path):
            flash(f'Course outline file not found.', 'danger')
            return redirect(url_for('courses.view_course', course_id=course.id))
        
        # Send file directly
        return send_file(
            file_path,
            as_attachment=True,
            download_name=f"{course.name.replace(' ', '_')}_Outline.pdf",
            mimetype='application/pdf'
        )
            
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'danger')
        return redirect(url_for('courses.view_course', course_id=course_id))
