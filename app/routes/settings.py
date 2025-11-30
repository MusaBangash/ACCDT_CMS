"""
Settings and configuration routes.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from app.models import db, Setting
from app.decorators import admin_required

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')


@settings_bp.route('/')
@admin_required
def index():
    """Settings management page"""
    # Get current settings
    reg_prefix = Setting.get('reg_number_prefix', 'ACCDT')
    reg_format = Setting.get('reg_number_format', '{prefix}-{year}-{count:05d}')
    school_name = Setting.get('school_name', 'ACCDT')
    
    return render_template('settings.html', 
                          reg_prefix=reg_prefix,
                          reg_format=reg_format,
                          school_name=school_name)


@settings_bp.route('/registration', methods=['POST'])
@admin_required
def update_registration_settings():
    """Update registration number settings"""
    try:
        prefix = request.form.get('reg_prefix', 'ACCDT').strip().upper()
        
        # Validate prefix (alphanumeric, max 10 chars)
        if not prefix or len(prefix) > 10 or not prefix.replace('_', '').isalnum():
            flash('Invalid prefix. Use alphanumeric characters only (max 10 chars).', 'error')
            return redirect(url_for('settings.index'))
        
        # Update settings
        Setting.set('reg_number_prefix', prefix, 'Registration number prefix')
        
        flash(f'✓ Registration prefix updated to: {prefix}', 'success')
    except Exception as e:
        flash(f'Error updating settings: {str(e)}', 'error')
    
    return redirect(url_for('settings.index'))


@settings_bp.route('/school-info', methods=['POST'])
@admin_required
def update_school_info():
    """Update school information"""
    try:
        school_name = request.form.get('school_name', 'ACCDT').strip()
        
        if not school_name or len(school_name) > 100:
            flash('Invalid school name.', 'error')
            return redirect(url_for('settings.index'))
        
        Setting.set('school_name', school_name, 'School name')
        
        flash(f'✓ School name updated to: {school_name}', 'success')
    except Exception as e:
        flash(f'Error updating school info: {str(e)}', 'error')
    
    return redirect(url_for('settings.index'))
