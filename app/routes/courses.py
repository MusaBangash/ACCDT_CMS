"""
Course CRUD routes.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from app.models import db, Course
from app.decorators import admin_required

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')


@courses_bp.route('/')
@login_required
def list_courses():
    """List all courses"""
    return render_template('courses.html')


@courses_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    """Create new course"""
    return render_template('course_form.html')


@courses_bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_course(course_id):
    """Edit course"""
    course = Course.query.get_or_404(course_id)
    return render_template('course_form.html', course=course)


@courses_bp.route('/<int:course_id>/delete', methods=['POST'])
@admin_required
def delete_course(course_id):
    """Delete course"""
    course = Course.query.get_or_404(course_id)
    return redirect(url_for('courses.list_courses'))
