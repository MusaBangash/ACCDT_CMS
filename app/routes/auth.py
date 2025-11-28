"""
Authentication routes: login, logout, and admin registration.
"""

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import func

from app.models import db, User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False)
        
        # Validate input
        if not username or not password:
            flash('Username and password are required.', 'warning')
            return redirect(url_for('auth.login'))
        
        # Check user credentials
        user = User.query.filter_by(username=username).first()
        
        if user is None or not user.check_password(password):
            flash('Invalid username or password.', 'danger')
            return redirect(url_for('auth.login'))
        
        if not user.is_active:
            flash('This account has been disabled.', 'danger')
            return redirect(url_for('auth.login'))
        
        # Login user
        login_user(user, remember=remember)
        
        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        
        flash(f'Welcome, {user.username}!', 'success')
        return redirect(url_for('dashboard.index'))
    
    return render_template('login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    username = current_user.username
    logout_user()
    flash(f'{username} logged out successfully.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register-admin', methods=['GET', 'POST'])
def register_admin():
    """
    Register first admin user (only if no users exist).
    This endpoint is accessible only when the database is empty.
    """
    # Check if any admin already exists
    admin_exists = User.query.filter_by(role='admin').first() is not None
    user_count = db.session.query(func.count(User.id)).scalar()
    
    if user_count > 0 and admin_exists:
        flash('An admin already exists. Contact system administrator.', 'danger')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # Validation
        if not username or len(username) < 3:
            flash('Username must be at least 3 characters.', 'warning')
            return redirect(url_for('auth.register_admin'))
        
        if not password or len(password) < 6:
            flash('Password must be at least 6 characters.', 'warning')
            return redirect(url_for('auth.register_admin'))
        
        if password != password_confirm:
            flash('Passwords do not match.', 'warning')
            return redirect(url_for('auth.register_admin'))
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'warning')
            return redirect(url_for('auth.register_admin'))
        
        # Create admin user
        admin = User(
            username=username,
            email=email if email else None,
            role='admin'
        )
        admin.set_password(password)
        
        try:
            db.session.add(admin)
            db.session.commit()
            flash('Admin user created successfully! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating admin: {str(e)}', 'danger')
            return redirect(url_for('auth.register_admin'))
    
    return render_template('register_admin.html', user_count=user_count)
