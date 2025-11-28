"""
Attendance marking routes.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required

from app.models import db, Attendance, Course
from app.decorators import teacher_required

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')


@attendance_bp.route('/')
@teacher_required
def mark_attendance():
    """Mark attendance for students in a course"""
    return render_template('attendance.html')


@attendance_bp.route('/report')
@login_required
def attendance_report():
    """View attendance report"""
    return render_template('attendance_report.html')
