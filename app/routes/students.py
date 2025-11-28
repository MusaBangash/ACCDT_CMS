"""
Student CRUD routes and bulk upload.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from app.models import db, Student
from app.decorators import admin_required, roles_required

students_bp = Blueprint('students', __name__, url_prefix='/students')


@students_bp.route('/')
@login_required
def list_students():
    """List all students"""
    return render_template('students.html')


@students_bp.route('/create', methods=['GET', 'POST'])
@roles_required('admin')
def create_student():
    """Create new student"""
    return render_template('student_form.html')


@students_bp.route('/<int:student_id>')
@login_required
def view_student(student_id):
    """View student details"""
    student = Student.query.get_or_404(student_id)
    return render_template('student_detail.html', student=student)


@students_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
@roles_required('admin')
def edit_student(student_id):
    """Edit student details"""
    student = Student.query.get_or_404(student_id)
    return render_template('student_form.html', student=student)


@students_bp.route('/<int:student_id>/delete', methods=['POST'])
@admin_required
def delete_student(student_id):
    """Delete student"""
    student = Student.query.get_or_404(student_id)
    return redirect(url_for('students.list_students'))


@students_bp.route('/bulk-upload', methods=['GET', 'POST'])
@admin_required
def bulk_upload():
    """Bulk upload students from CSV"""
    return render_template('bulk_upload.html')
